"""Cartes du 06 (analyse spatiale). Lit data/analysis/06_spatial/ et les contours de data/processed/geo/.

Règles de lecture (06_data_spatial_analysis.md, section 1) :
- projection à surfaces égales ; limites des préfectures en trait fin sur chaque carte ;
- classes des cartes : une classe « 0 » à part quand elle existe, puis les quartiles des valeurs positives des communes ;
  les mêmes bornes servent aux cartes des préfectures, pour que les deux mailles se comparent (P2) ;
- ratio non défini (aucun point au dénominateur) : hachures, jamais une couleur de valeur ;
- rampe bleue quand plus foncé = mieux doté ; rampe orange quand plus foncé = moins bien doté (habitants par point) ;
- encart du Grand Lomé sur les cartes par commune, avec l'avertissement de P2.
"""
import sys
from pathlib import Path

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "prep"))
from commun import CRS_SURFACE, GEO, PROCESSED  # noqa: E402

ICI = Path(__file__).resolve().parents[1] / "data" / "analysis" / "06_spatial"
EDA = ICI.parent / "05_eda"
FIG = ICI / "cartes"
FIG.mkdir(parents=True, exist_ok=True)

SURFACE, INK, INK2, MUTED, GRID, AXE = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
S = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
BLEUS = ["#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]          # rampe séquentielle validée (100 à 700)
ORANGES = [matplotlib.colors.to_hex(c) for c in
           LinearSegmentedColormap.from_list("o", ["#fde7da", "#eb6834", "#6e2a0e"])(np.linspace(0, 1, 5))]
DIVERGENT = ["#e34948", "#f0a09f", "#f0efec", "#86b6ef", "#2a78d6"]    # rouge <-> bleu, milieu gris
LISA = {"élevé entouré d'élevés": "#2a78d6", "élevé entouré de faibles": "#4a3aa7",
        "faible entouré de faibles": "#e34948", "faible entouré d'élevés": "#eda100", "non significatif": "#ecebe6"}
plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE, "font.family": "sans-serif",
    "font.size": 9, "text.color": INK, "axes.titlesize": 9.5, "axes.titleweight": "bold", "axes.titlelocation": "left",
    "legend.frameon": False})


def fr(x, d=0):
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",")


