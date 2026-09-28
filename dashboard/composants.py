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
import plotly.graph_objects as go
import streamlit as st

from donnees import centres, contours, nombre
from i18n import bi, definir_langue, langue, region, t
from theme import BLEUS, COULEUR_REGION, ENCRE, HORS_SELECTION, OCRE, PRIORITE

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
    # Le contexte est encadré dans la couleur de l'étiquette du coin supérieur droit ; vert clair par défaut
    teinte = ton if etiquette and ton in ("alerte", "ok", "critique") else "defaut"
    ctx = f'<div class="kpi-contexte {teinte}">{insecable(contexte)}</div>' if contexte else ""
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
    fig.update_geos(visible=False, bgcolor="#ffffff", projection_type="mercator",
                    lonaxis_range=[min(xs) - 0.05, max(xs) + 0.05], lataxis_range=[min(ys) - 0.05, max(ys) + 0.05])
    fig.update_layout(height=hauteur, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="#ffffff",
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
    fig.update_geos(visible=False, bgcolor="#ffffff", projection_type="mercator",
                    lonaxis_range=[min(xs) - 0.05, max(xs) + 0.05], lataxis_range=[min(ys) - 0.05, max(ys) + 0.05])
    fig.update_layout(height=hauteur, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="#ffffff",
                      font=dict(family="IBM Plex Sans, system-ui, sans-serif", color="#141413"),
                      hoverlabel=dict(bgcolor="#ffffff", font_size=12),
                      coloraxis_colorbar=dict(title=""), legend=dict(title=""))
    st.plotly_chart(fig, key=cle, config={"displayModeBar": False, "scrollZoom": False})


def onglets(cle: str, libelles: list[str]) -> list:
    """Sous-onglets d’une page, en pastilles (demande du 27/09/2026). Seul l’onglet ouvert s’exécute : chaque onglet
    se lit avec `if onglet.open is not False:`. L’onglet actif est gardé par son rang, pas par son libellé, pour qu’il
    survive au changement de langue (les libellés changent, le rang non) et au passage par une autre page. Le repère
    « vue 2 sur 6 » est écrit en tête de l’onglet ouvert, avant son contenu."""
    cle_rang, cle_widget = f"{cle}_rang", f"{cle}_{langue()}"
    rang = min(st.session_state.get(cle_rang, 0), len(libelles) - 1)

    def _retenir():
        st.session_state[cle_rang] = libelles.index(st.session_state[cle_widget])

    st.markdown(f'<div class="onglets-aide">{html.escape(t("onglets.aide", n=len(libelles)))}</div>', unsafe_allow_html=True)
    liste = st.tabs(libelles, default=libelles[rang], key=cle_widget, on_change=_retenir)
    with liste[rang]:
        st.markdown(f'<div class="onglets-repere">{html.escape(t("onglets.repere", vue=libelles[rang], i=rang + 1, n=len(libelles)))}</div>',
                    unsafe_allow_html=True)
    return liste


def carte_regions(df: pd.DataFrame, cle: str, colonne: str, bornes: list[float], classes: list[str],
                  selection: list[str] | None = None, hauteur: int = 520):
    """Carte des 6 unités régionales en classes fixées à l’avance (celles des cartes régionales du 06), la valeur
    écrite sur chaque région. `df` porte `code`, `nom`, la colonne à classer, `etiquette` (texte écrit sur la carte) et
    `survol`. Le Grand Lomé, trop petit pour porter son texte, l’a sous la côte, relié par un trait. Les régions du filtre
    sont cerclées de noir : leur couleur garde sa valeur. La légende montre toujours les 5 classes, même vides, pour que
    deux cartes côte à côte se comparent."""
    geo = contours("unites_regionales")
    pts = centres("unites_regionales")
    rang_classe = pd.cut(df[colonne], [-float("inf")] + list(bornes) + [float("inf")], right=False, labels=False)
    fig = go.Figure()
    for i, lib in enumerate(classes):
        sub = df[rang_classe == i]
        fig.add_choropleth(geojson=geo, featureidkey="properties.code", locations=list(sub.code), z=[i] * len(sub),
                           colorscale=[[0, BLEUS[i]], [1, BLEUS[i]]], showscale=False, showlegend=False,
                           marker_line_color="#ffffff", marker_line_width=1, hovertext=list(sub.survol), hoverinfo="text")
        # Légende : un carré par classe, même quand aucune région n’y tombe (un tracé de carte vide n’y apparaîtrait pas)
        fig.add_scattergeo(lon=[None], lat=[None], mode="markers", name=lib, hoverinfo="skip",
                           marker=dict(symbol="square", size=13, color=BLEUS[i], line=dict(color="#b9b6ad", width=0.5)))
    if selection:
        sel = df[df.nom.isin(selection)]
        fig.add_choropleth(geojson=geo, featureidkey="properties.code", locations=list(sel.code), z=[0] * len(sel),
                           colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]], showscale=False, showlegend=False,
                           marker_line_color=ENCRE, marker_line_width=2.5, hoverinfo="skip")
    # Étiquettes : au centre de chaque région, en blanc sur les deux classes les plus foncées ; le Grand Lomé sous la
    # côte, avec un trait de rappel, pour ne pas chevaucher l’étiquette du Maritime
    lon_gl, lat_gl = pts["GL"]
    ancre_gl = (lon_gl + 0.2, lat_gl - 0.3)
    autres = df[df.code != "GL"]
    couleur_texte = ["#ffffff" if c >= 3 else ENCRE for c in rang_classe[df.code != "GL"]]
    decalage = {"A_HGL": 0.12}  # le Maritime, voisin du Grand Lomé : son étiquette remonte un peu, loin de la côte
    fig.add_scattergeo(lon=[pts[c][0] for c in autres.code], lat=[pts[c][1] + decalage.get(c, 0) for c in autres.code], text=list(autres.etiquette),
                       mode="text", textfont=dict(size=11, color=couleur_texte), hoverinfo="skip", showlegend=False)
    gl = df[df.code == "GL"]
    if len(gl):
        fig.add_scattergeo(lon=[lon_gl, ancre_gl[0]], lat=[lat_gl, ancre_gl[1]], mode="lines", line=dict(color="#8a8780", width=1),
                           hoverinfo="skip", showlegend=False)
        fig.add_scattergeo(lon=[ancre_gl[0]], lat=[ancre_gl[1]], text=list(gl.etiquette), mode="text", textposition="bottom right",
                           textfont=dict(size=11, color=ENCRE), hoverinfo="skip", showlegend=False)
    xs, ys = [], []
    for ft in geo["features"]:
        x0, y0, x1, y1 = ft["bbox"]
        xs += [x0, x1]
        ys += [y0, y1]
    fig.update_geos(visible=False, bgcolor="#ffffff", projection_type="mercator",
                    lonaxis_range=[min(xs) - 0.05, max(xs) + 0.75], lataxis_range=[min(ys) - 0.7, max(ys) + 0.05])
    fig.update_layout(height=hauteur, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="#ffffff",
                      font=dict(family="IBM Plex Sans, system-ui, sans-serif", color=ENCRE),
                      hoverlabel=dict(bgcolor="#ffffff", font_size=12),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.01, yanchor="top", font=dict(size=11),
                                  itemclick=False, itemdoubleclick=False))
    st.plotly_chart(fig, key=cle, config={"displayModeBar": False, "scrollZoom": False})


