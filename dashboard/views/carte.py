"""Page 5 — Carte : « Que voit-on, commune par commune ? » (plan visuel, section 7, page 5).

Explorateur : un indicateur, une maille (commune, préfecture). L'indicateur choisi fixe sa propre limite, affichée
sous la carte."""
import streamlit as st

import numpy as np

from composants import ariane, carte_valeur, entete, export_csv, limite, pied
from donnees import contours, lire, operateurs_communes, prefectures
from i18n import bi, t, valeur
from theme import CATEGORIELLE, OCRE, PRIORITE, STATUT_O4_05

# Part des agences face à la part de la population : classes et couleurs de la carte 4 du 06 (bornes fixées à l’avance,
# symétriques autour de 1 ; rouge sous 1, gris neutre autour de 1, bleu au-dessus), ajoutées le 28/09/2026 (item 8 de l’objectif 3)
BORNES_Q = [0.5, 0.8, 1.25, 2.0, np.inf]
CLASSES_Q = [(bi("aucune agence", "no branch"), "#b3302f"), (bi("moins de 0,5", "under 0.5"), "#e34948"),
             (bi("0,5 à 0,8", "0.5 to 0.8"), "#f0a09f"), (bi("0,8 à 1,25 : suit la population", "0.8 to 1.25: follows the population"), "#e2dfd6"),
             (bi("1,25 à 2", "1.25 to 2"), "#86b6ef"), (bi("2 et plus", "2 and over"), "#2a78d6")]
# Opérateurs du mobile money (correction C7, plan 11, page 5) : catégorie la plus fréquente, mêmes couleurs que la page Offre financière
CATEGORIES_OP = [(bi("deux opérateurs", "both operators"), CATEGORIELLE[0]), ("Togocom (YAS)", CATEGORIELLE[1]),
                 ("Moov Africa", CATEGORIELLE[2]), (bi("non renseigné", "not reported"), "#b9b6ad")]


ORDRE_O4_03 = ["réseaux comparables", "mobile money prépondérant", "suppléance quasi totale", "mobile money uniquement (0 point formel)"]
LIB_PRIORITE = {"haute": t("priorite.haute"), "moyenne": t("priorite.moyenne"), "faible": t("priorite.faible"),
                "non classée": t("priorite.non_classee")}


def classe_q(v: float) -> int:
    return 0 if v == 0 else 1 + int(np.searchsorted(BORNES_Q, v, side="right"))

ariane(t("page.carte"))
entete(t("page.carte"), bi("Que voit-on, commune par commune ?", "What do we see, commune by commune?"),
       bi("Choisissez un indicateur et une maille : la carte, l'infobulle et la limite changent avec lui.",
          "Choose an indicator and a scale: the map, the tooltip and the limit change with it."))

