"""Page 8 — Recommandations : « Quelle action engager ? » (plan visuel, section 8).

Refaite le 29/09/2026 (relevé des objectifs 4 et 5, `workspace/conding-progress.md`, étape 2) : quatre sous-onglets.
« Les 12 actions » (filtres, vue d’ensemble sans addition de populations qui se recoupent, une carte par action) ; « Par
thème » (les territoires visés par chaque thème, leur situation et ce qu’il faut ajouter : plan 11, section 8.3) ; « Par
territoire » (toutes les actions d’une préfecture : section 8.4) ; « Ordre d’action et acteurs ».

La page montre les titres, jamais les numéros des recommandations (plan 11, section 8). Les textes des tables du 10 (cible,
territoires) sont réécrits dans le vocabulaire des décideurs et traduits ; les chiffres viennent des tables.
"""
import html

import pandas as pd
import streamlit as st

from composants import (ariane, carte_priorites, colorer_regions, constat, entete, export_csv, formater, limite, note, onglets,
                        pct, pied, titre_bloc)
from donnees import communes, contours, lire, nombre, prefectures
from i18n import bi, region, t, valeur

s = lire("10_recommandations", "synthese_recommandations").set_index("id")
r1 = lire("10_recommandations", "r1_communes_mobile_money_uniquement")
r2 = lire("10_recommandations", "r2_prefectures_points_formels")
r3 = lire("10_recommandations", "r3_maillage_mobile_money")
r4a = lire("10_recommandations", "r4_communes_a_mesurer")
r4b = lire("10_recommandations", "r4_couverture")
r5 = lire("10_recommandations", "r5_frais_mobile_money").iloc[0]
r6 = lire("10_recommandations", "r6_cout_data").iloc[0]
r7 = lire("10_recommandations", "r7_competences")
r7b = lire("10_recommandations", "r7b_equipement").iloc[0]
r8 = lire("10_recommandations", "r8_investissement").iloc[0]
r9 = lire("10_recommandations", "r9_fibre_non_raccordees")
r10 = lire("10_recommandations", "r10_sites_radio").iloc[0]
C, P = communes(), prefectures()
REPERE_SITES = 50  # ajouts nets de sites radio par an (seuil de veille déclaré, P26 du 10)

og, fg = bi("« ", "“"), bi(" »", "”")
r4b_p1 = r4b[r4b.classe_08 == "priorité 1"]
r3p, r3c = r3[r3.maille == "préfecture"], r3[r3.maille == "commune"]

THEME = {"R1": "formels", "R2": "formels", "R3": "mm", "R4a": "couverture", "R4b": "couverture", "R5": "prix",
         "R6": "prix", "R7": "competences", "R7b": "competences", "R8": "investissement", "R9": "fibre", "R10": "investissement"}
LIB_THEME = {"formels": bi("Agences financières", "Financial branches"), "mm": bi("Mobile money", "Mobile money"),
             "couverture": bi("Couverture réseau", "Network coverage"), "fibre": bi("Fibre", "Fibre"),
             "prix": bi("Prix et frais", "Price and fees"), "competences": bi("Compétences et équipement", "Skills and equipment"),
             "investissement": bi("Investissement (veille)", "Investment (watch)")}
