"""05 — Exploration des données (étape 07 de la procédure) : distributions, disparités, relations, contradictions.

Entrées : tables de data/processed/ (04). Sorties : data/analysis/05_eda/ (tables CSV et figures PNG).
Règles : aucun score, aucune classe du 02 appliquée, aucune carte (06). Les ratios sont descriptifs ;
0 point → ratio « habitants par point » non défini (jamais 0, jamais infini). Un dénominateur par ratio.
"""
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "prep"))
from commun import GEO, PROCESSED, RACINE  # noqa: E402

SORTIE = RACINE / "data" / "analysis" / "05_eda"
FIG = SORTIE / "figures"
FIG.mkdir(parents=True, exist_ok=True)
R: dict[str, pd.DataFrame] = {}  # tables de résultats, écrites en fin de script


def garder(nom: str, df: pd.DataFrame) -> pd.DataFrame:
    R[nom] = df
    return df


com = pd.read_csv(PROCESSED / "terr_commune.csv")
pref = pd.read_csv(PROCESSED / "terr_prefecture.csv")
ur = pd.read_csv(PROCESSED / "terr_region.csv")
pts = pd.read_csv(PROCESSED / "points_service.csv", low_memory=False)
sn = pd.read_csv(PROCESSED / "serie_nationale.csv", low_memory=False, dtype={"periode": str, "technologie": str})
eq = pd.read_csv(PROCESSED / "enquetes_region.csv")
bm = pd.read_csv(PROCESSED / "benchmark.csv")
sn["technologie"] = sn["technologie"].fillna("")

TYPES = ["n_banque", "n_imf", "n_assurance", "n_formels", "n_dab", "n_mm", "n_poste"]
LIB = {"n_banque": "Banques", "n_imf": "IMF", "n_assurance": "Assurances", "n_formels": "Points formels",
       "n_dab": "Sites de DAB", "n_mm": "Points mobile money", "n_poste": "Poste (variante)"}


def ratios(t: pd.DataFrame) -> pd.DataFrame:
    """Ratios descriptifs ; un seul dénominateur par ratio (RGPH-5)."""
    t = t.copy()
    t["part_urbaine"] = t.pop_urbaine / t.pop_totale
    t["hab_par_point_formel"] = (t.pop_totale / t.n_formels).where(t.n_formels > 0)  # non défini si 0
    t["formels_pour_10k_hab"] = 1e4 * t.n_formels / t.pop_totale
    t["mm_pour_10k_adultes"] = 1e4 * t.n_mm / t.pop15_prorata
    t["hab_par_point_mm"] = (t.pop_totale / t.n_mm).where(t.n_mm > 0)
    t["dab_pour_100k_adultes"] = 1e5 * t.n_dab / t.pop15_prorata
    t["mm_par_point_formel"] = (t.n_mm / t.n_formels).where(t.n_formels > 0)
    t["densite_hab_km2"] = t.pop_totale / t.superficie_km2
    t["formels_pour_1000_km2"] = 1e3 * t.n_formels / t.superficie_km2
    t["mm_pour_1000_km2"] = 1e3 * t.n_mm / t.superficie_km2
    return t


com, pref, ur = ratios(com), ratios(pref), ratios(ur)
NAT_POP, NAT_15 = int(com.pop_totale.sum()), int(com.pop15_prorata.sum())

# =============================================================== 2. Offre de services
nat = pd.DataFrame({"type": [LIB[c] for c in TYPES], "national": [int(com[c].sum()) for c in TYPES]})
for c in TYPES:
    nat.loc[nat.type == LIB[c], "part_grand_lome_pct"] = round(100 * ur.loc[ur.code == "GL", c].iloc[0] / com[c].sum(), 1)
    nat.loc[nat.type == LIB[c], "communes_a_zero"] = int((com[c] == 0).sum())
    nat.loc[nat.type == LIB[c], "prefectures_a_zero"] = int((pref[c] == 0).sum())
garder("s2_offre_nationale", nat)

part = ur[["code", "nom", "pop_totale", "superficie_km2"] + TYPES].copy()
for c in ["pop_totale", "superficie_km2"] + TYPES:
    part[f"part_{c}"] = (100 * part[c] / part[c].sum()).round(1)
