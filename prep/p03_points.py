"""Étape 3 — Points de service (04, sections 2, 3 et 4 : nettoyage, DD1 à DD3, R5, GE3).

Entrées : D4 (établissements), 4c (sites de DAB), D5 (points mobile money), GD1 (Poste).
Sortie : data/processed/points_service.csv (une ligne par point, aucune ligne supprimée).
Décisions appliquées : A6, A7, A8, A13, A21, Q5, V1 (DD1).
"""
import math

import geopandas as gpd
import pandas as pd

from commun import EXTRA, GEO, PROCESSED, RAW, Etape, ecrire_csv, norm

ET = Etape(3, "points")
ref = pd.read_csv(PROCESSED.parent / "interim" / "referentiel_territoires.csv", dtype=str)
MILLESIME = "2021/2022 (campagne PRISE)"

STATUT_GROUPE = {  # A6
    "UTILISE": "en_service",
    "FERME": "hors_service", "EN CONSTRUCTION": "hors_service", "INACHEVE": "hors_service",
    "ABANDONNE": "hors_service", "LOCATION": "hors_service", "EN REFECTION": "hors_service",
    "SANS LOCAL": "hors_service",
    "NEANT": "inconnu", "AUTRE": "inconnu", "NSP": "inconnu", "N A": "inconnu",
}
TYPE_D4 = {"Banque": "banque", "Micro-Finance": "imf", "Micro-Finace": "imf", "Mutuelle": "imf",  # A7
           "Assurance": "assurance"}
# DD1 (V1) : décisions du contrôle visuel des 18 paires, par noms (ligne principale = première du fichier).
DOUBLONS_FUSIONNES = [("ECOBANK Akodessewa", "ECOBANK d'Akodessewa"),
                      ("COOPEC Grace plus Amadahomé", "COOPEC Grâce plus Aménopé"),
                      ("COOPEC-AD Ramco", "COOPEC AD Agence Ramco"),
                      ("FINAM Agence Madiba", "Microfinance FINAM Adidogome Madiba")]
DOUBLONS_AMBIGUS = [("FUCEC Togo Bè", "COOPEC Maturite"), ("FUCEC Togo Afagnan", "COOPEC Afagnan")]


def statut(v):
    return STATUT_GROUPE.get(norm(str(v).strip("{}")), "inconnu")


def lire_points_csv(nom: str) -> gpd.GeoDataFrame:
    df = pd.read_csv(RAW / nom)
    df["ligne_source"] = df.index + 2  # l'en-tête est la ligne 1
    return gpd.GeoDataFrame(df, geometry=gpd.GeoSeries.from_wkt(df["geometry"]), crs="EPSG:4326")


# --- Lecture
d4 = lire_points_csv("D4_etablissements-financiers.csv")
c4 = lire_points_csv("D4_distributeurs-de-billets.csv")
d5 = lire_points_csv("D5_agents-mobile-money.csv")
g1 = gpd.read_file(EXTRA / "obj3" / "GD1_geodata_agences-la-poste.geojson")
g1["ligne_source"] = g1.index + 1  # rang de l'entité dans le GeoJSON
lus = [len(d4), len(c4), len(d5), len(g1)]
ET.controle("ST1", "effectifs lus (D4, 4c, D5, GD1)", [738, 184, 19788, 95], lus, lus == [738, 184, 19788, 95])

# --- Nettoyage et harmonisation (section 2)
d4["statut_groupe"] = d4["activite_statut"].map(statut)
n_stat = d4["statut_groupe"].value_counts().reindex(["en_service", "hors_service", "inconnu"]).tolist()
ET.controle("ST4", "statuts de D4 : en service / hors service / inconnu (A6)", [660, 17, 61], n_stat, n_stat == [660, 17, 61])
g1["statut_groupe"] = g1["activite_statut"].map(statut)

rows = []
for _, r in d4.iterrows():
    rows.append(dict(source="D4", id_source=r.FID, ligne_source=r.ligne_source,
                     type=TYPE_D4[r.activite_categorie.strip()], categorie_origine=r.activite_categorie,
                     statut_origine=r.activite_statut, statut_groupe=r.statut_groupe, nom=r.etab_nom,
                     nom_localite=r.nom_localite, region_nom_bdd=r.region_nom_bdd, prefecture_nom_bdd=r.prefecture_nom_bdd,
                     commune_nom_bdd=r.commune_nom_bdd, canton_nom_bdd=r.canton_nom_bdd, geometry=r.geometry))