EMOJI_THEME = {"formels": "🏦", "mm": "📱", "couverture": "📡", "fibre": "🌐", "prix": "💰", "competences": "🎓", "investissement": "📈"}
TITRE = {
    "R1": bi(f"Une première agence financière dans chacune des {len(r1)} communes où le mobile money est seul",
             f"A first financial branch in each of the {len(r1)} communes where mobile money is the only option"),
    "R2": bi(f"Des agences financières dans les {len(r2)} préfectures prioritaires", f"Financial branches in the {len(r2)} priority prefectures"),
    "R3": bi("Des points mobile money là où le réseau est mince", "Mobile money points where the network is thin"),
    "R4a": bi(f"Mesurer la couverture réelle dans {len(r4a)} communes", f"Measure actual coverage in {len(r4a)} communes"),
    "R4b": bi(f"Étendre le réseau dans {len(r4b_p1)} préfectures prioritaires", f"Extend the network in {len(r4b_p1)} priority prefectures"),
    "R5": bi("Ramener les frais du petit retrait sous 3 %", "Bring small-withdrawal fees below 3%"),
    "R6": bi("Ramener le coût de 1 Go sous 2 % du revenu", "Bring the cost of 1 GB below 2% of income"),
    "R7": bi("Relever les compétences numériques dans les Savanes et les Plateaux", "Raise digital skills in Savanes and Plateaux"),
    "R7b": bi("Réduire le frein de coût sur le smartphone", "Reduce the smartphone cost barrier"),
    "R8": bi("Garder l’investissement au-dessus de 15 % du chiffre d’affaires", "Keep investment above 15% of revenue"),
    "R9": bi(f"Étendre la fibre aux {len(r9)} préfectures sans fibre recensée", f"Extend fibre to the {len(r9)} prefectures with no recorded fibre"),
    "R10": bi("Relancer les ajouts de sites radio", "Revive radio-site additions"),
}
CIBLE = {
    "R1": bi(f"{len(r1)} agences, une par commune ; {int(r1.points_cible_3ans_tendu.sum())} à 3 ans pour passer sous 30 000 habitants par agence",
             f"{len(r1)} branches, one per commune; {int(r1.points_cible_3ans_tendu.sum())} within 3 years to get below 30,000 people per branch"),
    "R2": bi(f"{int(r2.points_a_ajouter.sum())} agences, dont {int(r2.dont_points_R1.sum())} apportées par les communes sans agence",
             f"{int(r2.points_a_ajouter.sum())} branches, {int(r2.dont_points_R1.sum())} of them from the communes with no branch"),
    "R3": bi(f"{nombre(int(r3p.points_a_ajouter.sum()))} points mobile money dans les préfectures ; {int(r3c.points_a_ajouter.sum())} dans les communes au maillage insuffisant",
             f"{nombre(int(r3p.points_a_ajouter.sum()))} mobile money points in the prefectures; {int(r3c.points_a_ajouter.sum())} in the communes with an insufficient network"),
    "R4a": bi("une couverture connue dans chaque commune", "a known coverage in every commune"),
    "R4b": bi(f"{nombre(int(r4b_p1.pop_a_couvrir_pour_la_cible.sum()))} habitants de plus dans la couverture théorique",
              f"{nombre(int(r4b_p1.pop_a_couvrir_pour_la_cible.sum()))} more people in theoretical coverage"),
    "R5": bi(f"retrait de 1 000 FCFA : de {nombre(r5.frais_fcfa)} à {nombre(r5.frais_cible_fcfa)} FCFA au plus",
             f"1,000 FCFA withdrawal: from {nombre(r5.frais_fcfa)} to {nombre(r5.frais_cible_fcfa)} FCFA at most"),
    "R6": bi(f"de {pct(r6.base_2025_pct, 2)} à {pct(r6.cible_pct, 0)} du revenu mensuel : une baisse de {pct(r6.baisse_relative_necessaire_pct, 0)} à revenu constant",
             f"from {pct(r6.base_2025_pct, 2)} to {pct(r6.cible_pct, 0)} of monthly income: a {pct(r6.baisse_relative_necessaire_pct, 0)} drop at constant income"),
    "R7": bi("sortir du quart des régions les moins alphabétisées et les moins compétentes", "leave the bottom quarter of regions for literacy and skills"),
    "R7b": bi(f"moins d’adultes sans smartphone pour raison de coût ({pct(r7b.sans_smartphone_cause_cout_pct)} aujourd’hui)",
              f"fewer adults without a smartphone because of cost ({pct(r7b.sans_smartphone_cause_cout_pct)} today)"),
    "R8": bi(f"au moins {pct(r8.seuil_sous_investissement_pct, 0)} du chiffre d’affaires investi ({pct(r8.base_2025_pct)} en 2025)",
             f"at least {pct(r8.seuil_sous_investissement_pct, 0)} of revenue invested ({pct(r8.base_2025_pct)} in 2025)"),
    "R9": bi("de la fibre recensée dans chaque préfecture", "recorded fibre in every prefecture"),
    "R10": bi(f"au moins {REPERE_SITES} sites radio ajoutés par an ({int(r10.ajouts_nets_2025)} en 2025)",
              f"at least {REPERE_SITES} radio sites added a year ({int(r10.ajouts_nets_2025)} in 2025)"),
}
TERRITOIRES = {
    "R1": bi(f"{len(r1)} communes sans agence", f"{len(r1)} communes with no branch"),
    "R2": bi(f"{len(r2)} préfectures prioritaires", f"{len(r2)} priority prefectures"),
    "R3": bi(f"{len(r3p)} préfectures et {len(r3c)} communes", f"{len(r3p)} prefectures and {len(r3c)} communes"),
    "R4a": bi(f"{len(r4a)} communes", f"{len(r4a)} communes"),
    "R4b": bi(f"{len(r4b_p1)} préfectures en priorité haute", f"{len(r4b_p1)} high-priority prefectures"),
    "R5": bi("national ; d’abord là où le mobile money est seul", "national; first where mobile money is the only option"),
    "R6": bi("national", "national"), "R7": "Savanes, Plateaux", "R7b": bi("national", "national"), "R8": bi("national", "national"),
    "R9": bi(f"{len(r9)} préfectures", f"{len(r9)} prefectures"),
    "R10": bi("national ; d’abord les zones blanches", "national; white zones first"),
}
PRIO_BADGE = {"R1": t("priorite.absolue"), "R2": t("priorite.haute"), "R3": t("priorite.haute"), "R4a": bi("Préalable", "Prerequisite"),
              "R4b": t("priorite.haute"), "R5": bi("National", "National"), "R6": bi("National", "National"),
              "R7": t("priorite.haute"), "R7b": bi("National", "National"), "R8": bi("National", "National"),
              "R9": t("priorite.haute"), "R10": bi("National", "National")}


def seuil(txt: str) -> str:
    """« 30 000 ou moins » → « 30 000 or less » en anglais."""
    return (str(txt).replace(" ou moins", bi(" ou moins", " or less")).replace(" ou plus", bi(" ou plus", " or more"))
            .replace("moins de ", bi("moins de ", "under ")).replace(" %", bi(" %", "%")))


