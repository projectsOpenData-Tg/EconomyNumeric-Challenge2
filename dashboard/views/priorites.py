"""Page 6 — Priorités : « Par quels territoires commencer ? » (plan visuel, section 7, page 6).

Refaite le 29/09/2026 (relevé des objectifs 4 et 5, `workspace/conding-progress.md`, étape 2) : quatre sous-onglets.
« Vue synthèse » (chiffres clés, carte avec et sans la couverture, les classes qui en dépendent) ; « Classement » (les 39
préfectures, score décomposé en trois dimensions, confiance, population ; ce qui place les 7 priorités hautes en tête) ;
« Poids et robustesse » (poids modifiables : seule exception au « pas de recalcul », même formule que le 08 — moyenne
pondérée des rangs percentiles, classes à 70 et 40 ; tests de sensibilité) ; « Comparateur ».

Vocabulaire des décideurs : pas de codes de dimension (D1, D2, D3), ni de « min-max », « rho » ou « rang percentile » ; la
confiance affichée est celle de la lecture retenue par le 08 (variante validée), la règle stricte à côté (correction C11).
"""
import html

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from composants import (BLEU_FONCE, ariane, carte_kpi, carte_valeur, colorer_regions, constat, entete, export_csv, formater,
                        habiller, limite, note, onglets, pct, pied, rangee_kpi, titre_bloc, tracer)
from donnees import communes, contours, lire, nombre, prefectures
from i18n import bi, region, t, valeur
from theme import DIMENSION, PRIORITE

S = prefectures()
sensi = lire("08_priorisation", "sensibilite_tests")
synth = lire("08_priorisation", "synthese_classes")
C = communes()

og, fg = bi("« ", "“"), bi(" »", "”")
p1 = S[S.classe_retenue == "priorité 1"]
non_classees = S[S.classe_retenue == "non déterminable (couverture)"]
dependantes = S[S.depend_de_la_couverture.astype(bool)]
p1_robustes_02 = int((p1.robustesse == "robuste").sum())
p1_robustes = int((p1.robustesse_P13 == "robuste").sum())
p1_sans_couv = int((p1.sans_couv_classe == "priorité 1").sum())
p1_poids = p1[[c for c in S.columns if c.startswith("classe_test_poids")]].eq("priorité 1").all(axis=1).all() if len(p1) else False

DIM = {"D1": (bi("agences financières", "financial branches"), bi("habitants par agence", "people per branch"), DIMENSION["acces"]),
       "D2": (bi("mobile money", "mobile money"), bi("habitants par point mobile money", "people per mobile money point"), DIMENSION["maillage"]),
       "D3": (bi("couverture (estimation)", "coverage (estimate)"), bi("habitants hors couverture théorique (%)", "people outside theoretical coverage (%)"),
              DIMENSION["couverture"])}
LIB_PRIO = {"haute": t("priorite.haute"), "moyenne": t("priorite.moyenne"), "faible": t("priorite.faible"), "non classée": t("priorite.non_classee")}
COUL_PRIO = {LIB_PRIO[k]: PRIORITE[k] for k in LIB_PRIO}
CLASSE_VERS_PRIO = {"priorité 1": "haute", "priorité 2": "moyenne", "priorité 3": "faible", "non déterminable (couverture)": "non classée"}


def confiance(v) -> str:
    """Confiance de la lecture retenue ; « non classée (lecture à 2 dimensions) » devient « non classée »."""
    return valeur("non déterminable (couverture)") if str(v).startswith("non classée") else valeur(v)


ariane(t("page.priorites"))
entete(t("page.priorites"), bi("Par quels territoires commencer ?", "Which territories to start with?"),
       bi(f"<strong>{len(p1)} préfectures en priorité haute</strong> ({nombre(int(p1.pop_totale.sum()))} habitants) ; "
          f"<strong>{len(non_classees)} non classées</strong> faute de couverture connue, en priorité haute sur les deux autres mesures.",
          f"<strong>{len(p1)} high-priority prefectures</strong> ({nombre(int(p1.pop_totale.sum()))} people); "
          f"<strong>{len(non_classees)} not ranked</strong> for lack of known coverage, high priority on the two other measures."))

