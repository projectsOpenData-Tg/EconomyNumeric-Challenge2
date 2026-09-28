"""Dictionnaire bilingue (français, anglais) — plan visuel, section 3.3, « Deux langues ».

Portée du dictionnaire central (`t()`) : le chrome commun à toutes les pages (barre du haut, pied de page, barre
latérale) et le vocabulaire partagé entre plusieurs pages (classes de priorité, statuts, régions, en-têtes de bloc,
libellés imposés par les analyses). Le texte propre à une seule page (titres, phrases des chiffres clés, constats,
réserves) est écrit deux fois dans la page elle-même, avec `FR = langue() == "fr"` puis un choix conditionnel : un
texte de page n’a pas vocation à être réutilisé ailleurs, et un dictionnaire central grossirait sans bénéfice.

La langue est conservée dans l’état de session, comme les filtres ; le français est la langue par défaut. Les noms
de lieux ne sont pas traduits, sauf « Maritime hors Grand Lomé » (imposé par la section 3.3). Les nombres suivent la
langue via `fr()` / `nombre()` de `donnees.py`.
"""
import streamlit as st

LANGUES = ("fr", "en")
DEFAUT = "fr"

_T: dict[str, dict[str, str]] = {
    # ------------------------------------------------------------------------- Barre du haut, pied de page
    "topbar.ministry": {"fr": "Ministère de l’Efficacité du Service Public et de la Transformation Numérique",
                        "en": "Ministry of Public Service Efficiency and Digital Transformation"},
    "topbar.brand": {"fr": "Togo Digital &amp; Financial Inclusion", "en": "Togo Digital &amp; Financial Inclusion"},
    "topbar.subtitle": {"fr": "Accès numérique et inclusion financière au Togo",
                        "en": "Digital access and financial inclusion in Togo"},
    "footer.title": {"fr": "Togo AI Lab — Data Challenge | Économie numérique — Défi 2",
                     "en": "Togo AI Lab — Data Challenge | Digital Economy — Challenge 2"},
    "footer.subtitle": {"fr": "Diagnostic territorial et aide à la décision pour l’accès numérique et l’inclusion "
                              "financière au Togo",
                        "en": "Territorial diagnostic and decision support for digital access and financial "
                              "inclusion in Togo"},
    "footer.sources": {"fr": "Données : portail national de données géographiques du Togo et sources "
                             "institutionnelles complémentaires. Mise à jour : septembre 2026.",
                       "en": "Data: Togo’s national geographic data portal and complementary institutional "
                             "sources. Updated: September 2026."},

    # ------------------------------------------------------------------------- Barre latérale
    "sidebar.filters": {"fr": "Filtres", "en": "Filters"},
    "sidebar.region": {"fr": "Région", "en": "Region"},
    "sidebar.grille": {"fr": "Maille de la carte", "en": "Map scale"},
    "sidebar.priorite": {"fr": "Priorité", "en": "Priority"},
    "sidebar.milieu": {"fr": "Milieu", "en": "Area type"},
    "sidebar.reinitialiser": {"fr": "Réinitialiser les filtres", "en": "Reset filters"},
    "sidebar.caption": {"fr": "39 préfectures · 117 communes · points de service 2021/2022 · population 2022",
                        "en": "39 prefectures · 117 communes · service points 2021/2022 · population 2022"},
    "sidebar.langue": {"fr": "Langue", "en": "Language"},

    # ------------------------------------------------------------------------- Fil d’Ariane
    "ariane.racine": {"fr": "Tableau de bord", "en": "Dashboard"},
    "ariane.suivant": {"fr": "Page suivante", "en": "Next page"},

    # ------------------------------------------------------------------------- Menu (groupes et titres de page)
    "menu.principal": {"fr": "Principal", "en": "Main"},
    "menu.analyses": {"fr": "Analyses", "en": "Analysis"},
    "menu.pilotage": {"fr": "Pilotage", "en": "Action"},
    "menu.methodologie": {"fr": "Méthodologie", "en": "Methodology"},
    "page.synthese": {"fr": "Synthèse nationale", "en": "National overview"},
    "page.internet": {"fr": "Usage d’Internet", "en": "Internet use"},
    "page.marche": {"fr": "Marché des télécoms", "en": "Telecom market"},
    "page.offre": {"fr": "Offre financière", "en": "Financial services"},
    "page.population": {"fr": "Population et offre", "en": "Population and services"},
    "page.carte": {"fr": "Carte", "en": "Map"},
    "page.priorites": {"fr": "Priorités", "en": "Priorities"},
    "page.diagnostic": {"fr": "Diagnostic", "en": "Diagnosis"},
    "page.recommandations": {"fr": "Recommandations", "en": "Recommendations"},
    "page.projections": {"fr": "Estimations et projections", "en": "Estimates and projections"},
    "page.methodologie": {"fr": "Sources et méthode", "en": "Sources and method"},

    # ------------------------------------------------------------------------- Gabarit (blocs communs à chaque page)
    "bloc.constat": {"fr": "Constat", "en": "Finding"},
    "bloc.synthese": {"fr": "Synthèse chiffrée", "en": "Key figures"},
    "bloc.limite": {"fr": "Limite de cette page", "en": "Limits of this page"},
    "bloc.ne_montre_pas": {"fr": "Ce que cette page ne montre pas", "en": "What this page does not show"},
    "export.csv": {"fr": "Exporter (CSV)", "en": "Export (CSV)"},
    "lien.voir_fiche": {"fr": "Voir la fiche du territoire", "en": "See the territory’s profile"},
    "lien.voir_carte": {"fr": "Voir sur la carte", "en": "See on the map"},
    "lien.voir_recommandations": {"fr": "Voir les recommandations", "en": "See the recommendations"},

    # ------------------------------------------------------------------------- Classes de priorité et statuts
    "priorite.haute": {"fr": "Priorité haute", "en": "High priority"},
    "priorite.moyenne": {"fr": "Priorité moyenne", "en": "Medium priority"},
    "priorite.faible": {"fr": "Priorité faible", "en": "Low priority"},
    "priorite.non_classee": {"fr": "Non classée", "en": "Not ranked"},
    "priorite.absolue": {"fr": "Priorité absolue", "en": "Absolute priority"},
    "priorite.hors_selection": {"fr": "Hors sélection", "en": "Outside selection"},
    "confiance.elevee": {"fr": "Confiance élevée", "en": "High confidence"},
    "confiance.moyenne": {"fr": "Confiance moyenne", "en": "Medium confidence"},
    "confiance.faible": {"fr": "Confiance faible", "en": "Low confidence"},

    # ------------------------------------------------------------------------- Régions (une seule à traduire)
    "region.Maritime hors Grand Lomé": {"fr": "Maritime hors Grand Lomé", "en": "Maritime excluding Greater Lomé"},

    # ------------------------------------------------------------------------- Libellés imposés par les analyses (3.3)
    "lib.acces_declare": {"fr": "Accès déclaré à Internet", "en": "Self-reported Internet access"},
    "lib.usage_toute_freq": {"fr": "Usage d’Internet, toute fréquence", "en": "Internet use, any frequency"},
    "lib.couverture_theorique": {"fr": "couverture théorique", "en": "theoretical coverage"},
    "lib.sans_fibre": {"fr": "sans fibre recensée", "en": "no recorded fibre"},
    "lib.non_raccordee": {"fr": "non raccordée", "en": "not connected"},
    "lib.points_service": {"fr": "points de service", "en": "service points"},
    "lib.type_a_part": {"fr": "Type à part : pas une agence", "en": "Separate type: not a branch"},

    # ------------------------------------------------------------------------- Milieux
    "milieu.Grand Lomé": {"fr": "Grand Lomé", "en": "Greater Lomé"},
    "milieu.Autres villes": {"fr": "Autres villes", "en": "Other towns"},
    "milieu.Rural": {"fr": "Rural", "en": "Rural"},

    # ------------------------------------------------------------------------- Filtres actifs (page 1 et autres)
    "filtres.actifs": {"fr": "Filtres actifs", "en": "Active filters"},

    # ------------------------------------------------------------------------- Sous-onglets d’une page
    "onglets.aide": {"fr": "{n} vues — cliquez sur un onglet", "en": "{n} views — click a tab"},
    "onglets.repere": {"fr": "{vue} · vue {i} sur {n}", "en": "{vue} · view {i} of {n}"},

    # ------------------------------------------------------------------------- Frein présumé à l’usage d’Internet (pages Internet, Diagnostic)
    "frein.capacite_cout": {"fr": "capacité et coût (présumés)", "en": "skills and cost (presumed)"},
    "frein.cout": {"fr": "coût (présumé)", "en": "cost (presumed)"},
    "frein.non_etabli": {"fr": "non établi (couverture ≤ 85 %)", "en": "not established (coverage ≤ 85%)"},
    "frein.non_recherche": {"fr": "non recherché (usage élevé)", "en": "not examined (high use)"},
}


