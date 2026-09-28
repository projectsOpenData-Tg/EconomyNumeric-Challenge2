"""Page 6 — Priorités : « Par quels territoires commencer ? » (plan visuel, section 7, page 6).

Score décomposé (D1 accès formel, D2 maillage mobile money, D3 couverture) ; poids modifiables (seule exception au
« pas de recalcul », section 11 : même formule que le 08 — moyenne pondérée des rangs percentiles, classes à 70 et
40) ; robustesse ; comparateur de deux préfectures."""
import html

import pandas as pd
import streamlit as st

from composants import ariane, carte_kpi, carte_valeur, constat, entete, export_csv, limite, pied, rangee_kpi
from donnees import contours, lire, nombre, prefectures
from i18n import bi, region, t
from theme import DIMENSION, PRIORITE

S = prefectures()
regle = lire("08_priorisation", "regles_score")
sensi = lire("08_priorisation", "sensibilite_tests")
synth = lire("08_priorisation", "synthese_classes")

p1 = S[S.classe_retenue == "priorité 1"]
non_classees = S[S.classe_retenue == "non déterminable (couverture)"]
dependantes = S[S.depend_de_la_couverture]

ariane(t("page.priorites"))
entete(t("page.priorites"), bi("Par quels territoires commencer ?", "Which territories to start with?"),
       bi(f"<strong>{len(p1)} préfectures en priorité haute</strong> ({nombre(int(p1.pop_totale.sum()))} habitants) ; "
          f"<strong>{len(non_classees)} non classées</strong> faute de couverture connue.",
          f"<strong>{len(p1)} high-priority prefectures</strong> ({nombre(int(p1.pop_totale.sum()))} people); "
          f"<strong>{len(non_classees)} not ranked</strong> for lack of known coverage."))

rangee_kpi(bi("Priorité, national", "Priority, national"), [
    carte_kpi(t("priorite.haute"), str(len(p1)), bi("préfectures", "prefectures"), nombre(int(p1.pop_totale.sum())) + bi(" habitants", " people"),
              "", None, "neutre"),
    carte_kpi(t("priorite.non_classee"), str(len(non_classees)), ", ".join(non_classees.nom),
              bi("couverture inconnue : la carte de couverture y donne 0 % alors que des points mobile money y fonctionnent",
                 "coverage unknown: the coverage map shows 0% there although mobile money points operate"), "", bi("À combler", "Gap"), "neutre"),
    carte_kpi(bi("Dépendent de la couverture", "Depend on coverage"), str(len(dependantes)), bi("préfectures changent de classe sans elle", "prefectures change class without it"),
              "", bi("La couverture est un proxy.", "Coverage is a proxy."), None, "alerte"),
    carte_kpi(bi("Robustesse", "Robustness"), f"{int((S.robustesse=='robuste').sum())}/{len(S)}",
              bi("préfectures robustes à tous les tests", "prefectures robust to every test"),
              "", bi("6 tests de sensibilité (tableau « Tests de robustesse »).", "6 sensitivity tests (“Robustness tests” table)."), None, "ok"),
])

# Ce que le score ne couvre pas : l’usage d’Internet (08, sections 1 et 8.1). Affiché en tête, pour qu’aucun lecteur ne lise
# ce classement comme une priorité pour l’usage d’Internet.
p1_hors_d3 = int((p1["classe_test_poids D3 doublé"] != "priorité 1").sum())
test_d3 = (bi(f"Doubler le poids de la couverture ne fait sortir aucune des {len(p1)} préfectures de la priorité haute.",
              f"Doubling the weight of coverage takes none of the {len(p1)} prefectures out of high priority.") if p1_hors_d3 == 0 else
           bi(f"Doubler le poids de la couverture fait sortir {p1_hors_d3} des {len(p1)} préfectures de la priorité haute.",
              f"Doubling the weight of coverage takes {p1_hors_d3} of the {len(p1)} prefectures out of high priority."))
