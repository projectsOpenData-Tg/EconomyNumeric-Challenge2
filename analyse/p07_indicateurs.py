"""07 — Indicateurs (étape 08 de la procédure) : catalogue des indicateurs O1-01 à O4-06 du 02.

Sections 1 à 3 : O1-02, croissance et ruptures, calculé en premier (il ne dépend pas du 06). Section 4 : les autres
indicateurs (07_indicators.md, sections 2 à 5). Règles de O1-02, fixées avant le calcul :
- période de référence de la moyenne et de l'écart-type : 2010-2024 (P1 du 05, validé le 26/09/2026) ;
  variante de sensibilité : 2015-2024 ;
- classes, dans cet ordre : rupture de série (non classé) ; régression (g < 0) ; stagnation (|g| < 2 %, seuil
  du 02) ; ralentissement (g < moyenne - 1 écart-type, écart déclaré au 02) ; accélération (g > moyenne +
  1 écart-type) ; sinon « rythme habituel » ;
- usage (D1, estimé par l'UIT) : une accélération ou un ralentissement n'est lu que si l'enquête le confirme
  (D-15) ;
- abonnements : une année n'est classée que si la valeur du T4 et la moyenne des 4 trimestres concordent (R6) ;
  les années de rupture (2020 : S6 ; 2021 : révision de l'ARCEP) ne sont ni classées ni comptées dans la
  moyenne et l'écart-type ;
- événements (CH1) : annotés, jamais présentés comme des causes (D-16).
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "prep"))
from commun import PROCESSED, RACINE  # noqa: E402

SORTIE = RACINE / "data" / "analysis" / "07_indicateurs"
SORTIE.mkdir(parents=True, exist_ok=True)
R: dict[str, pd.DataFrame] = {}

PERIODE = (2010, 2024)       # P1, validé le 26/09/2026
VARIANTE = (2015, 2024)      # sensibilité : dix dernières années
SEUIL_STAGNATION = 2.0       # seuil du 02, conservé à côté de l'écart déclaré
# Années dont la croissance traverse un changement de base : ni classées, ni comptées dans les références
RUPTURES_ABO = {2020: "rupture S6 : 3G de Togocel reclassée au T1 2020",
                2021: "révision de l'ARCEP : 2021 abaissé de 13 à 21 %, 2020 non révisé"}

sn = pd.read_csv(PROCESSED / "serie_nationale.csv", low_memory=False, dtype={"periode": str, "technologie": str})
sn["technologie"] = sn["technologie"].fillna("")
eq = pd.read_csv(PROCESSED / "enquetes_region.csv")
ch = pd.read_csv(PROCESSED / "chronologie.csv", dtype={"date": str})


def serie(ind, tech="", source=None, freq="annuel", var="principal", op="ensemble"):
    d = sn[(sn.indicateur == ind) & (sn.operateur == op) & (sn.technologie == tech)
           & (sn.frequence == freq) & (sn.variante == var)]
    if source:
        d = d[d.source.str.startswith(source)]
    return d.set_index("periode").valeur.sort_index()


def croissance(v: pd.Series) -> pd.Series:
    return (100 * v.pct_change()).replace([np.inf, -np.inf], np.nan)


def reference(g: pd.Series, bornes, exclues=()) -> dict:
    x = g[(g.index >= bornes[0]) & (g.index <= bornes[1]) & ~g.index.isin(exclues)].dropna()
    m, s = x.mean(), x.std(ddof=1)
    return dict(debut=bornes[0], fin=bornes[1], n=len(x), moyenne=m, ecart_type=s, seuil_bas=m - s, seuil_haut=m + s)


def classe(g, ref, rupture=False):
    if rupture:
        return "non classé (rupture)"
    if pd.isna(g):
        return "non défini"
    if g < 0:
        return "régression"
    if abs(g) < SEUIL_STAGNATION:
        return "stagnation"
    if g < ref["seuil_bas"]:
        return "ralentissement"
    if g > ref["seuil_haut"]:
        return "accélération"
    return "rythme habituel"


refs = []

# =============================================================== 1. Usage d'Internet (D1, estimations de l'UIT)
d1 = serie("usage_internet_pct_population", source="D1")
d1.index = d1.index.astype(int)
note_d1 = sn[(sn.indicateur == "usage_internet_pct_population")].set_index("periode").note
note_d1.index = note_d1.index.astype(int)
u = pd.DataFrame({"pct_population": d1, "croissance_pct": croissance(d1), "variation_points": d1.diff()})
ref_u = reference(u.croissance_pct, PERIODE)
ref_u_var = reference(u.croissance_pct, VARIANTE)
refs += [dict(serie="usage (D1)", convention="publiée", role="principal", **ref_u),
         dict(serie="usage (D1)", convention="publiée", role="sensibilité", **ref_u_var)]
u["classe"] = [classe(g, ref_u) for g in u.croissance_pct]
u["classe_variante_2015"] = [classe(g, ref_u_var) if a >= VARIANTE[0] else "" for a, g in u.croissance_pct.items()]
u["source_valeur"] = note_d1.reindex(u.index)

# Contrôle par les enquêtes (D-15) : croissance annualisée entre deux vagues de même définition
vagues = []
for src, ind, popref in (("Afrobaromètre", "usage_internet_toute_frequence", None),
                         ("EHCVM", "acces_internet_declare", "individus de 15 ans et plus")):
    e = eq[(eq.domaine == "Togo") & (eq.indicateur == ind) & eq.source.str.startswith(src)]
    if popref:
        e = e[e.population_reference == popref]
    e = e.assign(an=e.vague.astype(str).str[:4].astype(int)).sort_values("an")
    for (a1, v1), (a2, v2) in zip(e[["an", "estimation_pct"]].values[:-1], e[["an", "estimation_pct"]].values[1:]):
        vagues.append(dict(source=src, debut=int(a1), fin=int(a2), valeur_debut=v1, valeur_fin=v2,
                           croissance_annualisee_pct=100 * ((v2 / v1) ** (1 / (a2 - a1)) - 1)))
vg = pd.DataFrame(vagues)
# Repère propre à chaque enquête : moyenne de ses croissances entre vagues (il en faut au moins deux)
vg["moyenne_source"] = vg.groupby("source").croissance_annualisee_pct.transform(lambda x: x.mean() if len(x) >= 2 else np.nan)
vg["sens"] = np.where(vg.moyenne_source.isna(), "une seule période : pas de repère",
                      np.where(vg.croissance_annualisee_pct > vg.moyenne_source, "au-dessus de sa moyenne",
                               "au-dessous de sa moyenne"))
R["o1_02_enquetes_periodes"] = vg.round(2)


def confirmation(annee, cl):
    if cl not in ("accélération", "ralentissement"):
        return ""
    x = vg[(vg.source == "Afrobaromètre") & (vg.debut < annee) & (vg.fin >= annee)]
    if x.empty:
        return "non vérifiable (hors des vagues de l'Afrobaromètre)"
    r = x.iloc[0]
    ok = r.croissance_annualisee_pct > r.moyenne_source if cl == "accélération" else r.croissance_annualisee_pct < r.moyenne_source
    return f"{'confirmée' if ok else 'non confirmée'} (Afrobaromètre {r.debut}-{r.fin} : {r.croissance_annualisee_pct:+.1f} %/an, moyenne {r.moyenne_source:+.1f})"


u["controle_enquete"] = [confirmation(a, c) for a, c in u.classe.items()]
u["lecture"] = [c if c not in ("accélération", "ralentissement") else
                (c if k.startswith("confirmée") else f"{c} non retenue (D-15)") for c, k in zip(u.classe, u.controle_enquete)]
R["o1_02_usage"] = u.loc[PERIODE[0]:PERIODE[1]].reset_index(names="annee").round(2)

# =============================================================== 2. Abonnements data mobile (2b, puis ARCEP)
t4 = pd.concat([serie("abonnes_data_mobile", "total", "2b"), serie("abonnes_data_mobile", "total", "AR1")])
moy = serie("abonnes_data_mobile", "total", "AR1", var="sensibilite")
trim = serie("abonnes_data_mobile", "total", "AR1", freq="trimestriel")
# Moyenne de 2017 tirée des 4 trimestres de l'ARCEP (seule source trimestrielle de 2017), pour la croissance 2018
moy17 = trim[trim.index.str.startswith("2017")]
assert len(moy17) == 4
moy = pd.concat([pd.Series({"2017": moy17.mean()}), moy])
t4.index, moy.index = t4.index.astype(int), moy.index.astype(int)
a = pd.DataFrame({"abonnes_T4": t4, "abonnes_moyenne_4T": moy})
a["source"] = ["2b (valeur annuelle publiée)" if y <= 2017 else "ARCEP" for y in a.index]
a["croissance_T4_pct"] = croissance(a.abonnes_T4)
# Avant 2018, une seule valeur annuelle publiée : les deux conventions sont identiques par construction
a["croissance_moyenne_4T_pct"] = np.where(a.index <= 2017, a.croissance_T4_pct, croissance(a.abonnes_moyenne_4T))
pop = serie("population_totale", source="IN1")
pop.index = pop.index.astype(int)
a["pour_100_hab_IN1_T4"] = 100 * a.abonnes_T4 / pop.reindex(a.index)
a["variation_points_IN1_T4"] = a.pour_100_hab_IN1_T4.diff()
a["rupture"] = [RUPTURES_ABO.get(y, "") for y in a.index]
for conv, col in (("T4", "croissance_T4_pct"), ("moyenne_4T", "croissance_moyenne_4T_pct")):
    rp = reference(a[col], PERIODE, exclues=list(RUPTURES_ABO))
    rv = reference(a[col], VARIANTE, exclues=list(RUPTURES_ABO))
    rs = reference(a[col], PERIODE)  # sensibilité : années de rupture comptées
    refs += [dict(serie="abonnements data mobile", convention=conv, role="principal", **rp),
             dict(serie="abonnements data mobile", convention=conv, role="sensibilité (2015-2024)", **rv),
             dict(serie="abonnements data mobile", convention=conv, role="sensibilité (ruptures comptées)", **rs)]
    a[f"classe_{conv}"] = [classe(g, rp, y in RUPTURES_ABO) for y, g in a[col].items()]
    a[f"classe_{conv}_variante_2015"] = [classe(g, rv, y in RUPTURES_ABO) if y >= VARIANTE[0] else ""
                                        for y, g in a[col].items()]
    a[f"classe_{conv}_ruptures_comptees"] = [classe(g, rs) for g in a[col]]


def finale(r, suffixe=""):
    c1, c2 = r[f"classe_T4{suffixe}"], r[f"classe_moyenne_4T{suffixe}"]
    if not c1:
        return ""
    if r.name <= 2017:
        return f"{c1} (une seule valeur publiée)"
    return c1 if c1 == c2 else "dépend de la convention"


# Sensibilité : abonnements Internet = data mobile + Internet fixe (valeur du T4 seule)
fixe = pd.concat([serie("abonnes_internet_fixe", "total", "2b"), serie("abonnes_internet_fixe", "total", "AR1")])
fixe.index = fixe.index.astype(int)
a["abonnes_internet_total_T4"] = a.abonnes_T4 + fixe.reindex(a.index)
a["part_data_mobile_pct"] = 100 * a.abonnes_T4 / a.abonnes_internet_total_T4
a["croissance_total_T4_pct"] = croissance(a.abonnes_internet_total_T4)
rt = reference(a.croissance_total_T4_pct, PERIODE, exclues=list(RUPTURES_ABO))
refs.append(dict(serie="abonnements Internet (data mobile + fixe)", convention="T4", role="sensibilité (périmètre)", **rt))
a["classe_total_T4"] = [classe(g, rt, y in RUPTURES_ABO) for y, g in a.croissance_total_T4_pct.items()]

a["classe_finale"] = a.apply(finale, axis=1)
a["classe_finale_variante_2015"] = a.apply(finale, axis=1, suffixe="_variante_2015")
a["classe_finale_ruptures_comptees"] = a.apply(finale, axis=1, suffixe="_ruptures_comptees")
R["o1_02_abonnements"] = a.loc[2011:].reset_index(names="annee").round(2)

# Glissement trimestriel T / T-4 (R6), à partir de 2018 : lu, non classé
q = trim.to_frame("abonnes")
q["glissement_T_T4_pct"] = (100 * q.abonnes.pct_change(4)).round(2)
q["an"] = q.index.str[:4].astype(int)
q["trimestre"] = q.index.str[-1].astype(int)
q["traverse"] = np.select([q.an == 2020, q.an == 2021], [RUPTURES_ABO[2020], RUPTURES_ABO[2021]], "")
R["o1_02_abonnements_trimestres"] = q[q.an >= 2018].reset_index(names="periode")

R["o1_02_references"] = pd.DataFrame(refs).round(2)

# =============================================================== 3. Événements retenus (CH1)
# Règle fixée avant le dessin, d'après les catégories du 02 (technologies, entrées d'opérateur, réformes
# tarifaires, crise sanitaire), plus les infrastructures. Écartés : mouvements d'indice de prix (mesures, pas
# réformes), changements de nom ou de capital, régulation générale, programme social (objectif 4), et les
# ruptures statistiques, marquées sur les séries.


def retenu(r):
    if r.type in ("technologie", "infrastructure", "crise"):
        return True, ""
    if r.type == "tarif":
        return (False, "mouvement d'indice de prix, pas une réforme") if r.evenement.startswith("Baisse de l'indice") else (True, "")
    if r.type == "opérateur":
        entree = r.evenement.startswith(("Licence", "Premiers abonnés"))
        return (True, "") if entree else (False, "pas une entrée d'opérateur (nom, capital, licence de l'opérateur historique)")
    return False, {"statistique": "rupture de série, marquée sur la série", "régulation": "régulation générale",
                   "programme": "programme social (objectif 4)"}.get(r.type, r.type)


def date_decimale(d: str) -> float:
    if "-Q" in d:
        y, qq = d.split("-Q")
        return int(y) + (int(qq) - 0.5) / 4
    p = d.split("-")
    if len(p) == 3:
        t = pd.Timestamp(d)
        return t.year + (t.dayofyear - 0.5) / (366 if t.is_leap_year else 365)
    if len(p) == 2:
        return int(p[0]) + (int(p[1]) - 0.5) / 12
    return int(p[0]) + 0.5


ev = ch.copy()
ev[["retenu", "motif_exclusion"]] = ev.apply(lambda r: pd.Series(retenu(r)), axis=1)
ev["x"] = ev.date.map(date_decimale)
ev = ev[(ev.x >= PERIODE[0] - 1) & (ev.x < 2027)].sort_values("x")
ev["numero"] = np.where(ev.retenu, ev.retenu.cumsum(), np.nan)
R["o1_02_evenements"] = ev[["numero", "date", "precision", "evenement", "type", "niveau_preuve", "retenu",
                             "motif_exclusion", "x"]].round(3)

# =============================================================== 4. Catalogue : indicateurs O1-01 à O4-06
# Règles propres à chaque indicateur : 07_indicators.md, sections 2 à 5. Classes du 02 appliquées telles quelles,
# écarts déclarés dans le 03, le 05 et le 06 (P2, P6, S6, A13, A17, R1 à R6, S1 à S10).
import json  # noqa: E402

EDA = RACINE / "data" / "analysis" / "05_eda"
SPA = RACINE / "data" / "analysis" / "06_spatial"
RAW = RACINE / "data" / "raw"
EXTRA = RAW / "_extradatas"
bm = pd.read_csv(PROCESSED / "benchmark.csv")
pts = pd.read_csv(PROCESSED / "points_service.csv", low_memory=False)
com = pd.read_csv(PROCESSED / "terr_commune.csv")
pref = pd.read_csv(PROCESSED / "terr_prefecture.csv")
ur = pd.read_csv(PROCESSED / "terr_region.csv")
noms_pref, noms_ur = pref.set_index("code").nom, ur.set_index("code").nom
com["prefecture"] = com.prefecture_code.map(noms_pref)
for t in (com, pref):
    t["unite_regionale"] = t.unite_regionale_code.map(noms_ur)
ENQ = lambda src, ind: eq[eq.source.str.startswith(src) & (eq.indicateur == ind)]  # noqa: E731


def intervalles(e, nat):
    """Écart à la moyenne nationale retenu seulement si les intervalles de confiance à 95 % ne se recoupent pas (02)."""
    return np.select([e.ic95_bas > nat.ic95_haut, e.ic95_haut < nat.ic95_bas],
                     ["au-dessus du national", "au-dessous du national"], "non distinct du national")


# ----------------------------------------------------------------- O1-01 Pénétration d'Internet
C_O101 = lambda v: np.nan if pd.isna(v) else ("déficit d'usage" if v < 40 else "rattrapage" if v <= 60 else "usage généralisé")  # noqa: E731
ssa = bm[(bm.iso3 == "SSF") & (bm.indicateur == "usage_internet_pct_population")].set_index("annee").valeur
o101 = pd.DataFrame({"pct_population": d1.loc[2000:]})
o101["classe_02"] = o101.pct_population.map(C_O101)
o101["afrique_subsaharienne_pct"] = ssa.reindex(o101.index)
o101["ecart_ass_points"] = o101.pct_population - o101.afrique_subsaharienne_pct
o101["source_valeur"] = note_d1.reindex(o101.index)
R["o1_01_penetration"] = o101.reset_index(names="annee").round(2)
pm = eq[(eq.domaine == "Togo") & eq.indicateur.isin(["usage_internet_3_mois", "usage_internet_toute_frequence", "acces_internet_declare"])
        & (eq.population_reference != "tous les individus")]
pm = pm.assign(classe_02_indicative=pm.estimation_pct.map(C_O101))[["source", "vague", "indicateur", "population_reference",
                                                                    "estimation_pct", "ic95_bas", "ic95_haut", "classe_02_indicative"]]
R["o1_01_points_mesures"] = pm.round(2)

# ----------------------------------------------------------------- O1-03 Abonnements face aux utilisateurs (en nombres, P3)


def banque_mondiale(fichier):
    d = json.load(open(RAW / fichier, encoding="utf-8"))[1]
    return pd.Series({int(r["date"]): r["value"] for r in d if r["value"] is not None}).sort_index()


pop_bm = banque_mondiale("D3_worldbank-api-abonnements-cellulaires-mobiles.json") / \
    banque_mondiale("D3_worldbank-api-telephonie-mobile-pour-100.json") * 100
o103 = pd.DataFrame({"abonnements_data_mobile": a.abonnes_T4.loc[2010:2024],
                     "utilisateurs_reconstitues": (d1 / 100 * pop_bm).loc[2010:2024],
                     "population_banque_mondiale_implicite": pop_bm.loc[2010:2024]})
o103["ecart_nombre"] = o103.abonnements_data_mobile - o103.utilisateurs_reconstitues
o103["abonnements_par_utilisateur"] = o103.abonnements_data_mobile / o103.utilisateurs_reconstitues
R["o1_03_ecart"] = o103.reset_index(names="annee").round(3)
per = []
for deb, fin, src in ((2010, 2017, "2b"), (2018, 2024, "ARCEP")):
    r0, r1 = o103.abonnements_par_utilisateur[deb], o103.abonnements_par_utilisateur[fin]
    lecture = ("écart croissant : intensification ou multi-SIM" if r1 > 1.1 * r0 else
               "écart décroissant : les utilisateurs augmentent plus vite que les abonnements" if r1 < 0.9 * r0 else
               "écart stable : élargissement réel de la base d'usagers")
    per.append(dict(periode=f"{deb}-{fin}", source_abonnements=src, ratio_debut=r0, ratio_fin=r1, lecture=lecture))
R["o1_03_periodes"] = pd.DataFrame(per).round(2)

# ----------------------------------------------------------------- O1-04 Abonnements par technologie
ab5 = pd.read_csv(EDA / "s4_abonnements_data.csv").set_index("annee")
mix = pd.read_csv(EDA / "s4_mix_technologique_T4.csv").set_index("annee")
o104 = ab5.loc[2013:, ["abonnes_data_mobile", "dont_haut_debit", "part_haut_debit_pct", "source"]].join(mix)
o104["bascule_haut_debit_02"] = np.where(o104.part_haut_debit_pct > 80, "acquise (plus de 80 %)", "non acquise")
o104["serie_retenue_pour_la_bascule"] = o104.source.str.startswith("ARCEP")
o104["rupture"] = np.where(o104.index == 2020, "S6 : aucune évolution par technologie calculée entre 2019 et 2020", "")
ftth = serie("abonnes_ftth", "FTTH", "AR1")
ftth.index = ftth.index.astype(int)
o104["abonnes_ftth_T4"] = ftth.reindex(o104.index)
o104["part_ftth_internet_pct"] = 100 * o104.abonnes_ftth_T4 / a.abonnes_internet_total_T4.reindex(o104.index)
R["o1_04_technologies"] = o104.reset_index(names="annee").round(2)

# ----------------------------------------------------------------- O1-05 Accès à Internet par région (EHCVM)
e5 = ENQ("EHCVM", "acces_internet_declare")
e5 = e5[e5.population_reference == "individus de 15 ans et plus"]
nat5 = e5[e5.domaine_type == "national"].set_index("vague")
o105 = e5[e5.domaine_type == "region"].copy()
o105["unite_regionale"] = o105.unite_regionale_code.map(noms_ur)
o105["affichable"] = np.where(o105.cv_pct < 30, "oui (CV < 30 %)", "non déterminable")
o105["ecart_national"] = [intervalles(r, nat5.loc[r.vague]) for _, r in o105.iterrows()]
o105["classe_O1_01_indicative"] = o105.estimation_pct.map(C_O101)
R["o1_05_acces_regions"] = o105[["vague", "unite_regionale_code", "unite_regionale", "estimation_pct", "ic95_bas", "ic95_haut",
                                 "cv_pct", "affichable", "ecart_national", "classe_O1_01_indicative"]].round(2)
mics = ENQ("MICS6", "internet_utilise_3_derniers_mois")
R["o1_05_mics6"] = mics[mics.domaine_type == "region"][["domaine", "population_reference", "estimation_pct"]]

# ----------------------------------------------------------------- O1-06 Freins à l'usage
alpha = ENQ("EHCVM", "alphabetisation")
alpha = alpha[(alpha.domaine_type == "region") & (alpha.vague == "2021/22") & (alpha.population_reference.str.contains("15"))]
alpha = alpha.set_index("unite_regionale_code").estimation_pct
comp = ENQ("MICS6", "au_moins_une_activite_ODD_4_4_1")
comp = comp[comp.domaine_type == "region"].pivot_table(index="domaine", columns="population_reference", values="estimation_pct")
MICS_UR = {"Maritime": "A_HGL", "Plateaux": "B", "Centrale": "C", "Kara": "D", "Savanes": "E"}
couv_ur = pd.read_csv(SPA / "s6_couverture_unites.csv").set_index("unite_regionale").couverture_ponderee_pop_pct
couv_ur.index = couv_ur.index.map({v: k for k, v in noms_ur.items()})
usage21 = o105[o105.vague == "2021/22"].set_index("unite_regionale_code").estimation_pct
cout_1go = serie("cout_data_pct_rnb_mensuel", "i271mb_1GB_GNI", "IT1").iloc[-1]
q_alpha = alpha.quantile(.25)
q_comp = comp.quantile(.25)
lignes = []
for k in noms_ur.index:
    dom = next((d for d, c in MICS_UR.items() if c == k), None)
    comp_k = comp.loc[dom] if dom in comp.index else None
    faible, couvert = usage21[k] < 40, couv_ur[k] > 85
    cap = alpha[k] <= q_alpha or (comp_k is not None and any(comp_k[c] <= q_comp[c] for c in comp.columns))
    if not faible:
        lecture = "aucun frein recherché : l'usage n'est pas faible"
    elif not couvert:
        lecture = "aucun frein affirmé : couverture (proxy) de 85 % ou moins, la règle du 02 ne s'applique pas"
    else:
        lecture = " ; ".join(x for x in ("frein de capacité présumé" if cap else "",
                                         "frein de coût présumé (1 Go au-dessus de 2 % du revenu, national)" if cout_1go > 2 else "") if x)
    lignes.append(dict(unite_regionale_code=k, unite_regionale=noms_ur[k], acces_internet_2021_22_pct=usage21[k],
                       couverture_proxy_pct=couv_ur[k], alphabetisation_15plus_pct=alpha[k],
                       **({f"competences_TIC_{c}": comp_k[c] for c in comp.columns} if comp_k is not None else {}),
                       cout_1go_pct_revenu_national=cout_1go, lecture_02=lecture))
R["o1_06_freins"] = pd.DataFrame(lignes).round(1)
smart = eq[eq.source.str.startswith("Findex") & eq.indicateur.isin(["smartphone_telephone_principal", "sans_smartphone_cause_cout"])
           & (eq.domaine == "Togo")]
R["o1_06_smartphone_national"] = smart[["indicateur", "population_reference", "vague", "estimation_pct"]]

# ----------------------------------------------------------------- O2-01 et O2-02 Parts de marché, HHI, CA contre abonnés
C_HHI = lambda h: "duopole très concentré" if h > 5000 else ("concentré" if h >= 2500 else "modéré")  # noqa: E731


def parts(ind, source, tech="", conv_var="principal"):
    t = pd.DataFrame({o: serie(ind, tech, source, var=conv_var, op=o) for o in ("togocom", "moov")})
    t.index = t.index.astype(int)
    return 100 * t.div(t.sum(axis=1), axis=0)


seg = {"abonnés data mobile (ARCEP, T4)": parts("abonnes_data_mobile", "AR1", "total"),
       "chiffre d'affaires mobile (ARCEP)": parts("ca", "AR1")}
tel = pd.DataFrame({o: serie("part_marche_telephonie_mobile", "", "D3", op=o) for o in ("togocom", "moov")})
tel.index = tel.index.astype(int)
seg["abonnés téléphonie mobile (INSEED)"] = tel
o201 = []
for nom, t in seg.items():
    for y, r in t.dropna().iterrows():
        h = r.togocom ** 2 + r.moov ** 2
        o201.append(dict(segment=nom, annee=y, part_togocom_pct=r.togocom, part_moov_pct=r.moov, hhi=h, classe_02=C_HHI(h),
                         note="rupture S6 : part de 2020 non comparable" if ("data" in nom and y == 2020) else ""))
R["o2_01_parts_hhi"] = pd.DataFrame(o201).round(1)
o202 = seg["chiffre d'affaires mobile (ARCEP)"][["togocom"]].rename(columns={"togocom": "part_ca_togocom_pct"}).join(
    seg["abonnés data mobile (ARCEP, T4)"][["togocom"]].rename(columns={"togocom": "part_abonnes_data_togocom_pct"})).join(
    tel[["togocom"]].rename(columns={"togocom": "part_abonnes_telephonie_togocom_pct"}))
o202 = o202.loc[2018:].copy()
o202["ecart_points_data"] = o202.part_ca_togocom_pct - o202.part_abonnes_data_togocom_pct
o202["ecart_points_telephonie"] = o202.part_ca_togocom_pct - o202.part_abonnes_telephonie_togocom_pct
C_O202 = lambda e: np.nan if pd.isna(e) else ("haut de marché" if e > 5 else "volume / bas prix" if e < -5 else "alignement")  # noqa: E731
o202["classe_togocom_data"] = o202.ecart_points_data.map(C_O202)
o202["classe_togocom_telephonie"] = o202.ecart_points_telephonie.map(C_O202)
o202["classe_moov_data"] = (-o202.ecart_points_data).map(C_O202)
o202.loc[2020, ["classe_togocom_data", "classe_moov_data"]] = "non classé (rupture S6)"
R["o2_02_ca_contre_abonnes"] = o202.reset_index(names="annee").round(1)

# ----------------------------------------------------------------- O2-03 et O2-04 Chiffre d'affaires, inflation, investissement
infl = serie("inflation_annuelle_pct", source="4g")
infl.index = infl.index.astype(int)
ipc = sn[(sn.indicateur == "indice_prix_ensemble") & sn.source.str.startswith("IN3b")].copy()
ipc["an"] = ipc.periode.str[:4].astype(int)
ipc_an = ipc.groupby("an").valeur.agg(["mean", "size"])
ipc_an = ipc_an[ipc_an["size"] == 12]["mean"]
infl_in3 = (100 * ipc_an.pct_change()).dropna()
inflation = pd.concat([infl.loc[:2022], infl_in3.loc[2023:]])
o203 = []
for src, lab in (("2b", "INSEED (2b)"), ("AR1", "ARCEP")):
    ca = serie("ca", "", src, op="total_secteur")
    ca.index = ca.index.astype(int)
    g = croissance(ca)
    for y in ca.index:
        gy, iy = g.get(y), inflation.get(y)
        cl = (np.nan if pd.isna(gy) else "recul nominal" if gy < 0 else "stagnation (moins de 2 %)" if gy < 2 else
              "croissance réelle positive" if (not pd.isna(iy) and gy > iy) else
              "croissance nominale sans gain réel" if not pd.isna(iy) else "inflation inconnue")
        o203.append(dict(source=lab, annee=y, ca_md_fcfa=ca[y], croissance_pct=gy, inflation_pct=iy,
                         source_inflation="IN3b (moyenne annuelle de l'indice)" if y >= 2023 else "4g (Banque mondiale)",
                         classe_02=cl, note="CA fixe publié sans GVA (T1 2021 - T1 2023)" if (src == "AR1" and 2021 <= y <= 2023) else ""))
R["o2_03_ca"] = pd.DataFrame(o203).round(2)
inv = serie("investissement", "", "AR1", op="total_secteur")
ca_ar1 = serie("ca", "", "AR1", op="total_secteur")
o204 = pd.DataFrame({"investissement_md_fcfa": inv, "ca_md_fcfa": ca_ar1})
o204.index = o204.index.astype(int)
o204["taux_investissement_pct"] = 100 * o204.investissement_md_fcfa / o204.ca_md_fcfa
o204["classe_02"] = o204.taux_investissement_pct.map(lambda v: "sous-investissement" if v < 15 else
                                                    "régime normal" if v <= 25 else "cycle d'extension")
R["o2_04_investissement"] = o204.reset_index(names="annee").round(1)

# ----------------------------------------------------------------- O2-05 ARPU (a) et coût de 1 Go (b)
ca_mob = serie("ca", "", "AR1", op="total_mobile")
abo_moy = serie("abonnes_telephonie_mobile", "total", "AR1", var="sensibilite")
abo_t4 = serie("abonnes_telephonie_mobile", "total", "AR1")
o205 = pd.DataFrame({"ca_mobile_md_fcfa": ca_mob, "abonnes_moyenne_4T": abo_moy, "abonnes_T4": abo_t4})
o205.index = o205.index.astype(int)
o205["arpu_fcfa_mois"] = o205.ca_mobile_md_fcfa * 1e9 / o205.abonnes_moyenne_4T / 12
o205["arpu_fcfa_mois_sensibilite_T4"] = o205.ca_mobile_md_fcfa * 1e9 / o205.abonnes_T4 / 12
R["o2_05a_arpu"] = o205.loc[2018:2025].reset_index(names="annee").round(0)
go1 = serie("cout_data_pct_rnb_mensuel", "i271mb_1GB_GNI", "IT1")
go1.index = go1.index.astype(int)
R["o2_05b_cout_1go"] = pd.DataFrame({"annee": go1.index, "cout_pct_revenu_mensuel": go1.values,
                                      "classe_02": np.where(go1.values > 2, "non abordable (plus de 2 %)", "abordable")}).round(2)

# ----------------------------------------------------------------- O2-06 Couverture (proxy 3i)
C_O206 = lambda v: np.nan if pd.isna(v) else ("zone blanche prioritaire (proxy)" if v < 50 else  # noqa: E731
                                               "couverture partielle (proxy)" if v <= 85 else "territoire couvert (proxy)")
o206 = []
for m, t in (("commune", com), ("préfecture", pref)):
    for _, r in t.iterrows():
        nd = r.couv_20km_motif == "non_determinable"
        douteux = (not nd) and r.couv_20km_pct < 10 and r.n_mm > 0
        o206.append(dict(maille=m, code=r.code, nom=r.nom, unite_regionale=r.unite_regionale, couverture_proxy_pct=r.couv_20km_pct,
                         classe_02="non déterminable (A13)" if nd else C_O206(r.couv_20km_pct),
                         valeur_douteuse_P6=douteux, pop_totale=r.pop_totale))
o206 = pd.DataFrame(o206)
R["o2_06_couverture"] = o206.round(2)
decl = eq[eq.source.str.contains("communautaire") & (eq.domaine_type == "region")]
R["o2_06_reception_declaree"] = decl[["vague", "domaine", "indicateur", "estimation_pct"]]

# ----------------------------------------------------------------- O2-07 Fibre : FTTH pour 100 habitants, km de fibre (3i)
pop_in1 = serie("population_totale", source="IN1")
pop_in1.index = pop_in1.index.astype(int)
o207 = pd.DataFrame({"abonnes_ftth_T4": ftth, "population_IN1": pop_in1.reindex(ftth.index)}).dropna()
o207["ftth_pour_100_habitants"] = 100 * o207.abonnes_ftth_T4 / o207.population_IN1
o207["croissance_pct"] = croissance(o207.abonnes_ftth_T4)
R["o2_07_ftth"] = o207.reset_index(names="annee").round(3)
km = {}
for couche in ("fibre-enterree", "fibre-aerienne"):
    d = json.load(open(RAW / f"D3_geodata-longueur-{couche}_PREFECTURE.json", encoding="utf-8"))
    km[couche] = pd.Series({r["prefecture_id"]: float(r["valeur"]) / 1e3 for r in d})
fib = pref[["code", "nom", "unite_regionale", "superficie_km2", "pop_totale"]].set_index("code").join(
    pd.DataFrame(km).rename(columns={"fibre-enterree": "km_fibre_enterree", "fibre-aerienne": "km_fibre_aerienne"}))
fib["raccorde_02"] = np.where((fib.km_fibre_enterree > 0) | (fib.km_fibre_aerienne > 0), "raccordé", "non raccordé")
R["o2_07_fibre_prefectures"] = fib.reset_index().round(1)

# ----------------------------------------------------------------- O2-08 Sites radio (AR2, rapport 2025, tableau 12, national)
bts = pd.DataFrame({"annee": [2021, 2022, 2023, 2024, 2025],
                    "moov_sites": [531, 621, 671, 696, 718], "yas_sites": [875, 1000, 1064, 1123, 1122],
                    "moov_2g3g_seulement": [80, 0, 0, 0, 0], "yas_2g3g_seulement": [207, 0, 0, 0, 0]})
bts["total_sites"] = bts.moov_sites + bts.yas_sites
for c in ("moov_sites", "yas_sites", "total_sites"):
    bts[f"ajouts_nets_{c.split('_')[0]}"] = bts[c].diff()
bts["source"] = "ARCEP, rapport d'activité 2025, tableau 12 (transcrit) ; un site multi-technologies compte une fois"
R["o2_08_sites_radio"] = bts

# ----------------------------------------------------------------- O3-01 Présence par type
C_O301 = lambda n: "absence" if n == 0 else ("présence marginale" if n <= 2 else "présence établie")  # noqa: E731
TYPES = {"n_banque": "banques", "n_imf": "IMF", "n_assurance": "assurances", "n_dab": "sites de DAB"}
o301 = []
for m, t in (("commune", com), ("préfecture", pref)):
    for c, lab in TYPES.items():
        cl = t[c].map(C_O301)
        for k in ("absence", "présence marginale", "présence établie"):
            o301.append(dict(maille=m, type=lab, classe_02=k, territoires=int((cl == k).sum()),
                             population=int(t.pop_totale[cl == k].sum())))
R["o3_01_presence"] = pd.DataFrame(o301)
for m, t in (("commune", com), ("prefecture", pref)):
    R[f"o3_01_presence_{m}s"] = t[["code", "nom", "unite_regionale"] + list(TYPES)].assign(
        **{f"classe_{c}": t[c].map(C_O301) for c in TYPES})

# ----------------------------------------------------------------- O3-02 Concentration et gradient
o302 = []
for seuil in ("strate_50", "strate_75"):
    g = com.groupby(seuil).agg(pop=("pop_totale", "sum"), formels=("n_formels", "sum"))
    g["part_points_pct"] = 100 * g.formels / g.formels.sum()
    g["part_population_pct"] = 100 * g["pop"] / g["pop"].sum()
    g["indice_concentration"] = g.part_points_pct / g.part_population_pct
    for k, r in g.iterrows():
        o302.append(dict(strates=seuil.replace("strate_", "seuil de ") + " % d'urbains", strate=k, **r.to_dict()))
o302 = pd.DataFrame(o302)
R["o3_02_strates"] = o302.round(3)
gl = o302[(o302.strates == "seuil de 50 % d'urbains")].set_index("strate")
crit_points, crit_pop = gl.part_points_pct["grand_lome"] > 50, gl.part_population_pct["grand_lome"] < 25
gradient = gl.indice_concentration["grand_lome"] > gl.indice_concentration["autres_villes"] > gl.indice_concentration["rural"]
gl75 = o302[(o302.strates == "seuil de 75 % d'urbains")].set_index("strate")
gradient75 = gl75.indice_concentration["grand_lome"] > gl75.indice_concentration["autres_villes"] > gl75.indice_concentration["rural"]
R["o3_02_regles"] = pd.DataFrame([
    dict(regle="Grand Lomé : plus de 50 % des points formels", valeur=gl.part_points_pct["grand_lome"], verifiee=crit_points),
    dict(regle="Grand Lomé : moins de 25 % de la population", valeur=gl.part_population_pct["grand_lome"], verifiee=crit_pop),
    dict(regle="Concentration urbaine confirmée (les deux critères)", valeur=np.nan, verifiee=crit_points and crit_pop),
    dict(regle="Gradient urbain : indice décroissant Grand Lomé > autres villes > rural (seuil 50 %)", valeur=np.nan, verifiee=gradient),
    dict(regle="Gradient urbain, sensibilité au seuil de 75 %", valeur=np.nan, verifiee=gradient75)]).round(2)

# ----------------------------------------------------------------- O3-03 Points mobile money par territoire
q_mm = com.n_mm.quantile([.25, .5, .75]).values
C_O303 = lambda n: "non desservi (0 point)" if n == 0 else f"Q{1 + int(np.searchsorted(q_mm, n, side='left'))}"  # noqa: E731
R["o3_03_points_mm"] = com[["code", "nom", "prefecture", "unite_regionale", "n_mm"]].assign(
    classe_02=com.n_mm.map(C_O303)).sort_values("n_mm")

# ----------------------------------------------------------------- O3-04 Comptes et transactions (national)
cpt = serie("mm_comptes", source="AR1")
nbt = serie("mm_nombre_transactions", source="AR1")
val = serie("mm_valeur_transactions", source="AR1")
o304 = pd.DataFrame({"comptes_T4": cpt, "transactions_millions": nbt, "valeur_md_fcfa": val})
o304.index = o304.index.astype(int)
o304 = o304.loc[2021:2025]
o304["valeur_moyenne_transaction_fcfa"] = o304.valeur_md_fcfa * 1e9 / (o304.transactions_millions * 1e6)
o304["transactions_par_compte_an"] = o304.transactions_millions * 1e6 / o304.comptes_T4
R["o3_04_arcep"] = o304.reset_index(names="annee").round(1)
fx = eq[eq.source.str.startswith("Findex") & (eq.indicateur == "compte_mobile_money") & (eq.domaine == "Togo")]
det = fx.sort_values("vague").estimation_pct.iloc[-1] if len(fx) else np.nan
R["o3_04_bceao_findex"] = pd.DataFrame([
    dict(mesure="Comptes ouverts (BCEAO, 2024, transcrit du 03)", valeur=12553441),
    dict(mesure="Comptes actifs à 90 jours (BCEAO, 2024)", valeur=6069075),
    dict(mesure="Taux d'activité (%)", valeur=100 * 6069075 / 12553441),
    dict(mesure="Points de service actifs (%) (BCEAO, 2024)", valeur=100 * 65043 / 81137),
    dict(mesure="Détention d'un compte mobile money, 15 ans et plus (%) (Findex 2024)", valeur=det)]).round(1)

# ----------------------------------------------------------------- O3-05 Usage du mobile money par région (EHCVM 2021/22)
e35 = ENQ("EHCVM", "usage_mobile_banking")
nat35 = e35[e35.domaine_type == "national"].set_index("vague")
o305 = e35[e35.domaine_type == "region"].copy()
o305["unite_regionale"] = o305.unite_regionale_code.map(noms_ur)
o305["affichable"] = np.where(o305.cv_pct < 30, "oui (CV < 30 %)", "non déterminable")
o305["ecart_national"] = [intervalles(r, nat35.loc[r.vague]) for _, r in o305.iterrows()]
R["o3_05_usage_regions"] = o305[["vague", "unite_regionale_code", "unite_regionale", "estimation_pct", "ic95_bas", "ic95_haut",
                                 "cv_pct", "affichable", "ecart_national"]].round(2)

# ----------------------------------------------------------------- O3-06 Frais du mobile money (grille Flooz, R3)
TF1 = EXTRA / "obj3" / "TF1_tarifs-mobile-money_2026-09-26"
grille = pd.read_html(TF1 / "TF1_moov_retrait-flooz.html")[0]
grille.columns = ["tranche", "tarif"]
grille["borne_haute"] = grille.tranche.str.replace(" ", " ").str.extract(r"–\s*([\d ]+)\s*F")[0].str.replace(" ", "").astype(float)
grille["frais"] = pd.to_numeric(grille.tarif.str.replace(" ", " ").str.extract(r"^([\d ]+)\s*F$")[0].str.replace(" ", ""),
                                errors="coerce")
rnb = pd.read_excel(RAW.parent / "raw" / "_extradatas" / "obj2" / "IT1_uit_paniers-prix-tic_2008-2025.xlsx", sheet_name="GNI_denominator",
                    header=None)
rnb_mois = float(rnb[rnb[0] == "Togo"].iloc[0, 1])
MONTANTS = (1_000, 10_000, 100_000)  # un montant par ordre de grandeur, fixés avant la lecture de la grille
o306 = []
for mt in MONTANTS:
    f = grille[grille.borne_haute >= mt].iloc[0].frais
    o306.append(dict(operateur="Moov Africa (Flooz)", operation="retrait chez un agent", montant_fcfa=mt, frais_fcfa=f,
                     frais_pct_montant=100 * f / mt, frais_pct_revenu_mensuel=100 * f / rnb_mois,
                     au_dessus_repere_3pct=100 * f / mt > 3))
o306 += [dict(operateur="Moov Africa (Flooz)", operation="transfert national", montant_fcfa=np.nan, frais_fcfa=0,
              note="gratuit jusqu'au troisième transfert (conditions publiées)"),
         dict(operateur="YAS Togo (Mixx)", operation="transfert national", montant_fcfa=np.nan, frais_fcfa=0,
              note="6 premiers transferts du jour gratuits, puis 1 % du montant"),
         dict(operateur="YAS Togo (Mixx)", operation="retrait chez un agent", montant_fcfa=np.nan, frais_fcfa=np.nan,
              note="grille officielle non publiée : indicateur partiel (R3)")]
o306 = pd.DataFrame(o306)
o306["revenu_mensuel_par_habitant_fcfa"] = rnb_mois
R["o3_06_frais"] = o306.round(2)

# ----------------------------------------------------------------- O4-01 à O4-04 Ratios et classes, trois mailles


def ratios(t):
    t = t.copy()
    t["hab_par_point_formel"] = (t.pop_totale / t.n_formels).where(t.n_formels > 0)
    for c in TYPES:
        t[f"hab_par_{c[2:]}"] = (t.pop_totale / t[c]).where(t[c] > 0)
    t["diversite_types"] = (t[list(TYPES)] > 0).sum(axis=1)
    t["mm_par_point_formel"] = (t.n_mm / t.n_formels).where(t.n_formels > 0)
    t["hab_par_point_mm"] = (t.pop_totale / t.n_mm).where(t.n_mm > 0)
    t["mm_pour_10k_adultes"] = 1e4 * t.n_mm / t.pop15_prorata
    return t


com, pref, ur = ratios(com), ratios(pref), ratios(ur)
C_O401 = lambda v: "non défini et critique (0 point)" if pd.isna(v) else (  # noqa: E731
    "bien desservi" if v < 10_000 else "tendu" if v <= 30_000 else "sous-desservi")
C_O403 = lambda r, n: "mobile money uniquement (0 point formel)" if n == 0 else (  # noqa: E731
    "réseaux comparables" if r < 5 else "mobile money prépondérant" if r <= 20 else "suppléance quasi totale")
C_O404 = lambda v: "absence totale (0 point)" if pd.isna(v) else (  # noqa: E731
    "maillage dense" if v < 1_000 else "acceptable" if v <= 5_000 else "maillage insuffisant")
for t in (com, pref, ur):
    t["classe_O4_01"] = t.hab_par_point_formel.map(C_O401)
    t["classe_O4_03"] = [C_O403(r, n) for r, n in zip(t.mm_par_point_formel, t.n_formels)]
    t["classe_O4_04"] = t.hab_par_point_mm.map(C_O404)
med_type = {c: com[f"hab_par_{c[2:]}"].median() for c in TYPES}
for c in TYPES:
    com[f"{c[2:]}_vs_mediane"] = np.where(com[c] == 0, "aucun point", np.where(
        com[f"hab_par_{c[2:]}"] > med_type[c], "moins bien servi que la médiane", "mieux servi que la médiane"))
Q_O401 = com.hab_par_point_formel.quantile([.25, .5, .75]).values
com["classe_O4_01_quartiles"] = com.hab_par_point_formel.map(
    lambda v: "non défini (0 point)" if pd.isna(v) else f"Q{1 + int(np.searchsorted(Q_O401, v, side='left'))} (Q4 = le moins bien servi)")

# O4-05 Statut d'accès financier, règle en cascade (première condition vraie)


def statut(t, formels="n_formels", regle5_avant_4=False):
    hpp = (t.pop_totale / t[formels]).where(t[formels] > 0)
    ratio = (t.n_mm / t[formels]).where(t[formels] > 0)
    div = (t[list(TYPES)] > 0).sum(axis=1)
    r4, r5 = ((ratio > 20) | (hpp > 30_000), "mobile money dominant"), ((div == 4) & (hpp < 10_000), "desserte diversifiée")
    r45 = [r5, r4] if regle5_avant_4 else [r4, r5]  # P9 : ordre inverse en variante, jamais à la place
    return np.select([t.pop_totale.isna() | t.n_mm.isna(), (t[formels] == 0) & (t.n_mm == 0), (t[formels] == 0) & (t.n_mm >= 1)]
                     + [c for c, _ in r45],
                     ["non déterminable", "non desservi", "mobile money uniquement"] + [k for _, k in r45], "desserte faible")


for t in (com, pref, ur):
    t["statut_O4_05"] = statut(t)
    t["n_formels_avec_poste"] = t.n_formels + t.n_poste
    t["statut_O4_05_variante_poste"] = statut(t, "n_formels_avec_poste")
    t["statut_O4_05_variante_P9"] = statut(t, regle5_avant_4=True)
COLS4 = ["code", "nom", "unite_regionale", "pop_totale", "pop15_prorata", "n_formels", "n_banque", "n_imf", "n_assurance", "n_dab",
         "n_mm", "n_poste", "hab_par_point_formel", "classe_O4_01", "diversite_types", "mm_par_point_formel", "classe_O4_03",
         "hab_par_point_mm", "mm_pour_10k_adultes", "classe_O4_04", "statut_O4_05", "statut_O4_05_variante_poste", "statut_O4_05_variante_P9"]
R["o4_communes"] = com[COLS4[:3] + ["prefecture", "strate_50"] + COLS4[3:] + ["classe_O4_01_quartiles"] +
                       [f"{c[2:]}_vs_mediane" for c in TYPES]].round(2)
R["o4_prefectures"] = pref[COLS4 + ["couv_20km_pct", "couv_20km_motif"]].round(2)
R["o4_unites_regionales"] = ur[[c for c in COLS4 if c != "unite_regionale"]].round(2)
synth = []
for m, t in (("commune", com), ("préfecture", pref)):
    for col in ("classe_O4_01", "classe_O4_03", "classe_O4_04", "statut_O4_05", "statut_O4_05_variante_poste",
                "statut_O4_05_variante_P9"):
        for k, g in t.groupby(col):
            synth.append(dict(maille=m, indicateur=col.replace("classe_", "").replace("statut_", ""), classe=k, territoires=len(g),
                              population=int(g.pop_totale.sum()), part_population_pct=100 * g.pop_totale.sum() / t.pop_totale.sum()))
R["o4_synthese_classes"] = pd.DataFrame(synth).round(1)
R["o4_05_strates"] = pd.crosstab(com.statut_O4_05, com.strate_50, values=com.pop_totale, aggfunc="sum").fillna(0).astype(int).reset_index()

# O4-02 Points pour 10 000 adultes et pour 1 000 km², par type ; repères médiane nationale et UEMOA (R1, S2 à S4)
fas = bm[bm.source.str.startswith("C5") & (bm.annee == 2024)].pivot_table(index="iso3", columns="indicateur", values="valeur")
uemoa = fas.mean()
o402 = []
for m, t in (("préfecture", pref), ("unité régionale", ur)):
    for c, lab in TYPES.items():
        p10k = 1e4 * t[c] / t.pop15_prorata
        pkm = 1e3 * t[c] / t.superficie_km2
        q1 = p10k.quantile(.25)
        for i, r in t.iterrows():
            o402.append(dict(maille=m, code=r.code, nom=r.nom, type=lab, pour_10k_adultes=p10k[i], pour_1000_km2=pkm[i],
                             mediane_nationale_10k=p10k.median(), quartile_inferieur_02=p10k[i] <= q1,
                             repere_uemoa_10k=uemoa["FB.CBK.BRCH.P5"] / 10 if c == "n_banque" else np.nan))
R["o4_02_densites"] = pd.DataFrame(o402).round(3)
R["o4_02_national_uemoa"] = pd.DataFrame([
    dict(mesure="Agences bancaires pour 100 000 adultes (FAS 2024)", togo=fas.loc["TGO", "FB.CBK.BRCH.P5"],
         moyenne_uemoa=uemoa["FB.CBK.BRCH.P5"], mediane_uemoa=fas["FB.CBK.BRCH.P5"].median()),
    dict(mesure="DAB pour 100 000 adultes (FAS 2024, appareils)", togo=fas.loc["TGO", "FB.ATM.TOTL.P5"],
         moyenne_uemoa=uemoa["FB.ATM.TOTL.P5"], mediane_uemoa=fas["FB.ATM.TOTL.P5"].median())]).round(2)

# O4-06 Matrice statut × couverture (préfecture, pondérée par la population ; commune en complément)
pc = o206[o206.maille == "préfecture"].set_index("code").classe_02
pref["couverture_O2_06"] = pref.code.map(pc)
cc = o206[o206.maille == "commune"].set_index("code")
com["couverture_O2_06"] = com.code.map(cc.classe_02)
com["couverture_douteuse_P6"] = com.code.map(cc.valeur_douteuse_P6)
for m, t in (("préfecture", pref), ("commune", com)):
    mat = pd.crosstab(t.statut_O4_05, t.couverture_O2_06, values=t.pop_totale, aggfunc="sum").fillna(0).astype(int)
    R[f"o4_06_matrice_{'prefectures' if m == 'préfecture' else 'communes'}"] = mat.reset_index()
    t["cellule_O4_06"] = np.select(
        [t.statut_O4_05.isin(["mobile money uniquement", "mobile money dominant"]) & (t.couverture_O2_06 == "zone blanche prioritaire (proxy)"),
         (t.statut_O4_05 == "desserte diversifiée") & (t.couverture_O2_06 == "territoire couvert (proxy)"),
         t.couverture_O2_06 == "non déterminable (A13)"],
        ["critique (à confirmer : couverture proxy)", "favorable", "non déterminable"], "intermédiaire")
R["o4_06_cellules"] = pd.concat([pref[["code", "nom", "unite_regionale", "pop_totale", "statut_O4_05", "couverture_O2_06", "cellule_O4_06"]]
                                 .assign(maille="préfecture"),
                                 com[["code", "nom", "unite_regionale", "pop_totale", "statut_O4_05", "couverture_O2_06",
                                      "couverture_douteuse_P6", "cellule_O4_06"]].assign(maille="commune")])

# P2 : divergence commune / préfecture (classes différentes du 02 pour O4-01, O4-03, O4-04)
pc4 = pref.set_index("code")
div = com[["code", "nom", "prefecture", "prefecture_code", "strate_50", "pop_totale"]].copy()
for ind in ("classe_O4_01", "classe_O4_03", "classe_O4_04"):
    div[f"{ind}_commune"] = com[ind].values
    div[f"{ind}_prefecture"] = div.prefecture_code.map(pc4[ind])
    div[f"diverge_{ind[7:]}"] = div[f"{ind}_commune"] != div[f"{ind}_prefecture"]
div["diverge_au_moins_une"] = div[[c for c in div if c.startswith("diverge_O")]].any(axis=1)
div["avertissement_P2"] = div.strate_50.isin(["grand_lome", "autres_villes"])
R["p2_divergence_communes"] = div
R["p2_divergence_synthese"] = pd.DataFrame([dict(indicateur=c[8:], communes_divergentes=int(div[c].sum()),
                                                 population=int(div.pop_totale[div[c]].sum()))
                                            for c in div if c.startswith("diverge_")])

for nom, df in R.items():
    df.to_csv(SORTIE / f"{nom}.csv", index=False, encoding="utf-8")
print(f"{len(R)} tables écrites dans {SORTIE.relative_to(RACINE)}")
