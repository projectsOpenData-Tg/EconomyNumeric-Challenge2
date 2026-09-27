"""Page 2 — Internet : usage et marché : « L’usage progresse-t-il, et à quel prix ? » (plan visuel, section 7, page 2).

Six sous-onglets (demande du 27/09/2026, `workspace/conding-progress.md`) : une « Vue synthèse » de l’objectif 1
(retracer l’usage d’Internet, repérer les périodes d’accélération ou de stagnation), quatre onglets qui en détaillent
les analyses (évolution de l’usage, accès et freins par région, le Togo dans l’UEMOA, technologies), et un dernier onglet
pour le marché des télécommunications (objectif 2). Seul l’onglet ouvert s’exécute. La Vue synthèse résume sans
dupliquer : un visuel détaillé dans un autre onglet n’y est qu’annoncé.

Chiffres nationaux, sauf ceux de l’onglet régional, dont les cartes cerclent les régions du filtre.
"""
import html

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from composants import (ariane, carte_kpi, carte_regions, constat, entete, export_csv, limite, onglets, pied, rangee_kpi,
                        synthese)
from donnees import lire, nombre, rang
from i18n import bi, frein, langue, region, t
from theme import CATEGORIELLE, ENCRE, OCRE, PRIORITE

f_regions = st.session_state.f_regions
SEUIL_USAGE = 40        # seuil de l’usage d’Internet (O1-01, hypothèse du sujet)
SEUIL_STAGNATION = 2    # croissance annuelle sous laquelle une année est une stagnation (O1-02)

# ----------------------------------------------------------------- Tables (lectures en cache, aucun recalcul d’indicateur)
d1 = lire("05_eda", "s4_usage_internet_d1").set_index("annee")          # UIT, depuis les premiers utilisateurs (1996)
pen = lire("07_indicateurs", "o1_01_penetration").set_index("annee")    # repère Afrique subsaharienne (depuis 2005)
usage = lire("07_indicateurs", "o1_02_usage").set_index("annee")        # classes de croissance, 2010-2024
enq = lire("05_eda", "s4_usage_internet_enquetes")
periodes = lire("07_indicateurs", "o1_02_enquetes_periodes")
abo = lire("07_indicateurs", "o1_02_abonnements").set_index("annee")
ecart_abo = lire("07_indicateurs", "o1_03_ecart").set_index("annee")
acces = lire("06_spatial", "s6_usage_internet_regions")
alpha = lire("06_spatial", "s9_capacites_usage_regions")
freins = lire("07_indicateurs", "o1_06_freins")
smart = lire("07_indicateurs", "o1_06_smartphone_national").set_index("indicateur").estimation_pct
bench = lire("05_eda", "s4_benchmark_usage_internet")
techno = lire("07_indicateurs", "o1_04_technologies").set_index("annee")
hhi = lire("07_indicateurs", "o2_01_parts_hhi")
inv = lire("07_indicateurs", "o2_04_investissement")
c1go = lire("07_indicateurs", "o2_05b_cout_1go").set_index("annee")
fibre = lire("07_indicateurs", "o2_07_fibre_prefectures")
sites = lire("07_indicateurs", "o2_08_sites_radio")
r6 = lire("10_recommandations", "r6_cout_data").iloc[0]

# ----------------------------------------------------------------- Chiffres partagés entre onglets
a_u = int(usage.index.max())
u_now, u_prev = usage.loc[a_u, "pct_population"], usage.loc[a_u - 1, "pct_population"]
ass_now = pen.loc[a_u, "afrique_subsaharienne_pct"]
multiple_2017 = d1.loc[a_u, "pct_population"] / d1.loc[2017, "pct_population"]
annees_accel = [int(a) for a in usage.index if usage.loc[a, "classe"] == "accélération"]
annees_ralent = [int(a) for a in usage.index if usage.loc[a, "classe"] == "ralentissement"]
annees_stagn = [int(a) for a in usage.index if usage.loc[a, "croissance_pct"] < SEUIL_STAGNATION]
debut_ralent_uit = min(a for a in annees_ralent if a > max(annees_accel))
abo_ralent = [int(a) for a in abo.index if str(abo.loc[a, "classe_finale"]).startswith("ralentissement")]
debut_ralent_abo = min(abo_ralent)
afro = periodes[periodes.source == "Afrobaromètre"].sort_values("debut")
afro_dern = afro.iloc[-1]

acces = acces.set_index("code")
gl_1, sav_1 = acces.loc["GL", "estimation_pct_2018_19"], acces.loc["E", "estimation_pct_2018_19"]
gl_2, sav_2 = acces.loc["GL", "estimation_pct_2021_22"], acces.loc["E", "estimation_pct_2021_22"]
ecart_1, ecart_2 = gl_1 - sav_1, gl_2 - sav_2

tgo = bench[bench.iso3 == "TGO"].set_index("annee")
a_b = int(tgo.index.max())
rang_now = int(tgo.loc[a_b, "rang_uemoa_sur_8"])
rang_debut = int(tgo.rang_uemoa_sur_8.iloc[0])
a_debut_b = int(tgo.index.min())
bas = tgo[tgo.rang_uemoa_sur_8 >= 5]
rang_bas_de, rang_bas_a = int(bas.index.min()), int(bas.index.max())
rangs_bas = bi(" ou ", " or ").join(rang(r) for r in sorted(bas.rang_uemoa_sur_8.unique()))
meme_rang = tgo.rang_uemoa_sur_8 == rang_now
depuis_b = int(tgo.index[~meme_rang].max() + 1) if (~meme_rang).any() else a_debut_b
PAYS = {"BEN": ("Bénin", "Benin"), "BFA": ("Burkina Faso", "Burkina Faso"), "CIV": ("Côte d’Ivoire", "Côte d’Ivoire"),
        "GNB": ("Guinée-Bissau", "Guinea-Bissau"), "MLI": ("Mali", "Mali"), "NER": ("Niger", "Niger"),
        "SEN": ("Sénégal", "Senegal"), "TGO": ("Togo", "Togo")}
pays = lambda iso: bi(*PAYS[iso])
devant = bench[(bench.annee == a_b) & bench.iso3.isin(PAYS) & (bench.valeur > tgo.loc[a_b, "valeur"])].sort_values("valeur", ascending=False)
devant_noms = bi(" et ", " and ").join(pays(i) for i in devant.iso3)

a_t = int(techno.index.max())
a_t0 = int(techno[techno.serie_retenue_pour_la_bascule].index.min())
c1go_now = c1go.iloc[-1]


def titre_bloc(titre: str, sous_titre: str | None = None, marge: bool = False):
    style = ' style="margin-top:1rem;"' if marge else ""
    sous = f'<div class="bloc-sous-titre">{html.escape(sous_titre)}</div>' if sous_titre else ""
    st.markdown(f'<div class="bloc-titre"{style}>{html.escape(titre)}</div>{sous}', unsafe_allow_html=True)


