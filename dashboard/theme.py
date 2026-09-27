"""Thème du tableau de bord : polices, couleurs et styles des composants partagés.

Palette reprise des figures du projet (rampe bleue pour les classes de priorité, ocre pour les communes où le mobile
money est seul, palette de statuts pour les étiquettes). Les couleurs de base sont dans .streamlit/config.toml.
"""
import streamlit as st

ENCRE, ENCRE2, DISCRET, FILET, FOND, CARTE = "#141413", "#3a3935", "#55534e", "#e2dfd6", "#f4f2ec", "#ffffff"
PRIORITE = {"haute": "#0d366b", "moyenne": "#3987e5", "faible": "#cde2fb", "non classée": "#b9b6ad"}
OCRE = "#eda100"
HORS_SELECTION = "#ebe8e0"
BLEUS = ["#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]  # rampe séquentielle validée (analyse/cartes_06.py)
CATEGORIELLE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]  # palette catégorielle validée
DIMENSION = {"acces": "#eb6834", "maillage": "#1baf7a", "couverture": "#4a3aa7"}  # figures_08.py, D1/D2/D3
STATUT_O4_05 = {"desserte diversifiée": "#2a78d6", "desserte faible": "#eda100",
                "mobile money dominant": "#4a3aa7", "mobile money uniquement": "#e34948"}  # figures_07.py

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=IBM+Plex+Sans:wght@400;500;600&display=swap');
html, body, [class*="css"], .stMarkdown, .stText, button, input, label { font-family: 'IBM Plex Sans', system-ui, sans-serif; }
h1, h2, h3 { font-family: 'Fraunces', Georgia, serif !important; font-weight: 600 !important; letter-spacing: 0 !important; }
[data-testid="stMainBlockContainer"] { padding-top: 0.6rem; padding-bottom: 2rem; max-width: 1280px; }
[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] span { font-size: 0.93rem; }
[data-testid="stSidebarHeader"] img { height: 2.6rem !important; max-width: 100% !important; }
[data-testid="stSidebar"] [data-testid="stNavSectionHeader"] { text-transform: uppercase; letter-spacing: 0.08em; font-size: 0.72rem; color: #9fb2c6; }
.marque { display: flex; gap: 12px; align-items: center; padding: 4px 0 12px; }
.marque-titre { font-family: 'Fraunces', Georgia, serif; font-size: 1.12rem; font-weight: 600; color: #ffffff; }
.marque-sous-titre { font-size: 0.78rem; color: #c9d4e0; }
.ariane { font-size: 0.85rem; color: #55534e; margin-bottom: 0.4rem; }
.ariane b { color: #141413; }
.surtitre { font-size: 0.78rem; letter-spacing: 0.08em; text-transform: uppercase; color: #0d366b; font-weight: 600; }
.question { font-family: 'Fraunces', Georgia, serif; font-size: 2.6rem; font-weight: 600; line-height: 1.1; margin: 0.2rem 0 0.5rem; color: #141413; }
.reponse { font-size: 1.05rem; line-height: 1.5; color: #3a3935; max-width: 880px; margin-bottom: 0.6rem; }
.filtres-actifs { font-size: 0.85rem; color: #3a3935; background: #ffffff; border: 1px solid #e2dfd6; border-radius: 10px; padding: 8px 12px; margin-bottom: 0.6rem; }
.groupe { font-size: 0.82rem; font-weight: 600; color: #55534e; margin: 0.6rem 0 0.4rem; }
.kpi-grille { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 12px; margin-bottom: 6px; }
.kpi { background: #ffffff; border: 1px solid #e2dfd6; border-radius: 14px; padding: 16px 18px; display: flex; flex-direction: column; gap: 6px; box-sizing: border-box; }
.kpi-tete { display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; min-height: 2.5rem; }
.kpi-libelle { font-size: 0.82rem; color: #55534e; }
.kpi-valeur { font-family: 'Fraunces', Georgia, serif; font-size: 2.2rem; font-weight: 600; line-height: 1.1; color: #141413; }
.kpi-unite { font-family: 'IBM Plex Sans', system-ui, sans-serif; font-size: 1.05rem; font-weight: 600; margin-left: 6px; }
.kpi-phrase { font-size: 0.95rem; font-weight: 600; line-height: 1.4; color: #141413; }
.kpi-contexte { font-size: 0.84rem; line-height: 1.45; color: #3a3935; }
.kpi-reserve { font-size: 0.78rem; line-height: 1.4; color: #55534e; border-top: 1px solid #efece4; padding-top: 7px; margin-top: auto; }
.etiquette { font-size: 0.74rem; font-weight: 600; padding: 3px 8px; border-radius: 999px; white-space: nowrap; }
.etiquette.alerte { background: #fdf0d2; color: #6b4700; }
.etiquette.ok { background: #e3eefb; color: #0d366b; }
.etiquette.critique { background: #fbe3e2; color: #8a1c1b; }
.etiquette.neutre { background: #efece4; color: #3a3935; }
.etiquette.national { background: #efece4; color: #55534e; font-weight: 500; }
.bloc-titre { font-family: 'Fraunces', Georgia, serif; font-size: 1.3rem; font-weight: 600; color: #141413; margin-bottom: 0.2rem; }
.bloc-sous-titre { font-size: 0.86rem; color: #55534e; line-height: 1.45; margin-bottom: 0.4rem; }
.constat { background: #e8f0fb; border: 1px solid #c7d8f0; border-radius: 14px; padding: 16px 18px; margin-bottom: 14px; }
.constat-titre, .limite-titre, .synthese-titre { font-size: 0.78rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; }
.constat-titre { color: #0d366b; }
.constat-texte { font-size: 0.95rem; line-height: 1.5; color: #141413; margin-top: 4px; }
.ecarts { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 12px; }
.ecarts li { display: flex; gap: 12px; font-size: 0.92rem; line-height: 1.5; }
.ecarts .num { font-family: 'Fraunces', Georgia, serif; font-size: 1.1rem; font-weight: 600; color: #0d366b; width: 16px; flex-shrink: 0; }
.action { padding: 10px 0; border-bottom: 1px solid #efece4; }
.action:last-child { border-bottom: 0; }
.action-titre { font-size: 0.92rem; font-weight: 600; line-height: 1.45; margin-bottom: 6px; }
.action-meta { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; font-size: 0.82rem; color: #55534e; }
.synthese { background: #ffffff; border: 1px solid #e2dfd6; border-radius: 14px; padding: 20px 24px; display: grid; grid-template-columns: 280px 1fr; gap: 26px; align-items: center; margin-top: 8px; }
.synthese-titre { color: #55534e; }
.synthese-chiffre { font-family: 'Fraunces', Georgia, serif; font-size: 2.6rem; font-weight: 600; color: #0d366b; line-height: 1.05; margin: 4px 0; }
.synthese-legende { font-size: 0.88rem; line-height: 1.45; }
.synthese ul { margin: 0; padding-left: 18px; display: flex; flex-direction: column; gap: 8px; font-size: 0.92rem; line-height: 1.5; }
.limite { background: #fdf3d7; border: 1px solid #ecd28f; border-radius: 14px; padding: 14px 18px; margin-top: 14px; }
.limite-titre { color: #6b4700; }
.limite-texte { font-size: 0.9rem; line-height: 1.5; color: #3a2a00; margin-top: 4px; }
.limite.discret { background: transparent; border: 0; border-top: 1px solid #e2dfd6; border-radius: 0; padding: 12px 0 0; margin-top: 18px; }
.limite.discret .limite-titre { color: #55534e; }
.limite.discret .limite-texte { font-size: 0.86rem; color: #55534e; }
.pied { font-size: 0.8rem; color: #55534e; margin-top: 18px; }
.legende { display: flex; flex-direction: column; gap: 10px; font-size: 0.86rem; line-height: 1.4; }
.legende .ligne { display: flex; gap: 10px; align-items: flex-start; }
.legende .pastille { width: 15px; height: 15px; border-radius: 4px; flex-shrink: 0; margin-top: 2px; box-sizing: border-box; }

/* Barre du haut (section 3.3) : armoiries + ministère · nom du projet · langue + logo Togo AI Lab */
.topbar-ligne { display: flex; align-items: center; gap: 10px; }
.armoiries { height: 38px; width: auto; flex-shrink: 0; }
.armoiries-repli { font-size: 1.4rem; flex-shrink: 0; }
.topbar-ministere { font-size: 0.76rem; color: #3a3935; line-height: 1.3; }
.topbar-centre { text-align: center; }
.topbar-titre { font-family: 'Fraunces', Georgia, serif; font-size: 1.2rem; font-weight: 600; color: #0d366b; }
.topbar-sous-titre { font-size: 0.76rem; color: #55534e; font-style: italic; margin-top: 1px; }
.ai-lab-logo-carte { display: inline-flex; align-items: center; justify-content: center; height: 40px; }
.ai-lab-logo-carte img { height: 34px; width: auto; max-width: 140px; object-fit: contain; }
.ai-lab-logo-repli { font-size: 0.55rem; font-weight: 700; color: #0d366b; line-height: 1.2; text-align: center; }
.pied-identite { margin-top: 8px; padding-top: 10px; border-top: 1px solid #e2dfd6; }
.pied-identite-titre { font-size: 0.86rem; font-weight: 700; color: #0d366b; }
.pied-identite-sous-titre { font-size: 0.78rem; color: #55534e; margin-top: 2px; line-height: 1.4; }
[data-testid="stVerticalBlockBorderWrapper"]:has(div.st-key-topbar) { margin-bottom: 0.8rem; }
div.st-key-topbar { padding: 6px 0 12px; border-bottom: 1px solid #e2dfd6; margin-bottom: 0.6rem; }
div.st-key-topbar_droite { display: flex; align-items: center; justify-content: flex-end; gap: 8px; }
div.st-key-topbar_droite button { padding: 0.15rem 0.55rem !important; min-height: 1.6rem !important; }
</style>
"""


def appliquer_theme():
    st.markdown(CSS, unsafe_allow_html=True)