INDICATEURS = {
    "hab_par_point_formel": dict(lib=bi("Habitants par agence financière", "People per financial branch"), palette="Blues", table="o4",
                                 limite=bi("Recensement 2021/2022 ; population résidente, pas fréquentation.", "2021/2022 survey; resident population, not footfall.")),
    "hab_par_point_mm": dict(lib=bi("Habitants par point mobile money", "People per mobile money point"), palette="Oranges", table="o4",
                             limite=bi("Des points de service, pas des agents.", "Service points, not agents.")),
    "couverture_proxy_pct": dict(lib=t("lib.couverture_theorique").capitalize() + " (%)", palette="Blues", table="couverture",
                                 limite=bi("Estimation : part des habitants à moins de 20 km d’une antenne, toutes technologies confondues ; ce n’est pas une mesure du signal.",
                                          "Estimate: share of residents within 20 km of an antenna, all technologies combined; not a measurement of the signal.")),
    "km_fibre_enterree": dict(lib=bi("Fibre enterrée recensée (km)", "Recorded buried fibre (km)"), palette="Blues", table="fibre",
                              limite=bi("Longueur de câble recensée (carte de 2021/2022), sans date de pose ni distinction entre transport et accès : ni un "
                                        "raccordement à domicile, ni un nombre d’abonnés. 0 = aucune fibre recensée. Fibre enterrée et aérienne ne "
                                        "s’additionnent pas.",
                                        "Recorded cable length (2021/2022 map), no laying date, backbone and access combined: neither a home "
                                        "connection nor a number of subscribers. 0 = no recorded fibre. Buried and aerial fibre are not added "
                                        "together.")),
    "km_fibre_aerienne": dict(lib=bi("Fibre aérienne recensée (km)", "Recorded aerial fibre (km)"), palette="Blues", table="fibre",
                              limite=bi("Longueur de câble recensée (carte de 2021/2022), sans date de pose ni distinction entre transport et accès : ni un "
                                        "raccordement à domicile, ni un nombre d’abonnés. 0 = aucune fibre recensée. Fibre enterrée et aérienne ne "
                                        "s’additionnent pas.",
                                        "Recorded cable length (2021/2022 map), no laying date, backbone and access combined: neither a home "
                                        "connection nor a number of subscribers. 0 = no recorded fibre. Buried and aerial fibre are not added "
                                        "together.")),
    "classe_O4_03": dict(lib=bi("Agents mobile money par agence financière", "Mobile money agents per financial branch"), table="o4",
                         categorique=True, libelles={k: valeur(k) for k in ORDRE_O4_03},
                         couleurs={valeur(k): c for k, c in zip(ORDRE_O4_03, [CATEGORIELLE[0], OCRE, STATUT_O4_05["mobile money dominant"],
                                                                                STATUT_O4_05["mobile money uniquement"]])},
                         limite=bi("Points mobile money par agence de banque, de microfinance ou d’assurance : moins de 5 = réseaux comparables ; "
                                   "5 à 20 = mobile money prépondérant ; plus de 20 = le mobile money supplée presque tout ; aucune agence = "
                                   "mobile money seul. Des lieux, pas des agents : le ratio en agents est plus élevé.",
                                   "Mobile money points per bank, microfinance or insurance branch: under 5 = comparable networks; 5 to 20 = "
                                   "mobile money predominant; over 20 = mobile money almost fully substitutes; no branch = mobile money only. "
                                   "Places, not agents: the ratio in agents is higher.")),
    "mm_pour_10k_adultes": dict(lib=bi("Points mobile money pour 10 000 adultes", "Mobile money points per 10,000 adults"), palette="Oranges",
                                table="o4", limite=bi("Adultes : 15 ans et plus, recensement de 2022. Des lieux, pas des agents.",
                                                      "Adults: aged 15 and over, 2022 census. Places, not agents.")),
    "part_plus_10km_guichet_pct": dict(lib=bi("Points mobile money à plus de 10 km d’une agence (%)", "Mobile money points over 10 km from a branch (%)"),
                                       palette="Oranges", table="distance", mailles=["Commune"],
                                       limite=bi("Distance à vol d’oiseau de chaque point mobile money à l’agence financière la plus proche ; le trajet "
                                                 "réel est plus long. Mesurée par commune seulement.",
                                                 "Distance as the crow flies from each mobile money point to the nearest financial branch; the actual "
                                                 "journey is longer. Measured by commune only.")),
    "statut_O4_05": dict(lib=bi("Statut d'accès financier", "Financial access status"), table="o4", categorique=True,
                        libelles={k: valeur(k) for k in STATUT_O4_05}, couleurs={valeur(k): v for k, v in STATUT_O4_05.items()},
                        limite=bi("Règle en cascade : la première condition remplie l’emporte. Une variante, où la desserte diversifiée "
                                  f"l’emporte sur le mobile money dominant, est sur la page « {t('page.population')} ».",
                                  "Cascading rule: the first condition met prevails. A variant, where diversified service takes precedence "
                                  f"over mobile money dominant, is on the “{t('page.population')}” page.")),
    "quotient_agences": dict(lib=bi("Part des agences face à la part de la population", "Share of branches against share of population"),
                             table="quotient", categorique=True, couleurs=dict(CLASSES_Q),
                             limite=bi("Part des agences financières (banque, microfinance, assurance) du pays divisée par la part de sa "
                                       "population. À 1, les agences suivent la population ; au-dessus, le territoire en a plus que son poids. "
                                       "Bornes fixées à l’avance, symétriques autour de 1. Population résidente, pas fréquentation : les "
                                       "quartiers d’affaires du Grand Lomé et les chefs-lieux en paraissent surdotés.",
                                       "Share of the country’s financial branches (bank, microfinance, insurance) divided by its share of the "
                                       "population. At 1, branches follow the population; above, the territory has more than its weight. Bounds "
                                       "set in advance, symmetric around 1. Resident population, not footfall: Greater Lomé business districts and "
                                       "main towns look over-served.")),
    "operateurs_mm": dict(lib=bi("Opérateurs du mobile money", "Mobile money operators"), table="operateurs", categorique=True,
                          couleurs=dict(CATEGORIES_OP),
                          limite=bi("Catégorie la plus fréquente parmi les points mobile money du territoire : elle ne dit pas qu’un seul "
                                    "opérateur est présent. Opérateur non renseigné pour 11,8 % des points de la région de Kara, jusqu’à la "
                                    "moitié dans certaines communes. Recensement de 2021/2022.",
                                    "Most frequent category among the territory’s mobile money points: it does not mean only one operator is "
                                    "present. Operator not reported for 11.8% of points in the Kara region, up to half in some communes. "
                                    "2021/2022 survey.")),
    "priorite": dict(lib=bi("Classe de priorité", "Priority class"), table="priorite", categorique=True,
                     libelles=LIB_PRIORITE, couleurs={LIB_PRIORITE[k]: PRIORITE[k] for k in LIB_PRIORITE},
                     limite=bi("Un rang est relatif : voir la page Priorités pour les seuils et la robustesse.",
                              "A rank is relative: see the Priorities page for thresholds and robustness.")),
}

