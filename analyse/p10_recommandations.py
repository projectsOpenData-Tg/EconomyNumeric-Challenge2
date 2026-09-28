"""10 — Recommandations (étape 11 de la procédure) : quoi faire, où, pour combien d'habitants, dans quel ordre.

Lit les tables du 07, du 08 et du 09 ; écrit des tables dans data/analysis/10_recommandations/.

Règles, fixées avant le calcul (02 : O5-02 à O5-04 ; procédure, étape 11 ; P16, P17, P19 validés le 27/09/2026) :
- recevabilité : chaque recommandation cite l'indicateur du 02 qui chiffre son écart ; sans indicateur, rejetée ;
- chaîne de la procédure : fait -> écart -> impact (habitants) -> action -> priorité ;
- cible (O5-04) : seuil de la classe supérieure du 02, base = dernier millésime. Un territoire déjà dans la meilleure
  classe du 02 mais parmi le quart le plus mal servi (rang de 75 ou plus au 08) vise la médiane des préfectures ;
- points à ajouter pour passer sous un seuil S d'habitants par point : n = pop / S arrondi au-dessus pour « S ou
  moins » (tendu, acceptable), n = partie entière de pop / S + 1 pour « moins de S » (bien desservi, dense) ;
  on compte des points, pas des agents (A8) ;
- couverture (O2-06) : population à couvrir pour atteindre le seuil T = population x (T - couverture) / 100 ;
  action toujours conditionnée à la confirmation de la couverture réelle (A17, P16) ; là où elle est inconnue,
  la première action est de la mesurer ;
- immédiat / conditionnel (P16) : points formels et points mobile money n'attendent pas ; le réseau attend ;
- priorité : (1) priorité absolue d'O5-03 aux communes « mobile money uniquement » (P17), indépendamment de la classe
  de leur préfecture : toutes ont le même statut, la population départage (règle du 02 à classe égale) ; (2) préfectures en priorité 1 (ordre du 08), puis non classées ;
  (3) réseau, conditionnel ; (4) leviers nationaux et régionaux ;
- horizons (02 : 1, 3, 5 ans), convention à valider : 1 an = premier point formel dans chaque commune « mobile money
  uniquement », et mesure de la couverture là où elle est inconnue ou douteuse ; 3 ans = seuils de classe supérieure
  des préfectures prioritaires ; 5 ans = couverture (conditionnelle), leviers nationaux et régionaux ;
- scénarios (procédure) : O1-01 prolongé en points par an (linéaire), 3 rythmes tirés d'O1-02 : tendanciel = moyenne
  2023-2024 (ralentissement confirmé) ; accéléré = moyenne 2019-2024 ; ambitieux = moyenne des années d'accélération
  (2016, 2020). O2-05b : rythme linéaire 2023-2025. Ordre de grandeur, pas une prévision ; le coût n'est pas dans
  les données.

Ajouts validés le 27/09/2026 (P21 à P25) :
- R1 : variante d'ordre par isolement (distance médiane au guichet, décroissante), affichée à côté (P21) ;
- R4a : toutes les communes de Sotouboua (zone blanche, priorité 2) s'ajoutent aux communes à mesurer (P24) ;
- R7b équipement (O1-06, composante nationale du Findex) : pas de seuil du 02, suivi en tendance ;
- R8 investissement (O2-04) : seuil du 02 de 15 % (sous-investissement) ; veille, et décision du 02 si franchi ;
- R9 fibre (O2-07) : préfectures « non raccordées » au sens du 02 ; cible = passer « raccordée » ;
- R10 sites radio (O2-08) : le 02 lit un gel quand les ajouts nets sont proches de 0 deux ans de suite et demande
  de recalibrer sur la série ; « proche de 0 » est déclaré ici comme moins de la moitié de la médiane des ajouts
  nets 2022-2025 (écart déclaré, fixé après lecture de la série, comme le 02 le prévoit).
"""
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "prep"))
from commun import PROCESSED, RACINE  # noqa: E402

