"""06 — Analyse spatiale (suite de l'étape 07 de la procédure) : où se trouvent l'offre, les écarts et les déficits.

Tables écrites dans data/analysis/06_spatial/ ; les cartes sont dans cartes_06.py. Règles fixées avant le calcul
(06_data_spatial_analysis.md, section 1) :
- aucune classe du 02 (seuils de O4-01, O4-03, O4-04, statut O4-05, matrice O4-06), aucun score ;
- P2 : trois mailles (commune, préfecture, unité régionale) ; Grand Lomé agrégé comme lecture de référence ;
- P3 : voisinage = contours qui se touchent ; poids normalisés par ligne ;
- distances à vol d'oiseau, en projection à surfaces égales ; seuils de lecture 5 et 10 km (conventions) ;
- autocorrélation : indice de Moran et indicateurs locaux (LISA), 999 permutations, seuil 5 %, graine fixe.
"""
import sys
from pathlib import Path

import json

import geopandas as gpd
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from scipy.stats import spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "prep"))
from commun import CRS_SURFACE, GEO, PROCESSED, RACINE  # noqa: E402

SORTIE = RACINE / "data" / "analysis" / "06_spatial"
SORTIE.mkdir(parents=True, exist_ok=True)
EDA = RACINE / "data" / "analysis" / "05_eda"
R: dict[str, pd.DataFrame] = {}
SEUILS_KM = (5, 10)
PERMUTATIONS, ALPHA = 999, 0.05
rng = np.random.default_rng(2026)


def garder(nom, df):
    R[nom] = df
    return df


com = pd.read_csv(PROCESSED / "terr_commune.csv")
pref = pd.read_csv(PROCESSED / "terr_prefecture.csv")
ur = pd.read_csv(PROCESSED / "terr_region.csv")
pts = pd.read_csv(PROCESSED / "points_service.csv", low_memory=False)
noms_pref, noms_ur = pref.set_index("code").nom, ur.set_index("code").nom


def ratios(t):
    """Ratios descriptifs, un dénominateur par ratio (comme le 05) ; non défini quand le dénominateur de points est nul."""
    t = t.copy()
    t["formels_pour_10k_hab"] = 1e4 * t.n_formels / t.pop_totale
    t["mm_pour_10k_adultes"] = 1e4 * t.n_mm / t.pop15_prorata
    t["dab_pour_100k_adultes"] = 1e5 * t.n_dab / t.pop15_prorata
    t["hab_par_point_formel"] = (t.pop_totale / t.n_formels).where(t.n_formels > 0)
    t["hab_par_point_mm"] = (t.pop_totale / t.n_mm).where(t.n_mm > 0)
    t["mm_par_point_formel"] = (t.n_mm / t.n_formels).where(t.n_formels > 0)
    t["formels_pour_1000_km2"] = 1e3 * t.n_formels / t.superficie_km2
    t["mm_pour_1000_km2"] = 1e3 * t.n_mm / t.superficie_km2
    # Quotient de localisation (O3-02) : part des points formels du pays / part de la population du pays
    t["quotient_localisation_formels"] = (t.n_formels / t.n_formels.sum()) / (t.pop_totale / t.pop_totale.sum())
    return t


com, pref, ur = ratios(com), ratios(pref), ratios(ur)
com["prefecture"] = com.prefecture_code.map(noms_pref)
com["unite_regionale"] = com.unite_regionale_code.map(noms_ur)
# P2 : avertissement « population résidente, pas fréquentation » pour les communes urbaines
com["avertissement_p2"] = com.strate_50.isin(["grand_lome", "autres_villes"])
pref["unite_regionale"] = pref.unite_regionale_code.map(noms_ur)
COLS = ["pop_totale", "pop15_prorata", "n_formels", "n_mm", "n_dab", "formels_pour_10k_hab", "mm_pour_10k_adultes",
        "dab_pour_100k_adultes", "hab_par_point_formel", "hab_par_point_mm", "mm_par_point_formel",
        "formels_pour_1000_km2", "mm_pour_1000_km2", "quotient_localisation_formels", "couv_20km_pct", "couv_20km_motif"]
garder("s3_communes", com[["code", "nom", "prefecture", "unite_regionale", "strate_50", "avertissement_p2"] + COLS].round(3))
garder("s3_prefectures", pref[["code", "nom", "unite_regionale"] + COLS].round(3))
garder("s3_unites_regionales", ur[["code", "nom"] + [c for c in COLS if not c.startswith("couv")]].round(3))

