"""Figures du 05 (exploration). Lit les tables de data/analysis/05_eda/ et écrit des PNG dans figures/.

Palette de référence validée (skill dataviz, validate_palette.js, mode clair) : créneaux 1 à 3 pour les nuages
de points et les courbes (toutes paires), 1 à 5 pour les barres empilées (paires adjacentes). Un seul axe par
graphique ; les grandeurs de nature différente vont dans des panneaux séparés. Chaque figure a sa table CSV.
"""
from pathlib import Path

import matplotlib
import matplotlib.ticker

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

ICI = Path(__file__).resolve().parents[1] / "data" / "analysis" / "05_eda"
FIG = ICI / "figures"
FIG.mkdir(parents=True, exist_ok=True)

SURFACE, INK, INK2, MUTED, GRID, AXE = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
S = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]  # créneaux 1 à 5
# Sur les figures, aucun sigle sans son sens en clair
L_FORMELS = "Points formels (banques, microfinance, assurances)"
L_DAB = "Distributeurs automatiques de billets (DAB)"
L_MM = "Points mobile money"
plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "font.family": "sans-serif", "font.size": 9.5, "text.color": INK, "axes.labelcolor": INK2,
    "axes.edgecolor": AXE, "axes.linewidth": 0.8, "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
    "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False, "lines.linewidth": 1.6,
    "axes.titlesize": 11, "axes.titleweight": "bold", "axes.titlelocation": "left", "axes.titlecolor": INK})


def lire(nom):
    return pd.read_csv(ICI / f"{nom}.csv")


def finir(fig, nom, source):
    fig.text(0.01, -0.01, source, color=MUTED, fontsize=7.5, ha="left", va="top")
    fig.savefig(FIG / f"{nom}.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def fr(x, d=0):
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",")


# F1 — Part de la population et parts des points, par unité régionale
p = lire("s2_parts_unites_regionales").sort_values("part_pop_totale")
fig, ax = plt.subplots(figsize=(7.2, 3.6))
y = np.arange(len(p))
for yy, a, b in zip(y, p.part_pop_totale, p[["part_n_formels", "part_n_mm", "part_n_dab"]].max(axis=1)):
    ax.plot([min(a, b), max(a, b)], [yy, yy], color=GRID, lw=1.2, zorder=1)
ax.scatter(p.part_pop_totale, y, s=70, color=SURFACE, edgecolor=INK2, linewidth=1.4, zorder=3, label="Population")
for col, c, lab, m in (("part_n_formels", S[0], L_FORMELS, "o"), ("part_n_mm", S[1], L_MM, "s"),
                       ("part_n_dab", S[2], L_DAB, "D")):
    dy = {"part_n_formels": -0.16, "part_n_mm": 0.0, "part_n_dab": 0.16}[col]
    ax.scatter(p[col], y + dy, s=48, color=c, marker=m, edgecolor=SURFACE, linewidth=1.5, zorder=4, label=lab)
ax.set_yticks(y, p.nom)
ax.set_xlabel("Part du total national (%)")
ax.set_xlim(0, 62)
ax.grid(axis="y", visible=False)
gl = p[p.code == "GL"].iloc[0]
ax.annotate(f"{fr(gl.part_n_dab, 1)} %", (gl.part_n_dab, len(p) - 1 + 0.16), xytext=(-8, 0), textcoords="offset points",
            ha="right", va="center", color=INK2, fontsize=8.5)
ax.set_title("Le Grand Lomé concentre les distributeurs de billets bien plus que la population")
ax.legend(loc="lower right", fontsize=8.2, ncol=1)
finir(fig, "f1_parts_unites_regionales", "Sources : recensement des établissements financiers, des DAB et des points mobile money (2021/2022) ;\nrecensement de la population (RGPH-5, 2022). Table : s2_parts_unites_regionales.csv")

