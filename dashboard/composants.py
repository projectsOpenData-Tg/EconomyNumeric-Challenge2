"""Composants partagés par toutes les pages : barre du haut, en-tête, chiffres clés, bandeaux, synthèse, carte, export.

Gabarit commun (plan visuel, section 5) : barre du haut, en-tête sous forme de question, chiffres clés, visuel avec
son constat, synthèse chiffrée, limite de la page, pied de page avec la mention générale des sources et le cadre
d’identité du projet. Bilingue (section 3.3) : les libellés fixes de ces blocs viennent du dictionnaire central
(`i18n.t`), le texte propre à chaque page est déjà bilingue quand il arrive ici.
"""
import html
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from i18n import bi, definir_langue, langue, t
from theme import HORS_SELECTION, OCRE, PRIORITE

STATIQUE = Path(__file__).resolve().parent / "static"
EMBLEME = STATIQUE / "armoiries-togo-ecu.svg"
LOGO_AI_LAB = STATIQUE / "logo_togo_ai_lab.png"


def topbar():
    """Barre du haut, fixe en haut de chaque page, en trois zones (plan visuel, section 3.3) : armoiries et ministère
    à gauche, nom du projet et sous-titre au centre, sélecteur de langue et logo Togo AI Lab à droite. Reprise du
    tableau de bord du défi 1 (`EconomyNumeric-Challenge-1/dashboard/components/methodology.bande_officielle`)."""
    with st.container(key="topbar"):
        gauche, centre, droite = st.columns([1, 1.3, 1], vertical_alignment="center")
        with gauche:
            emblem_html = (f'<img class="armoiries" src="app/static/{EMBLEME.name}" alt="">' if EMBLEME.exists()
                           else '<span class="armoiries-repli">🛡️</span>')
            st.markdown(f'<div class="topbar-ligne">{emblem_html}<div class="topbar-ministere">{t("topbar.ministry")}</div></div>',
                        unsafe_allow_html=True)
        with centre:
            st.markdown('<div class="topbar-centre">'
                        f'<div class="topbar-titre">🇹🇬 {t("topbar.brand")}</div>'
                        f'<div class="topbar-sous-titre">{t("topbar.subtitle")}</div></div>', unsafe_allow_html=True)
        with droite:
            with st.container(key="topbar_droite"):
                lang = langue()
                c_fr, c_en, c_logo = st.columns([1, 1, 2], vertical_alignment="center")
                if c_fr.button("FR", key="lang_fr", type="primary" if lang == "fr" else "secondary", use_container_width=True):
                    definir_langue("fr")
                    st.rerun()
                if c_en.button("EN", key="lang_en", type="primary" if lang == "en" else "secondary", use_container_width=True):
                    definir_langue("en")
                    st.rerun()
                if LOGO_AI_LAB.exists():
                    logo_html = f'<img src="app/static/{LOGO_AI_LAB.name}" alt="Togo AI Lab">'
                else:
                    logo_html = '<div class="ai-lab-logo-repli">TOGO<br>AI LAB</div>'
                c_logo.markdown(f'<div class="ai-lab-logo-carte">{logo_html}</div>', unsafe_allow_html=True)


def ariane(page: str):
    st.markdown(f'<div class="ariane">{html.escape(t("ariane.racine"))} › <b>{html.escape(page)}</b></div>', unsafe_allow_html=True)


def entete(surtitre: str, question: str, reponse_html: str):
    st.markdown(f'<div class="surtitre">{html.escape(surtitre)}</div><div class="question">{html.escape(question)}</div>'
                f'<div class="reponse">{reponse_html}</div>', unsafe_allow_html=True)


def carte_kpi(libelle: str, valeur: str, phrase: str, contexte: str, reserve: str, etiquette: str | None = None,
              ton: str = "neutre", unite: str = "") -> str:
    """Chiffre clé : la valeur se lit avec sa phrase (« 39,5 % » + « de la population utilise Internet ») ; l’étiquette
    est sur la ligne du titre pour ne pas les séparer ; le contexte donne le seuil ou la comparaison ; la réserve, en bas,
    dit ce que le chiffre ne mesure pas (aucune si elle est vide)."""
    def insecable(txt: str) -> str:  # « 2 % » ne se coupe pas en fin de ligne
        return txt.replace(" %", "&nbsp;%")

    tag = f'<span class="etiquette {ton}">{html.escape(etiquette)}</span>' if etiquette else ""
    u = f'<span class="kpi-unite">{html.escape(unite)}</span>' if unite else ""
    ctx = f'<div class="kpi-contexte">{insecable(contexte)}</div>' if contexte else ""
    res = f'<div class="kpi-reserve">{insecable(html.escape(reserve))}</div>' if reserve else ""
    return (f'<div class="kpi"><div class="kpi-tete"><div class="kpi-libelle">{html.escape(libelle)}</div>{tag}</div>'
            f'<div class="kpi-valeur">{insecable(html.escape(valeur))}{u}</div>'
            f'<div class="kpi-phrase">{insecable(html.escape(phrase))}</div>{ctx}{res}</div>')