def prio_prefecture(v) -> str:
    return valeur(v)


ariane(t("page.recommandations"))
entete(t("page.recommandations"), bi("Quelle action engager ?", "What action to take?"),
       bi(f"<strong>{len(s)} recommandations</strong>, en 7 thèmes, de l’agence financière manquante au prix de la data.",
          f"<strong>{len(s)} recommendations</strong>, across 7 themes, from the missing financial branch to the price of data."))

LIBELLES = [bi("Les 12 actions", "The 12 actions"), bi("Par thème", "By theme"), bi("Par territoire", "By territory"),
            bi("Ordre d’action et acteurs", "Order of action and actors")]
o_actions, o_theme, o_territoire, o_ordre = onglets("recommandations_onglets", LIBELLES)

# =================================================================== 1. Les 12 actions
if o_actions.open is not False:
    with o_actions:
        themes_dispo = sorted(set(LIB_THEME[v] for v in THEME.values()))
        c1, c2, c3 = st.columns(3)
        choisir = bi("Tous", "All")
        f_theme = c1.multiselect(bi("Thème", "Theme"), themes_dispo, key="reco_theme", placeholder=choisir)
        f_nature = c2.multiselect(bi("Nature", "Nature"), sorted(set(s.nature.map(valeur))), key="reco_nature", placeholder=choisir)
        f_horizon = c3.multiselect(bi("Horizon", "Horizon"), list(dict.fromkeys(s.horizon.map(valeur))), key="reco_horizon", placeholder=choisir)
        sf = s.copy()
        sf["theme_lib"] = [LIB_THEME[THEME[i]] for i in sf.index]
        if f_theme:
            sf = sf[sf.theme_lib.isin(f_theme)]
        if f_nature:
            sf = sf[sf.nature.map(valeur).isin(f_nature)]
        if f_horizon:
            sf = sf[sf.horizon.map(valeur).isin(f_horizon)]

        # Vue d’ensemble : jamais d’addition d’habitants qui se recoupent
        n22 = int(C.priorite_absolue.sum())
        pop22 = int(C[C.priorite_absolue].pop_totale.sum())
        p1 = P[P.priorite == "haute"]
        st.markdown(f'<div class="filtres-actifs">'
                    f'{len(sf)} {bi("recommandations", "recommendations")} · '
                    f'{n22} {bi("communes en priorité absolue", "absolute-priority communes")} ({nombre(pop22)} {bi("habitants", "people")}) · '
                    f'{len(r2)} {bi("préfectures prioritaires", "priority prefectures")} ({nombre(int(r2.pop_totale.sum()))} {bi("habitants", "people")}) · '
                    f'{int((s.nature == "conditionnelle").sum())} {bi("action conditionnelle", "conditional action")} · '
                    f'{int((s.nature == "veille").sum())} {bi("veilles", "watch items")}</div>', unsafe_allow_html=True)
        st.caption(bi("Les habitants ne sont jamais additionnés d’une recommandation à l’autre : les territoires se recoupent.",
                      "People are never added up from one recommendation to another: territories overlap."))
        st.write("")
        cols = st.columns(3)
        for i, (idx, row) in enumerate(sf.iterrows()):
            with cols[i % 3]:
                with st.container(border=True, key=f"carte_reco_{idx}"):
                    th = THEME[idx]
                    st.markdown(f'<div class="reco-theme theme-{th}"><span class="reco-pastille">{EMOJI_THEME[th]}</span>'
                                f'<span class="reco-theme-lib">{html.escape(row.theme_lib)}</span></div>'
                                f'<div class="action-titre" style="min-height:3.4rem">{html.escape(TITRE[idx])}</div>'
                                f'<div class="kpi-phrase" style="margin:6px 0">{html.escape(CIBLE[idx])}</div>'
                                f'<div class="kpi-contexte">{html.escape(TERRITOIRES[idx])} · {nombre(int(row.population)).replace(" ", "&nbsp;")} {bi("habitants concernés", "people concerned")}</div>'
                                f'<div class="action-meta reco-meta">'
                                f'<span class="etiquette {"critique" if idx == "R1" else "reco-priorite"}">{html.escape(PRIO_BADGE[idx])}</span>'
                                f'<span class="etiquette reco-nature">{html.escape(valeur(row.nature))}</span>'
                                f'<span class="etiquette reco-horizon">{html.escape(valeur(row.horizon))}</span></div>', unsafe_allow_html=True)
        export_csv(sf.reset_index()[["id", "territoires", "population", "nature", "horizon", "cible"]], "recommandations.csv", "export_recos")
        limite(bi("Des ordres de grandeur, pas des devis : les cibles viennent des seuils des classes, pas d’un calcul de coût. Les habitants "
                  "concernés sont ceux du territoire visé, pas un gain.",
                  "Orders of magnitude, not quotes: targets come from class thresholds, not from a cost calculation. The people concerned "
                  "are those of the targeted territory, not a gain."))

