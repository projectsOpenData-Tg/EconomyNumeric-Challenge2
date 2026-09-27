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
    "page.internet": {"fr": "Internet : usage et marché", "en": "Internet: use and market"},
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
    "lib.type_a_part": {"fr": "Type à part : hors des points formels", "en": "Separate type: outside formal points"},

    # ------------------------------------------------------------------------- Milieux
    "milieu.Grand Lomé": {"fr": "Grand Lomé", "en": "Greater Lomé"},
    "milieu.Autres villes": {"fr": "Autres villes", "en": "Other towns"},
    "milieu.Rural": {"fr": "Rural", "en": "Rural"},

    # ------------------------------------------------------------------------- Filtres actifs (page 1 et autres)
    "filtres.actifs": {"fr": "Filtres actifs", "en": "Active filters"},
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


def region(nom: str) -> str:
    """Nom de région : traduit seulement pour « Maritime hors Grand Lomé » (section 3.3) ; les autres noms de lieux
    ne sont pas traduits, ils restent tels quels dans les deux langues."""
    cle = f"region.{nom}"
    return _T[cle][langue()] if cle in _T else nom