# Structure par opérateur des points mobile money, par commune (vues non additives, DD2)
op = pd.read_csv(EDA / "s2_offre_par_commune.csv")
for c in ("mm_deux_operateurs", "mm_togocom_seul", "mm_moov_seul", "mm_operateur_non_renseigne"):
    op[f"part_{c[3:]}_pct"] = 100 * op[c] / op.n_mm
garder("s2_operateurs_communes", op[["code", "nom", "prefecture", "unite_regionale", "n_mm"] +
                                    [c for c in op if c.startswith("part_")]].round(1))

# =============================================================== 5. Distance des points mobile money au guichet le plus proche
pts = gpd.GeoDataFrame(pts, geometry=gpd.points_from_xy(pts.lon, pts.lat), crs="EPSG:4326").to_crs(CRS_SURFACE)
xy = np.c_[pts.geometry.x, pts.geometry.y]
formels = pts.compte_formel == 1
mm = (pts["type"] == "mobile_money").values
arbre_f, arbre_d = cKDTree(xy[formels.values]), cKDTree(xy[(pts["type"] == "dab").values])
d_f, i_f = arbre_f.query(xy[mm])
d_d, _ = arbre_d.query(xy[mm])
dist = pts.loc[mm, ["commune_code", "unite_regionale_code"]].assign(
    km_guichet=d_f / 1e3, km_dab=d_d / 1e3,
    commune_guichet=pts.loc[formels, "commune_code"].values[i_f])


def resume_dist(g):
    out = {"points_mm": len(g), "mediane_km_guichet": g.km_guichet.median(), "mediane_km_dab": g.km_dab.median()}
    for s in SEUILS_KM:
        out[f"part_plus_{s}km_guichet_pct"] = 100 * (g.km_guichet > s).mean()
        out[f"part_plus_{s}km_dab_pct"] = 100 * (g.km_dab > s).mean()
    return pd.Series(out)


du = dist.groupby("unite_regionale_code").apply(resume_dist)
du.loc["national"] = resume_dist(dist)
du.insert(0, "nom", [noms_ur.get(k, "National") for k in du.index])
garder("s5_distances_unites", du.reset_index(names="code").round(1))
dc = dist.groupby("commune_code").apply(resume_dist).join(com.set_index("code")[["nom", "prefecture", "unite_regionale",
                                                                                   "n_formels", "pop_totale"]])
garder("s5_distances_communes", dc.reset_index(names="code").round(2))
# Communes sans guichet : où est le guichet le plus proche de leurs points mobile money ?
zero = com[com.n_formels == 0].code
dz = dist[dist.commune_code.isin(zero)]
proche = dz.groupby("commune_code").agg(mediane_km_guichet=("km_guichet", "median"), max_km_guichet=("km_guichet", "max"),
                                        commune_guichet=("commune_guichet", lambda x: x.mode().iloc[0]))
proche["commune_du_guichet_le_plus_proche"] = proche.pop("commune_guichet").map(com.set_index("code").nom)
proche = proche.join(com.set_index("code")[["nom", "prefecture", "unite_regionale", "pop_totale", "n_mm"]])
garder("s5_communes_sans_guichet_distance", proche.reset_index(names="code").sort_values("mediane_km_guichet", ascending=False).round(1))

# =============================================================== 6. Couverture 3i (proxy de niveau C)
cv = com[com.couv_20km_motif != "non_determinable"]
lignes = []
for v in ("densite", "mm_pour_10k_adultes", "formels_pour_10k_hab"):
    x = cv.pop_totale / cv.superficie_km2 if v == "densite" else cv[v]
    r, p = spearmanr(x, cv.couv_20km_pct)
    lignes.append(dict(maille="commune", relation=f"couverture 3i et {v}", n=len(cv), rho=r, p=p))
garder("s6_couverture_correlations", pd.DataFrame(lignes).round(3))
cu = com.assign(nd=com.couv_20km_motif == "non_determinable").groupby("unite_regionale").apply(lambda g: pd.Series({
    "communes": len(g), "non_determinables": int(g.nd.sum()),
    "couverture_ponderee_pop_pct": np.average(g.couv_20km_pct[~g.nd], weights=g.pop_totale[~g.nd]),
    "communes_sous_50pct": int((g.couv_20km_pct < 50).sum())}))
garder("s6_couverture_unites", cu.reset_index().round(1))

