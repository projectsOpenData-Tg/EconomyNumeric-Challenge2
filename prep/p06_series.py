"""Étape 6 — Séries nationales (04, section 5 : SN1, SN3 à SN9) → data/processed/serie_nationale.csv (format long).

Décisions appliquées : P1 (D1 : API, estimations UIT), P3 / R2 (IN1 pour nos taux nationaux), P4 / R6 (raccord
D2 / 2b jusqu'en 2017 puis AR1 ; valeur du T4 par convention, moyenne des 4 trimestres en variante ; flux = somme),
A2 (noms d'opérateurs), A3 (fixe sans technologie), A4 (CA : 2b et AR1 côte à côte), A20, S6, S7.
Aucun ratio ni classement : les indicateurs sont calculés à l'étape suivante.
"""
import json

import pandas as pd

from commun import EXTRA, INTERIM, PROCESSED, RAW, Etape, ecrire_csv, norm

ET = Etape(6, "series")
L: list[dict] = []
OPS = {"togocom": "Togocom (Togo Cellulaire)", "moov": "Moov Africa (Atlantique Telecom)",
       "togo_telecom": "Togo Telecom (YAS, fixe)", "cafe": "CAFE Informatique", "teolis": "TEOLIS", "gva": "GVA Togo",
       "ensemble": "Ensemble", "total_mobile": "Total mobile", "total_fixe": "Total fixe", "total_secteur": "Secteur"}


def ajouter(indicateur, source, periode, valeur, unite, frequence="annuel", operateur="ensemble", technologie="",
            convention="publie", variante="principal", rupture="", niveau_preuve="A", base_population="", note=""):
    if valeur is None or pd.isna(valeur):
        return
    L.append(dict(indicateur=indicateur, source=source, periode=str(periode), frequence=frequence,
                  operateur=operateur, operateur_libelle=OPS.get(operateur, operateur), technologie=technologie,
                  valeur=float(valeur), unite=unite, convention=convention, variante=variante, rupture=rupture,
                  niveau_preuve=niveau_preuve, base_population=base_population, note=note))


# --- SN1 : usage d'Internet (D1 / 1b, API ; P1)
api = json.loads((RAW / "D1_worldbank-api.json").read_text())[1]
for x in api:
    if x["value"] is not None:
        est = x["date"] != "2017"
        ajouter("usage_internet_pct_population", "D1 / 1b (Banque mondiale, API)", x["date"], x["value"],
                "% de la population", niveau_preuve="C", base_population="Banque mondiale (implicite)",
                note="estimation UIT" if est else "INSEED (enquête)")
ET.effectif("D1 (API)", len([x for x in api if x["value"] is not None]), "une valeur par année, drapeau P1",
            sum(1 for r in L if r["indicateur"] == "usage_internet_pct_population"))

# --- AR1 trimestriel (étape 5) : copie trimestrielle, puis annuel (stocks : T4 et moyenne ; flux : somme)
ar1 = pd.read_csv(INTERIM / "ar1_trimestriel.csv", dtype={"technologie": str})
ar1["technologie"] = ar1["technologie"].fillna("")
STOCKS = {"abonnes_data_mobile", "abonnes_internet_fixe", "abonnes_internet_fixe_acces", "abonnes_ftth",
          "abonnes_telephonie_mobile", "abonnes_telephonie_fixe", "mm_comptes", "mm_points_de_vente"}
for _, r in ar1.iterrows():
    ajouter(r.indicateur, "AR1 (ARCEP)", r.trimestre, r.valeur, r.unite, "trimestriel", r.operateur, r.technologie,
            rupture=r.rupture if isinstance(r.rupture, str) else "", note=f"publication {r.numero_source}"
            + (f" ; révisée ({r.ecart_revision_pct} %)" if r.revise else ""))
