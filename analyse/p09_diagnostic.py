"""09 — Diagnostic territorial (étape 10 de la procédure) : pourquoi ces territoires, et pas seulement à quel rang.

Lit les tables du 08 (score), du 07 (indicateurs) et du 06 (spatial) ; écrit des tables dans data/analysis/09_diagnostic/.
Aucun nouveau score, aucun nouveau classement.

Règles, fixées avant le calcul :
- périmètre : les 7 préfectures en priorité 1 et les 3 non classées du 08 (P14) ; les communes signalées (P15) =
  communes sans point formel ou en cellule critique O4-06 ;
- nature du déficit : une dimension du score est un « déficit marqué » si son rang percentile est de 75 ou plus
  (quartile le plus mal servi, comme le quartile de O4-02) ; le « moteur » est la dimension au rang le plus haut.
  Pour les 3 préfectures non classées : D1 et D2 seulement, rangs sur les 39 préfectures ;
- facteurs associés : mesures de contexte par préfecture, chacune située par son rang parmi les 39 préfectures,
  orienté « 100 = le plus défavorable ». Ce sont des associations, jamais des causes ;
- un facteur « se répète » s'il est du côté défavorable de la médiane des 39 préfectures dans au moins 6 des 7
  préfectures en priorité 1 ; « partagé » pour 4 ou 5 ; sinon « non commun » ;
- contexte régional (accès à Internet, alphabétisation, usage du mobile money : EHCVM 2021/22, niveau B) : attaché à
  la région, jamais attribué à la préfecture.

Ajouts validés le 27/09/2026 (P16 à P18) : structure par opérateur du mobile money et agences Togocom (3i, niveau C)
dans chaque fiche, ajoutées aux facteurs situés parmi les 39 ; diagnostic régional de l'usage d'Internet (6 régions) ;
leviers possibles par territoire, tirés de la nature du déficit par une correspondance fixe (D1 -> infrastructure
financière, D2 -> réseau d'agents, D3 -> infrastructure réseau, conditionnée à la couverture réelle) ; priorité
absolue d'O5-03 à la maille communale (P17) pour toute commune « mobile money uniquement ».
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "prep"))
from commun import PROCESSED, RACINE  # noqa: E402

A = RACINE / "data" / "analysis"
SC, IND, SPA = A / "08_priorisation", A / "07_indicateurs", A / "06_spatial"
SORTIE = A / "09_diagnostic"
SORTIE.mkdir(parents=True, exist_ok=True)
R: dict[str, pd.DataFrame] = {}
SEUIL_DEFICIT = 75
lire = lambda d, n: pd.read_csv(d / f"{n}.csv")  # noqa: E731

sc = lire(SC, "score_prefectures")
tp = pd.read_csv(PROCESSED / "terr_prefecture.csv")
tc = pd.read_csv(PROCESSED / "terr_commune.csv")
com = lire(IND, "o4_communes").merge(tc[["code", "prefecture_code", "part_urbaine", "superficie_km2"]], on="code")
dist = lire(SPA, "s5_distances_communes")
dsg = lire(SPA, "s5_communes_sans_guichet_distance")
ope = lire(SPA, "s2_operateurs_communes")
fib = lire(SPA, "s6_fibre_communes")
lisa = lire(SPA, "s7_lisa_communes")
couv = lire(IND, "o2_06_couverture")
cel = lire(IND, "o4_06_cellules")
fr_ = lire(IND, "o1_06_freins").set_index("unite_regionale")
mmr = lire(IND, "o3_05_usage_regions").set_index("unite_regionale")

P1 = sc[sc.classe_retenue == "priorité 1"].code.tolist()
ND = sc[sc.classe_retenue.str.startswith("non")].code.tolist()
FICHES = P1 + ND

# ----------------------------------------------------------------- Facteurs associés, par préfecture (39)
com = com.merge(dist[["code", "points_mm", "part_plus_5km_guichet_pct", "part_plus_10km_guichet_pct", "mediane_km_guichet"]], on="code")
com = com.merge(ope[["code", "part_deux_operateurs_pct", "part_togocom_seul_pct", "part_moov_seul_pct", "part_operateur_non_renseigne_pct"]],
                on="code")
com = com.merge(fib[["code", "km_fibre_enterree", "km_fibre_aerienne", "aucune_fibre_recensee"]], on="code")
cc = couv[couv.maille == "commune"].set_index("code")
com["couverture_commune_pct"] = com.code.map(cc.couverture_proxy_pct)
com["couverture_classe"] = com.code.map(cc.classe_02)
com["couverture_douteuse_P6"] = com.code.map(cc.valeur_douteuse_P6).astype(bool)
com["cellule_O4_06"] = com.code.map(cel[cel.maille == "commune"].set_index("code").cellule_O4_06)
for v, lab in (("formels_pour_10k_hab", "grappe_points_formels"), ("mm_pour_10k_adultes", "grappe_mobile_money")):
    com[lab] = com.code.map(lisa[lisa.variable == v].set_index("code").grappe)
w = lambda g, c: (g[c] * g.points_mm).sum() / g.points_mm.sum()  # noqa: E731 moyenne pondérée par les points


def par_prefecture(g):
    top = g.loc[g.n_formels.idxmax()]
    aucun = g.n_formels.sum() == 0  # Kpendjal : pas de commune « la mieux dotée »
    return pd.Series({
        "communes": len(g),
        "part_points_mm_plus_10km_guichet_pct": w(g, "part_plus_10km_guichet_pct"),
        "part_points_mm_plus_5km_guichet_pct": w(g, "part_plus_5km_guichet_pct"),
        "part_points_mm_togocom_seul_pct": w(g, "part_togocom_seul_pct"),
        "part_points_mm_deux_operateurs_pct": w(g, "part_deux_operateurs_pct"),
        "part_points_mm_moov_seul_pct": w(g, "part_moov_seul_pct"),
        "communes_togocom_seul_50pct_ou_plus": ", ".join(sorted(g.nom[g.part_togocom_seul_pct >= 50])),
        "part_points_mm_operateur_nd_pct": w(g, "part_operateur_non_renseigne_pct"),
        "commune_la_mieux_dotee": None if aucun else top.nom,
        "part_points_formels_commune_la_mieux_dotee_pct": np.nan if aucun else 100 * top.n_formels / g.n_formels.sum(),
        "part_population_commune_la_mieux_dotee_pct": np.nan if aucun else 100 * top.pop_totale / g.pop_totale.sum(),
        "communes_sans_fibre_recensee": int(g.aucune_fibre_recensee.sum()),
        "communes_grappe_faible_points_formels": ", ".join(sorted(g.nom[g.grappe_points_formels == "faible entouré de faibles"])),
        "communes_grappe_faible_mobile_money": ", ".join(sorted(g.nom[g.grappe_mobile_money == "faible entouré de faibles"])),
    })


fp = com.groupby("prefecture_code").apply(par_prefecture, include_groups=False)
t = sc.set_index("code").join(fp).join(tp.set_index("code")[["part_urbaine", "superficie_km2", "n_banque", "n_imf", "n_assurance",
                                                             "n_dab", "n_poste", "n_mm", "pop15_prorata"]])
t["part_urbaine_pct"] = 100 * t.index.map(tp.set_index("code").pop_urbaine) / t.pop_totale  # part_urbaine vide par préfecture
t["densite_hab_km2"] = t.pop_totale / t.superficie_km2
t["types_formels_presents"] = (t[["n_banque", "n_imf", "n_assurance", "n_dab"]] > 0).sum(axis=1)
t["banques_pour_10k_adultes"] = 1e4 * t.n_banque / t.pop15_prorata
t["km_fibre_enterree"] = t.index.map(lire(IND, "o2_07_fibre_prefectures").set_index("code").km_fibre_enterree)
for ind, col in (("nombre-agences-togocom", "agences_togocom"), ("pct-habitants-5km-agence-togocom", "pct_hab_5km_agence_togocom")):
    j = json.load(open(RACINE / "data" / "raw" / f"D3_geodata-{ind}_PREFECTURE.json", encoding="utf-8"))
    t[col] = t.index.map({r["prefecture_id"]: float(r["valeur"]) for r in j})
t["concentration_points_formels_pts"] = t.part_points_formels_commune_la_mieux_dotee_pct - t.part_population_commune_la_mieux_dotee_pct

# Facteurs situés parmi les 39 : (colonne, libellé, sens défavorable)
FACTEURS = [("part_urbaine_pct", "part de la population urbaine", "bas"),
            ("densite_hab_km2", "densité de population", "bas"),
            ("types_formels_presents", "types de points formels présents (sur 4, DAB compris)", "bas"),
            ("banques_pour_10k_adultes", "agences bancaires pour 10 000 adultes", "bas"),
            ("concentration_points_formels_pts", "concentration des points formels dans une commune (points en % moins population en %)", "haut"),
            ("part_points_mm_plus_10km_guichet_pct", "points mobile money à plus de 10 km d'un guichet", "haut"),
            ("part_points_mm_togocom_seul_pct", "points mobile money servis par Togocom seul", "haut"),
            ("part_points_mm_deux_operateurs_pct", "points mobile money servis par les deux opérateurs", "bas"),
            ("pct_hab_5km_agence_togocom", "habitants à moins de 5 km d'une agence Togocom", "bas"),
            ("km_fibre_enterree", "fibre enterrée recensée (km)", "bas")]
pos = []
for c, lab, sens in FACTEURS:
    r = t[c].rank(method="average", ascending=(sens == "haut"))
    t[f"{c}_rang_defavorable"] = 100 * (r - 1) / (t[c].notna().sum() - 1)
    med = t[c].median()
    t[f"{c}_defavorable"] = (t[c] < med) if sens == "bas" else (t[c] > med)
    n = int(t.loc[P1, f"{c}_defavorable"].sum())
    pos.append(dict(facteur=lab, colonne=c, sens_defavorable=sens, mediane_39=round(med, 2),
                    mediane_priorite_1=round(t.loc[P1, c].median(), 2), mediane_autres_classees=round(t.loc[~t.index.isin(P1 + ND), c].median(), 2),
                    priorite_1_du_cote_defavorable=f"{n} sur 7",
                    lecture="se répète" if n >= 6 else "partagé" if n >= 4 else "non commun",
                    non_classees_du_cote_defavorable=f"{int(t.loc[ND, f'{c}_defavorable'].sum())} sur 3"))
R["facteurs_repetition"] = pd.DataFrame(pos)

# ----------------------------------------------------------------- Fiches (10 préfectures)
f = t.loc[FICHES].copy()
f["lecture_score"] = np.where(f.index.isin(ND), "2 dimensions (couverture non déterminable)", "3 dimensions")
dims = DIMS_L = {"D1": "accès formel", "D2": "maillage mobile money", "D3": "couverture (proxy)"}
for i in f.index:
    rg = {d: (f.loc[i, f"sans_couv_{d}_rang_pct"] if i in ND else f.loc[i, f"{d}_rang_pct"]) for d in dims if not (i in ND and d == "D3")}
    f.loc[i, "moteur"] = dims[max(rg, key=rg.get)]
    f.loc[i, "deficits_marques"] = ", ".join(f"{dims[d]} ({rg[d]:.0f})" for d in rg if rg[d] >= SEUIL_DEFICIT) or "aucun"
    f.loc[i, "sans_deficit_relatif"] = ", ".join(f"{dims[d]} ({rg[d]:.0f})" for d in rg if rg[d] < 50) or "aucune"
f["acces_internet_region_pct"] = f.unite_regionale.map(fr_.acces_internet_2021_22_pct)
f["alphabetisation_region_pct"] = f.unite_regionale.map(fr_.alphabetisation_15plus_pct)
f["frein_region_02"] = f.unite_regionale.map(fr_.lecture_02)
f["usage_mobile_money_region_pct"] = f.unite_regionale.map(mmr.estimation_pct)
f["usage_mobile_money_region_ecart"] = f.unite_regionale.map(mmr.ecart_national)
COLS = (["nom", "unite_regionale", "pop_totale", "classe_retenue", "lecture_score", "score", "sans_couv_score", "confiance_P13",
         "moteur", "deficits_marques", "sans_deficit_relatif", "D1", "D2", "D3", "couverture_proxy_pct", "statut_O4_05",
         "n_banque", "n_imf", "n_assurance", "n_dab", "n_poste", "n_mm", "communes", "commune_la_mieux_dotee",
         "part_points_formels_commune_la_mieux_dotee_pct", "part_population_commune_la_mieux_dotee_pct"]
        + [c for c, _, _ in FACTEURS] + [f"{c}_rang_defavorable" for c, _, _ in FACTEURS]
        + ["part_points_mm_plus_5km_guichet_pct", "part_points_mm_moov_seul_pct", "part_points_mm_operateur_nd_pct",
           "communes_togocom_seul_50pct_ou_plus", "agences_togocom", "communes_sans_fibre_recensee",
           "communes_grappe_faible_points_formels", "communes_grappe_faible_mobile_money", "communes_critiques_O4_06",
           "noms_communes_sans_point_formel", "communes_couverture_douteuse_P6", "communes_couverture_nd",
           "acces_internet_region_pct", "alphabetisation_region_pct", "frein_region_02", "usage_mobile_money_region_pct",
           "usage_mobile_money_region_ecart"])
R["fiches_prefectures"] = f.reset_index()[["code"] + COLS].round(1)

# ----------------------------------------------------------------- Communes des 10 préfectures, et communes signalées
CC = ["code", "nom", "prefecture", "prefecture_code", "unite_regionale", "strate_50", "pop_totale", "n_formels", "n_banque", "n_imf",
      "n_assurance", "n_mm", "statut_O4_05", "cellule_O4_06", "couverture_commune_pct", "couverture_classe", "couverture_douteuse_P6",
      "mediane_km_guichet", "part_plus_10km_guichet_pct", "part_togocom_seul_pct", "part_operateur_non_renseigne_pct",
      "aucune_fibre_recensee", "grappe_points_formels", "grappe_mobile_money"]
R["communes_des_prefectures_fiches"] = com[com.prefecture_code.isin(FICHES)][CC].round(1)
sig = com[(com.n_formels == 0) | com.cellule_O4_06.str.startswith("critique")][CC].copy()
sig["signal"] = np.select([(sig.n_formels == 0) & sig.cellule_O4_06.str.startswith("critique"), sig.n_formels == 0],
                          ["sans point formel et cellule critique", "sans point formel"], "cellule critique")
sig["classe_prefecture_08"] = sig.prefecture_code.map(sc.set_index("code").classe_retenue)
sig["priorite_absolue_O5_03_commune"] = sig.statut_O4_05 == "mobile money uniquement"  # P17, validé le 27/09/2026
sig["km_guichet_le_plus_proche_mediane"] = sig.code.map(dsg.set_index("code").mediane_km_guichet)
sig["commune_du_guichet_le_plus_proche"] = sig.code.map(dsg.set_index("code").commune_du_guichet_le_plus_proche)
ordre = {"priorité 1": 1, "non déterminable (couverture)": 2, "priorité 2": 3, "priorité 3": 4}
sig = sig.assign(_o=sig.classe_prefecture_08.map(ordre)).sort_values(["_o", "prefecture", "nom"]).drop(columns="_o")
R["communes_signalees"] = sig.round(1)
R["communes_signalees_synthese"] = (sig.groupby(["classe_prefecture_08", "signal"])
                                    .agg(communes=("nom", "size"), population=("pop_totale", "sum"), noms=("nom", ", ".join)).reset_index())

# ----------------------------------------------------------------- Diagnostic régional de l'usage d'Internet (6 régions)
ui = lire(SPA, "s6_usage_internet_regions").set_index("nom")
cap = lire(SPA, "s9_capacites_usage_regions")
alpha = cap[(cap.indicateur == "alphabetisation") & (cap.vague == "2021/22")].set_index("nom")
reg = []
for r_, g in t.groupby("unite_regionale"):
    fi_ = g[g.index.isin(FICHES)]
    sg = sig[sig.unite_regionale == r_]
    reg.append(dict(
        region=r_, acces_internet_2018_19_pct=ui.loc[r_, "estimation_pct_2018_19"], acces_internet_2021_22_pct=ui.loc[r_, "estimation_pct_2021_22"],
        ic95_2021_22=f"{ui.loc[r_, 'ic95_bas_2021_22']:.1f} à {ui.loc[r_, 'ic95_haut_2021_22']:.1f}",
        variation_points=ui.loc[r_, "variation_points"], couverture_proxy_ponderee_pct=ui.loc[r_, "couverture_ponderee_pop_pct"],
        communes_couverture_nd=int(ui.loc[r_, "non_determinables"]), alphabetisation_2021_22_pct=alpha.loc[r_, "estimation_pct"],
        alphabetisation_variation_points=alpha.loc[r_, "variation_points"],
        competences_TIC_femmes_pct=fr_.loc[r_, "competences_TIC_Femmes 15-49 ans"], competences_TIC_hommes_pct=fr_.loc[r_, "competences_TIC_Hommes 15-49 ans"],
        lecture_O1_06=fr_.loc[r_, "lecture_02"], usage_mobile_money_pct=mmr.loc[r_, "estimation_pct"],
        prefectures_des_fiches=", ".join(fi_.nom), population_prefectures_des_fiches=int(fi_.pop_totale.sum()),
        communes_signalees=len(sg), population_communes_signalees=int(sg.pop_totale.sum()), population_region=int(g.pop_totale.sum())))
R["internet_regions"] = pd.DataFrame(reg).sort_values("acces_internet_2021_22_pct").round(1)

# ----------------------------------------------------------------- Leviers possibles (à instruire à l'étape 11, jamais des recommandations)
LEVIER = {"D1": ("infrastructure financière : points formels", "O4-01, O4-02"),
          "D2": ("réseau d'agents mobile money", "O4-04, O4-05"),
          "D3": ("infrastructure réseau", "O2-06, O4-06")}
lev = []
for i in FICHES:
    r = t.loc[i]
    nd_ = i in ND
    rg = {d: (r[f"sans_couv_{d}_rang_pct"] if nd_ else r[f"{d}_rang_pct"]) for d in ("D1", "D2", "D3") if not (nd_ and d == "D3")}
    for d in sorted(rg, key=rg.get, reverse=True):
        if rg[d] >= SEUIL_DEFICIT:
            cond = ("couverture proxy (A17) : à confirmer avant toute action réseau" +
                    (" ; P16 : les actions sur les guichets n'attendent pas" if r.nom == "Kéran" else "")) if d == "D3" else ""
            lev.append(dict(territoire=r.nom, maille="préfecture", nature=f"{DIMS_L[d]} (rang {rg[d]:.0f})", levier_possible=LEVIER[d][0],
                            indicateur_qui_chiffrera=LEVIER[d][1], condition=cond))
    if nd_:
        lev.append(dict(territoire=r.nom, maille="préfecture", nature="couverture inconnue (A13)", levier_possible="mesurer la couverture réelle",
                        indicateur_qui_chiffrera="O2-06", condition="préalable à toute action réseau"))
    c = sig[(sig.prefecture_code == i) & sig.priorite_absolue_O5_03_commune]
    if len(c):
        lev.append(dict(territoire=r.nom, maille="commune", nature="sans point formel : " + ", ".join(c.nom), levier_possible=LEVIER["D1"][0] + " de proximité",
                        indicateur_qui_chiffrera="O4-01, O4-05", condition="priorité absolue d'O5-03 à la maille communale (P17)"))
c = sig[sig.priorite_absolue_O5_03_commune & sig.classe_prefecture_08.isin(["priorité 2", "priorité 3"])]
lev.append(dict(territoire=f"{len(c)} communes « mobile money uniquement » des préfectures en priorité 2 ou 3", maille="commune",
                nature="sans point formel : " + ", ".join(c.nom), levier_possible=LEVIER["D1"][0] + " de proximité",
                indicateur_qui_chiffrera="O4-01, O4-05", condition="priorité absolue d'O5-03 à la maille communale (P17)"))
for r_, x in fr_.iterrows():
    if "capacité" in str(x.lecture_02):
        lev.append(dict(territoire=r_, maille="région", nature="usage d'Internet faible, frein de capacité présumé (O1-06)",
                        levier_possible="compétences numériques", indicateur_qui_chiffrera="O1-06", condition="proxy de compétence ; maille régionale"))
lev.append(dict(territoire="toutes les régions", maille="national", nature="1 Go = 5,30 % du revenu mensuel (O2-05b)", levier_possible="tarification",
                indicateur_qui_chiffrera="O2-05b", condition="national"))
R["leviers_possibles"] = pd.DataFrame(lev)

for nom, df in R.items():
    df.to_csv(SORTIE / f"{nom}.csv", index=False, encoding="utf-8")
print(f"{len(R)} tables écrites dans {SORTIE.relative_to(RACINE)}")