def finir(fig, nom, source, y=0.005):
    fig.text(0.01, y, source, color=MUTED, fontsize=7.3, ha="left", va="top")
    fig.savefig(FIG / f"{nom}.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def lire_geo(nom):
    return gpd.read_file(GEO / f"{nom}.geojson").to_crs(CRS_SURFACE)


G_COM, G_PREF, G_UR = lire_geo("communes"), lire_geo("prefectures"), lire_geo("unites_regionales")
com = G_COM.merge(pd.read_csv(ICI / "s3_communes.csv").drop(columns="nom"), on="code")
pref = G_PREF.merge(pd.read_csv(ICI / "s3_prefectures.csv").drop(columns="nom"), on="code")
GL = com[com.strate_50 == "grand_lome"]
XMIN, YMIN, XMAX, YMAX = G_COM.total_bounds


def fond(ax, etendre_bas=0.0):
    ax.set_axis_off()
    ax.set_aspect("equal")
    ax.set_xlim(XMIN - 5e3, XMAX + 5e3)
    ax.set_ylim(YMIN - 5e3 - etendre_bas * (YMAX - YMIN), YMAX + 5e3)


def bornes(valeurs):
    """Classe 0 à part si elle existe, puis quartiles des valeurs positives (communes)."""
    v = valeurs.dropna()
    pos = v[v > 0]
    q = list(np.quantile(pos, [0, .25, .5, .75, 1]))
    return ([0.0] if (v == 0).any() else []) + q


def classer(v, b):
    if pd.isna(v):
        return -1
    if b[0] == 0.0 and v == 0:
        return 0
    k = int(np.searchsorted(b[1:] if b[0] == 0.0 else b, v, side="left"))
    base = 1 if b[0] == 0.0 else 0
    return min(base + max(k - 1, 0), len(b) - 2 + (0 if b[0] == 0.0 else 0))


def etiquettes(b, d, unite=""):
    if b[0] == 0.0:
        q = b[1:]
        return ["0"] + [f"{fr(q[i], d)} à {fr(q[i + 1], d)}{unite}" for i in range(4)]
    return [f"{fr(b[i], d)} à {fr(b[i + 1], d)}{unite}" for i in range(4)]


def choro(ax, gdf, col, b, rampe, titre, nd_label=None, avec_encart=False, pointilles=None):
    classes = gdf[col].map(lambda v: classer(v, b))
    couleurs = rampe[-(len(b) - 1):] if b[0] != 0.0 else [rampe[0]] + rampe[1:]
    n_cls = len(b) - 1
    couleurs = rampe[5 - n_cls:] if n_cls < 5 else rampe
    for k in range(n_cls):
        gdf[classes == k].plot(ax=ax, color=couleurs[k], edgecolor=SURFACE, linewidth=0.3)
    nd = gdf[classes == -1]
    if len(nd):
        nd.plot(ax=ax, facecolor=SURFACE, edgecolor=MUTED, hatch="/////", linewidth=0.3)
    G_PREF.boundary.plot(ax=ax, color=INK2, linewidth=0.35)
    fond(ax, 0.22 if avec_encart else 0)
    ax.set_title(titre)
    if avec_encart:
        enc = ax.inset_axes([0.52, 0.0, 0.48, 0.2])
        for k in range(n_cls):
            GL[GL.code.isin(gdf[classes == k].code)].plot(ax=enc, color=couleurs[k], edgecolor=SURFACE, linewidth=0.4)
        GL.boundary.plot(ax=enc, color=INK2, linewidth=0.3)
        enc.set_axis_off()
        enc.set_aspect("equal")
        enc.set_title("Grand Lomé †", fontsize=7, loc="left", fontweight="normal", color=INK2)
    return couleurs


def legende(fig, couleurs, labels, titre, nd_label=None, y=0.02, x=0.5, ncol=None):
    h = [Patch(color=c, label=l) for c, l in zip(couleurs, labels)]
    if nd_label:
        h.append(Patch(facecolor=SURFACE, edgecolor=MUTED, hatch="/////", label=nd_label))
    fig.legend(handles=h, loc="upper center", bbox_to_anchor=(x, y), ncol=ncol or len(h), fontsize=7.6, title=titre,
               title_fontsize=7.8)


P2 = "† Grand Lomé et communes des « autres villes » : population résidente, pas fréquentation (P2). Lecture de référence du Grand Lomé : l'agrégat."

# =============================================================== C1 — Où sont les points ? (O3-01, O3-03)
pts = pd.read_csv(PROCESSED / "points_service.csv", low_memory=False)
pts = gpd.GeoDataFrame(pts, geometry=gpd.points_from_xy(pts.lon, pts.lat), crs="EPSG:4326").to_crs(CRS_SURFACE)
PANNEAUX = [("banque", "Banques\n(212)", S[0], 7), ("imf", "Institutions de\nmicrofinance (382)", S[0], 7),
            ("assurance", "Assurances\n(62)", S[0], 7), ("dab", "Distributeurs de billets\n(184), par emplacement", None, 7),
            ("mobile_money", "Points mobile money\n(19 788)", S[1], 0.4)]
fig, axes = plt.subplots(1, 5, figsize=(13, 6.4), gridspec_kw={"wspace": 0.02})
for ax, (t, titre, c, s) in zip(axes, PANNEAUX):
    G_COM.plot(ax=ax, color="#f4f3ef", edgecolor=SURFACE, linewidth=0.3)
    G_PREF.boundary.plot(ax=ax, color=AXE, linewidth=0.4)
    d = pts[(pts["type"] == t) & ((pts.compte_formel == 1) if t in ("banque", "imf", "assurance") else True)]
    if t == "dab":
        for cat, col in (("Dans une banque", S[0]), ("Independant", S[1]), ("Dans un autre etablissement", S[2])):
            e = d[d.categorie_origine == cat]
            ax.scatter(e.geometry.x, e.geometry.y, s=9, color=col, edgecolor=SURFACE, linewidth=0.3, zorder=3)
    else:
        ax.scatter(d.geometry.x, d.geometry.y, s=s, color=c, edgecolor=SURFACE if s > 1 else "none", linewidth=0.3,
                   alpha=0.9 if s > 1 else 0.6, zorder=3)
    fond(ax)
    ax.set_title(titre, fontsize=8.5)
axes[3].legend(handles=[Line2D([], [], marker="o", ls="", color=S[0], mec=SURFACE, label="dans une banque (126)"),
                        Line2D([], [], marker="o", ls="", color=S[1], mec=SURFACE, label="indépendant (53)"),
                        Line2D([], [], marker="o", ls="", color=S[2], mec=SURFACE, label="dans un autre\nétablissement (5)")],
               loc="upper left", bbox_to_anchor=(0.0, 0.02), fontsize=7.4)
fig.suptitle("Où sont les points de service ? Les points formels suivent les villes et les axes ;\nle mobile money couvre tout le pays",
             x=0.01, ha="left", fontsize=11, fontweight="bold", y=1.02)
finir(fig, "c1_points_par_type", "Points formels en service ; recensement 2021/2022 (banques, IMF, assurances, DAB, mobile money). Traits : limites des préfectures.\n"
      "La Poste n'est pas cartographiée (décision Q5). Table : 05, s2_offre_par_commune.csv")

# =============================================================== C2 — Densité des points (O3-03)
fig, axes = plt.subplots(1, 2, figsize=(7.6, 7.4))
for ax, (t, titre) in zip(axes, (("mobile_money", "Points mobile money"), ("formels", "Points formels"))):
    d = pts[pts["type"] == t] if t == "mobile_money" else pts[pts.compte_formel == 1]
    G_COM.plot(ax=ax, color="#f4f3ef", edgecolor=SURFACE, linewidth=0.3)
    hb = ax.hexbin(d.geometry.x, d.geometry.y, gridsize=(18, 50), bins="log", mincnt=1,
                   cmap=LinearSegmentedColormap.from_list("b", BLEUS), linewidths=0.2, edgecolors=SURFACE, zorder=2)
    G_PREF.boundary.plot(ax=ax, color=INK2, linewidth=0.35, zorder=3)
    fond(ax)
    ax.set_title(f"{titre}\npar hexagone d'environ {fr((XMAX - XMIN) / 18 / 1e3)} km de large")
    cb = fig.colorbar(hb, ax=ax, orientation="horizontal", fraction=0.035, pad=0.02)
    cb.set_label("points par hexagone (échelle logarithmique)", fontsize=7.5)
    cb.ax.tick_params(labelsize=7)
fig.suptitle("Densité : le mobile money est dense aussi hors des villes,\nles points formels restent groupés dans les chefs-lieux",
             x=0.01, ha="left", fontsize=11, fontweight="bold")
finir(fig, "c2_densite_points", "Hexagones vides : aucun point. Recensement 2021/2022.")

# =============================================================== C3 — Offre rapportée à la population, commune et préfecture (O4-01, O4-02, O4-04)
VARS3 = [("hab_par_point_formel", "Habitants par point formel", ORANGES, 0, " hab.", "aucun point formel : non défini"),
         ("mm_pour_10k_adultes", "Points mobile money pour 10 000 adultes", BLEUS, 1, "", None),
         ("dab_pour_100k_adultes", "Sites de DAB pour 100 000 adultes", BLEUS, 1, "", None)]
fig, axes = plt.subplots(2, 3, figsize=(11.5, 15))
for j, (col, titre, rampe, d, u, ndl) in enumerate(VARS3):
    b = bornes(com[col])
    c = choro(axes[0, j], com, col, b, rampe, f"{titre}\npar commune", avec_encart=True)
    choro(axes[1, j], pref, col, b, rampe, f"{titre}\npar préfecture")
    labels = etiquettes(b, d, u)
    h = [Patch(color=cc, label=l) for cc, l in zip(c, labels)]
    if ndl:
        h.append(Patch(facecolor=SURFACE, edgecolor=MUTED, hatch="/////", label=ndl))
    axes[1, j].legend(handles=h, loc="upper center", bbox_to_anchor=(0.5, -0.01), fontsize=7.3, ncol=1,
                      title="plus foncé = moins bien doté" if rampe is ORANGES else "plus foncé = mieux doté", title_fontsize=7.4)
fig.suptitle("Offre rapportée à la population : communes (en haut) et préfectures (en bas), mêmes classes",
             x=0.01, ha="left", fontsize=12, fontweight="bold", y=0.995)
fig.tight_layout(rect=(0, 0.02, 1, 0.985))
finir(fig, "c3_offre_population", "Classes : 0 à part, puis quartiles des communes ; mêmes bornes pour les préfectures. Population : RGPH-5 2022. " + "\n" + P2 +
      "\nTables : s3_communes.csv, s3_prefectures.csv")

# =============================================================== C4 — Quotient de localisation des points formels (O3-02)
BQ = [0.0, 0.5, 0.8, 1.25, 2.0, np.inf]
LQ = ["0 (aucun point)", "moins de 0,5", "0,5 à 0,8", "0,8 à 1,25 (proportionnel)", "1,25 à 2", "plus de 2"]
CQ = ["#b3302f", "#e34948", "#f0a09f", "#f0efec", "#86b6ef", "#2a78d6"]


def classe_q(v):
    return 0 if v == 0 else 1 + int(np.searchsorted(BQ[1:], v, side="right"))


fig, axes = plt.subplots(1, 2, figsize=(7.8, 7.8))
for ax, g, titre, enc in ((axes[0], com, "Par commune", True), (axes[1], pref, "Par préfecture", False)):
    k = g.quotient_localisation_formels.map(classe_q).clip(upper=5)
    for i in range(6):
        g[k == i].plot(ax=ax, color=CQ[i], edgecolor=SURFACE, linewidth=0.3, hatch="////" if i == 0 else None)
    G_PREF.boundary.plot(ax=ax, color=INK2, linewidth=0.35)
    fond(ax, 0.22 if enc else 0)
    ax.set_title(titre)
    if enc:
        e = ax.inset_axes([0.52, 0.0, 0.48, 0.2])
        kk = GL.quotient_localisation_formels.map(classe_q).clip(upper=5)
        for i in range(6):
            GL[kk == i].plot(ax=e, color=CQ[i], edgecolor=SURFACE, linewidth=0.4)
        e.set_axis_off()
        e.set_aspect("equal")
        e.set_title("Grand Lomé †", fontsize=7, loc="left", fontweight="normal", color=INK2)
fig.legend(handles=[Patch(facecolor=c, edgecolor=SURFACE, hatch="////" if i == 0 else None, label=l) for i, (c, l) in enumerate(zip(CQ, LQ))],
           loc="upper center", bbox_to_anchor=(0.5, 0.05), ncol=3,
           fontsize=7.6, title="Part des points formels du pays ÷ part de la population du pays", title_fontsize=7.8)
fig.suptitle("Où les points formels sont-ils sur- ou sous-représentés\npar rapport à la population ?", x=0.01, ha="left",
             fontsize=11, fontweight="bold")
finir(fig, "c4_quotient_localisation", "1 = les points suivent exactement la population. Bornes fixées à l'avance (0,5 ; 0,8 ; 1,25 ; 2), symétriques autour de 1.\n" + P2 +
      "\nTable : s3_communes.csv, s3_prefectures.csv", y=-0.05)

# =============================================================== C5 — Points mobile money par guichet et distance au guichet (O4-03)
dist = pd.read_csv(ICI / "s5_distances_communes.csv")
fig, axes = plt.subplots(1, 3, figsize=(11.5, 7.8))
b = bornes(com.mm_par_point_formel)
c = choro(axes[0], com, "mm_par_point_formel", b, ORANGES, "Agents mobile money par guichet financier\n(en points de service), par commune",
          avec_encart=True)
choro(axes[1], pref, "mm_par_point_formel", b, ORANGES, "Agents mobile money par guichet financier\n(en points de service), par préfecture")
axes[1].legend(handles=[Patch(color=cc, label=l) for cc, l in zip(c, etiquettes(b, 1))] +
               [Patch(facecolor=SURFACE, edgecolor=MUTED, hatch="/////", label="aucun point formel :\nmobile money uniquement")],
               loc="upper center", bbox_to_anchor=(0.5, -0.01), fontsize=7.3, title="plus foncé = moins de guichets par point", title_fontsize=7.4)
ax = axes[2]
G_COM.plot(ax=ax, color="#f4f3ef", edgecolor=SURFACE, linewidth=0.3)
com[com.n_formels == 0].plot(ax=ax, facecolor=SURFACE, edgecolor=MUTED, hatch="/////", linewidth=0.3)
G_PREF.boundary.plot(ax=ax, color=AXE, linewidth=0.4)
mm = pts[pts["type"] == "mobile_money"].copy()
from scipy.spatial import cKDTree  # noqa: E402
f = pts[pts.compte_formel == 1]
mm["km"] = cKDTree(np.c_[f.geometry.x, f.geometry.y]).query(np.c_[mm.geometry.x, mm.geometry.y])[0] / 1e3
for lo, hi, col, lab in ((0, 5, AXE, "5 km ou moins"), (5, 10, "#eda100", "5 à 10 km"), (10, 1e9, "#e34948", "plus de 10 km")):
    e = mm[(mm.km > lo) & (mm.km <= hi)] if lo else mm[mm.km <= hi]
    ax.scatter(e.geometry.x, e.geometry.y, s=1.2 if lo else 0.4, color=col, zorder=3 if lo else 2, label=f"{lab} ({fr(len(e))})")
fond(ax)
ax.set_title("Distance de chaque point mobile money\nau point formel le plus proche")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.01), fontsize=7.3, markerscale=6,
          title="à vol d'oiseau ; hachures : commune sans point formel", title_fontsize=7.4)