# =================================================================== 2. Par thème
if o_theme.open is not False:
    with o_theme:
        cles = list(LIB_THEME)
        th = st.segmented_control(bi("Thème", "Theme"), cles, format_func=lambda k: f"{EMOJI_THEME[k]} {LIB_THEME[k]}", default="formels",
                                  key="reco_vue_theme") or "formels"
        c_reg = bi("région", "region")
        if th == "formels":
            constat(html.escape(bi(f"D’abord une agence dans chacune des {len(r1)} communes où le mobile money est seul ; puis, dans les "
                                   f"{len(r2)} préfectures prioritaires, assez d’agences pour passer la classe supérieure.",
                                   f"First a branch in each of the {len(r1)} communes where mobile money is the only option; then, in the "
                                   f"{len(r2)} priority prefectures, enough branches to move up a class.")))
            with st.container(border=True):
                titre_bloc(TITRE["R1"], bi("Ordre d’action : par population ; la distance à l’agence la plus proche est à côté.",
                                          "Order of action: by population; the distance to the nearest branch is alongside."))
                d = r1.sort_values("ordre_action")
                st.dataframe(formater(pd.DataFrame({bi("ordre", "order"): d.ordre_action.astype(int), bi("commune", "commune"): d.nom,
                                           bi("préfecture", "prefecture"): d.prefecture, bi("priorité de la préfecture", "prefecture priority"): d.classe_prefecture_08.map(prio_prefecture),
                                           bi("habitants", "people"): d.pop_totale.astype(int), bi("points mobile money", "mobile money points"): d.n_mm.astype(int),
                                           bi("agence la plus proche (km)", "nearest branch (km)"): d.km_guichet_mediane,
                                           bi("agences à 1 an", "branches in 1 year"): d.points_cible_1an_sortir_du_statut.astype(int),
                                           bi("à 3 ans", "in 3 years"): d.points_cible_3ans_tendu.astype(int)})),
                             hide_index=True, use_container_width=True, height=330)
                export_csv(r1, "communes_premiere_agence.csv", "export_r1")
            with st.container(border=True):
                titre_bloc(TITRE["R2"], bi("Cible : la classe supérieure (30 000 habitants par agence au plus, ou moins de 10 000).",
                                          "Target: the next class up (30,000 people per branch at most, or under 10,000)."))
                st.dataframe(formater(pd.DataFrame({bi("préfecture", "prefecture"): r2.nom, bi("priorité", "priority"): r2.classe_08.map(prio_prefecture),
                                           bi("habitants", "people"): r2.pop_totale.astype(int),
                                           bi("agences (dont banques)", "branches (of which banks)"): [f"{int(a)} ({int(b)})" for a, b in zip(r2.n_formels, r2.n_banque)],
                                           bi("habitants par agence", "people per branch"): [bi("aucune agence", "no branch") if pd.isna(v) or v == float("inf") else nombre(v, 0) for v in r2.hab_par_point_formel],
                                           bi("cible", "target"): [f"{valeur(c)} ({seuil(sv)})" for c, sv in zip(r2.cible, r2.seuil_habitants_par_point)],
                                           bi("agences à ajouter", "branches to add"): r2.points_a_ajouter.astype(int),
                                           bi("dont communes", "from communes"): r2.dont_points_R1.astype(int)})),
                             hide_index=True, use_container_width=True)
                export_csv(r2, "prefectures_agences.csv", "export_r2")
        elif th == "mm":
            constat(html.escape(bi("Là où un point mobile money sert trop d’habitants, en ajouter jusqu’au seuil de la classe supérieure, ou jusqu’à la "
                                   "médiane des préfectures.", "Where one mobile money point serves too many people, add some up to the next class "
                                   "threshold, or up to the prefectures’ median.")))
            with st.container(border=True):
                titre_bloc(TITRE["R3"])
                d = r3
                st.dataframe(formater(pd.DataFrame({bi("territoire", "territory"): [f"{n} ({bi('commune', 'commune') if m == 'commune' else bi('préfecture', 'prefecture')})" for n, m in zip(d.nom, d.maille)],
                                           bi("habitants", "people"): d.pop_totale.astype(int), bi("points mobile money", "mobile money points"): d.n_mm.astype(int),
                                           bi("habitants par point", "people per point"): d.hab_par_point_mm.round(0),
                                           bi("aujourd’hui", "today"): d.classe_O4_04.map(valeur), bi("cible (habitants par point)", "target (people per point)"): d.seuil_habitants_par_point.map(seuil),
                                           bi("points à ajouter", "points to add"): d.points_a_ajouter.astype(int)})),
                             hide_index=True, use_container_width=True)
                note(bi("La médiane des préfectures (602 habitants par point) est un ordre de grandeur, pas une norme.",
                        "The prefectures’ median (602 people per point) is an order of magnitude, not a standard."))
                export_csv(r3, "maillage_mobile_money.csv", "export_r3")
        elif th == "couverture":
            constat(html.escape(bi("D’abord mesurer la couverture réelle là où l’estimation est inconnue ou douteuse ; ensuite seulement, étendre "
                                   "le réseau dans les préfectures prioritaires.", "First measure actual coverage where the estimate is unknown or "
                                   "doubtful; only then extend the network in priority prefectures.")))
            g, d_ = st.columns(2, gap="large")
            with g:
                with st.container(border=True):
                    titre_bloc(TITRE["R4a"])
                    st.dataframe(colorer_regions(pd.DataFrame({bi("commune", "commune"): r4a.nom, c_reg: r4a.unite_regionale.map(region),
                                                               bi("habitants", "people"): r4a.pop_totale.astype(int),
                                                               bi("couverture estimée (%)", "estimated coverage (%)"): r4a.couverture_proxy_pct.round(1),
                                                               bi("douteuse", "doubtful"): r4a.valeur_douteuse_P6.map(lambda x: bi("oui", "yes") if x is True or x == "True" else "")}), c_reg),
                                 hide_index=True, use_container_width=True, height=330)
                    note(bi("Couverture vide : inconnue. « Douteuse » : sous 10 % alors que des points mobile money fonctionnent.",
                            "Empty coverage: unknown. “Doubtful”: below 10% although mobile money points operate."))
            with d_:
                with st.container(border=True):
                    titre_bloc(TITRE["R4b"], bi("Action conditionnelle : après la mesure.", "Conditional action: after the measurement."))
                    st.dataframe(formater(pd.DataFrame({bi("préfecture", "prefecture"): r4b_p1.nom, bi("habitants", "people"): r4b_p1.pop_totale.astype(int),
                                               bi("couverture estimée (%)", "estimated coverage (%)"): r4b_p1.couverture_proxy_pct.round(1),
                                               bi("cible", "target"): r4b_p1.cible.map(seuil),
                                               bi("habitants à couvrir", "people to cover"): r4b_p1.pop_a_couvrir_pour_la_cible.astype(int)})),
                                 hide_index=True, use_container_width=True)
            export_csv(r4b, "couverture_prefectures.csv", "export_r4")
        elif th == "fibre":
            constat(html.escape(bi(f"{len(r9)} préfectures n’ont aucune fibre recensée, ni enterrée ni aérienne.",
                                   f"{len(r9)} prefectures have no recorded fibre, neither buried nor aerial.")))
            with st.container(border=True):
                titre_bloc(TITRE["R9"])
                st.dataframe(colorer_regions(pd.DataFrame({bi("préfecture", "prefecture"): r9.nom, c_reg: r9.unite_regionale.map(region),
                                                           bi("priorité", "priority"): r9.classe_08.map(prio_prefecture),
                                                           bi("habitants", "people"): r9.pop_totale.astype(int),
                                                           bi("superficie (km²)", "area (km²)"): r9.superficie_km2.round(0).astype(int)}), c_reg),
                             hide_index=True, use_container_width=True)
                note(bi("Une longueur de câble recensée n’est pas un raccordement à domicile.", "A recorded cable length is not a home connection."))
                export_csv(r9, "prefectures_sans_fibre.csv", "export_r9")
        elif th == "prix":
            with st.container(border=True):
                titre_bloc(TITRE["R5"])
                note(bi(f"Retirer 1 000 FCFA chez un agent coûte {nombre(r5.frais_fcfa)} FCFA ({pct(r5.frais_pct)}) ; le repère est {pct(r5.repere_pct, 0)} : "
                        f"{nombre(r5.frais_cible_fcfa)} FCFA au plus, une baisse de {pct(r5.baisse_necessaire_pct, 0)}. {nombre(int(r5.pop_communes_mm_uniquement_ou_dominant))} "
                        "habitants vivent là où le mobile money est seul ou dominant.",
                        f"Withdrawing 1,000 FCFA at an agent costs {nombre(r5.frais_fcfa)} FCFA ({pct(r5.frais_pct)}); the reference is {pct(r5.repere_pct, 0)}: "
                        f"{nombre(r5.frais_cible_fcfa)} FCFA at most, a {pct(r5.baisse_necessaire_pct, 0)} drop. {nombre(int(r5.pop_communes_mm_uniquement_ou_dominant))} "
                        "people live where mobile money is alone or dominant."), forte=True)
                note(bi("La grille de retrait de YAS (Mixx) n’est pas publiée : l’indicateur ne porte que sur Moov Africa (Flooz).",
                        "YAS (Mixx) does not publish its withdrawal grid: the indicator only covers Moov Africa (Flooz)."))
            with st.container(border=True):
                titre_bloc(TITRE["R6"])
                note(bi(f"1 Go coûte {pct(r6.base_2025_pct, 2)} du revenu mensuel ; au rythme récent, 2 % serait atteint vers {int(r6.annee_cible_au_rythme_actuel)}. "
                        f"Pour y être en 2030, il faudrait aller {nombre(r6.multiple_du_rythme_actuel, 1)} fois plus vite.",
                        f"1 GB costs {pct(r6.base_2025_pct, 2)} of monthly income; at the recent pace, 2% would be reached around {int(r6.annee_cible_au_rythme_actuel)}. "
                        f"To get there by 2030, the pace would have to be {nombre(r6.multiple_du_rythme_actuel, 1)} times faster."), forte=True)
        elif th == "competences":
            with st.container(border=True):
                titre_bloc(TITRE["R7"], bi("Adultes de 15 ans et plus ; « repère » : le quart des régions le plus bas.",
                                          "Adults aged 15 and over; “reference”: the bottom quarter of regions."))
                st.dataframe(colorer_regions(pd.DataFrame({c_reg: r7.region.map(region), bi("adultes", "adults"): r7.pop15.astype(int),
                                                           bi("alphabétisation (%)", "literacy (%)"): r7.alphabetisation_pct.round(1),
                                                           bi("repère (%)", "reference (%)"): r7.seuil_quartile_alphabetisation.round(1),
                                                           bi("compétences, femmes (%)", "skills, women (%)"): r7["competences_Femmes 15-49 ans"],
                                                           bi("compétences, hommes (%)", "skills, men (%)"): r7["competences_Hommes 15-49 ans"]}), c_reg),
                             hide_index=True, use_container_width=True)
                note(bi("Compétences : 15-49 ans, enquête de 2017 ; l’alphabétisation n’est qu’un indice des compétences.",
                        "Skills: aged 15-49, 2017 survey; literacy is only a proxy for skills."))
            with st.container(border=True):
                titre_bloc(TITRE["R7b"])
                note(bi(f"{pct(r7b.smartphone_telephone_principal_pct)} des adultes ont un smartphone comme téléphone principal ; "
                        f"{pct(r7b.sans_smartphone_cause_cout_pct)} citent le coût pour ne pas en avoir ({nombre(int(r7b.adultes_citant_le_cout))} adultes). "
                        "Aucun seuil : le suivi porte sur la baisse de cette part.",
                        f"{pct(r7b.smartphone_telephone_principal_pct)} of adults use a smartphone as their main phone; {pct(r7b.sans_smartphone_cause_cout_pct)} "
                        f"cite cost for not having one ({nombre(int(r7b.adultes_citant_le_cout))} adults). No threshold: tracking covers the drop in this share."), forte=True)
        else:
            with st.container(border=True):
                titre_bloc(TITRE["R8"])
                note(bi(f"{pct(r8.base_2025_pct)} du chiffre d’affaires investi en 2025, à {nombre(r8.marge_points, 1)} point du seuil de "
                        f"{pct(r8.seuil_sous_investissement_pct, 0)}. Si la baisse de 2024-2025 se répétait : {pct(r8.valeur_2026_si_la_variation_2024_2025_se_repete)} "
                        "en 2026, sous le seuil ; la décision prévue serait alors un mécanisme de financement (fonds du service universel).",
                        f"{pct(r8.base_2025_pct)} of revenue invested in 2025, {nombre(r8.marge_points, 1)} points above the {pct(r8.seuil_sous_investissement_pct, 0)} "
                        f"threshold. If the 2024-2025 drop repeated: {pct(r8.valeur_2026_si_la_variation_2024_2025_se_repete)} in 2026, below the threshold; "
                        "the planned decision would then be a funding mechanism (universal service fund)."), forte=True)
            with st.container(border=True):
                titre_bloc(TITRE["R10"])
                note(bi(f"Sites radio ajoutés : {int(r10.ajouts_nets_2022)} en 2022, {int(r10.ajouts_nets_2023)} en 2023, {int(r10.ajouts_nets_2024)} en 2024, "
                        f"{int(r10.ajouts_nets_2025)} en 2025, pour un repère de {REPERE_SITES} par an. Deux années de suite sous le repère : un « gel » à constater.",
                        f"Radio sites added: {int(r10.ajouts_nets_2022)} in 2022, {int(r10.ajouts_nets_2023)} in 2023, {int(r10.ajouts_nets_2024)} in 2024, "
                        f"{int(r10.ajouts_nets_2025)} in 2025, against a reference of {REPERE_SITES} a year. Two years in a row below it: a “freeze” to be noted."), forte=True)
        limite(bi("Les cibles sont les seuils des classes supérieures ; les nombres à ajouter sont des ordres de grandeur. Tous les territoires "
                  "prioritaires ne sont pas couverts par un même thème.",
                  "Targets are the next classes’ thresholds; numbers to add are orders of magnitude. Not every priority territory is "
                  "covered by the same theme."))