garder("s2_parts_unites_regionales", part.sort_values("pop_totale", ascending=False))


def resume(serie: pd.Series) -> dict:
    s = serie.dropna()
    return dict(n=len(s), min=s.min(), q1=s.quantile(.25), mediane=s.median(), q3=s.quantile(.75), max=s.max(),
                moyenne=s.mean(), p90_sur_p10=(s.quantile(.9) / s.quantile(.1)) if s.quantile(.1) > 0 else np.nan)


garder("s2_distribution_comptages", pd.DataFrame(
    [dict(maille=m, variable=LIB[c], **resume(t[c])) for m, t in (("commune", com), ("préfecture", pref)) for c in TYPES]
).round(1))


def lorenz(t: pd.DataFrame, col: str, poids: str = "pop_totale"):
    """Courbe de concentration des points face à la population, et indice de Gini correspondant."""
    d = t[[col, poids]].copy()
    d["taux"] = d[col] / d[poids]
    d = d.sort_values("taux")
    x = np.concatenate([[0], d[poids].cumsum() / d[poids].sum()])
    y = np.concatenate([[0], d[col].cumsum() / d[col].sum()])
    gini = 1 - np.sum((x[1:] - x[:-1]) * (y[1:] + y[:-1]))
    return x, y, gini


LZ = {c: lorenz(com, c) for c in ("n_formels", "n_dab", "n_mm")}
garder("s2_concentration", pd.DataFrame([dict(variable=LIB[c], gini_communes=round(LZ[c][2], 3),
                                              gini_prefectures=round(lorenz(pref, c)[2], 3)) for c in LZ]))
top = com.sort_values("n_formels", ascending=False)
garder("s2_top_communes_formels", top[["nom", "unite_regionale_code", "n_formels", "pop_totale"]].head(10).assign(
    part_cumulee_points_pct=lambda d: (100 * d.n_formels.cumsum() / com.n_formels.sum()).round(1),
    part_cumulee_pop_pct=lambda d: (100 * d.pop_totale.cumsum() / NAT_POP).round(1)))

# Structure par opérateur des points mobile money (vues non additives, DD2) et emplacement des DAB (4c)
mm = pts[pts.type == "mobile_money"]
MM_CAT = {"mm_deux_operateurs": (mm.nb_operateurs == 2),
          "mm_togocom_seul": (mm.nb_operateurs == 1) & (mm.op_togocom == 1),
          "mm_moov_seul": (mm.nb_operateurs == 1) & (mm.op_moov == 1),
          "mm_operateur_non_renseigne": mm.nb_operateurs.isna()}
mm = mm.assign(categorie=np.select(list(MM_CAT.values()), list(MM_CAT), default=""))
assert (mm.categorie != "").all()
dab = pts[pts.type == "dab"]
DAB_CAT = {"Dans une banque": "dab_dans_une_banque", "Independant": "dab_independant",
           "Dans un autre etablissement": "dab_autre_etablissement"}
dab = dab.assign(categorie=dab.categorie_origine.map(DAB_CAT))
assert dab.categorie.notna().all()


def structure(points: pd.DataFrame, cle: str, colonnes) -> pd.DataFrame:
    return pd.crosstab(points[cle], points.categorie).reindex(columns=list(colonnes), fill_value=0)


op_ur = structure(mm, "unite_regionale_code", MM_CAT)
op_ur.loc["national"] = op_ur.sum()
op_ur = op_ur.join(ur.set_index("code").nom).fillna({"nom": "National"})
op_ur["total"] = op_ur[list(MM_CAT)].sum(axis=1)
for c in MM_CAT:
    op_ur[f"part_{c}_pct"] = (100 * op_ur[c] / op_ur.total).round(1)
op_ur["presence_moov_pct"] = (100 * (op_ur.mm_deux_operateurs + op_ur.mm_moov_seul) / op_ur.total).round(1)
op_ur["presence_togocom_pct"] = (100 * (op_ur.mm_deux_operateurs + op_ur.mm_togocom_seul) / op_ur.total).round(1)
garder("s2_mm_operateurs", op_ur.reset_index(names="code"))
dab_ur = structure(dab, "unite_regionale_code", DAB_CAT.values())
dab_ur.loc["national"] = dab_ur.sum()
dab_ur = dab_ur.join(ur.set_index("code").nom).fillna({"nom": "National"})
dab_ur["total"] = dab_ur[list(DAB_CAT.values())].sum(axis=1)
garder("s2_dab_emplacement", dab_ur.reset_index(names="code"))

