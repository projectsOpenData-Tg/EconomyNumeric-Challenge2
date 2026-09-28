"""Figures du 08 (priorisation). Lit les tables de data/analysis/08_priorisation/ et écrit des PNG dans figures/.

Même style que les figures du 07. Classes de priorité en rampe séquentielle bleue (foncé = priorité 1) ;
dimensions en palette catégorielle validée (orange, vert, violet), la couverture en marqueur creux (proxy).
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
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "prep"))
from commun import CRS_SURFACE, GEO  # noqa: E402

ICI = Path(__file__).resolve().parents[1] / "data" / "analysis" / "08_priorisation"
FIG = ICI / "figures"
FIG.mkdir(parents=True, exist_ok=True)

SURFACE, INK, INK2, MUTED, GRID, AXE = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
CLASSE = {"priorité 1": "#0d366b", "priorité 2": "#3987e5", "priorité 3": "#cde2fb"}  # rampe BLEUS
ND = "#f0efec"
DIM = {"D1": ("accès formel (habitants par point formel)", "#eb6834", "o", True),
       "D2": ("maillage mobile money (habitants par point)", "#1baf7a", "s", True),
       "D3": ("couverture (part hors couverture, proxy)", "#4a3aa7", "D", False)}  # palette validée, mode clair
plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "font.family": "sans-serif", "font.size": 9.5, "text.color": INK, "axes.labelcolor": INK2,
    "axes.edgecolor": AXE, "axes.linewidth": 0.8, "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
    "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False,
    "axes.titlesize": 9.5, "axes.titleweight": "bold", "axes.titlelocation": "left", "axes.titlecolor": INK})


def lire(nom):
    return pd.read_csv(ICI / f"{nom}.csv")


def fr(x, d=1):
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",")


def finir(fig, nom, source, y=-0.005):
    fig.text(0.01, y, source, color=MUTED, fontsize=7.5, ha="left", va="top")
    fig.savefig(FIG / f"{nom}.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


s = lire("score_prefectures")
nd = s.classe_retenue.str.startswith("non")
s = pd.concat([s[~nd].sort_values("ordre_final"), s[nd].sort_values("sans_couv_score", ascending=False)]).reset_index(drop=True)
nd = s.classe_retenue.str.startswith("non")
n = len(s)
y = np.arange(n)

# =============================================================== F1 — Classement décomposé, robustesse et population
TESTS = [("classe_test_poids D1 doublé", "sans_couv_classe_test_poids D1 doublé", "D1\n×2"),
         ("classe_test_poids D2 doublé", "sans_couv_classe_test_poids D2 doublé", "D2\n×2"),
         ("classe_test_poids D3 doublé", None, "D3\n×2"),
         ("classe_test_min-max", "sans_couv_classe_test_min-max", "min-\nmax"),
         ("classe_test_min-max lu en rang (P13)", "sans_couv_classe_test_min-max lu en rang (P13)", "en\nrang*"),
         (None, None, "sans\nextrême"),
         ("sans_couv_classe", None, "sans\ncouv.")]
ext3 = [c for c in s if c.startswith("classe_test_sans ")][0]
ext2 = [c for c in s if c.startswith("sans_couv_classe_test_sans ")][0]

fig, axes = plt.subplots(1, 4, figsize=(13, 11.5), sharey=True, gridspec_kw={"width_ratios": [3.2, 2.2, 2.1, 1.3], "wspace": 0.08})
a0, a1, a2, a3 = axes
for ax in axes:
    ax.set_ylim(n - 0.4, -0.6)
    for yy in (s.index[s.classe_retenue.ne(s.classe_retenue.shift())][1:] - 0.5):
        ax.axhline(yy, color=INK2, linewidth=0.7)
a0.set_yticks(y)
a0.set_yticklabels([f"{r.nom}  ({r.unite_regionale})" if r.unite_regionale in ("Grand Lomé",) else r.nom for r in s.itertuples()], fontsize=8)
a0.tick_params(axis="y", length=0)

# A : rangs percentiles des dimensions
for d, (lab, col, m, plein) in DIM.items():
    v = s[f"{d}_rang_pct"].where(~nd, s.get(f"sans_couv_{d}_rang_pct"))
    a0.scatter(v, y, s=26, marker=m, facecolor=col if plein else SURFACE, edgecolor=col, linewidth=1.3, zorder=3, label=lab)
a0.set_xlim(-4, 104)
a0.set_xticks([0, 25, 50, 75, 100])
a0.set_title("Rang percentile par dimension\n(100 = la préfecture la plus mal servie)")
a0.grid(axis="y", visible=False)

# B : score et classe
for i, r in s.iterrows():
    if r.classe_retenue.startswith("non"):
        a1.barh(i, r.sans_couv_score, height=0.62, color=ND, edgecolor=MUTED, hatch="////", linewidth=0.6)
        a1.text(r.sans_couv_score + 1.5, i, f"{fr(r.sans_couv_score)} (2 dim.)", va="center", fontsize=7.2, color=INK2)
    else:
        a1.barh(i, r.score, height=0.62, color=CLASSE[r.classe_retenue])
        a1.text(r.score + 1.5, i, fr(r.score), va="center", fontsize=7.2, color=INK2)
for x in (40, 70):
    a1.axvline(x, color=INK2, linewidth=0.8, linestyle=(0, (3, 2)))
a1.set_xlim(0, 142)
a1.set_xticks([0, 40, 70, 100])
a1.set_title("Score (moyenne des rangs)\nseuils du 02 : 40 et 70")
a1.grid(axis="y", visible=False)

# C : classe sous chaque test
for j, (c3, c2, lab) in enumerate(TESTS):
    for i, r in s.iterrows():
        est_nd = r.classe_retenue.startswith("non")
        if lab.startswith("sans\nextr"):
            col = r[ext2] if est_nd else r[ext3]
        elif lab.startswith("sans\ncouv"):
            col = r[c3] if not est_nd else None
        else:
            col = r[c2] if (est_nd and c2) else (None if est_nd else r[c3])
        base = r.sans_couv_classe if est_nd else r.classe_retenue
        if isinstance(col, str):
            a2.add_patch(plt.Rectangle((j - 0.4, i - 0.36), 0.8, 0.72, facecolor=CLASSE[col], edgecolor=SURFACE))
            if col != base:
                a2.text(j, i, "×", ha="center", va="center", fontsize=8, fontweight="bold",
                        color=SURFACE if col != "priorité 3" else INK)
        else:
            a2.text(j, i, "–", ha="center", va="center", fontsize=8, color=MUTED)
a2.set_xlim(-0.6, len(TESTS) - 0.4)
a2.set_xticks(range(len(TESTS)))
a2.set_xticklabels([t[2] for t in TESTS], fontsize=6.8)
a2.xaxis.tick_top()
a2.tick_params(axis="x", length=0)
a2.grid(False)
a2.spines[["left", "bottom"]].set_visible(False)
a2.set_title("Classe sous chaque test\n(× = la classe change)", pad=26)

# D : population
a3.barh(y, s.pop_totale / 1e3, height=0.62, color=AXE)
for i, v in enumerate(s.pop_totale):
    a3.text(v / 1e3 + 15, i, fr(v / 1e3, 0), va="center", fontsize=7, color=INK2)
a3.set_xlim(0, 1700)
a3.set_xticks([0, 500, 1000])
a3.set_title("Population\n(milliers)")
a3.grid(axis="y", visible=False)

h = [Line2D([], [], marker=m, linestyle="", markersize=6, markerfacecolor=col if plein else SURFACE, markeredgecolor=col,
            markeredgewidth=1.3, label=lab) for lab, col, m, plein in DIM.values()]
h += [Patch(color=c, label=k) for k, c in CLASSE.items()]
h += [Patch(facecolor=ND, edgecolor=MUTED, hatch="////", label="non classée : couverture non déterminable, score à 2 dimensions")]
fig.legend(handles=h, loc="upper center", bbox_to_anchor=(0.5, 0.075), ncol=3, fontsize=7.8)
fig.suptitle("O5-01 : 7 préfectures en priorité 1 (989 617 habitants) ; Tchamba, Kpendjal et Mô, non classées,\n"
             "seraient aussi en priorité 1 sur les deux dimensions mesurées", x=0.01, ha="left", fontsize=11.5, fontweight="bold", y=0.985)
finir(fig, "f1_classement", "Ordre : classe, puis population décroissante (règle du 02). Tests du 02 : chaque poids doublé, min-max, retrait du territoire extrême "
      "(Akébou ; Kpendjal pour la lecture à 2 dimensions).\n* Variante P13, décidée après avoir vu le résultat : le test min-max lu en rang. "
      "« Sans couv. » : lecture A11, 39 préfectures. « – » : test sans objet. Table : score_prefectures.csv", y=0.0)

# =============================================================== F2 — Carte des priorités : 3 dimensions et sans couverture
gp = gpd.read_file(GEO / "prefectures.geojson").to_crs(CRS_SURFACE).merge(
    s[["code", "classe_retenue", "sans_couv_classe", "depend_de_la_couverture"]], on="code")
syn = lire("synthese_classes").set_index(["lecture", "classe"])
DECALAGE = {"Kpendjal-Ouest": (2000, -4000), "Kpendjal": (24000, 12000), "Tandjoaré": (-4000, -6000)}  # mètres
fig, axes = plt.subplots(1, 2, figsize=(9, 8.6))
for ax, col, titre, lec in ((axes[0], "classe_retenue", "Score à 3 dimensions (règle du 02)", "3 dimensions"),
                            (axes[1], "sans_couv_classe", "Sans la couverture (2 dimensions)", "sans couverture")):
    for k, c in CLASSE.items():
        gp[gp[col] == k].plot(ax=ax, color=c, edgecolor=SURFACE, linewidth=0.6)
    m = gp[col].str.startswith("non")
    gp[m].plot(ax=ax, facecolor=ND, edgecolor=MUTED, hatch="////", linewidth=0.6)
    if lec == "3 dimensions":
        gp[gp.depend_de_la_couverture].boundary.plot(ax=ax, color="#eb6834", linewidth=1.6)
    lab = gp[(gp[col] == "priorité 1") | m | (gp.depend_de_la_couverture & (lec == "3 dimensions"))]
    for r in lab.itertuples():
        p = r.geometry.representative_point()
        dx, dy = DECALAGE.get(r.nom, (0, 0))
        ax.text(p.x + dx, p.y + dy, r.nom, fontsize=6.6, ha="center", va="center", color=INK,
                style="italic" if r.depend_de_la_couverture else "normal",
                path_effects=[pe.withStroke(linewidth=2.2, foreground=SURFACE)])
    ax.set_axis_off()
    ax.set_aspect("equal")
    ax.set_title(titre)
    h = []
    for k, c in CLASSE.items():
        r = syn.loc[(lec, k)]
        h.append(Patch(color=c, label=f"{k} : {int(r.prefectures)} préfectures, {fr(r.part_population_pct)} % de la population"))
    if lec == "3 dimensions":
        h.append(Patch(facecolor=ND, edgecolor=MUTED, hatch="////", label="non classée : couverture non déterminable"))
        h.append(Patch(facecolor=SURFACE, edgecolor="#eb6834", linewidth=1.6, label="la classe change sans la couverture"))
    ax.legend(handles=h, loc="upper left", bbox_to_anchor=(0, -0.01), fontsize=7.2)
fig.suptitle("O5-01 : aucune priorité 1 dans le Maritime ; sans la couverture, 12 préfectures en priorité 1 au lieu de 7", x=0.01, ha="left", fontsize=11.5, fontweight="bold")
finir(fig, "f2_carte_priorites", "Noms : préfectures en priorité 1, non classées, et (en italique) celles dont la classe change sans la couverture. Couverture = proxy de niveau C (rayon de 20 km autour des tours, 3i) : "
      "toute classe qui en dépend est « à confirmer ».\nTables : score_prefectures.csv, synthese_classes.csv")
print(f"2 figures écrites dans {FIG}")