# F2 — Courbes de concentration (communes)
import sys  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
com = pd.read_csv(ICI.parents[1] / "processed" / "terr_commune.csv")
conc = lire("s2_concentration").set_index("variable")
fig, ax = plt.subplots(figsize=(5.4, 5.0))
ax.plot([0, 1], [0, 1], color=AXE, lw=1, zorder=1)
for col, c, lab, cle in (("n_formels", S[0], L_FORMELS, "Points formels"), ("n_mm", S[1], L_MM, "Points mobile money"),
                         ("n_dab", S[2], L_DAB, "Sites de DAB")):
    d = com[[col, "pop_totale"]].assign(t=lambda x: x[col] / x.pop_totale).sort_values("t")
    xx = np.concatenate([[0], d.pop_totale.cumsum() / d.pop_totale.sum()])
    yy = np.concatenate([[0], d[col].cumsum() / d[col].sum()])
    ax.plot(xx, yy, color=c, lw=1.8, label=f"{lab} : Gini {fr(conc.loc[cle, 'gini_communes'], 2)}")
ax.set_xlabel("Part cumulée de la population (communes, de la moins à la mieux dotée)")
ax.set_ylabel("Part cumulée des points")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_title("Les distributeurs de billets sont bien plus concentrés\nque le mobile money")
ax.legend(loc="upper left", fontsize=7.8)
ax.text(0.99, 0.02, "Indice de Gini : mesure l'inégalité de répartition\ndes points par rapport à la population.\n"
        "0 = les points suivent exactement la population ;\nplus il approche de 1, plus ils se concentrent\n"
        "dans quelques communes.", transform=ax.transAxes, ha="right", va="bottom", fontsize=7.8, color=INK2,
        bbox=dict(boxstyle="round,pad=0.4", fc=SURFACE, ec=GRID))
ax.text(0.40, 0.44, "répartition proportionnelle", color=MUTED, fontsize=8, rotation=42, ha="center", va="center")
finir(fig, "f2_concentration_communes", "117 communes ; population RGPH-5 2022. Table : s2_concentration.csv")

# F3 — Ratios par strate (communes), deux panneaux
com_r = com.assign(formels_10k=1e4 * com.n_formels / com.pop_totale, mm_10k=1e4 * com.n_mm / com.pop15_prorata)
ordre = [("grand_lome", "Grand Lomé"), ("autres_villes", "Autres villes"), ("rural", "Rural")]
fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.6))
rng = np.random.default_rng(7)
for ax, col, titre in ((axes[0], "formels_10k", "Points formels (banques, microfinance, assurances)\npour 10 000 habitants"),
                       (axes[1], "mm_10k", "Points mobile money\npour 10 000 adultes")):
    for i, ((k, lab), c, m) in enumerate(zip(ordre, S[:3], ("o", "s", "D"))):
        v = com_r[com_r.strate_50 == k][col]
        ax.scatter(i + rng.uniform(-0.18, 0.18, len(v)), v, s=20, color=c, marker=m, alpha=0.75, edgecolor=SURFACE,
                   linewidth=0.5)
        ax.plot([i - 0.28, i + 0.28], [v.median()] * 2, color=INK, lw=2)
        ax.annotate(fr(v.median(), 2 if col == "formels_10k" else 1), (i + 0.3, v.median()), va="center", fontsize=8.5, color=INK)
    ax.set_xticks(range(3), [l for _, l in ordre])
    ax.set_title(titre, fontsize=10)
    ax.grid(axis="x", visible=False)
fig.suptitle("L'écart est urbain / rural plus qu'entre Lomé et les autres villes", x=0.01, ha="left",
             fontweight="bold", fontsize=11)
fig.tight_layout()
finir(fig, "f3_ratios_par_strate", "Un point = une commune, couleur = strate ; trait noir = médiane. Autres villes : communes à 50 % d'urbains ou plus. Table : s5_strates_ratios.csv")