# Effectifs par type aux mailles fines (objectif 3), pour les cartes du 06 et le tableau de bord ; Poste exclue
OBJ3 = ["n_banque", "n_imf", "n_assurance", "n_formels", "n_dab", "n_mm"]
noms_ur, noms_pref = ur.set_index("code").nom, pref.set_index("code").nom
for maille, t, cle in (("prefecture", pref, "prefecture_code"), ("commune", com, "commune_code")):
    o = t[["code", "nom"] + (["prefecture_code"] if maille == "commune" else []) + ["unite_regionale_code",
                                                                                     "pop_totale", "pop15_prorata"] + OBJ3]
    o = o.join(structure(mm, cle, MM_CAT), on="code").join(structure(dab, cle, DAB_CAT.values()), on="code")
    if maille == "commune":
        o.insert(3, "prefecture", o.prefecture_code.map(noms_pref))
    o.insert(o.columns.get_loc("unite_regionale_code") + 1, "unite_regionale", o.unite_regionale_code.map(noms_ur))
    fins = list(MM_CAT) + list(DAB_CAT.values())
    o[fins] = o[fins].fillna(0).astype(int)
    assert (o[list(MM_CAT)].sum(axis=1) == o.n_mm).all() and (o[list(DAB_CAT.values())].sum(axis=1) == o.n_dab).all()
    garder(f"s2_offre_par_{maille}", o.sort_values(["unite_regionale_code", "code"]))

# =============================================================== 3. Population
pop_ur = ur[["code", "nom", "pop_totale", "pop15_prorata", "pop_urbaine", "superficie_km2", "densite_hab_km2"]].copy()
pop_ur["part_pop_pct"] = (100 * pop_ur.pop_totale / NAT_POP).round(1)
pop_ur["part_15plus_pct"] = (100 * pop_ur.pop15_prorata / pop_ur.pop_totale).round(1)
pop_ur["part_urbaine_pct"] = (100 * pop_ur.pop_urbaine / pop_ur.pop_totale).round(1)
garder("s3_population_unites_regionales", pop_ur.sort_values("pop_totale", ascending=False).round(1))
garder("s3_distribution_population", pd.DataFrame(
    [dict(maille=m, variable=v, **resume(t[v])) for m, t in (("commune", com), ("préfecture", pref))
     for v in ("pop_totale", "densite_hab_km2", "part_urbaine")]).round(2))
strates = com.groupby("strate_50").agg(communes=("code", "size"), pop=("pop_totale", "sum"), formels=("n_formels", "sum"),
                                       mm=("n_mm", "sum"), dab=("n_dab", "sum"), pop15=("pop15_prorata", "sum"))
for c in ("pop", "formels", "mm", "dab"):
    strates[f"part_{c}_pct"] = (100 * strates[c] / strates[c].sum()).round(1)
garder("s3_strates", strates.reset_index())

# =============================================================== 4. Séries nationales
def serie(ind, op="ensemble", tech="", source=None, freq="annuel", var="principal"):
    d = sn[(sn.indicateur == ind) & (sn.operateur == op) & (sn.technologie == tech) & (sn.frequence == freq)
           & (sn.variante == var)]
    if source:
        d = d[d.source.str.startswith(source)]
    return d.set_index("periode").valeur.sort_index()


d1 = serie("usage_internet_pct_population", source="D1")
d1g = (100 * d1.pct_change()).round(1).replace([np.inf, -np.inf], np.nan)  # croissance depuis 0 : non définie
premiere = d1[d1 > 0].index.min()  # 1996 : première année où l'UIT estime un usage non nul (0 % de 1990 à 1995)
garder("s4_usage_internet_d1", pd.DataFrame({"annee": d1.index, "pct_population": d1.values.round(3),
                                              "croissance_pct": d1g.values}).query("annee >= @premiere"))
survey = eq[(eq.domaine == "Togo") & eq.indicateur.isin(["acces_internet_declare", "usage_internet_toute_frequence",
                                                           "usage_internet_3_mois"])
            & ~((eq.indicateur == "acces_internet_declare") & (eq.population_reference == "tous les individus"))]
