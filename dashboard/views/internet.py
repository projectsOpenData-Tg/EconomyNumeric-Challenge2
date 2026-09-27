"""Page 2 — Internet : usage et marché : « L’usage progresse-t-il, et à quel prix ? » (plan visuel, section 7, page 2).

Usage d’Internet (série, croissance annuelle, événements) ; accès déclaré par région ; marché des télécommunications
(duopole, chiffre d’affaires, investissement, sites radio) ; prix de la data ; fibre. Chiffres nationaux : les filtres
de région et de milieu n’y changent rien (mention affichée, comme sur la Synthèse) ; le tableau régional répond au
filtre de région.
"""
import html

import plotly.graph_objects as go
import streamlit as st

from composants import ariane, constat, entete, export_csv, limite, pied, rangee_kpi, carte_kpi
from donnees import lire, nombre
from i18n import bi, langue, region, t
from theme import CATEGORIELLE, ENCRE, PRIORITE

FR = langue() == "fr"
f_regions = st.session_state.f_regions

pen = lire("07_indicateurs", "o1_01_penetration").set_index("annee")
usage = lire("07_indicateurs", "o1_02_usage").set_index("annee")
acces = lire("07_indicateurs", "o1_05_acces_regions")
hhi = lire("07_indicateurs", "o2_01_parts_hhi")
ca = lire("07_indicateurs", "o2_03_ca")
inv = lire("07_indicateurs", "o2_04_investissement")
c1go = lire("07_indicateurs", "o2_05b_cout_1go").set_index("annee")
fibre = lire("07_indicateurs", "o2_07_fibre_prefectures")
sites = lire("07_indicateurs", "o2_08_sites_radio")
freins = lire("07_indicateurs", "o1_06_freins")
r6 = lire("10_recommandations", "r6_cout_data").iloc[0]

a_u = int(usage.index.max())
u_now, u_prev = usage.loc[a_u, "pct_population"], usage.loc[a_u - 1, "pct_population"]
inv_now = inv.iloc[-1]
c1go_now = c1go.iloc[-1]
acces_now = acces[acces.vague == acces.vague.max()].set_index("unite_regionale")
gl_pct, sav_pct = acces_now.loc["Grand Lomé", "estimation_pct"], acces_now.loc["Savanes", "estimation_pct"]
sans_fibre = fibre[fibre.raccorde_02 == "non raccordé"]

# ----------------------------------------------------------------- En-tête
ariane(t("page.internet"))
entete(t("page.internet"), bi("L’usage progresse-t-il, et à quel prix ?", "Is use growing, and at what cost?"),
       bi(f"L’usage ralentit depuis 2021 : <strong>{nombre(u_now, 1)} %</strong> en {a_u}, contre {nombre(u_prev, 1)} % l’an d’avant. "
          f"1 Go coûte <strong>{nombre(c1go_now.cout_pct_revenu_mensuel, 2)} %</strong> du revenu mensuel.",
          f"Use has slowed since 2021: <strong>{nombre(u_now, 1)}%</strong> in {a_u}, against {nombre(u_prev, 1)}% the year before. "
          f"1 GB costs <strong>{nombre(c1go_now.cout_pct_revenu_mensuel, 2)}%</strong> of monthly income."))
st.markdown(f'<div class="filtres-actifs">{html.escape(bi("Chiffres nationaux : ils ne changent pas avec les filtres de région et de milieu. Le tableau régional répond au filtre de région.", "National figures: they do not change with the region and area-type filters. The regional table responds to the region filter."))}</div>',
            unsafe_allow_html=True)

