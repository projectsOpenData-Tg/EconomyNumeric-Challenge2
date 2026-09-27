## Tasks to do on the dashboard

Guard: for every task, correct the grammar in this file, and once done, update the task with the ✅ icon and the date the fix was applied.

1. ✅ (27/09/2026) Read the footer implementation in the Economy Challenge 1 folder: `/home/automater/Desktop/data-engineering-chall/EconomyNumeric-Challenge-1`
2. ✅ (27/09/2026) Apply the same configuration to the current project.

   Applied: the footer is now a centered card (white background, border, rounded corners, light shadow), matching `EconomyNumeric-Challenge-1/dashboard/theme.py` (`.pied-page`), with our own colours (dark blue title, grey subtitle). See `dashboard/theme.py` (`.pied-identite`).

---

- ✅ (27/09/2026) Remove the gap between the main content of each page and the left sidebar.

  Looked at the winning project [eco-num.streamlit.app](https://eco-num.streamlit.app/), mentioned in `REFERENTIEL_dashboard-territorial.md`, in the folder `/home/automater/Desktop/data-engineering-chall/EconomyNumeric-Challenge-1`. The gap came from Streamlit's default left/right padding on the main container, wider than needed. Fixed by setting `padding-left`/`padding-right` to `1.5rem`, the same value already used in Challenge 1's `theme.py` (`.block-container`). See `dashboard/theme.py` (`[data-testid="stMainBlockContainer"]`).

- ✅ (27/09/2026) Apply the same colour as the "Togo AI Lab" design to the topbar.

  Looked at `/home/automater/Desktop/data-engineering-chall/EconomyNumeric-Challenge-1` to see how it was done: the Togo AI Lab logo sits in a card with a gold border (`#FFCE00`), a white background and a light shadow (`.ai-lab-logo-card`, `dashboard/theme.py`). Applied the same card style here (`.ai-lab-logo-carte`), including the red fallback text while the logo file is still missing.

- ✅ (27/09/2026) Remove the remaining gap on wide screens: space still showing between the sidebar and the content, and a large empty gap on the right of the page.

  Root cause: the main container had a fixed `max-width: 1280px`, so on a screen wider than that, the leftover space was split as two symmetric gaps around the centred content block — the padding fix above only affected the space right next to that fixed-width block, not the whole issue. Matched Challenge 1's `theme.py` (`.block-container`), which keeps the width fluid (`max-width: 100%`) and relies only on the fixed side padding. Changed `max-width` to `100%` in `dashboard/theme.py` (`[data-testid="stMainBlockContainer"]`). Checked at 1440px and 2200px: content now fills the available width on both sides, with no dead space.

- ✅ (27/09/2026) Topbar background: set it to white so it stands out from the rest of the page; and fix the subtitle text and the Togo AI Lab card being cut off by the topbar's separator line.

  Both came from the same cause: the topbar had no background colour of its own (it showed the page's cream background), and its height was only as tall as its own padding, snug against the content — enough under most conditions, but the subtitle and the 56px AI Lab card had no safety margin, so a slightly taller font rendering (a fallback font, a different browser) could make them touch the line, looking "eaten" by it. Matched Challenge 1's `.st-key-bande_officielle` (`dashboard/theme.py`): white background, a light shadow instead of a plain line, a generous minimum height, and the row's content centred vertically within it rather than fitted tightly. Changed `div.st-key-topbar` in `dashboard/theme.py`. Checked at 1440px and 2740px (the width of the screenshot that reported the bug): the background is now white, and there is clear space around the subtitle and the card on both.



---
# Suivi des développements — tableau de bord

Ce fichier a deux usages, gardés côte à côte :

- **Tâches en cours** (ci-dessous) : la file d'attente où l'utilisateur dépose les corrections à faire sur le tableau de bord, et où chaque tâche est cochée une fois faite.
- **Journal par branche** (plus bas) : le compte rendu horodaté d'une branche de fonctionnalité, tenu par son auteur.

---

## Tâches en cours

Goal of this file is to keep track of all fixes applied to the dashboard and changes made after the first run of the app.

## Tasks to do on the dashboard

Guard: for every task, correct the grammar in this file, and once done, update the task with the ✅ icon and the date the fix was applied.

1. ✅ (27/09/2026) Read the footer implementation in the Economy Challenge 1 folder: `/home/automater/Desktop/data-engineering-chall/EconomyNumeric-Challenge-1`
2. ✅ (27/09/2026) Apply the same configuration to the current project.

   Applied: the footer is now a centered card (white background, border, rounded corners, light shadow), matching `EconomyNumeric-Challenge-1/dashboard/theme.py` (`.pied-page`), with our own colours (dark blue title, grey subtitle). See `dashboard/theme.py` (`.pied-identite`).

---

- ✅ (27/09/2026) Remove the gap between the main content of each page and the left sidebar.

  Looked at the winning project [eco-num.streamlit.app](https://eco-num.streamlit.app/), mentioned in `REFERENTIEL_dashboard-territorial.md`, in the folder `/home/automater/Desktop/data-engineering-chall/EconomyNumeric-Challenge-1`. The gap came from Streamlit's default left/right padding on the main container, wider than needed. Fixed by setting `padding-left`/`padding-right` to `1.5rem`, the same value already used in Challenge 1's `theme.py` (`.block-container`). See `dashboard/theme.py` (`[data-testid="stMainBlockContainer"]`).

- ✅ (27/09/2026) Apply the same colour as the "Togo AI Lab" design to the topbar.

  Looked at `/home/automater/Desktop/data-engineering-chall/EconomyNumeric-Challenge-1` to see how it was done: the Togo AI Lab logo sits in a card with a gold border (`#FFCE00`), a white background and a light shadow (`.ai-lab-logo-card`, `dashboard/theme.py`). Applied the same card style here (`.ai-lab-logo-carte`), including the red fallback text while the logo file is still missing.

- ✅ (27/09/2026) Remove the remaining gap on wide screens: space still showing between the sidebar and the content, and a large empty gap on the right of the page.

  Root cause: the main container had a fixed `max-width: 1280px`, so on a screen wider than that, the leftover space was split as two symmetric gaps around the centred content block — the padding fix above only affected the space right next to that fixed-width block, not the whole issue. Matched Challenge 1's `theme.py` (`.block-container`), which keeps the width fluid (`max-width: 100%`) and relies only on the fixed side padding. Changed `max-width` to `100%` in `dashboard/theme.py` (`[data-testid="stMainBlockContainer"]`). Checked at 1440px and 2200px: content now fills the available width on both sides, with no dead space.

- ✅ (27/09/2026) Topbar background: set it to white so it stands out from the rest of the page; and fix the subtitle text and the Togo AI Lab card being cut off by the topbar's separator line.

  Both came from the same cause: the topbar had no background colour of its own (it showed the page's cream background), and its height was only as tall as its own padding, snug against the content — enough under most conditions, but the subtitle and the 56px AI Lab card had no safety margin, so a slightly taller font rendering (a fallback font, a different browser) could make them touch the line, looking "eaten" by it. Matched Challenge 1's `.st-key-bande_officielle` (`dashboard/theme.py`): white background, a light shadow instead of a plain line, a generous minimum height, and the row's content centred vertically within it rather than fitted tightly. Changed `div.st-key-topbar` in `dashboard/theme.py`. Checked at 1440px and 2740px (the width of the screenshot that reported the bug): the background is now white, and there is clear space around the subtitle and the card on both.

---

## Journal de la branche `feature/jaune-clair-sidebar-tableaux`

Journal horodaté (UTC) des changements appliqués au tableau de bord (`dashboard/`).
Branche de validation : `feature/jaune-clair-sidebar-tableaux` (créée depuis `dev`), mergée dans `dev` (PR #1).

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
Goal of this file is to keep track of all fixes applied to the dashboard and changes made after the first run of the app.