fig.suptitle("Le mobile money comme accès unique : 22 communes sans guichet, et 1 point sur 13 à plus de 10 km d'un guichet",
             x=0.01, ha="left", fontsize=11, fontweight="bold")
fig.tight_layout(rect=(0, 0.03, 1, 0.97))
finir(fig, "c5_mm_par_guichet_distance", "Agents comptés en points de service (A8) : un lieu servi par les deux opérateurs compte une fois ; guichet = banque, IMF ou "
      "assurance.\nSeuils de 5 et 10 km : conventions de lecture, pas des normes. " + P2 +
      "\nTables : s3_communes.csv, s3_prefectures.csv, s5_distances_communes.csv")

# =============================================================== C6 — Couverture 3i (proxy de niveau C, O2-06)
fig, axes = plt.subplots(1, 2, figsize=(7.8, 7.8))
BC = [0, 50, 75, 90, 99, 100.0001]
LC = ["moins de 50 %", "50 à 75 %", "75 à 90 %", "90 à 99 %", "99 % et plus"]
for ax, g, titre in ((axes[0], com, "Par commune"), (axes[1], pref, "Par préfecture")):
    nd = g.couv_20km_motif == "non_determinable"
    k = pd.cut(g.couv_20km_pct, BC, right=False, labels=False)
    for i in range(5):
        g[(k == i) & ~nd].plot(ax=ax, color=BLEUS[i], edgecolor=SURFACE, linewidth=0.3)
    g[nd].plot(ax=ax, facecolor=SURFACE, edgecolor=MUTED, hatch="/////", linewidth=0.3)
    G_PREF.boundary.plot(ax=ax, color=INK2, linewidth=0.35)
    fond(ax)
    ax.set_title(titre)
