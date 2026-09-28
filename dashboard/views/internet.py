"""Page 2 — Usage d’Internet : « L’usage progresse-t-il, et à quel prix ? » (plan visuel, section 7, page 2).

Quatre sous-onglets (demande du 27/09/2026, `workspace/conding-progress.md`) : une « Vue synthèse » de l’objectif 1
(retracer l’usage d’Internet, repérer les périodes d’accélération ou de stagnation), puis trois onglets qui en détaillent
les analyses (évolution de l’usage, accès et freins par région, le Togo dans l’UEMOA). Seul l’onglet ouvert s’exécute.
La Vue synthèse résume sans dupliquer : un visuel détaillé dans un autre onglet n’y est qu’annoncé. Le marché des
télécommunications et les technologies (objectif 2) ont leur page depuis le 28/09/2026 (`marche.py`).

Chiffres nationaux, sauf ceux de l’onglet régional, dont les cartes cerclent les régions du filtre.
"""
import html

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from composants import (BLEU_FONCE, ariane, carte_kpi, carte_regions, colorer_regions, constat, entete, export_csv, habiller, limite, note,
                        onglets, pct, pied, rangee_kpi, synthese, titre_bloc, tracer)
from donnees import lire, nombre, rang
from i18n import bi, frein, langue, region, t
from theme import CATEGORIELLE, CATEGORIELLE_8, ENCRE, OCRE, PRIORITE, TEXTE_CATEGORIELLE

f_regions = st.session_state.f_regions
SEUIL_USAGE = 40        # seuil de l’usage d’Internet (O1-01, hypothèse du sujet)
SEUIL_STAGNATION = 2    # croissance annuelle sous laquelle une année est une stagnation (O1-02)
ROUGE_CLAIR = "#e34948"  # rouge de la palette du tableau de bord : libellé du repère « un abonnement par utilisateur »

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
c1go = lire("07_indicateurs", "o2_05b_cout_1go").set_index("annee")
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


def _classe(x) -> str:
    """Classe sans sa précision entre parenthèses (« accélération (une seule valeur publiée) » → « accélération »)."""
    return str(x).split(" (")[0] if pd.notna(x) else ""


# Sensibilité des classes (05, constat C2 ; 07, O1-02) : une année « dépend de la convention » si sa classe change avec la
# période de référence 2015-2024 (usage, abonnements) ou quand les ruptures sont comptées (abonnements). Lu dans les tables.
usage_dep = [int(a) for a in usage.index if pd.notna(usage.loc[a, "classe_variante_2015"])
             and usage.loc[a, "classe_variante_2015"] != usage.loc[a, "classe"]]
abo_dep = [int(a) for a in abo.index if _classe(abo.loc[a, "classe_finale"]) != "non classé"
           and any(pd.notna(abo.loc[a, c]) and _classe(abo.loc[a, c]) != _classe(abo.loc[a, "classe_finale"])
                   for c in ("classe_finale_variante_2015", "classe_finale_ruptures_comptees"))]
variante_dep = sorted({usage.loc[a, "classe_variante_2015"] for a in usage_dep})
debut_ralent_abo = min(abo_ralent)
ralent_sur_uit = min(a for a in annees_ralent if a not in usage_dep)
ralent_sur_abo = min(a for a in abo_ralent if a not in abo_dep)
au_dessus_ass = pen.ecart_ass_points.dropna() > 0
depuis_ass = int(au_dessus_ass[~au_dessus_ass].index.max() + 1) if (~au_dessus_ass).any() else int(au_dessus_ass.index.min())
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
COULEUR_PAYS = dict(zip(["SEN", "CIV", "TGO", "MLI", "BEN", "GNB", "BFA", "NER"],
                        [CATEGORIELLE_8[i] for i in (1, 2, 0, 3, 4, 5, 6, 7)]))  # le Togo garde le bleu du tableau de bord
