"""Reference helper: curve-form comparison for flood_real_estate model v0.1 / docs r1.

Reproduces the Plymouth trial fit-catalogue method (Hazard_Modeling feature/plymouth_trial @ 09b95acb,
06_damage_curve_catalog): anchored logistic / Richards / Weibull fits, linear and PCHIP interpolants,
leave-one-out RMSE over interior knots, monotone and range gates, and the catalogue 10% rule.

Usage:
    python flood_real_estate_form_comparison.py <haz_fl_dept.csv> <output_dir>

haz_fl_dept.csv is the Pollack (2023) Zenodo compilation, DOI 10.5281/zenodo.10027236
(sha256 863397b877aa7022d17239d527e0ea264dd9fd6431d3b6facdfbaa4add3b94a8). NACCS knots are transcribed from
the 2015 report Tables 25, 35 and 56. Writes form_comparison.csv and the candidate-curves chart.
Requires numpy, scipy, matplotlib. Not a stable src API.
"""
import csv, json, sys, warnings
import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.optimize import curve_fit
warnings.filterwarnings("ignore")
haz_csv, out = sys.argv[1], sys.argv[2]

# ---- curves: Hazus defaults (structure rows) and NACCS published knots ------------------------------
cols = ["ft04m","ft03m","ft02m","ft01m"] + [f"ft{d:02d}" for d in range(0,25)]
H = {int(x["DmgFnId"]): x for x in csv.DictReader(open(haz_csv, encoding="utf-8-sig")) if x["Source_Table"] == "flBldgStructDmgFn"}
dh = np.arange(-4, 25, dtype=float)
nd = np.array([-1, -0.5, 0, 0.5, 1, 2, 3, 5, 7, 10], float)
NACCS = {  # report Tables 56, 25, 35
 "RES1-1SNB": {"Min":[0,0,0,6,10,16,20,30,42,55],"ML":[0,0,1,10,18,28,33,42,55,65],"Max":[0,5,10,20,30,40,45,60,94,100]},
 "COM-ENG":   {"Min":[0,0,0,5,12,18,28,33,43,48],"ML":[0,0,5,10,20,30,35,40,53,58],"Max":[0,0,9,17,27,36,43,48,60,69]},
 "COM-PRE":   {"Min":[0,0,0,5,10,15,20,28,35,40],"ML":[0,0,5,12,20,28,35,45,55,60],"Max":[0,10,15,20,30,42,55,65,75,78]},
}
CURVES = []
for b, df in [("house", 129), ("commercial", 217), ("warehouse", 341)]:
    CURVES.append((b, "freshwater", f"Hazus DF {df}", "-", dh, np.array([float(H[df][c]) for c in cols])))
for b, k in [("house", "RES1-1SNB"), ("commercial", "COM-ENG"), ("warehouse", "COM-PRE")]:
    for band in ("ML", "Min", "Max"):
        CURVES.append((b, "coastal", f"NACCS {k}", band, nd, np.array(NACCS[k][band], float)))

# ---- fit families (same forms as the Plymouth catalogue) --------------------------------------------
def f_log(d, Dmax, k, m, d0):
    s = 1/(1+np.exp(-np.clip(k*(d-m), -500, 500))); return Dmax*s*(-np.expm1(-k*np.maximum(d-d0, 0)))
def f_ric(d, Dmax, k, m, nu, d0):
    nu = max(nu, 1e-3); lr = lambda x: -np.log1p(nu*np.exp(np.clip(-x, -500, 500)))/nu
    la, lb = lr(k*(np.maximum(d, d0)-m)), lr(k*(d0-m))
    return np.where(d >= d0, Dmax*np.exp(lb)*np.expm1(la-lb)/max(float(-np.expm1(lb)), 1e-300), 0.0)
def f_wei(d, Dmax, lam, kap, d0):
    x = np.clip((d-d0)/max(lam, 1e-6), 0, None); return Dmax*(1-np.exp(-np.power(x, max(kap, 1e-6))))
FAM = {"logistic": f_log, "richards": f_ric, "weibull": f_wei}
def anchor(d, v):
    z = d[v == 0]; return float(z.max()) if z.size else None
def fit(kind, d, v):
    lo, hi = d.min(), d.max()
    if kind == "linear": return lambda x: np.interp(x, d, v)
    if kind == "pchip":
        p = PchipInterpolator(d, v, extrapolate=False); return lambda x: p(np.clip(x, lo, hi))
    d0 = anchor(d, v)
    if d0 is None: return None
    P = max(v.max(), 1.0); fn = FAM[kind]; m_ = d > d0; dd, vv = d[m_], v[m_]; f = lambda x, *p: fn(x, *p, d0)
    if kind == "logistic": starts = [[.95*P, k0, float(np.median(dd))] for k0 in (.3, 1)]; bnd = ([1e-6, 1e-3, dd.min()-20], [P, 10, dd.max()+20])
    elif kind == "richards": starts = [[.95*P, k0, float(np.median(dd)), 1] for k0 in (.3, 1)]; bnd = ([1e-6, 1e-3, dd.min()-20, 1e-3], [P, 10, dd.max()+20, 20])
    else: starts = [[.95*P, max((dd.max()-d0)/2, .5), k0] for k0 in (1, 2)]; bnd = ([1e-6, 1e-3, 1e-3], [P, 500, 20])
    best = (None, np.inf)
    for p0 in starts:
        try: popt, _ = curve_fit(f, dd, vv, p0=p0, bounds=bnd, maxfev=60000)
        except Exception: continue
        sse = float(np.sum((f(d, *popt)-v)**2))
        if sse < best[1]: best = (popt, sse)
    if best[0] is None: return None
    return (lambda x, p=best[0]: fn(np.asarray(x, float), *p, d0))

