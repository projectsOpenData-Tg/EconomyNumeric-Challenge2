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
    "statut_O4_05": dict(lib=bi("Statut d'accès financier", "Financial access status"), table="o4", categorique=True, couleurs=STATUT_O4_05,
                        limite=bi("Règle en cascade ; la variante P9 est sur la page Population et offre.",
                                 "Cascading rule; the P9 variant is on the Population and services page.")),
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
