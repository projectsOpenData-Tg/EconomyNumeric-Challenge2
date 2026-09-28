"""Page 10 — Méthodologie : sources, conventions, les 27 indicateurs, glossaire, crédits (plan visuel, section 7,
page 10). Seule page où apparaissent les codes internes, toujours avec leur intitulé (section 3.1)."""
import html
import re
from pathlib import Path

import pandas as pd
import streamlit as st

from composants import ariane, entete, export_csv, pied
from i18n import bi, langue, t

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
        cellules = [c.strip().replace("**", "") for c in l.strip("|").split("|")]  # le gras du document n’a pas sa place dans un tableau (C16)
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

# Sources (demande du 28/09/2026) : les pages d’analyse désignent les sources externes de façon générique ; elles sont nommées
# ici, avec le manque des jeux de données du défi que chacune comble et les croisements qu’elle a permis (03, sections 11.B et 12)
with st.container(border=True):
    st.markdown(f'<div class="bloc-titre">{html.escape(bi("Les données du défi", "The challenge data"))}</div>'
                f'<div class="bloc-sous-titre">{html.escape(bi("Les six jeux de données ouverts fournis avec le sujet, et ce qui leur manquait pour répondre aux cinq objectifs.", "The six open datasets provided with the brief, and what they lacked to answer the five objectives."))}</div>',
                unsafe_allow_html=True)
    defi = pd.DataFrame([
        (bi("Individus utilisant Internet (% de la population)", "Individuals using the Internet (% of population)"),
         bi("usage d’Internet, national, annuel", "Internet use, national, annual"),
         bi("une estimation, pas une mesure ; aucun repère hors du Togo", "an estimate, not a measurement; no benchmark outside Togo")),
        (bi("Abonnés Internet par type d’accès", "Internet subscribers by access type"),
         bi("abonnements par type d’accès, technologie et opérateur, 2013-2019", "subscriptions by access type, technology and operator, 2013-2019"),
         bi("rien après 2019 : ni la 4G devenue majoritaire, ni la fibre récente", "nothing after 2019: neither 4G becoming the majority, nor recent fibre")),
        (bi("Récapitulatif téléphonie et GSM", "Telephony and GSM summary"),
         bi("abonnés, parts de marché, chiffre d’affaires, 2013-2019", "subscribers, market shares, revenue, 2013-2019"),
         bi("rien après 2019 ; ni investissement, ni prix de la data", "nothing after 2019; no investment, no data price")),
        (bi("Établissements financiers", "Financial institutions"),
         bi("banques, microfinance, assurances, distributeurs de billets, localisés (2021/2022)",
            "banks, microfinance, insurers, cash machines, located (2021/2022)"),
         bi("ni comptes, ni usage, ni nombre de guichets par agence", "no accounts, no use, no number of counters per branch")),
        (bi("Agents mobile money", "Mobile money agents"),
         bi("lieux localisés et leur opérateur (2021/2022)", "located places and their operator (2021/2022)"),
         bi("des lieux, pas des agents actifs ; ni comptes, ni transactions, ni frais", "places, not active agents; no accounts, transactions or fees")),
        (bi("Recensement de la population (2022)", "Population census (2022)"),
         bi("population par préfecture et par commune", "population by prefecture and commune"),
         bi("ni âge, ni milieu urbain ou rural dans le fichier ; aucune population annuelle",
            "no age, no urban or rural area in the file; no annual population")),
        (bi("Compléments du portail national de données géographiques", "National geographic data portal (additions)"),
         bi("contours administratifs, couverture théorique du réseau, fibre recensée", "administrative boundaries, theoretical network coverage, recorded fibre"),
         bi("couverture toutes technologies, estimée par un rayon de 20 km", "all-technology coverage, estimated with a 20 km radius")),
    ], columns=[bi("jeu de données", "dataset"), bi("ce qu’il donne", "what it provides"), bi("ce qui lui manquait", "what it lacked")])
    # Tableau statique : des phrases, qui doivent revenir à la ligne (un tableau interactif les coupe)
    st.table(defi.set_index(bi("jeu de données", "dataset")))

