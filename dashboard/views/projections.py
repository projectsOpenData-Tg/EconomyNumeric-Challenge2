"""Page 9 — Estimations et projections : « Où va le Togo si l’on agit, et si rien ne change ? »
(plan visuel, section 9). Prolongements linéaires, déclarés comme ordres de grandeur, jamais comme des prévisions."""
import html

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from composants import ariane, carte_kpi, constat, entete, export_csv, limite, pied, rangee_kpi
from donnees import lire, nombre
from i18n import bi, langue, t
from theme import CATEGORIELLE, ENCRE

FR = langue() == "fr"
usage = lire("07_indicateurs", "o1_02_usage").set_index("annee")
r6 = lire("10_recommandations", "r6_cout_data").iloc[0]
r8i = lire("10_recommandations", "r8_investissement").iloc[0]
r8s = lire("10_recommandations", "r8_scenarios_synthese")
r8u = lire("10_recommandations", "r8_scenarios_usage")
r8t = lire("10_recommandations", "r8_trajectoires_reference")
r4c = lire("10_recommandations", "r4_couverture")
s = lire("10_recommandations", "synthese_recommandations").set_index("id")
c1go = lire("07_indicateurs", "o2_05b_cout_1go").set_index("annee")

a_u = int(usage.index.max())
tendanciel = r8s[r8s.scenario.str.contains("2023")].iloc[0] if len(r8s[r8s.scenario.str.contains("2023")]) else r8s.iloc[0]

ariane(t("page.projections"))
entete(t("page.projections"), bi("Où va le Togo si l’on agit, et si rien ne change ?", "Where is Togo headed if it acts, and if nothing changes?"),
       bi(f"Au rythme actuel, l’usage d’Internet atteint <strong>{nombre(tendanciel.pct_2030, 1)} %</strong> en 2030 ; le seuil de 60 % "
          f"attend {int(tendanciel.annee_60pct)}.",
          f"At the current pace, Internet use reaches <strong>{nombre(tendanciel.pct_2030, 1)}%</strong> by 2030; the 60% threshold "
          f"waits until {int(tendanciel.annee_60pct)}."))

# ----------------------------------------------------------------- 9.1 Chiffres clés
rangee_kpi(bi("Aujourd’hui, au rythme actuel, cible", "Today, at the current pace, target"), [
    carte_kpi(bi(f"Usage d’Internet ({a_u})", f"Internet use ({a_u})"), f"{nombre(usage.loc[a_u,'pct_population'], 2)} %",
              bi(f"au rythme actuel : {nombre(tendanciel.pct_2030, 1)} % en 2030", f"at the current pace: {nombre(tendanciel.pct_2030, 1)}% by 2030"),
              bi(f"cible : 60 % (usage généralisé), vers {int(tendanciel.annee_60pct)} au rythme actuel", f"target: 60% (widespread use), around {int(tendanciel.annee_60pct)} at the current pace"),
              "", None, "neutre"),
    carte_kpi(bi(f"Coût de 1 Go ({int(c1go.index[-1])})", f"Cost of 1 GB ({int(c1go.index[-1])})"), f"{nombre(r6.base_2025_pct, 2)} %",
              bi(f"au rythme actuel : {nombre(r6.valeur_2030_au_rythme_actuel, 1)} % en 2030", f"at the current pace: {nombre(r6.valeur_2030_au_rythme_actuel, 1)}% by 2030"),
              bi(f"cible : {nombre(r6.cible_pct, 0)} %, vers {int(r6.annee_cible_au_rythme_actuel)} au rythme actuel",
                 f"target: {nombre(r6.cible_pct, 0)}%, around {int(r6.annee_cible_au_rythme_actuel)} at the current pace"),
              "", None, "neutre"),
    carte_kpi(bi("Investissement des opérateurs", "Operators' investment"), f"{nombre(r8i.base_2025_pct, 1)} %",
              bi("pas de projection : série cyclique", "no projection: cyclical series"),
              bi(f"seuil d’alerte : {nombre(r8i.seuil_sous_investissement_pct, 0)} % au moins", f"alert threshold: at least {nombre(r8i.seuil_sous_investissement_pct, 0)}%"),
              "", None, "ok" if r8i.base_2025_pct >= r8i.seuil_sous_investissement_pct else "alerte"),
])

