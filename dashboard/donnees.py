"""Lecture des résultats du projet pour le tableau de bord.

Le tableau de bord lit les tables de data/analysis/ ; il ne recalcule aucun indicateur. Les seules opérations faites
ici sont des lectures, des jointures et des filtres, pour que chaque chiffre affiché remonte à une table du projet.
"""
from pathlib import Path

import geopandas as gpd
import pandas as pd
import streamlit as st
from shapely.geometry import MultiPolygon
from shapely.geometry.polygon import orient

RACINE = Path(__file__).resolve().parents[1]
ANALYSE = RACINE / "data" / "analysis"
GEO = RACINE / "data" / "processed" / "geo"

CLASSES = {"priorité 1": "haute", "priorité 2": "moyenne", "priorité 3": "faible", "non déterminable (couverture)": "non classée"}
ORDRE_CLASSES = ["haute", "moyenne", "faible", "non classée"]
REGIONS = ["Grand Lomé", "Maritime hors Grand Lomé", "Plateaux", "Centrale", "Kara", "Savanes"]
MILIEUX = {"grand_lome": "Grand Lomé", "autres_villes": "Autres villes", "rural": "Rural"}


@st.cache_data(show_spinner=False)
def lire(dossier: str, nom: str) -> pd.DataFrame:
    return pd.read_csv(ANALYSE / dossier / f"{nom}.csv")


@st.cache_data(show_spinner=False)
def contours(niveau: str) -> dict:
    """Contours en longitude et latitude, simplifiés pour l’affichage (pas pour un calcul)."""
    g = gpd.read_file(GEO / f"{niveau}.geojson")[["code", "nom", "geometry"]]
    # Plotly (d3-geo) veut l’anneau extérieur dans le sens horaire ; sinon il remplit le globe entier hors du polygone
    g["geometry"] = [orient(x, sign=-1.0) if x.geom_type == "Polygon" else MultiPolygon([orient(q, sign=-1.0) for q in x.geoms])
                     for x in g.geometry.simplify(0.002, preserve_topology=True)]
    return g.__geo_interface__


@st.cache_data(show_spinner=False)
def operateurs_communes() -> pd.DataFrame:
    """Part des points mobile money de chaque commune servis par les deux opérateurs, par Togocom seul, par Moov seul,
    et sans opérateur renseigné (06_spatial, carte 10 ; O3)."""
    return pd.read_csv(RACINE / "data" / "analysis" / "06_spatial" / "s2_operateurs_communes.csv")


@st.cache_data(show_spinner=False)
def prefectures() -> pd.DataFrame:
    s = lire("08_priorisation", "score_prefectures")
    s["priorite"] = s.classe_retenue.map(CLASSES)
    return s


@st.cache_data(show_spinner=False)
def communes() -> pd.DataFrame:
    c = lire("07_indicateurs", "o4_communes")
    cel = lire("07_indicateurs", "o4_06_cellules")
    c["cellule_critique"] = c.code.map(cel[cel.maille == "commune"].set_index("code").cellule_O4_06).fillna("").str.startswith("critique")
    p = prefectures().set_index("nom")
    c["priorite_prefecture"] = c.prefecture.map(p.priorite)
    c["priorite_absolue"] = c.statut_O4_05 == "mobile money uniquement"
    c["milieu"] = c.strate_50.map(MILIEUX)
    return c


def filtrer_communes(c: pd.DataFrame, f: dict) -> pd.DataFrame:
    if f["regions"]:
        c = c[c.unite_regionale.isin(f["regions"])]
    if f["milieux"]:
        c = c[c.milieu.isin(f["milieux"])]
    if f["priorites"]:
        garde = c.priorite_prefecture.isin([p for p in f["priorites"] if p != "absolue"])
        if "absolue" in f["priorites"]:
            garde |= c.priorite_absolue
        c = c[garde]
    return c


def filtrer_prefectures(p: pd.DataFrame, f: dict) -> pd.DataFrame:
    if f["regions"]:
        p = p[p.unite_regionale.isin(f["regions"])]
    if f["priorites"]:
        classes = [x for x in f["priorites"] if x != "absolue"]
        if "absolue" in f["priorites"]:
            classes += list(communes()[communes().priorite_absolue].prefecture.map(prefectures().set_index("nom").priorite).unique())
        p = p[p.priorite.isin(classes)]
    return p


@st.cache_data(show_spinner=False)
def chiffres_nationaux() -> dict:
    """Chiffres de tête nationaux, lus dans les tables des indicateurs, des recommandations et du diagnostic."""
    u = lire("07_indicateurs", "o1_01_penetration").set_index("annee")
    a_u = int(u.index.max())
    t = lire("07_indicateurs", "o1_04_technologies").set_index("annee")
    a_t = int(t.index.max())
    h = lire("07_indicateurs", "o2_01_parts_hhi")
    data = h[h.segment.str.contains("data", case=False)]
    data = data[data.annee == data.annee.max()].iloc[0]
    tous_hhi = h.hhi.min()
    c1 = lire("07_indicateurs", "o2_05b_cout_1go").set_index("annee")
    bf = lire("07_indicateurs", "o3_04_bceao_findex").set_index("mesure").valeur
    u2 = lire("07_indicateurs", "o1_02_usage").set_index("annee")
    r6 = lire("10_recommandations", "r6_cout_data").iloc[0]
    fac = lire("09_diagnostic", "facteurs_repetition").set_index("colonne")
    dist = fac.loc["part_points_mm_plus_10km_guichet_pct"]
    return dict(
        usage=u.loc[a_u, "pct_population"], usage_annee=a_u, usage_ass=u.loc[a_u, "afrique_subsaharienne_pct"],
        usage_2016=u.loc[2016, "pct_population"], usage_var_recentes=u2.loc[[a_u - 1, a_u], "variation_points"].max(),
        haut_debit=t.loc[a_t, "part_haut_debit_pct"], haut_debit_annee=a_t, haut_debit_statut=t.loc[a_t, "bascule_haut_debit_02"],
        togocom_data=data.part_togocom_pct, marche_annee=int(data.annee), hhi_min=tous_hhi,
        cout_1go=c1.iloc[-1].cout_pct_revenu_mensuel, cout_annee=int(c1.index[-1]), cout_2pct_annee=int(r6.annee_cible_au_rythme_actuel),
        comptes_actifs=bf["Taux d'activité (%)"],
        dist_p1=dist.mediane_priorite_1, dist_autres=dist.mediane_autres_classees,
    )


def fr(x, d=0) -> str:
    """Nombre au format français : espace pour les milliers, virgule décimale."""
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",")


def nombre(x, d=0) -> str:
    """Nombre selon la langue courante (section 3.3, « Deux langues ») : espace/virgule en français, virgule/point en anglais."""
    from i18n import langue
    return f"{x:,.{d}f}" if langue() == "en" else fr(x, d)