A = RACINE / "data" / "analysis"
IND, SC, DG = A / "07_indicateurs", A / "08_priorisation", A / "09_diagnostic"
SORTIE = A / "10_recommandations"
SORTIE.mkdir(parents=True, exist_ok=True)
R: dict[str, pd.DataFrame] = {}
lire = lambda d, n: pd.read_csv(d / f"{n}.csv")  # noqa: E731


def au_plus(pop, s):
    """Points pour « s habitants par point ou moins »."""
    return math.ceil(pop / s)


def moins_de(pop, s):
    """Points pour « moins de s habitants par point »."""
    return math.floor(pop / s) + 1


sc = lire(SC, "score_prefectures")
pref = lire(IND, "o4_prefectures")
com = lire(IND, "o4_communes").merge(pd.read_csv(PROCESSED / "terr_commune.csv")[["code", "prefecture_code"]], on="code")
sig = lire(DG, "communes_signalees")
couv = lire(IND, "o2_06_couverture")
P1 = sc[sc.classe_retenue == "priorité 1"].sort_values("ordre_final").code.tolist()
ND = sc[sc.classe_retenue.str.startswith("non")].sort_values("sans_couv_score", ascending=False).code.tolist()
FICHES = P1 + ND
classe08 = sc.set_index("code").classe_retenue

# ----------------------------------------------------------------- R1 Priorité absolue : communes « mobile money uniquement »
mmu = com[com.statut_O4_05 == "mobile money uniquement"].copy()
mmu["classe_prefecture_08"] = mmu.prefecture_code.map(classe08)
mmu = mmu.sort_values("pop_totale", ascending=False)
mmu["ordre_action"] = np.arange(1, len(mmu) + 1)
g = sig.set_index("code")
mmu["km_guichet_mediane"] = mmu.code.map(g.km_guichet_le_plus_proche_mediane)
mmu["commune_du_guichet_le_plus_proche"] = mmu.code.map(g.commune_du_guichet_le_plus_proche)
mmu["couverture_proxy_pct"] = mmu.code.map(couv[couv.maille == "commune"].set_index("code").couverture_proxy_pct)
mmu["cellule_critique"] = mmu.code.map(g.cellule_O4_06).fillna("").str.startswith("critique")
mmu["ordre_variante_isolement"] = mmu.km_guichet_mediane.rank(ascending=False, method="first").astype(int)  # P21
mmu["points_cible_1an_sortir_du_statut"] = 1
mmu["points_cible_3ans_tendu"] = [au_plus(p, 30_000) for p in mmu.pop_totale]
mmu["points_cible_bien_desservi"] = [moins_de(p, 10_000) for p in mmu.pop_totale]
R["r1_communes_mobile_money_uniquement"] = mmu[["ordre_action", "ordre_variante_isolement", "code", "nom", "prefecture", "classe_prefecture_08", "pop_totale", "n_mm",
                                               "km_guichet_mediane", "commune_du_guichet_le_plus_proche", "couverture_proxy_pct",
                                               "cellule_critique", "points_cible_1an_sortir_du_statut", "points_cible_3ans_tendu",
                                               "points_cible_bien_desservi"]].round(1)

