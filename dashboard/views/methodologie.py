"""Page 10 — Méthodologie : sources, conventions, les 27 indicateurs, glossaire, crédits (plan visuel, section 7,
page 10). Seule page où apparaissent les codes internes, toujours avec leur intitulé (section 3.1)."""
import html
import re
from pathlib import Path

import pandas as pd
import streamlit as st

from composants import ariane, entete, export_csv, pied
from i18n import bi, t

RACINE = Path(__file__).resolve().parents[2]


@st.cache_data(show_spinner=False)
def indicateurs() -> pd.DataFrame:
    """Les 27 indicateurs, lus dans le tableau du 07 (ID, indicateur, maille, source, sens, statut, résultat clé) —
    jamais retapés. Seul le tableau qui suit l'en-tête « | ID | Indicateur | Maille | ... » est lu : le code d'un
    indicateur est aussi cité ailleurs dans le document (ex. la table de divergence), sans y être une ligne du
    tableau (moins de colonnes)."""
    lignes_fichier = (RACINE / "07_indicators.md").read_text(encoding="utf-8").splitlines()
    debut = next(i for i, l in enumerate(lignes_fichier) if l.startswith("| ID | Indicateur | Maille")) + 2  # saute l'en-tête et le filet
    rows = []
    for l in lignes_fichier[debut:]:
        if not re.match(r"^\| O[1-5]-\d", l):
            break
        cellules = [c.strip() for c in l.strip("|").split("|")]
        if len(cellules) == 7:
            rows.append(cellules)
    return pd.DataFrame(rows, columns=["id", "indicateur", "maille", "source", "sens", "statut", "resultat"])


ind = indicateurs()

ariane(t("page.methodologie"))
entete(t("page.methodologie"), bi("Sources, conventions et limites", "Sources, conventions and limits"),
       bi(f"Les <strong>{len(ind)} indicateurs</strong> du projet, leur maille, leur source et leur résultat clé ; les conventions "
          "qui gouvernent les seuils et les classes ; le glossaire des codes.",
          f"The project’s <strong>{len(ind)} indicators</strong>, their scale, source and key result; the conventions governing "
          "thresholds and classes; the code glossary."))

with st.container(border=True):
    st.markdown(f'<div class="bloc-titre">{html.escape(bi("Sources et millésimes", "Sources and vintages"))}</div>', unsafe_allow_html=True)
    src = pd.DataFrame([
        (bi("Population", "Population"), "RGPH, 2022", bi("recensement général", "general census")),
        (bi("Points de service (formels et mobile money)", "Service points (formal and mobile money)"), "PRISE, 2021/2022", bi("recensement", "survey")),
        (bi("Usage d’Internet", "Internet use"), "UIT, 2000–2024", bi("estimation internationale", "international estimate")),
        (bi("Accès déclaré à Internet", "Self-reported Internet access"), "EHCVM, 2018/19 et 2021/22", bi("enquête ménages", "household survey")),
        (bi("Marché des télécommunications", "Telecommunications market"), "ARCEP, INSEED, 2010–2025", bi("rapports d’activité", "activity reports")),
        (bi("Mobile money : comptes et activité", "Mobile money: accounts and activity"), "BCEAO, 2024", bi("service financiers numériques", "digital financial services")),
        (bi("Couverture réseau", "Network coverage"), "3i, 2021/2022", bi("proxy théorique (rayon de 20 km)", "theoretical proxy (20 km radius)")),
        (bi("Alphabétisation et compétences numériques", "Literacy and digital skills"), "MICS6", bi("enquête par grappes", "cluster survey")),
        (bi("Équipement et coût du smartphone", "Equipment and smartphone cost"), "Findex, 2024/2025", bi("enquête individuelle", "individual survey")),
    ], columns=[bi("thème", "topic"), bi("source et millésime", "source and vintage"), bi("nature", "nature")])
    st.dataframe(src, hide_index=True, use_container_width=True)

with st.container(border=True):
    st.markdown(f'<div class="bloc-titre">{html.escape(bi("Conventions", "Conventions"))}</div>', unsafe_allow_html=True)
    texte_conventions = bi(
        "Seuils déclarés avant le résultat : 40 % et 60 % pour l’usage d’Internet, 2 % pour le coût de 1 Go, 3 % pour le retrait de "
        "petit montant, 15 % pour l’investissement, 50 sites radio par an, 85 % et 50 % pour la couverture, 10 000 et 30 000 "
        "habitants par point formel. Les classes de priorité viennent d’un rang percentile (100 × (rang − 1) / (n − 1)), moyenné sur "
        "trois dimensions à poids égaux : 70 ou plus = priorité haute, de 40 à 70 = priorité moyenne, moins de 40 = priorité faible. "
        "Une variante décidée après avoir vu le résultat (P9, P13) est toujours affichée à côté de la règle de référence, jamais à "
        "la place.",
        "Thresholds declared before the result: 40% and 60% for Internet use, 2% for the cost of 1 GB, 3% for small withdrawals, "
        "15% for investment, 50 radio sites a year, 85% and 50% for coverage, 10,000 and 30,000 people per formal point. Priority "
        "classes come from a percentile rank (100 × (rank − 1) / (n − 1)), averaged over three equally weighted dimensions: 70 or "
        "more = high priority, 40 to 70 = medium priority, under 40 = low priority. A variant decided after seeing the result (P9, "
        "P13) is always shown alongside the reference rule, never instead of it.")
    st.markdown(f'<div class="reponse">{html.escape(texte_conventions)}</div>', unsafe_allow_html=True)