ar1["annee"] = ar1["trimestre"].str[:4].astype(int)
ar1["t"] = ar1["trimestre"].str[-1].astype(int)
for (ind, op, tech, an), g in ar1[ar1.annee >= 2018].groupby(["indicateur", "operateur", "technologie", "annee"]):
    unite = g.unite.iloc[0]
    complet = set(g.t) == {1, 2, 3, 4}
    rup = "; ".join(sorted({x for x in g.rupture.dropna() if x}))
    if ind in STOCKS:
        t4 = g[g.t == 4].valeur
        if len(t4):
            ajouter(ind, "AR1 (ARCEP)", an, t4.iloc[0], unite, "annuel", op, tech, "valeur_T4", "principal", rup)
        if complet:
            ajouter(ind, "AR1 (ARCEP)", an, g.valeur.mean(), unite, "annuel", op, tech, "moyenne_4T", "sensibilite", rup)
        elif an == 2026:
            ajouter(ind, "AR1 (ARCEP)", f"{an}S1", g.valeur.mean(), unite, "semestriel", op, tech, "moyenne_trimestres",
                    "principal", rup, note="année incomplète : T1 et T2 seulement")
    else:  # flux
        if complet:
            ajouter(ind, "AR1 (ARCEP)", an, g.valeur.sum(), unite, "annuel", op, tech, "somme_4T", "principal", rup)
        elif an == 2026:
            ajouter(ind, "AR1 (ARCEP)", f"{an}S1", g.valeur.sum(), unite, "semestriel", op, tech, "somme_trimestres",
                    "principal", rup, note="année incomplète : T1 et T2 seulement")

# --- SN3 : abonnements Internet jusqu'en 2017 (2b par opérateur ; D2 par technologie) ; valeurs 2019 écartées
b2 = pd.read_csv(RAW / "D2_communications-electroniques.csv")
OP_2B = {"Togo Cellulaire": "togocom", "Moov Africa Togo": "moov", "Togo Telecom": "togo_telecom",
         "CAFE Informatique": "cafe", "GVA": "gva", "TEOLIS": "teolis", "Total Mobile": "ensemble",
         "Total Fixe": "ensemble", "Total Secteur": "total_secteur"}
for _, r in b2.iterrows():
    ind = r["indicateur"]
    op = OP_2B[r["operateur"]]
    if ind == "Nombre d'abonnements internet":
        code = "abonnes_data_mobile" if r["type-operateur"] == "Mobile" else "abonnes_internet_fixe"
        tech = "total"
        if r.Date <= 2017:
            ajouter(code, "2b (INSEED, opendata)", r.Date, r.Value, "abonnés", operateur=op, technologie=tech,
                    note="raccord P4 : 2b jusqu'en 2017, AR1 ensuite")
        else:
            ajouter(code, "2b (INSEED, opendata)", r.Date, r.Value, "abonnés", operateur=op, technologie=tech,
                    variante="controle", note="non retenu après 2017 (P4)" + (" ; valeur 2019 écartée" if r.Date == 2019 else ""))
    elif ind == "Chiffre d'affaires du secteur":  # A4 : série nationale 2b, sans raccord avec AR1
        ajouter("ca", "2b (INSEED, opendata)", r.Date, r.Value / 1e9, "Md FCFA", operateur="total_secteur",
                convention="publie", note="série nationale 2010-2022 ; pas de raccord avec AR1 (A4)")
    elif ind == "Nombre d'abonnés actifs mobile money":
        ajouter("mm_abonnes_actifs", "2b (INSEED, opendata)", r.Date, r.Value, "abonnés actifs",
                rupture="2019-2020 : rupture signalée, non corrigée (A20)" if r.Date in (2019, 2020) else "")
    elif ind == "Valeur des transactions mobiles money":
        ajouter("mm_valeur_transactions", "2b (INSEED, opendata)", r.Date, r.Value / 1e9, "Md FCFA")
    else:  # télédensités et pénétration publiées (pour 100 habitants)
        code = {"Lignes télephoniques pour 100 habitants": "teledensite_fixe",
                "Abonnés à la télephonie mobile pour 100 habitants": "teledensite_mobile",
                "Abonnements à large bande fixe pour 100 habitants": "large_bande_fixe_pour_100"}[ind]
        ajouter(code, "2b (INSEED, opendata)", r.Date, r.Value, "pour 100 habitants", niveau_preuve="C",
                base_population="INSEED (implicite)")