# ----------------------------------------------------------------- R2 Points formels : préfectures prioritaires (O4-01)
med_formel = pref.hab_par_point_formel.median()
r2 = []
for c in FICHES:
    p = pref.set_index("code").loc[c]
    hpp = p.pop_totale / p.n_formels if p.n_formels else np.inf
    if p.n_formels == 0:
        cl, cible, seuil, need = "non défini et critique (0 point)", "tendu", "30 000 ou moins", au_plus(p.pop_totale, 30_000)
    elif hpp > 30_000:
        cl, cible, seuil, need = "sous-desservi", "tendu", "30 000 ou moins", au_plus(p.pop_totale, 30_000)
    elif hpp >= 10_000:
        cl, cible, seuil, need = "tendu", "bien desservi", "moins de 10 000", moins_de(p.pop_totale, 10_000)
    else:
        cl, cible, seuil, need = "bien desservi", "médiane", f"{med_formel:.0f}", moins_de(p.pop_totale, med_formel)
    r1 = int(((mmu.prefecture_code == c)).sum())
    ajout = max(0, need - int(p.n_formels))
    r2.append(dict(code=c, nom=p.nom, classe_08=classe08[c], pop_totale=int(p.pop_totale), n_formels=int(p.n_formels), n_banque=int(p.n_banque),
                   hab_par_point_formel=hpp, classe_O4_01=cl, cible=cible, seuil_habitants_par_point=seuil, points_requis=need,
                   points_a_ajouter=ajout, dont_points_R1=min(r1, ajout), reste_apres_R1=max(0, ajout - r1)))
R["r2_prefectures_points_formels"] = pd.DataFrame(r2).round(0)

# ----------------------------------------------------------------- R3 Réseau d'agents mobile money (O4-04)
med_mm = pref.hab_par_point_mm.median()
r3 = []
for _, x in com[com.hab_par_point_mm > 5_000].iterrows():
    need = au_plus(x.pop_totale, 5_000)
    r3.append(dict(maille="commune", code=x.code, nom=x.nom, prefecture=x.prefecture, pop_totale=int(x.pop_totale), n_mm=int(x.n_mm),
                   hab_par_point_mm=x.hab_par_point_mm, classe_O4_04="maillage insuffisant", cible="acceptable",
                   seuil_habitants_par_point="5 000 ou moins", points_requis=need, points_a_ajouter=need - int(x.n_mm)))
s8 = sc.set_index("code")
for c in FICHES:
    p = pref.set_index("code").loc[c]
    rang = s8.loc[c, "sans_couv_D2_rang_pct"] if c in ND else s8.loc[c, "D2_rang_pct"]
    h = p.hab_par_point_mm
    if h > 5_000:
        cl, cible, seuil, need = "maillage insuffisant", "acceptable", "5 000 ou moins", au_plus(p.pop_totale, 5_000)
    elif h >= 1_000:
        cl, cible, seuil, need = "acceptable", "dense", "moins de 1 000", moins_de(p.pop_totale, 1_000)
    elif rang >= 75:
        cl, cible, seuil, need = "maillage dense", "médiane des préfectures", f"{med_mm:.0f}", moins_de(p.pop_totale, med_mm)
    else:
        continue
    r3.append(dict(maille="préfecture", code=c, nom=p.nom, prefecture=p.nom, pop_totale=int(p.pop_totale), n_mm=int(p.n_mm),
                   hab_par_point_mm=h, rang_D2_08=rang, classe_O4_04=cl, cible=cible, seuil_habitants_par_point=seuil,
                   points_requis=need, points_a_ajouter=need - int(p.n_mm)))
R["r3_maillage_mobile_money"] = pd.DataFrame(r3).round(1)