# Ce que le score ne couvre pas : l’usage d’Internet (08, sections 1 et 8.1). Affiché en tête, sur toutes les vues, pour
# qu’aucun lecteur ne lise ce classement comme une priorité pour l’usage d’Internet.
p1_hors_d3 = int((p1["classe_test_poids D3 doublé"] != "priorité 1").sum())
test_d3 = (bi(f"Doubler le poids de la couverture ne fait sortir aucune des {len(p1)} préfectures de la priorité haute.",
              f"Doubling the weight of coverage takes none of the {len(p1)} prefectures out of high priority.") if p1_hors_d3 == 0 else
           bi(f"Doubler le poids de la couverture fait sortir {p1_hors_d3} des {len(p1)} préfectures de la priorité haute.",
              f"Doubling the weight of coverage takes {p1_hors_d3} of the {len(p1)} prefectures out of high priority."))
limite(bi("Le classement porte sur l’accès aux agences financières, au mobile money et au réseau. Aucune mesure de l’usage d’Internet "
          "n’existe à la préfecture : à poids égaux, les deux mesures financières pèsent les deux tiers du score. "
          f"{test_d3} Pour l’usage d’Internet, les priorités se lisent par région : page {og}{t('page.internet')}{fg}, onglet "
          f"{og}{bi('Accès et freins par région', 'Access and barriers by region')}{fg}.",
          "The ranking covers access to financial branches, mobile money and the network. No measure of Internet use exists at "
          "prefecture level: with equal weights, the two financial measures make up two thirds of the score. "
          f"{test_d3} For Internet use, priorities are read by region: {og}{t('page.internet')}{fg} page, "
          f"{og}{bi('Accès et freins par région', 'Access and barriers by region')}{fg} tab."),
       titre=bi("Ce classement ne porte pas sur l’usage d’Internet", "This ranking is not about Internet use"))

LIBELLES = [bi("Vue synthèse", "Overview"), bi("Classement", "Ranking"), bi("Poids et robustesse", "Weights and robustness"),
            bi("Comparateur", "Comparison")]
o_synth, o_classement, o_poids, o_comparateur = onglets("priorites_onglets", LIBELLES)