# F4 — Usage d'Internet : estimations UIT (courbes) et enquêtes (panneau séparé, une courbe par source)
d1 = lire("s4_usage_internet_d1")
bmk = pd.read_csv(ICI.parents[1] / "processed" / "benchmark.csv")
ssa = bmk[(bmk.iso3 == "SSF") & (bmk.indicateur == "usage_internet_pct_population") & (bmk.annee >= 2005)]
enq = lire("s4_usage_internet_enquetes")
fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.8), sharey=True)
ax = axes[0]
ax.plot(d1.annee.astype(int), d1.pct_population, color=S[0], lw=1.8, label="Togo (estimations, sauf 2017 : INSEED)")
ax.plot(ssa.annee, ssa.valeur, color=S[1], lw=1.8, label="Afrique subsaharienne (série disponible depuis 2005)")
ax.annotate("1996 : premiers\nutilisateurs (0,01 %)", (1996, 0.2), xytext=(12, 40), textcoords="offset points",
            ha="left", fontsize=7.8, color=INK2, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
ax.annotate(f"{fr(d1.pct_population.iloc[-1], 1)} %", (2024, d1.pct_population.iloc[-1]), xytext=(4, 0),
            textcoords="offset points", va="center", fontsize=8.5)
ax.set_title("Union internationale des télécommunications (UIT),\n% de la population", fontsize=10)
ax.legend(loc="upper left", fontsize=8)
ax = axes[1]
for src, c, lab, m in (("Afrobaromètre", S[0], "Afrobaromètre : usage, toute fréquence (18 ans et +)", "o"),
                       ("EHCVM", S[1], "Enquête ménages EHCVM : accès déclaré (15 ans et +)", "s"),
                       ("Findex", S[2], "Findex (Banque mondiale) : usage sur 3 mois (15 ans et +)", "D")):
    e = enq[enq.source.str.startswith(src)].copy()
    e["an"] = e.vague.astype(str).str[:4].astype(int)
    e = e.sort_values("an")
    ax.errorbar(e.an, e.estimation_pct, yerr=[e.estimation_pct - e.ic95_bas.fillna(e.estimation_pct),
                                              e.ic95_haut.fillna(e.estimation_pct) - e.estimation_pct],
                color=c, marker=m, ms=6, lw=1.6, elinewidth=1, capsize=0, label=lab, mec=SURFACE, mew=1)
ax.set_title("Enquêtes auprès des ménages\n(définitions différentes : jamais comparées entre elles)", fontsize=10)
ax.legend(loc="lower right", fontsize=7.8)
ax.set_xlim(2010, 2026)
axes[0].set_xlim(1995, 2026)
axes[0].xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(5))
axes[0].xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter("%d"))
fig.suptitle("L'usage d'Internet a au moins doublé depuis 2017, quelle que soit la source", x=0.01, ha="left",
             fontweight="bold", fontsize=11)
fig.tight_layout()
finir(fig, "f4_usage_internet", "Sources : UIT via Banque mondiale ; Afrobaromètre ; EHCVM (INSEED) ; Findex. Barres : intervalle de confiance à 95 %. Tables : s4_usage_internet_d1.csv, s4_usage_internet_enquetes.csv")

# F5 — Mix technologique des abonnements data mobile (T4)
mix = lire("s4_mix_technologique_T4").set_index("annee")
cols = ["2G", "3G+4G (Moov, non ventilé)", "3G", "4G"]
lab = {"2G": "2G", "3G+4G (Moov, non ventilé)": "3G et 4G de Moov, non ventilées", "3G": "3G", "4G": "4G", "5G": "5G"}
col_c = {"2G": S[4], "3G+4G (Moov, non ventilé)": S[3], "3G": S[1], "4G": S[0], "5G": S[2]}
fig, ax = plt.subplots(figsize=(7.2, 3.8))
bas = np.zeros(len(mix))
for c in cols:
    v = mix[c].values
    ax.bar(mix.index, v, bottom=bas, width=0.62, color=col_c[c], edgecolor=SURFACE, linewidth=1.5, label=lab[c])
    bas += v
for a, v in zip(mix.index, mix["4G"]):
    if v >= 15:
        ax.text(a, mix.loc[a, ["2G", "3G+4G (Moov, non ventilé)", "3G"]].sum() + v / 2, f"{fr(v)} %",
                ha="center", va="center", color="white", fontsize=8.5, fontweight="bold")
ax.set_ylim(0, 100)
ax.set_ylabel("% des abonnements data mobile (4e trimestre)")
ax.set_title("La 4G devient majoritaire en 2025 ; la 2G recule")
h, l = ax.get_legend_handles_labels()
ax.legend(h[::-1], l[::-1], loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=8.5)
ax.grid(axis="x", visible=False)
ax.axvline(2019.5, color=INK2, lw=0.8)
ax.text(2019.44, 3, "rupture de série (1er trim. 2020)", color=INK2, fontsize=7.5, va="bottom", ha="right", rotation=90)
finir(fig, "f5_mix_technologique", "Source : ARCEP (valeur du 4e trimestre, par convention). 5G : 3 951 abonnés au 2e trimestre 2026, hors figure. Table : s4_mix_technologique_T4.csv")