devant = bench[(bench.annee == a_b) & bench.iso3.isin(PAYS) & (bench.valeur > tgo.loc[a_b, "valeur"])].sort_values("valeur", ascending=False)
devant_noms = bi(" et ", " and ").join(pays(i) for i in devant.iso3)

a_t = int(techno.index.max())
c1go_now = c1go.iloc[-1]


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
            bi("Accès et freins par région", "Access and barriers by region"), bi("Le Togo dans l’UEMOA", "Togo within WAEMU")]
o_synth, o_evol, o_regions, o_uemoa = onglets("internet_onglets", LIBELLES)

# =================================================================== 1. Vue synthèse
if o_synth.open is not False:
    with o_synth:
        rangee_kpi(bi("L’usage d’Internet en quatre chiffres", "Internet use in four figures"), [
            carte_kpi(bi(f"Usage d’Internet ({a_u})", f"Internet use ({a_u})"), pct(u_now),
                      bi("de la population utilise Internet", "of the population uses the Internet"),
                      bi(f"Afrique subsaharienne : {pct(ass_now)}, dépassée depuis {depuis_ass} ; seuil : {SEUIL_USAGE} %",
                         f"Sub-Saharan Africa: {pct(ass_now)}, exceeded since {depuis_ass}; threshold: {SEUIL_USAGE}%"),
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
                              "Les points marquent les années d’accélération et de ralentissement ; un cercle vide, une classe qui "
                              "dépend de la période de référence.",
                              "ITU estimate, with the Sub-Saharan Africa reference (published since 2005) and the 40% threshold. "
                              "Dots mark the years of acceleration and slowdown; a hollow circle, a class that depends on the "
                              "reference period."))
                fig = go.Figure()
                fig.add_scatter(x=d1.index, y=d1.pct_population, mode="lines", name="Togo", line=dict(color=PRIORITE["haute"], width=3),
                                hovertemplate="%{x} : %{y:.1f} %<extra>Togo</extra>")
                ass = pen.afrique_subsaharienne_pct.dropna()
                fig.add_scatter(x=ass.index, y=ass.values, mode="lines", name=bi("Afrique subsaharienne", "Sub-Saharan Africa"),
                                line=dict(color="#8a8780", width=2, dash="dot"))
                for annees, coul, nom in ((annees_accel, PRIORITE["moyenne"], bi("année d’accélération", "year of acceleration")),
                                          (annees_ralent, OCRE, bi("année de ralentissement", "year of slowdown"))):
                    sures, dep = [a for a in annees if a not in usage_dep], [a for a in annees if a in usage_dep]
                    fig.add_scatter(x=sures, y=[d1.loc[a, "pct_population"] for a in sures], mode="markers", name=nom, legendgroup=nom,
                                    marker=dict(color=coul, size=11, line=dict(color="#ffffff", width=2)))
                    fig.add_scatter(x=dep, y=[d1.loc[a, "pct_population"] for a in dep], mode="markers", name=nom, legendgroup=nom,
                                    showlegend=False, marker=dict(color="#ffffff", size=11, line=dict(color=coul, width=2.5)))
                fig.add_scatter(x=[None], y=[None], mode="markers", name=bi("cercle vide : dépend de la période de référence",
                                                                           "hollow circle: depends on the reference period"),
                                marker=dict(color="#ffffff", size=11, line=dict(color="#55534e", width=2)))
                fig.add_hline(y=SEUIL_USAGE, line=dict(color="#8a1c1b", width=1, dash="dash"),
                              annotation_text=bi("Seuil de 40 %", "40% threshold"), annotation_position="top left")
                a0 = int(d1.index.min())
                fig.add_annotation(x=a0, y=d1.loc[a0, "pct_population"], ax=40, ay=-60, showarrow=True, arrowcolor="#8a8780",
                                   text=bi(f"{a0} : premiers utilisateurs ({nombre(d1.loc[a0, 'pct_population'], 2)} %)",
                                           f"{a0}: first users ({nombre(d1.loc[a0, 'pct_population'], 2)}%)"),
                                   font=dict(size=10, color="#55534e"), xanchor="left")
                fig.add_annotation(x=a_u, y=u_now, text=f"<b>{pct(u_now)}</b>", showarrow=False, xanchor="left", xshift=8, font=dict(size=12))
                habiller(fig, 420, " %", legende_y=-0.1, xaxis=dict(gridcolor="#efece4", range=[1995, a_u + 3], dtick=5))
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
                           bi("Classes de la croissance annuelle, période de référence 2010-2024. En gras, les classes sûres.",
                              "Classes of annual growth, reference period 2010-2024. In bold, the firm classes."))
                virg, dp = ", ", bi(" : ", ": ")
                aucune = bi("aucune année", "no year")
                stagn_txt = virg.join(map(str, annees_stagn)) if annees_stagn else aucune
                selon = html.escape(bi("selon la période de référence", "depending on the reference period"))

                def annees_html(annees: list[int]) -> str:
                    sures = virg.join(f"<b>{a}</b>" for a in annees if a not in usage_dep)
                    dep = virg.join(str(a) for a in annees if a in usage_dep)
                    pv = bi(" ; ", "; ")
                    return sures + (f'{pv}<span style="color:#55534e">{dep} ({selon})</span>' if dep else "")

                en_anglais = {"rythme habituel": "usual pace", "accélération": "acceleration", "ralentissement": "slowdown"}
                lib_variante = bi(" et ".join(f"« {v} »" for v in variante_dep), " and ".join(f"“{en_anglais.get(v, v)}”" for v in variante_dep))
                note = bi(f"Avec 2015-2024 comme période de référence, {virg.join(map(str, usage_dep))} passent en {lib_variante} : "
                          f"seules {' et '.join(str(a) for a in annees_accel + annees_ralent if a not in usage_dep)} gardent leur classe.",
                          f"With 2015-2024 as the reference period, {virg.join(map(str, usage_dep))} move to {lib_variante}: "
                          f"only {' and '.join(str(a) for a in annees_accel + annees_ralent if a not in usage_dep)} keep their class.")
                st.markdown(
                    f'<div class="periodes">'
                    f'<div><b>{html.escape(bi("Accélération", "Acceleration"))}</b>{dp}{annees_html(annees_accel)}</div>'
                    f'<div><b>{html.escape(bi("Ralentissement", "Slowdown"))}</b>{dp}{annees_html(annees_ralent)}</div>'
                    f'<div><b>{html.escape(bi("Stagnation", "Stagnation"))}</b>{dp}{html.escape(stagn_txt)} '
                    f'{html.escape(bi(f"(croissance jamais sous {SEUIL_STAGNATION} % par an)", f"(growth never below {SEUIL_STAGNATION}% a year)"))}</div>'
                    f'<div style="font-size:0.84rem;color:#55534e;border-top:1px solid #efece4;padding-top:8px">{html.escape(note)}</div>'
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
               f"4G accounts for {pct(techno.loc[a_t, '4G'])} of mobile data subscriptions in {a_t}.")
            + f" <i>({bi('détail : page', 'details:')} {og}{t('page.marche')}{fg}{bi(', onglet', ' page,')} {og}{bi('Technologies et fibre', 'Technologies and fibre')}{fg}{bi('', ' tab')})</i>",
        ])
        limite(bi("Série d’usage estimée par l’UIT (sauf 2017), pas mesurée directement. Les classes de croissance portent sur 2010-2024 : "
                  "avant 2005, les taux portent sur des niveaux inférieurs à 2 % et ne se lisent pas. Le classement de la page "
                  f"{og}{t('page.priorites')}{fg} ne porte pas sur l’usage d’Internet : aucune mesure d’usage n’existe à la préfecture ; "
                  f"pour l’usage, les priorités se lisent par région (onglet {og}{LIBELLES[2]}{fg}).",
                  "Usage series estimated by the ITU (except 2017), not directly measured. Growth classes cover 2010-2024: before 2005, "
                  "rates apply to levels below 2% and are not interpreted. The ranking on the "
                  f"{og}{t('page.priorites')}{fg} page is not about Internet use: no measure of use exists at prefecture level; for use, "
                  f"priorities are read by region ({og}{LIBELLES[2]}{fg} tab)."))