with st.container(border=True):
    st.markdown(f'<div class="bloc-titre">{html.escape(bi("Sources institutionnelles externes : leur rôle", "External institutional sources: their role"))}</div>'
                f'<div class="bloc-sous-titre">{html.escape(bi("Chacune comble un manque des données du défi et permet un croisement que le projet demandait. Les pages d’analyse les désignent de façon générique (dernière colonne) ; elles sont nommées ici.", "Each fills a gap in the challenge data and enables a cross-analysis the project required. Analysis pages refer to them generically (last column); they are named here."))}</div>',
                unsafe_allow_html=True)
    externes = pd.DataFrame([
        (bi("ARCEP (régulateur des télécoms) : observatoire trimestriel des marchés 2018-2026, rapports d’activité",
            "ARCEP (telecom regulator): quarterly market observatory 2018-2026, activity reports"),
         bi("séries télécoms arrêtées en 2019 ; aucun investissement, aucun mobile money",
            "telecom series stopping in 2019; no investment, no mobile money"),
         bi("parts de marché et concentration année par année ; taux d’investissement ; passage à la 4G et à la fibre ; abonnements face aux utilisateurs ; transactions du mobile money",
            "market shares and concentration year by year; investment rate; shift to 4G and fibre; subscriptions against users; mobile money transactions"),
         "1, 2, 3", bi("séries publiées du secteur ; série trimestrielle", "published sector series; quarterly series")),
        (bi("INSEED (statistique nationale) : livrets du recensement 2022, projections démographiques, séries 2010-2022, indices des prix",
            "INSEED (national statistics): 2022 census booklets, population projections, 2010-2022 series, price indices"),
         bi("population sans âge ni milieu par commune ; aucune population annuelle ; aucune inflation",
            "population without age or area by commune; no annual population; no inflation"),
         bi("points mobile money pour 10 000 adultes ; écart entre villes et campagnes ; croissance réelle du chiffre d’affaires",
            "mobile money points per 10,000 adults; town-countryside gap; real revenue growth"),
         "1, 2, 3, 4", bi("recensement ; série annuelle", "census; annual series")),
        (bi("Enquêtes auprès des ménages : conditions de vie 2018/19 et 2021/22 (INSEED, UEMOA, Banque mondiale), indicateurs multiples 2017 (INSEED, UNICEF)",
            "Household surveys: living conditions 2018/19 and 2021/22 (INSEED, WAEMU, World Bank), multiple indicators 2017 (INSEED, UNICEF)"),
         bi("aucune mesure de l’usage, des compétences ni de la réception par région",
            "no measure of use, skills or reception by region"),
         bi("freins à l’usage d’Internet par région ; offre de mobile money face à son usage ; couverture théorique face à la réception déclarée",
            "barriers to Internet use by region; mobile money supply against its use; theoretical coverage against reported reception"),
         "1, 2, 3, 5", bi("enquête nationale auprès des ménages", "national household survey")),
        (bi("Afrobaromètre : six vagues, 2012-2024", "Afrobarometer: six waves, 2012-2024"),
         bi("aucun point mesuré de l’usage d’Internet", "no measured point of Internet use"),
         bi("contrôle de la tendance de l’estimation internationale ; date du ralentissement", "check on the international estimate’s trend; timing of the slowdown"),
         "1", bi("enquête d’opinion auprès des adultes", "adult opinion survey")),
        (bi("BCEAO (banque centrale) : services financiers numériques et inclusion financière, 2024",
            "BCEAO (central bank): digital financial services and financial inclusion, 2024"),
         bi("aucun compte ni activité du mobile money", "no mobile money accounts or activity"),
         bi("comptes ouverts face aux comptes actifs : accès acquis, usage faible", "opened against active accounts: access gained, low use"),
         "3", bi("relevé de la banque centrale", "central bank records")),
        (bi("Banque mondiale : enquête Findex 2011-2024 ; usage d’Internet et agences bancaires des 8 pays de l’UEMOA et de l’Afrique subsaharienne",
            "World Bank: Findex survey 2011-2024; Internet use and bank branches for the 8 WAEMU countries and Sub-Saharan Africa"),
         bi("aucune détention de compte par les adultes ; aucun repère hors du Togo", "no account ownership by adults; no benchmark outside Togo"),
         bi("mobile money face au compte bancaire ; rang du Togo dans l’UEMOA ; dépassement de l’Afrique subsaharienne ; coût du smartphone",
            "mobile money against bank accounts; Togo’s rank in WAEMU; overtaking Sub-Saharan Africa; smartphone cost"),
         "1, 3, 4", bi("enquête internationale ; estimation internationale", "international survey; international estimate")),
        (bi("UIT (Union internationale des télécommunications) : paniers de prix 2008-2025",
            "ITU (International Telecommunication Union): price baskets 2008-2025"),
         bi("aucun prix de la data ni revenu par habitant", "no data price or income per person"),
         bi("coût de 1 Go face au seuil de 2 % du revenu mensuel ; année où il serait atteint", "cost of 1 GB against the 2% of monthly income threshold; year it would be reached"),
         "2, 5", bi("panier de prix international", "international price basket")),
        (bi("Opérateurs Moov Africa (Flooz) et YAS (Mixx) : grilles tarifaires publiées, relevées le 26/09/2026",
            "Operators Moov Africa (Flooz) and YAS (Mixx): published fee grids, recorded on 26/09/2026"),
         bi("aucun frais du mobile money", "no mobile money fees"),
         bi("frais du petit retrait face au repère de 3 %, fondement de la recommandation sur les frais",
            "small-withdrawal fees against the 3% reference, basis of the fees recommendation"),
         "3, 5", bi("grille publiée par l’opérateur", "grid published by the operator")),
    ], columns=[bi("source", "source"), bi("manque comblé", "gap filled"), bi("croisements rendus possibles", "cross-analyses enabled"),
                bi("objectifs", "objectives"), bi("désignée sur les pages comme", "referred to on pages as")])
    st.table(externes.set_index(bi("source", "source")))
    st.caption(bi("Niveaux de preuve : les recensements et les séries publiées sont des comptages ; les enquêtes sont des estimations sur "
                  "échantillon, avec leur marge d’erreur ; les estimations internationales et la couverture théorique sont des approximations. "
                  "Deux sources d’une même grandeur ne sont jamais raccordées.",
                  "Levels of evidence: censuses and published series are counts; surveys are sample estimates, with their margin of error; "
                  "international estimates and theoretical coverage are approximations. Two sources for the same quantity are never joined."))

