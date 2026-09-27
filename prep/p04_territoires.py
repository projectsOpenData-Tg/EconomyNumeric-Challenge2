"""Étape 4 — Tables territoriales (04, section 6) : dim_territoire, terr_commune, terr_prefecture, terr_region.

Les tables portent numérateurs et dénominateurs ; aucun ratio, classement ni score (04, principe 8).
Décisions appliquées : A6, A8, A9 (DAB hors agrégat), A12, A13 (zéro vérifié ; couverture non déterminable),
A17 (3i en proxy, niveau C), A18 (geodata en contrôle), Q5 (Poste en variante), S5, O3-02 (strates).
"""
import json

import pandas as pd

from commun import INTERIM, PROCESSED, RAW, Etape, ecrire_csv

ET = Etape(4, "territoires")
ref = pd.read_csv(INTERIM / "referentiel_territoires.csv", dtype={"grand_lome": "Int64"})
pop = pd.read_csv(INTERIM / "population_territoires.csv")
pts = pd.read_csv(PROCESSED / "points_service.csv", low_memory=False)
PREF_A13 = {"C02": "Mô", "C04": "Tchamba", "E02": "Kpendjal"}  # couverture « non déterminable » (A13)

# --- Comptages par point (colonnes 0/1), puis somme par unité
p = pd.DataFrame({
    "commune_code": pts.commune_code, "prefecture_code": pts.prefecture_code,
    "unite_regionale_code": pts.unite_regionale_code,
    "n_banque": (pts.type == "banque") & (pts.compte_formel == 1),
    "n_imf": (pts.type == "imf") & (pts.compte_formel == 1),
    "n_assurance": (pts.type == "assurance") & (pts.compte_formel == 1),
    "n_formels": pts.compte_formel == 1,                      # agrégat du 02 (O4-01) : DAB exclus
    "n_formels_var_statut": pts.compte_formel_var_statut == 1,  # A6 : + statuts inconnus
    "n_formels_var_doublon": pts.compte_formel_var_doublon == 1,  # V1 : + fusion FUCEC / COOPEC
    "n_dab": pts.type == "dab",                                # sites (A19), pas appareils
    "n_mm": pts.type == "mobile_money",                        # lieux (A8)
    "n_mm_moov": (pts.type == "mobile_money") & (pts.op_moov == 1),         # non additif
    "n_mm_togocom": (pts.type == "mobile_money") & (pts.op_togocom == 1),   # non additif
    "n_mm_operateur_nd": (pts.type == "mobile_money") & (pts.operateur_motif == "non_renseigne"),
    "n_poste": (pts.type == "poste") & (pts.en_service == 1),  # variante Q5
}).astype({c: int for c in ["n_banque", "n_imf", "n_assurance", "n_formels", "n_formels_var_statut",
                            "n_formels_var_doublon", "n_dab", "n_mm", "n_mm_moov", "n_mm_togocom",
                            "n_mm_operateur_nd", "n_poste"]})
COMPTES = [c for c in p.columns if c.startswith("n_")]

# --- Couverture 3i (proxy, niveau C) aux niveaux publiés
def couverture(niveau_json: str, cle: str) -> pd.Series:
    d = json.loads((RAW / f"D3_geodata-pct-habitants-couverts-reseau-mobile-20km_{niveau_json}.json").read_text())
    return pd.Series({x[cle]: float(x["valeur"]) for x in d})


couv = {"commune": couverture("COMMUNE", "commune_id"), "prefecture": couverture("PREFECTURE", "prefecture_id"),
        "region": couverture("REGION", "region_id")}
couv_nat = float(json.loads((RAW / "D3_geodata-pct-habitants-couverts-reseau-mobile-20km_PAYS.json").read_text())[0]["valeur"])
ET.controle("CX2", "couverture nationale de 3i ni à 0 % ni à 100 %", "0 < x < 100", couv_nat, 0 < couv_nat < 100)