# ----------------------------------------------------------------- R4 Couverture réseau (O2-06), conditionnelle
cp = couv[couv.maille == "préfecture"].set_index("code")
r4 = []
cibles_couv = FICHES + [c for c in cp.index if cp.loc[c, "couverture_proxy_pct"] < 50 and c not in FICHES]
for c in cibles_couv:
    v, pop = cp.loc[c, "couverture_proxy_pct"], int(cp.loc[c, "pop_totale"])
    if pd.isna(v):
        r4.append(dict(code=c, nom=cp.loc[c, "nom"], classe_08=classe08[c], pop_totale=pop, couverture_proxy_pct=np.nan,
                       classe_O2_06="non déterminable (A13)", cible="mesurer la couverture réelle", pop_hors_couverture_theorique=np.nan,
                       pop_a_couvrir_pour_la_cible=np.nan, action="immédiate : mesure", condition="préalable à toute action réseau"))
        continue
    cl = "zone blanche" if v < 50 else "couverture partielle" if v <= 85 else "territoire couvert"
    if cl == "territoire couvert":
        continue
    t_ = 50 if cl == "zone blanche" else 85
    r4.append(dict(code=c, nom=cp.loc[c, "nom"], classe_08=classe08[c], pop_totale=pop, couverture_proxy_pct=v, classe_O2_06=cl,
                   cible=f"{t_} %", pop_hors_couverture_theorique=round(pop * (100 - v) / 100), pop_a_couvrir_pour_la_cible=round(pop * (t_ - v) / 100),
                   action="conditionnelle" if c in FICHES else "mesure (R4a) ; hors R4b (P24)",
                   condition="confirmer la couverture réelle (A17)" + ("; P16" if cp.loc[c, "nom"] == "Kéran" else "")))
r4 = pd.DataFrame(r4)
cc = couv[couv.maille == "commune"]
sotou = cp.index[cp.nom == "Sotouboua"][0]
mesure = cc[cc.classe_02.str.startswith("non déterminable") | cc.valeur_douteuse_P6.astype(bool)
            | cc.code.isin(com[com.prefecture_code == sotou].code)]  # P24 : Sotouboua entière
R["r4_couverture"] = r4
R["r4_communes_a_mesurer"] = mesure[["code", "nom", "unite_regionale", "pop_totale", "couverture_proxy_pct", "classe_02", "valeur_douteuse_P6"]]

# ----------------------------------------------------------------- R5 Frais du mobile money (O3-06), national
fr6 = lire(IND, "o3_06_frais")
f1k = fr6[(fr6.operation == "retrait chez un agent") & (fr6.montant_fcfa == 1000)].iloc[0]
pop_mm = com[com.statut_O4_05.isin(["mobile money uniquement", "mobile money dominant"])].pop_totale.sum()
R["r5_frais_mobile_money"] = pd.DataFrame([dict(
    operation="retrait chez un agent, 1 000 FCFA (Flooz)", frais_fcfa=f1k.frais_fcfa, frais_pct=f1k.frais_pct_montant,
    repere_pct=3.0, frais_cible_fcfa=30.0, baisse_necessaire_pct=100 * (1 - 30 / f1k.frais_fcfa),
    pop_communes_mm_uniquement_ou_dominant=int(pop_mm), note="grille Mixx du retrait non publiée : indicateur partiel (R3)")]).round(1)

# ----------------------------------------------------------------- R6 Coût de la data (O2-05b), national
c1 = lire(IND, "o2_05b_cout_1go").set_index("annee").cout_pct_revenu_mensuel
base, a0, a1 = c1.iloc[-1], c1.index[0], c1.index[-1]
rythme = (c1.iloc[-1] - c1.iloc[0]) / (a1 - a0)
R["r6_cout_data"] = pd.DataFrame([dict(
    base_2025_pct=base, cible_pct=2.0, baisse_relative_necessaire_pct=100 * (1 - 2 / base), rythme_2023_2025_points_par_an=rythme,
    annee_cible_au_rythme_actuel=a1 + math.ceil(round((base - 2) / -rythme, 6)), rythme_necessaire_pour_2030=(2 - base) / (2030 - a1),
    valeur_2030_au_rythme_actuel=base + rythme * (2030 - a1),
    multiple_du_rythme_actuel=((2 - base) / (2030 - a1)) / rythme, points_de_la_serie=len(c1))]).round(2)

# ----------------------------------------------------------------- R7 Compétences numériques (O1-06), régions à frein de capacité
eq = pd.read_csv(PROCESSED / "enquetes_region.csv")
alpha = eq[eq.source.str.startswith("EHCVM") & (eq.indicateur == "alphabetisation") & (eq.domaine_type == "region")
           & (eq.vague == "2021/22") & eq.population_reference.str.contains("15")].set_index("unite_regionale_code").estimation_pct