for _, r in c4.iterrows():
    rows.append(dict(source="4c", id_source=r.FID, ligne_source=r.ligne_source, type="dab", categorie_origine=r.dab_type,
                     statut_groupe=pd.NA, nom=r.etab_nom, banque_dab=r.banque, nom_localite=r.nom_localite,
                     region_nom_bdd=r.region_nom_bdd, prefecture_nom_bdd=r.prefecture_nom_bdd,
                     commune_nom_bdd=r.commune_nom_bdd, canton_nom_bdd=r.canton_nom_bdd, geometry=r.geometry))
for _, r in d5.iterrows():
    rows.append(dict(source="D5", id_source=r.FID, ligne_source=r.ligne_source, type="mobile_money",
                     categorie_origine=r.operateur, statut_groupe=pd.NA, region_nom_bdd=r.region_nom_bdd,
                     prefecture_nom_bdd=r.prefecture_nom_bdd, commune_nom_bdd=r.commune_nom_bdd,
                     canton_nom_bdd=r.canton_nom_bdd, geometry=r.geometry))
for _, r in g1.iterrows():
    rows.append(dict(source="GD1", id_source=r.id, ligne_source=r.ligne_source, type="poste",
                     categorie_origine=r.activite_categorie, statut_origine=r.activite_statut,
                     statut_groupe=r.statut_groupe, nom=r.etab_nom, nom_localite=r.nom_localite,
                     region_nom_bdd=r.region_nom_bdd, prefecture_nom_bdd=r.prefecture_nom_bdd,
                     commune_nom_bdd=r.commune_nom_bdd, canton_nom_bdd=r.canton_nom_bdd, geometry=r.geometry))
pts = gpd.GeoDataFrame(rows, geometry="geometry", crs="EPSG:4326")
pts["en_service"] = pts["statut_groupe"].map({"en_service": 1, "hors_service": 0, "inconnu": pd.NA})

# Valeurs manquantes : jeton → NA avec motif (jamais 0)
MANQUANTS = {"NSP", "NEANT", "N A", ""}
for col in ("nom", "nom_localite"):
    brut = pts[col]
    manque = brut.isna() | brut.map(lambda v: norm(v) in MANQUANTS)
    pts[f"{col}_motif"] = manque.map({True: "non_renseigne", False: ""})
    pts[col] = brut.where(~manque, pd.NA).map(lambda v: v.strip() if isinstance(v, str) else v)
for _, r in pts[(pts.source == "4c") & (pts.nom_motif == "non_renseigne")].iterrows():
    ET.anomalie("4c", r.id_source, "etab_nom", "manquant", "gardé", "2.1", "aucun", "nom non renseigné")

# D5 : opérateurs (A8) ; « Nsp » → NA pour les deux opérateurs
op = pts["categorie_origine"].where(pts["source"] == "D5")
pts["op_moov"] = op.map({"Moov, Togocom": 1, "Moov": 1, "Togocom": 0, "Nsp": pd.NA})
pts["op_togocom"] = op.map({"Moov, Togocom": 1, "Moov": 0, "Togocom": 1, "Nsp": pd.NA})
pts["nb_operateurs"] = op.map({"Moov, Togocom": 2, "Moov": 1, "Togocom": 1, "Nsp": pd.NA})
pts["operateur_motif"] = op.map({"Nsp": "non_renseigne"}).fillna("")
n_op = op.value_counts().reindex(["Moov, Togocom", "Togocom", "Moov", "Nsp"]).tolist()
ET.controle("ST5", "opérateurs de D5 (Moov+Togocom / Togocom / Moov / Nsp)", [12649, 4773, 1018, 1348], n_op,
            n_op == [12649, 4773, 1018, 1348])
for _, r in pts[pts.operateur_motif == "non_renseigne"].iterrows():
    ET.anomalie("D5", r.id_source, "operateur", "manquant", "gardé", "A8", "aucun sur le nombre de lieux",
                "opérateur non renseigné")

# Statuts de D4 et de GD1 hors du calcul principal (A6, Q5)
for _, r in pts[pts.source.isin(["D4", "GD1"]) & (pts.statut_groupe != "en_service")].iterrows():
    dec = "exclu du calcul principal" + (" ; compté en variante" if r.statut_groupe == "inconnu" else "")
    ET.anomalie(r.source, r.id_source, "activite_statut", "statut exclu", dec, "A6" if r.source == "D4" else "Q5",
                "-1 point formel" if r.source == "D4" else "aucun (Poste hors calcul principal)",
                f"{r.statut_origine} ({r.statut_groupe})")