# =================================================================== 1. Vue synthèse
if o_synth.open is not False:
    with o_synth:
        rangee_kpi(bi("La priorité en quatre chiffres", "Priority in four figures"), [
            carte_kpi(t("priorite.haute"), str(len(p1)), bi("préfectures", "prefectures"),
                      bi(f"{nombre(int(p1.pop_totale.sum()))} habitants ; aucune dans le Maritime ni le Grand Lomé",
                         f"{nombre(int(p1.pop_totale.sum()))} people; none in Maritime or Greater Lomé"), "", None, "critique"),
            carte_kpi(t("priorite.non_classee"), str(len(non_classees)), ", ".join(non_classees.nom),
                      bi("couverture inconnue ; en priorité haute sur les agences et le mobile money",
                         "coverage unknown; high priority on branches and mobile money"),
                      bi("Kpendjal est aussi en priorité absolue : aucune agence financière.", "Kpendjal is also an absolute priority: no financial branch."),
                      bi("À mesurer", "To measure"), "neutre"),
            carte_kpi(bi("Dépendent de la couverture", "Depend on coverage"), str(len(dependantes)),
                      bi("préfectures changent de classe sans elle", "prefectures change class without it"), ", ".join(dependantes.nom),
                      bi("La couverture est une estimation (rayon de 20 km).", "Coverage is an estimate (20 km radius)."), None, "alerte"),
            carte_kpi(bi("Robustesse", "Robustness"), f"{p1_robustes}/{len(p1)}",
                      bi("priorités hautes le restent sous tous les tests", "high priorities stay so under every test"),
                      bi(f"{p1_robustes_02}/{len(p1)} à la lettre de la règle (onglet {og}{LIBELLES[2]}{fg})",
                         f"{p1_robustes_02}/{len(p1)} by the letter of the rule ({og}{LIBELLES[2]}{fg} tab)"),
                      "", bi("Noyau stable", "Stable core") if p1_robustes == len(p1) else None, "ok"),
        ])
        st.write("")
        constat(bi(f"Les {len(p1)} préfectures en priorité haute le restent sous tous les poids testés"
                   + (" et sans la couverture." if p1_sans_couv == len(p1) else "."),
                   f"The {len(p1)} high-priority prefectures stay so under every weighting tested"
                   + (" and without coverage." if p1_sans_couv == len(p1) else ".")))
        gauche, droite = st.columns([0.85, 1.15], gap="large")  # le Togo est étroit : la carte cède de la largeur au tableau
        with gauche:
            with st.container(border=True):
                titre_bloc(bi("Carte des priorités", "Priority map"),
                           bi("Classe de chaque préfecture ; la bascule retire la couverture, estimée, du calcul.",
                              "Class of each prefecture; the switch removes coverage, which is estimated, from the calculation."))
                sans = st.toggle(bi("Sans la couverture théorique", "Without theoretical coverage"), key="prio_sans_couv")
                col = "sans_couv_classe" if sans else "classe_retenue"
                Sm = S.copy()
                Sm["_prio"] = Sm[col].map(CLASSE_VERS_PRIO)
                Sm["_rang"] = Sm._prio.map(list(LIB_PRIO).index)
                lib_cl = bi("classe", "class")
                Sm[lib_cl] = Sm._prio.map(LIB_PRIO)
                carte_valeur(contours("prefectures"), Sm.sort_values("_rang"), f"carte_prio_{col}", lib_cl, lib_cl, categorique=True,
                             couleurs_categorie=COUL_PRIO, hauteur=560)
                if sans:
                    note(bi("Sans la couverture, les 39 préfectures sont classées sur les deux mesures financières ; les 3 non classées "
                            "le deviennent.", "Without coverage, all 39 prefectures are ranked on the two financial measures; the 3 unranked "
                            "ones become ranked."))
        with droite:
            with st.container(border=True):
                titre_bloc(bi(f"Les {len(dependantes)} préfectures dont la classe dépend de la couverture",
                              f"The {len(dependantes)} prefectures whose class depends on coverage"),
                           bi("Leur classe change quand la couverture, une estimation, est retirée : elle est à confirmer.",
                              "Their class changes when coverage, an estimate, is removed: it needs confirming."))
                tab = pd.DataFrame({bi("préfecture", "prefecture"): dependantes.nom,
                                    bi("avec la couverture", "with coverage"): dependantes.classe_retenue.map(valeur),
                                    bi("sans", "without"): dependantes.sans_couv_classe.map(valeur),
                                    bi("couverture", "coverage"): dependantes.couverture_proxy_pct.map(lambda v: pct(v))})
                st.dataframe(tab, hide_index=True, use_container_width=True)
                montent = dependantes[dependantes.sans_couv_classe < dependantes.classe_retenue]
                note(bi(f"{', '.join(montent.nom)} montent sans la couverture : bien couvertes, elles sont faibles sur les agences ou le "
                        "mobile money. Les autres descendent : c’est leur couverture qui les classait.",
                        f"{', '.join(montent.nom)} move up without coverage: well covered, they are weak on branches or mobile money. The "
                        "others move down: their coverage was what ranked them."))
                note(bi(f"Les {len(p1)} priorités hautes ne dépendent pas de la couverture." if p1_sans_couv == len(p1) else
                        f"{len(p1) - p1_sans_couv} priorités hautes dépendent de la couverture.",
                        f"The {len(p1)} high priorities do not depend on coverage." if p1_sans_couv == len(p1) else
                        f"{len(p1) - p1_sans_couv} high priorities depend on coverage."), forte=True)
                export_csv(dependantes[["code", "nom", "classe_retenue", "sans_couv_classe", "couverture_proxy_pct"]],
                           "classes_dependant_couverture.csv", "export_dependantes")
        limite(bi("Un rang est relatif : un territoire est prioritaire par rapport aux autres, pas dans l’absolu. La préfecture cache des "
                  "communes : 8 communes sans agence financière sont dans des préfectures en priorité faible. La couverture reste une "
                  "estimation.",
                  "A rank is relative: a territory is a priority compared to others, not in absolute terms. The prefecture hides "
                  "communes: 8 communes with no financial branch are in low-priority prefectures. Coverage remains an estimate."))

