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

## Objectif 1 : analyses déjà produites mais absentes du tableau de bord

Relevé du 27/09/2026. Documents lus : `05_data_analysis.md` (figures 4, 5 et 11), `06_data_spatial_analysis.md` (cartes 9 et 12) et `11_plan_visuel_dashboard.md` (page 2). Rappel de l'objectif 1 : « retracer l'évolution de l'usage d'Internet au Togo et repérer les périodes d'accélération ou de stagnation ».

**Ce que le tableau de bord montre déjà pour l'objectif 1** :
- page Internet : la courbe d'usage de l'UIT depuis 2010 (repère Afrique subsaharienne, seuil de 40 %, 5 événements) ; la croissance annuelle classée (accélération, rythme habituel, ralentissement) ; l'accès déclaré par région, pour la dernière vague seulement, en barres ;
- page Synthèse : les chiffres de tête 39,5 % (usage) et 81,3 % (3G ou 4G) ;
- page Diagnostic : un tableau accès, alphabétisation et frein présumé par région.

**Ce qui manque** (du plus important au moins important) :

| # | Analyse | Source | Page proposée | Priorité | Statut |
| - | ------- | ------ | ------------- | -------- | ------ |
| 1 | Carte de l'accès déclaré par région, deux vagues | 06, carte 9 | Internet | haute : prévue au plan 11, remplacée par des barres | ✅ (27/09/2026) |
| 2 | Tableau des freins par région | plan 11 (page 2), table du 07 | Internet | haute : prévu au plan, chargé par la page mais jamais affiché | ✅ (27/09/2026) |
| 3 | L'usage selon les enquêtes auprès des ménages | 05, figure 4 (panneau de droite) | Internet | haute : la réserve du chiffre de tête y renvoie | ✅ (27/09/2026) |
| 4 | Le Togo face aux pays de l'UEMOA | 05, figure 11 | Internet | moyenne | ✅ (27/09/2026) |
| 5 | Le mix technologique des abonnements data | 05, figure 5 | Internet | moyenne | ✅ (27/09/2026) |
| 6 | L'alphabétisation par région | 06, carte 12 (moitié gauche) | Internet | moyenne : preuve du constat affiché sur la page | ✅ (27/09/2026) |
| 7 | La courbe de l'UIT depuis 1996 | 05, figure 4 (panneau de gauche) | Internet | haute : demandée le 27/09/2026 | ✅ (27/09/2026) |

**Item 7, ajouté le 27/09/2026** : la figure 4 du 05 trace l'usage depuis 1996 (premiers utilisateurs : 0,01 % ; usage nul de 1990 à 1995). La page Internet la coupe à 2010 : un choix fait à la construction, pour caler la courbe sur la période de référence des classes de croissance (2010-2024), mais jamais écrit dans le plan 11, qui ne fixait pas d'année de départ. Correction : la courbe part de 1996 (table `s4_usage_internet_d1`, 1996-2024), le repère Afrique subsaharienne à partir de 2005, sa première année disponible. La croissance annuelle classée reste sur 2010-2024 : avant 2005, les taux portent sur des niveaux inférieurs à 2 % et ne se lisent pas.

### 1. Carte de l'accès déclaré à Internet par région, 2018/19 et 2021/22 (06, carte 9)

- **Ce qu'elle montre** : l'accès progresse dans toutes les régions (de +7,3 points dans les Savanes à +14,7 dans le Grand Lomé), mais l'écart entre le Grand Lomé et les Savanes se creuse : 45,0 points en 2018/19 (52,0 % contre 7,0 %), 52,3 points en 2021/22 (66,7 % contre 14,3 %).
- **Aujourd'hui** : un graphique en barres de la seule vague 2021/22, sans marge d'erreur ni évolution. Le plan 11 (page 2) prévoyait une carte.
- **Proposition** : deux cartes côte à côte, avec les mêmes classes (moins de 15 %, 15 à 25 %, 25 à 35 %, 35 à 50 %, 50 % et plus) et, sur chaque région, « valeur (± marge) » puis le gain en points. Un chiffre clé ajouté : « écart Grand Lomé – Savanes : 45,0 puis 52,3 points ». Le filtre de région met toujours la région choisie en évidence.
- **Données** : `o1_05_acces_regions` (les deux vagues y sont déjà ; la page n'en lit qu'une) et `s6_usage_internet_regions` (gain, marge).
- **Limite à afficher** : 6 régions seulement, aucune enquête ne descend plus bas ; l'accès déclaré n'est pas l'usage.