# --- R5 : rattachement par les noms déclarés (A21)
com = ref[ref.niveau == "commune"]
cant = ref[ref.niveau == "canton"]
code_commune = dict(zip(com.nom_norm, com.code))
code_canton = {(c, n): k for c, n, k in zip(cant.commune_code, cant.nom_norm, cant.code)}
pts["commune_code"] = pts["commune_nom_bdd"].map(norm).map(code_commune)
pts["canton_code"] = [code_canton.get((c, norm(n))) for c, n in zip(pts["commune_code"], pts["canton_nom_bdd"])]
ref_c = cant.set_index("code")
for col in ("prefecture_code", "unite_regionale_code", "region_code"):
    pts[col] = pts["canton_code"].map(ref_c[col])
non_rattaches = pts["canton_code"].isna().sum()
ET.controle("GE2", "points rattachés à un canton, donc à tous les niveaux", "100 %",
            f"{100 * (1 - non_rattaches / len(pts)):.2f} % ({non_rattaches} non rattachés)", non_rattaches == 0)
nom_pref = ref[ref.niveau == "prefecture"].set_index("code")["nom_norm"]
nom_reg = ref[ref.niveau == "region"].set_index("code")["nom_norm"]
incoh = ((pts["prefecture_nom_bdd"].map(norm) != pts["prefecture_code"].map(nom_pref))
         | (pts["region_nom_bdd"].map(norm) != pts["region_code"].map(nom_reg))).sum()
ET.controle("GE2-noms", "préfecture et région déclarées = parents du canton", 0, incoh, incoh == 0)

# --- GE3 : contrôle par la position (jamais utilisé pour déplacer un point)
def unite_du_point(couche: str, nom_col: str) -> pd.Series:
    g = gpd.read_file(GEO / f"{couche}.geojson")[["code", "geometry"]].rename(columns={"code": nom_col})
    j = gpd.sjoin(pts[["geometry"]], g, how="left", predicate="within")
    return j[~j.index.duplicated()][nom_col]


pts["pos_region"] = unite_du_point("regions", "pos_region")
pts["pos_prefecture"] = unite_du_point("prefectures", "pos_prefecture")
pts["pos_commune"] = unite_du_point("communes", "pos_commune")
pts["pos_canton"] = unite_du_point("cantons", "pos_canton")
orig = gpd.read_file(RAW / "D6_geodata-limites-prefectures.geojson")
orig["pos_prefecture_origine"] = orig["id"].str.split(".").str[1]
j = gpd.sjoin(pts[["geometry"]], orig[["pos_prefecture_origine", "geometry"]], how="left", predicate="within")
pts["pos_prefecture_origine"] = j[~j.index.duplicated()]["pos_prefecture_origine"]


def ecart(r) -> str:
    if pd.isna(r.pos_region):
        return "hors_frontiere"
    if r.pos_canton == r.canton_code and r.pos_commune != r.commune_code:
        return "canton_autre_commune"
    if r.pos_commune == r.commune_code and r.pos_prefecture_origine != r.prefecture_code:
        return "debordement_contour"
    if (r.pos_canton, r.pos_commune, r.pos_prefecture, r.pos_region) != (r.canton_code, r.commune_code,
                                                                          r.prefecture_code, r.region_code):
        return "autre_ecart"
    return ""


pts["ecart_position"] = pts.apply(ecart, axis=1)
for src in ("D4", "4c", "GD1"):
    n = (pts[pts.source == src].ecart_position != "").sum()
    ET.controle(f"GE3-{src}", f"{src} : points hors du polygone de leur unité déclarée", 0 if src != "GD1" else "signalé",
                n, n == 0, bloquant=src != "GD1")
e5 = pts[(pts.source == "D5") & (pts.ecart_position != "")].ecart_position.value_counts().to_dict()
attendu = {"hors_frontiere": 49, "debordement_contour": 22, "canton_autre_commune": 25}
ET.controle("GE3-D5", "D5 : écarts de position par type", attendu, e5, e5 == attendu, bloquant=False)
pref_apres = ((pts.source == "D5") & pts.pos_region.notna() & (pts.pos_prefecture != pts.prefecture_code)).sum()
ET.controle("GE3-R3", "D5 : écarts à la préfecture après reconstitution (hors frontière exclus)", 0, pref_apres,
            pref_apres == 0, bloquant=False)