# ----------------------------------------------------------------- Chiffres clés
rangee_kpi(bi("Internet et marché", "Internet and market"), [
    carte_kpi(bi(f"Usage d’Internet ({a_u})", f"Internet use ({a_u})"), f"{nombre(u_now, 1)} %",
              bi("de la population utilise Internet", "of the population uses the Internet"),
              bi(f"Afrique subsaharienne : {nombre(pen.loc[a_u, 'afrique_subsaharienne_pct'], 1)} %",
                 f"Sub-Saharan Africa: {nombre(pen.loc[a_u, 'afrique_subsaharienne_pct'], 1)}%"),
              bi("Estimation internationale (UIT).", "International estimate (ITU)."),
              bi("Seuil franchi", "Threshold reached") if u_now >= 40 else bi("Sous le seuil", "Below threshold"),
              "ok" if u_now >= 40 else "alerte"),
    carte_kpi(bi("Accès déclaré, écart régional", "Self-reported access, regional gap"), f"{nombre(sav_pct, 1)} %",
              bi(f"dans les Savanes, contre {nombre(gl_pct, 1)} % dans le Grand Lomé", f"in Savanes, against {nombre(gl_pct, 1)}% in Greater Lomé"),
              bi(f"enquête EHCVM, {acces_now.loc['Savanes'].vague}", "EHCVM survey, 2021/22"),
              t("lib.acces_declare") + bi(" : pas la même mesure que l’usage d’Internet ci-dessus.", ": not the same measure as Internet use above."),
              bi("Écart régional", "Regional gap"), "critique"),
    carte_kpi(bi(f"Prix de la data ({int(c1go.index[-1])})", f"Data price ({int(c1go.index[-1])})"),
              f"{nombre(c1go_now.cout_pct_revenu_mensuel, 2)} %", bi("du revenu mensuel pour 1 Go", "of monthly income for 1 GB"),
              bi(f"seuil : 2 % ; au rythme récent, atteint vers {int(r6.annee_cible_au_rythme_actuel)}",
                 f"threshold: 2%; at the recent pace, reached around {int(r6.annee_cible_au_rythme_actuel)}"),
              bi("Revenu moyen, pas médian.", "Average income, not median."), bi("Non abordable", "Not affordable"), "alerte"),
    carte_kpi(bi(f"Investissement ({int(inv_now.annee)})", f"Investment ({int(inv_now.annee)})"),
              f"{nombre(inv_now.taux_investissement_pct, 1)} %", bi("du chiffre d’affaires des opérateurs", "of operators' revenue"),
              bi("seuil d’alerte : 15 % ; série cyclique", "alert threshold: 15%; cyclical series"),
              bi("Mesure en valeur (FCFA) ; O2-08 la complète en volume (sites radio).", "Measured in value (FCFA); O2-08 complements it in volume (radio sites)."),
              inv_now.classe_02.replace("cycle d’extension", bi("Cycle d’extension", "Extension cycle")).replace(
                  "régime normal", bi("Régime normal", "Normal regime")), "ok" if inv_now.taux_investissement_pct >= 15 else "alerte"),
])

st.write("")
gauche, droite = st.columns([1.25, 1], gap="large")