def rangee_kpi(groupe: str, cartes: list[str]):
    """Une rangée = une grille : les cartes d’une même rangée ont la même hauteur."""
    st.markdown(f'<div class="groupe">{html.escape(groupe)}</div><div class="kpi-grille">{"".join(cartes)}</div>',
                unsafe_allow_html=True)


def constat(texte_html: str):
    st.markdown(f'<div class="constat"><div class="constat-titre">{html.escape(t("bloc.constat"))}</div>'
                f'<div class="constat-texte">{texte_html}</div></div>', unsafe_allow_html=True)


def synthese(chiffre: str, legende: str, puces_html: list[str]):
    puces = "".join(f"<li>{p}</li>" for p in puces_html)
    st.markdown(f'<div class="synthese"><div><div class="synthese-titre">{html.escape(t("bloc.synthese"))}</div>'
                f'<div class="synthese-chiffre">{chiffre}</div><div class="synthese-legende">{legende}</div></div>'
                f'<ul>{puces}</ul></div>', unsafe_allow_html=True)


def limite(texte: str, titre: str | None = None, discret: bool = False):
    """Bandeau jaune par défaut ; « discret » quand les réserves sont déjà sous chaque chiffre (page Synthèse)."""
    titre = titre if titre is not None else t("bloc.limite")
    classe = "limite discret" if discret else "limite"
    st.markdown(f'<div class="{classe}"><div class="limite-titre">{html.escape(titre)}</div>'
                f'<div class="limite-texte">{html.escape(texte)}</div></div>', unsafe_allow_html=True)


def pied():
    """Pied de page : mention générale des sources, puis le cadre d’identité du projet (section 3.3), identique sur
    chaque page. Le détail des sources va sur la page Méthodologie."""
    st.markdown(f'<div class="pied">{html.escape(t("footer.sources"))}</div>'
                f'<div class="pied-identite"><div class="pied-identite-titre">{html.escape(t("footer.title"))}</div>'
                f'<div class="pied-identite-sous-titre">{html.escape(t("footer.subtitle"))}</div></div>',
                unsafe_allow_html=True)


def export_csv(df: pd.DataFrame, nom_fichier: str, cle: str, libelle: str | None = None):
    st.download_button(libelle or t("export.csv"), df.to_csv(index=False).encode("utf-8"), file_name=nom_fichier,
                       mime="text/csv", key=cle, icon=":material/download:")