mics = eq[(eq.source.str.startswith("MICS6")) & (eq.domaine == "Togo") & (eq.indicateur == "internet_utilise_3_derniers_mois")]
garder("s4_usage_internet_enquetes", pd.concat([survey, mics])[["source", "vague", "indicateur", "population_reference",
                                                                "estimation_pct", "ic95_bas", "ic95_haut"]])
ssa = bm[(bm.iso3 == "SSF") & (bm.indicateur == "usage_internet_pct_population")].set_index("annee").valeur
uemoa = bm[bm.source.str.startswith("C5b") & bm.iso3.isin(["BEN", "BFA", "CIV", "GNB", "MLI", "NER", "SEN", "TGO"])]
# Repère régional (C5b, décision S1) : 8 pays de l'UEMOA et agrégat Afrique subsaharienne, estimations de l'UIT
rang = uemoa.pivot_table(index="annee", columns="iso3", values="valeur").rank(axis=1, ascending=False, method="min")
bench = pd.concat([uemoa, bm[(bm.iso3 == "SSF") & (bm.indicateur == "usage_internet_pct_population")]])
bench = bench[["iso3", "pays", "annee", "valeur", "note"]].merge(
    rang.stack().rename("rang_uemoa_sur_8").reset_index(), on=["annee", "iso3"], how="left")
garder("s4_benchmark_usage_internet", bench.sort_values(["iso3", "annee"]).round(2))

dm = pd.concat([serie("abonnes_data_mobile", tech="total", source="2b"),
                serie("abonnes_data_mobile", tech="total", source="AR1")])
hd = pd.concat([serie("abonnes_data_mobile", tech="haut_debit", source="D2"),
                serie("abonnes_data_mobile", tech="haut_debit", source="AR1")])
pop_in1 = serie("population_totale")
techs = {}
for o in ("togocom", "moov"):
    for t in ("2G", "3G", "4G", "5G", "3G+4G"):
        techs[(o, t)] = serie("abonnes_data_mobile", op=o, tech=t, source="AR1")
tt = pd.DataFrame(techs).fillna(0)
mix = pd.DataFrame({"2G": tt.xs("2G", axis=1, level=1).sum(axis=1),
                    "3G": tt.xs("3G", axis=1, level=1).sum(axis=1),
                    "4G": tt.xs("4G", axis=1, level=1).sum(axis=1),
                    "5G": tt.xs("5G", axis=1, level=1).sum(axis=1),
                    "3G+4G (Moov, non ventilé)": tt.xs("3G+4G", axis=1, level=1).sum(axis=1)})
mix_pct = (100 * mix.div(mix.sum(axis=1), axis=0)).round(1)
abo = pd.DataFrame({"abonnes_data_mobile": dm, "dont_haut_debit": hd})
abo["pour_100_hab_IN1"] = (100 * abo.abonnes_data_mobile / pop_in1.reindex(abo.index)).round(1)
abo["part_haut_debit_pct"] = (100 * abo.dont_haut_debit / abo.abonnes_data_mobile).round(1)
abo["croissance_pct"] = (100 * abo.abonnes_data_mobile.pct_change()).round(1)
abo["source"] = ["2b" if int(a) <= 2017 else "ARCEP (T4)" for a in abo.index]
garder("s4_abonnements_data", abo.reset_index(names="annee"))
garder("s4_mix_technologique_T4", mix_pct.reset_index(names="annee"))


def trim(ind, op, tech):
    return serie(ind, op=op, tech=tech, source="AR1", freq="trimestriel")


# Fibre (FTTH) : Togo Telecom par la ventilation des accès (T1 2017 - T3 2021), puis série FTTH de l'ARCEP (depuis T1 2024).
# GVA : Internet fixe entièrement en fibre de 2024 à 2026 ; avant 2024, sa fibre n'est pas isolée (fixe affiché à part).
fibre = pd.DataFrame({"internet_fixe_total": trim("abonnes_internet_fixe", "ensemble", "total"),
                      "evdo_togo_telecom": trim("abonnes_internet_fixe_acces", "togo_telecom", "Evdo"),
                      "internet_fixe_gva": trim("abonnes_internet_fixe", "gva", "total"),
                      "ftth_togo_telecom": pd.concat([trim("abonnes_internet_fixe_acces", "togo_telecom", "FTTH"),
                                                      trim("abonnes_ftth", "togo_telecom", "FTTH")]),
                      "ftth_gva": trim("abonnes_ftth", "gva", "FTTH"),
                      "ftth_total": trim("abonnes_ftth", "ensemble", "FTTH")})