# Usage : accès déclaré à Internet par région (EHCVM, 15 ans et plus, deux vagues de même définition et mêmes grappes, R5).
# Afrobaromètre (petits effectifs par région) et MICS6 (15-49 ans, par sexe, 2017, 7 domaines) ne sont pas cartographiés.
eq = pd.read_csv(PROCESSED / "enquetes_region.csv")
us = eq[(eq.source.str.startswith("EHCVM")) & (eq.indicateur == "acces_internet_declare") & (eq.domaine_type == "region")
        & (eq.population_reference == "individus de 15 ans et plus")]
us = us.pivot_table(index="unite_regionale_code", columns="vague", values=["estimation_pct", "ic95_bas", "ic95_haut", "cv_pct"])
us.columns = [f"{v}_{w.replace('/', '_')}" for v, w in us.columns]
us["variation_points"] = us["estimation_pct_2021_22"] - us["estimation_pct_2018_19"]
us = us.join(cu.set_index(cu.index.map({v: k for k, v in noms_ur.items()}))[["couverture_ponderee_pop_pct", "non_determinables"]])
us.insert(0, "nom", us.index.map(noms_ur))
garder("s6_usage_internet_regions", us.reset_index(names="code").round(2))

# Fibre (3i, niveau C) : longueur par commune, enterrée et aérienne, sans date ni distinction transport / accès ;
# jamais additionnée aux abonnements FTTH (règle de O2-07)
fibre = {}
for couche in ("fibre-enterree", "fibre-aerienne"):
    d = json.load(open(RACINE / "data" / "raw" / f"D3_geodata-longueur-{couche}_COMMUNE.json", encoding="utf-8"))
    fibre[f"km_{couche.replace('-', '_')}"] = pd.Series({r["commune_id"]: float(r["valeur"]) / 1e3 for r in d})
fb = com.set_index("code")[["nom", "prefecture", "unite_regionale", "superficie_km2", "pop_totale"]].join(pd.DataFrame(fibre))
assert fb[list(fibre)].notna().all().all()
fb["aucune_fibre_recensee"] = (fb.km_fibre_enterree == 0) & (fb.km_fibre_aerienne == 0)
garder("s6_fibre_communes", fb.reset_index(names="code").round(2))

# Capacités et usage déclarés par région (EHCVM, 15 ans et plus) : alphabétisation (deux vagues), mobile banking (2021/22)
cap = []
for ind in ("alphabetisation", "usage_mobile_banking"):
    e = eq[(eq.source.str.startswith("EHCVM")) & (eq.indicateur == ind)]
    nat = e[e.domaine_type == "national"].set_index("vague")
    for _, r in e[e.domaine_type == "region"].iterrows():
        n = nat.loc[r.vague]
        cap.append(dict(indicateur=ind, vague=r.vague, code=r.unite_regionale_code, nom=noms_ur[r.unite_regionale_code],
                        estimation_pct=r.estimation_pct, ic95_bas=r.ic95_bas, ic95_haut=r.ic95_haut, cv_pct=r.cv_pct,
                        national_pct=n.estimation_pct,
                        ecart_national=("au-dessus" if r.ic95_bas > n.ic95_haut else "au-dessous" if r.ic95_haut < n.ic95_bas
                                        else "non distinct")))
cap = pd.DataFrame(cap)
alpha_var = cap[cap.indicateur == "alphabetisation"].pivot_table(index="code", columns="vague", values="estimation_pct")
cap["variation_points"] = [alpha_var.loc[k, "2021/22"] - alpha_var.loc[k, "2018/19"] if i == "alphabetisation" and v == "2021/22" else np.nan
                           for i, v, k in zip(cap.indicateur, cap.vague, cap.code)]
garder("s9_capacites_usage_regions", cap.round(2))

# =============================================================== 7. Structure spatiale : voisinage (P3), Moran, LISA
geo = gpd.read_file(GEO / "communes.geojson")[["code", "geometry"]].merge(com[["code", "nom"]], on="code")
paires = gpd.sjoin(geo, geo, predicate="touches")
paires = paires[paires.code_left != paires.code_right][["code_left", "code_right"]]
voisins = paires.groupby("code_left").code_right.apply(list).to_dict()
assert set(voisins) == set(com.code), "une commune sans voisine : le voisinage par contiguïté ne s'applique pas"
assert len(paires) // 2 == 275


