"""Étape 1 — Référentiel territorial (04, section 4 : R1 à R4).

Entrées : contours de 6b (codes seuls) ; noms des unités tirés des indicateurs geodata.
Sorties : data/interim/referentiel_territoires.csv ; contours dans data/processed/geo/.
Décisions appliquées : A14 (codes geodata), A21 (codes de canton, préfectures reconstituées),
A12 (Grand Lomé en 6e unité régionale).
"""
import json

import geopandas as gpd
import pandas as pd

from commun import (CRS_SURFACE, GEO, INTERIM, PREFECTURES_GRAND_LOME, RAW, Etape, ecrire_csv, norm)

ET = Etape(1, "referentiel")
NIVEAUX = {"region": "REGION", "prefecture": "PREFECTURE", "commune": "COMMUNE", "canton": "CANTON"}
CONTOURS = {"region": "regions", "prefecture": "prefectures", "commune": "communes", "canton": "cantons"}
# A21 : codes corrigés d'après la position du polygone ; codes gardés tels que déclarés et signalés.
CANTONS_CORRIGES = {"KATI", "DJEMEGNI", "TAKPAMBA", "KPAHA", "ANIMA"}
CANTONS_SIGNALES = {"AGOME GLOZOU", "AKPAKPAKPE", "YOKELE"}

# --- Noms par code (indicateur geodata « habitants par point mobile money », présent à tous les niveaux)
noms = {}
for niv, suffixe in NIVEAUX.items():
    lignes = json.loads((RAW / f"D5_geodata-habitants-par-point-mm_{suffixe}.json").read_text())
    noms[niv] = {l[f"{niv}_id"]: l[f"{niv}_nom"].strip() for l in lignes}

# --- Contours
geo = {}
for niv, fichier in CONTOURS.items():
    g = gpd.read_file(RAW / f"D6_geodata-limites-{fichier}.geojson")
    g["code"] = g["id"].str.split(".").str[1]
    geo[niv] = g[["code", "geometry"]].to_crs(CRS_SURFACE)
    manquants = set(g["code"]) - set(noms[niv])
    ET.controle(f"R1-{niv}", f"chaque contour de {niv} a un nom geodata", 0, len(manquants), not manquants)

ET.controle("GE1", "nombre d'entités par maille = découpage geodata",
            "5 / 39 / 117 / 396", " / ".join(str(len(geo[n])) for n in CONTOURS),
            [len(geo[n]) for n in CONTOURS] == [5, 39, 117, 396])

# --- R2 : commune de chaque canton, par le code puis par la position du polygone
cant = geo["canton"].copy()
cant["nom"] = cant["code"].map(noms["canton"])
cant["commune_code_declare"] = cant["code"].str[:6]
inter = gpd.overlay(cant[["code", "geometry"]], geo["commune"].rename(columns={"code": "commune_poly"}),
                    how="intersection", keep_geom_type=True)
inter["aire"] = inter.area
commune_poly = inter.sort_values("aire").groupby("code")["commune_poly"].last()
cant["commune_code_polygone"] = cant["code"].map(commune_poly)
ecarts = cant[cant["commune_code_declare"] != cant["commune_code_polygone"]]
ET.controle("R2", "cantons dont le code ne correspond pas à la commune du polygone", 8, len(ecarts), len(ecarts) == 8)

cant["commune_code"] = cant["commune_code_declare"]
cant["drapeau"] = ""
for _, r in ecarts.iterrows():
    n = norm(r["nom"])
    if n in CANTONS_CORRIGES:
        cant.loc[cant["code"] == r["code"], "commune_code"] = r["commune_code_polygone"]
        cant.loc[cant["code"] == r["code"], "drapeau"] = "code_corrige_position"
        ET.anomalie("6b", r["code"], "commune du canton", "code corrigé", "corrigé", "A21",
                    f"commune {r['commune_code_declare']} → {r['commune_code_polygone']}", r["nom"])
    elif n in CANTONS_SIGNALES:
        cant.loc[cant["code"] == r["code"], "drapeau"] = "code_garde_signale"
        ET.anomalie("6b", r["code"], "commune du canton", "canton rattaché à une autre commune", "signalé", "A21",
                    f"gardé dans {r['commune_code_declare']}, polygone dans {r['commune_code_polygone']}", r["nom"])
    else:
        ET.controle("R2-liste", f"canton en écart hors des listes A21 : {r['nom']}", "aucun", r["nom"], False)
ET.controle("R2-bilan", "codes corrigés / gardés et signalés", "5 / 3",
            f"{(cant.drapeau == 'code_corrige_position').sum()} / {(cant.drapeau == 'code_garde_signale').sum()}",
            (cant.drapeau == "code_corrige_position").sum() == 5 and (cant.drapeau == "code_garde_signale").sum() == 3)
ET.controle("R2-parents", "chaque canton a une commune existante", 0,
            (~cant["commune_code"].isin(geo["commune"]["code"])).sum(),
            cant["commune_code"].isin(geo["commune"]["code"]).all())

# --- R3 : préfectures reconstituées par fusion des communes ; régions ; unités régionales
com = geo["commune"].copy()
com["prefecture_code"] = com["code"].str[:3]
pref = com.dissolve(by="prefecture_code").reset_index()[["prefecture_code", "geometry"]].rename(
    columns={"prefecture_code": "code"})