# ----------------------------------------------------------------- Visuel principal : usage + événements
with gauche:
    with st.container(border=True):
        st.markdown(f'<div class="bloc-titre">{html.escape(bi("L’usage d’Internet depuis 2010", "Internet use since 2010"))}</div>'
                    f'<div class="bloc-sous-titre">{html.escape(bi("Estimation UIT, avec le repère de l’Afrique subsaharienne et le seuil de 40 %.", "ITU estimate, with the Sub-Saharan Africa reference and the 40% threshold."))}</div>',
                    unsafe_allow_html=True)
        pen10 = pen.loc[2010:]
        fig = go.Figure()
        fig.add_scatter(x=pen10.index, y=pen10.pct_population, mode="lines", name=bi("Togo", "Togo"),
                        line=dict(color=PRIORITE["haute"], width=3))
        fig.add_scatter(x=pen10.index, y=pen10.afrique_subsaharienne_pct, mode="lines", name=bi("Afrique subsaharienne", "Sub-Saharan Africa"),
                        line=dict(color="#b9b6ad", width=2, dash="dot"))
        fig.add_hline(y=40, line=dict(color="#8a1c1b", width=1, dash="dash"),
                     annotation_text=bi("Seuil de 40 %", "40% threshold"), annotation_position="bottom right")
        # Événements retenus (5), comme des coïncidences temporelles, pas des causes (limite affichée sous le graphique)
        evenements = [(2016, bi("3G de Moov (commerciale)", "Moov 3G (commercial)")),
                     (2018, bi("4G lancée à Lomé", "4G launched in Lomé")),
                     (2020, bi("Covid-19 ; 5G Togocom (novembre)", "Covid-19; Togocom 5G (November)")),
                     (2022, bi("Câble sous-marin Equiano", "Equiano submarine cable")),
                     (2023, bi("Baisse des forfaits Moov (-71 %)", "Moov plan prices cut (-71%)"))]
        for an, lib in evenements:
            fig.add_vline(x=an, line=dict(color="#cde2fb", width=1))
            fig.add_annotation(x=an, y=pen10.pct_population.max() + 6, text=lib, showarrow=False, textangle=-90,
                              font=dict(size=9, color="#55534e"), xanchor="left", yanchor="top")
        fig.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font=dict(family="IBM Plex Sans, system-ui, sans-serif", color=ENCRE),
                          legend=dict(orientation="h", y=1.12, x=0), yaxis=dict(ticksuffix=" %", gridcolor="#efece4"),
                          xaxis=dict(gridcolor="#efece4"))
        st.plotly_chart(fig, key="courbe_usage", config={"displayModeBar": False})

        st.markdown(f'<div class="bloc-titre" style="margin-top:1rem;">{html.escape(bi("Croissance annuelle", "Annual growth"))}</div>', unsafe_allow_html=True)
        u10 = usage.loc[2011:]
        couleur_classe = {"accélération": "#0d366b", "rythme habituel": "#86b6ef", "ralentissement": "#eda100"}
        lib_classe = {"accélération": bi("accélération", "acceleration"), "rythme habituel": bi("rythme habituel", "usual pace"),
                     "ralentissement": bi("ralentissement", "slowdown")}
        fig2 = go.Figure()
        for cl, coul in couleur_classe.items():
            sub = u10[u10.classe == cl]
            fig2.add_bar(x=sub.index, y=sub.variation_points, name=lib_classe[cl], marker_color=coul)
        fig2.update_layout(height=220, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font=dict(family="IBM Plex Sans, system-ui, sans-serif", color=ENCRE, size=11),
                          legend=dict(orientation="h", y=1.15, x=0), yaxis=dict(ticksuffix=" pts", gridcolor="#efece4"),
                          xaxis=dict(gridcolor="#efece4"), bargap=0.3)
        st.plotly_chart(fig2, key="croissance_usage", config={"displayModeBar": False})
        export_csv(u10.reset_index()[["annee", "pct_population", "variation_points", "classe"]], "usage_internet.csv", "export_usage")