LIB = {"hors_frontiere": "hors du Togo, à la frontière", "debordement_contour": "commune qui déborde de sa préfecture (résolu par R3)",
       "canton_autre_commune": "canton rattaché à une autre commune que son polygone (A21)", "autre_ecart": "à examiner"}
for _, r in pts[pts.ecart_position != ""].iterrows():
    ET.anomalie(r.source, r.id_source, "geometry", r.ecart_position.replace("_", " "), "signalé", "A21",
                "aucun (rattachement par les noms)", LIB[r.ecart_position])

# --- DD1 : doublons de D4 (présélection, puis décisions du contrôle visuel)
d4p = pts[pts.source == "D4"].to_crs("+proj=laea +lat_0=8.6 +lon_0=0.9 +datum=WGS84 +units=m")
cat = d4p["type"]
paires = []
xy = list(zip(d4p.index, d4p.geometry.x, d4p.geometry.y, cat))
for i in range(len(xy)):
    for k in range(i + 1, len(xy)):
        (a, xa, ya, ca), (b, xb, yb, cb) = xy[i], xy[k]
        if ca == cb and math.hypot(xa - xb, ya - yb) < 30:
            paires.append((a, b, math.hypot(xa - xb, ya - yb)))
ET.controle("DD1-presel", "paires de D4 de même catégorie à moins de 30 m", 18, len(paires), len(paires) == 18)
pts["doublon_de"] = pd.NA
pts["doublon_statut"] = ""
nom_idx = {n.strip(): i for i, n in zip(pts.index, pts["nom"]) if isinstance(n, str) and pts.at[i, "source"] == "D4"}
decides = {}
for liste, statut_sec in ((DOUBLONS_FUSIONNES, "secondaire_fusionne"), (DOUBLONS_AMBIGUS, "secondaire_variante")):
    for na, nb in liste:
        a, b = sorted((nom_idx[na], nom_idx[nb]), key=lambda i: pts.at[i, "ligne_source"])
        pts.at[b, "doublon_de"] = pts.at[a, "id_source"]
        pts.at[b, "doublon_statut"] = statut_sec
        pts.at[a, "doublon_statut"] = "principal" if statut_sec == "secondaire_fusionne" else "principal_variante"
        for col in ("nom_localite",):  # la ligne principale est complétée par la secondaire
            if pd.isna(pts.at[a, col]) and pd.notna(pts.at[b, col]):
                pts.at[a, col] = pts.at[b, col]
        decides[frozenset((a, b))] = statut_sec
for a, b, d in paires:
    s = decides.get(frozenset((a, b)), "gardé")
    lib = {"secondaire_fusionne": "fusionné dans la ligne principale", "secondaire_variante":
           "gardé ; fusionné en variante"}.get(s, "gardé : institutions différentes")
    ET.anomalie("D4", f"lignes {pts.at[a, 'ligne_source']} et {pts.at[b, 'ligne_source']}", "etab_nom",
                "doublon (fusionné ou variante)" if s != "gardé" else "paire proche, institutions différentes",
                lib, "V1 (DD1)", "-1 point formel" if s == "secondaire_fusionne" else
                ("-1 en variante" if s == "secondaire_variante" else "aucun"),
                f"{pts.at[a, 'nom']} / {pts.at[b, 'nom']} ({d:.1f} m)")
ET.controle("DD1", "doublons décidés : fusionnés / ambigus (variante) / gardés", "4 / 2 / 12",
            f"{(pts.doublon_statut == 'secondaire_fusionne').sum()} / {(pts.doublon_statut == 'secondaire_variante').sum()}"
            f" / {len(paires) - len(decides)}", len(decides) == 6 and all(frozenset((a, b)) in {frozenset(x[:2]) for x in paires}
                                                                       for a, b in [tuple(k) for k in decides]))

# --- DD3 : points de D5 proches (cellules d'environ 11 m, coordonnées arrondies à 4 décimales)
d5p = pts[pts.source == "D5"]
cellule = d5p.geometry.x.round(4).astype(str) + "_" + d5p.geometry.y.round(4).astype(str)
taille = cellule.map(cellule.value_counts())
dans_groupes, surplus = int((taille > 1).sum()), int((taille > 1).sum() - cellule[taille > 1].nunique())
ET.controle("DD3", "D5 : points partageant une cellule de ~11 m / en surplus", "974 / 509",
            f"{dans_groupes} / {surplus}", (dans_groupes, surplus) == (974, 509), bloquant=False)