comp = eq[eq.source.str.startswith("MICS6") & (eq.indicateur == "au_moins_une_activite_ODD_4_4_1") & (eq.domaine_type == "region")]
comp = comp.pivot_table(index="domaine", columns="population_reference", values="estimation_pct")
q_alpha, q_comp = alpha.quantile(.25), comp.quantile(.25)
ur = pd.read_csv(PROCESSED / "terr_region.csv").set_index("code")
MICS_UR = {"Maritime": "A_HGL", "Plateaux": "B", "Centrale": "C", "Kara": "D", "Savanes": "E"}
fr1 = lire(IND, "o1_06_freins").set_index("unite_regionale_code")
r7 = []
for k in fr1.index[fr1.lecture_02.str.contains("capacité")]:
    dom = next(d for d, v in MICS_UR.items() if v == k)
    ligne = dict(code=k, region=fr1.loc[k, "unite_regionale"], pop15=int(ur.loc[k, "pop15_prorata"]),
                 alphabetisation_pct=alpha[k], seuil_quartile_alphabetisation=q_alpha, frein_alphabetisation=alpha[k] <= q_alpha,
                 ecart_alphabetisation_points=max(0, q_alpha - alpha[k]))
    for c in comp.columns:
        ligne[f"competences_{c}"] = comp.loc[dom, c]
        ligne[f"seuil_quartile_{c}"] = q_comp[c]
        ligne[f"frein_{c}"] = comp.loc[dom, c] <= q_comp[c]
    r7.append(ligne)
R["r7_competences"] = pd.DataFrame(r7).round(2)

# ----------------------------------------------------------------- R8 Scénarios d'usage d'Internet (O1-01), ordre de grandeur
u = lire(IND, "o1_02_usage").set_index("annee")
b = lire(IND, "o1_01_penetration").set_index("annee").pct_population
RYTHMES = {"tendanciel (moyenne 2023-2024)": u.loc[[2023, 2024], "variation_points"].mean(),
           "accéléré (moyenne 2019-2024)": u.loc[2019:2024, "variation_points"].mean(),
           "ambitieux (années d'accélération 2016 et 2020)": u.loc[[2016, 2020], "variation_points"].mean()}
sce = []
for nom, r in RYTHMES.items():
    for a in range(2025, 2031):
        sce.append(dict(scenario=nom, points_par_an=r, annee=a, pct_population=min(100, b[2024] + r * (a - 2024))))
sce = pd.DataFrame(sce)
syn = sce.groupby("scenario").agg(points_par_an=("points_par_an", "first"),
                                  pct_2030=("pct_population", "last")).reset_index()
syn["annee_60pct"] = [2024 + math.ceil(round((60 - b[2024]) / r, 6)) for r in syn.points_par_an]
syn["classe_2030"] = np.select([syn.pct_2030 > 60, syn.pct_2030 >= 40], ["usage généralisé", "rattrapage"], "déficit d'usage")
R["r8_scenarios_usage"] = sce.round(2)
R["r8_scenarios_synthese"] = syn.round(2)

# ----------------------------------------------------------------- R7b Équipement en smartphone (O1-06, composante nationale)
sm = lire(IND, "o1_06_smartphone_national").set_index("indicateur").estimation_pct
pop15 = int(pd.read_csv(PROCESSED / "terr_region.csv").pop15_prorata.sum())
R["r7b_equipement"] = pd.DataFrame([dict(
    smartphone_telephone_principal_pct=sm["smartphone_telephone_principal"], sans_smartphone_cause_cout_pct=sm["sans_smartphone_cause_cout"],
    adultes_15_plus=pop15, adultes_citant_le_cout=round(pop15 * sm["sans_smartphone_cause_cout"] / 100),
    seuil_02="aucun (quartile inférieur non calculable : national seulement)", suivi="tendance, prochain Findex", source="Findex 2024 (C)")]).round(1)