st.write("")

# ----------------------------------------------------------------- 9.2 Où va-t-on si rien ne change
with st.container(border=True):
    st.markdown(f'<div class="bloc-titre">{html.escape(bi("Où va-t-on si rien ne change ?", "Where are we headed if nothing changes?"))}</div>', unsafe_allow_html=True)
    # R4b ne porte que sur les 6 préfectures déjà prioritaires (P24) : Sotouboua (priorité 2) reste hors extension, mesurée par R4a
    couv_total = int(r4c[r4c.classe_08 == "priorité 1"].pop_a_couvrir_pour_la_cible.sum())
    lignes = [
        (bi("Usage d’Internet", "Internet use"), f"{nombre(usage.loc[a_u,'pct_population'],2)} % ({a_u})", f"{nombre(tendanciel.pct_2030,1)} %",
         bi(f"seuil de 40 % franchi dès 2025 ; 60 % attend {int(tendanciel.annee_60pct)}", f"40% threshold crossed by 2025; 60% waits until {int(tendanciel.annee_60pct)}")),
        (bi("Coût de 1 Go", "Cost of 1 GB"), f"{nombre(r6.base_2025_pct,2)} % ({int(c1go.index[-1])})", f"{nombre(r6.valeur_2030_au_rythme_actuel,1)} %",
         bi(f"pour 2 % en 2030, il faudrait aller {nombre(r6.multiple_du_rythme_actuel,1)} fois plus vite", f"reaching 2% by 2030 would need {nombre(r6.multiple_du_rythme_actuel,1)}× the current pace")),
        (bi("Investissement", "Investment"), f"{nombre(r8i.base_2025_pct,1)} % (2025)", bi("pas de projection", "no projection"),
         bi(f"série cyclique ; si la baisse récente se répétait : {nombre(r8i.valeur_2026_si_la_variation_2024_2025_se_repete,1)} % en 2026, sous le seuil",
            f"cyclical series; if the recent drop repeated: {nombre(r8i.valeur_2026_si_la_variation_2024_2025_se_repete,1)}% in 2026, below threshold")),
        (t("lib.couverture_theorique").capitalize(), bi("88,4 % (recensement 2021/2022)", "88.4% (2021/2022 survey)"), bi("pas de projection : un seul point de mesure", "no projection: a single data point"),
         bi(f"l’extension prévue ferait entrer {nombre(couv_total)} habitants de plus dans la couverture", f"the planned extension would bring {nombre(couv_total)} more people into coverage")),
    ]
    df92 = pd.DataFrame(lignes, columns=[bi("indicateur", "indicator"), bi("dernière valeur", "latest value"),
                                        bi("2030 au rythme actuel", "2030 at current pace"), bi("lecture", "reading")])
    st.dataframe(df92, hide_index=True, use_container_width=True)

st.write("")
gauche, droite = st.columns([1.2, 1], gap="large")

# ----------------------------------------------------------------- 9.3 Scénarios
with gauche:
    with st.container(border=True):
        st.markdown(f'<div class="bloc-titre">{html.escape(bi("Scénarios d’usage d’Internet à 2030", "Internet use scenarios to 2030"))}</div>', unsafe_allow_html=True)
        lib_scenario = {}
        for sc in r8s.scenario.unique():
            lib_scenario[sc] = sc  # noms déjà déclaratifs (tendanciel, accéléré, ambitieux), gardés tels quels
        choix = st.multiselect(bi("Scénarios affichés", "Scenarios shown"), list(r8s.scenario), default=list(r8s.scenario),
                               key="proj_scenarios", placeholder=bi("Tous", "All"))
        obs = usage.loc[2010:a_u]
        fig = go.Figure()
        fig.add_scatter(x=obs.index, y=obs.pct_population, mode="lines", name=bi("Observé", "Observed"), line=dict(color=ENCRE, width=3))
        for i, sc in enumerate(choix):
            su = r8u[r8u.scenario == sc]
            fig.add_scatter(x=su.annee, y=su.pct_population, mode="lines", name=sc, line=dict(color=CATEGORIELLE[i % len(CATEGORIELLE)], width=2, dash="dot"))
        fig.add_hline(y=40, line=dict(color="#8a1c1b", width=1, dash="dash"), annotation_text=bi("40 %", "40%"))
        fig.add_hline(y=60, line=dict(color="#0d366b", width=1, dash="dash"), annotation_text=bi("60 %", "60%"))
        fig.update_layout(height=360, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
                          font=dict(family="IBM Plex Sans, system-ui, sans-serif", color=ENCRE),
                          legend=dict(orientation="h", y=1.15, x=0), yaxis=dict(ticksuffix=" %", gridcolor="#efece4"), xaxis=dict(gridcolor="#efece4"))
        st.plotly_chart(fig, key="scenarios_usage", config={"displayModeBar": False})
        export_csv(r8u, "scenarios_usage.csv", "export_scenarios")
        st.dataframe(r8s.rename(columns={"scenario": bi("scénario", "scenario"), "points_par_an": bi("points par an", "points a year"),
                                         "pct_2030": bi("usage en 2030 (%)", "use in 2030 (%)"), "annee_60pct": bi("60 % atteint en", "60% reached in"),
                                         "classe_2030": bi("classe en 2030", "class in 2030")}),
                    hide_index=True, use_container_width=True)