# F6 — Parts de Togocom selon trois mesures
pt = lire("s4_parts_togocom")
fig, ax = plt.subplots(figsize=(7.2, 3.6))
for col, c, lab in (("telephonie_D3", S[0], "Abonnés à la téléphonie (INSEED)"), ("data_mobile_ARCEP", S[1], "Abonnés data mobile (ARCEP)"),
                    ("ca_mobile_ARCEP", S[2], "Chiffre d'affaires mobile (ARCEP)")):
    d = pt.dropna(subset=[col])
    ax.plot(d.annee, d[col], color=c, marker="o", ms=4.5, mec=SURFACE, mew=1, label=lab)
ax.axhline(50, color=AXE, lw=0.8)
ax.annotate("2020 : rupture de série\n(3G de Togocel reclassée)", (2020, pt.set_index("annee").loc[2020, "data_mobile_ARCEP"]),
            xytext=(10, 0), textcoords="offset points", fontsize=7.8, color=INK2, va="center")
ax.set_ylim(30, 75)
ax.set_ylabel("Part de Togocom (%) ; Moov = 100 - part")
ax.set_title("Togocom domine, surtout en chiffre d'affaires")
ax.legend(loc="upper left", fontsize=8.3)
finir(fig, "f6_parts_togocom", "Téléphonie par opérateur : publiée par l'INSEED de 2013 à 2019 seulement ; l'ARCEP ne la donne qu'en graphique. Table : s4_parts_togocom.csv")

# F7 — CA et investissement du secteur (même unité, un seul axe)
cai = lire("s4_ca_investissement")
fig, ax = plt.subplots(figsize=(7.2, 3.6))
for col, c, lab in (("ca_secteur_2b", S[0], "Chiffre d'affaires du secteur (INSEED)"), ("ca_secteur_ARCEP", S[1], "Chiffre d'affaires du secteur (ARCEP)"),
                    ("investissement_ARCEP", S[2], "Investissement (ARCEP)")):
    d = cai.dropna(subset=[col])
    ax.plot(d.annee, d[col], color=c, marker="o", ms=4.5, mec=SURFACE, mew=1, label=lab)
ax.axvspan(2020.5, 2023.1, color=GRID, alpha=0.6, lw=0)
ax.text(2020.62, 165, "ARCEP : chiffre\nd'affaires fixe\npublié sans GVA\n(1er trim. 2021 -\n1er trim. 2023)", fontsize=7.5, color=INK2, va="top")
ax.set_ylabel("Milliards de FCFA")
ax.set_ylim(0, 280)
ax.set_title("Deux séries de chiffre d'affaires, affichées côte à côte, sans raccord")
ax.legend(loc="lower left", fontsize=8.3)
finir(fig, "f7_ca_investissement", "ARCEP : Autorité de régulation des communications électroniques. Flux annuels = somme des 4 trimestres. Table : s4_ca_investissement.csv")

# F8 — Mobile money national : petits multiples (unités différentes)
mm = lire("s4_mobile_money")
fx = lire("s4_findex")
fig, axes = plt.subplots(1, 3, figsize=(10, 3.2))
d = mm.dropna(subset=["points_de_vente_T4"])
axes[0].bar(d.annee, d.points_de_vente_T4 / 1e3, width=0.6, color=S[0], edgecolor=SURFACE)
axes[0].set_title("Points de vente\n(milliers, 4e trimestre)", fontsize=10)
axes[0].text(2025, d.points_de_vente_T4.iloc[-1] / 1e3, fr(d.points_de_vente_T4.iloc[-1] / 1e3, 1), ha="center",
             va="bottom", fontsize=8.5)
for col, c, lab in (("valeur_transactions_Md_2b", S[0], "INSEED"), ("valeur_transactions_Md_ARCEP", S[1], "ARCEP")):
    dd = mm.dropna(subset=[col])
    axes[1].plot(dd.annee, dd[col], color=c, marker="o", ms=4, mec=SURFACE, label=lab)