# ----------------------------------------------------------------- R8 Investissement (O2-04)
inv = lire(IND, "o2_04_investissement").set_index("annee").taux_investissement_pct
pente = inv.iloc[-1] - inv.iloc[-2]
R["r8_investissement"] = pd.DataFrame([dict(
    base_2025_pct=inv.iloc[-1], classe_02="régime normal (15 à 25 %)", seuil_sous_investissement_pct=15.0,
    marge_points=inv.iloc[-1] - 15, pic_recent_pct=inv.loc[2023], variation_2024_2025_points=pente,
    valeur_2026_si_la_variation_2024_2025_se_repete=inv.iloc[-1] + pente,
    decision_02_si_franchi="recommander un mécanisme de financement (fonds de service universel)")]).round(1)

# ----------------------------------------------------------------- R9 Fibre (O2-07) : préfectures non raccordées
fib = lire(IND, "o2_07_fibre_prefectures")
nr = fib[fib.raccorde_02 == "non raccordé"].copy()
nr["classe_08"] = nr.code.map(classe08)
ordre9 = {"priorité 1": 1, "non déterminable (couverture)": 2, "priorité 2": 3, "priorité 3": 4}
nr = nr.assign(_o=nr.classe_08.map(ordre9)).sort_values(["_o", "pop_totale"], ascending=[True, False]).drop(columns="_o")
R["r9_fibre_non_raccordees"] = nr[["code", "nom", "unite_regionale", "classe_08", "pop_totale", "superficie_km2", "km_fibre_enterree",
                                   "km_fibre_aerienne", "raccorde_02"]]

# ----------------------------------------------------------------- R10 Sites radio (O2-08)
st = lire(IND, "o2_08_sites_radio").set_index("annee")
aj = st.ajouts_nets_total.dropna()
med = aj.median()
R["r10_sites_radio"] = pd.DataFrame([dict(
    sites_2025=int(st.loc[2025, "total_sites"]), ajouts_nets_2022=aj.loc[2022], ajouts_nets_2023=aj.loc[2023], ajouts_nets_2024=aj.loc[2024],
    ajouts_nets_2025=aj.loc[2025], ajouts_nets_yas_2025=st.loc[2025, "ajouts_nets_yas"], mediane_2022_2025=med,
    seuil_declare_proche_de_zero=med / 2, annees_sous_le_seuil_consecutives=int((aj[::-1] < med / 2).cummin().sum()),  # depuis 2025, à rebours
    regle_02="gel si ajouts nets proches de 0 deux ans de suite")]).round(1)