fibre["part_ftth_internet_fixe_pct"] = (100 * fibre.ftth_total / fibre.internet_fixe_total).round(1)
fibre["part_ftth_data_mobile_pct"] = (100 * fibre.ftth_total / trim("abonnes_data_mobile", "ensemble", "total")).round(1)
garder("s4_fibre", fibre.reset_index(names="periode"))

parts = pd.DataFrame({
    "telephonie_D3": serie("part_marche_telephonie_mobile", op="togocom", source="D3"),
    "data_mobile_ARCEP": (100 * serie("abonnes_data_mobile", op="togocom", tech="total", source="AR1")
                          / serie("abonnes_data_mobile", tech="total", source="AR1")),
    "ca_mobile_ARCEP": (100 * serie("ca", op="togocom", source="AR1") / serie("ca", op="total_mobile", source="AR1"))})
garder("s4_parts_togocom", parts.round(1).reset_index(names="annee"))

ca = pd.DataFrame({"ca_secteur_2b": serie("ca", op="total_secteur", source="2b"),
                   "ca_secteur_ARCEP": serie("ca", op="total_secteur", source="AR1"),
                   "investissement_ARCEP": serie("investissement", op="total_secteur", source="AR1"),
                   "ca_D3": serie("ca", op="total_d3", source="D3"),
                   "investissement_D3": serie("investissement", op="total_d3", source="D3")}).round(2)
garder("s4_ca_investissement", ca.reset_index(names="annee"))

it1 = sn[sn.indicateur == "cout_data_pct_rnb_mensuel"].pivot_table(index="periode", columns="note", values="valeur")
garder("s4_paniers_uit", it1.round(2).reset_index(names="annee"))
com_idx = sn[(sn.indicateur == "indice_prix_communication") & sn.source.str.startswith("IN3b")].copy()
com_idx["annee"] = com_idx.periode.str[:4]
garder("s4_indice_communication", com_idx.groupby("annee").valeur.mean().round(1).reset_index())

mm = pd.DataFrame({
    "points_de_vente_T4": serie("mm_points_de_vente", source="AR1"),
    "comptes_T4": serie("mm_comptes", source="AR1"),
    "valeur_transactions_Md_ARCEP": serie("mm_valeur_transactions", source="AR1"),
    "valeur_transactions_Md_2b": serie("mm_valeur_transactions", source="2b"),
    "abonnes_actifs_2b": serie("mm_abonnes_actifs", source="2b")})
garder("s4_mobile_money", mm.reset_index(names="annee"))
fx = eq[eq.source.str.startswith("Findex") & (eq.domaine == "Togo") & eq.indicateur.isin(
    ["compte_total", "compte_mobile_money", "compte_institution_financiere"])].pivot_table(
    index="vague", columns="indicateur", values="estimation_pct").round(1)
garder("s4_findex", fx.reset_index())

# =============================================================== 5. Disparités territoriales
VARS = ["hab_par_point_formel", "formels_pour_10k_hab", "mm_pour_10k_adultes", "hab_par_point_mm",
        "dab_pour_100k_adultes", "mm_par_point_formel", "densite_hab_km2"]
garder("s5_distribution_ratios", pd.DataFrame(
    [dict(maille=m, ratio=v, non_defini=int(t[v].isna().sum()), **resume(t[v])) for m, t in (("commune", com),
                                                                                           ("préfecture", pref)) for v in VARS]).round(2))
extremes = []
for v in ("formels_pour_10k_hab", "mm_pour_10k_adultes"):
    for sens, d in (("plus bas", pref.nsmallest(5, v)), ("plus haut", pref.nlargest(5, v))):
        for _, r in d.iterrows():
            extremes.append(dict(ratio=v, sens=sens, prefecture=r.nom, valeur=round(r[v], 2), n_formels=r.n_formels,
                                 n_mm=r.n_mm, pop=r.pop_totale))