col1, col2 = st.columns([2, 1])
cle = col1.selectbox(bi("Indicateur", "Indicator"), list(INDICATEURS.keys()), format_func=lambda k: INDICATEURS[k]["lib"], key="carte_indicateur")
info = INDICATEURS[cle]
mailles_dispo = info.get("mailles") or (["Préfecture"] if info["table"] == "priorite" else ["Commune", "Préfecture"])
maille = col2.segmented_control(bi("Maille", "Scale"), mailles_dispo, default=mailles_dispo[-1], key=f"carte_maille_{cle}")
maille = maille or mailles_dispo[-1]
niveau = "communes" if maille == "Commune" else "prefectures"

if info["table"] == "priorite":
    territoires = prefectures()
elif info["table"] == "fibre":  # carte 11 du 06 ; préfectures : O2-07
    territoires = lire("06_spatial", "s6_fibre_communes") if maille == "Commune" else lire("07_indicateurs", "o2_07_fibre_prefectures")
elif info["table"] == "couverture":
    cv = lire("07_indicateurs", "o2_06_couverture")
    territoires = cv[cv.maille == ("commune" if maille == "Commune" else "préfecture")]
elif info["table"] == "quotient":  # carte 4 du 06
    territoires = lire("06_spatial", "s3_communes" if maille == "Commune" else "s3_prefectures").copy()
    rang_q = territoires.quotient_localisation_formels.map(classe_q)
    territoires[cle] = rang_q.map(lambda i: CLASSES_Q[i][0])
    territoires = territoires.assign(_rang=rang_q).sort_values("_rang")  # légende dans l’ordre des classes
elif info["table"] == "operateurs":  # carte 10 du 06 ; préfectures : effectifs par catégorie du 05
    if maille == "Commune":
        territoires = operateurs_communes().copy()
        cols = ["part_deux_operateurs_pct", "part_togocom_seul_pct", "part_moov_seul_pct", "part_operateur_non_renseigne_pct"]
    else:
        territoires = lire("05_eda", "s2_offre_par_prefecture").copy()
        cols = ["mm_deux_operateurs", "mm_togocom_seul", "mm_moov_seul", "mm_operateur_non_renseigne"]
    territoires[cle] = territoires[cols].idxmax(axis=1).map(lambda c: CATEGORIES_OP[cols.index(c)][0])
    territoires = territoires.assign(_rang=territoires[cols].idxmax(axis=1).map(cols.index)).sort_values("_rang")
elif info["table"] == "distance":  # carte 5 du 06 (droite), commune seulement
    territoires = lire("06_spatial", "s5_distances_communes")
else:  # o4 : hab_par_point_formel, hab_par_point_mm, classe_O4_03, mm_pour_10k_adultes, statut_O4_05
    territoires = lire("07_indicateurs", "o4_communes" if maille == "Commune" else "o4_prefectures")
if info.get("libelles"):  # valeurs de table en clair, dans la langue choisie ; légende dans l’ordre des libellés
    ordre = list(info["libelles"])
    territoires = territoires.assign(_rang=territoires[cle].map(lambda v: ordre.index(v) if v in ordre else len(ordre))).sort_values("_rang")
    territoires[cle] = territoires[cle].map(lambda v: info["libelles"].get(v, v))

geo = contours(niveau)

with st.container(border=True):
    if info.get("categorique"):
        couleurs = {k: v for k, v in info["couleurs"].items() if k in set(territoires[cle])}
        carte_valeur(geo, territoires, f"carte_explorer_{cle}_{maille}", cle, info["lib"], hauteur=620, categorique=True,
                    couleurs_categorie=couleurs)
    else:
        carte_valeur(geo, territoires, f"carte_explorer_{cle}_{maille}", cle, info["lib"], hauteur=620, palette=info.get("palette", "Blues"))
    export_csv(territoires[["code", "nom", "unite_regionale", cle]], f"carte_{cle}.csv", "export_carte_explorer")

limite(info["limite"])
pied()
