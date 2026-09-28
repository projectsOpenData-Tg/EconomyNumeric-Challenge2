"""Page 4 — Population et offre : « Combien d’habitants par point, et où le mobile money est-il seul ? »
(plan visuel, section 7, page 4). Seuil d’habitants par point formel déplaçable (section 6) : bascule d’un seuil
déjà calculé, pas un recalcul de l’indicateur."""
import html

import pandas as pd
import streamlit as st

from composants import ariane, carte_kpi, carte_valeur, constat, entete, export_csv, limite, pied, rangee_kpi
from donnees import ANALYSE, communes, contours, filtrer_communes, lire, nombre
from i18n import bi, langue, t
from theme import STATUT_O4_05

FR = langue() == "fr"
f = {"regions": st.session_state.f_regions, "priorites": st.session_state.f_priorites, "milieux": st.session_state.f_milieux}
C = communes()
Cf = filtrer_communes(C, f)

sans_guichet = C[C.n_formels == 0]
suppl = C[C.classe_O4_03 == "suppléance quasi totale"]
insuffisant = C[C.classe_O4_04 == "maillage insuffisant"]
crit = C[C.cellule_critique]
div = pd.read_csv(ANALYSE / "07_indicateurs" / "p2_divergence_communes.csv")

ariane(t("page.population"))
entete(t("page.population"), bi("Combien d’habitants par point, et où le mobile money est-il seul ?",
                                "How many people per service point, and where is mobile money the only option?"),
       bi(f"<strong>{len(sans_guichet)} communes</strong> n’ont aucun point formel ; <strong>{len(suppl)} communes</strong> "
          "n’ont presque que le mobile money.",
          f"<strong>{len(sans_guichet)} communes</strong> have no formal point at all; <strong>{len(suppl)} communes</strong> "
          "have almost only mobile money."))

rangee_kpi(bi("Accès aux points, national", "Access to service points, national"), [
    carte_kpi(bi("Sans point formel", "No formal point"), str(len(sans_guichet)), bi("communes", "communes"),
              "", "", t("priorite.absolue"), "critique"),
    carte_kpi(bi("Mobile money supplée", "Mobile money substitutes"), str(len(suppl)), bi("communes", "communes"),
              bi("plus de 20 points de service par guichet", "over 20 service points per formal point"), "", None, "alerte"),
    carte_kpi(bi("Maillage insuffisant", "Insufficient network"), str(len(insuffisant)), bi("communes (mobile money)", "communes (mobile money)"),
              bi("Blitta 2, Blitta 3, Kpendjal 2", "Blitta 2, Blitta 3, Kpendjal 2"), "", None, "alerte"),
    carte_kpi(bi("Cellules critiques", "Critical cells"), str(len(crit)), bi("communes", "communes"),
              t("lib.couverture_theorique") + bi(" sous 50 %", " below 50%"), bi("À confirmer.", "To confirm."),
              bi("À confirmer", "To confirm"), "neutre"),
])

st.write("")
gauche, droite = st.columns([1.15, 1], gap="large")

with gauche:
    with st.container(border=True):
        st.markdown(f'<div class="bloc-titre">{html.escape(bi("Habitants par point formel", "People per formal point"))}</div>', unsafe_allow_html=True)
        s1, s2 = st.slider(bi("Seuils (valeur de référence : 10 000 et 30 000)", "Thresholds (reference: 10,000 and 30,000)"),
                           1000, 60000, (10000, 30000), step=1000, key="seuil_formel")
        def classer(x):
            if pd.isna(x):
                return bi("sans point formel", "no formal point")
            return bi("bien desservi", "well served") if x <= s1 else (bi("tendu", "stretched") if x <= s2 else bi("sous-desservi", "under-served"))
        Cc = C.copy()
        Cc["classe_seuil"] = Cc.hab_par_point_formel.map(classer)
        couleurs = {bi("bien desservi", "well served"): "#0d366b", bi("tendu", "stretched"): "#3987e5",
                   bi("sous-desservi", "under-served"): "#eda100", bi("sans point formel", "no formal point"): "#8a1c1b"}
        carte_valeur(contours("communes"), Cc, "carte_hab_formel", "classe_seuil", bi("Classe", "Class"), categorique=True,
                    couleurs_categorie=couleurs, hover_extra={"hab_par_point_formel": ":,.0f"})
        if (s1, s2) != (10000, 30000):
            st.caption(bi(f"Vous regardez une variante : la référence est 10 000 et 30 000 (repère national : {nombre(C.hab_par_point_formel.median(),0)} à la médiane).",
                         f"You are viewing a variant: the reference is 10,000 and 30,000 (national median: {nombre(C.hab_par_point_formel.median(),0)})."))
        export_csv(Cc[["code", "nom", "hab_par_point_formel", "classe_seuil"]], "habitants_par_point_formel.csv", "export_hab_formel")

    with st.container(border=True):
        st.markdown(f'<div class="bloc-titre">{html.escape(bi("Statut d’accès financier", "Financial access status"))}</div>', unsafe_allow_html=True)
        # Variante de l’ordre de la cascade (07, O4-05) : la règle « desserte diversifiée » est testée avant « mobile money dominant »
        variante = st.toggle(bi("Variante : la desserte diversifiée l’emporte sur le mobile money dominant",
                                "Variant: diversified service takes precedence over mobile money dominant"), key="variante_p9",
                             help=bi("Règle de référence : une commune qui a plus de 20 points mobile money par guichet est « mobile money "
                                     "dominant », même si elle a les 4 types de points et moins de 10 000 habitants par guichet. La variante "
                                     "la classe alors en « desserte diversifiée ».",
                                     "Reference rule: a commune with more than 20 mobile money points per formal point is “mobile money "
                                     "dominant”, even if it has all 4 point types and fewer than 10,000 people per formal point. The variant "
                                     "then classes it as “diversified service”."))
        colonne = "statut_O4_05_variante_P9" if variante else "statut_O4_05"
        carte_valeur(contours("communes"), C, f"carte_statut_{colonne}", colonne, bi("Statut", "Status"), categorique=True,
                    couleurs_categorie=STATUT_O4_05)
        if variante:
            bascule = C[(C.statut_O4_05 == "mobile money dominant") & (C.statut_O4_05_variante_P9 == "desserte diversifiée")]
            noms_bascule = ", ".join(bascule.nom)
            st.caption(bi(f"Variante décidée après avoir vu le résultat : affichée à côté, jamais à la place de la règle de référence. "
                          f"{len(bascule)} communes passent de « mobile money dominant » à « desserte diversifiée » "
                          f"({nombre(int(bascule.pop_totale.sum()))} habitants) : {noms_bascule}.",
                          f"Variant decided after seeing the result: shown alongside, never instead of the reference rule. "
                          f"{len(bascule)} communes move from “mobile money dominant” to “diversified service” "
                          f"({nombre(int(bascule.pop_totale.sum()))} people): {noms_bascule}."))
        export_csv(C[["code", "nom", "statut_O4_05", "statut_O4_05_variante_P9"]], "statut_acces.csv", "export_statut")