### 2. Tableau des freins par région (plan 11, page 2)

- **Ce qu'il montre** : pour chaque région, l'accès, la couverture théorique, l'alphabétisation, les compétences numériques des 15-49 ans par sexe (de 0,4 % pour les femmes des Savanes à 9,6 % pour les hommes de Kara), le coût de 1 Go et le frein présumé qui en découle : frein de capacité dans les Savanes et les Plateaux, frein de coût partout où la règle s'applique. Au niveau national : 45,1 % des adultes ont un smartphone, et 32,1 % n'en ont pas à cause du coût (Findex 2024).
- **Aujourd'hui** : la table est lue par la page Internet (`freins`, dans `dashboard/views/internet.py`) mais jamais affichée. La page Diagnostic n'en montre que trois colonnes.
- **Proposition** : un tableau coloré sous la carte de l'item 1, avec export CSV ; les deux chiffres du smartphone sur une ligne sous le tableau.
- **Données** : `o1_06_freins`, `o1_06_smartphone_national`.
- **Limite à afficher** : un frein « présumé » découle d'une règle, il n'est pas démontré ; l'alphabétisation n'est qu'un proxy de compétence ; les compétences numériques datent de 2017.

### 3. L'usage selon les enquêtes auprès des ménages (05, figure 4, panneau de droite)