d2 = pd.read_csv(RAW / "D2_abonnes-internet-type-acces.csv")
D2_MAP = {  # libellé → (indicateur, opérateur, technologie)
    "Abonnés GPRS /EDGE Togo Cellulaire": ("abonnes_data_mobile", "togocom", "2G"),
    "Abonnés GPRS/EDGE Atlantique Telecom": ("abonnes_data_mobile", "moov", "2G"),
    "Nombre de clients 3G Togo Cellulaire": ("abonnes_data_mobile", "togocom", "3G"),
    "Nombre de clients 3G Atlantique Telecom": ("abonnes_data_mobile", "moov", "3G+4G"),
    "Nombre de clients 4G Togo Cellulaire": ("abonnes_data_mobile", "togocom", "4G"),
    "Nombre de clients 4G Atlantique Telecom": ("abonnes_data_mobile", "moov", "4G"),
    "T Togo Cellulaire": ("abonnes_data_mobile", "togocom", "total"),
    "T Atlantique Telecom": ("abonnes_data_mobile", "moov", "total"),
    "T abonnés Internet mobiles (Toutes technologies)": ("abonnes_data_mobile", "ensemble", "total"),
    "T abonnés Internet mobiles (Haut débit)": ("abonnes_data_mobile", "ensemble", "haut_debit"),
    "T Abonnés Internet Togo Telecom": ("abonnes_internet_fixe", "togo_telecom", "total"),
    "ADSL": ("abonnes_internet_fixe_acces", "togo_telecom", "ADSL"),
    "FTTH": ("abonnes_internet_fixe_acces", "togo_telecom", "FTTH"),
    "Wimax": ("abonnes_internet_fixe_acces", "togo_telecom", "Wimax"),
    "LS Internet": ("abonnes_internet_fixe_acces", "togo_telecom", "fixe_technologie_non_precisee"),
    "LS point à point": ("abonnes_internet_fixe_acces", "togo_telecom", "fixe_technologie_non_precisee"),
    "Illiconet": ("abonnes_internet_fixe_acces", "togo_telecom", "fixe_technologie_non_precisee"),
    "EvDo": ("abonnes_internet_fixe_acces", "togo_telecom", "fixe_technologie_non_precisee"),
}
d2_tech = {}
for _, r in d2.iterrows():
    m = D2_MAP.get(r.indicateur.strip())
    if not m or r.Date > 2017:
        continue
    ind, op, tech = m
    if ind == "abonnes_data_mobile" and tech in ("total",) and op != "ensemble":
        continue  # totaux par opérateur : 2b (2010-2017), contrôlés contre D2 ci-dessous
    if ind == "abonnes_internet_fixe":
        continue
    d2_tech[(ind, op, tech, r.Date)] = d2_tech.get((ind, op, tech, r.Date), 0) + r.Value  # A3 : LS, Illiconet, EvDo sommés
for (ind, op, tech, an), v in d2_tech.items():
    if ind == "abonnes_data_mobile" and op == "ensemble" and tech == "total":
        continue  # total national : 2b
    ajouter(ind, "D2 (INSEED, opendata)", an, v, "abonnés", operateur=op, technologie=tech,
            note=("A3 : EvDo, LS, Illiconet → fixe, technologie non précisée" if tech == "fixe_technologie_non_precisee"
                  else "4G de Moov non distinguée jusqu'en 2019" if tech == "3G+4G" else ""))

# Contrôle : totaux par opérateur de D2 = 2b (2013-2017)
d2t = d2[d2.indicateur.isin(["T Togo Cellulaire", "T Atlantique Telecom"]) & (d2.Date <= 2017)]
b2t = b2[(b2.indicateur == "Nombre d'abonnements internet") & b2.operateur.isin(["Togo Cellulaire", "Moov Africa Togo"])]
ecarts = 0
for _, r in d2t.iterrows():
    op = "Togo Cellulaire" if "Cellulaire" in r.indicateur else "Moov Africa Togo"
    v = b2t[(b2t.operateur == op) & (b2t.Date == r.Date)].Value
    ecarts += int(len(v) == 1 and abs(v.iloc[0] - r.Value) > 0.5)
ET.controle("SN3-D2-2b", "totaux mobiles par opérateur : D2 = 2b (2013-2017)", 0, ecarts, ecarts == 0)

