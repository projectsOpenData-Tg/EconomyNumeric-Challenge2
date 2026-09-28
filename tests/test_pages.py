"""Test de fumée du tableau de bord : les 11 pages et tous leurs sous-onglets, en français et en anglais.

Repris du défi 1 et étendu aux sous-onglets. C'est le contrôle qui détecte qu'une page ou un
onglet ne s'affiche plus : ni ruff ni un import ne chargent les données.

⚠️ **Les pages ne sont jamais exécutées isolément.** Le parcours passe par `app.py` puis
`switch_page`, comme un visiteur : hors de `st.navigation`, les filtres de la barre latérale
ne sont pas initialisés et une page testée seule échoue pour une raison qui n'existe pas en
production. Un onglet s'ouvre en posant son rang dans l'état de session (`<page>_onglets_rang`,
voir `onglets()` dans `dashboard/composants.py`) : seul l'onglet ouvert s'exécute.

⚠️ **Le dossier s'appelle `views/`, pas `pages/`** : un dossier `pages/` fait basculer
Streamlit sur sa navigation héritée et `app.py` n'est plus exécuté au premier run.

Vocabulaire : hors de la page Sources et méthode, aucune page n'affiche de sigle (DAB, IMF,
« point formel »), de nom de source (UIT, EHCVM, Findex…) ni de code interne (O4-03, R1, P13…).
L'ARCEP et la BCEAO restent nommées comme acteurs sur la page Recommandations.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

RACINE = Path(__file__).resolve().parent.parent
APP = RACINE / "dashboard" / "app.py"
PAGES = [f"views/{chemin.name}" for chemin in sorted((RACINE / "dashboard" / "views").glob("*.py"))]
ONGLETS = {"internet": 4, "marche": 5, "offre": 4, "population": 4, "priorites": 4, "diagnostic": 3, "recommandations": 4}

SIGLES = (r"\bDAB\b|\bATMs?\b|\bIMF\b|\bMFIs?\b|points? formels?|formal points?|guichets?|EHCVM|Findex|INSEED|\bUIT\b|\bITU\b|"
          r"Afrobarom|O[1-5]-0\d|\bD[123]\b|\bP1?[0-9]\b|\bR(?:[1-9]|10|4a|4b|7b)\b|min-max|\(A13\)")
SOURCES_ACTEURS = r"ARCEP|BCEAO"  # sources sur les pages d'analyse, acteurs sur la page Recommandations


def ouvrir(page: str, langue: str, onglet: int | None = None) -> AppTest:
    app = AppTest.from_file(str(APP), default_timeout=180)
    app.session_state["lang"] = langue
    if onglet is not None:
        app.session_state[f"{Path(page).stem}_onglets_rang"] = onglet
    app.run()
    if Path(page).stem != "synthese":
        app.switch_page(page)
        app.run()
    return app


def texte_affiche(app: AppTest) -> str:
    """Textes, tableaux et légendes des graphiques, sans balises HTML."""
    morceaux = [m.value for m in app.markdown] + [c.value for c in app.caption]
    for tableau in list(app.dataframe) + list(app.table):
        valeur = tableau.value.data if hasattr(tableau.value, "data") else tableau.value
        # `map(str)` et non `astype(str)` : avec pandas 3, une valeur manquante reste manquante après `astype(str)`
        morceaux.append(" | ".join(map(str, valeur.columns)) + " | " + " | ".join(map(str, valeur.values.ravel())))
    for graphique in app.get("plotly_chart"):
        morceaux += [str(trace.get("name", "")) for trace in json.loads(graphique.proto.spec)["data"]]
    return html.unescape(re.sub(r"<[^>]+>", " ", " ".join(morceaux)))


def verifier(app: AppTest, page: str, langue: str, contexte: str) -> None:
    assert not app.exception, f"{contexte} : " + " · ".join(str(getattr(e, "value", e)) for e in app.exception)
    if Path(page).stem == "methodologie":  # la seule page où codes et sources sont expliqués
        return
    texte = texte_affiche(app)
    trouves = set(re.findall(SIGLES, texte))
    if Path(page).stem != "recommandations":
        trouves |= set(re.findall(SOURCES_ACTEURS, texte))
    assert not trouves, f"{contexte} : sigle, source ou code affiché : {sorted(trouves)}"


@pytest.mark.lent
@pytest.mark.parametrize("langue", ["fr", "en"])
@pytest.mark.parametrize("page", PAGES)
def test_la_page_s_affiche_sans_erreur(page, langue):
    verifier(ouvrir(page, langue), page, langue, f"{page} [{langue}]")


@pytest.mark.lent
@pytest.mark.parametrize("langue", ["fr", "en"])
@pytest.mark.parametrize("page,onglet", [(f"views/{p}.py", i) for p, n in ONGLETS.items() for i in range(1, n)])
def test_chaque_onglet_s_affiche_sans_erreur(page, onglet, langue):
    """Le premier onglet est couvert par le test de la page ; ici, les suivants."""
    verifier(ouvrir(page, langue, onglet), page, langue, f"{page}, onglet {onglet + 1} [{langue}]")


def test_les_onze_pages_sont_toutes_declarees():
    """Un fichier ajouté dans `views/` sans entrée dans la navigation ne serait pas testé."""
    declarees = APP.read_text(encoding="utf-8")
    for page in PAGES:
        assert page in declarees, f"{page} n'est pas déclarée dans app.py"
    assert len(PAGES) == 11, f"{len(PAGES)} pages trouvées, 11 attendues"


def test_le_dossier_ne_s_appelle_pas_pages():
    assert not (RACINE / "dashboard" / "pages").exists(), (
        "Un dossier `dashboard/pages/` fait basculer Streamlit sur sa navigation héritée : les pages vivent dans `views/`.")


def test_chaque_table_lue_existe():
    """Le tableau de bord lit des tables déjà produites : une table renommée ou oubliée ne se verrait qu'en production."""
    appels = set()
    for fichier in (RACINE / "dashboard").rglob("*.py"):
        appels |= set(re.findall(r'lire\("([0-9a-z_]+)",\s*"([0-9A-Za-z_]+)"\)', fichier.read_text(encoding="utf-8")))
    assert appels, "aucun appel à lire() trouvé"
    manquantes = [f"{d}/{n}.csv" for d, n in sorted(appels) if not (RACINE / "data" / "analysis" / d / f"{n}.csv").exists()]
    assert not manquantes, f"tables introuvables dans data/analysis : {manquantes}"
    for niveau in ("communes", "prefectures", "unites_regionales"):
        assert (RACINE / "data" / "processed" / "geo" / f"{niveau}.geojson").exists(), f"contours {niveau} introuvables"
    assert (RACINE / "07_indicators.md").exists(), "07_indicators.md est lu par la page Sources et méthode"