def table(niveau: str, cle: str) -> pd.DataFrame:
    unites = ref[ref.niveau == niveau].copy()
    t = unites.merge(p.groupby(cle)[COMPTES].sum(), left_on="code", right_index=True, how="left")
    # A13 : un territoire sans point est un vrai zéro seulement s'il a été enquêté (preuve : points de D5)
    t["enquete_prouvee"] = (t["n_mm"].fillna(0) > 0).astype(int)
    for c in COMPTES:
        t[c] = t[c].fillna(0).astype(int).where(t["enquete_prouvee"] == 1, pd.NA)
    pp = pop[pop.niveau == niveau].set_index("code")
    for c in ["pop_totale", "pop_urbaine", "pop_rurale", "part_urbaine", "pop15_prorata", "pop15_hors_nd",
              "strate_50", "strate_75"]:
        if c in pp:
            t[c] = t["code"].map(pp[c])
    t["source_population"] = "RGPH-5 2022 (RG2, RG3)"
    # Couverture 3i : NA « non déterminable » si < 1 % alors que D5 prouve un réseau (critère de A13)
    s = couv.get(niveau if niveau != "unite_regionale" else "region")
    if s is not None and niveau != "unite_regionale":
        t["couv_20km_pct"] = t["code"].map(s)
    elif niveau == "unite_regionale":
        t["couv_20km_pct"] = t["code"].map(lambda c: s.get(c) if c in "BCDE" else pd.NA)
    contradiction = (t["couv_20km_pct"] < 1) & (t["n_mm"] > 0)
    t["couv_20km_motif"] = ""
    t.loc[t["couv_20km_pct"].isna(), "couv_20km_motif"] = "non_publie"
    t.loc[contradiction, "couv_20km_motif"] = "non_determinable"
    for _, r in t[contradiction].iterrows():
        dans_a13 = r["prefecture_code"] in PREF_A13 if pd.notna(r.get("prefecture_code")) else False
        ET.anomalie("3i", r["code"], "couv_20km_pct", "manquant", "mis à NA (non déterminable)",
                    "A13" if dans_a13 else "A13 (critère étendu, à confirmer)",
                    f"{r['couv_20km_pct']} % → NA", f"{r['nom']} : {int(r['n_mm'])} points mobile money")
    t.loc[contradiction, "couv_20km_pct"] = pd.NA
    t["couv_20km_niveau_preuve"] = "C"
    t["millesime_points"] = "2021/2022 (PRISE)"
    return t


cols_communs = ["code", "nom", "niveau", "commune_code", "prefecture_code", "unite_regionale_code", "region_code",
                "grand_lome", "superficie_km2", "pop_totale", "pop_urbaine", "pop_rurale", "part_urbaine",
                "pop15_prorata", "pop15_hors_nd", "strate_50", "strate_75", "source_population", *COMPTES,
                "enquete_prouvee", "couv_20km_pct", "couv_20km_motif", "couv_20km_niveau_preuve", "millesime_points"]
tc = table("commune", "commune_code")
tp = table("prefecture", "prefecture_code")
tr = table("unite_regionale", "unite_regionale_code")
ET.controle("GE1-tables", "lignes des tables communes / préfectures / unités régionales", "117 / 39 / 6",
            f"{len(tc)} / {len(tp)} / {len(tr)}", (len(tc), len(tp), len(tr)) == (117, 39, 6))

# --- Contrôles d'emboîtement et de totaux (GE4)
totaux = {c: int(p[c].sum()) for c in COMPTES}
for nom, t in (("communes", tc), ("préfectures", tp), ("unités régionales", tr)):
    ecarts = {c: int(t[c].sum()) - totaux[c] for c in COMPTES if int(t[c].sum()) != totaux[c]}
    ET.controle(f"GE4-{nom}", f"{nom} : sommes des comptages = totaux des points", "aucun écart", ecarts or "aucun écart",
                not ecarts)
    ecart_pop = int(t["pop_totale"].sum()) - 8095498
    ET.controle(f"GE4-pop-{nom}", f"{nom} : population totale", 8095498, int(t["pop_totale"].sum()), ecart_pop == 0)