# CX3 (P4) : raccord D2 / AR1 au T4 2017 et 2018 (total data mobile, 3G de Togocel)
def ar1_q(ind, op, tech, q):
    v = ar1[(ar1.indicateur == ind) & (ar1.operateur == op) & (ar1.technologie == tech) & (ar1.trimestre == q)].valeur
    return v.iloc[0] if len(v) else None


for an in (2017, 2018):
    v_d2 = d2[(d2.indicateur == "Nombre de clients 3G Togo Cellulaire") & (d2.Date == an)].Value.iloc[0]
    v_ar1 = ar1_q("abonnes_data_mobile", "togocom", "3G", f"{an}T4")
    ET.controle("CX3", f"raccord D2 / AR1 ({an}) : 3G de Togocel", "écart nul", f"{v_d2:.0f} / {v_ar1:.0f}",
                abs(v_d2 - v_ar1) < 1)
    v_d2 = d2[(d2.indicateur == "T abonnés Internet mobiles (Toutes technologies)") & (d2.Date == an)].Value.iloc[0]
    v_ar1 = ar1_q("abonnes_data_mobile", "ensemble", "total", f"{an}T4")
    e = 100 * (v_d2 - v_ar1) / v_ar1
    ET.controle("CX3", f"raccord D2 / AR1 ({an}) : total data mobile", "≤ 0,03 %", f"{e:+.3f} %", abs(e) <= 0.035)

# --- SN4 : téléphonie (D3, 2013-2019) ; AR1 ensuite (totaux seulement : pas de tableau par opérateur)
d3 = pd.read_csv(RAW / "D3_recap-telephonie-gsm.csv")
D3_MAP = {"Le nombre total d'abonnées mobiles GSM": ("abonnes_telephonie_mobile", "ensemble", "abonnés", "A"),
          "Le nombre total d'abonnés fixe": ("abonnes_telephonie_fixe", "ensemble", "abonnés", "A"),
          "Part de marché Togo Cellulaire (en abonnées) en %": ("part_marche_telephonie_mobile", "togocom", "%", "C"),
          "Part de marché Atlantique Telecom Togo (en abonnées)": ("part_marche_telephonie_mobile", "moov", "%", "C"),
          "Chiffres d'Affaires": ("ca", "total_d3", "Md FCFA", "A"),
          "Investissement": ("investissement", "total_d3", "Md FCFA", "A")}
for _, r in d3.iterrows():
    m = D3_MAP.get(r.indicateur)
    if not m:
        continue  # ARPU écarté (A5) ; télédensités : 2b ; total fixe + mobile : redondant
    ind, op, unite, niv = m
    val = r.Value / 1e9 if unite == "Md FCFA" else r.Value
    ajouter(ind, "D3 (INSEED, opendata)", r.Date, val, unite, operateur=op, niveau_preuve=niv,
            variante="principal" if r.Date <= 2017 or ind not in ("abonnes_telephonie_mobile", "abonnes_telephonie_fixe")
            else "controle",
            note=("périmètre du CA non documenté ; sert au ratio Investissement / CA 2013-2019 (A4)" if op == "total_d3"
                  else "valeur 2019 d'origine inconnue" if r.Date == 2019 else ""))
v_d3 = d3[(d3.indicateur == "Le nombre total d'abonnées mobiles GSM") & (d3.Date == 2018)].Value.iloc[0]
v_ar1 = ar1_q("abonnes_telephonie_mobile", "ensemble", "total", "2018T4")
e = 100 * (v_d3 - v_ar1) / v_ar1
ET.controle("SN4-raccord", "téléphonie mobile : D3 2018 face à AR1 T4 2018", "égalité (raccord P4)", f"{e:+.2f} %",
            abs(e) < 0.05, bloquant=False)
ET.controle("SN4-operateurs", "abonnés téléphonie mobile par opérateur dans AR1 (tableaux)", "présents",
            "absents : graphiques seulement", False, bloquant=False)

