"""Tableau de bord — accès numérique et inclusion financière au Togo.

Restitue les résultats du projet (documents 05 à 10) selon le plan visuel (document 11) : 11 pages en 4 groupes,
filtres globaux dans la barre latérale, gabarit commun à toutes les pages, barre du haut et pied de page identiques
sur chaque page, bilingue (français, anglais).

Lancement, depuis la racine du projet :  streamlit run dashboard/app.py
"""
import sys
from pathlib import Path

import streamlit as st

ICI = Path(__file__).resolve().parent
if str(ICI) not in sys.path:
    sys.path.insert(0, str(ICI))

from composants import topbar  # noqa: E402
from donnees import REGIONS  # noqa: E402
from i18n import bi, langue, region, t  # noqa: E402
from notify import signaler_visite  # noqa: E402
from theme import appliquer_theme  # noqa: E402

st.set_page_config(page_title=t("topbar.brand").replace("&amp;", "&"), page_icon=":material/insights:", layout="wide",
                   initial_sidebar_state="expanded")
appliquer_theme()

# Alerte de visite Telegram (notify.py) : sans effet tant que les deux variables d'environnement ne sont pas posées sur
# le dyno. Appelée après le thème pour qu'un incident réseau ne retarde jamais le premier rendu : l'envoi part dans un
# thread démon.
signaler_visite()

topbar()

# ----------------------------------------------------------------- Filtres globaux (conservés d’une page à l’autre)
DEFAUTS = {"f_regions": [], "f_maille": "Préfecture", "f_priorites": [], "f_milieux": []}
for k, v in DEFAUTS.items():
    st.session_state.setdefault(k, v)


def reinitialiser():
    for k, v in DEFAUTS.items():
        st.session_state[k] = v


PAGES = {
    t("menu.principal"): [st.Page("views/synthese.py", title=t("page.synthese"), icon=":material/home:", default=True)],
    t("menu.analyses"): [
        st.Page("views/internet.py", title=t("page.internet"), icon=":material/wifi:", url_path="internet"),
        st.Page("views/marche.py", title=t("page.marche"), icon=":material/cell_tower:", url_path="marche"),
        st.Page("views/offre.py", title=t("page.offre"), icon=":material/account_balance:", url_path="offre"),
        st.Page("views/population.py", title=t("page.population"), icon=":material/groups:", url_path="population"),
        st.Page("views/carte.py", title=t("page.carte"), icon=":material/map:", url_path="carte"),
    ],
    t("menu.pilotage"): [
        st.Page("views/priorites.py", title=t("page.priorites"), icon=":material/flag:", url_path="priorites"),
        st.Page("views/diagnostic.py", title=t("page.diagnostic"), icon=":material/troubleshoot:", url_path="diagnostic"),
        PAGE_RECOS := st.Page("views/recommandations.py", title=t("page.recommandations"), icon=":material/task_alt:",
                              url_path="recommandations"),
        PAGE_PROJ := st.Page("views/projections.py", title=t("page.projections"), icon=":material/trending_up:",
                             url_path="projections"),
    ],
    t("menu.methodologie"): [
        st.Page("views/methodologie.py", title=t("page.methodologie"), icon=":material/menu_book:", url_path="methodologie"),
    ],
}

st.logo(str(ICI / "static" / f"logo_{langue()}.svg"), size="large", icon_image=str(ICI / "static" / "icone.svg"))

st.session_state["pages"] = {"recommandations": PAGE_RECOS, "projections": PAGE_PROJ}
navigation = st.navigation(PAGES)

PRIORITES = ["absolue", "haute", "moyenne", "faible", "non classée"]
LIB_PRIORITE = {"absolue": t("priorite.absolue"), "haute": t("priorite.haute"), "moyenne": t("priorite.moyenne"),
                "faible": t("priorite.faible"), "non classée": t("priorite.non_classee")}
MILIEUX = ["Grand Lomé", "Autres villes", "Rural"]
LIB_MILIEU = {m: t(f"milieu.{m}") for m in MILIEUX}
LIB_MAILLE = {"Commune": bi("Commune", "Commune"), "Préfecture": bi("Préfecture", "Prefecture")}

with st.sidebar:
    st.divider()
    st.markdown(f"**{t('sidebar.filters')}**")
    st.pills(t("sidebar.region"), REGIONS, selection_mode="multi", key="f_regions", format_func=region)
    st.segmented_control(t("sidebar.grille"), ["Commune", "Préfecture"], selection_mode="single", key="f_maille",
                         format_func=lambda x: LIB_MAILLE[x])
    st.pills(t("sidebar.priorite"), PRIORITES, selection_mode="multi", key="f_priorites", format_func=lambda x: LIB_PRIORITE[x])
    st.pills(t("sidebar.milieu"), MILIEUX, selection_mode="multi", key="f_milieux", format_func=lambda x: LIB_MILIEU[x])
    st.button(t("sidebar.reinitialiser"), on_click=reinitialiser, use_container_width=True, icon=":material/restart_alt:")
    st.caption(t("sidebar.caption"))

navigation.run()