ET.controle("GE4-totaux", "totaux nationaux : formels / DAB / mobile money / Poste", "656 / 184 / 19788 / 84",
            f"{totaux['n_formels']} / {totaux['n_dab']} / {totaux['n_mm']} / {totaux['n_poste']}",
            (totaux["n_formels"], totaux["n_dab"], totaux["n_mm"], totaux["n_poste"]) == (656, 184, 19788, 84))
ET.controle("A13-enquete", "communes sans point mobile money (enquête non prouvée)", 0,
            int((tc.enquete_prouvee == 0).sum()), int((tc.enquete_prouvee == 0).sum()) == 0)
z_c, z_p = int((tc.n_formels == 0).sum()), int((tp.n_formels == 0).sum())
ET.effectif("zéros vérifiés (points formels en service)", "117 communes / 39 préfectures", "A13",
            f"{z_c} communes et {z_p} préfecture(s) à 0, enquête prouvée par D5")
ET.controle("A13-kpendjal", "préfectures sans point formel", "Kpendjal", tp[tp.n_formels == 0].nom.tolist(),
            tp[tp.n_formels == 0].nom.tolist() == ["Kpendjal"], bloquant=False)
nd_pref = tp[tp.couv_20km_motif == "non_determinable"].nom.tolist()
ET.controle("A13-couv", "préfectures à couverture non déterminable", sorted(PREF_A13.values()), sorted(nd_pref),
            sorted(nd_pref) == sorted(PREF_A13.values()))
nd_com_hors = tc[(tc.couv_20km_motif == "non_determinable") & ~tc.prefecture_code.isin(PREF_A13)].nom.tolist()
ET.controle("A13-couv-communes", "communes non déterminables hors des 3 préfectures de A13 (critère étendu)",
            "à confirmer", nd_com_hors, True, bloquant=False)

# --- CX5 : comptages pré-calculés de geodata (4j), en contrôle seulement (A18)
def g_nat(nom: str) -> float:
    return float(json.loads((RAW / f"D4_geodata-{nom}_PAYS.json").read_text())[0]["valeur"])


tous_d4 = pts[pts.source == "D4"]
cx5 = {"banques (toutes lignes)": (g_nat("nombre-agences-bancaires"), int((tous_d4.type == "banque").sum())),
       "microfinances (« Micro-Finance » seul)": (g_nat("nombre-agences-microfinance"),
                                                  int((tous_d4.categorie_origine == "Micro-Finance").sum())),
       "assurances (toutes lignes)": (g_nat("nombre-agences-assurance"), int((tous_d4.type == "assurance").sum())),
       "DAB": (g_nat("nombre-dab"), int((pts.type == "dab").sum())),
       "Poste (toutes lignes)": (g_nat("nombre-agences-poste"), int((pts.type == "poste").sum()))}
for k, (g, n) in cx5.items():
    ET.controle("CX5", f"geodata (4j) face à notre recomptage : {k}", int(g), n, int(g) == n, bloquant=False)

# --- Sorties
for t, nom in ((tc, "terr_commune"), (tp, "terr_prefecture"), (tr, "terr_region")):
    ET.sortie(ecrire_csv(t.reindex(columns=cols_communs), PROCESSED / f"{nom}.csv"))
dim = ref.merge(pop[pop.niveau == "commune"][["code", "part_urbaine", "strate_50", "strate_75"]], on="code", how="left")
ET.sortie(ecrire_csv(dim, PROCESSED / "dim_territoire.csv"))
ET.effectif("tables territoriales", "20 805 points ; 168 unités peuplées", "agrégation", f"{len(tc)} + {len(tp)} + {len(tr)} lignes")
ET.fin()