# =================================================================== 2. Classement
if o_classement.open is not False:
    with o_classement:
        constat(bi("Aucune mesure n’explique seule le classement : chaque priorité haute a son point faible, et la plupart en cumulent "
                   "plusieurs.", "No single measure explains the ranking: each high priority has its weak point, and most combine several."))
        with st.container(border=True):
            titre_bloc(bi(f"Ce qui place les {len(p1)} priorités hautes en tête", f"What puts the {len(p1)} high priorities first"),
                       bi("Position sur chaque mesure, de 0 (la mieux servie) à 100 (la plus mal servie des 36 préfectures classées) ; "
                          "le losange est le score, moyenne des trois, écrit à côté du nom. Cercle vide : la couverture, une estimation.",
                          "Position on each measure, from 0 (best served) to 100 (worst served of the 36 ranked prefectures); the diamond "
                          "is the score, the average of the three, written next to the name. Hollow circle: coverage, an estimate."))
            pp = p1.sort_values("score").assign(etiquette=lambda d: [f"{n} ({nombre(v, 1)})" for n, v in zip(d.nom, d.score)])
            fig = go.Figure()
            for d, symbole in (("D1", "circle"), ("D2", "circle"), ("D3", "circle-open")):
                fig.add_scatter(x=pp[f"{d}_rang_pct"], y=pp.etiquette, mode="markers", name=DIM[d][0],
                                marker=dict(size=13, color=DIM[d][2], symbol=symbole, line=dict(color=DIM[d][2] if symbole.endswith("open") else "#ffffff", width=2)),
                                customdata=pp[d].round(1), hovertemplate="%{y} : %{x:.0f} / 100<br>" + DIM[d][1] + " : %{customdata:,.1f}<extra>" + DIM[d][0] + "</extra>")
            fig.add_scatter(x=pp.score, y=pp.etiquette, mode="markers", name=bi("score (entre parenthèses)", "score (in brackets)"),
                            marker=dict(size=11, color=BLEU_FONCE, symbol="diamond"), hovertemplate="%{y} : score %{x:.1f}<extra></extra>")
            fig.add_vline(x=70, line_dash="dot", line_color="#8a8780", line_width=1)
            fig.add_annotation(x=70, y=1, yref="paper", yanchor="bottom", xanchor="right", showarrow=False, font=dict(size=11, color=BLEU_FONCE),
                               text=bi("seuil de la priorité haute : 70", "high-priority threshold: 70"))
            tracer(habiller(fig, 380, legende_y=1.16, xaxis=dict(range=[0, 108], gridcolor="#efece4"), yaxis=dict(gridcolor="#efece4")), "prio_decomposition")
            pire = {d: p1.loc[p1[f"{d}_rang_pct"].idxmax()] for d in ("D1", "D2", "D3")}
            note(bi(f"{pire['D1'].nom} a le pire accès aux agences ({nombre(pire['D1'].D1, 0)} habitants par agence) ; {pire['D2'].nom}, le mobile "
                    f"money le plus mince ({nombre(pire['D2'].D2, 0)} habitants par point) ; {pire['D3'].nom}, la plus forte part hors couverture "
                    f"({nombre(pire['D3'].D3, 1)} %, une estimation fragile). Les autres cumulent trois positions élevées.",
                    f"{pire['D1'].nom} has the worst access to branches ({nombre(pire['D1'].D1, 0)} people per branch); {pire['D2'].nom}, the "
                    f"thinnest mobile money ({nombre(pire['D2'].D2, 0)} people per point); {pire['D3'].nom}, the largest share outside coverage "
                    f"({nombre(pire['D3'].D3, 1)}%, a fragile estimate). The others combine three high positions."), forte=True)

        st.write("")
        with st.container(border=True):
            titre_bloc(bi("Les 39 préfectures", "The 39 prefectures"),
                       bi("Ordre de la règle : la classe, puis la population. Le score mesure l’intensité du manque, la population son "
                          "volume : à classe égale, la plus peuplée passe devant.",
                          "Order of the rule: class, then population. The score measures how intense the gap is, population how large: "
                          "within a class, the most populous comes first."))
            So = S.sort_values("ordre_final")
            c_reg = bi("région", "region")
            c_d = {"D1": bi("agences", "branches"), "D2": "mobile money", "D3": bi("couverture", "coverage")}
            tab = pd.DataFrame({
                bi("préfecture", "prefecture"): So.nom, c_reg: So.unite_regionale.map(region),
                bi("classe", "class"): So.classe_retenue.map(valeur), bi("score", "score"): So.score.round(1),
                **{c_d[d]: So[f"{d}_rang_pct"].round(0) for d in DIM},
                bi("confiance", "confidence"): So.confiance_P13.map(confiance),
                bi("habitants", "people"): So.pop_totale.astype(int),
                bi("communes signalées", "flagged communes"): [", ".join(dict.fromkeys([x.strip() for x in (str(a) + "," + str(b)).split(",")
                                                                                          if x.strip() and x.strip() != "nan"]))
                                                               for a, b in zip(So.noms_communes_sans_point_formel, So.communes_critiques_O4_06)]})
            st.dataframe(colorer_regions(tab, c_reg), hide_index=True, use_container_width=True, height=520,
                         column_config={**{c_d[d]: st.column_config.ProgressColumn(c_d[d], min_value=0, max_value=100, format="%d", width="small") for d in DIM},
                                        c_reg: st.column_config.TextColumn(c_reg, width="medium")})
            note(bi("Colonnes des trois mesures : la position, de 0 (la mieux servie) à 100 (la plus mal servie). Communes signalées : sans "
                    "agence, ou avec un réseau faible.", "Columns of the three measures: the position, from 0 (best served) to 100 (worst served). "
                    "Flagged communes: with no branch, or with a weak network."))
            note(bi(f"Les {len(non_classees)} préfectures non classées ({', '.join(non_classees.nom)}) n’ont pas de score à trois mesures : "
                    "leur couverture est inconnue. Sur les deux autres, elles seraient en priorité haute ; elles sont suivies à part, jamais "
                    "mêlées au classement.",
                    f"The {len(non_classees)} unranked prefectures ({', '.join(non_classees.nom)}) have no three-measure score: their coverage is "
                    "unknown. On the two others, they would be high priority; they are tracked separately, never mixed into the ranking."))
            export_csv(So[["ordre_final", "code", "nom", "unite_regionale", "classe_retenue", "score", "D1_rang_pct", "D2_rang_pct", "D3_rang_pct",
                           "confiance_P13", "pop_totale", "noms_communes_sans_point_formel", "communes_critiques_O4_06"]], "classement_prefectures.csv",
                       "export_classement")
        limite(bi("La position va de 0 à 100 parmi les préfectures classées : 100 est la plus mal servie, pas un besoin absolu. La confiance "
                  "est celle de la lecture retenue pour le diagnostic (voir l’onglet sur la robustesse).",
                  "The position runs from 0 to 100 among ranked prefectures: 100 is the worst served, not an absolute need. Confidence is "
                  "that of the reading retained for the diagnosis (see the robustness tab)."))