rows, preds = [], {}
for b, w, src, band, d, v in CURVES:
    res = {}
    for kind in ["linear", "pchip", "logistic", "richards", "weibull"]:
        pr = fit(kind, d, v)
        if pr is None: continue
        errs = []
        for i in range(1, len(d)-1):
            k = np.ones(len(d), bool); k[i] = False
            p2 = fit(kind, d[k], v[k])
            if p2 is not None: errs.append(float(p2(np.array([d[i]]))[0]-v[i]))
        loocv = float(np.sqrt(np.mean(np.square(errs))))
        g = np.linspace(d.min(), d.max(), 3001); y = np.asarray(pr(g), float)
        mono = int(np.sum(np.diff(y) < -1e-9)); oor = int(np.sum((y < -1e-9) | (y > v.max()+1e-9)))
        knot_rmse = float(np.sqrt(np.mean((np.asarray(pr(d), float)-v)**2)))
        knot_max = float(np.max(np.abs(np.asarray(pr(d), float)-v)))
        maxdiff_lin = float(np.max(np.abs(y-np.interp(g, d, v))))
        res[kind] = dict(loocv=loocv, gates="PASS" if mono == 0 and oor == 0 else "FAIL", knot_rmse=knot_rmse, knot_max=knot_max, maxdiff_lin=maxdiff_lin)
        preds[(b, w, band, kind)] = pr
    knot_exact = min(("linear", "pchip"), key=lambda k: res[k]["loocv"] if res[k]["gates"] == "PASS" else 1e9)
    smooth = [k for k in ("logistic", "richards", "weibull") if k in res and res[k]["gates"] == "PASS"]
    best_s = min(smooth, key=lambda k: res[k]["loocv"]) if smooth else None
    rule = best_s if best_s and res[best_s]["loocv"] <= 0.9*res[knot_exact]["loocv"] else knot_exact
    for kind, r in res.items():
        rows.append(dict(building=b, water=w, source=src, band=band, form=kind, LOOCV_RMSE_pts=round(r["loocv"], 2), gates=r["gates"],
                         RMSE_at_published_knots=round(r["knot_rmse"], 2), max_miss_at_published_knot=round(r["knot_max"], 2),
                         max_diff_from_linear_pts=round(r["maxdiff_lin"], 2), best_smooth=(kind == best_s), catalogue_rule_pick=(kind == rule)))
    print(f"{b:10} {w:10} {src:16} {band:3} | linear {res['linear']['loocv']:5.2f} pchip {res['pchip']['loocv']:5.2f} | best smooth {best_s} {res[best_s]['loocv'] if best_s else float('nan'):5.2f} "
          f"(misses a published value by up to {res[best_s]['knot_max'] if best_s else float('nan'):4.1f} pts; differs from linear by up to {res[best_s]['maxdiff_lin'] if best_s else float('nan'):4.1f}) | 10%-rule -> {rule}")
with open(f"{out}/form_comparison.csv", "w", newline="") as fh:
    w_ = csv.DictWriter(fh, fieldnames=list(rows[0])); w_.writeheader(); w_.writerows(rows)

# ---- chart -----------------------------------------------------------------------------------------
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 3, figsize=(15, 4.6), sharey=True)
for ax, b in zip(axes, ["house", "commercial", "warehouse"]):
    for (bb, w, src, band, d, v) in CURVES:
        if bb != b: continue
        col = "#2563eb" if w == "freshwater" else "#ea580c"
        if band in ("Min", "Max"):
            g = np.linspace(d.min(), d.max(), 400); ax.plot(g, np.interp(g, d, v), color=col, lw=0.8, ls=":", alpha=0.8)
            continue
        g = np.linspace(d.min(), d.max(), 800)
        ax.plot(g, np.interp(g, d, v), color=col, lw=2.0, label=f"{src} ({w}) — straight lines")
        bs = next(r["form"] for r in rows if r["building"] == b and r["water"] == w and r["band"] == band and r["best_smooth"])
        ax.plot(g, preds[(b, w, band, bs)](g), color=col, lw=1.3, ls="--", label=f"{src} — best smooth fit ({bs})")
        ax.plot(d, v, "o", ms=4, mfc="white", mec=col)
    ax.set_title(f"{b}  (dotted: NACCS low / high)"); ax.set_xlabel("water depth above first floor (ft)"); ax.grid(alpha=.3); ax.set_xlim(-4, 24)
    ax.legend(fontsize=7, loc="lower right")
axes[0].set_ylabel("damage, % of structure replacement cost")
fig.suptitle("flood_real_estate v0.1 — proposed curves: straight lines between published points vs best smooth fit", fontsize=11)
fig.tight_layout(); fig.savefig(f"{out}/flood_real_estate_v0_1_candidate_curves.png", dpi=130)
print("wrote", out)