def habiller(fig: go.Figure, hauteur: int, suffixe_y: str = "", legende_y: float = 1.12, **kw) -> go.Figure:
    """Mise en forme commune des graphiques de la page ; `kw` complète ou remplace les réglages par défaut (axes compris)."""
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


def pct(x, d=1) -> str:
    """Pourcentage selon la langue : « 39,5 % » en français, « 39.5% » en anglais."""
    return f"{nombre(x, d)}\u00a0%" if langue() == "fr" else f"{nombre(x, d)}%"


# ----------------------------------------------------------------- En-tête (commun aux onglets)
ariane(t("page.internet"))
entete(t("page.internet"), bi("L’usage progresse-t-il, et à quel prix ?", "Is use growing, and at what cost?"),
       bi(f"L’usage ralentit depuis {debut_ralent_uit} : <strong>{pct(u_now)}</strong> en {a_u}, contre {pct(u_prev)} l’an d’avant. "
          f"1 Go coûte <strong>{pct(c1go_now.cout_pct_revenu_mensuel, 2)}</strong> du revenu mensuel.",
          f"Use has slowed since {debut_ralent_uit}: <strong>{pct(u_now)}</strong> in {a_u}, against {pct(u_prev)} the year before. "
          f"1 GB costs <strong>{pct(c1go_now.cout_pct_revenu_mensuel, 2)}</strong> of monthly income."))
st.markdown(f'<div class="filtres-actifs">{html.escape(bi("Chiffres nationaux : ils ne changent pas avec les filtres de région et de milieu. Dans l’onglet « Accès et freins par région », les régions du filtre sont cerclées de noir.", "National figures: they do not change with the region and area-type filters. In the “Access and barriers by region” tab, the filtered regions are outlined in black."))}</div>',
            unsafe_allow_html=True)

LIBELLES = [bi("Vue synthèse", "Overview"), bi("Évolution de l’usage", "Usage trends"),
            bi("Accès et freins par région", "Access and barriers by region"), bi("Le Togo dans l’UEMOA", "Togo within WAEMU"),
            bi("Technologies", "Technologies"), bi("Marché des télécoms", "Telecom market")]
o_synth, o_evol, o_regions, o_uemoa, o_techno, o_marche = onglets("internet_onglets", LIBELLES)