axes[1].set_title("Valeur des transactions\n(milliards de FCFA)", fontsize=10)
axes[1].legend(fontsize=8)
dd = fx.dropna(subset=["compte_mobile_money"])
axes[2].plot(dd.vague, dd.compte_mobile_money, color=S[0], marker="o", ms=5, mec=SURFACE, label="Compte mobile money")
dd = fx.dropna(subset=["compte_institution_financiere"])
axes[2].plot(dd.vague, dd.compte_institution_financiere, color=S[1], marker="s", ms=5, mec=SURFACE, label="Compte en institution financière")
axes[2].set_title("Adultes détenteurs\nd'un compte (%)", fontsize=10)
axes[2].legend(fontsize=7.8, loc="upper left")
for a in axes:
    a.grid(axis="x", visible=False)
    a.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True, nbins=5))
fig.suptitle("Depuis 2021, plus d'adultes ont un compte mobile money qu'un compte en institution financière (Findex)",
             x=0.01, ha="left", fontweight="bold", fontsize=11)
fig.tight_layout()
finir(fig, "f8_mobile_money_national", "Sources : ARCEP, INSEED, Findex (Banque mondiale). Tables : s4_mobile_money.csv, s4_findex.csv")

# F9 — Offre de mobile money et usage déclaré, par région (6 points)
od = lire("s6_offre_demande_regions")
bas_ic = od.ic95.str.split("-").str[0].astype(float)
haut_ic = od.ic95.str.split("-").str[1].astype(float)
fig, ax = plt.subplots(figsize=(6.4, 4.0))
ax.errorbar(od.mm_pour_10k_adultes, od.usage_mobile_banking_2021_pct,
            yerr=[od.usage_mobile_banking_2021_pct - bas_ic, haut_ic - od.usage_mobile_banking_2021_pct],
            fmt="o", color=S[0], ms=7, mec=SURFACE, mew=1.2, elinewidth=1, capsize=0)
for _, r in od.iterrows():
    gauche = r.code == "A_HGL"
    ax.annotate(r.unite, (r.mm_pour_10k_adultes, r.usage_mobile_banking_2021_pct), xytext=(-7 if gauche else 7, 0),
                textcoords="offset points", va="center", ha="right" if gauche else "left", fontsize=8.5, color=INK)
ax.set_xlabel("Points mobile money pour 10 000 adultes (recensement des points, 2021/2022)")
ax.set_ylabel("Adultes faisant du mobile banking (%)\nenquête ménages EHCVM 2021/22")
ax.set_xlim(15, 60)
ax.set_ylim(0, 70)
ax.set_title("La Centrale : beaucoup de points, peu d'usage")
finir(fig, "f9_offre_usage_regions", "Barres : intervalle de confiance à 95 %. Table : s6_offre_demande_regions.csv")

# F10 — Points formels et points mobile money, par commune
fig, ax = plt.subplots(figsize=(6.8, 4.4))
for (k, lab), c, m in zip(ordre, S[:3], ("o", "s", "D")):
    d = com_r[com_r.strate_50 == k]
    ax.scatter(d.formels_10k, d.mm_10k, s=28, color=c, marker=m, edgecolor=SURFACE, linewidth=0.8, label=lab, alpha=0.9)
for _, r in com_r.nlargest(3, "mm_10k").iterrows():
    ax.annotate(r.nom, (r.formels_10k, r.mm_10k), xytext=(5, 0), textcoords="offset points", fontsize=8, va="center")