def langue() -> str:
    return st.session_state.get("lang", DEFAUT)


def definir_langue(l: str) -> None:
    st.session_state["lang"] = l


def t(cle: str, **kwargs) -> str:
    """Texte du dictionnaire central, dans la langue courante (repli sur le français, puis sur la clé elle-même)."""
    entree = _T.get(cle, {})
    texte = entree.get(langue()) or entree.get("fr") or cle
    return texte.format(**kwargs) if kwargs else texte


def bi(fr_txt: str, en_txt: str) -> str:
    """Choix bilingue ponctuel, pour un texte propre à une page (pas dans le dictionnaire central)."""
    return fr_txt if langue() == "fr" else en_txt


def frein(lecture: str) -> str:
    """Frein présumé à l’usage d’Internet, en clair : les tables écrivent « la règle du 02 », un renvoi à un document
    qui n’a pas sa place sur une page (plan visuel, section 3.1)."""
    for debut, cle in (("frein de capacité", "frein.capacite_cout"), ("frein de coût", "frein.cout"),
                       ("aucun frein affirmé", "frein.non_etabli"), ("aucun frein recherché", "frein.non_recherche")):
        if str(lecture).startswith(debut):
            return t(cle)
    return lecture


def region(nom: str) -> str:
    """Nom de région : traduit seulement pour « Maritime hors Grand Lomé » (section 3.3) ; les autres noms de lieux
    ne sont pas traduits, ils restent tels quels dans les deux langues."""
    cle = f"region.{nom}"
    return _T[cle][langue()] if cle in _T else nom