garder("s5_extremes_prefectures", pd.DataFrame(extremes))
garder("s5_unites_regionales_ratios", ur[["nom"] + VARS].round(2))
# Nombre de types présents (banque, IMF, assurance, DAB), décrit sans la classe de O4-05
TYPES4 = ["n_banque", "n_imf", "n_assurance", "n_dab"]
garder("s5_diversite_types", pd.concat([
    t.assign(nb_types=(t[TYPES4] > 0).sum(axis=1)).groupby("nb_types").agg(territoires=("code", "size"), pop=("pop_totale", "sum"))
    .assign(maille=m, part_pop_pct=lambda d: (100 * d["pop"] / d["pop"].sum()).round(1)).reset_index()
    for m, t in (("commune", com), ("préfecture", pref))])[["maille", "nb_types", "territoires", "pop", "part_pop_pct"]])
strates_r = strates.assign(formels_pour_10k_hab=lambda d: 1e4 * d.formels / d["pop"],
                           mm_pour_10k_adultes=lambda d: 1e4 * d.mm / d.pop15,
                           dab_pour_100k_adultes=lambda d: 1e5 * d.dab / d.pop15).round(2)
# Médianes des communes (traits noirs de la figure 3), à côté des ratios agrégés : les deux lectures diffèrent
medianes = com.groupby("strate_50")[["formels_pour_10k_hab", "mm_pour_10k_adultes", "dab_pour_100k_adultes"]].median()
strates_r = strates_r.join(medianes.add_prefix("mediane_communes_").round(2))
garder("s5_strates_ratios", strates_r.reset_index())
reg_eq = eq[eq.source.str.startswith("EHCVM (W2, micro") & (eq.domaine_type == "region")
            & eq.indicateur.isin(["acces_internet_declare", "usage_mobile_banking", "compte_mobile_banking",
                                  "telephone_portable", "alphabetisation"])
            & eq.population_reference.str.contains("15 ans|module 6")]
garder("s5_enquetes_regions", reg_eq[["vague", "domaine", "indicateur", "estimation_pct", "ic95_bas", "ic95_haut",
                                      "cv_pct", "n_obs"]].sort_values(["indicateur", "vague", "estimation_pct"]))

# =============================================================== 6. Relations
def spearman(t, a, b):
    d = t[[a, b]].dropna()
    return round(d[a].rank().corr(d[b].rank()), 2), len(d)


paires = [("pop_totale", "n_formels"), ("pop_totale", "n_mm"), ("pop_totale", "n_dab"), ("n_formels", "n_mm"),
          ("densite_hab_km2", "formels_pour_1000_km2"), ("densite_hab_km2", "mm_pour_1000_km2"),
          ("part_urbaine", "formels_pour_10k_hab"), ("part_urbaine", "mm_pour_10k_adultes"),
          ("formels_pour_10k_hab", "mm_pour_10k_adultes")]
rel = []
for m, t in (("commune", com), ("préfecture", pref)):
    for a, b in paires:
        rho, n = spearman(t, a, b)
        rel.append(dict(maille=m, x=a, y=b, rho_spearman=rho, n=n))
for a in ("mm_pour_10k_adultes", "formels_pour_10k_hab", "densite_hab_km2", "part_urbaine"):
    rho, n = spearman(pref, "couv_20km_pct", a)
    rel.append(dict(maille="préfecture", x="couv_20km_pct (3i, C)", y=a, rho_spearman=rho, n=n))
garder("s6_correlations_spearman", pd.DataFrame(rel))
# Région : offre (points MM par adulte) face à la demande déclarée (EHCVM 2021/22)
dem = eq[(eq.indicateur == "usage_mobile_banking") & (eq.domaine_type == "region")].set_index("unite_regionale_code")
off = ur.set_index("code")
garder("s6_offre_demande_regions", pd.DataFrame({
    "unite": off.nom, "mm_pour_10k_adultes": off.mm_pour_10k_adultes.round(1),
    "usage_mobile_banking_2021_pct": dem.estimation_pct, "ic95": dem.ic95_bas.round(1).astype(str) + "-" + dem.ic95_haut.round(1).astype(str),
    "acces_internet_2021_pct": eq[(eq.indicateur == "acces_internet_declare") & (eq.vague == "2021/22") & (eq.domaine_type == "region")
                                  & (eq.population_reference == "individus de 15 ans et plus")].set_index("unite_regionale_code").estimation_pct,
    "formels_pour_10k_hab": off.formels_pour_10k_hab.round(2)}).reset_index(names="code"))