# =================================================================== 3. Par territoire
if o_territoire.open is not False:
    with o_territoire:
        pref_r1 = dict(zip(r1.nom, r1.prefecture))
        com_pref = dict(zip(C.code, C.prefecture))
        touchees = list(dict.fromkeys(list(r2.nom) + list(r3p.nom) + list(r3c.prefecture) + list(r4b_p1.nom) + list(r9.nom) + list(r1.prefecture)))
        choix = st.selectbox(bi("Préfecture", "Prefecture"), touchees, key="reco_territoire")
        info = P[P.nom == choix].iloc[0]
        region_choix = info.unite_regionale
        lignes = []
        c1 = r1[r1.prefecture == choix]
        if len(c1):
            lignes.append((LIB_THEME["formels"], bi(f"une agence dans chacune de : {', '.join(c1.nom)} (priorité absolue)",
                                                    f"a branch in each of: {', '.join(c1.nom)} (absolute priority)"),
                           bi("sortir de « mobile money seul »", "leave “mobile money only”"), "immédiate", "1 an"))
        c2 = r2[r2.nom == choix]
        if len(c2):
            x = c2.iloc[0]
            na, nc = int(x.points_a_ajouter), int(x.dont_points_R1)
            lignes.append((LIB_THEME["formels"], bi(f"+{na} agence{'s' if na > 1 else ''}" + (f", dont {nc} apportée{'s' if nc > 1 else ''} par les communes" if nc else ""),
                                                    f"+{na} branch{'es' if na > 1 else ''}" + (f", {nc} of them from the communes" if nc else "")),
                           f"{valeur(x.cible)} ({seuil(x.seuil_habitants_par_point)})", "immédiate", "3 ans"))
        for _, x in pd.concat([r3p[r3p.nom == choix], r3c[r3c.prefecture == choix]]).iterrows():
            ou = "" if x.maille == "préfecture" else f" ({x.nom})"
            lignes.append((LIB_THEME["mm"], bi(f"+{int(x.points_a_ajouter)} points mobile money{ou}", f"+{int(x.points_a_ajouter)} mobile money points{ou}"),
                           bi(f"{seuil(x.seuil_habitants_par_point)} habitants par point", f"{seuil(x.seuil_habitants_par_point)} people per point"), "immédiate", "3 ans"))
        c4a = r4a[r4a.code.map(com_pref) == choix]
        if len(c4a):
            lignes.append((LIB_THEME["couverture"], bi(f"mesurer la couverture réelle : {', '.join(c4a.nom)}", f"measure actual coverage: {', '.join(c4a.nom)}"),
                           bi("une couverture connue", "a known coverage"), "immédiate", "1 an"))
        c4b = r4b_p1[r4b_p1.nom == choix]
        if len(c4b):
            x = c4b.iloc[0]
            lignes.append((LIB_THEME["couverture"], bi(f"+{nombre(int(x.pop_a_couvrir_pour_la_cible))} habitants dans la couverture",
                                                       f"+{nombre(int(x.pop_a_couvrir_pour_la_cible))} people in coverage"), seuil(x.cible), "conditionnelle", "5 ans"))
        if choix in set(r9.nom):
            lignes.append((LIB_THEME["fibre"], bi("étendre la fibre", "extend fibre"), bi("de la fibre recensée", "recorded fibre"), "immédiate", "5 ans"))
        if region_choix in set(r7.region):
            lignes.append((LIB_THEME["competences"], bi(f"compétences numériques (région {region(region_choix)})", f"digital skills ({region(region_choix)} region)"),
                           bi("sortir du quart le plus bas", "leave the bottom quarter"), "immédiate", "5 ans"))
        lignes.append((LIB_THEME["prix"], bi("actions nationales : prix de la data, frais du petit retrait, équipement", "national actions: data price, small-withdrawal fees, equipment"),
                       bi("nationales", "national"), "immédiate", "5 ans"))
        constat(html.escape(bi(f"{choix} ({region(region_choix)}, {nombre(int(info.pop_totale))} habitants) : {len(lignes) - 1} actions ciblées, "
                               "plus les actions nationales.",
                               f"{choix} ({region(region_choix)}, {nombre(int(info.pop_totale))} people): {len(lignes) - 1} targeted actions, "
                               "plus the national ones.")))
        with st.container(border=True):
            titre_bloc(bi(f"Les actions à {choix}", f"Actions in {choix}"))
            st.dataframe(formater(pd.DataFrame(lignes, columns=[bi("thème", "theme"), bi("action", "action"), bi("cible", "target"),
                                                        bi("nature", "nature"), bi("horizon", "horizon")]).assign(
                **{bi("nature", "nature"): lambda d: d[bi("nature", "nature")].map(valeur), bi("horizon", "horizon"): lambda d: d[bi("horizon", "horizon")].map(valeur)})),
                hide_index=True, use_container_width=True)
            note(bi(f"La fiche de {choix} est sur la page {og}{t('page.diagnostic')}{fg}.", f"{choix}’s profile is on the {og}{t('page.diagnostic')}{fg} page."))
        limite(bi("Une préfecture peut avoir des actions sans être en priorité haute : les communes sans agence sont en priorité absolue où "
                  "qu’elles soient.", "A prefecture can have actions without being high priority: communes with no branch are an absolute "
                  "priority wherever they are."))

