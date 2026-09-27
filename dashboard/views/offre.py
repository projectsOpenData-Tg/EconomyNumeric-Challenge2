"""Page 3 — Offre financière : « Où sont les établissements financiers ? » (plan visuel, section 7, page 3 ; DAB
précisés le 27/09/2026, section 7 du 11)."""
import html

import streamlit as st

from composants import ariane, carte_kpi, carte_valeur, constat, entete, export_csv, limite, pied, rangee_kpi
from donnees import communes, contours, filtrer_communes, nombre, operateurs_communes
from i18n import bi, langue, region, t
from theme import CATEGORIELLE

FR = langue() == "fr"
f = {"regions": st.session_state.f_regions, "priorites": st.session_state.f_priorites, "milieux": st.session_state.f_milieux}
C = communes()
Cf = filtrer_communes(C, f)

points_formels = int(C.n_formels.sum())
points_mm = int(C.n_mm.sum())
sans_assurance = int((C.n_assurance == 0).sum())
dab_total, communes_dab = int(C.n_dab.sum()), int((C.n_dab > 0).sum())

ariane(t("page.offre"))
entete(t("page.offre"), bi("Où sont les établissements financiers ?", "Where are the financial institutions?"),
       bi(f"<strong>{nombre(points_formels)} points formels</strong> (banques, IMF, assurances) et "
          f"<strong>{nombre(points_mm)} points mobile money</strong> ; <strong>{sans_assurance} communes sur {len(C)}</strong> "
          "n’ont aucune assurance.",
          f"<strong>{nombre(points_formels)} formal points</strong> (banks, MFIs, insurers) and "
          f"<strong>{nombre(points_mm)} mobile money points</strong>; <strong>{sans_assurance} out of {len(C)} communes</strong> "
          "have no insurer."))

rangee_kpi(bi("Offre financière (national)", "Financial services (national)"), [
    carte_kpi(bi("Points formels", "Formal points"), nombre(points_formels), bi("banques, IMF et assurances", "banks, MFIs and insurers"),
              "", bi("Recensement 2021/2022.", "2021/2022 survey."), None, "neutre"),
    carte_kpi(bi("Points mobile money", "Mobile money points"), nombre(points_mm), bi("points de service actifs", "active service points"),
              "", bi("Des points de service, pas des agents.", "Service points, not agents."), None, "neutre"),
    carte_kpi(bi("Communes sans assurance", "Communes with no insurer"), f"{sans_assurance}/{len(C)}",
              bi("n’ont aucune assurance recensée", "have no insurer surveyed"), "", "", bi("Offre rare", "Scarce offer"), "alerte"),
    carte_kpi(bi("DAB", "ATMs"), nombre(dab_total), bi(f"dans {communes_dab} communes", f"in {communes_dab} communes"),
              t("lib.type_a_part"), bi("Un DAB en banque n’est pas un second guichet.", "An ATM in a bank is not a second service point."),
              None, "neutre"),
])

st.write("")
gauche, droite = st.columns([1.15, 1], gap="large")

with gauche:
    with st.container(border=True):
        st.markdown(f'<div class="bloc-titre">{html.escape(bi("Points par type", "Points by type"))}</div>', unsafe_allow_html=True)
        types = {"n_banque": bi("Banques", "Banks"), "n_imf": bi("IMF", "MFIs"), "n_assurance": bi("Assurances", "Insurers"),
                "n_dab": bi("DAB", "ATMs")}
        choix = st.segmented_control(bi("Type de point", "Point type"), list(types.keys()), format_func=lambda k: types[k],
                                     default="n_banque", key="offre_type")
        choix = choix or "n_banque"
        if choix == "n_dab":
            st.markdown(f'<span class="etiquette alerte">{html.escape(t("lib.type_a_part"))}</span>', unsafe_allow_html=True)
        carte_valeur(contours("communes"), C, f"carte_offre_{choix}", choix, types[choix], palette="Blues")
        export_csv(C[["code", "nom", "unite_regionale", "n_banque", "n_imf", "n_assurance", "n_dab"]], "points_formels_communes.csv", "export_offre_type")

    with st.container(border=True):
        st.markdown(f'<div class="bloc-titre">{html.escape(bi("Points mobile money", "Mobile money points"))}</div>', unsafe_allow_html=True)
        carte_valeur(contours("communes"), C, "carte_mm", "n_mm", bi("Points mobile money", "Mobile money points"), palette="Oranges")

with droite:
    constat(bi("L’écart oppose les villes aux campagnes, bien plus que Lomé aux autres villes.",
               "The gap sets towns against the countryside, far more than Lomé against other towns."))

    with st.container(border=True):
        st.markdown(f'<div class="bloc-titre">{html.escape(bi("Opérateurs du mobile money", "Mobile money operators"))}</div>'
                    f'<div class="bloc-sous-titre">{html.escape(bi("Catégorie dominante par commune (part la plus élevée parmi les quatre).", "Dominant category per commune (highest share of the four)."))}</div>',
                    unsafe_allow_html=True)
        op = operateurs_communes()
        cols = {"part_deux_operateurs_pct": bi("Deux opérateurs", "Both operators"), "part_togocom_seul_pct": "Togocom (YAS)",
               "part_moov_seul_pct": "Moov Africa", "part_operateur_non_renseigne_pct": bi("Non renseigné", "Not reported")}
        op["Categorie"] = op[list(cols)].idxmax(axis=1).map(cols)
        couleurs_op = {cols["part_deux_operateurs_pct"]: CATEGORIELLE[0], "Togocom (YAS)": CATEGORIELLE[1],
                      "Moov Africa": CATEGORIELLE[2], cols["part_operateur_non_renseigne_pct"]: "#b9b6ad"}
        carte_valeur(contours("communes"), op, "carte_operateurs", "Categorie", bi("Opérateur", "Operator"), categorique=True,
                    couleurs_categorie=couleurs_op)
        st.caption(bi("Opérateur non renseigné jusqu’à 23 % des points dans la région de Kara.",
                     "Operator not reported for up to 23% of points in the Kara region."))
        export_csv(op, "operateurs_mobile_money.csv", "export_operateurs")

st.write("")
with st.container(border=True):
    st.markdown(f'<div class="bloc-titre">{html.escape(bi("Points par préfecture et par type", "Points by prefecture and type"))}</div>', unsafe_allow_html=True)
    pf = communes().groupby(["prefecture", "unite_regionale"], as_index=False)[["n_banque", "n_imf", "n_assurance", "n_dab", "n_mm"]].sum()
    pf = pf.rename(columns={"prefecture": bi("préfecture", "prefecture"), "unite_regionale": bi("région", "region"),
                            "n_banque": bi("banques", "banks"), "n_imf": "IMF", "n_assurance": bi("assurances", "insurers"),
                            "n_dab": "DAB", "n_mm": bi("mobile money", "mobile money")})
    pf[bi("région", "region")] = pf[bi("région", "region")].map(region)
    st.dataframe(pf, hide_index=True, use_container_width=True)
    export_csv(pf, "points_par_prefecture.csv", "export_pf_type")

limite(bi("Recensement 2021/2022 : des lieux, pas des agents ni des transactions. L’opérateur n’est pas renseigné pour jusqu’à 23 % "
         "des points dans la région de Kara. La catégorie dominante affichée sur la carte des opérateurs ne dit pas qu’un seul "
         "opérateur y est présent, seulement lequel y a la part la plus élevée.",
         "2021/2022 survey: places, not agents or transactions. The operator is not reported for up to 23% of points in the Kara "
         "region. The dominant category on the operator map does not mean only one operator is present there, only which one has "
         "the highest share."))
pied()