# =============================================================== 7. Les cinq contradictions de la procédure
q_pop = com.pop_totale.quantile(.75)
q_off = com.formels_pour_10k_hab.quantile(.25)
c1 = com[(com.pop_totale >= q_pop) & (com.formels_pour_10k_hab <= q_off)]
garder("s7_c1_population_forte_offre_faible", c1[["nom", "unite_regionale_code", "pop_totale", "n_formels",
                                                  "formels_pour_10k_hab", "n_mm", "mm_pour_10k_adultes"]].sort_values("pop_totale", ascending=False).round(2))

med_mm = pref.mm_pour_10k_adultes.median()
c2 = pref[(pref.mm_pour_10k_adultes >= med_mm) & ((pref.couv_20km_pct < pref.couv_20km_pct.median()) | pref.couv_20km_pct.isna())]
garder("s7_c2_offre_correcte_couverture_faible", c2[["nom", "mm_pour_10k_adultes", "couv_20km_pct", "couv_20km_motif",
                                                     "pop_totale"]].sort_values("couv_20km_pct").round(2))

g = gpd.read_file(GEO / "communes.geojson")[["code", "geometry"]]
voisins = gpd.sjoin(g, g, predicate="touches")
voisins = voisins[voisins.code_left < voisins.code_right][["code_left", "code_right"]]
c = com.set_index("code")
vv = voisins.assign(a=lambda d: d.code_left.map(c.nom), b=lambda d: d.code_right.map(c.nom),
                    fa=lambda d: d.code_left.map(c.formels_pour_10k_hab), fb=lambda d: d.code_right.map(c.formels_pour_10k_hab),
                    ma=lambda d: d.code_left.map(c.mm_pour_10k_adultes), mb=lambda d: d.code_right.map(c.mm_pour_10k_adultes),
                    popa=lambda d: d.code_left.map(c.pop_totale), popb=lambda d: d.code_right.map(c.pop_totale))
vv["ecart_formels_pour_10k"] = (vv.fa - vv.fb).abs()
vv["ecart_mm_pour_10k_adultes"] = (vv.ma - vv.mb).abs()
garder("s7_c3_voisins_formels", vv.sort_values("ecart_formels_pour_10k", ascending=False).head(10).round(2))
garder("s7_c3_voisins_mm", vv.sort_values("ecart_mm_pour_10k_adultes", ascending=False).head(10).round(2))
R["s7_c3_bilan"] = pd.DataFrame([dict(paires_de_communes_voisines=len(vv))])

c4a = com[(com.formels_pour_10k_hab >= com.formels_pour_10k_hab.quantile(.75)) & (com.n_formels <= 2)]
c4b = com[(com.n_formels >= com.n_formels.quantile(.9)) & (com.formels_pour_10k_hab <= com.formels_pour_10k_hab.median())]
garder("s7_c4_taux_eleve_volume_faible", c4a[["nom", "pop_totale", "n_formels", "formels_pour_10k_hab"]].round(2))
garder("s7_c4_volume_eleve_taux_faible", c4b[["nom", "pop_totale", "n_formels", "formels_pour_10k_hab"]].round(2))