fig.legend(handles=[Patch(color=c, label=l) for c, l in zip(BLEUS, LC)] +
           [Patch(facecolor=SURFACE, edgecolor=MUTED, hatch="/////", label="non déterminable (A13)")],
           loc="upper center", bbox_to_anchor=(0.5, 0.05), ncol=3, fontsize=7.6,
           title="Part de la population à moins de 20 km d'une tour (proxy 3i)", title_fontsize=7.8)
fig.suptitle("Couverture réseau (proxy) : forte au Sud et le long des axes,\nnon déterminable dans 9 communes du Centre et du Nord",
             x=0.01, ha="left", fontsize=11, fontweight="bold")
finir(fig, "c6_couverture_3i", "Proxy de niveau C : distance à une tour, pas un signal mesuré. « Non déterminable » : 3i donne 0 % alors que des points mobile money "
      "prouvent un réseau (A13, V4 du 04).\nBornes fixées à l'avance. Tables : s3_communes.csv, s3_prefectures.csv", y=-0.05)

# =============================================================== C7 — Grappes locales (LISA, voisinage P3)
lisa = pd.read_csv(ICI / "s7_lisa_communes.csv")
fig, axes = plt.subplots(1, 3, figsize=(11.5, 7.8))
for ax, (v, titre) in zip(axes, (("formels_pour_10k_hab", "Points formels\npour 10 000 habitants"),
                                 ("mm_pour_10k_adultes", "Points mobile money\npour 10 000 adultes"),
                                 ("couv_20km_pct", "Couverture 3i\n(proxy)"))):
    g = G_COM.merge(lisa[lisa.variable == v], on="code", how="left")
    G_COM.plot(ax=ax, facecolor=SURFACE, edgecolor=MUTED, hatch="/////", linewidth=0.3)
    for cat, col in LISA.items():
        g[g.grappe == cat].plot(ax=ax, color=col, edgecolor=SURFACE, linewidth=0.3)
    G_PREF.boundary.plot(ax=ax, color=INK2, linewidth=0.35)
    fond(ax)
    ax.set_title(titre)