# ----------------------------------------------------------------- Synthèse et suivi (O5-04)
r2d, r3d = R["r2_prefectures_points_formels"], R["r3_maillage_mobile_money"]
r4c = r4[r4.action == "conditionnelle"]
p1c = r4c[r4c.classe_08 == "priorité 1"]
pop_nat = int(pref.pop_totale.sum())
SYN = [
    dict(id="R1", volet="inclusion financière (O5-03)", recommandation="un premier point formel dans chaque commune « mobile money uniquement »",
         indicateur="O4-01, O4-05", territoires=f"{len(mmu)} communes", population=int(mmu.pop_totale.sum()), nature="immédiate", horizon="1 an",
         cible=f"{len(mmu)} points (1 par commune) ; seuil « tendu » à 3 ans : {int(mmu.points_cible_3ans_tendu.sum())} points"),
    dict(id="R2", volet="inclusion financière (O5-03)", recommandation="points formels dans les préfectures prioritaires, jusqu'au seuil de classe supérieure",
         indicateur="O4-01", territoires=f"{len(r2d)} préfectures", population=int(r2d.pop_totale.sum()), nature="immédiate", horizon="3 ans",
         cible=f"{int(r2d.points_a_ajouter.sum())} points, dont {int(r2d.dont_points_R1.sum())} apportés par R1"),
    dict(id="R3", volet="inclusion financière (O5-03)", recommandation="points mobile money là où le maillage est insuffisant ou dans le quart le plus mal servi",
         indicateur="O4-04", territoires=f"{int((r3d.maille == 'préfecture').sum())} préfectures et {int((r3d.maille == 'commune').sum())} communes au maillage insuffisant",
         population=int(r3d[r3d.maille == "préfecture"].pop_totale.sum()), nature="immédiate", horizon="3 ans",
         cible=f"{int(r3d[r3d.maille == 'préfecture'].points_a_ajouter.sum())} points pour les préfectures ; {int(r3d[r3d.maille == 'commune'].points_a_ajouter.sum())} pour les communes insuffisantes"),
    dict(id="R4a", volet="Internet (O5-02)", recommandation="mesurer la couverture réelle là où elle est inconnue ou douteuse", indicateur="O2-06",
         territoires=f"{len(mesure)} communes", population=int(mesure.pop_totale.sum()), nature="immédiate", horizon="1 an",
         cible="couverture déterminable dans chaque commune"),
    dict(id="R4b", volet="Internet (O5-02)", recommandation="étendre le réseau dans les préfectures prioritaires sous 85 % (Kéran : 50 %)", indicateur="O2-06, O4-06",
         territoires=f"{len(p1c)} préfectures", population=int(p1c.pop_hors_couverture_theorique.sum()), nature="conditionnelle", horizon="5 ans",
         cible=f"{int(p1c.pop_a_couvrir_pour_la_cible.sum())} habitants de plus dans la couverture théorique"),
    dict(id="R5", volet="inclusion financière (O5-03)", recommandation="frais du retrait de petit montant sous le repère de 3 %", indicateur="O3-06",
         territoires="national ; d'abord là où le mobile money n'a pas d'alternative", population=int(pop_mm), nature="immédiate", horizon="5 ans",
         cible="retrait de 1 000 FCFA : de 75 à 30 FCFA au plus"),
    dict(id="R6", volet="Internet (O5-02)", recommandation="coût de 1 Go sous 2 % du revenu mensuel", indicateur="O2-05b", territoires="national",
         population=pop_nat, nature="immédiate", horizon="5 ans", cible="de 5,30 % à 2 % : baisse de 62 % à revenu constant"),
    dict(id="R7", volet="Internet (O5-02)", recommandation="compétences numériques dans les régions à frein de capacité présumé", indicateur="O1-06",
         territoires="Savanes, Plateaux", population=int(R["r7_competences"].pop15.sum()), nature="immédiate", horizon="5 ans",
         cible="sortir du quartile inférieur (alphabétisation ; compétences TIC)"),
    dict(id="R7b", volet="Internet (O5-02)", recommandation="réduire le frein de coût sur le smartphone", indicateur="O1-06 (équipement, national)",
         territoires="national", population=int(R["r7b_equipement"].adultes_citant_le_cout.iloc[0]), nature="immédiate", horizon="5 ans",
         cible="baisse de la part des adultes sans smartphone pour raison de coût (32,1 %) ; pas de seuil du 02"),
    dict(id="R8", volet="Internet (O5-02), marché", recommandation="garder l'investissement au-dessus du seuil de sous-investissement",
         indicateur="O2-04", territoires="national", population=pop_nat, nature="veille", horizon="chaque année",
         cible="15 % du chiffre d'affaires au moins (16,3 % en 2025)"),
    dict(id="R9", volet="Internet (O5-02), marché", recommandation="étendre la fibre aux préfectures non raccordées", indicateur="O2-07",
         territoires=f"{len(nr)} préfectures", population=int(nr.pop_totale.sum()), nature="immédiate", horizon="5 ans",
         cible="chaque préfecture « raccordée » au sens du 02"),
    dict(id="R10", volet="Internet (O5-02), marché", recommandation="relancer les ajouts nets de sites radio", indicateur="O2-08",
         territoires="national ; d'abord les zones blanches de R4b", population=pop_nat, nature="veille", horizon="1 à 3 ans",
         cible=f"au moins {med / 2:.0f} ajouts nets par an (seuil déclaré)"),
]
R["synthese_recommandations"] = pd.DataFrame(SYN)

