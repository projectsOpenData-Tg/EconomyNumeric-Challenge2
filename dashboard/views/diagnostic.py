"""Page 7 — Diagnostic : « Pourquoi ces territoires ? » (plan visuel, section 7, page 7).

Fiche d’une préfecture prioritaire (sélecteur, 10 fiches) ; carte des 25 communes signalées ; usage d’Internet par
région (freins présumés)."""
import html

import streamlit as st

from composants import ariane, carte_kpi, carte_valeur, colorer_regions, constat, entete, export_csv, limite, pied, rangee_kpi
from donnees import contours, lire, nombre
from i18n import bi, frein, region, t
from theme import PRIORITE

fiches = lire("09_diagnostic", "fiches_prefectures")
signalees = lire("09_diagnostic", "communes_signalees")
internet_reg = lire("09_diagnostic", "internet_regions")
fac = lire("09_diagnostic", "facteurs_repetition").set_index("colonne")
dist = fac.loc["part_points_mm_plus_10km_guichet_pct"]

ariane(t("page.diagnostic"))
entete(t("page.diagnostic"), bi("Pourquoi ces territoires ?", "Why these territories?"),
       bi(f"Le trait commun est la distance au guichet : <strong>{nombre(dist.mediane_priorite_1)} %</strong> des points mobile money "
          f"des préfectures en priorité haute sont à plus de 10 km d’un guichet, contre {nombre(dist.mediane_autres_classees)} % ailleurs.",
          f"The common trait is distance to the service point: <strong>{nombre(dist.mediane_priorite_1)}%</strong> of mobile money "
          f"points in high-priority prefectures are over 10 km from a service point, against {nombre(dist.mediane_autres_classees)}% elsewhere."))

rangee_kpi(bi("Diagnostic, national", "Diagnosis, national"), [
    carte_kpi(bi("Fiches préfectures", "Prefecture profiles"), str(len(fiches)), bi("préfectures prioritaires", "priority prefectures"),
              "", "", None, "neutre"),
    carte_kpi(bi("Communes signalées", "Flagged communes"), str(len(signalees)), nombre(int(signalees.pop_totale.sum())) + bi(" habitants", " people"),
              "", "", None, "critique"),
    carte_kpi(bi("Facteurs répétés", "Repeated factors"), f"{int((fac.priorite_1_du_cote_defavorable.str.startswith('7')).sum())}/4",
              bi("se répètent dans les 7 préfectures", "recur across the 7 prefectures"), "", "", None, "neutre"),
    carte_kpi(bi("Distance au guichet", "Distance to service point"), f"{nombre(dist.mediane_priorite_1)} %",
              bi("des points mobile money à plus de 10 km", "of mobile money points over 10 km away"), "", "", bi("Écart marqué", "Marked gap"), "alerte"),
])

st.write("")
gauche, droite = st.columns([1.2, 1], gap="large")

with gauche:
    with st.container(border=True):
        st.markdown(f'<div class="bloc-titre">{html.escape(bi("Fiche de préfecture", "Prefecture profile"))}</div>', unsafe_allow_html=True)
        noms = fiches.nom.tolist()
        choix = st.selectbox(bi("Préfecture", "Prefecture"), noms, key="diag_prefecture")
        signaler = st.toggle(bi("Communes signalées de cette préfecture", "Flagged communes in this prefecture"), value=True, key="diag_communes")
        fi = fiches[fiches.nom == choix].iloc[0]
        st.markdown(
            f'<div class="reponse"><strong>{html.escape(fi.nom)}</strong> ({region(fi.unite_regionale)}, {nombre(int(fi.pop_totale))} '
            f'{bi("habitants", "people")}) — {html.escape(str(fi.classe_retenue))}, {bi("confiance", "confidence")} {fi.confiance_P13}.<br>'
            f'{bi("Moteur du déficit", "Main driver")} : <strong>{html.escape(str(fi.moteur))}</strong> ({html.escape(str(fi.deficits_marques))}).<br>'
            f'{bi("Statut d’accès", "Access status")} : {html.escape(str(fi.statut_O4_05))} ; '
            f'{bi("couverture", "coverage")} {nombre(fi.couverture_proxy_pct)} % ; '
            f'{fi.n_banque} {bi("banques", "banks")}, {fi.n_imf} IMF, {fi.n_assurance} {bi("assurances", "insurers")}, {fi.n_dab} DAB, {fi.n_mm} {bi("points mobile money", "mobile money points")}.<br>'
            f'{bi(f"Fibre : {nombre(fi.km_fibre_enterree)} km enterrée.", f"Fibre: {nombre(fi.km_fibre_enterree)} km buried.")}</div>',
            unsafe_allow_html=True)
        pf_signalees = signalees[signalees.prefecture == choix] if signaler else signalees
        st.dataframe(pf_signalees[["nom", "statut_O4_05", "signal", "pop_totale"]].rename(columns={
            "nom": bi("commune", "commune"), "statut_O4_05": bi("statut", "status"), "signal": bi("signal", "flag"),
            "pop_totale": bi("habitants", "population")}), hide_index=True, use_container_width=True)
        export_csv(fiches, "fiches_prefectures.csv", "export_fiches")

with droite:
    constat(bi("Le trait commun est la distance au guichet : 39 % des points mobile money à plus de 10 km d’un guichet, contre 6 % ailleurs.",
               "The common trait is distance to the service point: 39% of mobile money points over 10 km away, against 6% elsewhere."))

    with st.container(border=True):
        st.markdown(f'<div class="bloc-titre">{html.escape(bi("Les 25 communes signalées", "The 25 flagged communes"))}</div>', unsafe_allow_html=True)
        carte_valeur(contours("communes"), signalees.assign(**{"signal_lib": signalees.signal}), "carte_signalees", "signal_lib",
                    bi("Signal", "Flag"), categorique=True, hauteur=420,
                    couleurs_categorie={"sans point formel et cellule critique": "#e34948", "sans point formel": "#eda100",
                                       "cellule critique": "#4a3aa7"})
        export_csv(signalees, "communes_signalees.csv", "export_signalees")

    with st.container(border=True):
        st.markdown(f'<div class="bloc-titre">{html.escape(bi("Usage d’Internet par région", "Internet use by region"))}</div>', unsafe_allow_html=True)
        ir = internet_reg[["region", "acces_internet_2021_22_pct", "alphabetisation_2021_22_pct", "lecture_O1_06"]].rename(columns={
            "region": bi("région", "region"), "acces_internet_2021_22_pct": bi("accès (%)", "access (%)"),
            "alphabetisation_2021_22_pct": bi("alphabétisation (%)", "literacy (%)"), "lecture_O1_06": bi("frein présumé", "presumed barrier")})
        ir[bi("région", "region")] = ir[bi("région", "region")].map(region)
        ir[bi("frein présumé", "presumed barrier")] = ir[bi("frein présumé", "presumed barrier")].map(frein)
        st.dataframe(colorer_regions(ir, bi("région", "region")), hide_index=True, use_container_width=True)
        export_csv(internet_reg, "internet_regions.csv", "export_internet_regions")

limite(bi("Ce sont des associations, pas des causes démontrées. Les distances sont mesurées à vol d’oiseau, pas par la route.",
         "These are associations, not demonstrated causes. Distances are measured as the crow flies, not by road."))
pied()