with st.container(border=True):
    st.markdown(f'<div class="bloc-titre">{html.escape(bi("Conventions", "Conventions"))}</div>', unsafe_allow_html=True)
    texte_conventions = bi(
        "Seuils déclarés avant le résultat : 40 % et 60 % pour l’usage d’Internet, 2 % pour le coût de 1 Go, 3 % pour le retrait de "
        "petit montant, 15 % pour l’investissement, 50 sites radio par an, 85 % et 50 % pour la couverture, 10 000 et 30 000 "
        "habitants par agence financière. Les classes de priorité viennent d’un rang percentile (100 × (rang − 1) / (n − 1)), moyenné sur "
        "trois dimensions à poids égaux : 70 ou plus = priorité haute, de 40 à 70 = priorité moyenne, moins de 40 = priorité faible. "
        "Une variante décidée après avoir vu le résultat (P9, P13) est toujours affichée à côté de la règle de référence, jamais à "
        "la place.",
        "Thresholds declared before the result: 40% and 60% for Internet use, 2% for the cost of 1 GB, 3% for small withdrawals, "
        "15% for investment, 50 radio sites a year, 85% and 50% for coverage, 10,000 and 30,000 people per financial branch. Priority "
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
    if langue() == "en":
        st.caption("This table is read as is from the project’s indicator document, which is written in French: it is not translated.")
    export_csv(ind, "indicateurs_27.csv", "export_indicateurs")

with st.container(border=True):
    st.markdown(f'<div class="bloc-titre">{html.escape(bi("Glossaire des codes", "Code glossary"))}</div>', unsafe_allow_html=True)
    glossaire = pd.DataFrame([
        ("O1–O5", bi("Objectifs 1 à 5 du projet (usage, marché, offre financière, rapport population/offre, priorisation)",
                     "Project objectives 1 to 5 (use, market, financial supply, population/supply ratio, prioritization)")),
        (bi("Agence financière", "Financial branch"), bi("Agence ou guichet en service d’une banque, d’une institution de microfinance ou d’une "
                                                         "compagnie d’assurance (« point formel » dans les documents d’analyse) ; les distributeurs de billets n’en font pas partie",
                                                         "Operating branch or counter of a bank, microfinance institution or insurer (“formal point” in the analysis "
                                                         "documents); cash machines are not included")),
        (bi("Point mobile money", "Mobile money point"), bi("Lieu où un agent mobile money sert la clientèle ; un lieu servi par les deux opérateurs compte une fois",
                                                            "Place where a mobile money agent serves customers; a place served by both operators counts once")),
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
