# Suivi des développements — tableau de bord

Journal horodaté (UTC) des changements appliqués au tableau de bord (`dashboard/`).
Branche de validation : `feature/jaune-clair-sidebar-tableaux` (créée depuis `dev`).

---

## 2026-09-27 18:03 UTC — Retours de validation (itération 2)

**Bouton d'ouverture/fermeture de la barre latérale**
- Le jaune clair (`#fce588`) passe du fond à la **bordure** du bouton : fond transparent, bordure de 1,5 px, coins arrondis.
- Le bouton reste visible en permanence (barre ouverte et fermée), pas seulement au survol.
- Fichier : `dashboard/theme.py`.

**Logo de la barre latérale**
- L'icône placée avant « Togo Digital & Financial » est remplacée par le **drapeau du Togo** (le même que celui de la barre du haut) : cinq bandes vert/jaune, canton rouge et étoile blanche.
- Même remplacement pour l'icône affichée quand la barre latérale est fermée.
- Fichiers : `dashboard/static/logo.svg`, `logo_fr.svg`, `logo_en.svg`, `icone.svg`.

**Onglet actif de la barre latérale**
- Correction de l'itération 1 : la page ouverte dans la barre latérale (ex. « Synthèse nationale ») est encadrée d'une **bordure arrondie jaune clair**. Ce style ne s'applique qu'à la barre latérale, pas au contenu principal.
- Les bordures jaunes ajoutées sur les tableaux du contenu principal à l'itération 1 sont retirées (réglage `dataframeBorderColor` supprimé de `.streamlit/config.toml`).
- Fichiers : `dashboard/theme.py`, `.streamlit/config.toml`.

**Graphiques et cartes sur fond blanc**
- Tous les graphiques Plotly (courbes, barres, cartes) ont désormais un fond blanc (`paper_bgcolor`, `plot_bgcolor` et fond des cartes géographiques à `#ffffff`). Ils se distinguent ainsi du fond beige de la page.
- Le conteneur de chaque graphique reçoit aussi un fond blanc à coins arrondis.
- Fichiers : `dashboard/theme.py`, `dashboard/composants.py`, `dashboard/views/internet.py`, `dashboard/views/projections.py`.

---

## 2026-09-27 17:08 UTC — Couleur jaune clair (itération 1)

- Bouton d'ouverture/fermeture de la barre latérale en jaune clair (`#fce588`), visible en permanence et plus seulement au survol.
- Bordures et quadrillage des tableaux en jaune clair. *Retiré à l'itération 2 : la demande concernait l'onglet actif de la barre latérale.*
- Fichiers : `dashboard/theme.py`, `.streamlit/config.toml`.
