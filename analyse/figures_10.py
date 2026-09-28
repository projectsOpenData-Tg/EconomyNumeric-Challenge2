"""Figures du 10 (recommandations). Lit les tables de data/analysis/10_recommandations/ et du 07, écrit des PNG dans figures/.

F1 : scénarios d'usage d'Internet (O1-01) à 2030, trois rythmes tirés d'O1-02 (palette catégorielle validée, ordre fixe).
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

A = Path(__file__).resolve().parents[1] / "data" / "analysis"
ICI, IND = A / "10_recommandations", A / "07_indicateurs"
FIG = ICI / "figures"
FIG.mkdir(parents=True, exist_ok=True)

SURFACE, INK, INK2, MUTED, GRID, AXE = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
S = ["#2a78d6", "#eb6834", "#1baf7a"]
plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "font.family": "sans-serif", "font.size": 9.5, "text.color": INK, "axes.labelcolor": INK2,
    "axes.edgecolor": AXE, "axes.linewidth": 0.8, "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
    "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False, "lines.linewidth": 2,
    "axes.titlesize": 10.5, "axes.titleweight": "bold", "axes.titlelocation": "left", "axes.titlecolor": INK})


def fr(x, d=1):
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",")


h = pd.read_csv(IND / "o1_01_penetration.csv")
h = h[h.annee >= 2010]
sc = pd.read_csv(ICI / "r8_scenarios_usage.csv")
syn = pd.read_csv(ICI / "r8_scenarios_synthese.csv").set_index("scenario")
ORDRE = ["tendanciel (moyenne 2023-2024)", "accéléré (moyenne 2019-2024)", "ambitieux (années d'accélération 2016 et 2020)"]

fig, ax = plt.subplots(figsize=(9.5, 5.2))
ax.plot(h.annee, h.pct_population, color=INK, linewidth=2, label="observé (estimation UIT)")
ax.scatter([2024], [h.pct_population.iloc[-1]], s=40, color=INK, zorder=4, edgecolor=SURFACE, linewidth=1.5)
for col, nom in zip(S, ORDRE):
    g = sc[sc.scenario == nom]
    x = [2024] + g.annee.tolist()
    y = [h.pct_population.iloc[-1]] + g.pct_population.tolist()
    ax.plot(x, y, color=col, linestyle=(0, (4, 2)), label=nom)
    r = syn.loc[nom]
    ax.text(2030.25, y[-1], f"{fr(y[-1])} %  ({fr(r.points_par_an)} pt/an ; 60 % en {int(r.annee_60pct)})",
            color=INK2, fontsize=8, va="center")
for yy, lab in ((40, "40 % : fin du déficit d'usage"), (60, "60 % : usage généralisé")):
    ax.axhline(yy, color=INK2, linewidth=0.8, linestyle=(0, (1, 2)))
    ax.text(2010.2, yy + 1.2, lab, fontsize=7.8, color=INK2)
ax.axvspan(2024, 2030, color="#f0efec", zorder=0)
ax.text(2027, 3, "projection : ordre de grandeur,\npas une prévision", ha="center", fontsize=7.8, color=MUTED)
ax.set_xlim(2010, 2030)
ax.set_xticks(range(2010, 2031, 2))
ax.set_ylim(0, 85)
ax.set_ylabel("Part de la population utilisant Internet (%)")
ax.legend(loc="upper left", fontsize=8, bbox_to_anchor=(0.0, 0.93))
fig.suptitle("Usage d'Internet : 60 % vers 2028 à 2035 selon le rythme ; le seuil de 40 % est à portée dès 2025",
             x=0.01, ha="left", fontsize=11, fontweight="bold")
fig.text(0.01, -0.02, "Prolongement linéaire en points par an depuis 2024 (39,48 %, estimation UIT, niveau C). Rythmes tirés d'O1-02 : tendanciel = 2023-2024 "
         "(ralentissement confirmé) ; accéléré = 2019-2024 ;\nambitieux = années d'accélération 2016 et 2020. Tables : r8_scenarios_usage.csv, r8_scenarios_synthese.csv ; "
         "o1_01_penetration.csv (07)", color=MUTED, fontsize=7.5, ha="left", va="top")
fig.savefig(FIG / "f1_scenarios_usage.png", dpi=160, bbox_inches="tight")
plt.close(fig)
print(f"1 figure écrite dans {FIG}")
