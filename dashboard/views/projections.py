"""Page 9 — Estimations et projections : « Où va le Togo si l’on agit, et si rien ne change ? »
(plan visuel, section 9). Prolongements linéaires, déclarés comme ordres de grandeur, jamais comme des prévisions."""
import html

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from composants import ariane, carte_kpi, constat, entete, export_csv, limite, note, pct, pied, rangee_kpi
from donnees import lire, nombre
from i18n import bi, langue, t, valeur
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
couv = lire("07_indicateurs", "o2_06_couverture")
r1 = lire("10_recommandations", "r1_communes_mobile_money_uniquement")
r2 = lire("10_recommandations", "r2_prefectures_points_formels")
r3 = lire("10_recommandations", "r3_maillage_mobile_money")
r4a = lire("10_recommandations", "r4_communes_a_mesurer")
r5 = lire("10_recommandations", "r5_frais_mobile_money").iloc[0]
r7 = lire("10_recommandations", "r7_competences").set_index("region")
r7b = lire("10_recommandations", "r7b_equipement").iloc[0]
r9 = lire("10_recommandations", "r9_fibre_non_raccordees")
r10 = lire("10_recommandations", "r10_sites_radio").iloc[0]
REPERE_SITES = 50  # ajouts nets de sites radio par an (seuil de veille déclaré, P26 du 10)

# Libellés en clair des scénarios et des repères (les tables les écrivent en français seulement : correction C13)
SCENARIO = {"accéléré (moyenne 2019-2024)": bi("accéléré (rythme moyen de 2019-2024)", "accelerated (2019-2024 average pace)"),
            "ambitieux (années d'accélération 2016 et 2020)": bi("ambitieux (rythme des années d’accélération, 2016 et 2020)",
                                                                 "ambitious (pace of the acceleration years, 2016 and 2020)"),
            "tendanciel (moyenne 2023-2024)": bi("tendanciel (rythme de 2023-2024)", "trend (2023-2024 pace)")}
TERRITOIRE = {"Togo": "Togo", "Afrique subsaharienne": bi("Afrique subsaharienne", "Sub-Saharan Africa"),
              "UEMOA, médiane des 8 pays": bi("UEMOA, médiane des 8 pays", "WAEMU, median of the 8 countries")}
couv_c = couv[couv.maille == "commune"]
couvertes = couv_c[couv_c.classe_02 == "territoire couvert (proxy)"]

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
        (t("lib.couverture_theorique").capitalize(),
         bi(f"{len(couvertes)} communes sur {len(couv_c)} couvertes à plus de 85 % ({nombre(couvertes.pop_totale.sum() / 1e6, 2)} millions d’habitants, 2021/2022)",
            f"{len(couvertes)} communes out of {len(couv_c)} covered above 85% ({nombre(couvertes.pop_totale.sum() / 1e6, 2)} million people, 2021/2022)"),
         bi("pas de projection : un seul point de mesure", "no projection: a single data point"),
         bi(f"l’extension prévue ferait entrer {nombre(couv_total)} habitants de plus dans la couverture", f"the planned extension would bring {nombre(couv_total)} more people into coverage")),
    ]
    df92 = pd.DataFrame(lignes, columns=[bi("indicateur", "indicator"), bi("dernière valeur", "latest value"),
                                        bi("2030 au rythme actuel", "2030 at current pace"), bi("lecture", "reading")])
    st.table(df92.set_index(bi("indicateur", "indicator")))  # des phrases : tableau statique, le texte revient à la ligne

st.write("")
gauche, droite = st.columns([1.2, 1], gap="large")