# ----------------------------------------------------------------- Trajectoires de référence (page Estimations et projections, 27/09/2026)
# Même règle que le scénario tendanciel du Togo : moyenne des deux dernières variations annuelles, prolongée
# linéairement depuis la dernière année observée de chaque série. Ordre de grandeur, pas une prévision.
bm = pd.read_csv(PROCESSED / "benchmark.csv")
b5 = bm[bm.source.str.startswith("C5b") & (bm.indicateur == "usage_internet_pct_population")]
serie = b5.pivot_table(index="annee", columns="iso3", values="valeur")
uemoa = [c for c in serie.columns if c != "SSF"]
serie["UEMOA_mediane"] = serie[uemoa].median(axis=1).where(serie[uemoa].notna().all(axis=1))
ref = []
for code, nom in (("TGO", "Togo"), ("SSF", "Afrique subsaharienne"), ("UEMOA_mediane", "UEMOA, médiane des 8 pays")):
    x = serie[code].dropna()
    rythme_ = x.diff().iloc[-2:].mean()
    ref.append(dict(territoire=nom, derniere_annee=int(x.index[-1]), valeur=x.iloc[-1], rythme_points_par_an=rythme_,
                    valeur_2030=min(100, x.iloc[-1] + rythme_ * (2030 - x.index[-1]))))
ref = pd.DataFrame(ref)
# Togo : mêmes valeurs que le scénario tendanciel (même règle, série des indicateurs), pour n'afficher qu'un chiffre
tend = next(k for k in RYTHMES if k.startswith("tendanciel"))
ref.loc[ref.territoire == "Togo", ["valeur", "rythme_points_par_an", "valeur_2030"]] = [b[2024], RYTHMES[tend], b[2024] + RYTHMES[tend] * 6]
a24 = serie.loc[2024, uemoa].sort_values(ascending=False)
ref["rang_uemoa_2024"] = ref.territoire.map({"Togo": f"{list(a24.index).index('TGO') + 1} sur {len(a24)}"})
R["r8_trajectoires_reference"] = ref.round(2)

# ----------------------------------------------------------------- Non retenues ou rejetées
R["non_retenues"] = pd.DataFrame([
    dict(piste="interopérabilité ou concurrence (Mô : 50 % des points Togocom seul)", statut="rejetée comme recommandation (P19)",
         raison="aucun indicateur du 02 ne la chiffre ; gardée comme constat"),
    dict(piste="usage du mobile money dans la Centrale (19,9 %)", statut="non retenue en l'état",
         raison="cause non établie (H3 du 06) : l'offre et l'accès à Internet n'y sont pas faibles"),
    dict(piste="sensibilisation, demande d'Internet", statut="non retenue",
         raison="aucun indicateur du 02 ne mesure la demande ; l'écart d'accès (O1-05) est traité par ses freins (R6, R7, R7b)"),
    dict(piste="leviers tirés des événements d'O1-02", statut="rejetée", raison="les événements sont des coïncidences, pas des causes (D-16)"),
    dict(piste="optimisation de localisation sur les lieux candidats (GD2)", statut="non faite", raison="aucune population sous la commune : "
         "le gain en habitants d'un site ne peut pas être calculé (point à valider)"),
])

for nom, df in R.items():
    df.to_csv(SORTIE / f"{nom}.csv", index=False, encoding="utf-8")
print(f"{len(R)} tables écrites dans {SORTIE.relative_to(RACINE)}")