# =================================================================== 4. Ordre d’action et acteurs
if o_ordre.open is not False:
    with o_ordre:
        with st.container(border=True):
            titre_bloc(bi("Ordre d’action", "Order of action"),
                       bi("Le premier rang applique la priorité absolue et lève l’incertitude qui bloque le réseau ; le deuxième suit le "
                          "classement ; le troisième attend le premier ; le quatrième est national et se mène en parallèle.",
                          "The first rank applies absolute priority and removes the uncertainty blocking the network; the second follows the "
                          "ranking; the third waits for the first; the fourth is national and runs in parallel."))
            ordre = [(1, ["R1", "R4a"]), (2, ["R2", "R3"]), (3, ["R4b", "R9"]), (4, ["R5", "R6", "R7", "R7b", "R8", "R10"])]
            lignes = []
            for rang, ids in ordre:
                for i in ids:
                    lignes.append((rang, TITRE[i], TERRITOIRES[i], valeur(s.loc[i, "horizon"]), valeur(s.loc[i, "nature"])))
            # Tableau statique : des phrases, qui doivent revenir à la ligne (un tableau interactif les coupe)
            st.table(pd.DataFrame(lignes, columns=[bi("rang", "rank"), bi("action", "action"), bi("où", "where"), bi("horizon", "horizon"),
                                                   bi("nature", "nature")]).set_index(bi("rang", "rank")))
        gauche, droite = st.columns([0.8, 1.2], gap="large")
        with gauche:
            with st.container(border=True):
                titre_bloc(bi("Priorité des territoires visés", "Priority of the targeted territories"),
                           bi("Classe de chaque préfecture ; en ocre, les communes en priorité absolue.", "Class of each prefecture; in ochre, the absolute-priority communes."))
                carte_priorites(contours("prefectures"), P, "carte_recos", set(P.code), C[C.priorite_absolue], contours("communes"), hauteur=560)
        with droite:
            with st.container(border=True):
                titre_bloc(bi("Qui agit ?", "Who acts?"), bi("Rôles vérifiés sur des sources publiques.", "Roles checked against public sources."))
                acteurs = pd.DataFrame([
                    (bi("Banques", "Banks"), bi("agences financières", "financial branches"), bi("Commission bancaire de l’UMOA, sous l’égide de la BCEAO (banque centrale)", "UMOA Banking Commission, under the BCEAO (central bank)")),
                    (bi("Institutions de microfinance", "Microfinance institutions"), bi("agences financières", "financial branches"), bi("loi 2011-009 ; BCEAO ; Commission bancaire", "Law 2011-009; BCEAO; Banking Commission")),
                    (bi("Assurances", "Insurers"), bi("agences financières", "financial branches"), bi("code CIMA (régulation régionale) ; CRCA", "CIMA code (regional regulation); CRCA")),
                    (bi("Émetteurs de mobile money (Moov Africa, YAS)", "Mobile money issuers (Moov Africa, YAS)"), bi("points mobile money, frais", "mobile money points, fees"), bi("agrément de la BCEAO", "BCEAO licence")),
                    (bi("ARCEP (régulateur des télécoms)", "ARCEP (telecom regulator)"), bi("mesure de la couverture, prix de la data, fonds du service universel", "coverage measurement, data price, universal service fund"), bi("décret 2018-070", "Decree 2018-070")),
                    (bi("Opérateurs télécoms", "Telecom operators"), bi("réseau, sites radio, équipement", "network, radio sites, equipment"), bi("licences", "licences")),
                    (bi("Société d’infrastructures numériques", "Digital Infrastructure Company"), bi("fibre", "fibre"), bi("décret 2016-166 ; coentreprise CSquared Woezon", "Decree 2016-166; CSquared Woezon joint venture")),
                    (bi("Ministère chargé du numérique", "Ministry in charge of digital affairs"), bi("compétences, équipement, investissement", "skills, equipment, investment"), bi("stratégie Togo Digital 2025-2030", "Togo Digital 2025-2030 strategy")),
                ], columns=[bi("acteur", "actor"), bi("actions", "actions"), bi("fondement", "grounding")])
                st.table(acteurs.set_index(bi("acteur", "actor")))
                note(bi("Qui peut agir, pas qui doit payer : les budgets et le rôle des collectivités restent hors des données.",
                        "Who can act, not who must pay: budgets and the role of local authorities remain outside the data."))
            with st.container(border=True):
                titre_bloc(bi("Ce qui n’est pas recommandé", "What is not recommended"))
                nr = pd.DataFrame([
                    (bi("Interopérabilité ou concurrence (Mô : la moitié des points tenus par Togocom seul)", "Interoperability or competition (Mô: half of points served by Togocom alone)"),
                     bi("rejetée", "rejected"), bi("aucun indicateur ne la chiffre ; gardée comme constat", "no indicator measures it; kept as a finding")),
                    (bi("Usage du mobile money dans la Centrale (19,9 %)", "Mobile money use in Centrale (19.9%)"), bi("non retenue en l’état", "not retained as is"),
                     bi("cause non établie : ni l’offre ni l’accès à Internet n’y sont faibles", "cause not established: neither supply nor Internet access is weak there")),
                    (bi("Sensibilisation, demande d’Internet", "Awareness, Internet demand"), bi("non retenue", "not retained"),
                     bi("aucun indicateur ne mesure la demande ; l’écart d’accès est traité par ses freins (prix, compétences, équipement)",
                        "no indicator measures demand; the access gap is addressed through its barriers (price, skills, equipment)")),
                    (bi("Leviers tirés des événements passés de l’usage d’Internet", "Levers drawn from past Internet-use events"), bi("rejetée", "rejected"),
                     bi("ces événements sont des coïncidences, pas des causes", "these events are coincidences, not causes")),
                    (bi("Choix des sites parmi des lieux candidats (marchés, écoles, centres de santé)", "Site choice among candidate places (markets, schools, health centres)"),
                     bi("non faite", "not done"), bi("aucune population sous la commune : le gain d’un site ne peut pas être calculé", "no population below the commune: a site’s gain cannot be computed")),
                ], columns=[bi("piste", "option"), bi("statut", "status"), bi("raison", "reason")])
                st.table(nr.set_index(bi("piste", "option")))
        limite(bi("Les habitants concernés ne sont jamais additionnés d’une action à l’autre. L’ordre d’action suit le classement et la priorité "
                  "absolue ; il ne dit rien des budgets.",
                  "People concerned are never added up from one action to another. The order of action follows the ranking and absolute "
                  "priority; it says nothing about budgets."))
pied()