# ----------------------------------------------------------------- 9.3 Scénarios
with gauche:
    with st.container(border=True):
        st.markdown(f'<div class="bloc-titre">{html.escape(bi("Scénarios d’usage d’Internet à 2030", "Internet use scenarios to 2030"))}</div>', unsafe_allow_html=True)
        # Une couleur par scénario, dans l’ordre fixe de la table : décocher un scénario ne repeint pas les autres
        couleur_sc = {sc: CATEGORIELLE[k % len(CATEGORIELLE)] for k, sc in enumerate(r8s.scenario)}
        lib_sc = {sc: SCENARIO.get(sc, sc) for sc in r8s.scenario}
        choix_lib = st.multiselect(bi("Scénarios affichés", "Scenarios shown"), list(lib_sc.values()), default=list(lib_sc.values()),
                                   key=f"proj_scenarios_{langue()}", placeholder=bi("Tous", "All"))
        choix = [sc for sc, lib in lib_sc.items() if lib in choix_lib]
        obs = usage.loc[2010:a_u]
        fig = go.Figure()
        fig.add_scatter(x=obs.index, y=obs.pct_population, mode="lines", name=bi("Observé", "Observed"), line=dict(color=ENCRE, width=3))
        for sc in choix:
            su = r8u[r8u.scenario == sc]
            fig.add_scatter(x=su.annee, y=su.pct_population, mode="lines", name=lib_sc[sc], line=dict(color=couleur_sc[sc], width=2, dash="dot"))
        fig.add_hline(y=40, line=dict(color="#8a1c1b", width=1, dash="dash"), annotation_text=bi("40 %", "40%"))
        fig.add_hline(y=60, line=dict(color="#0d366b", width=1, dash="dash"), annotation_text=bi("60 %", "60%"))
        fig.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
                          font=dict(family="IBM Plex Sans, system-ui, sans-serif", color=ENCRE), separators=", " if langue() == "fr" else ".,",
                          legend=dict(orientation="h", y=1.22, x=0), yaxis=dict(ticksuffix=" %", gridcolor="#efece4"), xaxis=dict(gridcolor="#efece4"))
        st.plotly_chart(fig, key="scenarios_usage", config={"displayModeBar": False})
        export_csv(r8u, "scenarios_usage.csv", "export_scenarios")
        st.table(pd.DataFrame({bi("scénario", "scenario"): r8s.scenario.map(lib_sc), bi("points par an", "points a year"): r8s.points_par_an.map(lambda v: nombre(v, 2)),
                               bi("en 2030", "in 2030"): r8s.pct_2030.map(lambda v: pct(v)), bi("60 % atteint en", "60% reached in"): r8s.annee_60pct.astype(int).astype(str),
                               bi("classe en 2030", "class in 2030"): r8s.classe_2030.map(valeur)}).set_index(bi("scénario", "scenario")))

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
            fig2.add_bar(x=[TERRITOIRE.get(row.territoire, row.territoire)], y=[row.valeur], name=bi("Aujourd’hui", "Today"), marker_color=CATEGORIELLE[0],
                        showlegend=(i == 0), width=0.35, offsetgroup="a")
            fig2.add_bar(x=[TERRITOIRE.get(row.territoire, row.territoire)], y=[row.valeur_2030], name="2030", marker_color=CATEGORIELLE[1],
                        showlegend=(i == 0), width=0.35, offsetgroup="b")
        fig2.update_layout(barmode="group", height=260, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="#ffffff",
                          plot_bgcolor="#ffffff", font=dict(family="IBM Plex Sans, system-ui, sans-serif", color=ENCRE, size=11),
                          legend=dict(orientation="h", y=1.15, x=0), yaxis=dict(ticksuffix=" %", gridcolor="#efece4"))
        st.plotly_chart(fig2, key="trajectoires", config={"displayModeBar": False})
        export_csv(r8t, "trajectoires_reference.csv", "export_trajectoires")