- **Ce qu'elle montre** : l'usage a au moins doublé depuis 2017, quelle que soit la source (Afrobaromètre : de 29,0 % à 60,8 % en 2024 ; enquête EHCVM : de 23,7 % à 35,3 % ; Findex 2024 : 43,7 %). Le ralentissement se confirme, mais plus tard que dans la série de l'UIT : l'Afrobaromètre croît de 16,2 % par an de 2017 à 2020, de 11,2 % de 2020 à 2022, puis de 4,0 % de 2022 à 2024.
- **Aujourd'hui** : absente. Pourtant la réserve du premier chiffre de tête (page Synthèse) y renvoie : « les enquêtes auprès des ménages en confirment la tendance, pas le niveau ». Le lecteur ne voit ces enquêtes nulle part.
- **Proposition** : un second graphique à côté de la courbe de l'UIT, jamais sur le même graphique (définitions différentes), une série par source, avec l'intervalle de confiance, et les libellés imposés distincts (« Usage d'Internet, toute fréquence », « Accès déclaré à Internet »). Options : l'écart femmes-hommes de la MICS6 (15-49 ans, 2017 : 14,1 % contre 27,6 %) ; la courbe de l'UIT prolongée jusqu'en 1996 (premiers utilisateurs, 0,01 %), aujourd'hui coupée à 2010.
- **Données** : `s4_usage_internet_enquetes`, `o1_02_enquetes_periodes`.
- **Limite à afficher** : chaque enquête a sa définition et sa tranche d'âge ; elles ne se comparent jamais entre elles.

### 4. Le Togo face aux pays de l'UEMOA (05, figure 11)

- **Ce qu'elle montre** : le Togo est premier de l'UEMOA en 2000 (0,8 %), 5e ou 6e de 2013 à 2018 (ses voisins progressent plus vite), 4e en 2019, 3e depuis 2022 (39,5 % en 2024, derrière le Sénégal, 60,1 %, et la Côte d'Ivoire, 41,4 %).
- **Aujourd'hui** : seul le repère Afrique subsaharienne figure sur la page Internet. La page Estimations et projections montre des trajectoires futures, pas le rang passé.
- **Proposition** : les courbes des 8 pays, le Togo en trait épais et en couleur, les 7 autres en gris (nom au survol, légende triée par la valeur 2024) ; à côté, le rang du Togo en escalier, ou un chiffre clé « 3e sur 8 ». Option : un sélecteur pour colorer un pays de comparaison.
- **Données** : `s4_benchmark_usage_internet` (le rang y est déjà calculé).
- **Limite à afficher** : des deux côtés, la plupart des valeurs sont des estimations de l'UIT ; un rang compare des estimations, pas des mesures.

### 5. Le mix technologique des abonnements data mobile (05, figure 5)

- **Ce qu'elle montre** : la 4G passe de 3,4 % des abonnements (fin 2018) à 56,9 % (fin 2025) ; la 2G recule de 31,0 % à 18,7 %. C'est l'indicateur de l'objectif 1 sur la part des abonnements par technologie ; il sert aussi l'objectif 2 (passage aux nouvelles technologies).
- **Aujourd'hui** : seul le chiffre de 81,3 % en 3G ou 4G (page Synthèse), sans son évolution.
- **Proposition** : des barres empilées à 100 % par année (2G, 3G, 4G, et « 3G et 4G de Moov, non ventilées » avant 2020), la rupture de série marquée début 2020, un repère à 80 % (passage au haut débit).
- **Données** : `o1_04_technologies`.
- **Limite à afficher** : un abonnement n'est pas une personne ; rupture de série en 2020 (reclassement de la 3G de Togocel).

### 6. L'alphabétisation par région (06, carte 12, moitié gauche)

- **Ce qu'elle montre** : 71,0 % au niveau national ; les Savanes sont très en dessous (41,2 %, +2,1 points seulement depuis 2018/19), Kara aussi (60,2 %) ; la Centrale et les Plateaux progressent le plus (+8,1 et +7,3 points).
- **Aujourd'hui** : la page Internet affiche le constat « les Savanes cumulent l'accès le plus faible et l'alphabétisation la plus faible », sans aucun visuel qui le montre.
- **Proposition** : une carte de l'alphabétisation à côté de celle de l'accès (item 1), avec la marge et le gain. La moitié droite de la carte 12 (mobile banking) relève de l'inclusion financière (voir V2).
- **Données** : `s9_capacites_usage_regions`.
- **Limite à afficher** : 6 régions seulement ; l'alphabétisation n'est qu'un proxy de compétence.

**Hors du 05 et du 06, à signaler** : deux autres analyses de l'objectif 1 existent dans le 07 sans place sur le tableau de bord : la croissance des abonnements data mobile, classée, avec ses 22 événements (07, figure 2 : ralentissement depuis 2022) ; l'écart entre abonnements et utilisateurs (2,86 abonnements par utilisateur en 2018, 1,50 en 2024 : les utilisateurs rattrapent les abonnements).

**Règles de mise en œuvre** (rappel) : chaque visuel en français et en anglais ; aucun code ni numéro de document sur la page ; chaque visuel porte son constat et sa limite ; les tables sont lues telles quelles, sans recalcul.

**Points à valider** :

| # | Question | Proposition |
| - | -------- | ----------- |
| V1 | Où placer ces 6 visuels ? La page Internet couvre déjà les objectifs 1 et 2 : les y ajouter tous la surchargerait | **Décidé (27/09/2026)** : des sous-onglets sur la page Internet, sur le modèle de l'image jointe par l'utilisateur. Le premier, « Vue synthèse », montre les visuels communs et la synthèse des résultats de l'objectif ; les suivants détaillent les analyses du même objectif. Structure ci-dessous |
| V2 | Moitié « mobile banking » de la carte 12 | La placer sur la page Offre financière, à côté de l'offre de mobile money, plutôt que sur la page Internet. **Validé (27/09/2026)** |
| V3 | Périmètre | **Validé (27/09/2026)** : les 6 items, dans l'ordre de priorité ; plus l'item 7 |
| V4 | Les deux analyses du 07 signalées plus haut | Les ajouter à l'onglet « Évolution de l'usage », ou les laisser hors du tableau de bord. **Validé (27/09/2026)** : ajoutées à l'onglet « Évolution de l'usage » |
| V5 | Le contenu de l'objectif 2 (marché, sites radio, fibre), aujourd'hui sur la même page | Le garder sur la page Internet, dans un dernier onglet « Marché des télécoms » : le menu garde ses 10 pages. Autre choix : une page à part pour l'objectif 2 (11 pages). **Validé (27/09/2026)** : dernier onglet, le menu garde ses 10 pages |

**Structure de la page Internet** (V1, construite le 27/09/2026) :

| Onglet | Contenu | Items |
| ------ | ------- | ----- |
| Vue synthèse | les 4 chiffres clés ; la courbe de l'usage depuis 1996, avec le repère Afrique subsaharienne et le seuil de 40 % ; le constat ; trois phrases de lecture, chacune renvoyant à l'onglet qui la détaille | 7 |
| Évolution de l'usage | la croissance annuelle classée (accélération, rythme habituel, ralentissement) avec les 5 événements ; l'usage selon les enquêtes auprès des ménages | 3 (et V4) |
| Accès et freins par région | les cartes de l'accès déclaré (2018/19, 2021/22) ; la carte de l'alphabétisation ; le tableau des freins | 1, 6, 2 |
| Le Togo dans l'UEMOA | les courbes des 8 pays ; le rang du Togo | 4 |
| Technologies | le mix technologique des abonnements data (2G, 3G, 4G) | 5 |
| Marché des télécoms | parts et concentration, chiffre d'affaires et investissement, prix de 1 Go, sites radio, fibre : le contenu actuel, déplacé | V5 |

Forme des onglets, comme l'image : des pastilles sur une barre blanche, l'onglet actif en couleur pleine, et le repère « vue 1 sur 6 » dessous. L'onglet choisi est gardé quand on change de langue. La Vue synthèse résume sans dupliquer : un visuel détaillé dans un autre onglet n'y est pas repris, il y est seulement annoncé.

### ✅ (27/09/2026) Mise en œuvre

- **Page Internet en 6 sous-onglets** (`dashboard/views/internet.py`) : Vue synthèse (4 chiffres clés, courbe de l'usage depuis 1996, « accélération ou stagnation ? », synthèse chiffrée qui renvoie à chaque onglet) ; Évolution de l'usage (croissance classée avec les 5 événements, enquêtes auprès des ménages, croissance des abonnements data, abonnements par utilisateur) ; Accès et freins par région (cartes de l'accès 2018/19 et 2021/22, carte de l'alphabétisation, tableau des freins) ; Le Togo dans l'UEMOA (courbes des 8 pays avec un pays de comparaison au choix, rang du Togo, classement de la dernière année) ; Technologies (4 chiffres clés, mix 2G, 3G, 4G) ; Marché des télécoms (le contenu de l'objectif 2, déplacé). Chaque onglet a son constat et sa limite. Seul l'onglet ouvert s'exécute ; l'onglet choisi est gardé au changement de langue et au passage par une autre page.
- **Composants partagés** (`dashboard/composants.py`) : `onglets()` (barre de sous-onglets et repère « vue 2 sur 6 », réutilisable sur les autres pages) et `carte_regions()` (carte des 6 régions en classes fixes, valeur écrite sur chaque région, légende complète même pour une classe vide, régions du filtre cerclées de noir). Style des pastilles dans `dashboard/theme.py`.
- **Page Offre financière** (V2) : bloc « Offre et usage du mobile money, par région », avec la carte du mobile banking et le tableau offre face à usage.
- **Page Diagnostic, corrigée au passage** : la colonne « frein présumé » affichait le texte brut de la table, en français même en anglais, avec un renvoi au document 02 (« la règle du 02 »). Elle passe par le même libellé en clair que la page Internet (`frein()` dans `dashboard/i18n.py`).
- **Vérifié** : les 10 pages et les 6 onglets s'ouvrent sans erreur, en français et en anglais, avec un filtre de région et avec un pays de comparaison ; captures d'écran de chaque onglet à 1440 px.
- **Écart de chiffre à signaler** : le 06 écrit que l'écart d'accès entre le Grand Lomé et les Savanes est de 52,3 points en 2021/22. Le tableau de bord affiche 52,4 : la table régionale est arrondie à deux décimales (66,67 − 14,32 = 52,35), et 52,4 est aussi la différence des deux valeurs affichées sur la même carte (66,7 % et 14,3 %). Le 52,3 du 06 vient sans doute des données d'enquête non arrondies. Aucun des deux n'est faux ; à harmoniser si besoin, dans le 06 ou en ajoutant l'écart aux tables.

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

---

## Journal de la branche `feature/cartes-synthese-hover`

Branche créée le 2026-09-28 depuis `dev`. Horodatage en UTC.

## 2026-09-28 18:07 UTC — Effet de survol sur les cartes de synthèse

- Les cartes de synthèse affichées en haut de chaque page (chiffres clés : ex. « Internet (2024) » sur la Synthèse nationale) réagissent au survol de la souris : la carte se soulève légèrement, sa bordure passe en jaune clair (`#fce588`) avec un halo, et un reflet lumineux la traverse de gauche à droite (effet « brillant »).
- S'applique à toutes les pages qui affichent ces cartes : Synthèse, Internet, Offre, Population, Priorités, Diagnostic, Projections.
- Désactivé pour les utilisateurs qui ont demandé moins d'animations dans leur système (`prefers-reduced-motion`).
- Fichier : `dashboard/theme.py` (`.kpi`, `.kpi::after`, `.kpi:hover`).