def moran(codes, valeurs):
    """Indice de Moran global et LISA, poids par contiguïté normalisés par ligne, sur le sous-ensemble fourni."""
    idx = {k: i for i, k in enumerate(codes)}
    n = len(codes)
    W = np.zeros((n, n))
    for k in codes:
        vs = [idx[v] for v in voisins[k] if v in idx]
        if vs:
            W[idx[k], vs] = 1 / len(vs)
    z = (valeurs - valeurs.mean()) / valeurs.std()
    lag = W @ z
    I = z @ lag / (z @ z)
    perm = np.array([(zp := rng.permutation(z)) @ (W @ zp) / (zp @ zp) for _ in range(PERMUTATIONS)])
    e = -1 / (n - 1)
    p_glob = ((perm >= I).sum() + 1) / (PERMUTATIONS + 1) if I > e else ((perm <= I).sum() + 1) / (PERMUTATIONS + 1)
    Ii = z * lag
    p_loc = np.ones(n)
    for i in range(n):
        k = int((W[i] > 0).sum())
        if k == 0:
            continue
        autres = np.delete(z, i)
        tirages = np.array([rng.choice(autres, k, replace=False).mean() for _ in range(PERMUTATIONS)])
        Ip = z[i] * tirages
        p_loc[i] = (((Ip >= Ii[i]).sum() if Ii[i] >= 0 else (Ip <= Ii[i]).sum()) + 1) / (PERMUTATIONS + 1)
    cat = np.where(p_loc > ALPHA, "non significatif",
                   np.select([(z > 0) & (lag > 0), (z < 0) & (lag < 0), (z > 0) & (lag < 0), (z < 0) & (lag > 0)],
                             ["élevé entouré d'élevés", "faible entouré de faibles", "élevé entouré de faibles",
                              "faible entouré d'élevés"], "non significatif"))
    return dict(n=n, I=I, esperance=e, p=p_glob), pd.DataFrame({"code": codes, "Ii": Ii, "p": p_loc, "grappe": cat})


VARIABLES = {"formels_pour_10k_hab": "points formels pour 10 000 habitants",
             "mm_pour_10k_adultes": "points mobile money pour 10 000 adultes",
             "couv_20km_pct": "couverture 3i (%)"}
glob, loc = [], []
for v, lab in VARIABLES.items():
    d = com if v != "couv_20km_pct" else cv
    g, l = moran(list(d.code), d[v].to_numpy(float))
    glob.append(dict(variable=lab, **g))
    loc.append(l.assign(variable=v))
garder("s7_moran_global", pd.DataFrame(glob).round(4))
lisa = pd.concat(loc).merge(com[["code", "nom", "prefecture", "unite_regionale", "strate_50"]], on="code")
garder("s7_lisa_communes", lisa.round(4))

# Communes sans guichet : leurs voisines en ont-elles ?
vz = pd.DataFrame([{"code": k, "voisines": len(voisins[k]),
                    "voisines_avec_guichet": sum(com.set_index("code").n_formels[v] > 0 for v in voisins[k]),
                    "voisines_sans_guichet": ", ".join(sorted(com.set_index("code").nom[v] for v in voisins[k]
                                                             if com.set_index("code").n_formels[v] == 0))}
                   for k in zero]).merge(com[["code", "nom", "prefecture", "unite_regionale", "pop_totale"]], on="code")
garder("s7_communes_sans_guichet_voisinage", vz.sort_values(["voisines_avec_guichet", "pop_totale"], ascending=[True, False]))

# Pôles urbains (H4) : part du mobile money de la préfecture concentrée dans la commune chef-lieu
poles = []
for pole in ("Tchaoudjo 1", "Kozah 1", "Cinkassé 1"):
    r = com[com.nom == pole].iloc[0]
    sub = com[com.prefecture_code == r.prefecture_code]
    poles.append(dict(pole=pole, prefecture=r.prefecture, communes_de_la_prefecture=len(sub),
                      part_population_pct=100 * r.pop_totale / sub.pop_totale.sum(),
                      part_points_mm_pct=100 * r.n_mm / sub.n_mm.sum(),
                      part_points_formels_pct=100 * r.n_formels / sub.n_formels.sum(),
                      mm_pour_10k_adultes_pole=r.mm_pour_10k_adultes,
                      mm_pour_10k_adultes_reste=1e4 * sub.n_mm.drop(r.name).sum() / sub.pop15_prorata.drop(r.name).sum()))
garder("s7_poles_urbains", pd.DataFrame(poles).round(1))

for nom, df in R.items():
    df.to_csv(SORTIE / f"{nom}.csv", index=False, encoding="utf-8")
print(f"{len(R)} tables écrites dans {SORTIE.relative_to(RACINE)}")