pts["cellule_11m_partagee"] = 0
pts.loc[d5p.index[taille > 1], "cellule_11m_partagee"] = 1
ET.anomalie("D5", f"{dans_groupes} points", "geometry", "points proches (~11 m)", "gardés, signalés", "A8",
            "aucun", f"{surplus} en surplus ; colonne cellule_11m_partagee")

# --- Variables de comptage (principal et variantes)
formel = pts["type"].isin(["banque", "imf", "assurance"]) & (pts["source"] == "D4")
pts["compte_formel"] = (formel & (pts.en_service == 1) & (pts.doublon_statut != "secondaire_fusionne")).astype(int)
pts["compte_formel_var_statut"] = (formel & (pts.statut_groupe != "hors_service")
                                   & (pts.doublon_statut != "secondaire_fusionne")).astype(int)
pts["compte_formel_var_doublon"] = (pts["compte_formel"].astype(bool)
                                    & (pts.doublon_statut != "secondaire_variante")).astype(int)
n_f, n_v = pts.compte_formel.sum(), pts.compte_formel_var_doublon.sum()
ET.effectif("D4", 738, "statut en service (A6)", 660)
ET.effectif("D4 en service", 660, "4 lignes marquées doublon_de, fusionnées dans 4 lignes principales (V1)", n_f)
ET.effectif("D4 en service", n_f, "variante : 2 paires FUCEC / COOPEC fusionnées", n_v)
ET.controle("ST-formels", "points formels : principal / variante doublons / variante statuts", "656 / 654 / 717",
            f"{n_f} / {n_v} / {pts.compte_formel_var_statut.sum()}", (n_f, n_v) == (656, 654))
ET.effectif("4c", 184, "aucun filtre ; hors agrégat formel (DD7)", int((pts.source == "4c").sum()))
ET.effectif("D5", 19788, "ni filtre ni dédoublonnage (A8)", int((pts.source == "D5").sum()))
ET.effectif("GD1", 95, "en service, variante (Q5)", int(((pts.source == "GD1") & (pts.en_service == 1)).sum()))

# --- CX1 et CX4 : vues par opérateur non additives ; D5 face à l'ARCEP (T4 2021 : 33 924)
d5v = pts[pts.source == "D5"]
po = int(d5v.op_moov.fillna(0).sum() + d5v.op_togocom.fillna(0).sum())
nsp = int((d5v.operateur_motif == "non_renseigne").sum())
ET.controle("CX1", "lieux mobile money (total) ≠ somme des vues par opérateur", 19788,
            f"{len(d5v)} lieux ; {po} points-opérateurs hors Nsp", len(d5v) == 19788)
ET.controle("CX4", "D5 en points-opérateurs face aux 33 924 de l'ARCEP (T4 2021)",
            "31 089 / 32 437 / 33 785", f"{po} / {po + nsp} / {po + 2 * nsp} ; écarts "
            f"{100 * (33924 - po) / 33924:.1f} / {100 * (33924 - po - nsp) / 33924:.1f} / "
            f"{100 * (33924 - po - 2 * nsp) / 33924:.1f} %", po == 31089, bloquant=False)

# --- Sortie
pts["lon"], pts["lat"] = pts.geometry.x.round(7), pts.geometry.y.round(7)
pts["millesime"] = MILLESIME
pts["niveau_preuve"] = "A"
cols = ["source", "id_source", "ligne_source", "type", "categorie_origine", "statut_origine", "statut_groupe",
        "en_service", "compte_formel", "compte_formel_var_statut", "compte_formel_var_doublon", "doublon_statut",
        "doublon_de", "nom", "nom_motif", "nom_localite", "nom_localite_motif", "banque_dab", "op_moov", "op_togocom",
        "nb_operateurs", "operateur_motif", "canton_code", "commune_code", "prefecture_code", "unite_regionale_code",
        "region_code", "region_nom_bdd", "prefecture_nom_bdd", "commune_nom_bdd", "canton_nom_bdd", "lon", "lat",
        "ecart_position", "cellule_11m_partagee", "millesime", "niveau_preuve"]
sortie = pd.DataFrame(pts[cols])
ET.controle("ST2", "lignes en sortie = lignes lues (aucune supprimée)", sum(lus), len(sortie), len(sortie) == sum(lus))
ET.sortie(ecrire_csv(sortie, PROCESSED / "points_service.csv"))
ET.fin()