onglet_regions = bi("« Accès et freins par région »", "“Access and barriers by region”")
page_internet = bi(f"« {t('page.internet')} »", f"“{t('page.internet')}”")
limite(bi("Le score classe les préfectures sur l’accès financier (points formels, mobile money) et sur la couverture réseau. Aucune "
          "mesure de l’usage d’Internet n’existe à la préfecture : à poids égaux, les deux dimensions financières pèsent les deux tiers "
          f"du score. {test_d3} Pour l’usage d’Internet, les priorités se lisent par région : page {page_internet}, onglet {onglet_regions}.",
          "The score ranks prefectures on financial access (formal points, mobile money) and on network coverage. No measure of "
          "Internet use exists at prefecture level: with equal weights, the two financial dimensions make up two thirds of the score. "
          f"{test_d3} For Internet use, priorities are read by region: {page_internet} page, {onglet_regions} tab."),
       titre=bi("Ce classement ne porte pas sur l’usage d’Internet", "This ranking is not about Internet use"))

st.write("")
gauche, droite = st.columns([1.2, 1], gap="large")

with gauche:
    with st.container(border=True):
        st.markdown(f'<div class="bloc-titre">{html.escape(bi("Score décomposé et poids", "Decomposed score and weights"))}</div>'
                    f'<div class="bloc-sous-titre">{html.escape(bi("Poids égaux par défaut (référence) ; le score recalculé utilise la même formule (moyenne pondérée des rangs percentiles).", "Equal weights by default (reference); the recalculated score uses the same formula (weighted average of percentile ranks)."))}</div>',
                    unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        w1 = c1.slider(bi("D1 — accès formel", "D1 — formal access"), 0.0, 1.0, 1 / 3, 0.05, key="poids_d1")
        w2 = c2.slider(bi("D2 — maillage mobile money", "D2 — mobile money network"), 0.0, 1.0, 1 / 3, 0.05, key="poids_d2")
        w3 = c3.slider(bi("D3 — couverture (proxy)", "D3 — coverage (proxy)"), 0.0, 1.0, 1 / 3, 0.05, key="poids_d3")
        wt = w1 + w2 + w3 or 1
        w1n, w2n, w3n = w1 / wt, w2 / wt, w3 / wt
        variante = abs(w1n - 1 / 3) > 0.01 or abs(w2n - 1 / 3) > 0.01

        Sr = S.copy()
        Sr["score_var"] = w1n * Sr.D1_rang_pct + w2n * Sr.D2_rang_pct + w3n * Sr.D3_rang_pct
        Sr["classe_var"] = pd.cut(Sr.score_var, bins=[-1, 40, 70, 101], labels=["priorité 3", "priorité 2", "priorité 1"])
        Sr["classe_var"] = Sr["classe_var"].astype(object).where(Sr.score_var.notna(), "non déterminable (couverture)")
        Sr["priorite"] = Sr.classe_var.map({"priorité 1": "haute", "priorité 2": "moyenne", "priorité 3": "faible",
                                            "non déterminable (couverture)": "non classée"})
        if variante:
            n_change = int((Sr.classe_var != Sr.classe_retenue).sum())
            st.caption(bi(f"Vous regardez une variante : la référence est 1/3, 1/3, 1/3. {n_change} préfectures changent de classe.",
                         f"You are viewing a variant: the reference is 1/3, 1/3, 1/3. {n_change} prefectures change class."))
        carte_valeur(contours("prefectures"), Sr, "carte_score_variante", "priorite", bi("Classe", "Class"), categorique=True,
                    couleurs_categorie={"haute": PRIORITE["haute"], "moyenne": PRIORITE["moyenne"], "faible": PRIORITE["faible"],
                                       "non classée": PRIORITE["non classée"]}, hover_extra={"score_var": ":.1f"})
        export_csv(Sr[["code", "nom", "D1_rang_pct", "D2_rang_pct", "D3_rang_pct", "score_var", "classe_var", "classe_retenue"]],
                  "score_variante.csv", "export_score_variante")

    with st.container(border=True):
        st.markdown(f'<div class="bloc-titre">{html.escape(bi("Tests de robustesse", "Robustness tests"))}</div>'
                    f'<div class="bloc-sous-titre">{html.escape(bi("Nombre de préfectures qui changent de classe sous chaque test (référence : 3 dimensions, poids égaux).", "Number of prefectures that change class under each test (reference: 3 dimensions, equal weights)."))}</div>',
                    unsafe_allow_html=True)
        sensi_disp = sensi.rename(columns={"test": bi("test", "test"), "territoires": bi("territoires classés", "ranked territories"),
                                           "classes_changees": bi("classes changées", "classes changed"),
                                           "rho_avec_principal": bi("corrélation (rho)", "correlation (rho)"),
                                           "extreme_retire": bi("territoire extrême retiré", "extreme territory removed")})
        st.dataframe(sensi_disp.drop(columns=[bi("lecture", "lecture")], errors="ignore"), hide_index=True, use_container_width=True)
        export_csv(sensi, "sensibilite_tests.csv", "export_sensibilite")

with droite:
    p1_stable = p1[[c for c in S.columns if c.startswith("classe_test_poids")]].eq("priorité 1").all(axis=1).all() if len(p1) else False
    constat(bi(f"Les {len(p1)} préfectures en priorité haute " + ("le restent sous tous les poids testés." if p1_stable else "ne le restent pas toutes sous tous les poids testés."),
              f"The {len(p1)} high-priority prefectures " + ("stay so under every weighting tested." if p1_stable else "do not all stay so under every weighting tested.")))

    with st.container(border=True):
        st.markdown(f'<div class="bloc-titre">{html.escape(bi("Comparateur de deux préfectures", "Compare two prefectures"))}</div>', unsafe_allow_html=True)
        noms = sorted(S.nom)
        a = st.selectbox(bi("Préfecture A", "Prefecture A"), noms, index=noms.index("Dankpen") if "Dankpen" in noms else 0, key="cmp_a")
        b = st.selectbox(bi("Préfecture B", "Prefecture B"), noms, index=noms.index("Golfe") if "Golfe" in noms else 1, key="cmp_b")
        ra, rb = S[S.nom == a].iloc[0], S[S.nom == b].iloc[0]
        mesures = [(bi("Habitants par point formel", "People per formal point"), "D1", 0),
                  (bi("Habitants par point mobile money", "People per mobile money point"), "D2", 0),
                  (bi("Couverture hors zone (proxy, %)", "Out-of-coverage share (proxy, %)"), "D3", 1),
                  (bi("Score", "Score"), "score", 1), (bi("Population", "Population"), "pop_totale", 0)]
        lignes = "".join(
            f'<tr><td>{html.escape(lib)}</td><td style="text-align:right">{nombre(ra[col], d)}</td>'
            f'<td style="text-align:right">{nombre(rb[col], d)}</td></tr>' for lib, col, d in mesures)
        st.markdown(f'<table style="width:100%;font-size:0.88rem;border-collapse:collapse"><tr><th></th>'
                    f'<th style="text-align:right">{html.escape(a)}</th><th style="text-align:right">{html.escape(b)}</th></tr>{lignes}</table>',
                    unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(f'<div class="bloc-titre">{html.escape(bi("Répartition des classes", "Class breakdown"))}</div>', unsafe_allow_html=True)
        synth3 = synth[synth.lecture == "3 dimensions"].copy()
        synth3["population"] = synth3.population.map(lambda x: nombre(x))
        synth_disp = synth3[["classe", "prefectures", "robustes", "population", "part_population_pct"]].rename(columns={
            "classe": bi("classe", "class"), "prefectures": bi("préfectures", "prefectures"), "robustes": bi("robustes", "robust"),
            "population": bi("habitants", "population"), "part_population_pct": "% "})
        st.dataframe(synth_disp, hide_index=True, use_container_width=True)

limite(bi("Un rang est relatif : un territoire est prioritaire par rapport aux autres, pas dans l’absolu. La préfecture cache des "
         "communes (8 communes sans point formel dans des préfectures en priorité faible). La couverture reste un proxy.",
         "A rank is relative: a territory is a priority compared to others, not in absolute terms. The prefecture hides communes "
         "(8 communes with no formal point in low-priority prefectures). Coverage remains a proxy."))
pied()