# =================================================================== 3. Poids et robustesse
if o_poids.open is not False:
    with o_poids:
        constat(bi(f"Les {len(p1)} préfectures en priorité haute " + ("le restent sous tous les poids testés." if p1_poids else "ne le restent pas toutes sous tous les poids testés."),
                   f"The {len(p1)} high-priority prefectures " + ("stay so under every weighting tested." if p1_poids else "do not all stay so under every weighting tested.")))
        gauche, droite = st.columns([0.85, 1.15], gap="large")  # le Togo est étroit : la carte cède de la largeur aux tableaux
        with gauche:
            with st.container(border=True):
                titre_bloc(bi("Changer les poids", "Change the weights"),
                           bi("Poids égaux par défaut (référence) ; le score recalculé suit la même formule, une moyenne pondérée des positions.",
                              "Equal weights by default (reference); the recalculated score follows the same formula, a weighted average of positions."))
                c1, c2, c3 = st.columns(3)
                w1 = c1.slider(DIM["D1"][0].capitalize(), 0.0, 1.0, 1 / 3, 0.05, key="poids_d1")
                w2 = c2.slider(DIM["D2"][0].capitalize(), 0.0, 1.0, 1 / 3, 0.05, key="poids_d2")
                w3 = c3.slider(DIM["D3"][0].capitalize(), 0.0, 1.0, 1 / 3, 0.05, key="poids_d3")
                wt = w1 + w2 + w3 or 1
                w1n, w2n, w3n = w1 / wt, w2 / wt, w3 / wt
                variante = abs(w1n - 1 / 3) > 0.01 or abs(w2n - 1 / 3) > 0.01

                Sr = S.copy()
                Sr["score_var"] = w1n * Sr.D1_rang_pct + w2n * Sr.D2_rang_pct + w3n * Sr.D3_rang_pct
                Sr["classe_var"] = pd.cut(Sr.score_var, bins=[-1, 40, 70, 101], labels=["priorité 3", "priorité 2", "priorité 1"])
                Sr["classe_var"] = Sr["classe_var"].astype(object).where(Sr.score_var.notna(), "non déterminable (couverture)")
                Sr["_prio"] = Sr.classe_var.map(CLASSE_VERS_PRIO)
                Sr["_rang"] = Sr._prio.map(list(LIB_PRIO).index)
                lib_cl = bi("classe", "class")
                Sr[lib_cl] = Sr._prio.map(LIB_PRIO)
                Sr[bi("score", "score")] = Sr.score_var.round(1)
                if variante:
                    n_change = int((Sr.classe_var != Sr.classe_retenue).sum())
                    note(bi(f"Vous regardez une variante : la référence est un tiers pour chaque mesure. {n_change} préfectures changent de classe.",
                            f"You are viewing a variant: the reference is one third for each measure. {n_change} prefectures change class."))
                carte_valeur(contours("prefectures"), Sr.sort_values("_rang"), "carte_score_variante", lib_cl, lib_cl, categorique=True,
                             couleurs_categorie=COUL_PRIO, hover_extra={bi("score", "score"): ":.1f"}, hauteur=540)
                export_csv(Sr[["code", "nom", "D1_rang_pct", "D2_rang_pct", "D3_rang_pct", "score_var", "classe_var", "classe_retenue"]],
                           "score_variante.csv", "export_score_variante")
        with droite:
            with st.container(border=True):
                titre_bloc(bi("Répartition des classes", "Class breakdown"))
                s3 = synth[synth.lecture == "3 dimensions"]
                st.dataframe(formater(pd.DataFrame({bi("classe", "class"): s3.classe.map(valeur), bi("préfectures", "prefectures"): s3.prefectures.astype(int),
                                           bi("robustes (règle)", "robust (rule)"): s3.robustes.astype(int),
                                           bi("robustes (lecture retenue)", "robust (retained reading)"): s3.robustes_P13.astype(int),
                                           bi("habitants", "people"): s3.population.map(lambda x: nombre(x))})),
                             hide_index=True, use_container_width=True)
                note(bi(f"À la lettre de la règle, une classe est robuste si aucun test ne la change. Le test « autre échelle » écrase les "
                        f"scores (aucun n’y atteint 70) : {p1_robustes_02} priorité haute sur {len(p1)} y est robuste. Lue en ordre, lecture "
                        f"retenue pour le diagnostic et affichée à côté de la règle, les {p1_robustes} le sont.",
                        f"By the letter of the rule, a class is robust if no test changes it. The “other scale” test squeezes the scores "
                        f"(none reaches 70 there): {p1_robustes_02} high priority out of {len(p1)} is robust. Read as an order, the reading "
                        f"retained for the diagnosis and shown alongside the rule, all {p1_robustes} are."), forte=True)

        st.write("")
        with st.container(border=True):
            titre_bloc(bi("Tests de robustesse", "Robustness tests"),
                       bi("Nombre de préfectures qui changent de classe sous chaque test, et ressemblance avec le classement de référence "
                          "(1 = même ordre).", "Number of prefectures that change class under each test, and similarity with the reference "
                          "ranking (1 = same order)."))

            def lib_test(x: str) -> str:
                x = str(x)
                for debut, fr_, en_ in (("poids D1", "poids des agences doublé", "weight of branches doubled"),
                                        ("poids D2", "poids du mobile money doublé", "weight of mobile money doubled"),
                                        ("poids D3", "poids de la couverture doublé", "weight of coverage doubled"),
                                        ("min-max lu", "autre échelle, lue en ordre (lecture retenue)", "other scale, read as an order (retained reading)"),
                                        ("min-max", "autre échelle (écrase les scores)", "other scale (squeezes the scores)"),
                                        ("sans ", "sans le territoire extrême (" + x[5:] + ")", "without the extreme territory (" + x[5:] + ")")):
                    if x.startswith(debut):
                        return bi(fr_, en_)
                return x
            tests = pd.DataFrame({bi("test", "test"): sensi.test.map(lib_test),
                                  bi("lecture", "reading"): sensi.lecture.map(lambda v: bi("avec la couverture", "with coverage") if v.startswith("3")
                                                                               else bi("sans la couverture", "without coverage")),
                                  bi("classes qui changent", "classes that change"): sensi.classes_changees.astype(int),
                                  bi("ressemblance (0 à 1)", "similarity (0 to 1)"): sensi.rho_avec_principal.map(lambda v: nombre(v, 2))})
            st.dataframe(tests, hide_index=True, use_container_width=True, height=35 * (len(tests) + 1) + 3)
            export_csv(sensi, "sensibilite_tests.csv", "export_sensibilite")
        limite(bi("Les poids modifiables sont la seule exception au « pas de recalcul » : même formule que le classement de référence. "
                  "Une variante n’est jamais la référence.",
                  "Movable weights are the only exception to “no recalculation”: same formula as the reference ranking. A variant is never "
                  "the reference."))