# =================================================================== 1. Vue synthèse
if o_synth.open is not False:
    with o_synth:
        rangee_kpi(bi("L’usage d’Internet en quatre chiffres", "Internet use in four figures"), [
            carte_kpi(bi(f"Usage d’Internet ({a_u})", f"Internet use ({a_u})"), pct(u_now),
                      bi("de la population utilise Internet", "of the population uses the Internet"),
                      bi(f"Afrique subsaharienne : {pct(ass_now)} ; seuil : {SEUIL_USAGE} %",
                         f"Sub-Saharan Africa: {pct(ass_now)}; threshold: {SEUIL_USAGE}%"),
                      bi("Estimation internationale (UIT) ; les enquêtes auprès des ménages en confirment la tendance, pas le niveau.",
                         "International estimate (ITU); household surveys confirm the trend, not the level."),
                      bi("Seuil franchi", "Threshold reached") if u_now >= SEUIL_USAGE else bi("Sous le seuil", "Below threshold"),
                      "ok" if u_now >= SEUIL_USAGE else "alerte"),
            carte_kpi(bi("Accès déclaré, écart régional", "Self-reported access, regional gap"), nombre(ecart_2, 1),
                      bi(f"d’écart entre le Grand Lomé ({pct(gl_2)}) et les Savanes ({pct(sav_2)})",
                         f"gap between Greater Lomé ({pct(gl_2)}) and Savanes ({pct(sav_2)})"),
                      bi(f"{nombre(ecart_1, 1)} points en 2018/19 : l’écart se creuse", f"{nombre(ecart_1, 1)} points in 2018/19: the gap is widening"),
                      t("lib.acces_declare") + bi(" (enquête EHCVM, 15 ans et plus) : pas la même mesure que l’usage.",
                                                 " (EHCVM survey, aged 15 and over): not the same measure as use."),
                      bi("Écart qui se creuse", "Widening gap"), "critique", unite=bi("points", "points")),
            carte_kpi(bi(f"Rang dans l’UEMOA ({a_b})", f"Rank within WAEMU ({a_b})"), rang(rang_now),
                      bi("sur les 8 pays de l’UEMOA", "out of the 8 WAEMU countries"),
                      bi(f"{rang(rang_debut)} en {a_debut_b}, {rangs_bas} de {rang_bas_de} à {rang_bas_a}",
                         f"{rang(rang_debut)} in {a_debut_b}, {rangs_bas} from {rang_bas_de} to {rang_bas_a}"),
                      bi("Des estimations comparées entre elles, pas des mesures.", "Estimates compared with each other, not measurements."),
                      None, "neutre"),
            carte_kpi(bi(f"Prix de la data ({int(c1go.index[-1])})", f"Data price ({int(c1go.index[-1])})"),
                      pct(c1go_now.cout_pct_revenu_mensuel, 2), bi("du revenu mensuel pour 1 Go", "of monthly income for 1 GB"),
                      bi(f"seuil : 2 % ; au rythme récent, atteint vers {int(r6.annee_cible_au_rythme_actuel)}",
                         f"threshold: 2%; at the recent pace, reached around {int(r6.annee_cible_au_rythme_actuel)}"),
                      bi("Revenu moyen, pas médian.", "Average income, not median."), bi("Non abordable", "Not affordable"), "alerte"),
        ])
        st.write("")
        gauche, droite = st.columns([1.5, 1], gap="large")
        with gauche:
            with st.container(border=True):
                titre_bloc(bi(f"L’usage d’Internet depuis les premiers utilisateurs (1996-{a_u})", f"Internet use since the first users (1996-{a_u})"),
                           bi("Estimation de l’UIT, avec le repère de l’Afrique subsaharienne (publié depuis 2005) et le seuil de 40 %. "
                              "Les points marquent les années d’accélération et de ralentissement.",
                              "ITU estimate, with the Sub-Saharan Africa reference (published since 2005) and the 40% threshold. "
                              "Dots mark the years of acceleration and slowdown."))
                fig = go.Figure()
                fig.add_scatter(x=d1.index, y=d1.pct_population, mode="lines", name="Togo", line=dict(color=PRIORITE["haute"], width=3),
                                hovertemplate="%{x} : %{y:.1f} %<extra>Togo</extra>")
                ass = pen.afrique_subsaharienne_pct.dropna()
                fig.add_scatter(x=ass.index, y=ass.values, mode="lines", name=bi("Afrique subsaharienne", "Sub-Saharan Africa"),
                                line=dict(color="#8a8780", width=2, dash="dot"))
                for annees, coul, nom in ((annees_accel, PRIORITE["moyenne"], bi("année d’accélération", "year of acceleration")),
                                          (annees_ralent, OCRE, bi("année de ralentissement", "year of slowdown"))):
                    fig.add_scatter(x=annees, y=[d1.loc[a, "pct_population"] for a in annees], mode="markers", name=nom,
                                    marker=dict(color=coul, size=11, line=dict(color="#ffffff", width=2)))
                fig.add_hline(y=SEUIL_USAGE, line=dict(color="#8a1c1b", width=1, dash="dash"),
                              annotation_text=bi("Seuil de 40 %", "40% threshold"), annotation_position="top left")
                a0 = int(d1.index.min())
                fig.add_annotation(x=a0, y=d1.loc[a0, "pct_population"], ax=40, ay=-60, showarrow=True, arrowcolor="#8a8780",
                                   text=bi(f"{a0} : premiers utilisateurs ({nombre(d1.loc[a0, 'pct_population'], 2)} %)",
                                           f"{a0}: first users ({nombre(d1.loc[a0, 'pct_population'], 2)}%)"),
                                   font=dict(size=10, color="#55534e"), xanchor="left")
                fig.add_annotation(x=a_u, y=u_now, text=f"<b>{pct(u_now)}</b>", showarrow=False, xanchor="left", xshift=8, font=dict(size=12))
                habiller(fig, 400, " %", xaxis=dict(gridcolor="#efece4", range=[1995, a_u + 3], dtick=5))
                tracer(fig, "courbe_usage_1996")
                export_csv(d1.reset_index().merge(pen[["afrique_subsaharienne_pct"]].reset_index(), on="annee", how="left"),
                           "usage_internet_1996.csv", "export_usage_1996")
        with droite:
            constat(bi(f"L’usage a été multiplié par <strong>{nombre(multiple_2017, 1)}</strong> depuis 2017, mais il ralentit depuis "
                       f"{debut_ralent_uit} : +{nombre(d1.loc[a_u, 'croissance_pct'], 1)} % en {a_u}, contre "
                       f"+{nombre(d1.loc[2020, 'croissance_pct'], 1)} % en 2020.",
                       f"Use has been multiplied by <strong>{nombre(multiple_2017, 1)}</strong> since 2017, but it has slowed since "
                       f"{debut_ralent_uit}: +{nombre(d1.loc[a_u, 'croissance_pct'], 1)}% in {a_u}, against "
                       f"+{nombre(d1.loc[2020, 'croissance_pct'], 1)}% in 2020."))
            with st.container(border=True):
                titre_bloc(bi("Accélération ou stagnation ?", "Acceleration or stagnation?"),
                           bi("Classes de la croissance annuelle, 2010-2024.", "Classes of annual growth, 2010-2024."))
                virg, dp = ", ", bi(" : ", ": ")
                aucune = bi("aucune année", "no year")
                stagn_txt = virg.join(map(str, annees_stagn)) if annees_stagn else aucune
                st.markdown(
                    f'<div class="periodes">'
                    f'<div><b>{html.escape(bi("Accélération", "Acceleration"))}</b>{dp}{virg.join(map(str, annees_accel))}</div>'
                    f'<div><b>{html.escape(bi("Ralentissement", "Slowdown"))}</b>{dp}{virg.join(map(str, annees_ralent))}</div>'
                    f'<div><b>{html.escape(bi("Stagnation", "Stagnation"))}</b>{dp}{html.escape(stagn_txt)} '
                    f'{html.escape(bi(f"(croissance jamais sous {SEUIL_STAGNATION} % par an)", f"(growth never below {SEUIL_STAGNATION}% a year)"))}</div>'
                    f'</div>', unsafe_allow_html=True)
        detail = bi("détail : onglet", "details: tab")
        og, fg = bi("« ", "“"), bi(" »", "”")  # guillemets selon la langue
        synthese(f"× {nombre(multiple_2017, 1)}", bi(f"usage d’Internet de 2017 à {a_u} (UIT)", f"Internet use from 2017 to {a_u} (ITU)"), [
            bi(f"Toutes les sources voient le ralentissement, mais pas au même moment : l’UIT dès {debut_ralent_uit}, les abonnements "
               f"data dès {debut_ralent_abo}, l’enquête Afrobaromètre entre {int(afro_dern.debut)} et {int(afro_dern.fin)} "
               f"(+{nombre(afro_dern.croissance_annualisee_pct, 1)} % par an).",
               f"All sources see the slowdown, but not at the same time: the ITU from {debut_ralent_uit}, data subscriptions from "
               f"{debut_ralent_abo}, the Afrobarometer survey between {int(afro_dern.debut)} and {int(afro_dern.fin)} "
               f"(+{nombre(afro_dern.croissance_annualisee_pct, 1)}% a year).") + f" <i>({detail} {og}{LIBELLES[1]}{fg})</i>",
            bi(f"L’accès déclaré progresse dans toutes les régions, mais l’écart entre le Grand Lomé et les Savanes passe de "
               f"{nombre(ecart_1, 1)} à {nombre(ecart_2, 1)} points.",
               f"Self-reported access is rising in every region, but the gap between Greater Lomé and Savanes grows from "
               f"{nombre(ecart_1, 1)} to {nombre(ecart_2, 1)} points.") + f" <i>({detail} {og}{LIBELLES[2]}{fg})</i>",
            bi(f"{rang(rang_now)} de l’UEMOA depuis {depuis_b}, derrière {devant_noms}.",
               f"{rang(rang_now)} in WAEMU since {depuis_b}, behind {devant_noms}.") + f" <i>({detail} {og}{LIBELLES[3]}{fg})</i>",
            bi(f"La 4G fait {pct(techno.loc[a_t, '4G'])} des abonnements data mobile en {a_t}.",
               f"4G accounts for {pct(techno.loc[a_t, '4G'])} of mobile data subscriptions in {a_t}.") + f" <i>({detail} {og}{LIBELLES[4]}{fg})</i>",
        ])
        limite(bi("Série d’usage estimée par l’UIT (sauf 2017), pas mesurée directement. Les classes de croissance portent sur 2010-2024 : "
                  "avant 2005, les taux portent sur des niveaux inférieurs à 2 % et ne se lisent pas.",
                  "Usage series estimated by the ITU (except 2017), not directly measured. Growth classes cover 2010-2024: before 2005, "
                  "rates apply to levels below 2% and are not interpreted."))