z = com_r[com_r.n_formels == 0]
ax.annotate(f"{len(z)} communes sans point formel", (0, z.mm_10k.max()), xytext=(10, 12), textcoords="offset points",
            fontsize=8, color=INK2, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
ax.set_xlabel("Points formels (banques, microfinance, assurances) pour 10 000 habitants")
ax.set_ylabel("Points mobile money pour 10 000 adultes")
ax.set_title("Là où l'offre formelle est dense, le mobile money l'est aussi")
ax.legend(fontsize=8.5, loc="upper right")
finir(fig, "f10_formels_mm_communes", "117 communes, couleur = strate. Corrélation de rang (Spearman) : 0,50. Table : s6_correlations_spearman.csv")

# F11 — Togo face aux pays de l'UEMOA et à l'Afrique subsaharienne (repère de O1-01)
bu = lire("s4_benchmark_usage_internet")
NOMS = {"BEN": "Bénin", "BFA": "Burkina Faso", "CIV": "Côte d'Ivoire", "GNB": "Guinée-Bissau", "MLI": "Mali",
        "NER": "Niger", "SEN": "Sénégal", "TGO": "Togo", "SSF": "Afrique subsaharienne"}
fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.3), gridspec_kw={"width_ratios": [1.5, 1]})
ax = axes[0]
# Une couleur par pays, dans l'ordre fixe de la palette validée (8 créneaux, courbes : paires adjacentes) :
# le Togo prend le créneau 1, les autres pays suivent l'ordre alphabétique de leur code, jamais leur rang.
S8 = S + ["#008300", "#4a3aa7", "#e34948"]
COUL = {"TGO": S8[0], **{iso: S8[i + 1] for i, iso in enumerate(["BEN", "BFA", "CIV", "GNB", "MLI", "NER", "SEN"])}}
fin = bu[bu.annee == 2024].set_index("iso3").valeur
lignes = {}
for iso, d in bu[bu.annee >= 2005].groupby("iso3"):
    if iso == "SSF":
        lignes[iso] = ax.plot(d.annee, d.valeur, color=INK, lw=1.4, ls="--")[0]
    else:
        lignes[iso] = ax.plot(d.annee, d.valeur, color=COUL[iso], lw=2.6 if iso == "TGO" else 1.3,
                              zorder=4 if iso == "TGO" else 2)[0]
ordre = fin.sort_values(ascending=False).index
ax.legend([lignes[i] for i in ordre], [f"{NOMS[i]} : {fr(fin[i], 1)} %" for i in ordre], loc="upper left", fontsize=7.4,
          title="En 2024", title_fontsize=7.6, alignment="left")
tgo = bu[(bu.iso3 == "TGO") & (bu.annee >= 2005)]
ax.annotate("Togo", (2024, tgo.valeur.iloc[-1]), xytext=(5, 0), textcoords="offset points", va="center", fontsize=8.5,
            fontweight="bold", color=INK)
ax.set_xlim(2005, 2026.5)
ax.set_xticks(range(2005, 2026, 5))
ax.set_ylim(0, 65)
ax.set_ylabel("% de la population")
ax.set_title("Usage d'Internet, 2005-2024", fontsize=10)
ax = axes[1]
rg = bu[bu.iso3 == "TGO"]
ax.step(rg.annee, rg.rang_uemoa_sur_8, where="mid", color=S[0], lw=2)
for an, dx, dy in ((2000, 6, 8), (2017, 0, -16), (2024, -6, 8)):
    v = rg.loc[rg.annee == an, "rang_uemoa_sur_8"].iloc[0]
    ax.annotate(f"{int(v)}e" if v > 1 else "1er", (an, v), xytext=(dx, dy), textcoords="offset points", ha="center",
                fontsize=8, color=INK)
ax.set_ylim(8.5, 0.3)
ax.set_yticks(range(1, 9))
ax.set_xlim(1999, 2025)
ax.set_ylabel("Rang (1 = usage le plus élevé)")
ax.set_title("Rang du Togo parmi les 8 pays de l'UEMOA", fontsize=10)
fig.suptitle("Premier de l'UEMOA en 2000, 5e ou 6e de 2013 à 2018, le Togo est 3e depuis 2022",
             x=0.01, ha="left", fontsize=11.5, fontweight="bold")
fig.tight_layout()
finir(fig, "f11_benchmark_uemoa", "Source : UIT via Banque mondiale (estimations pour la plupart des valeurs, des deux côtés). "
      "La moyenne de l'Afrique subsaharienne commence en 2005.\nTable : s4_benchmark_usage_internet.csv")

# F12 — Structure par opérateur des points mobile money (barres empilées à 100 %, paires adjacentes)
op = lire("s2_mm_operateurs").set_index("code")
ordre = ["national", "GL", "B", "A_HGL", "E", "D", "C"]  # national, puis unités par population (comme la figure 1)
CATS = [("mm_deux_operateurs", "Les deux opérateurs", S[0], SURFACE), ("mm_togocom_seul", "Togocom seul", S[1], SURFACE),
        ("mm_moov_seul", "Moov seul", S[2], INK), ("mm_operateur_non_renseigne", "Opérateur non renseigné", AXE, INK)]