# ----------------------------------------------------------------- Graphiques des pages d’analyse (Internet, Marché)
BLEU_FONCE = "#0d366b"  # texte du pied de page (theme.py, .pied-identite-titre) : textes mis en avant sur les graphiques


def titre_bloc(titre: str, sous_titre: str | None = None, marge: bool = False):
    style = ' style="margin-top:1rem;"' if marge else ""
    sous = f'<div class="bloc-sous-titre">{html.escape(sous_titre)}</div>' if sous_titre else ""
    st.markdown(f'<div class="bloc-titre"{style}>{html.escape(titre)}</div>{sous}', unsafe_allow_html=True)


def habiller(fig: go.Figure, hauteur: int, suffixe_y: str = "", legende_y: float = 1.12, **kw) -> go.Figure:
    """Mise en forme commune des graphiques des pages d’analyse ; `kw` complète ou remplace les réglages par défaut (axes compris)."""
    reglages = dict(height=hauteur, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
                    font=dict(family="IBM Plex Sans, system-ui, sans-serif", color=ENCRE, size=11),
                    legend=dict(orientation="h", y=legende_y, x=0), yaxis=dict(ticksuffix=suffixe_y, gridcolor="#efece4"),
                    xaxis=dict(gridcolor="#efece4"), hoverlabel=dict(bgcolor="#ffffff", font_size=12),
                    separators=", " if langue() == "fr" else ".,")
    reglages.update(kw)
    fig.update_layout(**reglages)
    return fig


def tracer(fig: go.Figure, cle: str):
    st.plotly_chart(fig, key=cle, config={"displayModeBar": False})


def note(texte: str, forte: bool = False):
    """Phrase de lecture sous un graphique, en bleu foncé ; en gras si `forte` (demande du 28/09/2026)."""
    st.markdown(f'<div class="note-graphique{" forte" if forte else ""}">{html.escape(texte)}</div>', unsafe_allow_html=True)


def pct(x, d=1) -> str:
    """Pourcentage selon la langue : « 39,5 % » en français, « 39.5% » en anglais."""
    return f"{nombre(x, d)}\u00a0%" if langue() == "fr" else f"{nombre(x, d)}%"


def couleur_region(nom: str) -> str:
    """Couleur d’une région (nom de la table ou nom traduit), pour écrire son nom en couleur ; encre si inconnue."""
    return COULEUR_REGION.get(nom) or {region(k): v for k, v in COULEUR_REGION.items()}.get(nom, ENCRE)


def colorer_regions(df: pd.DataFrame, colonne: str):
    """Tableau dont la colonne des régions est écrite en couleur, une couleur par région (demande du 28/09/2026). Rend un
    `Styler` à passer à `st.dataframe`. Un `Styler` impose son propre format d’affichage (6 décimales par défaut) : chaque
    colonne décimale garde donc le nombre de décimales dont ses valeurs ont besoin (au plus 2), au format de la langue."""
    sty = df.style.map(lambda v: f"color: {couleur_region(v)}; font-weight: 600", subset=[colonne])
    for c in df.columns:
        if pd.api.types.is_float_dtype(df[c]):
            v = df[c].dropna()
            d = next((k for k in (0, 1) if ((v * 10 ** k).round(6) % 1 == 0).all()), 2)
            sty = sty.format(lambda x, d=d: "" if pd.isna(x) else nombre(x, d), subset=[c])
    return sty