zero = com[com.n_formels == 0]
un = com[com.n_formels == 1]
types_presents = (com[["n_banque", "n_imf", "n_assurance"]] > 0).sum(axis=1)
mono_type = com[(types_presents == 1) & (com.n_formels > 0)]
d5 = pts[pts.type == "mobile_money"].copy()
d5["seul_moov"] = (d5.op_moov == 1) & (d5.op_togocom == 0)
d5["seul_togocom"] = (d5.op_togocom == 1) & (d5.op_moov == 0)
d5["deux"] = d5.nb_operateurs == 2
opc = d5.groupby("commune_code")[["seul_moov", "seul_togocom", "deux"]].sum()
opc["n"] = d5.groupby("commune_code").size()
opc["part_moov_present_pct"] = (100 * (opc.seul_moov + opc.deux) / opc.n).round(1)
opc["part_togocom_present_pct"] = (100 * (opc.seul_togocom + opc.deux) / opc.n).round(1)
c5 = pd.DataFrame([
    dict(situation="0 point formel : desservies uniquement par le mobile money", communes=len(zero),
         population=int(zero.pop_totale.sum()), points_mm=int(zero.n_mm.sum())),
    dict(situation="1 seul point formel", communes=len(un), population=int(un.pop_totale.sum()), points_mm=int(un.n_mm.sum())),
    dict(situation="un seul type de point formel (banque, IMF ou assurance)", communes=len(mono_type),
         population=int(mono_type.pop_totale.sum()), points_mm=int(mono_type.n_mm.sum())),
    dict(situation="0 site de DAB", communes=int((com.n_dab == 0).sum()), population=int(com[com.n_dab == 0].pop_totale.sum()),
         points_mm=int(com[com.n_dab == 0].n_mm.sum())),
])
garder("s7_c5_service_unique", c5)
zero = zero.assign(prefecture=zero.prefecture_code.map(pref.set_index("code").nom),
                   unite_regionale=zero.unite_regionale_code.map(ur.set_index("code").nom))
garder("s7_c5_communes_sans_point_formel", zero[["nom", "prefecture", "unite_regionale", "pop_totale", "pop15_prorata", "n_mm",
                                                 "mm_pour_10k_adultes"]].sort_values("pop_totale", ascending=False).round(1))
op_c = com.set_index("code").join(opc)[["nom", "n_mm", "part_moov_present_pct", "part_togocom_present_pct", "n_formels"]]
garder("s7_c5_dependance_operateur", op_c[(op_c.part_moov_present_pct < 20) | (op_c.part_togocom_present_pct < 20)]
       .sort_values("n_mm", ascending=False).reset_index())

# Territoires signalés par l'exploration (entrée du diagnostic, étape 10) : aucun classement, aucune priorité.
# Communes nommées par les contradictions 1, 3, 4 et 5 ; pour la 3, la commune la moins dotée de chaque paire.
# La contradiction 2 porte sur des préfectures : elle devient un attribut de la commune.
signaux: dict[str, list[str]] = {}


def signaler(codes, etiquette):
    for k in codes:
        signaux.setdefault(k, []).append(etiquette)


signaler(c1.code, "C1 population forte, offre faible")
for ecart, a, b, lab in (("ecart_formels_pour_10k", "fa", "fb", "points formels"),
                         ("ecart_mm_pour_10k_adultes", "ma", "mb", "mobile money")):
    top = vv.sort_values(ecart, ascending=False).head(10)
    signaler(np.where(top[a] < top[b], top.code_left, top.code_right), f"C3 voisine moins dotée ({lab})")
signaler(c4a.code, "C4 taux élevé, volume faible")
signaler(c4b.code, "C4 volume élevé, taux faible")
signaler(zero.code, "C5 mobile money uniquement")
signaler(op_c[(op_c.part_moov_present_pct < 20) | (op_c.part_togocom_present_pct < 20)].index, "C5 un opérateur dominant")
sig = com[com.code.isin(signaux)].assign(
    prefecture=lambda d: d.prefecture_code.map(pref.set_index("code").nom),
    unite_regionale=lambda d: d.unite_regionale_code.map(ur.set_index("code").nom),
    contradictions=lambda d: d.code.map(lambda k: " ; ".join(dict.fromkeys(signaux[k]))),
    prefecture_en_c2=lambda d: d.prefecture_code.isin(c2.code))
garder("s7_territoires_signales", sig[["code", "nom", "prefecture", "unite_regionale", "strate_50", "pop_totale", "n_formels",
                                       "n_mm", "n_dab", "couv_20km_pct", "couv_20km_motif", "contradictions",
                                       "prefecture_en_c2"]].sort_values(["unite_regionale", "nom"]).round(1))

# =============================================================== Écriture des tables
for nom, df in R.items():
    df.to_csv(SORTIE / f"{nom}.csv", index=False, encoding="utf-8")
print(f"{len(R)} tables écrites dans {SORTIE.relative_to(RACINE)}")

if __name__ == "__main__" and "--figures" in sys.argv:
    import figures_05  # noqa: F401