fig, ax = plt.subplots(figsize=(8.6, 3.9))
y = np.arange(len(ordre))[::-1]
gauche = np.zeros(len(ordre))
for col, lab, c, txt in CATS:
    v = op.loc[ordre, f"part_{col}_pct"].values
    ax.barh(y, v, left=gauche, color=c, edgecolor=SURFACE, linewidth=1.5, height=0.66, label=lab)
    for yi, g, vi in zip(y, gauche, v):
        if vi >= 5:
            ax.text(g + vi / 2, yi, f"{fr(vi, 0)} %", ha="center", va="center", fontsize=7.8, color=txt)
    gauche += v
noms = [f"{op.loc[k, 'nom']} ({fr(op.loc[k, 'total'])})" for k in ordre]
ax.set_yticks(y)
ax.set_yticklabels(noms)
ax.get_yticklabels()[0].set_fontweight("bold")
ax.set_xlim(0, 100)
ax.set_xlabel("% des points mobile money de l'unité")
ax.grid(axis="y", visible=False)
ax.set_title("Deux points sur trois sont servis par les deux opérateurs ;\nKara et la Centrale dépendent surtout de Togocom", pad=24)
ax.legend(loc="lower left", bbox_to_anchor=(0, 1.0), ncol=4, fontsize=8, borderaxespad=0.3, handlelength=1.4)
finir(fig, "f12_mm_operateurs", "Entre parenthèses : nombre de points. Un point servi par les deux opérateurs compte une fois ; les vues par opérateur "
      "ne s'additionnent pas.\nSource : recensement des points mobile money (2021/2022). Table : s2_mm_operateurs.csv")

# F13 — Passage à la fibre : Internet fixe total et abonnés FTTH par opérateur (trimestriel)
fb = lire("s4_fibre")
fb["x"] = fb.periode.str[:4].astype(int) + (fb.periode.str[-1].astype(int) - 0.5) / 4
fig, ax = plt.subplots(figsize=(9, 4.2))
ax.plot(fb.x, fb.internet_fixe_total / 1e3, color=INK, lw=1.6, label="Internet fixe, tous opérateurs et technologies")
g_av = fb[fb.ftth_gva.isna() & fb.internet_fixe_gva.notna()]
ax.plot(g_av.x, g_av.internet_fixe_gva / 1e3, color=S[0], lw=1.6, ls="--", label="GVA : Internet fixe (fibre non isolée avant 2024)")
ax.plot(fb.x, fb.ftth_gva / 1e3, color=S[0], lw=2.2, marker="o", ms=3.5, mec=SURFACE, label="GVA : fibre (FTTH)")
ax.plot(fb.x, fb.ftth_togo_telecom / 1e3, color=S[1], lw=2.2, marker="o", ms=3.5, mec=SURFACE, label="Togo Telecom : fibre (FTTH)")
ax.annotate("fin de l'EvDo de Togo Telecom\n(25 679 abonnés au 1er trim. 2018, 0 au 2e)", (2018.375, 18.8), xytext=(2018.45, 92),
            fontsize=7.6, color=INK2, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
ax.axvspan(2021.75, 2024.0, color=GRID, alpha=0.5, zorder=0)
ax.text(2022.87, 5, "fibre de Togo Telecom\nnon publiée à part", ha="center", fontsize=7.4, color=INK2)
d = fb.iloc[-1]
ax.text(2024.15, 2, f"2e trim. 2026 : {fr(d.ftth_total / 1e3, 1)} milliers\nd'abonnés FTTH, soit {fr(d.part_ftth_internet_fixe_pct, 1)} %\n"
        f"de l'Internet fixe et {fr(d.part_ftth_data_mobile_pct, 1)} %\ndes abonnements data mobile", fontsize=7.4, color=INK, va="bottom")
ax.set_xlim(2016.8, 2026.8)
ax.set_ylim(0, 185)
ax.set_ylabel("Abonnés (milliers)")
ax.set_title("Passage à la fibre : l'Internet fixe se reconstruit sur la fibre depuis 2018")
ax.legend(loc="upper left", fontsize=7.8)
finir(fig, "f13_fibre", "Source : ARCEP, séries trimestrielles. Premiers abonnés FTTH : 92 au 4e trimestre 2017 (Togo Telecom). "
      "La fibre est publiée à part pour tous les opérateurs depuis le 1er trimestre 2024.\nTable : s4_fibre.csv")
print("13 figures écrites dans", FIG)