# Valeurs écrites en français dans les tables (classes du 02, statuts, couverture, priorités, confiance, nature, horizon) :
# un libellé en clair dans chaque langue (demande du 28/09/2026, corrections C9 et C13 : en anglais, ces valeurs restaient en
# français). Le libellé français peut différer de la table quand celle-ci porte un code ou un sigle (« (A13) », « 0 point formel »).
_VALEURS: dict[str, tuple[str, str]] = {
    # Habitants par agence financière (O4-01)
    "bien desservi": ("bien desservi", "well served"), "tendu": ("tendu", "stretched"), "sous-desservi": ("sous-desservi", "under-served"),
    "non défini et critique (0 point)": ("aucune agence", "no branch"),
    # Points mobile money par agence financière (O4-03)
    "réseaux comparables": ("réseaux comparables", "comparable networks"),
    "mobile money prépondérant": ("mobile money prépondérant", "mobile money predominant"),
    "suppléance quasi totale": ("le mobile money supplée presque tout", "mobile money almost fully substitutes"),
    "mobile money uniquement (0 point formel)": ("mobile money seul", "mobile money only"),
    # Habitants par point mobile money (O4-04)
    "maillage dense": ("maillage dense", "dense network"), "acceptable": ("acceptable", "acceptable"),
    "maillage insuffisant": ("maillage insuffisant", "insufficient network"),
    # Statut d’accès financier (O4-05)
    "desserte diversifiée": ("desserte diversifiée", "diversified service"), "desserte faible": ("desserte faible", "weak service"),
    "mobile money dominant": ("mobile money dominant", "mobile money dominant"),
    "mobile money uniquement": ("mobile money seul", "mobile money only"),
    # Couverture théorique (O2-06), classes du 02
    "territoire couvert (proxy)": ("couverte (plus de 85 %)", "covered (over 85%)"),
    "couverture partielle (proxy)": ("partielle (50 à 85 %)", "partial (50 to 85%)"),
    "zone blanche prioritaire (proxy)": ("zone blanche (moins de 50 %)", "white zone (under 50%)"),
    "non déterminable (A13)": ("inconnue", "unknown"), "non déterminable": ("inconnue", "unknown"),
    # Classes de priorité, confiance, robustesse (08)
    "priorité 1": ("priorité haute", "high priority"), "priorité 2": ("priorité moyenne", "medium priority"),
    "priorité 3": ("priorité faible", "low priority"), "non déterminable (couverture)": ("non classée", "not ranked"),
    "élevée": ("élevée", "high"), "moyenne": ("moyenne", "medium"), "faible": ("faible", "low"),
    "robuste": ("robuste", "robust"), "instable": ("instable", "unstable"),
    # Nature et horizon des recommandations (10)
    "immédiate": ("immédiate", "immediate"), "conditionnelle": ("conditionnelle", "conditional"), "veille": ("veille", "watch"),
    "1 an": ("1 an", "1 year"), "3 ans": ("3 ans", "3 years"), "5 ans": ("5 ans", "5 years"),
    "chaque année": ("chaque année", "every year"), "1 à 3 ans": ("1 à 3 ans", "1 to 3 years"),
    # Diagnostic (09) : signaux des communes, dimensions du score, leviers, lecture des facteurs
    "sans point formel et cellule critique": ("sans agence, réseau faible", "no branch, weak network"),
    "sans point formel": ("sans agence", "no branch"),
    "cellule critique": ("agence présente, réseau faible", "branch present, weak network"),
    "accès formel": ("agences financières", "financial branches"), "maillage mobile money": ("mobile money", "mobile money"),
    "couverture (proxy)": ("couverture (estimation)", "coverage (estimate)"),
    "infrastructure financière : points formels": ("ouvrir des agences financières", "open financial branches"),
    "infrastructure financière : points formels de proximité": ("ouvrir des agences de proximité", "open nearby branches"),
    "réseau d'agents mobile money": ("étendre le réseau d’agents mobile money", "extend the mobile money agent network"),
    "infrastructure réseau": ("étendre le réseau télécom, après mesure", "extend the telecom network, after measurement"),
    "mesurer la couverture réelle": ("mesurer la couverture réelle", "measure actual coverage"),
    "compétences numériques": ("compétences numériques", "digital skills"), "tarification": ("prix de la data", "data price"),
    "se répète": ("se répète", "recurs"), "partagé": ("partagé", "shared"), "non commun": ("non commun", "not common"),
    # Scénarios d’usage d’Internet (10)
    "usage généralisé": ("usage généralisé", "widespread use"), "rattrapage": ("rattrapage", "catching up"),
}


def valeur(v) -> str:
    """Libellé en clair d’une valeur de table, dans la langue courante ; la valeur telle quelle si elle est inconnue."""
    paire = _VALEURS.get(str(v))
    return (paire[0] if langue() == "fr" else paire[1]) if paire else v