# 3g : historique du CA et de l'investissement (1965-2010, Banque mondiale), séparé
g3 = pd.read_csv(RAW / "D3_hdx-infrastructures.csv", skiprows=[1])
for code, ind in (("IT.TEL.REVN.CN", "ca"), ("IT.TEL.INVS.CN", "investissement")):
    for _, r in g3[g3["Indicator Code"] == code].iterrows():
        ajouter(ind, "3g (Banque mondiale, historique)", int(r.Year), float(r.Value) / 1e9, "Md FCFA",
                operateur="total_secteur", variante="historique", niveau_preuve="C", note="historique séparé (A4)")

# --- SN6 : composantes de O2-05 (IT1) : chaque panier est une série distincte, jamais enchaînée
it1 = pd.read_excel(EXTRA / "obj2" / "IT1_uit_paniers-prix-tic_2008-2025.xlsx", sheet_name="economies_2008-2025")
tg = it1[(it1.IsoCode == "TGO") & (it1.Unit == "GNIpc")]
PANIERS = {"i271mb_1GB_GNI": ("principal", "O2-05b : 1 Go de data mobile seule"),
           "i271mb_2GB_GNI": ("panier_distinct", "2 Go, data seule (2021-2024 ; publié jusqu'en 2025)"),
           "i271mb_1GB5_GNI": ("panier_distinct", "1,5 Go, data seule (2018-2020)"),
           "i271md_pd_B1GB_GNI": ("panier_distinct", "1 Go postpayé sur ordinateur (2013-2017)"),
           "i271mb_5GB_GNI": ("panier_distinct", "5 Go, data seule (2025-)")}
for code, (var, lib) in PANIERS.items():
    r = tg[tg.Code == code]
    for an in [c for c in it1.columns if isinstance(c, int)]:
        if len(r) and pd.notna(r[an].iloc[0]):
            ajouter("cout_data_pct_rnb_mensuel", "IT1 (UIT)", an, r[an].iloc[0], "% du RNB mensuel par habitant",
                    technologie=code, variante=var, niveau_preuve="C", note=lib)
n1g = sum(1 for x in L if x["technologie"] == "i271mb_1GB_GNI")
ET.controle("SN6-1Go", "années du panier « 1 Go, data seule » (O2-05b)", "2023-2025 (3)", n1g, n1g == 3, bloquant=False)

# --- SN7 : mobile money, Findex (4h, tels que publiés)
for fn, ind in (("D4_worldbank-api-findex-compte.json", "compte_15ans_plus_pct"),
                ("D4_worldbank-api-findex-compte-femmes.json", "compte_femmes_15ans_plus_pct"),
                ("D4_worldbank-api-findex-compte-40-pourcent-plus-pauvres.json", "compte_40pct_plus_pauvres_pct")):
    for x in json.loads((RAW / fn).read_text())[1]:
        if x["value"] is not None:
            ajouter(ind, "4h (Findex, Banque mondiale)", x["date"], x["value"], "% des 15 ans et plus", niveau_preuve="C",
                    base_population="Findex (échantillon, 15 ans et plus)")

# --- SN8 : dénominateurs annuels (IN1)
in1 = pd.read_csv(EXTRA / "obj1" / "IN1_projections-demographiques-2011-2031.csv")
tot = in1[(in1["tranche-d-âges"] == "Togo") & (in1.sexe == "Total")].set_index("Date").Value
ages15 = ["15 - 19", "20 - 24", "25 - 29", "30 - 34", "35 - 39", "40 - 44", "45 - 49", "50 - 54", "55 - 59", "60 - 64",
          "65 - 69", "70 - 74", "75 - 79", "80 ou plus"]
p15 = in1[in1["tranche-d-âges"].isin(ages15) & (in1.sexe == "Total")].groupby("Date").Value.sum()
for an, v in tot.items():
    ajouter("population_totale", "IN1 (INSEED, projections)", an, v, "habitants", niveau_preuve="C", base_population="IN1")
for an, v in p15.items():
    ajouter("population_15ans_plus", "IN1 (INSEED, projections)", an, v, "habitants", niveau_preuve="C", base_population="IN1")
e22 = 100 * (p15[2022] - 4721488) / 4721488
ET.controle("SN8", "IN1 15 ans et plus en 2022 face au RGPH (03 : +6,6 %)", "+6,6 %", f"{e22:+.1f} %", round(e22, 1) == 6.6,
            bloquant=False)