# =================================================================== 2. Évolution de l’usage
if o_evol.open is not False:
    with o_evol:
        constat(bi(f"Toutes les sources voient le ralentissement, mais pas au même moment : l’UIT dès {debut_ralent_uit}, les abonnements "
                   f"data dès {debut_ralent_abo}, l’Afrobaromètre entre {int(afro_dern.debut)} et {int(afro_dern.fin)} "
                   f"(+{nombre(afro_dern.croissance_annualisee_pct, 1)} % par an).",
                   f"All sources see the slowdown, but not at the same time: the ITU from {debut_ralent_uit}, data subscriptions from "
                   f"{debut_ralent_abo}, the Afrobarometer between {int(afro_dern.debut)} and {int(afro_dern.fin)} "
                   f"(+{nombre(afro_dern.croissance_annualisee_pct, 1)}% a year)."))
        couleur_classe = {"accélération": PRIORITE["haute"], "rythme habituel": "#86b6ef", "ralentissement": OCRE}
        lib_classe = {"accélération": bi("accélération", "acceleration"), "rythme habituel": bi("rythme habituel", "usual pace"),
                      "ralentissement": bi("ralentissement", "slowdown"), "rupture": bi("non classé : rupture de série", "not classified: series break")}
        g1, g2 = st.columns(2, gap="large")
        with g1:
            with st.container(border=True):
                titre_bloc(bi("Croissance annuelle de l’usage", "Annual growth of use"),
                           bi("Gain en points de pourcentage chaque année (UIT), classé ; 5 événements annotés.",
                              "Gain in percentage points each year (ITU), classified; 5 events annotated."))
                u10 = usage.loc[2011:]
                fig = go.Figure()
                for cl, coul in couleur_classe.items():
                    sub = u10[u10.classe == cl]
                    fig.add_bar(x=sub.index, y=sub.variation_points, name=lib_classe[cl], marker_color=coul)
                # Événements retenus, lus comme des coïncidences dans le temps, pas comme des causes (limite de l’onglet)
                evenements = [(2016, bi("3G de Moov", "Moov 3G")), (2018, bi("4G à Lomé", "4G in Lomé")),
                              (2020, bi("Covid-19 ; 5G Togocom", "Covid-19; Togocom 5G")), (2022, bi("Câble Equiano", "Equiano cable")),
                              (2023, bi("Forfaits Moov -71 %", "Moov plans -71%"))]
                haut = u10.variation_points.max()
                for an, lib in evenements:  # au-dessus de la plus haute barre, pour ne jamais la chevaucher
                    fig.add_annotation(x=an, y=haut * 1.08, text=lib, showarrow=False, textangle=-90, font=dict(size=9, color="#55534e"),
                                       yanchor="bottom")
                habiller(fig, 360, " pts", legende_y=1.12, bargap=0.3, yaxis=dict(ticksuffix=" pts", gridcolor="#efece4", range=[0, haut * 2.0]),
                         xaxis=dict(gridcolor="#efece4", dtick=2))
                tracer(fig, "croissance_usage")
                export_csv(u10.reset_index()[["annee", "pct_population", "variation_points", "classe"]], "usage_internet.csv", "export_usage")
        with g2:
            with st.container(border=True):
                titre_bloc(bi("L’usage selon les enquêtes auprès des ménages", "Use according to household surveys"),
                           bi("Une série par enquête, avec l’intervalle de confiance à 95 %. Définitions et âges différents : "
                              "les enquêtes ne se comparent pas entre elles.",
                              "One series per survey, with the 95% confidence interval. Different definitions and ages: "
                              "surveys are not compared with each other."))
                series = [("usage_internet_toute_frequence", t("lib.usage_toute_freq") + bi(" (Afrobaromètre, 18 ans et plus)", " (Afrobarometer, 18 and over)"), CATEGORIELLE[0]),
                          ("acces_internet_declare", t("lib.acces_declare") + bi(" (EHCVM, 15 ans et plus)", " (EHCVM, 15 and over)"), CATEGORIELLE[1]),
                          ("usage_internet_3_mois", bi("Usage sur 3 mois (Findex, 15 ans et plus)", "Use in the last 3 months (Findex, 15 and over)"), CATEGORIELLE[2])]
                fig = go.Figure()
                for ind, nom, coul in series:
                    s = enq[enq.indicateur == ind].copy()
                    s["x"] = s.vague.astype(str).str[:4].astype(int)
                    err = dict(type="data", symmetric=False, array=(s.ic95_haut - s.estimation_pct).tolist(),
                               arrayminus=(s.estimation_pct - s.ic95_bas).tolist(), color=coul, thickness=1.5, width=4) if s.ic95_bas.notna().all() else None
                    fig.add_scatter(x=s.x, y=s.estimation_pct, mode="lines+markers" if len(s) > 1 else "markers", name=nom,
                                    line=dict(color=coul, width=2), marker=dict(color=coul, size=9, line=dict(color="#ffffff", width=1.5)),
                                    error_y=err, customdata=s.vague, hovertemplate="%{customdata} : %{y:.1f} %<extra></extra>")
                habiller(fig, 330, " %", legende_y=-0.14, xaxis=dict(gridcolor="#efece4", dtick=2))
                tracer(fig, "enquetes_usage")
                mics = enq[enq.indicateur == "internet_utilise_3_derniers_mois"].set_index("population_reference").estimation_pct
                st.caption(bi(f"Écart entre femmes et hommes (enquête MICS6, 2017, 15-49 ans, usage sur 3 mois) : "
                              f"{pct(mics['Femmes 15-49 ans'])} contre {pct(mics['Hommes 15-49 ans'])}.",
                              f"Gap between women and men (MICS6 survey, 2017, aged 15-49, use in the last 3 months): "
                              f"{pct(mics['Femmes 15-49 ans'])} against {pct(mics['Hommes 15-49 ans'])}."))
                export_csv(enq, "usage_enquetes.csv", "export_enquetes")
        g3, g4 = st.columns(2, gap="large")
        with g3:
            with st.container(border=True):
                titre_bloc(bi("Abonnements data mobile : croissance annuelle", "Mobile data subscriptions: annual growth"),
                           bi("Valeur du 4e trimestre (ARCEP), classée sur 2010-2024. Les années de rupture de série ne sont pas classées.",
                              "Fourth-quarter value (ARCEP), classified over 2010-2024. Series-break years are not classified."))
                ab = abo.copy()
                ab["cl"] = ab.classe_finale.astype(str).str.split(" \\(").str[0].replace({"non classé": "rupture"})
                fig = go.Figure()
                for cl, coul in list(couleur_classe.items()) + [("rupture", "#d9d6cd")]:
                    sub = ab[ab.cl == cl]
                    fig.add_bar(x=sub.index, y=sub.croissance_T4_pct, name=lib_classe[cl], marker_color=coul,
                                marker_pattern_shape="/" if cl == "rupture" else "", marker_line_color="#8a8780" if cl == "rupture" else coul)
                habiller(fig, 330, " %", legende_y=1.16, bargap=0.3, xaxis=dict(gridcolor="#efece4", dtick=2))
                tracer(fig, "croissance_abonnements")
                export_csv(abo.reset_index()[["annee", "abonnes_T4", "croissance_T4_pct", "classe_finale", "rupture"]],
                           "abonnements_data.csv", "export_abonnements")
        with g4:
            with st.container(border=True):
                titre_bloc(bi("Abonnements data par utilisateur d’Internet", "Data subscriptions per Internet user"),
                           bi("Au-dessus de 1, un utilisateur a en moyenne plus d’un abonnement (plusieurs cartes SIM).",
                              "Above 1, a user has on average more than one subscription (several SIM cards)."))
                r = ecart_abo.abonnements_par_utilisateur
                a_max = int(r.idxmax())
                fig = go.Figure()
                fig.add_scatter(x=r.index, y=r.values, mode="lines+markers", name=bi("abonnements par utilisateur", "subscriptions per user"),
                                line=dict(color=PRIORITE["haute"], width=2.5), marker=dict(size=6), showlegend=False,
                                hovertemplate="%{x} : %{y:.2f}<extra></extra>")
                fig.add_hline(y=1, line=dict(color="#8a8780", width=1, dash="dash"),
                              annotation_text=bi("un abonnement par utilisateur", "one subscription per user"), annotation_position="bottom right")
                for a in (a_max, int(r.index.max())):
                    fig.add_annotation(x=a, y=r.loc[a], text=f"<b>{nombre(r.loc[a], 2)}</b> ({a})", showarrow=False, yshift=14, font=dict(size=11))
                habiller(fig, 330)
                tracer(fig, "abonnements_par_utilisateur")
                st.caption(bi(f"L’écart se creuse jusqu’en {a_max} (multi-SIM), puis se resserre : les utilisateurs augmentent plus vite que les abonnements.",
                              f"The gap widens until {a_max} (multi-SIM), then narrows: users grow faster than subscriptions."))
                export_csv(ecart_abo.reset_index(), "abonnements_par_utilisateur.csv", "export_ecart_abo")
        limite(bi("Série d’usage estimée (UIT). Chaque enquête a sa définition et sa tranche d’âge : elles ne se comparent pas entre elles. "
                  "Les événements annotés sont des coïncidences dans le temps, pas des causes démontrées. Les ruptures de série de 2020 et 2021 "
                  "(reclassement de la 3G de Togocel, révision de l’ARCEP) ne sont pas classées. Les utilisateurs sont reconstitués (part des "
                  "utilisateurs × population) : le ratio par utilisateur est un ordre de grandeur.",
                  "Usage series estimated (ITU). Each survey has its own definition and age range: they are not compared with each other. "
                  "The annotated events are coincidences in time, not demonstrated causes. The 2020 and 2021 series breaks (Togocel 3G "
                  "reclassification, ARCEP revision) are not classified. Users are reconstructed (share of users × population): the "
                  "per-user ratio is an order of magnitude."))