# =================================================================== 2. Évolution de l’usage
if o_evol.open is not False:
    with o_evol:
        constat(bi(f"Toutes les sources voient le ralentissement, mais pas au même moment : l’UIT dès {debut_ralent_uit}, les abonnements "
                   f"data dès {debut_ralent_abo}, l’Afrobaromètre entre {int(afro_dern.debut)} et {int(afro_dern.fin)} "
                   f"(+{nombre(afro_dern.croissance_annualisee_pct, 1)} % par an).",
                   f"All sources see the slowdown, but not at the same time: the ITU from {debut_ralent_uit}, data subscriptions from "
                   f"{debut_ralent_abo}, the Afrobarometer between {int(afro_dern.debut)} and {int(afro_dern.fin)} "
                   f"(+{nombre(afro_dern.croissance_annualisee_pct, 1)}% a year).")
                + bi(f" Il est sûr en {ralent_sur_uit} pour l’usage et en {ralent_sur_abo} pour les abonnements ; la classe des années "
                     "suivantes dépend de la convention retenue (en pointillés).",
                     f" It is firm in {ralent_sur_uit} for use and in {ralent_sur_abo} for subscriptions; the class of later years "
                     "depends on the convention used (dotted)."))
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
                # motif posé par-dessus la couleur de la barre (par défaut, Plotly remplace la couleur par le motif)
                pointilles = dict(fgcolor="#ffffff", size=5, solidity=0.45, fillmode="overlay")
                for cl, coul in couleur_classe.items():
                    sub = u10[u10.classe == cl]
                    fig.add_bar(x=sub.index, y=sub.variation_points, name=lib_classe[cl], marker_color=coul,
                                marker_pattern=dict(shape=["." if a in usage_dep else "" for a in sub.index], **pointilles))
                # entrée de légende : une barre de hauteur nulle (une barre sans donnée n’aurait pas d’icône)
                fig.add_bar(x=[u10.index.min()], y=[0], name=bi("pointillés : selon la période de référence", "dotted: depends on the reference period"),
                            marker_color="#8a8780", marker_pattern=dict(shape=".", **pointilles), hoverinfo="skip")
                # Événements retenus, lus comme des coïncidences dans le temps, pas comme des causes (limite de l’onglet)
                evenements = [(2016, bi("3G de Moov", "Moov 3G")), (2018, bi("4G à Lomé", "4G in Lomé")),
                              (2020, bi("Covid-19 ; 5G Togocom", "Covid-19; Togocom 5G")), (2022, bi("Câble Equiano", "Equiano cable")),
                              (2023, bi("Forfaits Moov -71 %", "Moov plans -71%"))]
                haut = u10.variation_points.max()
                for an, lib in evenements:  # au-dessus de la plus haute barre, pour ne jamais la chevaucher
                    fig.add_annotation(x=an, y=haut * 1.08, text=lib, showarrow=False, textangle=-90, font=dict(size=11, color=BLEU_FONCE),
                                       yanchor="bottom")
                habiller(fig, 360, " pts", legende_y=1.12, bargap=0.3, barmode="relative", yaxis=dict(ticksuffix=" pts", gridcolor="#efece4", range=[0, haut * 2.0]),
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
                           bi("Valeur du 4e trimestre (ARCEP), classée sur 2010-2024. Les années de rupture de série ne sont pas classées ; "
                              "en pointillés, une classe qui change avec la période 2015-2024 ou quand les ruptures sont comptées.",
                              "Fourth-quarter value (ARCEP), classified over 2010-2024. Series-break years are not classified; dotted, a "
                              "class that changes with the 2015-2024 period or when breaks are counted."))
                ab = abo.copy()
                ab["cl"] = ab.classe_finale.astype(str).str.split(" \\(").str[0].replace({"non classé": "rupture"})
                fig = go.Figure()
                for cl, coul in list(couleur_classe.items()) + [("rupture", "#d9d6cd")]:
                    sub = ab[ab.cl == cl]
                    motif = ["/" if cl == "rupture" else "." if a in abo_dep else "" for a in sub.index]
                    fig.add_bar(x=sub.index, y=sub.croissance_T4_pct, name=lib_classe[cl], marker_color=coul,
                                marker_pattern=dict(shape=motif, fgcolor="#8a8780" if cl == "rupture" else "#ffffff", size=5,
                                                    solidity=0.45, fillmode="overlay"),
                                marker_line_color="#8a8780" if cl == "rupture" else coul)
                fig.add_bar(x=[ab.index.min()], y=[0], name=bi("pointillés : selon la convention", "dotted: depends on the convention"),
                            marker_color="#8a8780", marker_pattern=dict(shape=".", fgcolor="#ffffff", size=5, solidity=0.45, fillmode="overlay"),
                            hoverinfo="skip")
                # une seule barre par année : « relative » lui donne toute la largeur (en « group », chaque trace réserve sa place)
                habiller(fig, 330, " %", legende_y=1.16, bargap=0.3, barmode="relative", xaxis=dict(gridcolor="#efece4", dtick=2))
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
                              annotation_text=bi("un abonnement par utilisateur", "one subscription per user"), annotation_position="bottom right",
                              annotation_font=dict(size=11, color=ROUGE_CLAIR))
                for a in (a_max, int(r.index.max())):
                    fig.add_annotation(x=a, y=r.loc[a], text=f"<b>{nombre(r.loc[a], 2)}</b> ({a})", showarrow=False, yshift=14,
                                       font=dict(size=11, color=BLEU_FONCE))
                habiller(fig, 330)
                tracer(fig, "abonnements_par_utilisateur")
                note(bi(f"L’écart se creuse jusqu’en {a_max} (multi-SIM), puis se resserre : les utilisateurs augmentent plus vite que les abonnements.",
                        f"The gap widens until {a_max} (multi-SIM), then narrows: users grow faster than subscriptions."), forte=True)
                export_csv(ecart_abo.reset_index(), "abonnements_par_utilisateur.csv", "export_ecart_abo")
        limite(bi("Série d’usage estimée (UIT). Chaque enquête a sa définition et sa tranche d’âge : elles ne se comparent pas entre elles. "
                  "Les événements annotés sont des coïncidences dans le temps, pas des causes démontrées. Les ruptures de série de 2020 et 2021 "
                  "(reclassement de la 3G de Togocel, révision de l’ARCEP) ne sont pas classées. Les classes en pointillés changent si l’on "
                  "prend 2015-2024 comme période de référence (ou, pour les abonnements, si l’on compte les ruptures) : seules les autres "
                  "sont sûres. Les utilisateurs sont reconstitués (part des "
                  "utilisateurs × population) : le ratio par utilisateur est un ordre de grandeur.",
                  "Usage series estimated (ITU). Each survey has its own definition and age range: they are not compared with each other. "
                  "The annotated events are coincidences in time, not demonstrated causes. The 2020 and 2021 series breaks (Togocel 3G "
                  "reclassification, ARCEP revision) are not classified. Dotted classes change if 2015-2024 is taken as the reference "
                  "period (or, for subscriptions, if breaks are counted): only the others are firm. Users are reconstructed (share of "
                  "users × population): the "
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

        # Accès et couverture ne vont pas ensemble (06, section 6 et constat S6) : lu dans la table des freins
        fz = freins.set_index("unite_regionale")
        hors_gl = fz.drop(index="Grand Lomé")
        r_acces_min = hors_gl.acces_internet_2021_22_pct.idxmin()
        r_couv_min = hors_gl.couverture_proxy_pct.idxmin()
        rang_acces_couv_min = int(hors_gl.acces_internet_2021_22_pct.rank(ascending=False)[r_couv_min])
        qualif = bi("l’un des meilleurs accès" if rang_acces_couv_min <= 2 else "un accès moyen",
                    "one of the best access rates" if rang_acces_couv_min <= 2 else "an average access rate")
        constat(bi(f"Accès et couverture ne vont pas ensemble. {region(r_acces_min)} : couverture théorique de "
                   f"<strong>{pct(fz.loc[r_acces_min, 'couverture_proxy_pct'])}</strong>, mais l’accès le plus faible "
                   f"(<strong>{pct(fz.loc[r_acces_min, 'acces_internet_2021_22_pct'])}</strong>) : le réseau n’y est pas le premier frein. "
                   f"{region(r_couv_min)} : la couverture la plus faible ({pct(fz.loc[r_couv_min, 'couverture_proxy_pct'])}), mais "
                   f"{qualif} hors du Grand Lomé ({pct(fz.loc[r_couv_min, 'acces_internet_2021_22_pct'])}). "
                   "Six régions : c’est un constat, pas une corrélation.",
                   f"Access and coverage do not go together. {region(r_acces_min)}: theoretical coverage of "
                   f"<strong>{pct(fz.loc[r_acces_min, 'couverture_proxy_pct'])}</strong>, but the lowest access "
                   f"(<strong>{pct(fz.loc[r_acces_min, 'acces_internet_2021_22_pct'])}</strong>): the network is not the main barrier there. "
                   f"{region(r_couv_min)}: the lowest coverage ({pct(fz.loc[r_couv_min, 'couverture_proxy_pct'])}), but "
                   f"{qualif} outside Greater Lomé ({pct(fz.loc[r_couv_min, 'acces_internet_2021_22_pct'])}). "
                   "Six regions: an observation, not a correlation."))

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
            st.dataframe(colorer_regions(tab.sort_values(c_acc), c_reg), hide_index=True, use_container_width=True,
                         column_config={c_reg: st.column_config.TextColumn(c_reg, width="medium"), c_acc: barre(c_acc),
                                        c_couv: barre(c_couv), c_alp: barre(c_alp)})
            note(bi(f"Le coût pèse partout : 1 Go coûte {pct(freins.cout_1go_pct_revenu_national.iloc[0])} du revenu mensuel (chiffre national). "
                    f"{pct(smart['smartphone_telephone_principal'])} des adultes ont un smartphone comme téléphone principal ; "
                    f"{pct(smart['sans_smartphone_cause_cout'])} citent le coût comme raison de ne pas en avoir (Findex 2024).",
                    f"Cost weighs everywhere: 1 GB costs {pct(freins.cout_1go_pct_revenu_national.iloc[0])} of monthly income (national figure). "
                    f"{pct(smart['smartphone_telephone_principal'])} of adults use a smartphone as their main phone; "
                    f"{pct(smart['sans_smartphone_cause_cout'])} cite cost as the reason for not having one (Findex 2024)."), forte=True)
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
                           bi(f"Une couleur par pays, le Togo en trait épais ; légende triée par la valeur de {a_b}. "
                              "Choisir un pays estompe les autres.",
                              f"One colour per country, Togo in a thick line; legend sorted by the {a_b} value. "
                              "Choosing a country fades the others."))
                autres = [i for i in PAYS if i != "TGO"]
                noms_pays = {pays(i): i for i in autres}
                choix_lib = st.selectbox(bi("Pays à mettre en évidence", "Country to highlight"), [bi("aucun", "none")] + list(noms_pays),
                                         key=f"uemoa_pays_{langue()}")
                choix = noms_pays.get(choix_lib, "—")
                v_b = bench[bench.annee == a_b].set_index("iso3").valeur
                ordre_legende = {iso: k for k, iso in enumerate(v_b.sort_values(ascending=False).index)}
                sep = bi(" : ", ": ")
                fig = go.Figure()
                for iso in autres:
                    s_ = bench[bench.iso3 == iso]
                    estompe = choix in PAYS and iso != choix
                    fig.add_scatter(x=s_.annee, y=s_.valeur, mode="lines", name=f"{pays(iso)}{sep}{pct(v_b[iso])}",
                                    legendrank=ordre_legende[iso], opacity=0.25 if estompe else 1,
                                    line=dict(color=COULEUR_PAYS[iso], width=3 if iso == choix else 2),
                                    hovertemplate=f"{pays(iso)} " + "%{x} : %{y:.1f} %<extra></extra>")
                ssf = bench[bench.iso3 == "SSF"]
                fig.add_scatter(x=ssf.annee, y=ssf.valeur, mode="lines", name=bi("Afrique subsaharienne", "Sub-Saharan Africa") + f"{sep}{pct(v_b['SSF'])}",
                                legendrank=ordre_legende["SSF"], line=dict(color=ENCRE, width=1.5, dash="dash"))
                fig.add_scatter(x=tgo.index, y=tgo.valeur, mode="lines", name=f"<b>Togo{sep}{pct(v_b['TGO'])}</b>",
                                legendrank=ordre_legende["TGO"], line=dict(color=COULEUR_PAYS["TGO"], width=4),
                                hovertemplate="Togo %{x} : %{y:.1f} %<extra></extra>")
                fig.add_annotation(x=a_b, y=tgo.loc[a_b, "valeur"], text="<b>Togo</b>", showarrow=False, xanchor="left", xshift=6,
                                   font=dict(size=12, color=TEXTE_CATEGORIELLE[COULEUR_PAYS["TGO"]]))
                # légende dans le graphique, en haut à gauche : les courbes y restent sous 10 % jusqu’en 2010 (comme la figure 11 du 05)
                habiller(fig, 440, " %", xaxis=dict(gridcolor="#efece4", dtick=5, range=[1999.5, a_b + 2.8]),
                         legend=dict(orientation="v", x=0.01, y=0.99, xanchor="left", yanchor="top", bgcolor="rgba(255,255,255,0.85)",
                                     title=dict(text=bi(f"En {a_b}", f"In {a_b}")), font=dict(size=11)))
                tracer(fig, "uemoa_courbes")
                export_csv(bench, "usage_internet_uemoa.csv", "export_uemoa")
        with droite:
            with st.container(border=True):
                titre_bloc(bi("Rang du Togo parmi les 8 pays", "Togo’s rank among the 8 countries"), bi("1 = usage le plus élevé.", "1 = highest use."))
                fig = go.Figure()
                fig.add_scatter(x=tgo.index, y=tgo.rang_uemoa_sur_8, mode="lines", line=dict(color=CATEGORIELLE[0], width=3, shape="hv"),
                                showlegend=False, hovertemplate="%{x} : %{y}<extra></extra>")
                # rang écrit sur les phases importantes : l’année de départ, puis chaque palier tenu au moins 2 ans ; au milieu du
                # palier tel qu’il est tracé (en escalier, un palier court jusqu’à l’année suivante, sauf le dernier)
                rg = tgo.rang_uemoa_sur_8.astype(int)
                paliers = [(int(g.index.min()), int(g.index.max()), int(g.iloc[0])) for _, g in rg.groupby(rg.ne(rg.shift()).cumsum())]
                for de, a, r in [p for k, p in enumerate(paliers) if k == 0 or p[1] > p[0]]:
                    fin = a + 1 if a < a_b else a
                    fig.add_annotation(x=(de + fin) / 2, y=r, text=f"<b>{rang(r)}</b>", showarrow=False, yshift=13,
                                       font=dict(size=11, color=BLEU_FONCE))
                habiller(fig, 240, yaxis=dict(autorange="reversed", dtick=1, range=[8.5, 0.2], gridcolor="#efece4"))
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

pied()