# =================================================================== 4. Comparateur
if o_comparateur.open is not False:
    with o_comparateur:
        with st.container(border=True):
            titre_bloc(bi("Comparateur de deux préfectures", "Compare two prefectures"))
            noms = sorted(S.nom)
            ca, cb = st.columns(2)
            a = ca.selectbox(bi("Préfecture A", "Prefecture A"), noms, index=noms.index("Dankpen") if "Dankpen" in noms else 0, key="cmp_a")
            b = cb.selectbox(bi("Préfecture B", "Prefecture B"), noms, index=noms.index("Golfe") if "Golfe" in noms else 1, key="cmp_b")
            ra, rb = S[S.nom == a].iloc[0], S[S.nom == b].iloc[0]

            def v(r, col, d):
                return "—" if pd.isna(r[col]) else nombre(r[col], d)
            mesures = [(bi("Classe", "Class"), None), (DIM["D1"][1].capitalize(), ("D1", 0)), (DIM["D2"][1].capitalize(), ("D2", 0)),
                       (DIM["D3"][1].capitalize(), ("D3", 1)), (bi("Score", "Score"), ("score", 1)),
                       (bi("Confiance", "Confidence"), "confiance"), (bi("Habitants", "People"), ("pop_totale", 0))]
            lignes = ""
            for lib, spec in mesures:
                if spec is None:
                    va, vb = valeur(ra.classe_retenue), valeur(rb.classe_retenue)
                elif spec == "confiance":
                    va, vb = confiance(ra.confiance_P13), confiance(rb.confiance_P13)
                else:
                    va, vb = v(ra, *spec), v(rb, *spec)
                lignes += (f'<tr><td style="padding:6px 4px">{html.escape(lib)}</td><td style="text-align:right">{html.escape(str(va))}</td>'
                           f'<td style="text-align:right">{html.escape(str(vb))}</td></tr>')
            st.markdown(f'<table style="width:100%;font-size:0.92rem;border-collapse:collapse"><tr><th></th>'
                        f'<th style="text-align:right">{html.escape(a)}</th><th style="text-align:right">{html.escape(b)}</th></tr>{lignes}</table>',
                        unsafe_allow_html=True)
            note(bi("Un « — » : la couverture de la préfecture est inconnue ; elle n’a pas de score à trois mesures.",
                    "A “—”: the prefecture’s coverage is unknown; it has no three-measure score."))
        limite(bi("Deux préfectures se comparent sur leurs valeurs, pas sur leur rang seul : un rang dit « mieux ou moins bien que les autres », "
                  "pas « assez ».", "Two prefectures are compared on their values, not their rank alone: a rank says “better or worse than "
                  "the others”, not “enough”."))
pied()