orig = geo["prefecture"].set_index("code")
diff_km2 = {c: orig.loc[c].geometry.symmetric_difference(g).area / 1e6 for c, g in zip(pref["code"], pref.geometry)}
modifiees = {c: round(v, 1) for c, v in diff_km2.items() if v > 1}
ET.controle("R3", "préfectures dont le contour change à la reconstitution (> 1 km²)",
            "débordements Haho 1, Oti 2, Lacs 3", modifiees, len(modifiees) > 0, bloquant=False)
reg = pref.assign(region_code=pref["code"].str[0]).dissolve(by="region_code").reset_index()[["region_code", "geometry"]]
reg = reg.rename(columns={"region_code": "code"})
ecart_reg = max(geo["region"].set_index("code").loc[c].geometry.symmetric_difference(g).area / 1e6
                for c, g in zip(reg["code"], reg.geometry))
ET.controle("R3-regions", "régions inchangées par la reconstitution (écart max, km²)", "< 1", round(ecart_reg, 3), ecart_reg < 1)


def unite_regionale(code_pref: str) -> str:
    if code_pref in PREFECTURES_GRAND_LOME:
        return "GL"
    return "A_HGL" if code_pref[0] == "A" else code_pref[0]


pref["unite_regionale_code"] = pref["code"].map(unite_regionale)
ur = pref.dissolve(by="unite_regionale_code").reset_index()[["unite_regionale_code", "geometry"]].rename(
    columns={"unite_regionale_code": "code"})
NOMS_UR = {"GL": "Grand Lomé", "A_HGL": "Maritime hors Grand Lomé", **{c: noms["region"][c] for c in "BCDE"}}

# --- R4 : superficies (projection à surfaces égales)
for g in (cant, com, pref, reg, ur):
    g["superficie_km2"] = (g.area / 1e6).round(2)
total = round(reg["superficie_km2"].sum(), 1)
ET.controle("GE5", "superficie totale (km²)", 56654.6, total, abs(total - 56654.6) < 0.5)
ET.controle("GE5-emboitement", "somme des cantons = somme des unités régionales (km²)",
            total, round(ur["superficie_km2"].sum(), 1), abs(ur["superficie_km2"].sum() - total) < 0.5)

# --- Table du référentiel (une ligne par unité, tous niveaux)
cant["prefecture_code"] = cant["commune_code"].str[:3]
com["commune_code"] = com["code"]
lignes = []
for _, r in reg.iterrows():
    lignes.append(dict(niveau="region", code=r.code, nom=noms["region"][r.code], region_code=r.code,
                       superficie_km2=r.superficie_km2))
for _, r in ur.iterrows():
    lignes.append(dict(niveau="unite_regionale", code=r.code, nom=NOMS_UR[r.code],
                       region_code="A" if r.code in ("GL", "A_HGL") else r.code, unite_regionale_code=r.code,
                       superficie_km2=r.superficie_km2))
for _, r in pref.iterrows():
    lignes.append(dict(niveau="prefecture", code=r.code, nom=noms["prefecture"][r.code], prefecture_code=r.code,
                       region_code=r.code[0], unite_regionale_code=r.unite_regionale_code, superficie_km2=r.superficie_km2))
for _, r in com.iterrows():
    lignes.append(dict(niveau="commune", code=r.code, nom=noms["commune"][r.code], commune_code=r.code,
                       prefecture_code=r.prefecture_code, region_code=r.code[0],
                       unite_regionale_code=unite_regionale(r.prefecture_code), superficie_km2=r.superficie_km2))
for _, r in cant.iterrows():
    lignes.append(dict(niveau="canton", code=r.code, nom=r.nom, canton_code=r.code, commune_code=r.commune_code,
                       prefecture_code=r.prefecture_code, region_code=r.prefecture_code[0],
                       unite_regionale_code=unite_regionale(r.prefecture_code), superficie_km2=r.superficie_km2,
                       drapeau=r.drapeau))
ref = pd.DataFrame(lignes)
ref["grand_lome"] = (ref["unite_regionale_code"] == "GL").astype(int)
ref["nom_norm"] = ref["nom"].map(norm)
cols = ["niveau", "code", "nom", "nom_norm", "canton_code", "commune_code", "prefecture_code", "unite_regionale_code",
        "region_code", "grand_lome", "superficie_km2", "drapeau"]
ref = ref.reindex(columns=cols)
ref.loc[ref.niveau == "region", "grand_lome"] = pd.NA  # la région Maritime contient le Grand Lomé sans l'être
ET.controle("GE6-communes", "communes du Grand Lomé", 13, int(ref.query("niveau=='commune'").grand_lome.sum()),
            int(ref.query("niveau=='commune'").grand_lome.sum()) == 13)
ET.sortie(ecrire_csv(ref, INTERIM / "referentiel_territoires.csv"))

# --- Contours publiés (WGS 84), préfectures reconstituées
for nom_f, g, niv in (("regions", reg, "region"), ("unites_regionales", ur, "unite_regionale"),
                      ("prefectures", pref, "prefecture"), ("communes", com, "commune"), ("cantons", cant, "canton")):
    out = g[["code", "superficie_km2", "geometry"]].merge(ref.query("niveau==@niv")[["code", "nom"]], on="code")
    chemin = GEO / f"{nom_f}.geojson"
    out.to_crs("EPSG:4326").to_file(chemin, driver="GeoJSON")
    ET.sortie(chemin)

ET.effectif("unités territoriales", "5 + 39 + 117 + 396 contours", "référentiel", len(ref))
ET.fin()