fig.legend(handles=[Patch(color=c, label=l) for l, c in LISA.items()] +
           [Patch(facecolor=SURFACE, edgecolor=MUTED, hatch="/////", label="hors calcul (couverture non déterminable)")],
           loc="upper center", bbox_to_anchor=(0.5, 0.05), ncol=3, fontsize=7.6,
           title="Commune comparée à ses voisines (contours qui se touchent), seuil de 5 %", title_fontsize=7.8)
fig.suptitle("Grappes locales : le mobile money et la couverture forment des grappes ; pas les points formels",
             x=0.01, ha="left", fontsize=11, fontweight="bold")
finir(fig, "c7_grappes_lisa", "Indicateurs locaux d'association spatiale (LISA), 999 permutations, sans correction pour tests multiples : une grappe est un signal à vérifier.\n"
      "Tables : s7_moran_global.csv, s7_lisa_communes.csv", y=-0.05)

# =============================================================== C8 — Synthèse : territoires signalés (05) et signaux spatiaux
sig = pd.read_csv(EDA / "s7_territoires_signales.csv")
seul = com[com.n_formels == 0].code
autres = sig[~sig.code.isin(seul) & (sig.strate_50 != "grand_lome")].code
ll = set(lisa[(lisa.grappe == "faible entouré de faibles")].code)
fig, (ax, axl) = plt.subplots(1, 2, figsize=(8.2, 8.6), gridspec_kw={"width_ratios": [2.3, 1], "wspace": 0.02})
G_COM.plot(ax=ax, color="#f4f3ef", edgecolor=SURFACE, linewidth=0.3)
com[com.code.isin(seul)].plot(ax=ax, color="#e34948", edgecolor=SURFACE, linewidth=0.3)
com[com.code.isin(autres)].plot(ax=ax, color="#eda100", edgecolor=SURFACE, linewidth=0.3)
com[com.code.isin(ll)].boundary.plot(ax=ax, color=INK, linewidth=1.1)
G_PREF.boundary.plot(ax=ax, color=INK2, linewidth=0.35)
far = dist[dist.part_plus_10km_guichet_pct >= 50]
cent = com[com.code.isin(far.code)].representative_point()
ax.scatter(cent.x, cent.y, marker="o", s=16, color=INK, zorder=4)
# Les 22 communes sans point formel, numérotées du nord au sud (pas un classement)
z = com[com.code.isin(seul)].assign(pt=lambda d: d.representative_point())
z = z.assign(y=z.pt.y, x=z.pt.x).sort_values("y", ascending=False).reset_index(drop=True)
for i, r in z.iterrows():
    ax.annotate(str(i + 1), (r.x, r.y), xytext=(7, 4), textcoords="offset points", fontsize=6.8, color=INK, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.12", fc=SURFACE, ec="none", alpha=0.85), zorder=5)
fond(ax)
axl.axis("off")
axl.text(0, 0.98, "Communes sans point formel\n(du nord au sud)", fontsize=8, fontweight="bold", va="top")
axl.text(0, 0.925, "\n".join(f"{i + 1:>2}  {r.nom} ({r.prefecture})" for i, r in z.iterrows()), fontsize=7.2, va="top",
         family="monospace", linespacing=1.5)
ax.legend(handles=[Patch(color="#e34948", label="mobile money uniquement (22 communes)"),
                   Patch(color="#eda100", label="autre signal de l'exploration (hors Grand Lomé)"),
                   Line2D([], [], color=INK, lw=1.1, label="grappe « faible entouré de faibles » (une variable au moins)"),
                   Line2D([], [], marker="o", ls="", color=INK, ms=4, label="la moitié des points mobile money ou plus\nà plus de 10 km d'un point formel")],
          loc="upper left", bbox_to_anchor=(0.0, 0.0), fontsize=7.4)
ax.set_title("Où se cumulent les signaux ? Aucun classement :\nla priorité viendra du score (étape 09)", fontsize=10.5)
finir(fig, "c8_synthese_signaux", "Communes du Grand Lomé signalées par la seule comparaison avec leurs voisines : non colorées (P2). "
      "Numéros : ordre géographique, du nord au sud.\n"
      "Tables : 05, s7_territoires_signales.csv ; s7_lisa_communes.csv ; s5_distances_communes.csv")

# =============================================================== C9 — Accès déclaré à Internet par région (EHCVM, objectifs 1 et 5)
us = G_UR.merge(pd.read_csv(ICI / "s6_usage_internet_regions.csv").drop(columns="nom"), on="code")
BU, LU = [0, 15, 25, 35, 50, 100.01], ["moins de 15 %", "15 à 25 %", "25 à 35 %", "35 à 50 %", "50 % et plus"]
fig, axes = plt.subplots(1, 2, figsize=(8, 8.2))
for ax, v, titre in ((axes[0], "2018_19", "2018/19"), (axes[1], "2021_22", "2021/22")):
    k = pd.cut(us[f"estimation_pct_{v}"], BU, right=False, labels=False)
    for i in range(5):
        us[k == i].plot(ax=ax, color=BLEUS[i], edgecolor=SURFACE, linewidth=0.8)
    G_PREF.boundary.plot(ax=ax, color=SURFACE, linewidth=0.3)
    fond(ax)
    ax.set_title(f"Enquête EHCVM {titre}")
    for _, r in us.iterrows():
        demi = (r[f"ic95_haut_{v}"] - r[f"ic95_bas_{v}"]) / 2
        txt = f"{fr(r[f'estimation_pct_{v}'], 1)} %\n(± {fr(demi, 1)})"
        if v == "2021_22":
            txt += f"\n+{fr(r.variation_points, 1)} pt"
        pt = r.geometry.representative_point()
        fonce = k[_] >= 3
        if r.code == "GL":
            ax.annotate(txt, (pt.x, pt.y), xytext=(pt.x + 95e3, pt.y - 8e3), fontsize=7.4, color=INK, ha="left", va="center",
                        arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
        else:
            ax.text(pt.x, pt.y, txt, fontsize=7.4, ha="center", va="center", color=SURFACE if fonce else INK)
fig.legend(handles=[Patch(color=c, label=l) for c, l in zip(BLEUS, LU)], loc="upper center", bbox_to_anchor=(0.5, 0.06),
           ncol=5, fontsize=7.6, title="Individus de 15 ans et plus déclarant avoir accès à Internet", title_fontsize=7.8)
fig.suptitle("Accès à Internet par région : il progresse partout,\nmais les Savanes restent à 14 %, contre 67 % dans le Grand Lomé",
             x=0.01, ha="left", fontsize=11, fontweight="bold")
finir(fig, "c9_usage_internet_regions", "6 régions seulement : aucune enquête ne descend à la préfecture ni à la commune. Même définition et mêmes grappes aux deux vagues (R5). "
      "Entre parenthèses : demi-largeur de l'intervalle\nde confiance à 95 %. Afrobaromètre (petits effectifs par région) et MICS6 (15-49 ans, 2017) non cartographiés. "
      "Table : s6_usage_internet_regions.csv", y=-0.03)


def choro_fixe(ax, g, col, bins, couleurs, labels, titre, encart=True, legende_titre=None):
    """Classes à bornes fixées à l'avance ; légende sous la carte."""
    k = pd.cut(g[col], bins, right=False, labels=False)
    for i, c in enumerate(couleurs):
        g[k == i].plot(ax=ax, color=c, edgecolor=SURFACE, linewidth=0.3)
    G_PREF.boundary.plot(ax=ax, color=INK2, linewidth=0.35)
    fond(ax, 0.22 if encart else 0)
    ax.set_title(titre, fontsize=9)
    if encart:
        e = ax.inset_axes([0.52, 0.0, 0.48, 0.2])
        for i, c in enumerate(couleurs):
            g[g.code.isin(GL.code) & (k == i)].plot(ax=e, color=c, edgecolor=SURFACE, linewidth=0.4)
        e.set_axis_off()
        e.set_aspect("equal")
        e.set_title("Grand Lomé", fontsize=7, loc="left", fontweight="normal", color=INK2)
    ax.legend(handles=[Patch(color=c, label=l) for c, l in zip(couleurs, labels)], loc="upper center", bbox_to_anchor=(0.5, 0.0),
              fontsize=7, title=legende_titre, title_fontsize=7.2)


# =============================================================== C10 — Structure par opérateur des points mobile money (objectif 3)
opc = G_COM.merge(pd.read_csv(ICI / "s2_operateurs_communes.csv").drop(columns="nom"), on="code")
GRIS = ["#f0efec", "#d9d8d2", "#b0afa8", "#6f6e69"]
PANO = [("part_deux_operateurs_pct", "Servis par les deux opérateurs", [0, 40, 55, 70, 85, 100.01], BLEUS,
         ["moins de 40 %", "40 à 55 %", "55 à 70 %", "70 à 85 %", "85 % et plus"], "plus foncé = réseau dual"),
        ("part_togocom_seul_pct", "Servis par Togocom seul", [0, 5, 15, 30, 50, 100.01], ORANGES,
         ["moins de 5 %", "5 à 15 %", "15 à 30 %", "30 à 50 %", "50 % et plus"], "plus foncé = dépendance"),
        ("part_moov_seul_pct", "Servis par Moov seul", [0, 5, 15, 30, 50, 100.01], ORANGES,
         ["moins de 5 %", "5 à 15 %", "15 à 30 %", "30 à 50 %", "50 % et plus"], "plus foncé = dépendance"),
        ("part_operateur_non_renseigne_pct", "Opérateur non renseigné", [0, 5, 10, 25, 100.01], GRIS,
         ["moins de 5 %", "5 à 10 %", "10 à 25 %", "25 % et plus"], "plus foncé = structure moins sûre")]
fig, axes = plt.subplots(1, 4, figsize=(14, 8.4), gridspec_kw={"wspace": 0.05})
for ax, (col, titre, bins, rampe, labels, lt) in zip(axes, PANO):
    choro_fixe(ax, opc, col, bins, rampe, labels, f"{titre}\n(% des points de la commune)", legende_titre=lt)
fig.suptitle("Structure par opérateur : réseau dual dans le Sud, dépendance à Togocom autour de Sokodé et de Kara",
             x=0.01, ha="left", fontsize=11, fontweight="bold")
finir(fig, "c10_operateurs_mobile_money", "Recensement des points mobile money 2021/2022. Un point servi par les deux opérateurs compte une fois ; "
      "les quatre parts font 100 %. Bornes fixées à l'avance.\nTable : s2_operateurs_communes.csv", y=-0.02)

# =============================================================== C11 — Fibre recensée par commune (3i, objectif 2)
fbc = G_COM.merge(pd.read_csv(ICI / "s6_fibre_communes.csv").drop(columns="nom"), on="code")
fig, axes = plt.subplots(1, 2, figsize=(8, 8.4))
for ax, col, titre in ((axes[0], "km_fibre_enterree", "Fibre enterrée"), (axes[1], "km_fibre_aerienne", "Fibre aérienne")):
    b = bornes(fbc[col])
    c = choro(ax, fbc, col, b, BLEUS, f"{titre} (km), par commune", avec_encart=True)
    q = b[1:]
    labs = ["aucune fibre recensée", f"moins de {fr(q[1], 1)} km"] + [f"{fr(q[i], 1)} à {fr(q[i + 1], 1)} km" for i in (1, 2, 3)]
    ax.legend(handles=[Patch(color=cc, label=l) for cc, l in zip(c, labs)], loc="upper center", bbox_to_anchor=(0.5, 0.0), fontsize=7.2)
fig.suptitle("Fibre : un réseau enterré sur les grands axes, aérien surtout dans le Maritime ;\n45 communes sans fibre recensée",
             x=0.01, ha="left", fontsize=11, fontweight="bold")
finir(fig, "c11_fibre_communes", "Source : 3i (geodata, campagne PRISE), niveau C : longueur de câble, sans date ni distinction entre transport et accès. "
      "Jamais additionnée aux abonnements FTTH (O2-07).\nClasses : 0 à part, puis quartiles des communes qui en ont. Table : s6_fibre_communes.csv", y=-0.02)

# =============================================================== C12 — Capacités et usage déclarés par région (objectif 5)
cap = pd.read_csv(ICI / "s9_capacites_usage_regions.csv")
fig, axes = plt.subplots(1, 2, figsize=(8, 8.2))
PANC = [("alphabetisation", "Alphabétisation des 15 ans et plus, 2021/22", [0, 50, 60, 70, 80, 100.01],
         ["moins de 50 %", "50 à 60 %", "60 à 70 %", "70 à 80 %", "80 % et plus"]),
        ("usage_mobile_banking", "Adultes faisant du mobile banking, 2021/22", [0, 20, 30, 40, 50, 100.01],
         ["moins de 20 %", "20 à 30 %", "30 à 40 %", "40 à 50 %", "50 % et plus"])]
for ax, (ind, titre, bins, labels) in zip(axes, PANC):
    g = G_UR.merge(cap[(cap.indicateur == ind) & (cap.vague == "2021/22")].drop(columns="nom"), on="code")
    k = pd.cut(g.estimation_pct, bins, right=False, labels=False)
    for i in range(5):
        g[k == i].plot(ax=ax, color=BLEUS[i], edgecolor=SURFACE, linewidth=0.8)
    G_PREF.boundary.plot(ax=ax, color=SURFACE, linewidth=0.3)
    fond(ax)
    ax.set_title(titre, fontsize=9.5)
    for idx, r in g.iterrows():
        txt = f"{fr(r.estimation_pct, 1)} %\n(± {fr((r.ic95_haut - r.ic95_bas) / 2, 1)})"
        if not pd.isna(r.variation_points):
            txt += f"\n+{fr(r.variation_points, 1)} pt"
        pt = r.geometry.representative_point()
        if r.code == "GL":
            ax.annotate(txt, (pt.x, pt.y), xytext=(pt.x + 95e3, pt.y - 8e3), fontsize=7.4, ha="left", va="center",
                        arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
        else:
            ax.text(pt.x, pt.y, txt, fontsize=7.4, ha="center", va="center", color=SURFACE if k[idx] >= 3 else INK)
    ax.legend(handles=[Patch(color=c, label=l) for c, l in zip(BLEUS, labels)], loc="upper center", bbox_to_anchor=(0.5, 0.0),
              fontsize=7.2, ncol=2)
fig.suptitle("Capacités et usage : les Savanes cumulent la plus faible alphabétisation (41 %)\net un usage du mobile banking parmi les plus bas",
             x=0.01, ha="left", fontsize=11, fontweight="bold")
finir(fig, "c12_capacites_usage_regions", "Enquête EHCVM (niveau B, calculé par nous), 6 régions seulement. Entre parenthèses : demi-largeur de l'intervalle de "
      "confiance à 95 % ; « pt » : gain depuis 2018/19.\nMobile banking : question différente en 2018/19, pas de variation. Bornes fixées à l'avance. "
      "Table : s9_capacites_usage_regions.csv", y=-0.02)
print(f"cartes écrites dans {FIG}")
