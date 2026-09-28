"""Figures du 09 (diagnostic). Lit les tables de data/analysis/09_diagnostic/ et 08_priorisation/, écrit des PNG dans figures/.

F1 : carte d'identité des 10 préfectures (rang défavorable parmi les préfectures, rampe séquentielle bleue).
F2 : carte des communes signalées (palette de statuts validée), préfectures en gris selon leur classe du 08.
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import geopandas as gpd  # noqa: E402
import matplotlib.patheffects as pe  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "prep"))
from commun import CRS_SURFACE, GEO  # noqa: E402

A = Path(__file__).resolve().parents[1] / "data" / "analysis"
ICI, SC = A / "09_diagnostic", A / "08_priorisation"
FIG = ICI / "figures"
FIG.mkdir(parents=True, exist_ok=True)

SURFACE, INK, INK2, MUTED, GRID, AXE = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
BLEUS = ["#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]
SIGNAL = {"sans point formel et cellule critique": "#e34948", "sans point formel": "#eda100", "cellule critique": "#4a3aa7"}
plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "font.family": "sans-serif", "font.size": 9.5, "text.color": INK, "axes.labelcolor": INK2,
    "axes.edgecolor": AXE, "xtick.color": MUTED, "ytick.color": MUTED, "legend.frameon": False,
    "axes.titlesize": 10.5, "axes.titleweight": "bold", "axes.titlelocation": "left", "axes.titlecolor": INK})


def lire(d, nom):
    return pd.read_csv(d / f"{nom}.csv")


def fr(x, d=1):
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",")


def finir(fig, nom, source, y=-0.005):
    fig.text(0.01, y, source, color=MUTED, fontsize=7.5, ha="left", va="top")
    fig.savefig(FIG / f"{nom}.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


# =============================================================== F1 — Carte d'identité des 10 préfectures
sc = lire(SC, "score_prefectures").set_index("code")
fi = lire(ICI, "fiches_prefectures").set_index("code")
# Rangs défavorables des dimensions parmi les 39 (D3 : parmi les 36 où elle est déterminable)
for d in ("D1", "D2", "D3"):
    x = sc[d].fillna(np.inf) if d == "D1" else sc[d]  # D1 vide = 0 point formel = le plus défavorable
    r = x.rank(method="average")
    fi[f"{d}_rang_defavorable"] = (100 * (r - 1) / (x.notna().sum() - 1)).reindex(fi.index)
    fi[f"{d}_val"] = sc[d].reindex(fi.index)
COLS = [("D1", "habitants par\npoint formel", lambda v: "aucun point" if pd.isna(v) else fr(v, 0)),
        ("D2", "habitants par point\nmobile money", lambda v: fr(v, 0)),
        ("D3", "hors couverture\n(proxy, %)", lambda v: "non\ndéterminable" if pd.isna(v) else fr(v)),
        ("part_urbaine_pct", "population\nurbaine (%)", fr),
        ("densite_hab_km2", "habitants\npar km²", lambda v: fr(v, 0)),
        ("types_formels_presents", "types formels\nprésents\n(sur 4)", lambda v: fr(v, 0)),
        ("banques_pour_10k_adultes", "agences\nbancaires pour\n10 000 adultes", lambda v: fr(v, 2)),
        ("concentration_points_formels_pts", "concentration\ndes points\nformels", lambda v: "—" if pd.isna(v) else f"{fr(v, 0)} pts"),
        ("part_points_mm_plus_10km_guichet_pct", "mobile money\nà plus de 10 km\nd'un guichet (%)", lambda v: fr(v, 0)),
        ("part_points_mm_togocom_seul_pct", "mobile money\nTogocom\nseul (%)", lambda v: fr(v, 0)),
        ("part_points_mm_deux_operateurs_pct", "mobile money\ndeux\nopérateurs (%)", lambda v: fr(v, 0)),
        ("pct_hab_5km_agence_togocom", "à moins de 5 km\nd'une agence\nTogocom (%)", lambda v: fr(v, 0)),
        ("km_fibre_enterree", "fibre enterrée\n(km)", lambda v: fr(v, 0))]
nrow, ncol = len(fi), len(COLS)
fig, ax = plt.subplots(figsize=(15.5, 6.6))
for j, (c, lab, fmt) in enumerate(COLS):
    rc = f"{c}_rang_defavorable"
    for i, (code, r) in enumerate(fi.iterrows()):
        rg = r[rc]
        col = SURFACE if pd.isna(rg) else BLEUS[min(int(rg // 20), 4)]
        ax.add_patch(plt.Rectangle((j, i), 1, 1, facecolor=col, edgecolor=SURFACE, linewidth=2))
        v = r[f"{c}_val"] if c in ("D1", "D2", "D3") else r[c]
        ax.text(j + 0.5, i + 0.5, fmt(v), ha="center", va="center", fontsize=7.6,
                color=SURFACE if (not pd.isna(rg) and rg >= 60) else INK)
    ax.text(j + 0.5, -0.12, lab, ha="center", va="bottom", fontsize=7.2, color=INK2)
ax.axvline(3, color=INK2, linewidth=1.2)
ax.axhline(7, color=INK2, linewidth=1.2)
ax.set_xlim(0, ncol)
ax.set_ylim(nrow, -1.55)
ax.set_yticks(np.arange(nrow) + 0.5)
ax.set_yticklabels([f"{r.nom}  ({'non classée' if code in sc.index[sc.classe_retenue.str.startswith('non')] else 'priorité 1'})"
                    for code, r in fi.iterrows()], fontsize=8.4, color=INK)
ax.set_xticks([])
ax.tick_params(length=0)
for s_ in ax.spines.values():
    s_.set_visible(False)
ax.text(1.5, -1.5, "Dimensions du score", ha="center", fontsize=8.4, fontweight="bold", color=INK)
ax.text(8, -1.5, "Facteurs associés (contexte, pas des causes)", ha="center", fontsize=8.4, fontweight="bold", color=INK)
h = [Patch(color=c, label=l) for c, l in zip(BLEUS, ["0 à 20", "20 à 40", "40 à 60", "60 à 80", "80 à 100 (le plus défavorable)"])]
h.append(Patch(facecolor=SURFACE, edgecolor=AXE, label="non déterminable"))
ax.legend(handles=h, loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=6, fontsize=7.6,
          title="Rang défavorable parmi les préfectures (39 ; 36 pour la couverture)", title_fontsize=7.8)
fig.suptitle("Diagnostic : les 10 préfectures à regarder en premier, dimension par dimension", x=0.01, ha="left",
             fontsize=11.5, fontweight="bold")
finir(fig, "f1_carte_identite", "Couleur : position de la préfecture parmi toutes les préfectures, du côté défavorable (foncé = parmi les plus défavorables). "
      "Concentration : part des points formels dans la commune la mieux dotée,\nmoins sa part de la population. Tables : fiches_prefectures.csv ; score_prefectures.csv (08)", y=0.02)

# =============================================================== F2 — Carte des communes signalées
sig = lire(ICI, "communes_signalees").reset_index(drop=True)
sig["numero"] = np.arange(1, len(sig) + 1)
gc = gpd.read_file(GEO / "communes.geojson").to_crs(CRS_SURFACE)
gp = gpd.read_file(GEO / "prefectures.geojson").to_crs(CRS_SURFACE).merge(sc[["classe_retenue"]].reset_index(), on="code")
GRIS = {"priorité 1": "#c3c2b7", "priorité 2": "#e1e0d9", "priorité 3": "#f3f2ee"}
fig = plt.figure(figsize=(11, 9.2))
ax = fig.add_axes([0.0, 0.08, 0.52, 0.86])
for k, c in GRIS.items():
    gp[gp.classe_retenue == k].plot(ax=ax, color=c, edgecolor=SURFACE, linewidth=0.6)
gp[gp.classe_retenue.str.startswith("non")].plot(ax=ax, facecolor=SURFACE, edgecolor=MUTED, hatch="////", linewidth=0.6)
g = gc.merge(sig[["code", "signal", "numero"]], on="code")
for k, c in SIGNAL.items():
    g[g.signal == k].plot(ax=ax, color=c, edgecolor=SURFACE, linewidth=0.5)
gp.boundary.plot(ax=ax, color=INK2, linewidth=0.45)
for r in g.itertuples():
    p = r.geometry.representative_point()
    ax.text(p.x, p.y, str(r.numero), fontsize=6.8, ha="center", va="center", color=INK, fontweight="bold",
            path_effects=[pe.withStroke(linewidth=2.2, foreground=SURFACE)])
ax.set_axis_off()
ax.set_aspect("equal")
h = [Patch(color=c, label=k) for k, c in SIGNAL.items()]
h += [Patch(color=c, label=f"préfecture en {k}") for k, c in GRIS.items()]
h.append(Patch(facecolor=SURFACE, edgecolor=MUTED, hatch="////", label="préfecture non classée"))
ax.legend(handles=h, loc="upper left", bbox_to_anchor=(0.0, 0.03), fontsize=7.4, ncol=3)
ax2 = fig.add_axes([0.54, 0.08, 0.45, 0.86])
ax2.set_axis_off()
y, cl0 = 1.0, None
for r in sig.itertuples():
    if r.classe_prefecture_08 != cl0:
        cl0 = r.classe_prefecture_08
        lab = "Préfectures non classées" if cl0.startswith("non") else f"Préfectures en {cl0}"
        y -= 0.012
        ax2.text(0, y, lab, fontsize=8, fontweight="bold", color=INK, va="top")
        y -= 0.034
    km = "" if pd.isna(r.km_guichet_le_plus_proche_mediane) else f" · guichet à {fr(r.km_guichet_le_plus_proche_mediane)} km"
    ax2.scatter(0.012, y - 0.008, s=34, marker="s", color=SIGNAL[r.signal])
    ax2.text(0.035, y, f"{r.numero}. {r.nom} ({fr(r.pop_totale, 0)} hab.){km}", fontsize=7.4, color=INK2, va="top")
    y -= 0.031
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
fig.suptitle("Les 25 communes signalées : sans point formel ou en cellule critique, toutes rurales", x=0.01, ha="left",
             fontsize=11.5, fontweight="bold")
finir(fig, "f2_communes_signalees", "Numéros : ordre de la table (classe de la préfecture, puis préfecture). Guichet : distance médiane des points mobile money de la commune "
      "au point formel le plus proche, à vol d'oiseau (06).\nCellule critique = à confirmer (couverture proxy). Tables : communes_signalees.csv ; score_prefectures.csv (08)", y=-0.01)
print(f"2 figures écrites dans {FIG}")