with droite:
    constat(bi("L’usage ralentit depuis 2021 ; les Savanes cumulent l’accès le plus faible et l’alphabétisation la plus faible.",
               "Use has slowed since 2021; Savanes combines the lowest access with the lowest literacy rate."))

    with st.container(border=True):
        st.markdown(f'<div class="bloc-titre">{html.escape(bi("Accès déclaré, marché, prix", "Self-reported access, market, price"))}</div>', unsafe_allow_html=True)
        acces_2 = acces[acces.vague == acces.vague.max()].copy()
        acces_2["surlignee"] = acces_2.unite_regionale.isin(f_regions) if f_regions else True
        acces_2 = acces_2.sort_values("estimation_pct", ascending=True)
        fig3 = go.Figure()
        fig3.add_bar(x=acces_2.estimation_pct, y=[region(r) for r in acces_2.unite_regionale], orientation="h",
                    marker_color=[PRIORITE["haute"] if s else "#cde2fb" for s in acces_2.surlignee],
                    text=[f"{nombre(v,1)} %" for v in acces_2.estimation_pct], textposition="outside")
        fig3.update_layout(height=210, margin=dict(l=10, r=30, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font=dict(family="IBM Plex Sans, system-ui, sans-serif", color=ENCRE, size=11),
                          xaxis=dict(ticksuffix=" %", gridcolor="#efece4", range=[0, 80]), showlegend=False)
        st.plotly_chart(fig3, key="acces_regions", config={"displayModeBar": False})
        export_csv(acces_2[["unite_regionale", "estimation_pct", "ic95_bas", "ic95_haut"]], "acces_regions.csv", "export_acces_regions")

    with st.container(border=True):
        st.markdown(f'<div class="bloc-titre">{html.escape(bi("Marché : parts et concentration", "Market: shares and concentration"))}</div>', unsafe_allow_html=True)
        dernier = hhi[hhi.segment.str.contains("data", case=False)].sort_values("annee").iloc[-1]
        st.markdown(f'<div class="reponse">{html.escape(bi(f"Togocom (YAS) : {nombre(dernier.part_togocom_pct,1)} % des abonnés data ; Moov : {nombre(dernier.part_moov_pct,1)} %. Indice de concentration : {nombre(dernier.hhi,0)} ({dernier.classe_02}).", f"Togocom (YAS): {nombre(dernier.part_togocom_pct,1)}% of data subscribers; Moov: {nombre(dernier.part_moov_pct,1)}%. Concentration index: {nombre(dernier.hhi,0)} ({dernier.classe_02})."))}</div>',
                    unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(f'<div class="bloc-titre">{html.escape(bi("Sites radio (déploiement physique)", "Radio sites (physical deployment)"))}</div>'
                    f'<div class="bloc-sous-titre">{html.escape(bi("Ajouts nets par an, par opérateur ; repère de veille à 50.", "Net additions per year, by operator; watch reference at 50."))}</div>',
                    unsafe_allow_html=True)
        s4 = sites[sites.annee >= 2022]
        fig4 = go.Figure()
        fig4.add_bar(x=s4.annee, y=s4.ajouts_nets_moov, name="Moov Africa", marker_color=CATEGORIELLE[0])
        fig4.add_bar(x=s4.annee, y=s4.ajouts_nets_yas, name="YAS", marker_color=CATEGORIELLE[1])
        fig4.add_hline(y=50, line=dict(color="#8a1c1b", width=1, dash="dash"),
                      annotation_text=bi("Seuil de veille : 50", "Watch threshold: 50"), annotation_position="top left")
        fig4.update_layout(barmode="stack", height=220, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)",
                          plot_bgcolor="rgba(0,0,0,0)", font=dict(family="IBM Plex Sans, system-ui, sans-serif", color=ENCRE, size=11),
                          legend=dict(orientation="h", y=1.18, x=0), yaxis=dict(gridcolor="#efece4"), xaxis=dict(gridcolor="#efece4", dtick=1))
        st.plotly_chart(fig4, key="sites_radio", config={"displayModeBar": False})
        st.caption(bi(f"Les ajouts nets tombent de {int(sites.loc[sites.annee==2022,'ajouts_nets_total'].iloc[0])} à "
                     f"{int(sites.loc[sites.annee==2025,'ajouts_nets_total'].iloc[0])} en trois ans ; {int(sites.annee.max())} est la "
                     "première année sous le seuil de veille.",
                     f"Net additions fall from {int(sites.loc[sites.annee==2022,'ajouts_nets_total'].iloc[0])} to "
                     f"{int(sites.loc[sites.annee==2025,'ajouts_nets_total'].iloc[0])} in three years; {int(sites.annee.max())} is the "
                     "first year below the watch threshold."))
        export_csv(sites, "sites_radio.csv", "export_sites_radio")

st.write("")
with st.container(border=True):
    st.markdown(f'<div class="bloc-titre">{html.escape(bi("Fibre : préfectures non raccordées", "Fibre: unconnected prefectures"))}</div>', unsafe_allow_html=True)
    tab = sans_fibre[["nom", "unite_regionale", "pop_totale"]].rename(columns={
        "nom": bi("préfecture", "prefecture"), "unite_regionale": bi("région", "region"), "pop_totale": bi("habitants", "population")})
    tab[bi("région", "region")] = tab[bi("région", "region")].map(region)
    st.dataframe(tab, hide_index=True, use_container_width=True)
    export_csv(sans_fibre[["nom", "unite_regionale", "pop_totale"]], "fibre_non_raccordees.csv", "export_fibre")

limite(bi("Série d’usage estimée (UIT), pas mesurée directement. L’accès déclaré (EHCVM) n’est pas l’usage : ce sont deux mesures "
         "différentes. Les événements annotés sont des coïncidences temporelles, pas des causes démontrées. Le marché est mesuré au "
         "national seulement ; un site radio compte une fois, quelle que soit sa technologie.",
         "The usage series is estimated (ITU), not directly measured. Self-reported access (EHCVM) is not usage: they are two "
         "different measures. The annotated events are temporal coincidences, not demonstrated causes. The market is measured "
         "nationally only; a radio site counts once, whatever its technology."))
pied()