def carte_priorites(geo: dict, territoires: pd.DataFrame, cle: str, selection: set, communes_seules: pd.DataFrame | None = None,
                    geo_communes: dict | None = None, hauteur: int = 640):
    """Carte des classes de priorité ; les territoires hors sélection passent en gris ; en ocre, les communes où le
    mobile money est seul (priorité absolue)."""
    libelle_classe = {"haute": t("priorite.haute"), "moyenne": t("priorite.moyenne"), "faible": t("priorite.faible"),
                      "non classée": t("priorite.non_classee")}
    t_ = territoires.copy()
    t_["Classe"] = [libelle_classe.get(p, p) if c in selection else t("priorite.hors_selection") for c, p in zip(t_.code, t_.priorite)]
    couleurs = {t("priorite.haute"): PRIORITE["haute"], t("priorite.moyenne"): PRIORITE["moyenne"],
                t("priorite.faible"): PRIORITE["faible"], t("priorite.non_classee"): PRIORITE["non classée"]}
    couleurs[t("priorite.hors_selection")] = HORS_SELECTION
    # Légende lisible en dix secondes : chaque classe porte son nombre de territoires
    n = t_.Classe.value_counts()
    libelle = {k: f"{k} ({n[k]})" for k in n.index}
    t_["Classe"] = t_.Classe.map(libelle)
    couleurs = {libelle[k]: v for k, v in couleurs.items() if k in libelle}
    ordre = list(couleurs)
    fig = px.choropleth(t_, geojson=geo, locations="code", featureidkey="properties.code", color="Classe",
                        color_discrete_map=couleurs, category_orders={"Classe": ordre}, hover_name="nom",
                        hover_data={"code": False, "Classe": True, "pop_totale": ":,"},
                        labels={"pop_totale": bi("Habitants", "Population")})
    fig.update_traces(marker_line_color="#ffffff", marker_line_width=0.8)
    if communes_seules is not None and len(communes_seules) and geo_communes is not None:
        etiquette = bi("Mobile money seul", "Mobile money only") + f" ({len(communes_seules)} " + bi("communes", "communes") + ")"
        cs = communes_seules.assign(Classe=etiquette)
        f2 = px.choropleth(cs, geojson=geo_communes, locations="code", featureidkey="properties.code", color="Classe",
                           color_discrete_map={etiquette: OCRE}, hover_name="nom",
                           hover_data={"code": False, "Classe": True, "pop_totale": ":,"}, labels={"pop_totale": bi("Habitants", "Population")})
        f2.update_traces(marker_line_color="#141413", marker_line_width=0.7)
        fig.add_traces(f2.data)
    # Fenêtre explicite sur les contours affichés : le zoom automatique de Plotly (fitbounds) laissait le Togo minuscule
    xs, ys = [], []
    for ft in geo["features"]:
        x0, y0, x1, y1 = ft["bbox"]
        xs += [x0, x1]
        ys += [y0, y1]
    fig.update_geos(visible=False, bgcolor="rgba(0,0,0,0)", projection_type="mercator",
                    lonaxis_range=[min(xs) - 0.05, max(xs) + 0.05], lataxis_range=[min(ys) - 0.05, max(ys) + 0.05])
    fig.update_layout(height=hauteur, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="rgba(0,0,0,0)",
                      legend=dict(title="", orientation="v", x=1.0, xanchor="left", y=0.98, font=dict(size=12)),
                      font=dict(family="IBM Plex Sans, system-ui, sans-serif", color="#141413"),
                      hoverlabel=dict(bgcolor="#ffffff", font_size=12))
    st.plotly_chart(fig, key=cle, config={"displayModeBar": False, "scrollZoom": False})


def carte_valeur(geo: dict, territoires: pd.DataFrame, cle: str, colonne: str, titre_legende: str, hauteur: int = 640,
                 palette: str = "Blues", hover_extra: dict | None = None, categorique: bool = False,
                 couleurs_categorie: dict | None = None):
    """Carte d’un seul indicateur continu (ou catégoriel avec `categorique=True`), pour la page Carte et les pages
    d’analyse. Même fenêtre explicite lon/lat que `carte_priorites`, pour éviter le Togo minuscule de Plotly."""
    hover_data = {"code": False, colonne: True}
    if hover_extra:
        hover_data.update(hover_extra)
    kwargs = dict(color_discrete_map=couleurs_categorie) if categorique else dict(color_continuous_scale=palette)
    fig = px.choropleth(territoires, geojson=geo, locations="code", featureidkey="properties.code", color=colonne,
                        hover_name="nom", hover_data=hover_data, labels={colonne: titre_legende}, **kwargs)
    fig.update_traces(marker_line_color="#ffffff", marker_line_width=0.8)
    xs, ys = [], []
    for ft in geo["features"]:
        x0, y0, x1, y1 = ft["bbox"]
        xs += [x0, x1]
        ys += [y0, y1]
    fig.update_geos(visible=False, bgcolor="rgba(0,0,0,0)", projection_type="mercator",
                    lonaxis_range=[min(xs) - 0.05, max(xs) + 0.05], lataxis_range=[min(ys) - 0.05, max(ys) + 0.05])
    fig.update_layout(height=hauteur, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="rgba(0,0,0,0)",
                      font=dict(family="IBM Plex Sans, system-ui, sans-serif", color="#141413"),
                      hoverlabel=dict(bgcolor="#ffffff", font_size=12),
                      coloraxis_colorbar=dict(title=""), legend=dict(title=""))
    st.plotly_chart(fig, key=cle, config={"displayModeBar": False, "scrollZoom": False})
