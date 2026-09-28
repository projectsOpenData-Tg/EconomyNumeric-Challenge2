"""Page 5 — Carte : « Que voit-on, commune par commune ? » (plan visuel, section 7, page 5).

Explorateur : un indicateur, une maille (commune, préfecture). L'indicateur choisi fixe sa propre limite, affichée
sous la carte."""
import streamlit as st

from composants import ariane, carte_valeur, entete, export_csv, limite, pied
from donnees import contours, lire, prefectures
from i18n import bi, t
from theme import PRIORITE, STATUT_O4_05

ariane(t("page.carte"))
entete(t("page.carte"), bi("Que voit-on, commune par commune ?", "What do we see, commune by commune?"),
       bi("Choisissez un indicateur et une maille : la carte, l'infobulle et la limite changent avec lui.",
          "Choose an indicator and a scale: the map, the tooltip and the limit change with it."))

INDICATEURS = {
    "hab_par_point_formel": dict(lib=bi("Habitants par point formel", "People per formal point"), palette="Blues", table="o4",
                                 limite=bi("Recensement 2021/2022 ; population résidente, pas fréquentation.", "2021/2022 survey; resident population, not footfall.")),
    "hab_par_point_mm": dict(lib=bi("Habitants par point mobile money", "People per mobile money point"), palette="Oranges", table="o4",
                             limite=bi("Des points de service, pas des agents.", "Service points, not agents.")),
    "couverture_proxy_pct": dict(lib=t("lib.couverture_theorique").capitalize() + " (%)", palette="Blues", table="couverture",
                                 limite=bi("Proxy : rayon de 20 km autour des antennes, toutes technologies confondues.",
                                          "Proxy: 20 km radius around antennas, all technologies combined.")),
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
    "statut_O4_05": dict(lib=bi("Statut d'accès financier", "Financial access status"), table="o4", categorique=True, couleurs=STATUT_O4_05,
                        limite=bi("Règle en cascade : la première condition remplie l’emporte. Une variante, où la desserte diversifiée "
                                  f"l’emporte sur le mobile money dominant, est sur la page « {t('page.population')} ».",
                                  "Cascading rule: the first condition met prevails. A variant, where diversified service takes precedence "
                                  f"over mobile money dominant, is on the “{t('page.population')}” page.")),
    "priorite": dict(lib=bi("Classe de priorité", "Priority class"), table="priorite", categorique=True,
                     couleurs={"haute": PRIORITE["haute"], "moyenne": PRIORITE["moyenne"], "faible": PRIORITE["faible"],
                              "non classée": PRIORITE["non classée"]},
                     limite=bi("Un rang est relatif : voir la page Priorités pour les seuils et la robustesse.",
                              "A rank is relative: see the Priorities page for thresholds and robustness.")),
}

col1, col2 = st.columns([2, 1])
cle = col1.selectbox(bi("Indicateur", "Indicator"), list(INDICATEURS.keys()), format_func=lambda k: INDICATEURS[k]["lib"], key="carte_indicateur")
info = INDICATEURS[cle]
mailles_dispo = ["Préfecture"] if info["table"] == "priorite" else ["Commune", "Préfecture"]
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
else:  # o4 : hab_par_point_formel, hab_par_point_mm, statut_O4_05
    territoires = lire("07_indicateurs", "o4_communes" if maille == "Commune" else "o4_prefectures")

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
