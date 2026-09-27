"""Figures du 07 (indicateurs). Lit les tables de data/analysis/07_indicateurs/ et écrit des PNG dans figures/.

Même style que les figures du 05. Classes de O1-02 en couleurs divergentes (bleu : accélération ; rouge :
ralentissement ; gris : rythme habituel), doublées d'une texture pour les cas non retenus ou non classés.
Événements en encre neutre, forme selon le type, numérotés et listés à droite de chaque figure.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

ICI = Path(__file__).resolve().parents[1] / "data" / "analysis" / "07_indicateurs"
FIG = ICI / "figures"
FIG.mkdir(parents=True, exist_ok=True)

SURFACE, INK, INK2, MUTED, GRID, AXE = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
BLEU, ROUGE, NEUTRE, BANDE = "#2a78d6", "#e34948", "#c3c2b7", "#f0efec"  # paire divergente + milieu gris
plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "font.family": "sans-serif", "font.size": 9.5, "text.color": INK, "axes.labelcolor": INK2,
    "axes.edgecolor": AXE, "axes.linewidth": 0.8, "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
    "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False, "lines.linewidth": 1.6,
    "axes.titlesize": 10.5, "axes.titleweight": "bold", "axes.titlelocation": "left", "axes.titlecolor": INK})

COULEUR = {"accélération": BLEU, "ralentissement": ROUGE, "rythme habituel": NEUTRE}
FORME = {"technologie": "^", "infrastructure": "D", "opérateur": "s", "tarif": "o", "crise": "P"}
LIB_TYPE = {"technologie": "technologie", "infrastructure": "infrastructure", "opérateur": "entrée d'opérateur",
            "tarif": "réforme ou offre tarifaire", "crise": "crise sanitaire"}


def lire(nom):
    return pd.read_csv(ICI / f"{nom}.csv")


def fr(x, d=1):
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",")


def finir(fig, nom, source):
    fig.text(0.01, -0.01, source, color=MUTED, fontsize=7.5, ha="left", va="top")
    fig.savefig(FIG / f"{nom}.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def axe_annees(ax, debut, fin):
    ax.set_xlim(debut - 0.3, fin + 1.3)
    ax.set_xticks([a + 0.5 for a in range(debut, fin + 1)])
    ax.set_xticklabels([str(a) if a % 2 == 0 else "" for a in range(debut, fin + 1)])
    ax.grid(axis="x", visible=False)


def barres(ax, annees, valeurs, classes, retenues=None):
    """Une barre par année, centrée sur l'année ; texture pour ce qui n'est pas lu comme une classe."""
    for i, (a, v, c) in enumerate(zip(annees, valeurs, classes)):
        base = c.split(" (")[0]
        if base == "non classé":
            ax.bar(a + 0.5, v, 0.72, color=SURFACE, edgecolor=MUTED, hatch="////", linewidth=0.8)
            continue
        garde = True if retenues is None else retenues[i]
        couleur = COULEUR.get(base, NEUTRE)
        ax.bar(a + 0.5, v, 0.72, color=couleur if garde else SURFACE, edgecolor=couleur if not garde else SURFACE,
               hatch=None if garde else "////", linewidth=0.8 if not garde else 0.5)


def frise(ax, ev, debut, fin):
    ev = ev[(ev.x >= debut) & (ev.x < fin + 1)].sort_values("x")
    niveaux, dernier = [], {}
    for x in ev.x:  # empile les marqueurs trop proches
        n = 0
        while n in dernier and x - dernier[n] < 0.55:
            n += 1
        dernier[n] = x
        niveaux.append(n)
    for (_, r), n in zip(ev.iterrows(), niveaux):
        ax.scatter(r.x, -n, marker=FORME[r.type], s=34, color=INK2 if r.niveau_preuve == "A" else SURFACE,
                   edgecolor=INK2, linewidth=0.9, zorder=3)
        ax.text(r.x + 0.13, -n, str(int(r.numero)), fontsize=7, color=INK, va="center")
    ax.set_ylim(-max(niveaux) - 0.8, 0.8)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.grid(False)
    for a in range(debut, fin + 2):
        ax.axvline(a, color=GRID, lw=0.5, zorder=0)
    ax.set_title("Événements retenus (annotés, jamais présentés comme des causes)", fontsize=9)
    return ev


def liste(ax, ev):
    ax.axis("off")
    lignes = []
    for _, r in ev.iterrows():
        txt = r.evenement.split(" ; ")[0].split(" (arrêtés")[0]
        txt = txt if len(txt) <= 58 else txt[:56] + "…"
        lignes.append(f"{int(r.numero):>2}  {r.date:<10}  {txt}{'' if r.niveau_preuve == 'A' else '  [C]'}")
    ax.text(0, 1, "\n".join(lignes), fontsize=6.6, family="monospace", va="top", color=INK, linespacing=1.45)
    poignees = [Line2D([], [], marker=m, ls="", color=INK2, mec=INK2, ms=6, label=LIB_TYPE[t]) for t, m in FORME.items()]
    poignees.append(Line2D([], [], marker="o", ls="", color=SURFACE, mec=INK2, ms=6, label="marqueur creux : source presse [C]"))
    ax.legend(handles=poignees, loc="lower left", fontsize=7, bbox_to_anchor=(0, -0.02), ncol=1)


ev = lire("o1_02_evenements")
ev = ev[ev.retenu].copy()
refs = lire("o1_02_references").set_index(["serie", "convention", "role"])

# =============================================================== F1 — Usage d'Internet
u = lire("o1_02_usage")
vg = lire("o1_02_enquetes_periodes")
ref = refs.loc[("usage (D1)", "publiée", "principal")]
fig = plt.figure(figsize=(12.4, 8.2))
gs = fig.add_gridspec(3, 2, width_ratios=[3.3, 1.35], height_ratios=[3.1, 1.5, 1.35], hspace=0.42, wspace=0.04)
ax1, ax2, ax3, axl = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[1, 0]), fig.add_subplot(gs[2, 0]), fig.add_subplot(gs[:, 1])

ax1.axhspan(ref.seuil_bas, ref.seuil_haut, color=BANDE, zorder=0)
ax1.axhline(ref.moyenne, color=MUTED, lw=0.8, ls=":")
ax1.axhline(2, color=MUTED, lw=0.8, ls="--")
retenue = [not str(x).endswith("(D-15)") for x in u.lecture]
barres(ax1, u.annee, u.croissance_pct, u.classe, retenue)
for _, r in u[u.classe.isin(["accélération", "ralentissement"])].iterrows():
    ax1.text(r.annee + 0.5, r.croissance_pct + 1.2, f"{fr(r.croissance_pct)} %", ha="center", fontsize=7.5, color=INK)
for _, r in vg.iterrows():
    ls = "-" if r.source == "Afrobaromètre" else "--"
    ax1.plot([r.debut + 1, r.fin + 1], [r.croissance_annualisee_pct] * 2, color=INK, lw=2, ls=ls, solid_capstyle="butt")
axe_annees(ax1, 2010, 2024)
ax1.set_ylim(0, 86)
ax1.set_ylabel("Croissance annuelle (%)")
ax1.set_title("Croissance annuelle de l'usage d'Internet (série estimée par l'UIT), classée sur 2010-2024")
ax1.legend(handles=[Patch(color=BLEU, label="accélération (confirmée par l'enquête)"),
                    Patch(color=ROUGE, label="ralentissement (confirmé par l'enquête)"),
                    Patch(color=NEUTRE, label="rythme habituel"),
                    Patch(color=BANDE, label=f"moyenne ± 1 écart-type : {fr(ref.seuil_bas)} % à {fr(ref.seuil_haut)} %"),
                    Line2D([], [], color=MUTED, lw=0.8, ls=":", label=f"moyenne 2010-2024 : {fr(ref.moyenne)} %"),
                    Line2D([], [], color=MUTED, lw=0.8, ls="--", label="seuil de stagnation du 02 : 2 %"),
                    Line2D([], [], color=INK, lw=2, label="Afrobaromètre : croissance par an entre vagues"),
                    Line2D([], [], color=INK, lw=2, ls="--", label="EHCVM : croissance par an entre vagues")],
           loc="upper left", fontsize=7.1, ncol=2, columnspacing=1.2)

ax2.bar(u.annee + 0.5, u.variation_points, 0.72, color=MUTED)
m = u.variation_points.idxmax()
ax2.text(u.annee[m] + 0.5, u.variation_points[m] + 0.3, f"+{fr(u.variation_points[m])} pt", ha="center", fontsize=7.5)
axe_annees(ax2, 2010, 2024)
ax2.set_ylim(0, 10)
ax2.set_title("Variation en points de pourcentage de la population", fontsize=9.5)
ax2.set_ylabel("Points")

e1 = frise(ax3, ev, 2009, 2024)
axe_annees(ax3, 2010, 2024)
ax3.set_xlim(2009.7, 2025.3)
liste(axl, e1)
fig.suptitle("Usage d'Internet : accélérations en 2016 et 2020, ralentissements en 2021, 2023 et 2024",
             x=0.01, ha="left", fontsize=12, fontweight="bold", y=0.955)
finir(fig, "f1_o1_02_usage",
      "Sources : UIT via la Banque mondiale (estimations, sauf 2017 : enquête de l'INSEED) ; Afrobaromètre (18 ans et plus) ; EHCVM (15 ans et plus) ; "
      "chronologie des événements.\nSensibilité (2015-2024) : seules 2016 (accélération) et 2021 (ralentissement) gardent leur classe. Tables : o1_02_usage.csv, o1_02_enquetes_periodes.csv, "
      "o1_02_references.csv, o1_02_evenements.csv")

# =============================================================== F2 — Abonnements data mobile
a = lire("o1_02_abonnements")
q = lire("o1_02_abonnements_trimestres")
r4 = refs.loc[("abonnements data mobile", "T4", "principal")]
rm = refs.loc[("abonnements data mobile", "moyenne_4T", "principal")]
fig = plt.figure(figsize=(12.4, 8.2))
gs = fig.add_gridspec(3, 2, width_ratios=[3.3, 1.35], height_ratios=[3.1, 1.7, 1.35], hspace=0.42, wspace=0.04)
ax1, ax2, ax3, axl = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[1, 0]), fig.add_subplot(gs[2, 0]), fig.add_subplot(gs[:, 1])

ax1.axhspan(r4.seuil_bas, r4.seuil_haut, color=BANDE, zorder=0)
for v in (rm.seuil_bas, rm.seuil_haut):
    ax1.axhline(v, color=MUTED, lw=0.7, ls=":")
ax1.axhline(0, color=AXE, lw=0.8)
ax1.axhline(2, color=MUTED, lw=0.8, ls="--")
barres(ax1, a.annee, a.croissance_T4_pct, a.classe_finale)
d = a[a.annee >= 2018]
ax1.scatter(d.annee + 0.5, d.croissance_moyenne_4T_pct, marker="D", s=26, color=INK, edgecolor=SURFACE, linewidth=1,
            zorder=4, label="moyenne des 4 trimestres")
for _, r in a[a.rupture.notna()].iterrows():
    ax1.text(r.annee + 0.5, max(r.croissance_T4_pct, 0) + 3, "rupture", ha="center", fontsize=7, color=INK2)
axe_annees(ax1, 2011, 2025)
ax1.set_xlim(2010.7, 2026.8)
ax1.set_ylim(-10, 135)
ax1.set_ylabel("Croissance annuelle (%)")
ax1.set_title("Croissance annuelle des abonnements data mobile (valeur du 4e trimestre), classée sur 2010-2024")
ax1.legend(handles=[Patch(color=BLEU, label="accélération"), Patch(color=ROUGE, label="ralentissement"),
                    Patch(color=NEUTRE, label="rythme habituel"),
                    Patch(facecolor=SURFACE, edgecolor=MUTED, hatch="////", label="non classé : rupture de série"),
                    Patch(color=BANDE, label=f"moyenne ± 1 écart-type (4e trimestre) : {fr(r4.seuil_bas)} % à {fr(r4.seuil_haut)} %"),
                    Line2D([], [], color=MUTED, ls=":", label=f"même bande, moyenne des 4 trimestres : {fr(rm.seuil_bas)} % à {fr(rm.seuil_haut)} %"),
                    Line2D([], [], color=MUTED, lw=0.8, ls="--", label="seuil de stagnation du 02 : 2 %"),
                    Line2D([], [], marker="D", ls="", color=INK, mec=SURFACE, label="croissance selon la moyenne des 4 trimestres")],
           loc="upper left", fontsize=7.1, ncol=2, columnspacing=1.2)

q["x"] = q.an + (q.trimestre - 0.5) / 4
ok = q[q.traverse.isna()]
ax2.axvspan(2020, 2022, color=BANDE, zorder=0)
ax2.text(2022.15, 47, "comparaisons qui traversent\nune rupture (2020, 2021)", ha="left", fontsize=7, color=INK2, va="top")
ax2.plot(q.x, q.glissement_T_T4_pct, color=MUTED, lw=1, ls="--")
for seg in (ok[ok.an < 2020], ok[ok.an >= 2022]):
    ax2.plot(seg.x, seg.glissement_T_T4_pct, color=INK2, lw=1.6, marker="o", ms=3.5, mec=SURFACE)
ax2.axhline(0, color=AXE, lw=0.8)
axe_annees(ax2, 2011, 2025)
ax2.set_xlim(2010.7, 2026.8)
ax2.set_ylim(-10, 50)
ax2.set_ylabel("%")
ax2.set_title("Glissement trimestriel (trimestre face au même trimestre un an plus tôt), lu sans classe", fontsize=9.5)

e2 = frise(ax3, ev, 2010, 2026)
axe_annees(ax3, 2011, 2025)
ax3.set_xlim(2010.7, 2026.8)
liste(axl, e2)
fig.suptitle("Abonnements data mobile : trois accélérations avant 2017, ralentissement depuis 2022",
             x=0.01, ha="left", fontsize=12, fontweight="bold", y=0.955)
finir(fig, "f2_o1_02_abonnements",
      "Sources : INSEED (valeurs annuelles, 2010-2017) ; ARCEP (trimestres, depuis 2017) ; chronologie des événements. Ruptures : reclassement de la 3G de Togocel (1er trim. 2020) ; "
      "révision de 2021 par l'ARCEP.\nSensibilité : 2022 reste un ralentissement dans toutes les variantes ; 2023 à 2025 dépendent de la période (2015-2024) ou du traitement des ruptures.\nTables : o1_02_abonnements.csv, o1_02_abonnements_trimestres.csv, o1_02_references.csv, o1_02_evenements.csv")

# =============================================================== F3 — O1-01 Pénétration d'Internet, seuil de 40 % et repère régional
o = lire("o1_01_penetration")
pmes = lire("o1_01_points_mesures")
fig, ax = plt.subplots(figsize=(9, 4.4))
ax.axhspan(40, 60, color=BANDE, zorder=0)
ax.axhline(40, color=INK2, lw=0.9, ls="--")
ax.text(2000.3, 41, "40 % : seuil du 02 (hypothèse du sujet)", fontsize=7.6, color=INK2, va="bottom")
ax.text(2000.3, 58.5, "rattrapage (40 à 60 %)", fontsize=7.6, color=INK2, va="top")
ax.plot(o.annee, o.pct_population, color=BLEU, lw=2.2, label="Togo, % de la population (UIT, estimations sauf 2017)")
ax.plot(o.annee, o.afrique_subsaharienne_pct, color=INK, lw=1.3, ls=":", label="Afrique subsaharienne (UIT)")
for src, m, lab in (("Findex", "D", "Findex 2024 : 15 ans et plus, 3 derniers mois"), ("Afrobaromètre", "o", "Afrobaromètre : 18 ans et plus, toute fréquence")):
    d = pmes[pmes.source.str.startswith(src)]
    ax.scatter(d.vague.astype(str).str[:4].astype(int), d.estimation_pct, marker=m, s=30, color=SURFACE, edgecolor=INK2, lw=1.2,
               zorder=4, label=lab)
d = o.iloc[-1]
ax.annotate(f"{fr(d.pct_population, 2)} % en {int(d.annee)}", (d.annee, d.pct_population), xytext=(-10, 16), textcoords="offset points",
            ha="right", fontsize=8, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
ax.set_xlim(2000, 2025.5)
ax.set_ylim(0, 66)
ax.set_ylabel("%")
ax.legend(loc="upper left", fontsize=7.6, bbox_to_anchor=(0, 0.57))
ax.set_title("O1-01 : le Togo reste sous le seuil de 40 % (déficit d'usage), de peu ; les enquêtes le placent au-dessus")
finir(fig, "f3_o1_01_penetration", "Les enquêtes ont d'autres définitions et d'autres âges : elles situent le Togo, elles ne se comparent pas au taux de l'UIT. "
      "Tables : o1_01_penetration.csv, o1_01_points_mesures.csv")

# =============================================================== F4 — O4-05 Statut d'accès financier (commune, préfecture)
import sys  # noqa: E402

import geopandas as gpd  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "prep"))
from commun import CRS_SURFACE, GEO  # noqa: E402

STATUTS = {"desserte diversifiée": "#2a78d6", "desserte faible": "#eda100", "mobile money dominant": "#4a3aa7",
           "mobile money uniquement": "#e34948"}  # palette validée (toutes paires, mode clair)
gc = gpd.read_file(GEO / "communes.geojson").to_crs(CRS_SURFACE).merge(lire("o4_communes")[["code", "statut_O4_05"]], on="code")
gp = gpd.read_file(GEO / "prefectures.geojson").to_crs(CRS_SURFACE).merge(lire("o4_prefectures")[["code", "statut_O4_05"]], on="code")
syn = lire("o4_synthese_classes")
fig, axes = plt.subplots(1, 2, figsize=(8, 8.4))
for ax, g, titre, maille in ((axes[0], gc, "Par commune", "commune"), (axes[1], gp, "Par préfecture", "préfecture")):
    for st, col in STATUTS.items():
        g[g.statut_O4_05 == st].plot(ax=ax, color=col, edgecolor=SURFACE, linewidth=0.3)
    gp.boundary.plot(ax=ax, color=INK2, linewidth=0.35)
    ax.set_axis_off()
    ax.set_aspect("equal")
    ax.set_title(titre)
h = []
for st, col in STATUTS.items():
    s = syn[(syn.indicateur == "O4_05") & (syn.classe == st)].set_index("maille")
    nc = int(s.territoires.get("commune", 0))
    npf = int(s.territoires.get("préfecture", 0))
    pl = lambda n, mot: "aucune " + mot if n == 0 else f"{n} {mot}{'s' if n > 1 else ''}"  # noqa: E731
    h.append(Patch(color=col, label=f"{st} : {pl(nc, 'commune')}, {pl(npf, 'préfecture')}"))
fig.legend(handles=h, loc="upper center", bbox_to_anchor=(0.5, 0.06), ncol=2, fontsize=7.6, title="Règle en cascade du 02 (première condition vraie)",
           title_fontsize=7.8)
fig.suptitle("O4-05 : le mobile money domine presque partout ;\n22 communes n'ont que lui", x=0.01, ha="left", fontsize=11, fontweight="bold")
finir(fig, "f4_o4_05_statut", "« Mobile money dominant » : au moins un point formel, et plus de 20 points mobile money par point formel ou plus de 30 000 habitants "
      "par point formel.\nAucun territoire « non desservi » ni « non déterminable ». Tables : o4_communes.csv, o4_prefectures.csv, o4_synthese_classes.csv", )

# =============================================================== F5 — O4-06 Matrice statut × couverture (proxy), pondérée par la population
fig, axes = plt.subplots(1, 2, figsize=(12, 3.9), gridspec_kw={"wspace": 0.55})
COUV = ["zone blanche prioritaire (proxy)", "couverture partielle (proxy)", "territoire couvert (proxy)", "non déterminable (A13)"]
LIGNES = list(STATUTS)
for ax, nom, titre in ((axes[0], "o4_06_matrice_communes", "Communes"), (axes[1], "o4_06_matrice_prefectures", "Préfectures")):
    m = lire(nom).set_index("statut_O4_05").reindex(index=LIGNES, columns=COUV).fillna(0)
    tot = m.values.sum()
    for i, st in enumerate(LIGNES):
        for j, cv in enumerate(COUV):
            v = m.loc[st, cv]
            critique = st.startswith("mobile money") and cv.startswith("zone blanche")
            ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor="#fbe3e2" if critique else SURFACE, edgecolor=GRID))
            if v > 0:
                ax.scatter(j, i, s=1400 * np.sqrt(v / tot), color=STATUTS[st], alpha=0.85, edgecolor=SURFACE)
                ax.text(j, i + 0.36, f"{fr(v / 1e3)} k", ha="center", va="center", fontsize=7.2, color=INK)
    ax.set_xticks(range(4))
    ax.set_xticklabels(["moins de 50 %", "50 à 85 %", "plus de 85 %", "non déterminable"], fontsize=7.6)
    ax.set_yticks(range(4))
    ax.set_yticklabels(LIGNES, fontsize=7.6)
    ax.set_xlim(-0.5, 3.5)
    ax.set_ylim(3.5, -0.5)
    ax.grid(False)
    ax.set_xlabel("Couverture réseau (proxy 3i)", fontsize=8)
    ax.set_title(titre)
fig.suptitle("O4-06 : 8 communes en cellule critique (368 534 habitants), aucune préfecture ; toutes « à confirmer »",
             x=0.01, ha="left", fontsize=11, fontweight="bold", y=1.04)
finir(fig, "f5_o4_06_matrice", "Taille des disques : population ; « k » = milliers d'habitants. Cellule rose : critique au sens du 02 (mobile money uniquement ou dominant, "
      "couverture de moins de 50 %).\nCouverture = proxy de niveau C : toute cellule critique est « à confirmer » ; 3 des 8 communes critiques ont une valeur douteuse (P6). "
      "Tables : o4_06_matrice_communes.csv, o4_06_matrice_prefectures.csv, o4_06_cellules.csv")
print(f"5 figures écrites dans {FIG}")