# =================================================================== 3. Accès et freins par région
if o_regions.open is not False:
    with o_regions:
        constat(bi(f"L’accès progresse dans toutes les régions, mais l’écart entre le Grand Lomé et les Savanes se creuse : "
                   f"<strong>{nombre(ecart_1, 1)}</strong> puis <strong>{nombre(ecart_2, 1)} points</strong>. Les Savanes cumulent l’accès "
                   f"et l’alphabétisation les plus faibles.",
                   f"Access is rising in every region, but the gap between Greater Lomé and Savanes is widening: "
                   f"<strong>{nombre(ecart_1, 1)}</strong> then <strong>{nombre(ecart_2, 1)} points</strong>. Savanes combines the lowest "
                   f"access with the lowest literacy."))
        pts_lib = bi("pt", "pt")
        ic = bi("IC 95 %", "95% CI")
        cartes_g, cartes_d = st.columns([2, 1], gap="large")
        with cartes_g:
            with st.container(border=True):
                titre_bloc(t("lib.acces_declare"), bi("Individus de 15 ans et plus (enquête EHCVM). Entre parenthèses : la marge d’erreur à 95 % ; "
                                                     "en dessous, le gain depuis 2018/19.",
                                                     "Individuals aged 15 and over (EHCVM survey). In brackets: the 95% margin of error; "
                                                     "below, the gain since 2018/19."))
                classes_acces = [bi("moins de 15 %", "under 15%"), bi("15 à 25 %", "15 to 25%"), bi("25 à 35 %", "25 to 35%"),
                                 bi("35 à 50 %", "35 to 50%"), bi("50 % et plus", "50% and over")]
                c1, c2 = st.columns(2)
                for col, suffixe, vague, avec_gain in ((c1, "2018_19", "2018/19", False), (c2, "2021_22", "2021/22", True)):
                    a = acces.reset_index()
                    a["valeur"] = a[f"estimation_pct_{suffixe}"]
                    marge = (a[f"ic95_haut_{suffixe}"] - a[f"ic95_bas_{suffixe}"]) / 2
                    a["etiquette"] = [f"{pct(v)}<br>(± {nombre(m, 1)})" + (f"<br>+{nombre(g, 1)} {pts_lib}" if avec_gain else "")
                                      for v, m, g in zip(a.valeur, marge, a.variation_points)]
                    a["survol"] = [f"<b>{region(n)}</b><br>{pct(v)} ({ic} : {nombre(lo, 1)} – {nombre(hi, 1)})"
                                   for n, v, lo, hi in zip(a.nom, a.valeur, a[f"ic95_bas_{suffixe}"], a[f"ic95_haut_{suffixe}"])]
                    with col:
                        st.markdown(f'<div class="groupe" style="text-align:center;">{html.escape(bi("Enquête EHCVM", "EHCVM survey"))} {vague}</div>',
                                    unsafe_allow_html=True)
                        carte_regions(a, f"carte_acces_{suffixe}", "valeur", [15, 25, 35, 50], classes_acces, selection=f_regions, hauteur=500)
                export_csv(acces.reset_index(), "acces_internet_regions.csv", "export_acces_regions")
        with cartes_d:
            with st.container(border=True):
                al = alpha[(alpha.indicateur == "alphabetisation") & (alpha.vague == alpha[alpha.indicateur == "alphabetisation"].vague.max())].copy()
                titre_bloc(bi("Alphabétisation, indice des compétences", "Literacy, a proxy for skills"),
                           bi(f"15 ans et plus, {al.vague.iloc[0]} (EHCVM) ; national : {pct(al.national_pct.iloc[0])}. Gain depuis 2018/19.",
                              f"Aged 15 and over, {al.vague.iloc[0]} (EHCVM); national: {pct(al.national_pct.iloc[0])}. Gain since 2018/19."))
                st.markdown('<div class="groupe">&nbsp;</div>', unsafe_allow_html=True)
                al["valeur"] = al.estimation_pct
                marge = (al.ic95_haut - al.ic95_bas) / 2
                al["etiquette"] = [f"{pct(v)}<br>(± {nombre(m, 1)})<br>+{nombre(g, 1)} {pts_lib}" for v, m, g in zip(al.valeur, marge, al.variation_points)]
                al["survol"] = [f"<b>{region(n)}</b><br>{pct(v)} ({ic} : {nombre(lo, 1)} – {nombre(hi, 1)})"
                                for n, v, lo, hi in zip(al.nom, al.valeur, al.ic95_bas, al.ic95_haut)]
                carte_regions(al, "carte_alphabetisation", "valeur", [50, 60, 70, 80],
                              [bi("moins de 50 %", "under 50%"), bi("50 à 60 %", "50 to 60%"), bi("60 à 70 %", "60 to 70%"),
                               bi("70 à 80 %", "70 to 80%"), bi("80 % et plus", "80% and over")], selection=f_regions, hauteur=500)
                export_csv(alpha[alpha.indicateur == "alphabetisation"], "alphabetisation_regions.csv", "export_alphabetisation")

        with st.container(border=True):
            titre_bloc(bi("Les freins à l’usage, région par région", "Barriers to use, region by region"),
                       bi("Un frein n’est recherché que là où l’usage est faible (sous 40 %) et la couverture théorique supérieure à 85 % ; il est "
                          "présumé par cette règle, pas démontré. Accès déclaré en 2021/22 ; l’alphabétisation sert d’indice des compétences ; "
                          "compétences numériques des 15-49 ans en 2017.",
                          "A barrier is only looked for where use is low (below 40%) and theoretical coverage above 85%; it is presumed by this "
                          "rule, not demonstrated. Self-reported access in 2021/22; literacy is used as a proxy for skills; digital skills of those "
                          "aged 15-49 in 2017."))
            fr_ = freins.copy()
            if f_regions:
                fr_ = fr_[fr_.unite_regionale.isin(f_regions)]
            c_reg, c_acc, c_couv = bi("région", "region"), bi("accès déclaré (%)", "self-reported access (%)"), \
                bi("couverture théorique (%)", "theoretical coverage (%)")
            c_alp, c_comp = bi("alphabétisation (%)", "literacy (%)"), bi("compétences numériques (F / H)", "digital skills (W / M)")
            c_frein = bi("frein présumé", "presumed barrier")
            competences = [bi("non mesurées", "not measured") if pd.isna(f_) else f"{pct(f_)} / {pct(h_)}"
                           for f_, h_ in zip(fr_["competences_TIC_Femmes 15-49 ans"], fr_["competences_TIC_Hommes 15-49 ans"])]
            tab = pd.DataFrame({c_reg: fr_.unite_regionale.map(region), c_frein: fr_.lecture_02.map(frein), c_acc: fr_.acces_internet_2021_22_pct,
                                c_couv: fr_.couverture_proxy_pct, c_alp: fr_.alphabetisation_15plus_pct, c_comp: competences})
            barre = lambda lib: st.column_config.ProgressColumn(lib, min_value=0, max_value=100, format="%.1f")
            st.dataframe(tab.sort_values(c_acc), hide_index=True, use_container_width=True,
                         column_config={c_reg: st.column_config.TextColumn(c_reg, width="medium"), c_acc: barre(c_acc),
                                        c_couv: barre(c_couv), c_alp: barre(c_alp)})
            st.caption(bi(f"Le coût pèse partout : 1 Go coûte {pct(freins.cout_1go_pct_revenu_national.iloc[0])} du revenu mensuel (chiffre national). "
                          f"{pct(smart['smartphone_telephone_principal'])} des adultes ont un smartphone comme téléphone principal ; "
                          f"{pct(smart['sans_smartphone_cause_cout'])} citent le coût comme raison de ne pas en avoir (Findex 2024).",
                          f"Cost weighs everywhere: 1 GB costs {pct(freins.cout_1go_pct_revenu_national.iloc[0])} of monthly income (national figure). "
                          f"{pct(smart['smartphone_telephone_principal'])} of adults use a smartphone as their main phone; "
                          f"{pct(smart['sans_smartphone_cause_cout'])} cite cost as the reason for not having one (Findex 2024)."))
            export_csv(tab, "freins_regions.csv", "export_freins")
        limite(bi("Six régions seulement : aucune enquête ne descend à la préfecture ni à la commune. L’accès déclaré n’est pas l’usage. "
                  "Le frein est présumé par une règle, pas démontré ; l’alphabétisation n’est qu’un indice des compétences ; les compétences "
                  "numériques datent de 2017 (15-49 ans) ; le coût et le smartphone ne sont connus qu’au niveau national.",
                  "Six regions only: no survey goes down to prefecture or commune level. Self-reported access is not use. The barrier "
                  "is presumed by a rule, not demonstrated; literacy is only a proxy for skills; digital skills date from 2017 (aged 15-49); "
                  "cost and smartphones are only known nationally."))