# --- SN9 : prix (IN3a 2010-2022, IN3b 2014-2024 : fonction « Communication » et IPC) ; S7
i3b = pd.read_csv(EXTRA / "obj1" / "IN3b_indices-des-prix-fonctions-2014-2024.csv")
i3a = pd.read_csv(EXTRA / "obj1" / "IN3a_inhpc-fonctions-consommation-2010-2022.csv")
for src, df, col in (("IN3b (INSEED)", i3b, "indicateurs"), ("IN3a (INSEED)", i3a, "libellé")):
    for lib, code in (("Communication", "indice_prix_communication"), ("INDICE DES PRIX À LA CONSOMMATION (IPC)", "indice_prix_ensemble")):
        s = df[df[col] == lib]
        for _, r in s.iterrows():
            ajouter(code, src, r.Date, r.Value, "indice", "mensuel", niveau_preuve="C")
c = i3b[i3b.indicateurs == "Communication"].set_index("Date").Value
saut = 100 * (c["2020M12"] - c["2019M12"]) / c["2019M12"]
ET.controle("S7", "indice « Communication » : décembre 2019 → décembre 2020 (03 : +15 %)", "≈ +15 %, non lu comme hausse",
            f"{saut:+.1f} %", True, bloquant=False)
for x in L:
    if x["indicateur"] == "indice_prix_communication" and x["source"].startswith("IN3b") and x["periode"] == "2020M12":
        x["rupture"] = f"S7 : saut de {saut:+.1f} % sur un an, cause non vérifiée ; non lu comme une hausse des prix"
f4 = pd.read_csv(RAW / "D4_hdx-secteur-financier.csv", skiprows=[1])
for _, r in f4[f4["Indicator Code"] == "FP.CPI.TOTL.ZG"].iterrows():
    ajouter("inflation_annuelle_pct", "4g (Banque mondiale, HDX)", int(r.Year), float(r.Value), "%", niveau_preuve="C")

# --- Sortie et contrôles
sn = pd.DataFrame(L)
cle = ["indicateur", "source", "periode", "operateur", "technologie", "convention", "variante"]
doub = sn.duplicated(cle).sum()
ET.controle("SN-cle", "une seule ligne par série, période, convention et variante", 0, doub, doub == 0)
bases = sn[sn.base_population != ""].groupby("indicateur").base_population.nunique()
ET.controle("CX7", "une seule base de population par indicateur", "1", bases.max() if len(bases) else 1,
            (bases <= 1).all())
ann = sn[(sn.indicateur == "abonnes_data_mobile") & (sn.operateur == "ensemble") & (sn.technologie == "total")
         & (sn.frequence == "annuel") & (sn.variante == "principal")].periode.astype(int)
ET.controle("SN3-continuite", "abonnements data mobile, total annuel principal : 2010-2025 sans trou", "16 années",
            f"{ann.min()}-{ann.max()} ({ann.nunique()})", ann.nunique() == ann.max() - ann.min() + 1)
ca_c = sn[(sn.indicateur == "ca") & (sn.operateur == "total_secteur") & (sn.frequence == "annuel")]
for an in (2021, 2022):
    v2b = ca_c[(ca_c.source.str.startswith("2b")) & (ca_c.periode == str(an))].valeur.iloc[0]
    var = ca_c[(ca_c.source.str.startswith("AR1")) & (ca_c.periode == str(an))].valeur.iloc[0]
    ET.controle("CX6", f"CA {an} : 2b face à la somme des 4 trimestres de AR1 (03 : +2,8 % / +3,7 %)",
                "+2,8 %" if an == 2021 else "+3,7 %", f"{100 * (v2b - var) / var:+.1f} %", True, bloquant=False)
ET.sortie(ecrire_csv(sn.sort_values(["indicateur", "operateur", "technologie", "frequence", "periode"]),
                     PROCESSED / "serie_nationale.csv"))
ET.effectif("serie_nationale", "D1, 2b, D2, D3, 3g, AR1, IT1, 4h, 4g, IN1, IN3", "format long", f"{len(sn)} lignes, "
            f"{sn.indicateur.nunique()} indicateurs")
ET.fin()