with st.container(border=True):
    st.markdown(f'<div class="bloc-titre">{html.escape(bi(f"Les {len(ind)} indicateurs", f"The {len(ind)} indicators"))}</div>', unsafe_allow_html=True)
    filtre = st.text_input(bi("Filtrer (code ou mot-clé)", "Filter (code or keyword)"), key="meth_filtre")
    ind_disp = ind.rename(columns={"id": "ID", "indicateur": bi("indicateur", "indicator"), "maille": bi("maille", "scale"),
                                   "source": bi("source", "source"), "sens": bi("sens", "direction"), "statut": bi("statut", "status"),
                                   "resultat": bi("résultat clé", "key result")})
    if filtre:
        masque = ind_disp.apply(lambda r: filtre.lower() in " ".join(str(v) for v in r).lower(), axis=1)
        ind_disp = ind_disp[masque]
    st.dataframe(ind_disp, hide_index=True, use_container_width=True, height=420)
    export_csv(ind, "indicateurs_27.csv", "export_indicateurs")

with st.container(border=True):
    st.markdown(f'<div class="bloc-titre">{html.escape(bi("Glossaire des codes", "Code glossary"))}</div>', unsafe_allow_html=True)
    glossaire = pd.DataFrame([
        ("O1–O5", bi("Objectifs 1 à 5 du projet (usage, marché, offre financière, rapport population/offre, priorisation)",
                     "Project objectives 1 to 5 (use, market, financial supply, population/supply ratio, prioritization)")),
        ("IMF", bi("Institution de microfinance", "Microfinance institution")),
        ("DAB", bi("Distributeur automatique de billets", "Automated teller machine (ATM)")),
        ("HHI", bi("Indice de Herfindahl-Hirschman (concentration du marché)", "Herfindahl-Hirschman Index (market concentration)")),
        ("EHCVM", bi("Enquête harmonisée sur les conditions de vie des ménages", "Harmonized survey on household living conditions")),
        ("BCEAO", bi("Banque Centrale des États de l’Afrique de l’Ouest", "Central Bank of West African States")),
        ("ARCEP", bi("Autorité de régulation des communications électroniques et des postes", "Electronic communications and postal regulator")),
        ("UIT", bi("Union internationale des télécommunications", "International Telecommunication Union (ITU)")),
        ("UEMOA", bi("Union économique et monétaire ouest-africaine", "West African Economic and Monetary Union")),
        ("RGPH", bi("Recensement général de la population et de l’habitat", "General population and housing census")),
        ("FTTH", bi("Fibre jusqu’au domicile (Fiber To The Home)", "Fiber To The Home")),
        (bi("Couverture théorique", "Theoretical coverage"), bi("proxy : rayon de 20 km autour des antennes, toutes technologies", "proxy: 20 km radius around antennas, all technologies")),
    ], columns=[bi("code", "code"), bi("signifie", "meaning")])
    st.dataframe(glossaire, hide_index=True, use_container_width=True)

with st.container(border=True):
    st.markdown(f'<div class="bloc-titre">{html.escape(bi("Crédits", "Credits"))}</div>', unsafe_allow_html=True)
    texte_credits = bi(
        "Armoiries de la République togolaise : restitution d’Edem Fiadjoe, Wikimedia Commons, licence CC BY-SA 4.0. "
        "Logo Togo AI Lab : datalab.gouv.tg. Données : portail national de données géographiques du Togo et sources "
        "institutionnelles complémentaires (ARCEP, BCEAO, INSEED, 3i).",
        "Coat of arms of the Togolese Republic: rendition by Edem Fiadjoe, Wikimedia Commons, CC BY-SA 4.0 license. "
        "Togo AI Lab logo: datalab.gouv.tg. Data: Togo’s national geographic data portal and complementary institutional "
        "sources (ARCEP, BCEAO, INSEED, 3i).")
    st.markdown(f'<div class="reponse">{html.escape(texte_credits)}</div>', unsafe_allow_html=True)

pied()