# =================================================================== 4. Le Togo dans l’UEMOA
if o_uemoa.open is not False:
    with o_uemoa:
        constat(bi(f"{rang(rang_debut)} de l’UEMOA en {a_debut_b}, {rangs_bas} de {rang_bas_de} à {rang_bas_a} : ses voisins progressent plus vite. "
                   f"Le Togo est <strong>{rang(rang_now)}</strong> depuis {depuis_b} ({pct(tgo.loc[a_b, 'valeur'])} en {a_b}), derrière {devant_noms}.",
                   f"{rang(rang_debut)} in WAEMU in {a_debut_b}, {rangs_bas} from {rang_bas_de} to {rang_bas_a}: its neighbours grow faster. "
                   f"Togo has been <strong>{rang(rang_now)}</strong> since {depuis_b} ({pct(tgo.loc[a_b, 'valeur'])} in {a_b}), behind {devant_noms}."))
        gauche, droite = st.columns([1.6, 1], gap="large")
        with gauche:
            with st.container(border=True):
                titre_bloc(bi(f"Usage d’Internet dans les 8 pays de l’UEMOA, 2000-{a_b}", f"Internet use in the 8 WAEMU countries, 2000-{a_b}"),
                           bi("Le Togo en trait épais ; les autres pays en gris (nom au survol), sauf celui que vous choisissez.",
                              "Togo in a thick line; other countries in grey (name on hover), except the one you choose."))
                autres = [i for i in PAYS if i != "TGO"]
                noms_pays = {pays(i): i for i in autres}
                choix_lib = st.selectbox(bi("Pays à comparer", "Country to compare"), [bi("aucun", "none")] + list(noms_pays),
                                         key=f"uemoa_pays_{langue()}")
                choix = noms_pays.get(choix_lib, "—")
                fig = go.Figure()
                for iso in autres:
                    s = bench[bench.iso3 == iso]
                    mis_en_avant = iso == choix
                    fig.add_scatter(x=s.annee, y=s.valeur, mode="lines", name=pays(iso) if mis_en_avant else bi("autres pays de l’UEMOA", "other WAEMU countries"),
                                    legendgroup="autres" if not mis_en_avant else iso, showlegend=mis_en_avant or iso == [a for a in autres if a != choix][0],
                                    line=dict(color=CATEGORIELLE[1] if mis_en_avant else "#cfccc4", width=2.5 if mis_en_avant else 1.5),
                                    hovertemplate=f"{pays(iso)} " + "%{x} : %{y:.1f} %<extra></extra>")
                ssf = bench[bench.iso3 == "SSF"]
                fig.add_scatter(x=ssf.annee, y=ssf.valeur, mode="lines", name=bi("Afrique subsaharienne", "Sub-Saharan Africa"),
                                line=dict(color=ENCRE, width=1.5, dash="dash"))
                fig.add_scatter(x=tgo.index, y=tgo.valeur, mode="lines", name="Togo", line=dict(color=CATEGORIELLE[0], width=4),
                                hovertemplate="Togo %{x} : %{y:.1f} %<extra></extra>")
                habiller(fig, 420, " %", xaxis=dict(gridcolor="#efece4", dtick=5))
                tracer(fig, "uemoa_courbes")
                export_csv(bench, "usage_internet_uemoa.csv", "export_uemoa")
        with droite:
            with st.container(border=True):
                titre_bloc(bi("Rang du Togo parmi les 8 pays", "Togo’s rank among the 8 countries"), bi("1 = usage le plus élevé.", "1 = highest use."))
                fig = go.Figure()
                fig.add_scatter(x=tgo.index, y=tgo.rang_uemoa_sur_8, mode="lines", line=dict(color=CATEGORIELLE[0], width=3, shape="hv"),
                                showlegend=False, hovertemplate="%{x} : %{y}<extra></extra>")
                habiller(fig, 220, yaxis=dict(autorange="reversed", dtick=1, range=[8.5, 0.5], gridcolor="#efece4"))
                tracer(fig, "uemoa_rang")
            with st.container(border=True):
                titre_bloc(bi(f"Classement {a_b}", f"{a_b} ranking"))
                cl = bench[(bench.annee == a_b) & bench.iso3.isin(PAYS)].sort_values("valeur", ascending=False)
                st.dataframe(pd.DataFrame({bi("rang", "rank"): range(1, len(cl) + 1), bi("pays", "country"): cl.iso3.map(pays),
                                           bi("usage", "use"): [pct(v) for v in cl.valeur]}),
                             hide_index=True, use_container_width=True)
        limite(bi("Des deux côtés, la plupart des valeurs sont des estimations de l’UIT : un rang compare des estimations entre elles, pas "
                  "des mesures. Le repère de l’Afrique subsaharienne ne commence qu’en 2005.",
                  "On both sides, most values are ITU estimates: a rank compares estimates with each other, not measurements. The "
                  "Sub-Saharan Africa reference only starts in 2005."))