with droite:
    constat(bi("Le seuil de 40 % est à portée dès 2025 ; au rythme actuel, l’usage généralisé (60 %) attend "
              f"{int(tendanciel.annee_60pct)}.",
              f"The 40% threshold is within reach by 2025; at the current pace, widespread use (60%) waits until {int(tendanciel.annee_60pct)}."))

    with st.container(border=True):
        st.markdown(f'<div class="bloc-titre">{html.escape(bi("Trajectoires de référence", "Reference trajectories"))}</div>'
                    f'<div class="bloc-sous-titre">{html.escape(bi("Même règle que le scénario tendanciel du Togo : moyenne des deux dernières variations annuelles.", "Same rule as Togo’s trend scenario: average of the last two annual changes."))}</div>',
                    unsafe_allow_html=True)
        fig2 = go.Figure()
        for i, row in r8t.reset_index().iterrows():
            fig2.add_bar(x=[row.territoire], y=[row.valeur], name=bi("Aujourd’hui", "Today"), marker_color=CATEGORIELLE[0],
                        showlegend=(i == 0), width=0.35, offsetgroup="a")
            fig2.add_bar(x=[row.territoire], y=[row.valeur_2030], name="2030", marker_color=CATEGORIELLE[1],
                        showlegend=(i == 0), width=0.35, offsetgroup="b")
        fig2.update_layout(barmode="group", height=260, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="#ffffff",
                          plot_bgcolor="#ffffff", font=dict(family="IBM Plex Sans, system-ui, sans-serif", color=ENCRE, size=11),
                          legend=dict(orientation="h", y=1.15, x=0), yaxis=dict(ticksuffix=" %", gridcolor="#efece4"))
        st.plotly_chart(fig2, key="trajectoires", config={"displayModeBar": False})
        export_csv(r8t, "trajectoires_reference.csv", "export_trajectoires")

# ----------------------------------------------------------------- 9.4 Cibles
st.write("")
with st.container(border=True):
    st.markdown(f'<div class="bloc-titre">{html.escape(bi("Cibles à 1, 3 et 5 ans", "1-, 3- and 5-year targets"))}</div>', unsafe_allow_html=True)
    tab94 = s.reset_index()[["id", "recommandation", "cible", "horizon"]].rename(columns={
        "id": bi("id", "id"), "recommandation": bi("action", "action"), "cible": bi("cible", "target"), "horizon": bi("horizon", "horizon")})
    st.dataframe(tab94, hide_index=True, use_container_width=True)
    export_csv(s.reset_index(), "cibles.csv", "export_cibles")

limite(bi("Les prolongements sont linéaires : ce sont des ordres de grandeur, pas des prévisions. Aucune donnée ne dit quelle action "
         "produit quel rythme : les événements passés sont des coïncidences, pas des causes. Le coût de 1 Go n’a que trois points "
         "de série (2023 à 2025). La série d’usage du Togo est une estimation de l’UIT.",
         "The projections are linear: they are orders of magnitude, not forecasts. No data says which action produces which pace: "
         "past events are coincidences, not causes. The cost of 1 GB only has three data points (2023 to 2025). Togo’s usage series "
         "is an ITU estimate."))
pied()