with droite:
    constat(bi("Deux communes sur trois ne sont pas dans la classe de leur préfecture : la préfecture cache les communes.",
               "Two out of three communes are not in their prefecture’s class: the prefecture hides the communes."))

    with st.container(border=True):
        st.markdown(f'<div class="bloc-titre">{html.escape(bi("Matrice statut × couverture (communes)", "Status × coverage matrix (communes)"))}</div>', unsafe_allow_html=True)
        mat = lire("07_indicateurs", "o4_06_matrice_communes")
        cols = [c for c in mat.columns if c != "statut_O4_05"]
        # En-têtes en clair et dans la langue choisie : la table écrit « non déterminable (A13) », un code interne
        mat_disp = mat.rename(columns={"statut_O4_05": bi("statut", "status"),
                                       "couverture partielle (proxy)": bi("couverture partielle (proxy)", "partial coverage (proxy)"),
                                       "non déterminable (A13)": bi("couverture inconnue", "coverage unknown"),
                                       "territoire couvert (proxy)": bi("territoire couvert (proxy)", "covered territory (proxy)"),
                                       "zone blanche prioritaire (proxy)": bi("zone blanche prioritaire (proxy)", "priority white zone (proxy)")})
        st.dataframe(mat_disp, hide_index=True, use_container_width=True)
        export_csv(mat, "matrice_statut_couverture.csv", "export_matrice")

    with st.container(border=True):
        st.markdown(f'<div class="bloc-titre">{html.escape(bi("Communes qui divergent de leur préfecture", "Communes that diverge from their prefecture"))}</div>'
                    f'<div class="bloc-sous-titre">{html.escape(bi(f"{int((div.diverge_au_moins_une).sum())} communes sur {len(div)} n’ont pas la même classe que leur préfecture, sur au moins une des trois mesures.", f"{int((div.diverge_au_moins_une).sum())} out of {len(div)} communes do not share their prefecture’s class, on at least one of the three measures."))}</div>',
                    unsafe_allow_html=True)
        divt = div[div.diverge_au_moins_une][["nom", "prefecture", "classe_O4_01_commune", "classe_O4_01_prefecture"]].rename(columns={
            "nom": bi("commune", "commune"), "prefecture": bi("préfecture", "prefecture"),
            "classe_O4_01_commune": bi("classe (commune)", "class (commune)"), "classe_O4_01_prefecture": bi("classe (préfecture)", "class (prefecture)")})
        st.dataframe(divt, hide_index=True, use_container_width=True, height=240)
        export_csv(div, "divergence_communes_prefectures.csv", "export_divergence")

limite(bi("Population résidente, pas fréquentation (sous-estimée pour le Grand Lomé, où l’activité de jour dépasse la résidence). "
         "Couverture théorique. La classe par seuil est une application d’affichage : elle ne remplace pas classe_O4_01 (référence).",
         "Resident population, not footfall (understated for Greater Lomé, where daytime activity exceeds residence). Theoretical "
         "coverage. The threshold-based class is a display-only application: it does not replace the reference classe_O4_01."))
pied()