# =================================================================== 5. Technologies
if o_techno.open is not False:
    with o_techno:
        rangee_kpi(bi(f"Abonnements data mobile ({a_t})", f"Mobile data subscriptions ({a_t})"), [
            carte_kpi(bi("Haut débit", "Broadband"), pct(techno.loc[a_t, "part_haut_debit_pct"]),
                      bi("des abonnements data mobile sont en 3G ou 4G", "of mobile data subscriptions are 3G or 4G"),
                      bi("seuil du passage au haut débit : 80 %", "broadband switch threshold: 80%"),
                      bi("Un abonnement n’est pas une personne : un usager peut avoir plusieurs cartes SIM.",
                         "A subscription is not a person: a user may have several SIM cards."),
                      bi("Seuil franchi", "Threshold reached") if techno.loc[a_t, "part_haut_debit_pct"] >= 80 else bi("Sous le seuil", "Below threshold"),
                      "ok" if techno.loc[a_t, "part_haut_debit_pct"] >= 80 else "alerte"),
            carte_kpi("4G", pct(techno.loc[a_t, "4G"]), bi("des abonnements data mobile", "of mobile data subscriptions"),
                      bi(f"{pct(techno.loc[a_t0, '4G'])} en {a_t0}", f"{pct(techno.loc[a_t0, '4G'])} in {a_t0}"), "", None, "neutre"),
            carte_kpi("2G", pct(techno.loc[a_t, "2G"]), bi("des abonnements data mobile", "of mobile data subscriptions"),
                      bi(f"{pct(techno.loc[a_t0, '2G'])} en {a_t0}", f"{pct(techno.loc[a_t0, '2G'])} in {a_t0}"), "", None, "neutre"),
            carte_kpi(bi("Fibre jusqu’au domicile", "Fibre to the home"), pct(techno.loc[a_t, "part_ftth_internet_pct"]),
                      bi("des abonnements Internet", "of Internet subscriptions"),
                      bi(f"{nombre(techno.loc[a_t, 'abonnes_ftth_T4'])} abonnés en {a_t}", f"{nombre(techno.loc[a_t, 'abonnes_ftth_T4'])} subscribers in {a_t}"),
                      "", None, "neutre"),
        ])
        st.write("")
        gauche, droite = st.columns([1.6, 1], gap="large")
        with gauche:
            with st.container(border=True):
                titre_bloc(bi(f"Abonnements data mobile par technologie, {a_t0}-{a_t}", f"Mobile data subscriptions by technology, {a_t0}-{a_t}"),
                           bi("Part de chaque technologie (valeur du 4e trimestre, ARCEP).", "Share of each technology (fourth-quarter value, ARCEP)."))
                tt = techno.loc[a_t0:]
                fig = go.Figure()
                for col, nom, coul in (("2G", "2G", CATEGORIELLE[4]),
                                       ("3G+4G (Moov, non ventilé)", bi("3G et 4G de Moov, non ventilées", "Moov 3G and 4G, not broken down"), CATEGORIELLE[3]),
                                       ("3G", "3G", CATEGORIELLE[1]), ("4G", "4G", CATEGORIELLE[0])):
                    fig.add_bar(x=tt.index, y=tt[col], name=nom, marker_color=coul, marker_line_color="#ffffff", marker_line_width=1.5,
                                text=[pct(v, 0) if col == "4G" and v >= 10 else "" for v in tt[col]], textposition="inside",
                                textfont=dict(color="#ffffff", size=11), hovertemplate=f"{nom} " + "%{x} : %{y:.1f} %<extra></extra>")
                fig.add_vline(x=2019.5, line=dict(color="#55534e", width=1))
                fig.add_annotation(x=2019.5, y=100, text=bi("rupture de série (1er trimestre 2020)", "series break (Q1 2020)"), showarrow=False,
                                   xanchor="left", yanchor="bottom", xshift=4, font=dict(size=10, color="#55534e"))
                habiller(fig, 380, " %", legende_y=1.14, barmode="stack", bargap=0.3, xaxis=dict(gridcolor="#efece4", dtick=1),
                         yaxis=dict(ticksuffix=" %", gridcolor="#efece4", range=[0, 106]))
                tracer(fig, "mix_technologique")
                export_csv(tt.reset_index()[["annee", "2G", "3G", "4G", "3G+4G (Moov, non ventilé)", "part_haut_debit_pct"]],
                           "technologies_data.csv", "export_technologies")
        with droite:
            constat(bi(f"La 4G devient majoritaire en {a_t} ({pct(techno.loc[a_t, '4G'])} des abonnements data) ; la 2G recule de "
                       f"{pct(techno.loc[a_t0, '2G'])} à {pct(techno.loc[a_t, '2G'])}.",
                       f"4G becomes the majority in {a_t} ({pct(techno.loc[a_t, '4G'])} of data subscriptions); 2G falls from "
                       f"{pct(techno.loc[a_t0, '2G'])} to {pct(techno.loc[a_t, '2G'])}."))
            limite(bi("Un abonnement n’est pas une personne. Rupture de série au 1er trimestre 2020 (reclassement de la 3G de Togocel) ; "
                      "avant 2020, la 3G et la 4G de Moov ne sont pas ventilées. La fibre compte des abonnés à domicile, pas des km de câble.",
                      "A subscription is not a person. Series break in Q1 2020 (Togocel 3G reclassification); before 2020, Moov’s 3G "
                      "and 4G are not broken down. Fibre counts home subscribers, not km of cable."))