# ----------------------------------------------------------------- 9.4 Suivi des cibles (O5-04 ; item 22 du relevé)
# Base = dernier millésime ; cible = seuil de la classe supérieure ; réussite = franchissement du seuil (10, section 7). Les
# chiffres viennent des tables des recommandations ; la page montre les actions, jamais leurs numéros (correction C14).
st.write("")
with st.container(border=True):
    st.markdown(f'<div class="bloc-titre">{html.escape(bi("Suivi des cibles", "Target tracking"))}</div>'
                f'<div class="bloc-sous-titre">{html.escape(bi("Situation d’aujourd’hui, cible, horizon et ce qui dira que c’est réussi. Suivi annuel.", "Today’s situation, target, horizon and what will show success. Tracked yearly."))}</div>',
                unsafe_allow_html=True)
    r2_fini = r2[r2.hab_par_point_formel != float("inf")]
    r2_sans = r2[r2.hab_par_point_formel == float("inf")]
    r3c, r3p = r3[r3.maille == "commune"], r3[r3.maille == "préfecture"]
    r3_dense, r3_med = r3p[r3p.cible == "dense"], r3p[r3p.cible == "médiane des préfectures"]
    r4b_p1 = r4c[r4c.classe_08 == "priorité 1"]
    kpi = lambda v, d=0: nombre(v, d)
    suivi = [
        (bi("Une première agence financière", "A first financial branch"), bi(f"{len(r1)} communes sans agence", f"{len(r1)} communes with no branch"),
         bi("aucune agence (2021/2022)", "no branch (2021/2022)"), bi("au moins une agence", "at least one branch"), valeur("1 an"),
         bi("la commune quitte « mobile money seul »", "the commune leaves “mobile money only”")),
        (bi("Des agences dans ces communes", "Branches in these communes"), bi("les mêmes communes", "the same communes"), bi("aucune agence", "no branch"),
         bi(f"30 000 habitants par agence au plus ({int(r1.points_cible_3ans_tendu.sum())} agences)", f"30,000 people per branch at most ({int(r1.points_cible_3ans_tendu.sum())} branches)"),
         valeur("3 ans"), bi("la commune devient « tendue »", "the commune becomes “stretched”")),
        (bi("Des agences dans les préfectures prioritaires", "Branches in priority prefectures"), bi(f"{len(r2)} préfectures", f"{len(r2)} prefectures"),
         bi(f"{kpi(r2_fini.hab_par_point_formel.min())} à {kpi(r2_fini.hab_par_point_formel.max())} habitants par agence ; {', '.join(r2_sans.nom)} : aucune agence",
            f"{kpi(r2_fini.hab_par_point_formel.min())} to {kpi(r2_fini.hab_par_point_formel.max())} people per branch; {', '.join(r2_sans.nom)}: no branch"),
         bi(f"« tendu » pour {int((r2.cible == 'tendu').sum())}, « bien desservi » pour {int((r2.cible == 'bien desservi').sum())} ({int(r2.points_a_ajouter.sum())} agences)",
            f"“stretched” for {int((r2.cible == 'tendu').sum())}, “well served” for {int((r2.cible == 'bien desservi').sum())} ({int(r2.points_a_ajouter.sum())} branches)"),
         valeur("3 ans"), bi("la préfecture franchit son seuil", "the prefecture crosses its threshold")),
        (bi("Des points mobile money", "Mobile money points"), ", ".join(r3c.nom),
         bi(f"{kpi(r3c.hab_par_point_mm.min())} à {kpi(r3c.hab_par_point_mm.max())} habitants par point", f"{kpi(r3c.hab_par_point_mm.min())} to {kpi(r3c.hab_par_point_mm.max())} people per point"),
         bi("5 000 au plus", "5,000 at most"), valeur("3 ans"), bi("la commune devient « acceptable »", "the commune becomes “acceptable”")),
        (bi("Des points mobile money", "Mobile money points"), ", ".join(r3_dense.nom),
         bi(f"{kpi(r3_dense.hab_par_point_mm.min())} à {kpi(r3_dense.hab_par_point_mm.max())} habitants par point", f"{kpi(r3_dense.hab_par_point_mm.min())} to {kpi(r3_dense.hab_par_point_mm.max())} people per point"),
         bi("moins de 1 000", "under 1,000"), valeur("3 ans"), bi("la préfecture devient « dense »", "the prefecture becomes “dense”")),
        (bi("Des points mobile money", "Mobile money points"), ", ".join(r3_med.nom),
         bi(f"{kpi(r3_med.hab_par_point_mm.min())} à {kpi(r3_med.hab_par_point_mm.max())} habitants par point", f"{kpi(r3_med.hab_par_point_mm.min())} to {kpi(r3_med.hab_par_point_mm.max())} people per point"),
         bi(f"{r3_med.seuil_habitants_par_point.iloc[0]} (médiane des préfectures)", f"{r3_med.seuil_habitants_par_point.iloc[0]} (prefectures’ median)"), valeur("3 ans"),
         bi("la médiane est atteinte", "the median is reached")),
        (bi("Mesurer la couverture réelle", "Measure actual coverage"), bi(f"{len(r4a)} communes", f"{len(r4a)} communes"), bi("inconnue ou douteuse", "unknown or doubtful"),
         bi("une couverture mesurée", "a measured coverage"), valeur("1 an"), bi("la valeur est connue", "the value is known")),
        (bi("Étendre le réseau", "Extend the network"), bi(f"{len(r4b_p1)} préfectures en priorité haute", f"{len(r4b_p1)} high-priority prefectures"),
         bi(f"{pct(r4b_p1.couverture_proxy_pct.min())} à {pct(r4b_p1.couverture_proxy_pct.max())} (estimation, 2021/2022)",
            f"{pct(r4b_p1.couverture_proxy_pct.min())} to {pct(r4b_p1.couverture_proxy_pct.max())} (estimate, 2021/2022)"),
         bi("50 % (Kéran), 85 % (les autres)", "50% (Kéran), 85% (the others)"), valeur("5 ans"), bi("seuil franchi, sur la couverture réelle", "threshold crossed, on actual coverage")),
        (bi("Frais du petit retrait", "Small-withdrawal fees"), bi("national", "national"),
         bi(f"{pct(r5.frais_pct)} pour 1 000 FCFA (grille du 26/09/2026)", f"{pct(r5.frais_pct)} for 1,000 FCFA (grid of 26/09/2026)"),
         bi(f"{pct(r5.repere_pct, 0)} au plus", f"{pct(r5.repere_pct, 0)} at most"), valeur("5 ans"),
         bi(f"des frais de {kpi(r5.frais_cible_fcfa)} FCFA au plus", f"fees of {kpi(r5.frais_cible_fcfa)} FCFA at most")),
        (bi("Prix de la data", "Data price"), bi("national", "national"), bi(f"{pct(r6.base_2025_pct, 2)} du revenu mensuel (2025)", f"{pct(r6.base_2025_pct, 2)} of monthly income (2025)"),
         bi(f"{pct(r6.cible_pct, 0)} au plus", f"{pct(r6.cible_pct, 0)} at most"), valeur("5 ans"), bi("le seuil d’accessibilité est franchi", "the affordability threshold is crossed")),
        (bi("Compétences numériques", "Digital skills"), "Savanes, Plateaux",
         bi(f"alphabétisation : {pct(r7.loc['Savanes', 'alphabetisation_pct'])} dans les Savanes (2021/22)", f"literacy: {pct(r7.loc['Savanes', 'alphabetisation_pct'])} in Savanes (2021/22)"),
         bi("au-dessus du quart le plus bas", "above the bottom quarter"), valeur("5 ans"), bi("la région sort du quart le plus bas", "the region leaves the bottom quarter")),
        (bi("Équipement en smartphone", "Smartphone equipment"), bi("national", "national"),
         bi(f"{pct(r7b.sans_smartphone_cause_cout_pct)} des adultes sans smartphone pour raison de coût (2024)", f"{pct(r7b.sans_smartphone_cause_cout_pct)} of adults without a smartphone because of cost (2024)"),
         bi("une baisse (pas de seuil)", "a decrease (no threshold)"), valeur("5 ans"), bi("la baisse est mesurée à la prochaine enquête", "the decrease is measured in the next survey")),
        (bi("Investissement des opérateurs", "Operators’ investment"), bi("national", "national"), bi(f"{pct(r8i.base_2025_pct)} du chiffre d’affaires (2025)", f"{pct(r8i.base_2025_pct)} of revenue (2025)"),
         bi(f"{pct(r8i.seuil_sous_investissement_pct, 0)} au moins", f"at least {pct(r8i.seuil_sous_investissement_pct, 0)}"), valeur("chaque année"),
         bi("il reste au-dessus du seuil", "it stays above the threshold")),
        (bi("Fibre", "Fibre"), bi(f"{len(r9)} préfectures", f"{len(r9)} prefectures"), bi("aucune fibre recensée (2021/2022)", "no recorded fibre (2021/2022)"),
         bi("de la fibre recensée", "recorded fibre"), valeur("5 ans"), bi("fibre recensée dans la préfecture", "fibre recorded in the prefecture")),
        (bi("Sites radio", "Radio sites"), bi("national", "national"), bi(f"{int(r10.ajouts_nets_2025)} ajoutés (2025)", f"{int(r10.ajouts_nets_2025)} added (2025)"),
         bi(f"{REPERE_SITES} au moins par an", f"at least {REPERE_SITES} a year"), valeur("1 à 3 ans"),
         bi("pas deux années de suite sous le repère", "not two years in a row below the reference")),
        (bi("Usage d’Internet (résultat attendu, pas une action)", "Internet use (expected outcome, not an action)"), bi("national", "national"),
         bi(f"{pct(usage.loc[a_u, 'pct_population'], 2)} ({a_u}, estimation)", f"{pct(usage.loc[a_u, 'pct_population'], 2)} ({a_u}, estimate)"),
         bi("40 %, puis 60 %", "40%, then 60%"), bi(f"2025 ; 2028 à {int(tendanciel.annee_60pct)}", f"2025; 2028 to {int(tendanciel.annee_60pct)}"),
         bi("changement de classe", "change of class")),
    ]
    st.table(pd.DataFrame(suivi, columns=[bi("action", "action"), bi("où", "where"), bi("aujourd’hui", "today"), bi("cible", "target"),
                                          bi("horizon", "horizon"), bi("réussi si", "success if")]).set_index(bi("action", "action")))
    note(bi("La cible est le seuil de la classe supérieure : c’est lui qui dit quand l’action a produit son effet.",
            "The target is the next class’s threshold: it tells when the action has had its effect."))
    export_csv(s.reset_index(), "cibles.csv", "export_cibles")

limite(bi("Les prolongements sont linéaires : ce sont des ordres de grandeur, pas des prévisions. Aucune donnée ne dit quelle action "
         "produit quel rythme : les événements passés sont des coïncidences, pas des causes. Le coût de 1 Go n’a que trois points "
         "de série (2023 à 2025). La série d’usage du Togo est une estimation internationale.",
         "The projections are linear: they are orders of magnitude, not forecasts. No data says which action produces which pace: "
         "past events are coincidences, not causes. The cost of 1 GB only has three data points (2023 to 2025). Togo’s usage series "
         "is an international estimate."))
pied()