# =================================================================== 6. Marché des télécoms (objectif 2)
if o_marche.open is not False:
    with o_marche:
        dernier = hhi[hhi.segment.str.contains("data", case=False)].sort_values("annee").iloc[-1]
        inv_now = inv.iloc[-1]
        sans_fibre = fibre[fibre.raccorde_02 == "non raccordé"]
        s_der = sites.sort_values("annee").iloc[-1]
        rangee_kpi(bi("Marché des télécommunications", "Telecommunications market"), [
            carte_kpi(bi(f"Parts de marché ({int(dernier.annee)})", f"Market shares ({int(dernier.annee)})"), pct(dernier.part_togocom_pct),
                      bi("des abonnés data chez Togocom (YAS)", "of data subscribers with Togocom (YAS)"),
                      bi(f"Moov : {pct(dernier.part_moov_pct)} ; indice de concentration : {nombre(dernier.hhi, 0)}",
                         f"Moov: {pct(dernier.part_moov_pct)}; concentration index: {nombre(dernier.hhi, 0)}"),
                      "", bi("Très concentré", "Highly concentrated"), "alerte"),
            carte_kpi(bi(f"Investissement ({int(inv_now.annee)})", f"Investment ({int(inv_now.annee)})"),
                      pct(inv_now.taux_investissement_pct), bi("du chiffre d’affaires des opérateurs", "of operators' revenue"),
                      bi("seuil d’alerte : 15 % ; série cyclique", "alert threshold: 15%; cyclical series"),
                      bi("Mesure en valeur (FCFA) ; les sites radio la complètent en volume.", "Measured in value (FCFA); radio sites complement it in volume."),
                      inv_now.classe_02.replace("cycle d’extension", bi("Cycle d’extension", "Extension cycle")).replace(
                          "régime normal", bi("Régime normal", "Normal regime")), "ok" if inv_now.taux_investissement_pct >= 15 else "alerte"),
            carte_kpi(bi(f"Sites radio ({int(s_der.annee)})", f"Radio sites ({int(s_der.annee)})"), f"+{int(s_der.ajouts_nets_total)}",
                      bi("sites ajoutés en un an (ajouts nets)", "sites added in one year (net additions)"),
                      bi("repère de veille : 50 par an", "watch reference: 50 a year"),
                      bi("Un site compte une fois, quelle que soit sa technologie.", "A site counts once, whatever its technology."),
                      bi("Sous le repère", "Below reference") if s_der.ajouts_nets_total < 50 else bi("Au-dessus du repère", "Above reference"),
                      "alerte" if s_der.ajouts_nets_total < 50 else "ok"),
        ])
        st.write("")
        gauche, droite = st.columns([1.25, 1], gap="large")
        with gauche:
            with st.container(border=True):
                titre_bloc(bi("Sites radio (déploiement physique)", "Radio sites (physical deployment)"),
                           bi("Ajouts nets par an, par opérateur ; repère de veille à 50.", "Net additions per year, by operator; watch reference at 50."))
                s4 = sites[sites.annee >= 2022]
                fig = go.Figure()
                fig.add_bar(x=s4.annee, y=s4.ajouts_nets_moov, name="Moov Africa", marker_color=CATEGORIELLE[0])
                fig.add_bar(x=s4.annee, y=s4.ajouts_nets_yas, name="YAS", marker_color=CATEGORIELLE[1])
                fig.add_hline(y=50, line=dict(color="#8a1c1b", width=1, dash="dash"),
                              annotation_text=bi("Repère de veille : 50", "Watch reference: 50"), annotation_position="top left")
                habiller(fig, 260, legende_y=1.18, barmode="stack", xaxis=dict(gridcolor="#efece4", dtick=1))
                tracer(fig, "sites_radio")
                a22 = int(sites.loc[sites.annee == 2022, "ajouts_nets_total"].iloc[0])
                st.caption(bi(f"Les ajouts nets tombent de {a22} à {int(s_der.ajouts_nets_total)} en trois ans ; {int(s_der.annee)} est la "
                              "première année sous le repère de veille.",
                              f"Net additions fall from {a22} to {int(s_der.ajouts_nets_total)} in three years; {int(s_der.annee)} is the "
                              "first year below the watch reference."))
                export_csv(sites, "sites_radio.csv", "export_sites_radio")
        with droite:
            constat(bi(f"Deux opérateurs se partagent le marché ; Togocom (YAS) a {pct(dernier.part_togocom_pct)} des abonnés data. "
                       f"Le déploiement de sites radio ralentit : +{a22} en 2022, +{int(s_der.ajouts_nets_total)} en {int(s_der.annee)}.",
                       f"Two operators share the market; Togocom (YAS) has {pct(dernier.part_togocom_pct)} of data subscribers. "
                       f"Radio-site deployment is slowing: +{a22} in 2022, +{int(s_der.ajouts_nets_total)} in {int(s_der.annee)}."))
            with st.container(border=True):
                titre_bloc(bi("Fibre : préfectures non raccordées", "Fibre: unconnected prefectures"),
                           bi(f"{len(sans_fibre)} préfectures {t('lib.sans_fibre')}.", f"{len(sans_fibre)} prefectures with {t('lib.sans_fibre')}."))
                tab = sans_fibre[["nom", "unite_regionale", "pop_totale"]].rename(columns={
                    "nom": bi("préfecture", "prefecture"), "unite_regionale": bi("région", "region"), "pop_totale": bi("habitants", "population")})
                tab[bi("région", "region")] = tab[bi("région", "region")].map(region)
                st.dataframe(tab, hide_index=True, use_container_width=True)
                export_csv(sans_fibre[["nom", "unite_regionale", "pop_totale"]], "fibre_non_raccordees.csv", "export_fibre")
        limite(bi("Le marché est mesuré au niveau national seulement. Un site radio compte une fois, quelle que soit sa technologie. "
                  "L’investissement est une mesure en valeur, cyclique d’une année à l’autre.",
                  "The market is measured nationally only. A radio site counts once, whatever its technology. Investment is measured "
                  "in value, and cycles from year to year."))

pied()
