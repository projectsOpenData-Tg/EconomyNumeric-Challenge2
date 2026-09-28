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

| # | Analyse                                              | Source                           | Page proposée | Priorité                                                        | Statut          |
| - | ---------------------------------------------------- | -------------------------------- | -------------- | ---------------------------------------------------------------- | --------------- |
| 1 | Carte de l'accès déclaré par région, deux vagues | 06, carte 9                      | Internet       | haute : prévue au plan 11, remplacée par des barres            | ✅ (27/09/2026) |
| 2 | Tableau des freins par région                       | plan 11 (page 2), table du 07    | Internet       | haute : prévu au plan, chargé par la page mais jamais affiché | ✅ (27/09/2026) |
| 3 | L'usage selon les enquêtes auprès des ménages     | 05, figure 4 (panneau de droite) | Internet       | haute : la réserve du chiffre de tête y renvoie                | ✅ (27/09/2026) |
| 4 | Le Togo face aux pays de l'UEMOA                     | 05, figure 11                    | Internet       | moyenne                                                          | ✅ (27/09/2026) |
| 5 | Le mix technologique des abonnements data            | 05, figure 5                     | Internet       | moyenne                                                          | ✅ (27/09/2026) |
| 6 | L'alphabétisation par région                       | 06, carte 12 (moitié gauche)    | Internet       | moyenne : preuve du constat affiché sur la page                 | ✅ (27/09/2026) |
| 7 | La courbe de l'UIT depuis 1996                       | 05, figure 4 (panneau de gauche) | Internet       | haute : demandée le 27/09/2026                                  | ✅ (27/09/2026) |

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

| #  | Question                                                                                                             | Proposition                                                                                                                                                                                                                                                                                                           |
| -- | -------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| V1 | Où placer ces 6 visuels ? La page Internet couvre déjà les objectifs 1 et 2 : les y ajouter tous la surchargerait | **Décidé (27/09/2026)** : des sous-onglets sur la page Internet, sur le modèle de l'image jointe par l'utilisateur. Le premier, « Vue synthèse », montre les visuels communs et la synthèse des résultats de l'objectif ; les suivants détaillent les analyses du même objectif. Structure ci-dessous |
| V2 | Moitié « mobile banking » de la carte 12                                                                          | La placer sur la page Offre financière, à côté de l'offre de mobile money, plutôt que sur la page Internet.**Validé (27/09/2026)**                                                                                                                                                                        |
| V3 | Périmètre                                                                                                          | **Validé (27/09/2026)** : les 6 items, dans l'ordre de priorité ; plus l'item 7                                                                                                                                                                                                                               |
| V4 | Les deux analyses du 07 signalées plus haut                                                                         | Les ajouter à l'onglet « Évolution de l'usage », ou les laisser hors du tableau de bord.**Validé (27/09/2026)** : ajoutées à l'onglet « Évolution de l'usage »                                                                                                                                        |
| V5 | Le contenu de l'objectif 2 (marché, sites radio, fibre), aujourd'hui sur la même page                              | Le garder sur la page Internet, dans un dernier onglet « Marché des télécoms » : le menu garde ses 10 pages. Autre choix : une page à part pour l'objectif 2 (11 pages).**Validé (27/09/2026)** : dernier onglet, le menu garde ses 10 pages                                                             |

**Structure de la page Internet** (V1, construite le 27/09/2026) :

| Onglet                       | Contenu                                                                                                                                                                                                    | Items     |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| Vue synthèse                | les 4 chiffres clés ; la courbe de l'usage depuis 1996, avec le repère Afrique subsaharienne et le seuil de 40 % ; le constat ; trois phrases de lecture, chacune renvoyant à l'onglet qui la détaille | 7         |
| Évolution de l'usage        | la croissance annuelle classée (accélération, rythme habituel, ralentissement) avec les 5 événements ; l'usage selon les enquêtes auprès des ménages                                               | 3 (et V4) |
| Accès et freins par région | les cartes de l'accès déclaré (2018/19, 2021/22) ; la carte de l'alphabétisation ; le tableau des freins                                                                                               | 1, 6, 2   |
| Le Togo dans l'UEMOA         | les courbes des 8 pays ; le rang du Togo                                                                                                                                                                   | 4         |
| Technologies                 | le mix technologique des abonnements data (2G, 3G, 4G)                                                                                                                                                     | 5         |
| Marché des télécoms       | parts et concentration, chiffre d'affaires et investissement, prix de 1 Go, sites radio, fibre : le contenu actuel, déplacé                                                                              | V5        |

Forme des onglets, comme l'image : des pastilles sur une barre blanche, l'onglet actif en couleur pleine, et le repère « vue 1 sur 6 » dessous. L'onglet choisi est gardé quand on change de langue. La Vue synthèse résume sans dupliquer : un visuel détaillé dans un autre onglet n'y est pas repris, il y est seulement annoncé.

### ✅ (27/09/2026) Mise en œuvre

- **Page Internet en 6 sous-onglets** (`dashboard/views/internet.py`) : Vue synthèse (4 chiffres clés, courbe de l'usage depuis 1996, « accélération ou stagnation ? », synthèse chiffrée qui renvoie à chaque onglet) ; Évolution de l'usage (croissance classée avec les 5 événements, enquêtes auprès des ménages, croissance des abonnements data, abonnements par utilisateur) ; Accès et freins par région (cartes de l'accès 2018/19 et 2021/22, carte de l'alphabétisation, tableau des freins) ; Le Togo dans l'UEMOA (courbes des 8 pays avec un pays de comparaison au choix, rang du Togo, classement de la dernière année) ; Technologies (4 chiffres clés, mix 2G, 3G, 4G) ; Marché des télécoms (le contenu de l'objectif 2, déplacé). Chaque onglet a son constat et sa limite. Seul l'onglet ouvert s'exécute ; l'onglet choisi est gardé au changement de langue et au passage par une autre page.
- **Composants partagés** (`dashboard/composants.py`) : `onglets()` (barre de sous-onglets et repère « vue 2 sur 6 », réutilisable sur les autres pages) et `carte_regions()` (carte des 6 régions en classes fixes, valeur écrite sur chaque région, légende complète même pour une classe vide, régions du filtre cerclées de noir). Style des pastilles dans `dashboard/theme.py`.
- **Page Offre financière** (V2) : bloc « Offre et usage du mobile money, par région », avec la carte du mobile banking et le tableau offre face à usage.
- **Page Diagnostic, corrigée au passage** : la colonne « frein présumé » affichait le texte brut de la table, en français même en anglais, avec un renvoi au document 02 (« la règle du 02 »). Elle passe par le même libellé en clair que la page Internet (`frein()` dans `dashboard/i18n.py`).
- **Vérifié** : les 10 pages et les 6 onglets s'ouvrent sans erreur, en français et en anglais, avec un filtre de région et avec un pays de comparaison ; captures d'écran de chaque onglet à 1440 px.
- **Écart de chiffre à signaler** : le 06 écrit que l'écart d'accès entre le Grand Lomé et les Savanes est de 52,3 points en 2021/22. Le tableau de bord affiche 52,4 : la table régionale est arrondie à deux décimales (66,67 − 14,32 = 52,35), et 52,4 est aussi la différence des deux valeurs affichées sur la même carte (66,7 % et 14,3 %). Le 52,3 du 06 vient sans doute des données d'enquête non arrondies. Aucun des deux n'est faux ; à harmoniser si besoin, dans le 06 ou en ajoutant l'écart aux tables.

---

## Objectif 1 : contrôle croisé avec le 05, le 06 et le 08

Contrôle du 28/09/2026 : chaque analyse de l'objectif 1 citée dans `05_data_analysis.md`, `06_data_spatial_analysis.md` et `08_prioritization.md` a été recherchée dans le code du tableau de bord. Toutes les cartes et tous les graphiques y étaient ; trois messages clés et quelques détails manquaient.

| # | Manque | Source | Statut |
| - | ------ | ------ | ------ |
| 1 | Les classes de croissance présentées comme acquises, alors que 2020, 2023 et 2024 changent de classe avec la période de référence 2015-2024 (seules 2016 et 2021 tiennent) | 05, section 4.1 et constat C2 | ✅ (28/09/2026) |
| 2 | « Accès et couverture ne vont pas ensemble » : chiffres affichés côte à côte, conclusion jamais écrite | 06, section 6 et constat S6 | ✅ (28/09/2026) |
| 3 | « Le score ne priorise pas l'usage d'Internet » : absent de la page Priorités | 08, sections 1 et 8.1 | ✅ (28/09/2026) |
| 4 | Le Togo au-dessus de l'Afrique subsaharienne depuis 2020 : visible sur la courbe, jamais écrit | 05, section 4.1 | ✅ (28/09/2026) |
| 5 | Afrobaromètre × 2,1 à côté du × 3,2 de l'UIT | 05, constat C1 | non retenu (décision du 28/09/2026) : la synthèse chiffrée garde le seul × 3,2 de l'UIT, le chiffre le plus frappant pour un décideur |
| 6 | Code « A13 » et renvois « référence du 08 », « section 6 » sur la page Priorités | plan 11, règle 3.1 | ✅ (28/09/2026) |

### ✅ (28/09/2026) Mise en œuvre

- **1. Fragilité des classes** (`dashboard/views/internet.py`). Vue synthèse : sur la courbe, un cercle vide marque une classe qui dépend de la période de référence (2020, 2023, 2024) ; dans l'encadré « Accélération ou stagnation ? », les classes sûres sont en gras (2016, 2021), les autres suivies de « selon la période de référence », avec une note : « avec 2015-2024 comme période de référence, 2020, 2023, 2024 passent en rythme habituel ». Onglet « Évolution de l'usage » : les barres de ces années sont en pointillés, sur les deux graphiques de croissance (usage : 2020, 2023, 2024 ; abonnements : 2017 et 2023 à 2025, qui changent aussi quand les ruptures sont comptées) ; le constat ajoute que le ralentissement est sûr en 2021 pour l'usage et en 2022 pour les abonnements ; la limite de l'onglet l'explique. Tout est lu dans les tables du 07 (`classe_variante_2015`, `classe_finale_variante_2015`, `classe_finale_ruptures_comptees`), rien n'est recalculé.
- **2. Accès et couverture** : un constat au-dessus du tableau des freins, calculé à partir de la table des freins. Les Savanes, couvertes à 89,1 %, ont l'accès le plus faible (14,3 %) ; la Centrale a la couverture la plus faible (75,5 %) mais l'un des meilleurs accès hors du Grand Lomé (25,6 %) ; six régions : un constat, pas une corrélation.
- **3. Le score et l'usage d'Internet** (`dashboard/views/priorites.py`) : un bandeau « Ce classement ne porte pas sur l'usage d'Internet » sous les chiffres clés. Aucune mesure d'usage n'existe à la préfecture ; à poids égaux, les deux dimensions financières pèsent les deux tiers du score ; doubler le poids de la couverture ne fait sortir aucune des 7 préfectures de la priorité haute (lu dans la table du score) ; pour l'usage, les priorités se lisent par région, avec un renvoi à l'onglet « Accès et freins par région ». La limite de la Vue synthèse de la page Internet renvoie dans l'autre sens.
- **4. Afrique subsaharienne** : la carte « Usage d'Internet » dit « Afrique subsaharienne : 33,6 %, dépassée depuis 2020 ». L'année vient de la table (`ecart_ass_points`).
- **6. Page Priorités** : « couverture non déterminable (A13) » devient « couverture inconnue : la carte de couverture y donne 0 % alors que des points mobile money y fonctionnent » ; « référence du 08 » devient « référence » ; « section 6 » renvoie au tableau « Tests de robustesse » de la page.
- **Vérifié** : les 10 pages et les 6 onglets de la page Internet, en français et en anglais, avec un filtre de région et un pays de comparaison (39 contrôles, tous passés) ; textes générés relus dans les deux langues ; captures d'écran de la Vue synthèse, de l'onglet Évolution, de l'onglet régional et de la page Priorités. Deux défauts vus sur les captures et corrigés : les barres en pointillés disparaissaient (Plotly remplaçait leur couleur par le motif) puis devenaient trop fines (une trace de légende en plus en mode « groupé »).
- ✅ (28/09/2026) **Code « P9 » et « A13 » sur les pages Carte et Population et offre** (validé le 28/09/2026 ; plan 11, règle 3.1). « P9 » désignait la variante du statut d'accès où la règle « desserte diversifiée » (les 4 types de points et moins de 10 000 habitants par guichet) est testée avant la règle « mobile money dominant » (plus de 20 points mobile money par guichet).
  - Page Population et offre (`dashboard/views/population.py`) : la bascule s'appelle « Variante : la desserte diversifiée l'emporte sur le mobile money dominant », avec une aide au survol qui explique la règle de référence. Quand la variante est activée, la légende dit ce qu'elle change, lu dans la table : 6 communes passent de « mobile money dominant » à « desserte diversifiée » (995 191 habitants : Agoè-Nyivé 3, Golfe 1, 4 et 6, Bassar 1, Kozah 1), comme dans le 07.
  - Même page, trouvé en cherchant : le tableau « Matrice statut × couverture » affichait l'en-tête « non déterminable (A13) », tiré tel quel de la table, et gardait ses en-têtes en français dans la version anglaise. Il affiche désormais « couverture inconnue », et ses en-têtes suivent la langue.
  - Page Carte (`dashboard/views/carte.py`) : la limite du statut d'accès dit « Règle en cascade : la première condition remplie l'emporte. Une variante, où la desserte diversifiée l'emporte sur le mobile money dominant, est sur la page « Population et offre » ».
  - Vérifié : plus aucun code interne affiché hors de la page Méthodologie (recherche sur toutes les pages) ; bascule, légende, matrice et limite contrôlées en français et en anglais ; les 39 contrôles de la suite complète passent.

## Page Internet : lisibilité des graphiques

Demande du 28/09/2026.

1. ✅ (28/09/2026) Onglet « Évolution de l'usage », graphique « Croissance annuelle de l'usage » : les textes affichés au-dessus des barres sont peu lisibles. Les agrandir un peu et leur donner une couleur.
2. ✅ (28/09/2026) Même onglet, graphique « Abonnements data par utilisateur d'Internet » : mettre le libellé « un abonnement par utilisateur » en rouge clair, et les chiffres en gras en bleu foncé, comme le texte du pied de page ; mettre en gras la phrase sous le graphique : « L'écart se creuse jusqu'en 2018 (multi-SIM), puis se resserre : les utilisateurs augmentent plus vite que les abonnements. »
3. ✅ (28/09/2026) Onglet « Accès et freins par région » : mettre en gras et en couleur la phrase « Le coût pèse partout : 1 Go coûte 5,3 % du revenu mensuel (chiffre national). 45,1 % des adultes ont un smartphone comme téléphone principal ; 32,1 % citent le coût comme raison de ne pas en avoir (Findex 2024). »
4. ✅ (28/09/2026) Onglet « Le Togo dans l'UEMOA », graphique « Usage d'Internet dans les 8 pays de l'UEMOA, 2000-2024 » : donner leur couleur aux courbes et aux libellés des pays comparés au Togo, et ajouter les libellés avec le pourcentage de chaque pays, comme sur la figure 11 du 05.
5. ✅ (28/09/2026) Même onglet, graphique « Rang du Togo parmi les 8 pays » : écrire le rang du Togo sur les phases importantes.
6. ✅ (28/09/2026) Onglet « Technologies », encadré du constat « La 4G devient majoritaire en 2025 (56,9 % des abonnements data) ; la 2G recule de 31,0 % à 18,7 %. » : mettre en couleur « 4G » avec ses chiffres, et de même « 2G » avec les siens.

### ✅ (28/09/2026) Mise en œuvre

Tout est dans `dashboard/views/internet.py`, avec deux ajouts à `dashboard/theme.py`. Le bleu foncé est celui du texte du pied de page (`#0d366b`).

- **1. Événements au-dessus des barres** : taille 11 au lieu de 9, en bleu foncé au lieu du gris.
- **2. Abonnements par utilisateur** : le libellé « un abonnement par utilisateur » passe en rouge clair (`#e34948`, le rouge de la palette du tableau de bord) ; les deux chiffres en gras (2,86 en 2018, 1,50 en 2024) passent en bleu foncé. La phrase sous le graphique passe en gras et en bleu foncé : ce n'est plus une légende grise mais une « note de graphique » (nouvelle fonction `note()`, style `.note-graphique`, variante `forte` pour le gras).
- **3. Coût et smartphone** : la phrase passe en gras et en bleu foncé (même fonction, même variante).
- **4. Les 8 pays de l'UEMOA** : une couleur par pays, comme la figure 11 du 05, au lieu du gris. Les 8 teintes sont celles de la palette catégorielle du tableau de bord, prolongée de 3 teintes (`CATEGORIELLE_8`) ; le Togo garde son bleu. Chaque couleur est attachée à un pays, jamais à son rang. Palette vérifiée par le validateur : les courbes voisines restent distinctes, y compris pour un daltonien. Légende dans le graphique, en haut à gauche, titrée « En 2024 », triée par la valeur de 2024, avec le pourcentage de chaque pays (« Sénégal : 60,1 % », « **Togo : 39,5 %** », « Afrique subsaharienne : 33,6 % »…) ; « Togo » écrit au bout de sa courbe. Le sélecteur de pays est gardé, sous le nom « Pays à mettre en évidence » : il estompe les autres pays au lieu de colorer le seul pays choisi.
- **5. Rang du Togo** : le rang est écrit au milieu de chaque phase, en bleu foncé : l'année de départ, puis chaque rang tenu au moins 2 ans (1er en 2000, 3e de 2002 à 2007, 2e en 2008-2009, 3e en 2010-2011, 6e de 2016 à 2018, 4e de 2019 à 2021, 3e depuis 2022). Les rangs d'une seule année (4e en 2012, 5e en 2013 et 2015, 6e en 2014) ne sont pas écrits : on les lit sur l'axe. La règle est appliquée aux données, sans liste d'années écrite à la main.
- **6. Constat des technologies** : « 4G », 56,9 % en bleu ; « 2G », 31,0 % et 18,7 % en rose, les couleurs de leurs barres. Pour rester lisibles en texte, les deux teintes sont un peu plus foncées que les barres (contraste d'au moins 4,5:1 sur fond blanc), avec la même teinte (`TEXTE_CATEGORIELLE`).
- **Précisions de l'utilisateur** (point 2, 28/09/2026) : la phrase « L'écart se creuse… » devait être en gras : elle est en gras et en bleu foncé. Le libellé « un abonnement par utilisateur » devait être en rouge clair : il l'est, avec le rouge déjà utilisé sur le tableau de bord (une teinte plus claire serait trop pâle sur fond blanc).
- **Choix de lisibilité** (point 4) : les noms des pays dans la légende restent en noir, à côté de leur trait coloré. Écrits dans la couleur de leur courbe, le jaune (Mali), le vert d'eau (Côte d'Ivoire) et le rose (Bénin) seraient illisibles sur fond blanc (contraste sous 3:1).
- **Vérifié** : un test par point, en français et en anglais (tailles, couleurs, textes, 9 courbes avec leur pourcentage, 8 couleurs distinctes, rangs attendus, pays mis en évidence) ; la suite complète (10 pages, 6 onglets, filtres, dans les deux langues) et le test de la variante du statut d'accès passent. Captures d'écran des onglets Évolution, Accès et freins par région, UEMOA (en français et en anglais) et Technologies. Un défaut vu sur la capture et corrigé : sur le graphique du rang, deux étiquettes touchaient la courbe ; elles sont maintenant centrées sur le palier tracé et placées plus haut.

---

## Objectif 2 : analyses déjà produites mais absentes du tableau de bord

Demande du 28/09/2026 : faire pour l'objectif 2 le même relevé que pour l'objectif 1 (section plus haut). Lire le 05, le 06, le 07, le 08 et le 11, puis lister les cartes et les figures importantes déjà produites mais absentes du tableau de bord, avec leur priorité et s'il faut les ajouter ou non, pour validation avant la mise en œuvre.

Relevé du 28/09/2026. Documents lus : `_PROJECT.txt` (objectif 2), `05_data_analysis.md` (figures 5, 6, 7 et 13, section 4.3), `06_data_spatial_analysis.md` (cartes 6 et 11), `07_indicators.md` (O2-01 à O2-09, section 6), `08_prioritization.md` (sections 1 et 8.1), `10_recommendations.md` (R4a, R4b, R6, R8, R9, R10) et `11_plan_visuel_dashboard.md` (pages 2 et 5). Rappel de l'objectif 2 : « analyser le marché des télécommunications : parts de marché des opérateurs, chiffre d'affaires, investissements et passage aux nouvelles technologies (3G, 4G, fibre) ».

**Ce que le tableau de bord montre déjà, composante par composante** :

| Composante de l'objectif           | Déjà affiché                                                                                                                                         | Où                                                                              |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Parts de marché                    | la dernière année seulement : Togocom 64,4 % des abonnés data, indice de concentration 5 418, « très concentré » ; « duopole »                      | Internet, onglet Marché des télécoms (chiffre clé) ; Synthèse nationale         |
| Chiffre d'affaires                 | **rien**                                                                                                                                             | —                                                                               |
| Investissements                    | le taux de la dernière année (16,3 % du chiffre d'affaires) ; les ajouts nets de sites radio par opérateur, 2022-2025                                | Internet, onglet Marché des télécoms                                            |
| Passage aux nouvelles technologies | le mix 2G, 3G, 4G des abonnements data (2018-2025) ; 81,3 % en haut débit ; la fibre : un chiffre clé (2025) et les 8 préfectures sans fibre recensée | Internet, onglets Technologies et Marché des télécoms ; Synthèse nationale      |
| Liés : prix et couverture          | 1 Go = 5,30 % du revenu mensuel ; trajectoire vers 2 % ; carte de la couverture théorique ; couverture, 3e dimension du score                        | Synthèse nationale ; Internet ; Estimations et projections ; Carte ; Priorités |

**Constat** : des quatre composantes, le chiffre d'affaires est absent, et les parts de marché et l'investissement ne sont montrés que pour la dernière année, alors que le 05 et le 07 en ont tracé l'évolution. Le plan 11 (page 2) prévoyait pourtant « parts de marché et concentration ; chiffre d'affaires et investissement (deux graphiques, jamais deux axes) ».

**Ce qui manque** (du plus important au moins important) :

| # | Analyse                                                                       | Source                                   | Composante                   | Priorité                                                        | À ajouter ?                                             | Statut    |
| - | ----------------------------------------------------------------------------- | ---------------------------------------- | ---------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------- | --------- |
| 1 | Le chiffre d'affaires du secteur et sa croissance classée, 2010-2025          | 05, figure 7 ; 07, O2-03                 | chiffre d'affaires           | haute : composante de l'objectif, absente ; prévue au plan 11   | oui                                                     | ✅ (28/09/2026) |
| 2 | Les parts de marché et la concentration, année par année                      | 05, figure 6 ; 07, O2-01                 | parts de marché              | haute : prévue au plan 11 ; seule la dernière année est affichée | oui                                                     | ✅ (28/09/2026) |
| 3 | Le taux d'investissement, 2018-2025                                           | 05, figure 7 ; 07, O2-04                 | investissements              | haute : prévu au plan 11 ; seule la dernière année est affichée  | oui                                                     | ✅ (28/09/2026) |
| 4 | Le passage à la fibre : Internet fixe et abonnés FTTH, par trimestre          | 05, figure 13 ; 07, O2-07                | nouvelles technologies       | haute : la fibre est nommée dans l'objectif                     | oui                                                     | ✅ (28/09/2026) |
| 5 | La fibre recensée par commune                                                 | 06, carte 11 ; plan 11, page 5           | nouvelles technologies       | moyenne : prévue au plan 11 (indicateur « fibre » de la Carte)  | oui                                                     | ✅ (28/09/2026) |
| 6 | Le prix de la data dans le temps                                              | 05, section 4.3 ; 07, O2-05b             | liée (prix)                  | moyenne                                                          | oui                                                     | ✅ (28/09/2026) |
| 7 | La couverture théorique face à la réception déclarée, par région           | 07, O2-06                                | liée (couverture)            | moyenne : les deux mesures se contredisent                       | oui                                                     | ✅ (28/09/2026) |
| 8 | Le positionnement de Togocom : part du chiffre d'affaires moins part des abonnés | 07, O2-02                             | parts de marché              | basse                                                            | en option : une phrase sous le graphique de l'item 2    | ✅ (28/09/2026) |
| 9 | Le revenu moyen par abonnement (ARPU)                                         | 07, O2-05a                               | chiffre d'affaires           | basse                                                            | en option : un chiffre clé, pas un graphique            | ✅ (28/09/2026) |

**Écartés** : l'indice des prix de la communication (05, section 4.3 : le saut de 2020 n'est pas expliqué, S7) ; le mix technologique (05, figure 5), déjà affiché ; la carte de la couverture (06, carte 6), déjà sur la page Carte ; la couverture dans le score (08), déjà sur la page Priorités. Le 08 ne demande rien de plus pour l'objectif 2 : le score ne le couvre qu'en partie (la couverture), et la limite de l'onglet dit déjà que le marché n'est mesuré qu'au niveau national.

**Corrections sur l'onglet actuel** (des écarts au 07 et au plan 11, pas des analyses manquantes) :

- ✅ (28/09/2026) **C1** : le titre « Fibre : préfectures non raccordées ». Le 07 (section 6) demande « sans fibre recensée », jamais « non raccordée » : une longueur de câble n'est pas un raccordement. Le sous-titre le dit déjà.
- ✅ (28/09/2026) **C2** : le stock de sites radio (1 406 en 2021, 1 840 en 2025) devait figurer dans le titre du graphique (plan 11, page 2) ; il n'y est pas. Le 07 ajoute un fait absent : depuis 2022, tous les sites portent la 4G (287 sites 2G ou 3G seulement en 2021).
- ✅ (28/09/2026) **C3** : la qualité de service n'est mesurée qu'au niveau national (O2-09). Le 07 demande d'afficher la mention « non couverte par territoire » ; elle n'apparaît nulle part.

### 1. Le chiffre d'affaires du secteur, 2010-2025 (05, figure 7 ; 07, O2-03)

- **Ce qu'il montre** : 185,6 Md FCFA en 2018, 264,9 en 2025 (+43 %). Chaque année est classée face à l'inflation : croissance réelle positive en 2019, 2020, 2021 et 2023 ; croissance nominale sans gain réel en 2022 (+2,1 % pour 8,0 % d'inflation) ; **stagnation en 2025 (+1,0 %)**. La série de l'INSEED remonte à 2010 : reculs en 2016 et 2017.
- **Aujourd'hui** : absent de tout le tableau de bord.
- **Proposition** : des barres du chiffre d'affaires par année, colorées selon la classe ; les deux sources (INSEED, 2010-2022 ; ARCEP, depuis 2018) en deux séries distinctes, jamais raccordées. Chiffre clé : « 264,9 Md FCFA en 2025 : stagnation (+1,0 %) ».
- **Données** : `o2_03_ca`, `s4_ca_investissement`.
- **Limite à afficher** : du 1er trimestre 2021 au 1er trimestre 2023, l'ARCEP publie le chiffre d'affaires fixe sans GVA : une partie des hausses de 2023 et de 2024 tient à son retour ; inflation inconnue après 2023 (2024 non classé) ; net ou brut de taxes non documenté.

### 2. Les parts de marché et la concentration (05, figure 6 ; 07, O2-01)

- **Ce qu'elle montre** : Togocom renforce sa position : de 57,0 % des abonnés data en 2018 à 64,4 % en 2025, de 60,5 % à 68,2 % du chiffre d'affaires mobile ; en téléphonie, 54,6 % en 2013, série arrêtée en 2019. L'indice de concentration dépasse 5 000 chaque année et sur chaque segment (duopole très concentré), et il monte : de 5 098 à 5 418 pour les abonnés data, de 5 222 à 5 666 pour le chiffre d'affaires.
- **Aujourd'hui** : la dernière année seulement, en chiffre clé.
- **Proposition** : une courbe de la part de Togocom par mesure (abonnés data, chiffre d'affaires mobile, abonnés à la téléphonie), jamais additionnées ; le creux de 2020 (39,0 %) marqué comme une rupture de série, pas comme un mouvement du marché ; l'indice de concentration au survol ou dans un petit tableau, jamais sur un second axe.
- **Données** : `s4_parts_togocom`, `o2_01_parts_hhi`.
- **Limite à afficher** : les segments ne se mélangent pas ; 2020 est une rupture (reclassement de la 3G de Togocel) ; la téléphonie par opérateur s'arrête en 2019.

### 3. Le taux d'investissement, 2018-2025 (05, figure 7 ; 07, O2-04)

- **Ce qu'il montre** : 36,9 % du chiffre d'affaires en 2018, 16,3 % en 2025. Deux cycles d'extension (2018-2019, 2022-2023), puis un retour au régime normal, à 1,3 point du seuil de sous-investissement (15 %). En valeur : 68,5 Md FCFA (2018), 39,7 (2020), 75,6 (2023), 43,1 (2025).
- **Aujourd'hui** : la dernière année seulement, en chiffre clé.
- **Proposition** : des barres du taux par année, colorées selon la classe (cycle d'extension, régime normal, sous-investissement), avec les seuils de 15 % et de 25 % ; à côté du graphique du chiffre d'affaires (item 1) : deux graphiques, jamais deux axes (plan 11). Le seuil de 15 % est aussi celui de la recommandation de veille sur l'investissement.
- **Données** : `o2_04_investissement`, `s4_ca_investissement`.
- **Limite à afficher** : une mesure en valeur, cyclique d'une année à l'autre ; les sites radio la complètent en volume.

### 4. Le passage à la fibre (05, figure 13 ; 07, O2-07)

- **Ce qu'il montre** : l'Internet fixe chute au 2e trimestre 2018 (arrêt de l'EvDo de Togo Telecom : de 42 633 à 18 767 abonnés), puis se reconstruit sur la fibre : 153 499 abonnés FTTH au 2e trimestre 2026, soit 98,6 % de l'Internet fixe, dont 58 % chez GVA. 1,74 abonnement FTTH pour 100 habitants en 2025 (+17 %). Mais la fibre reste marginale face au mobile : 2,2 % des abonnements data mobile.
- **Aujourd'hui** : un chiffre clé (fibre jusqu'au domicile, 2025), onglet Technologies.
- **Proposition** : des courbes trimestrielles de l'Internet fixe et des abonnés FTTH par opérateur (Togo Telecom, GVA), avec l'arrêt de l'EvDo annoncé ; la phrase « 98,6 % de l'Internet fixe, mais 2,2 % des abonnements data mobile ».
- **Données** : `s4_fibre`, `o2_07_ftth`.
- **Limite à afficher** : la fibre de Togo Telecom n'est pas publiée à part de fin 2021 à fin 2023, celle de GVA avant 2024 (on affiche son Internet fixe, sans le supposer égal à sa fibre).

### 5. La fibre recensée par commune (06, carte 11)

- **Ce qu'elle montre** : la fibre enterrée dessine un axe nord-sud (2 162 km) ; la fibre aérienne est à 77 % dans le Grand Lomé (2 373 km sur 3 071). 45 communes, toutes rurales (2,19 millions d'habitants), n'ont aucune fibre recensée ; 12 d'entre elles n'ont pas non plus de point formel.
- **Aujourd'hui** : la liste des 8 préfectures sans fibre recensée. La page Carte n'a pas l'indicateur « fibre » prévu au plan 11 (page 5).
- **Proposition** : ajouter « fibre recensée (km) » aux indicateurs de la page Carte (commune et préfecture) ; sur l'onglet du marché, une carte des communes sans fibre recensée à côté de la liste des préfectures.
- **Données** : `s6_fibre_communes`, `o2_07_fibre_prefectures`.
- **Limite à afficher** : une longueur de câble, sans date, sans distinguer le transport de l'accès : ni un raccordement, ni un nombre d'abonnés.

### 6. Le prix de la data dans le temps (05, section 4.3 ; 07, O2-05b)

- **Ce qu'il montre** : 1 Go coûte 5,85 % du revenu mensuel en 2023, 5,45 % en 2024, 5,30 % en 2025 : il baisse, mais reste loin du seuil de 2 %. Le panier de 2 Go passe de 11,37 % (2021) à 5,68 % (2025).
- **Aujourd'hui** : le chiffre de 2025 (Synthèse nationale, Vue synthèse) ; la trajectoire vers 2 % sur la page Estimations et projections.
- **Proposition** : une petite courbe par panier, chacun lu séparément (décision V6 du 04), avec le seuil de 2 % en repère.
- **Données** : `o2_05b_cout_1go`, `s4_paniers_uit`.
- **Limite à afficher** : revenu moyen par habitant, pas revenu médian ; les paniers changent de définition (1 Go, 1,5 Go, 2 Go, 5 Go) : ils ne se raccordent pas.

### 7. La couverture théorique face à la réception déclarée (07, O2-06)

- **Ce qu'elle montre** : les deux mesures ne disent pas la même chose. La Centrale, région la moins couverte selon la carte de couverture (75,5 %), déclare la meilleure réception : le premier réseau y est bien capté par 93,7 % de la population des localités enquêtées (EHCVM 2021/22). À l'inverse, les Plateaux, couverts à 86,1 %, n'en déclarent que 51,0 %.
- **Aujourd'hui** : seule la couverture théorique est affichée (page Carte, score).
- **Proposition** : des barres par région, les deux mesures côte à côte, jamais combinées, avec la phrase « aucune des deux ne mesure le signal ».
- **Données** : `s6_couverture_unites`, `o2_06_reception_declaree`.
- **Limite à afficher** : la couverture est un rayon de 20 km autour des tours ; la réception est déclarée par la localité, et l'opérateur du « réseau 1 » n'est pas nommé dans le fichier.

### 8. Le positionnement de Togocom (07, O2-02) et 9. l'ARPU (07, O2-05a)

- **Positionnement** : la part de Togocom dans le chiffre d'affaires dépasse sa part des abonnés data de +3,5 à +7,2 points selon l'année : entre « alignement » et « haut de marché ». Face à la téléphonie (2018-2019) : +15,9 et +11,3 points, haut de marché. Proposition : une phrase sous le graphique de l'item 2.
- **ARPU** : 2 130 FCFA par mois et par abonnement en 2018, 2 406 en 2021, 2 183 en 2025. Proposition : un chiffre clé. Limite : tous services confondus ; 2 029 FCFA en 2025 si l'on compte les abonnés du 4e trimestre.
- **Données** : `o2_02_ca_contre_abonnes`, `o2_05a_arpu`.

**Règles de mise en œuvre** (rappel) : chaque visuel en français et en anglais ; aucun code ni numéro de document sur la page ; chaque visuel porte son constat et sa limite ; les tables sont lues telles quelles, sans recalcul ; phrases de lecture en bleu foncé et chiffres d'un constat dans la couleur de leur série (demande du 28/09/2026).

**Points à valider** :

| #   | Question                                                                                                                            | Proposition                                                                                                                                                                                                                                                                                         |
| --- | ----------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| V6  | Où placer ces visuels ? L'onglet « Marché des télécoms » compte déjà 3 chiffres clés et 2 visuels ; les items 1 à 7 le rendraient très long | **Proposé** : une page à part, « Marché des télécoms », dans le groupe Analyses, en sous-onglets comme la page Internet (structure ci-dessous) ; le menu passe à 11 pages. Cela revient sur la décision V5 du 27/09/2026, prise quand l'objectif 2 n'avait que 3 visuels. Autre choix : garder un seul onglet sur la page Internet, les visuels les uns sous les autres (10 pages, onglet long). **Validé (28/09/2026)** : page à part |
| V7  | L'onglet « Technologies » (mix 2G, 3G, 4G) sert l'objectif 1 (part des abonnements par technologie) et l'objectif 2 (« passage aux nouvelles technologies ») | Si V6 est validé : le déplacer sur la nouvelle page, avec la fibre ; la page Internet garde un renvoi. Sinon : le laisser où il est. **Validé (28/09/2026)**                                                                                                                                                                  |
| V8  | Périmètre                                                                                                                           | Les items 1 à 7, dans l'ordre de priorité ; les items 8 et 9 en option (une phrase, un chiffre clé). **Validé (28/09/2026)** : les 9 items                                                                                                                                                                                                |
| V9  | Les corrections C1 à C3                                                                                                             | Les faire en même temps. **Validé (28/09/2026)**                                                                                                                                                                                                                                                                            |

**Structure proposée pour la page « Marché des télécoms »** (si V6 et V7 sont validés) :

| Onglet                            | Contenu                                                                                                                                                                                     | Items         |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| Vue synthèse                     | 4 chiffres clés (part de Togocom et concentration ; chiffre d'affaires de 2025 et sa classe ; taux d'investissement ; abonnés à la fibre) ; le constat ; une synthèse chiffrée qui renvoie à chaque onglet | —             |
| Parts de marché                   | la part de Togocom selon trois mesures ; la concentration ; le positionnement                                                                                                              | 2, 8          |
| Chiffre d'affaires et investissement | le chiffre d'affaires et sa croissance classée ; le taux d'investissement ; l'ARPU ; les sites radio (déplacés)                                                                           | 1, 3, 9, C2   |
| Technologies et fibre             | le mix 2G, 3G, 4G (déplacé) ; l'Internet fixe et la fibre ; la carte de la fibre ; les préfectures sans fibre recensée (déplacées)                                                          | 4, 5, C1      |
| Prix et couverture                | le prix de la data ; la couverture théorique face à la réception déclarée ; la mention sur la qualité de service                                                                           | 6, 7, C3      |

Cette structure suit les trois vues que le 07 prévoyait pour l'objectif 2 (section 6 : marché, investissement, accès), plus une Vue synthèse. Question de la page, à valider : « Qui tient le marché, et investit-il encore ? ». La page Internet garderait 4 onglets (sans Technologies ni Marché ; « 5 » dans la première version de ce relevé, une erreur de compte) et sa question « L'usage progresse-t-il, et à quel prix ? ».

### ✅ (28/09/2026) Mise en œuvre

Tout est validé le 28/09/2026 (V6 à V9) et construit le même jour.

- **Nouvelle page « Marché des télécoms »** (`dashboard/views/marche.py`), 3e du menu, dans le groupe Analyses ; le menu passe à 11 pages. Question : « Qui tient le marché, et investit-il encore ? ». Cinq sous-onglets, avec les mêmes pastilles et le même repère « vue 2 sur 5 » que la page Internet :
  - **Vue synthèse** : 4 chiffres clés (Togocom 64,4 % des abonnés data, indice 5 418 ; chiffre d'affaires 264,9 Md FCFA, « stagnation » ; investissement 16,3 % ; fibre 1,74 abonnement pour 100 habitants) ; constat ; synthèse chiffrée « 16,3 % » (du chiffre d'affaires investi en 2025, contre 36,9 % en 2018, à 1,3 point du seuil de sous-investissement), qui renvoie à chaque onglet.
  - **Parts de marché** (items 2 et 8) : part de Togocom selon trois mesures, chacune avec sa dernière valeur dans la légende ; 2020 en cercle vide, détaché de la courbe, avec « rupture de série » ; indice de concentration par segment dans un tableau ; positionnement en phrase sous le graphique (+3,5 à +7,2 points, « alignement » ou « haut de marché »).
  - **Chiffre d'affaires et investissement** (items 1, 3 et 9, C2) : chiffre d'affaires en barres (ARCEP) et en ligne (INSEED), chaque année colorée selon sa classe, les deux sources jamais raccordées ; taux d'investissement en barres classées, seuils de 15 et 25 %, « deux cycles d'extension (2018-2019 et 2022-2023) » ; sites radio déplacés, avec le stock dans le titre (« 1 406 en 2021, 1 840 en 2025 ») et « depuis 2022, tous les sites portent la 4G » ; ARPU en chiffre clé (2 183 FCFA par mois).
  - **Technologies et fibre** (items 4 et 5, C1) : les 4 chiffres clés et le mix 2G, 3G, 4G de l'ancien onglet, avec le constat en couleur ; Internet fixe et fibre par trimestre (2017-2026), arrêt de l'EvDo annoté ; carte des 45 communes sans fibre recensée (toutes rurales, 12 sans point formel non plus) ; préfectures « sans fibre recensée » (au lieu de « non raccordées »), habitants avec séparateur de milliers.
  - **Prix et couverture** (items 6 et 7, C3) : prix de la data par panier de l'UIT (1,5 Go, 2 Go, 5 Go, 1 Go), seuil de 2 %, renvoi à l'horizon 2037 de la page Estimations et projections ; couverture théorique face à la réception déclarée par région (la Centrale : 75,5 % contre 93,7 % ; les Plateaux : 86,1 % contre 51,0 %) ; mention « qualité de service : non mesurée par territoire ».
- **Page Internet** : renommée « Usage d'Internet » (« Internet use »), 4 onglets ; la puce de la 4G de sa synthèse renvoie à la nouvelle page, onglet « Technologies et fibre ».
- **Page Carte** (item 5) : deux indicateurs, fibre enterrée et fibre aérienne recensées (km), par commune et par préfecture ; jamais additionnés.
- **Code** : les aides des graphiques (`titre_bloc()`, `habiller()`, `tracer()`, `note()`, `pct()`, `BLEU_FONCE`) passent de la page Internet à `dashboard/composants.py`, pour servir les deux pages. Le bandeau du bas de la Synthèse nationale nomme les pages par le dictionnaire (il écrivait encore « Internet : usage et marché »). Plan 11 mis à jour (page 2 bis, section 4 à 11 pages, section 11).
- **Choix faits en construisant** : la Vue synthèse n'a pas de graphique (elle résume sans dupliquer : chaque visuel a son onglet) ; la synthèse chiffrée retient l'investissement, le chiffre le plus proche d'un seuil de décision ; le panier de 2013-2017 (1 Go postpayé sur ordinateur) n'est pas tracé, ce n'est pas un forfait mobile (il est dans l'export) ; la réception montrée est celle du premier réseau, le second est au survol.
- **Vérifié** : un test par onglet, en français et en anglais (chiffres clés, légendes, classes, 45 communes et 12 sans point formel, « sans fibre recensée », 4G et 2G en couleur, mention de la qualité de service, horizon 2037) ; indicateurs de la fibre sur la page Carte, aux deux mailles ; aucun code interne affiché sur la nouvelle page ; suite complète (11 pages, 4 + 5 onglets, filtres, deux langues), test de lisibilité et test de la variante du statut d'accès : tout passe. Captures d'écran des 5 onglets et de la page Internet. Défauts vus sur les captures et corrigés : étiquette « Stagnation (moins de 2 %) » trop longue sur sa carte ; colonne coupée du tableau de concentration ; repère des sites radio posé sur une barre ; cycles d'extension écrits année par année ; « 1.3 point » au lieu de « 1.3 points » en anglais.

---

## Page Marché des télécoms : ajustements

Demande du 28/09/2026.

1. ✅ (28/09/2026) Étendre les onglets pour qu'ils occupent toute la largeur de leur barre (image jointe), sur cette page et sur les autres pages à onglets.
2. ✅ (28/09/2026) Graphique « Internet fixe et fibre jusqu'au domicile, 2017-2026 » : le vide entre fin 2021 et 2024 se voit bien ; y mettre une bande grise, comme sur la figure 13 du 05.
3. ✅ (28/09/2026) Onglet « Prix et couverture », constat « 1 Go coûte 5,30 % du revenu mensuel en 2025… » : mettre en gras et en couleur les régions et les chiffres.
4. ✅ (28/09/2026) Tableau « Préfectures sans fibre recensée » : écrire chaque nom de région dans une couleur différente, et faire de même dans les tableaux des autres pages qui ont une colonne de régions.
5. ✅ (28/09/2026) Graphique « Couverture théorique et réception déclarée, par région » : ne plus nommer l'ARCEP dans la note, et dire à la place : « les sources institutionnelles complémentaires ne publient que… ».
6. ✅ (28/09/2026) Mettre à jour ce fichier avec ces changements.

### ✅ (28/09/2026) Mise en œuvre

- **1. Onglets** (`dashboard/theme.py`) : les pastilles se partagent toute la largeur de la barre, texte centré ; elles passent toujours à la ligne sur un écran étroit. Le style est commun : il vaut pour les deux pages à onglets (Usage d'Internet, 4 onglets ; Marché des télécoms, 5 onglets).
- **2. Bande grise** (`dashboard/views/marche.py`) : du 4e trimestre 2021 au 1er trimestre 2024, avec la mention « fibre de Togo Telecom non publiée à part », comme la figure 13 du 05. Ses bornes sont lues dans la table (les trimestres sans fibre de Togo Telecom) ; le sous-titre dit « (bande grise) » au lieu de « (trou de la courbe) ».
- **3. Constat en couleur** : les régions dans leur couleur (la même que dans les tableaux : la Centrale en violet, les Plateaux en ocre) ; les chiffres dans la couleur de leur série sur les graphiques voisins : prix de 1 Go en bleu foncé (la courbe de l'indicateur), seuil de 2 % en rouge (sa ligne), couverture théorique en bleu, réception déclarée en orange (leurs barres). Tout en gras.
- **4. Régions en couleur dans les tableaux** : une couleur fixe par région (`COULEUR_REGION`, `dashboard/theme.py`) : Grand Lomé en bleu, Maritime hors Grand Lomé en vert, Plateaux en ocre, Centrale en violet, Kara en orange, Savanes en rose. Ce sont les teintes de la palette du tableau de bord, assez foncées pour du texte sur fond blanc (contraste d'au moins 4,5:1). Appliqué aux 5 tableaux qui ont une colonne de régions : préfectures sans fibre recensée (Marché des télécoms), freins par région (Usage d'Internet), offre et usage du mobile money et points par préfecture (Offre financière), usage d'Internet par région (Diagnostic). Fonction partagée `colorer_regions()` (`dashboard/composants.py`).
- **5. Qualité de service** : « Les sources institutionnelles complémentaires ne publient que des valeurs nationales et une comparaison « Grand Lomé / reste du pays » : la couverture affichée reste théorique. » En anglais : « Complementary institutional sources only publish… ».
- **Trouvé en vérifiant** : un tableau mis en couleur passe par un « Styler », qui impose 6 décimales (« 46.700000 », « 14.300000 » sur les pages Offre financière et Diagnostic). Chaque colonne décimale garde désormais le nombre de décimales dont elle a besoin, au format de la langue (« 46,7 » en français).
- **Vérifié** : test de la page Marché des télécoms complété (bande grise et sa mention, constat en couleur, note sans l'ARCEP), en français et en anglais ; suite complète (11 pages, 4 + 5 onglets, filtres), test de lisibilité et test de la variante du statut d'accès : tout passe. Captures d'écran des deux barres d'onglets, du graphique de la fibre, de l'onglet Prix et couverture et des 5 tableaux de régions.

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

## 2026-09-28 18:09 UTC — Titres des cartes de synthèse en gras, couleur et majuscules

- Le titre de chaque carte de synthèse (ex. « Internet (2024) » sur la Synthèse nationale, affiché désormais « INTERNET (2024) ») passe en **gras**, en **majuscules** et en **bleu foncé du thème** (`#0d366b`, la couleur des surtitres de page), au lieu du gris normal.
- Taille légèrement réduite (0,76 rem) et interlettrage serré pour que les titres longs (« MARCHÉ DES TÉLÉCOMS (2025) ») tiennent sur deux lignes à côté de l'étiquette, sans décaler les chiffres d'une carte à l'autre.
- S'applique à toutes les pages qui affichent ces cartes.
- Fichier : `dashboard/theme.py` (`.kpi-libelle`).

## 2026-09-28 18:44 UTC — Barre du haut arrondie

- La barre du haut (armoiries, ministère, nom du projet, langue, logo Togo AI Lab) passe d'un rectangle à une **carte arrondie** : coins arrondis de 18 px, bordure fine `#e2dfd6`, ombre légère conservée.
- Marges intérieures gauche et droite de 22 px, pour que les armoiries et le logo Togo AI Lab ne touchent pas les coins arrondis.
- Fichier : `dashboard/theme.py` (`div.st-key-topbar`).

## 2026-09-28 18:45 UTC — Page Recommandations : cartes sur fond blanc, étiquettes en couleur

- Chaque carte de recommandation passe sur **fond blanc**, avec des coins arrondis (18 px), une bordure fine et une ombre légère, comme sur l'image de référence. Elles se détachent du fond beige de la page.
- Les trois mini-étiquettes en bas de chaque carte ont chacune **leur couleur** au lieu du gris commun :
  - **priorité** : jaune clair, texte brun (`#fdf0d2` / `#6b4700`), comme « Moyenne » sur l'image ; la priorité absolue (R1) reste en rouge ;
  - **nature** (immédiate, conditionnelle, veille) : violet clair (`#ece9fb` / `#4a3aa7`) ;
  - **horizon** (1 an, 3 ans, 5 ans) : vert clair (`#e2f4ec` / `#11613f`).
- Le style ne touche que les cartes : elles ont une clé propre (`carte_reco_<id>`), distincte de celle des filtres Thème, Nature et Horizon (`reco_…`).
- Fichiers : `dashboard/views/recommandations.py`, `dashboard/theme.py` (`st-key-carte_reco_`, `.etiquette.reco-priorite`, `.reco-nature`, `.reco-horizon`).

## 2026-09-28 19:08 UTC — Page Recommandations : couleur et emoji par thème, espace en bas des cartes, survol

- **Une couleur par thème** : le libellé du thème en tête de chaque carte prend la couleur de son thème, avec une pastille arrondie de la même teinte en clair, comme sur l'image de référence :
  - 🏦 Points formels : bleu (`#1c5cab`) ;
  - 📱 Mobile money : orange (`#b4451a`) ;
  - 📡 Couverture réseau : vert (`#11613f`) ;
  - 🌐 Fibre : violet (`#4a3aa7`) ;
  - 💰 Prix et frais : magenta (`#a3246b`) ;
  - 🎓 Compétences et équipement : ocre (`#6b4700`) ;
  - 📈 Investissement (veille) : bleu canard (`#0e6475`).
- **Emoji du thème** dans la pastille, placée devant le libellé du thème.
- **Espace en bas des cartes** : les étiquettes priorité, nature et horizon ne collent plus au bord inférieur de la carte (marge de 10 px au-dessus, 8 px en dessous).
- **Effet de survol sans couleur** : au passage de la souris, la carte se soulève de 4 px et son ombre s'agrandit ; ni la bordure ni le fond ne changent de couleur. Désactivé si l'utilisateur a demandé moins d'animations.
- Fichiers : `dashboard/views/recommandations.py` (`EMOJI_THEME`, en-tête `.reco-theme`), `dashboard/theme.py` (`.reco-theme`, `.reco-pastille`, `.theme-*`, `.reco-meta`, survol `st-key-carte_reco_`).

## 2026-09-28 19:09 UTC — Barre latérale : titres des filtres distincts de leurs choix

- Dans la section Filtres de la barre latérale, les titres de chaque filtre (**RÉGION**, **MAILLE DE LA CARTE**, **PRIORITÉ**, **MILIEU**) passent en **majuscules**, en gras et en **jaune clair** (`#fce588`, la couleur d'accent de la barre latérale), avec un léger interlettrage. Les choix (Grand Lomé, Commune, Priorité haute…) restent en blanc : on distingue d'un coup d'œil le titre d'une section de son contenu.
- Un peu d'espace ajouté au-dessus de chaque titre pour séparer les sections.
- Fichier : `dashboard/theme.py` (`[data-testid="stSidebar"] [data-testid="stWidgetLabel"]`).


---

## Objectif 3 : analyses déjà produites mais absentes du tableau de bord

Demande du 28/09/2026 : faire pour l'objectif 3 le même relevé que pour les objectifs 1 et 2 (sections plus haut). Lire le 05, le 06, le 07, le 08 et le 11, puis lister les cartes et les figures importantes déjà produites mais absentes du tableau de bord, avec leur priorité et s'il faut les ajouter ou non, pour validation avant la mise en œuvre.

Relevé du 28/09/2026. Documents lus : `_PROJECT.txt` (objectif 3), `05_data_analysis.md` (sections 2, 4.4, 5, 7 et 8 : figures 1, 2, 8 et 12, tableau des DAB), `06_data_spatial_analysis.md` (cartes 1, 2, 4, 7 et 10, sections 7 à 9), `07_indicators.md` (O3-01 à O3-06, section 6), `08_prioritization.md` (sections 1 et 8.1), `09_diagnostic.md` (limites), `10_recommendations.md` (R5) et `11_plan_visuel_dashboard.md` (pages 3 et 5, section 11). Rappel de l'objectif 3 : « cartographier les établissements financiers (banques, microfinance, assurances) et les agents mobile money par région, préfecture et commune ».

**Ce que le tableau de bord montre déjà, composante par composante** :

| Composante de l'objectif | Déjà affiché | Où |
| --- | --- | --- |
| Établissements financiers (banques, IMF, assurances) | effectifs nationaux (656 points formels ; 105 communes sur 117 sans assurance) ; carte des effectifs par commune, un type à la fois ; tableau par préfecture et par type | Offre financière |
| DAB (type à part) | 184 sites, dans 36 communes ; un choix de la carte par type, avec l'étiquette « type à part » | Offre financière |
| Agents mobile money | 19 788 points ; carte des effectifs par commune ; opérateur dominant par commune ; 48,3 % des comptes actifs ; usage du mobile banking par région, face à l'offre | Offre financière ; Synthèse nationale |
| Maille région | l'offre de mobile money (points pour 10 000 adultes) et son usage ; **rien sur les points formels** | Offre financière |
| Maille préfecture | un tableau des effectifs ; **aucune carte** | Offre financière |
| Maille commune | les cartes des effectifs par type et du mobile money | Offre financière |

**Constat** : les trois mailles de l'objectif ne sont pas traitées de la même façon : la commune a ses cartes, la préfecture n'a qu'un tableau, la région n'a rien pour les points formels. Le constat affiché sur la page (« l'écart oppose les villes aux campagnes, bien plus que Lomé aux autres villes ») n'a aucun chiffre : l'indicateur qui le prouve (O3-02) n'est affiché nulle part. Le 07 (section 6) prévoyait trois vues pour l'objectif 3 : offre, usage et coût. L'usage se réduit à un chiffre (48,3 %) et à une carte par région ; le coût (les frais du mobile money) est absent, alors qu'il fonde la recommandation R5. Le 08 (section 8.1) le rappelle : l'usage et le coût du mobile money sont hors du score, ils doivent donc être lus ailleurs.

**Ce qui manque** (du plus important au moins important) :

| # | Analyse | Source | Composante | Priorité | À ajouter ? | Statut |
| - | --- | --- | --- | --- | --- | --- |
| 1 | Parts de la population et des points par région, type par type | 05, figure 1 et tableau de la section 2 | maille région | haute : maille nommée dans l'objectif, absente pour les points formels | oui || ✅ (28/09/2026) |
| 2 | Le gradient urbain : Grand Lomé, autres villes, rural | 07, O3-02 | établissements financiers | haute : indicateur du 02 ; seule preuve du constat de la page | oui || ✅ (28/09/2026) |
| 3 | La présence par type selon la règle du 02 (absence, présence marginale, présence établie), à la commune et à la préfecture | 07, O3-01 et O3-03 ; 06, carte 1 | établissements, mobile money ; maille préfecture | haute : indicateur de l'objectif ; la carte montre des effectifs bruts, à la commune seulement | oui || ✅ (28/09/2026) |
| 4 | Le mobile money dans le temps : points de vente, comptes, transactions, détention d'un compte | 05, figure 8 ; 07, O3-04 | agents mobile money (usage) | haute : vue « usage » du 07 ; un seul chiffre affiché | oui || ✅ (28/09/2026) |
| 5 | Les frais d'une opération de référence | 07, O3-06 ; 10, R5 | agents mobile money (coût) | moyenne : vue « coût » du 07 ; preuve de R5 | oui || ✅ (28/09/2026) |
| 6 | La structure par opérateur, par région | 05, figure 12 ; 06, carte 10 | agents mobile money | moyenne : la carte ne montre que la catégorie dominante | oui || ✅ (28/09/2026) |
| 7 | L'emplacement des DAB (dans une banque, indépendant, autre établissement) | 05, tableau de la section 2 ; 06, carte 1 | DAB | moyenne : le plan 11 fait des DAB un « type à part » sans dire pourquoi | oui || ✅ (28/09/2026) |
| 8 | Le quotient de localisation par commune et par préfecture | 06, carte 4 | établissements financiers | basse : complète l'item 2 à la maille fine | en option : un indicateur de la page Carte || ✅ (28/09/2026) |
| 9 | La concentration : 10 communes ont 44,1 % des points formels | 05, figure 2 | établissements financiers | basse | en option : une phrase sous l'item 1, sans courbe ni indice de Gini || ✅ (28/09/2026) |
| 10 | Une géographie locale, pas régionale ; les pôles urbains hors Lomé | 06, section 7 (S1, S4) | établissements, mobile money | basse | en option : une phrase, sans la carte des grappes || ✅ (28/09/2026) |

**Écartés** : la carte de densité en hexagones (06, carte 2) : elle répète la carte par type à une autre maille ; la carte des grappes locales (06, carte 7) : des signaux sans correction pour tests multiples (P7 du 06), seule leur lecture passe dans l'item 10 ; l'usage du mobile banking par région (O3-05), déjà affiché ; les ratios par strate (05, figure 3), la diversité des types (05, section 5) et le mobile money face aux points formels (05, figure 10) : ils rapportent l'offre à la population, ils relèvent de l'objectif 4 (prochaine passe) ; la Poste, hors de la définition du point formel (D4).

**Corrections sur la page actuelle** (des écarts au 05, au 06 et au plan 11, pas des analyses manquantes) :

- ✅ (28/09/2026) **C4** : la légende de la carte des opérateurs et la limite de la page disent « opérateur non renseigné jusqu'à 23 % des points dans la région de Kara ». 23 % est le chiffre de la seule préfecture de Kéran. Les tables donnent 11,8 % pour la région de Kara, 40,4 % dans la préfecture de Bassar et 49,8 % dans la commune de Bassar 1 (06, carte 10 : 7 communes au-dessus d'un quart, dont 6 à Kara). Le chiffre vient du 09 (limites) et du plan 11 (page 3). Proposé : « opérateur non renseigné pour 11,8 % des points de la région de Kara, jusqu'à la moitié dans certaines communes (Bassar 1 : 49,8 %) ».
- ✅ (28/09/2026) **C5** : les filtres de la barre latérale (région, priorité, milieu) ne changent ni les cartes des points ni le tableau par préfecture : la table filtrée est calculée, mais pas utilisée. Seuls la carte et le tableau de l'usage du mobile money par région suivent le filtre de région. La page n'a pas non plus le bandeau « chiffres nationaux » des pages Usage d'Internet et Marché des télécoms. Proposé : appliquer les filtres aux cartes et aux tableaux ; signaler les chiffres clés nationaux comme tels.
- ✅ (28/09/2026) **C6** : le sous-titre prévu par le plan 11 (page 3) quand « DAB » est choisi n'apparaît pas : « les 22 communes où le mobile money est seul n'ont pas de DAB non plus ».
- ✅ (28/09/2026) **C7** : l'indicateur « opérateurs » prévu sur la page Carte (plan 11, page 5) n'y est pas.

### 1. Parts de la population et des points, par région (05, figure 1)

- **Ce qu'elle montre** : le Grand Lomé a 27,0 % de la population, mais 39,9 % des points formels, 58,2 % des DAB et 83,9 % des assurances ; le mobile money y est moins concentré (32,9 %). Les Plateaux sont l'inverse : 20,2 % de la population, 15,4 % des points formels, 10,3 % des DAB. Les IMF sont le premier type de point formel dans chaque région ; hors du Grand Lomé, elles font deux points formels sur trois (259 sur 394). Les assurances n'existent que dans trois régions (Grand Lomé 52, Kara 7, Plateaux 3).
- **Aujourd'hui** : absente. La région n'apparaît que pour le mobile money rapporté aux adultes.
- **Proposition** : des barres groupées par région : la part de la population (en gris, le repère) face à la part des points formels, des DAB et des points mobile money ; dessous, le tableau des effectifs par type et par région, noms de région en couleur.
- **Données** : `s2_parts_unites_regionales`.
- **Limite à afficher** : stock de 2021/2022 ; Grand Lomé : population résidente, pas fréquentation.

### 2. Le gradient urbain (07, O3-02)

- **Ce qu'il montre** : l'indice (part des points formels divisée par la part de la population) vaut 1,48 dans le Grand Lomé, 1,43 dans les autres villes et 0,65 en milieu rural : le **gradient urbain est confirmé** (règle du 02). La **concentration urbaine n'est pas confirmée** : le Grand Lomé a 39,9 % des points formels (sous le seuil de 50 %) et 27,0 % de la population (au-dessus du plafond de 25 %). Le rural : 56,9 % de la population, 37,2 % des points formels. Même ordre au seuil de 75 % d'urbains (1,48 > 1,43 > 0,79).
- **Aujourd'hui** : la phrase de constat, sans chiffre.
- **Proposition** : trois barres (une par strate), avec la ligne à 1 (« les points suivent la population ») ; les deux règles du 02 en clair sous le graphique ; le constat de la page chiffré.
- **Données** : `o3_02_strates`, `o3_02_regles`.
- **Limite à afficher** : strates définies au seuil de 50 % d'urbains ; au seuil de 75 %, l'ordre ne change pas.

### 3. La présence par type selon la règle du 02 (07, O3-01 et O3-03)

- **Ce qu'elle montre** : communes en absence / présence marginale (1 ou 2) / présence établie (3 ou plus) : banques 67 / 23 / 27 ; IMF 23 / 39 / 55 ; assurances 105 / 6 / 6 ; DAB 81 / 20 / 16. Préfectures : banques 9 / 9 / 21 ; IMF 1 (Kpendjal) / 2 / 36 ; assurances 33 / 3 / 3 ; DAB 17 / 10 / 12. L'assurance est absente de 105 communes, où vivent 6,07 millions d'habitants. Mobile money : aucune commune sans point.
- **Aujourd'hui** : la carte montre les effectifs bruts, sur une échelle continue où le zéro ne se distingue pas, à la commune seulement.
- **Proposition** : la carte par type en trois classes du 02 (l'absence dans une couleur à part), avec un sélecteur commune / préfecture ; sous la carte, le nombre de territoires et d'habitants par classe. Même sélecteur pour la carte du mobile money, en classes par quartiles (O3-03).
- **Données** : `o3_01_presence`, `o3_01_presence_communes`, `o3_01_presence_prefectures`, `o3_03_points_mm`.
- **Limite à afficher** : des effectifs, pas des ratios (le rapport à la population est sur la page Population et offre) ; des lieux, pas des agents.

### 4. Le mobile money dans le temps (05, figure 8 ; 07, O3-04)

- **Ce qu'il montre** : les points de vente passent de 24 289 (2020) à 59 855 (2025), × 2,5 ; la valeur des transactions de 1 948 à 5 481 Md FCFA (2021-2025), × 2,8, pour 493 millions de transactions en 2025 ; les comptes de 2,61 à 5,10 millions. La détention d'un compte mobile money passe de 1,4 % des adultes (2014) à 48,0 % (2024) ; depuis 2021, elle dépasse le compte en institution financière (32,4 % en 2024). Mais 48,3 % seulement des comptes sont actifs à 90 jours : **accès acquis, usage faible** (règle du 02).
- **Aujourd'hui** : le seul 48,3 %, sur la Synthèse nationale.
- **Proposition** : deux petits graphiques, jamais deux axes : la détention (mobile money face à l'institution financière, 2011-2024), avec le seuil de 50 % ; la valeur des transactions par année. Deux chiffres clés : 48,3 % des comptes actifs ; 48,0 % des adultes titulaires.
- **Données** : `s4_mobile_money`, `s4_findex`, `o3_04_arcep`, `o3_04_bceao_findex`.
- **Limite à afficher** : trois définitions du compte (BCEAO, ARCEP, Findex), qui ne se comparent pas entre elles ; révision de l'ARCEP au 1er trimestre 2021 (rupture des comptes) ; national seulement.

### 5. Les frais d'une opération de référence (07, O3-06)

- **Ce qu'ils montrent** : retirer 1 000 FCFA chez un agent Flooz coûte 75 FCFA (7,5 %) ; 10 000 FCFA, 280 FCFA (2,8 %) ; 100 000 FCFA, 1 000 FCFA (1,0 %) : **structure régressive**, et seul le petit retrait dépasse le repère de 3 %. Transferts : gratuits jusqu'au 3e (Flooz), 6 par jour puis 1 % (Mixx). Le retrait Mixx n'est pas publié.
- **Aujourd'hui** : absents. La page Recommandations affiche la cible de R5, pas le fait qui la fonde.
- **Proposition** : trois barres (frais en % du montant), avec le repère de 3 % ; la mention « Mixx : grille de retrait non publiée » ; un renvoi à R5.
- **Données** : `o3_06_frais`.
- **Limite à afficher** : grilles relevées le 26/09/2026, sans historique ; Mixx partiel ; le repère de 3 % est indicatif.

### 6. La structure par opérateur, par région (05, figure 12 ; 06, carte 10)

- **Ce qu'elle montre** : 63,9 % des points sont servis par les deux opérateurs, 24,1 % par Togocom seul, 5,1 % par Moov seul ; 6,8 % n'ont pas d'opérateur renseigné. **Kara et la Centrale reposent surtout sur Togocom** : Moov n'est présent que dans 51,3 % et 53,0 % des points. Le Maritime hors Grand Lomé est l'inverse (15,4 % de points Moov seul). Dans 11 communes, Togocom seul sert la moitié des points ou plus.
- **Aujourd'hui** : la carte de la catégorie dominante par commune.
- **Proposition** : des barres empilées à 100 % par région (quatre catégories, le « non renseigné » jamais réparti), à côté de la carte actuelle ; la phrase sur Kara et la Centrale.
- **Données** : `s2_mm_operateurs`, `s2_operateurs_communes`.
- **Limite à afficher** : celle corrigée en C4.

### 7. L'emplacement des DAB (05, section 2)

- **Ce qu'il montre** : 126 DAB sont dans une banque, 53 indépendants, 5 dans un autre établissement. 41 des 53 DAB indépendants sont dans le Grand Lomé. Hors du Grand Lomé, 65 DAB sur 77 (84 %) sont dans une banque : **ils doublent l'agence plus qu'ils n'étendent l'accès**. La Centrale n'a aucun DAB indépendant. 81 communes (46,5 % de la population) n'ont aucun DAB.
- **Aujourd'hui** : le nombre de DAB par commune, sans leur emplacement.
- **Proposition** : quand « DAB » est choisi, des barres empilées par région sous la carte (dans une banque, indépendant, autre établissement), avec la phrase en gras.
- **Données** : `s2_dab_emplacement`.
- **Limite à afficher** : des sites, pas des appareils.

### 8 à 10. En option

- **Quotient de localisation (06, carte 4)** : 22 communes à 0, 22 sous 0,5, 7 au-dessus de 2 (quartiers d'affaires du Grand Lomé, chefs-lieux) ; 18 préfectures sur 39 sous 0,8. Proposition : un indicateur de la page Carte, aux deux mailles (`s3_communes`, `s3_prefectures`).
- **Concentration (05, figure 2)** : les 10 communes les mieux dotées (dont 6 du Grand Lomé) ont 44,1 % des points formels pour 25,0 % de la population. Proposition : une phrase sous l'item 1, sans la courbe ni l'indice de Gini (une lecture technique pour un décideur).
- **Géographie locale (06, S1 et S4)** : l'accès formel ne forme pas de blocs régionaux ; l'écart se joue entre le chef-lieu et ses campagnes. Sokodé a 89,9 % des points mobile money de sa préfecture pour 73,9 % de sa population (Kara : 87,5 % pour 68,2 % ; Cinkassé : 86,0 % pour 58,9 %). Proposition : une phrase dans la Vue synthèse (`s7_moran_global`, `s7_poles_urbains`).

**Règles de mise en œuvre** (rappel) : chaque visuel en français et en anglais ; aucun code ni numéro de document sur la page ; chaque visuel porte son constat et sa limite ; les tables sont lues telles quelles, sans recalcul ; phrases de lecture en bleu foncé, chiffres d'un constat dans la couleur de leur série, noms de région en couleur.

**Points à valider** :

| # | Question | Proposition |
| --- | --- | --- |
| V10 | Où placer ces visuels ? La page Offre financière n'a pas d'onglets ; les items 1 à 7 la rendraient très longue | **Proposé** : des sous-onglets, comme les pages Usage d'Internet et Marché des télécoms (structure ci-dessous) ; le menu reste à 11 pages. Autre choix : garder une seule page, les visuels les uns sous les autres. **Validé (28/09/2026)** : sous-onglets |
| V11 | Maille des cartes | **Proposé** : un sélecteur commune / préfecture sur les cartes par type et du mobile money ; la région en barres et en tableau (item 1), comme le 06 (règle 1). **Validé (28/09/2026)** ; le sélecteur est celui de la barre latérale (« Maille de la carte »), déjà présent : pas de second sélecteur sur la page |
| V12 | Périmètre | Les items 1 à 7, dans l'ordre de priorité ; les items 8 à 10 en option (un indicateur de la Carte, deux phrases). **Validé (28/09/2026)** : les 10 items |
| V13 | Les corrections C4 à C7 | Les faire en même temps. Pour C4, corriger aussi le chiffre dans le 09 (limites) et dans le plan 11 (page 3). **Validé (28/09/2026)** |

**Structure proposée pour la page « Offre financière »** (si V10 est validé) :

| Onglet | Contenu | Items |
| --- | --- | --- |
| Vue synthèse | les 4 chiffres clés actuels ; le constat, chiffré par le gradient ; une synthèse chiffrée (« 37,2 % des points formels pour 56,9 % de la population : les communes rurales ») qui renvoie à chaque onglet | 2, 10 |
| Établissements financiers | la carte par type, en classes du 02, commune ou préfecture ; les parts par région ; le gradient ; l'emplacement des DAB ; le tableau par préfecture (actuel) | 1, 2, 3, 7, 9, C6 |
| Réseau mobile money | la carte des points, commune ou préfecture ; les opérateurs : carte (actuelle) et barres par région | 3, 6, C4 |
| Usage et coût du mobile money | le mobile money dans le temps ; l'offre et l'usage par région (actuels) ; les frais | 4, 5 |

Cette structure suit les trois vues que le 07 prévoyait pour l'objectif 3 (section 6 : offre, usage, coût), l'offre étant partagée entre établissements financiers et mobile money, plus une Vue synthèse. La question de la page ne change pas : « Où sont les établissements financiers ? ».

### ✅ (28/09/2026) Mise en œuvre

Tout est validé le 28/09/2026 (V10 à V13) et construit le même jour.

- **Page « Offre financière »** (`dashboard/views/offre.py`, refaite) : quatre sous-onglets, avec les mêmes pastilles et le même repère « vue 2 sur 4 » que les pages Usage d'Internet et Marché des télécoms. Question inchangée : « Où sont les établissements financiers ? ».
  - **Vue synthèse** : 4 chiffres clés en langage clair (656 agences financières ; 19 788 points mobile money ; 105 communes sur 117 sans assurance ; 184 distributeurs de billets, « type à part ») ; constat chiffré par l'écart entre villes et campagnes (1,48, 1,43, 0,65, chaque milieu dans sa couleur) ; synthèse chiffrée « 37,2 % des agences financières pour 56,9 % de la population : les communes rurales », avec une puce par onglet et la phrase « les agences ne forment pas de blocs régionaux » (item 10).
  - **Établissements financiers** (items 1, 2, 3, 7 et 9, C6) : carte par type en trois classes (aucune, 1 ou 2, 3 ou plus), à la maille de la barre latérale, avec le nombre de territoires et d'habitants par classe ; écart entre villes et campagnes en barres, repère à 1, avec les deux règles en clair (gradient confirmé, concentration dans le Grand Lomé non confirmée) ; parts de la population, des agences, des distributeurs et du mobile money par région, noms de région en couleur, et le tableau des effectifs ; phrase des 10 communes les mieux dotées (44,1 % des agences pour 25,0 % de la population) ; quand « Distributeurs de billets » est choisi, leur emplacement par région (« hors du Grand Lomé, 84 % sont dans une banque ») et le sous-titre du plan 11 sur les 22 communes ; tableau par préfecture.
  - **Réseau mobile money** (items 6 et 10, C4) : carte des points en cinq classes fixes (une échelle continue était écrasée par Golfe, plus de 5 000 points) ; carte de l'opérateur le plus fréquent, aux deux mailles ; parts par région en barres empilées (deux opérateurs, Togocom seul, Moov seul, non renseigné) ; « Kara et la Centrale reposent surtout sur Togocom » (Moov Africa présent dans 51,3 % et 53,0 % des points), 11 communes où Togocom seul sert la moitié des points ou plus ; les pôles hors de Lomé (Sokodé : 89,9 % des points de sa préfecture pour 73,9 % de ses habitants).
  - **Usage et coût du mobile money** (items 4 et 5) : 4 chiffres clés (48,3 % des comptes actifs ; 48,0 % des adultes titulaires ; 5 481 milliards de FCFA de transactions en 2025 ; 59 855 points de vente) ; détention d'un compte mobile money face au compte en banque ou en microfinance, 2011-2024, seuil de 50 % (« depuis 2021, plus d'adultes ont un compte mobile money ») ; valeur des transactions, 2021-2025 ; offre et usage par région (déplacés de l'ancienne page) ; frais d'un retrait de 1 000, 10 000 et 100 000 FCFA, repère de 3 %, renvoi à la recommandation sur les frais.
- **Filtres (C5)** : les cartes et les tableaux par territoire suivent les filtres de région, de priorité et de milieu, et la maille de la barre latérale ; un bandeau dit ce qui reste national.
- **Page Carte** (item 8, C7) : deux indicateurs, « part des agences face à la part de la population » (classes et couleurs de la carte 4 du 06, bornes fixées à l'avance, symétriques autour de 1) et « opérateurs du mobile money », aux deux mailles.
- **Correction C4 dans les documents** : le « jusqu'à 23 % » est remplacé dans le 09 (limites) et le plan 11 (page 3), avec la trace de la correction.
- **Choix faits en construisant** : la maille des cartes est celle de la barre latérale, déjà présente, plutôt qu'un second sélecteur sur la page ; l'emplacement des distributeurs s'affiche sous la carte quand ce type est choisi, comme proposé ; les points de vente déclarés par les opérateurs (59 855) portent la mention « autre mesure que les 19 788 lieux recensés ».
- **Vérifié** : un test par onglet, en français et en anglais (chiffres attendus, aucun sigle ni nom de source, aucun code interne) ; type « distributeurs », maille commune et filtre de région (carte limitée aux communes de Kara et des Savanes, tableaux filtrés) ; indicateurs de la Carte aux deux mailles ; suite complète (11 pages, 4 + 5 + 4 onglets, filtres, deux langues), tests du Marché, de lisibilité et de la variante du statut d'accès : tout passe. Captures d'écran des 4 onglets. Défauts vus sur les captures et corrigés : étiquette « Type à part : pas une agence » qui débordait de sa carte ; libellé du repère « 1 » posé sur une barre ; entiers sans séparateur de milliers dans les tableaux à régions en couleur ; carte des points mobile money presque uniforme ; parts de Moov Africa écrites dans la couleur de Togocom ; légende des barres empilées en ordre inverse ; unité « milliards de FCFA » coupée sur une carte ; axe sans séparateur de milliers ; étiquette de frais posée sur la ligne du repère, puis tournée à la verticale.

---

## Pages des objectifs : sigles et noms de sources

Demande du 28/09/2026, avec la validation de l'objectif 3 :

1. ✅ (28/09/2026) Les sigles « DAB », « IMF », « points formels » des cartes de chiffres clés des 4 pages d'objectifs ne parlent pas aux décideurs : leur donner leur sens propre, en clair.
2. ✅ (28/09/2026) Sur les pages des 4 objectifs, éviter de nommer les sources (ARCEP, Afrobaromètre…) dans 80 % des cas : les remplacer par « sources institutionnelles externes ». Sur la page « Sources et méthode », les présenter avec leur rôle : les jeux de données qui manquaient et les croisements qu'elles ont apportés pour répondre au projet.

**Mise en œuvre** :

- **Sigles** (pages Usage d'Internet, Marché des télécoms, Offre financière, Population et offre) :
  - « point formel » devient « agence financière » (agence de banque, de microfinance ou d'assurance), « guichet » aussi ; « DAB » devient « distributeur de billets » ; « IMF », « microfinance » ;
  - sur le Marché, « ARPU » devient « revenu moyen mobile », « Md FCFA » devient « milliards de FCFA », l'indice de concentration est dit « sur 10 000 » ;
  - sur Usage d'Internet, « Rang dans l'UEMOA » devient « Rang régional », avec le nom de l'Union écrit en entier ;
  - sur Population et offre, « Cellules critiques » devient « Mobile money et réseau faible », « Maillage insuffisant » devient « Trop peu de points mobile money », et un code interne (`classe_O4_01`) sort de la limite de la page ;
  - le sens exact des termes est dans le glossaire de la page Sources et méthode (« agence financière », « point mobile money » ajoutés).
- **Sources** : aucun nom de source n'est plus affiché sur les 4 pages, dans les deux langues (vérifié par un test qui lit les textes, les graphiques et les tableaux) ; elles y sont désignées de façon générique : « estimation internationale », « enquête nationale auprès des ménages », « enquête d'opinion auprès des adultes », « série annuelle » et « série trimestrielle » pour les deux sources du chiffre d'affaires, « source institutionnelle externe ». Les opérateurs (Togocom, Moov Africa, GVA) restent nommés : ce sont des acteurs du marché, pas des sources.
- **Page Sources et méthode** : deux tableaux remplacent « Sources et millésimes ». « Les données du défi » : les six jeux de données du sujet (et les compléments du portail géographique national), ce que chacun donne et ce qui lui manquait. « Sources institutionnelles externes : leur rôle » : pour chaque source (ARCEP, INSEED, enquêtes auprès des ménages, Afrobaromètre, BCEAO, Banque mondiale, UIT, grilles des opérateurs), le manque comblé, les croisements rendus possibles, les objectifs servis et le nom générique qu'elle porte sur les pages. Tableaux statiques : leurs phrases reviennent à la ligne.
- **Au passage** : dans les cartes de chiffres clés, l'espace des milliers est insécable (« 10 000 » ne se coupe plus en fin de ligne).
- **Hors de ces 4 pages** : la Synthèse nationale garde ses sigles (IMF, DAB, UIT, BCEAO, guichet) ; elle n'était pas dans la demande. ✅ (29/09/2026) Traité depuis, avec les autres pages : étape 3 de la section « Objectifs 4 et 5, et les autres pages ».



---

## Objectifs 4 et 5, et les autres pages : analyses déjà produites mais absentes du tableau de bord

Demande du 28/09/2026 : faire pour les objectifs 4 et 5, et pour les autres pages, le même relevé que pour les objectifs 1, 2 et 3 (sections plus haut). Lire le 05, le 06, le 07, le 08 et le 11, puis lister les cartes et les figures importantes déjà produites mais absentes du tableau de bord, avec leur priorité et s'il faut les ajouter ou non, pour validation avant la mise en œuvre.

Relevé du 28/09/2026. Documents lus : `_PROJECT.txt` (objectifs 4 et 5), `05_data_analysis.md` (sections 5 à 8), `06_data_spatial_analysis.md` (sections 3, 5, 7 et 9), `07_indicators.md` (O4-01 à O4-06, divergence, section 6), `08_prioritization.md` (en entier), `09_diagnostic.md` (sections 2, 3, 5 à 7), `10_recommendations.md` (sections 1, 2, 6 à 9) et `11_plan_visuel_dashboard.md` (pages 1 et 4 à 10, sections 8 et 9). Le code des 8 pages concernées a été relu, et chaque page ouverte en français et en anglais par un test.

Rappel des objectifs :
- **4** : « rapporter ces points d'accès à la population : nombre d'habitants par point de service, nombre d'agents mobile money par guichet financier, territoires desservis uniquement par le mobile money » ;
- **5** : « proposer des recommandations ciblées pour accélérer l'usage d'Internet et renforcer l'inclusion financière numérique dans les territoires les moins bien servis ».

### A. Objectif 4 : page « Population et offre »

**Ce que le tableau de bord montre déjà** :

| Composante de l'objectif | Déjà affiché | Où |
| --- | --- | --- |
| Habitants par point de service | agences financières : carte par commune, avec des seuils déplaçables ; mobile money : **seulement** l'explorateur de la page Carte (échelle continue) et un chiffre clé (3 communes au maillage insuffisant) | Population et offre ; Carte |
| Agents mobile money par guichet financier | **un chiffre clé** (66 communes où le mobile money supplée) ; aucune carte, aucune classe | Population et offre ; Synthèse nationale |
| Territoires desservis uniquement par le mobile money | les 22 communes sur la carte de la Synthèse ; la liste des 25 communes signalées (sans distance) ; le statut d'accès en carte, avec sa variante | Synthèse ; Diagnostic ; Population et offre |
| Statut croisé avec la couverture | la matrice statut × couverture (comptes par case) | Population et offre |

**Constat** : des trois mesures que l'objectif nomme, une seule a sa carte sur la page (habitants par agence). « Agents mobile money par guichet », le libellé même de l'objectif, n'a ni carte ni classe nulle part. Les 22 communes où le mobile money est seul sont listées, mais sans ce qui les caractérise le mieux : la distance au guichet le plus proche (de 6 à 38 km en médiane). L'indicateur de densité (O4-02) et son repère UEMOA n'apparaissent nulle part.

**Ce qui manque** (du plus important au moins important) :

| # | Analyse | Source | Ce qu'elle montre | Proposition | Priorité | À ajouter ? | Statut |
| - | --- | --- | --- | --- | --- | --- | --- |
| 1 | Agents mobile money par guichet financier, en classes du 02 | 07, O4-03 ; 06, carte 5 (gauche et centre) | communes : 1 « réseaux comparables », 28 « mobile money prépondérant », **66 « suppléance quasi totale » (65,4 % de la population)**, 22 « mobile money uniquement » ; les 6 régions en suppléance (24,9 à 49,6 points par guichet) | carte en 4 classes, commune ou préfecture ; répartition de la population par classe | haute : libellé de l'objectif, absent partout | oui || ✅ (29/09/2026) |
| 2 | Les 22 communes où le mobile money est seul, avec leur distance au guichet | 06, section 5 ; 05, section 7 | 17 sur 22 (587 338 habitants) ont leurs points mobile money à plus de 10 km d'un guichet en médiane ; Kpendjal 1 : 37,8 km, Akébou 2 : 30,5 km ; commune du guichet le plus proche ; voisines dotées | tableau trié par distance (population, points mobile money, distance médiane, commune du guichet le plus proche), noms de région en couleur | haute : troisième composante de l'objectif | oui || ✅ (29/09/2026) |
| 3 | Habitants par point mobile money, en classes du 02 | 07, O4-04 ; plan 11, page 4 | maillage dense presque partout : 87 communes (78,9 % de la population) ; 3 communes insuffisantes (Blitta 2, Blitta 3, Kpendjal 2) ; aucune préfecture insuffisante | carte en 3 classes à côté de celle des agences (le plan 11 prévoyait les deux cartes) | haute : prévue au plan 11, absente de la page | oui || ✅ (29/09/2026) |
| 4 | Distance des points mobile money au guichet le plus proche, par région | 06, section 5 (carte 5, droite) | 7,8 % des points à plus de 10 km d'un guichet ; Centrale 15,4 %, Plateaux 14,0 %, Savanes 13,7 % ; 27,1 % à plus de 10 km d'un distributeur de billets | barres par région (plus de 5 km, plus de 10 km) | moyenne : c'est « le seul accès proche » en pratique | oui || ✅ (29/09/2026) |
| 5 | Densité : points pour 10 000 adultes et pour 1 000 km², face à l'UEMOA | 07, O4-02 | le Togo dépasse la moyenne UEMOA (4,38 agences bancaires pour 100 000 adultes contre 3,52), **mais 21 préfectures sur 39 sont en dessous** ; le Grand Lomé a 39 à 137 fois plus d'agences au km² que les autres régions | 2 chiffres clés (Togo, moyenne UEMOA) avec la phrase des 21 préfectures, que le 07 impose de ne jamais séparer | moyenne : indicateur de l'objectif, absent partout | oui || ✅ (29/09/2026) |
| 6 | Répartition de la population par classe, commune et préfecture | 07, O4-01, O4-03, O4-04 | agences : 22 communes sans agence (9,4 % de la population), 17 sous-desservies ; à la préfecture, 1 et 5 : **la préfecture resserre les écarts** | petit tableau sous chaque carte (communes, préfectures, part de la population) | moyenne | oui || ✅ (29/09/2026) |
| 7 | Les 8 communes en cellule critique, nommées | 07, O4-06 | Agou 2, Akébou 2, Blitta 3, Dankpen 2, Kéran 2 (mobile money seul), Anié 2, Kpendjal-Ouest 1, Oti-Sud 2 (dominant) ; 368 534 habitants ; 3 couvertures douteuses | liste sous la matrice, la couverture douteuse signalée | moyenne : la matrice ne donne que des comptes | oui || ✅ (29/09/2026) |
| 8 | Divergence entre commune et préfecture, par mesure | 07, section 5.7 | 58 communes pour les agences, 41 pour les agents par guichet, 27 pour le mobile money ; 77 sur 117 (5,03 millions d'habitants) sur au moins une | 3 chiffres au-dessus de la liste actuelle | basse | en option || ✅ (29/09/2026) |
| 9 | Diversité des types d'établissement | 05, section 5 | 11 communes ont les 4 types (21,9 % de la population) ; un habitant sur trois (35,2 %) vit dans une commune qui en a au plus un | une phrase sous la carte du statut | basse | en option || ✅ (29/09/2026) |
| 10 | Mobile money et agences : complément, pas substitut ; variante avec la Poste | 05, C9 (Spearman 0,50) ; 07, O4-05 | là où il y a plus d'agences, il y a aussi plus de mobile money ; avec la Poste, Kpendjal 1 et Kozah 4 quittent « mobile money uniquement » | deux phrases sous la carte du statut | basse | en option || ✅ (29/09/2026) |

**Écartés** : les ratios par strate (05, figure 3 : repris par l'écart entre villes et campagnes de la page Offre financière) ; les préfectures extrêmes (visibles sur les cartes) ; les contradictions de l'exploration (05, section 7 : elles alimentent les 25 communes de la page Diagnostic) ; les grappes locales (06, carte 7 : signaux sans correction pour tests multiples).

**Corrections sur la page actuelle** :

- ✅ (29/09/2026) **C8** : les filtres de la barre latérale ne changent rien sur la page (la table filtrée est calculée mais pas utilisée, comme sur l'ancienne page Offre financière) ; la maille de la barre latérale est ignorée (cartes à la commune seulement).
- ✅ (29/09/2026) **C9** : en anglais, les statuts (« desserte faible », « mobile money dominant »…), les classes du tableau des communes divergentes (« bien desservi », « tendu »…) et les lignes de la matrice restent en français. Même défaut sur la page Carte pour l'indicateur « statut d'accès ».
- ✅ (29/09/2026) **C10** : les en-têtes de la matrice disent « (proxy) » ; écrire « couverture théorique ».

### B. Objectif 5 : pages Priorités, Diagnostic, Recommandations, Estimations et projections

**Ce que le tableau de bord montre déjà** :

| Page | Déjà affiché |
| --- | --- |
| Priorités | 4 chiffres clés ; bandeau « ce classement ne porte pas sur l'usage d'Internet » ; carte des classes avec curseurs de poids ; tableau des tests de robustesse ; comparateur de deux préfectures ; répartition des classes |
| Diagnostic | 4 chiffres clés ; fiche d'une préfecture (chiffres, sans phrase) ; carte des 25 communes signalées ; usage d'Internet par région |
| Recommandations | 12 cartes filtrables par thème, nature et horizon ; vue d'ensemble ; carte des priorités ; ordre d'action ; qui agit ; ce qui n'est pas recommandé |
| Estimations et projections | chiffres clés ; « où va-t-on si rien ne change » ; scénarios d'usage à 2030 ; trajectoires de référence ; cibles (une ligne par recommandation) |

**Constat** : la page Priorités ne montre **pas le classement** : on voit la carte des classes, mais aucune liste des préfectures avec leur score, leurs trois dimensions, leur confiance et leur population, alors que le 08 demande de les afficher « sur la même vue ». La fiche du Diagnostic donne des chiffres, mais pas la phrase de diagnostic qui la résume dans le 09. La page Recommandations n'a que les cartes : les tableaux par thème et la vue par territoire du plan 11 (sections 8.3 et 8.4) manquent. Le suivi des cibles (O5-04 : base, cible, horizon, critère de succès) n'est pas affiché.

**Ce qui manque** :

| # | Analyse | Source | Ce qu'elle montre | Proposition | Priorité | À ajouter ? | Statut |
| - | --- | --- | --- | --- | --- | --- | --- |
| 11 | Le classement des 39 préfectures, décomposé | 08, figure 1 et section 6.1 ; plan 11, page 6 | classe, score, rang sur chaque dimension (agences, mobile money, couverture), confiance, population, statut, communes signalées ; ordre du 02 (classe, puis population) | graphique des trois rangs par préfecture (la couverture marquée comme estimation) et tableau des 39 préfectures, les 3 non classées à part | haute : cœur de la page, absent | oui || ✅ (29/09/2026) |
| 12 | Les 7 priorités hautes, ce qui les place en tête | 08, section 6.2 | aucune dimension n'explique seule le classement : Akébou a le pire accès aux agences, Blitta le mobile money le plus mince, Kéran la plus forte part hors couverture | trois phrases sous le graphique de l'item 11 | haute | oui || ✅ (29/09/2026) |
| 13 | Les classes qui dépendent de la couverture ; la carte sans elle | 08, section 7 et figure 2 | les 7 priorités hautes le restent sans la couverture ; 5 préfectures changent (Tandjoaré et Moyen-Mono montent, Sotouboua et Oti descendent, Vo monte) | la liste des 5 avec la raison ; une bascule « sans la couverture » sur la carte | moyenne : le chiffre clé dit « 5 » sans les nommer | oui || ✅ (29/09/2026) |
| 14 | La phrase de diagnostic de chaque préfecture | 09, section 7.1 ; plan 11, page 7 | ex. « Dankpen cumule les trois déficits ; tous les guichets à Dankpen 1 (41 % des habitants) ; 45 % des points mobile money à plus de 10 km d'un guichet » | en tête de la fiche, lue dans le 09 (comme les 27 indicateurs sont lus dans le 07) | haute : prévue au plan 11 | oui || ✅ (29/09/2026) |
| 15 | La carte d'identité des 10 préfectures | 09, figure 1 ; plan 11, page 7 | un tableau coloré : les trois dimensions et les facteurs associés, foncé = parmi les plus défavorables | tableau coloré (tableau de chaleur) des 10 préfectures | haute : prévue au plan 11 | oui || ✅ (29/09/2026) |
| 16 | La nature du déficit et les leviers possibles | 09, sections 7.3 et 7.5 | 4 natures : cumul (Dankpen, Oti-Sud, Kpendjal-Ouest) ; agences d'abord (Akébou, Est-Mono, Kpendjal) ; mobile money mince (Blitta, Mô, Tchamba) ; couverture d'abord (Kéran) ; un levier par déficit | tableau « nature du déficit → leviers » qui renvoie aux recommandations | moyenne : relie diagnostic et recommandations | oui || ✅ (29/09/2026) |
| 17 | Ce qui se répète ; deux situations parmi les communes sans agence | 09, sections 7.2 et 6 | 4 facteurs sur 10 se répètent (distance, part urbaine, densité, types d'établissement) ; dans les préfectures prioritaires, l'isolement (guichet à 13 à 38 km, réseau incertain) ; ailleurs, le guichet est dans la commune voisine (6 à 17 km, réseau présent) | tableau des facteurs (priorités hautes contre les autres) ; deux phrases sur les communes | moyenne | oui || ✅ (29/09/2026) |
| 18 | Ce que le marché apporte aux territoires | 09, section 7.4 | fibre enterrée plus rare (26 km contre 49 en médiane) ; 5 des 10 préfectures sans agence Togocom ; la concurrence ne se mesure pas par territoire | une phrase | basse | en option || ✅ (29/09/2026) |
| 19 | Recommandations : la vue par thème | 10, sections 3 à 5 ; plan 11, section 8.3 | pour chaque thème, les territoires visés, leur situation, la cible et ce qu'il faut ajouter (ex. agences : Est-Mono +3, Blitta +7, Tchamba +9… ; mobile money : Dankpen +119, Blitta +74…) | quand un thème est choisi, son tableau au-dessus des cartes | haute : prévue au plan 11 | oui || ✅ (29/09/2026) |
| 20 | Recommandations : la vue par territoire | plan 11, section 8.4 | pour une préfecture choisie, toutes ses actions (ex. Dankpen : un point à Dankpen 2 et 3, +119 points mobile money, +39 397 habitants dans la couverture) | sélecteur de préfecture et tableau de ses actions | moyenne | oui || ✅ (29/09/2026) |
| 21 | Recommandations : filtres de priorité et de région, situation et cible sur chaque carte | plan 11, section 8.1 | la carte dit « situation aujourd'hui → cible, avec le seuil » ; lien vers la fiche du Diagnostic | deux filtres ; une ligne « aujourd'hui → cible » | basse | en option || non fait (option) |
| 22 | Le suivi des cibles | 10, section 7 (O5-04) | 16 lignes de suivi : base (millésime), cible, horizon, critère de succès (ex. frais du petit retrait : 7,5 % → 3 % au plus en 5 ans) | remplace le tableau actuel des cibles, qui ne donne que la cible | moyenne : indicateur de l'objectif 5 | oui || ✅ (29/09/2026) |

**Écartés** : la vue « par type d'action » (plan 11, section 8.5) : elle répète l'ordre d'action déjà affiché ; les exemples de cartes (plan 11, section 8.2) : ce sont des maquettes ; la validation par les analyses communales (08, section 8.2) : une phrase de contrôle, qui relève de la page Sources et méthode.

**Corrections** :

- ✅ (29/09/2026) **C11** : sur Priorités, des codes internes et du jargon : « D1 », « D2 », « D3 » (curseurs, tests), « P13 », « min-max », « rho », « rang percentile ». La robustesse affichée est celle de la règle stricte (chiffre clé « Robustesse : 10/39 » ; aucune des 7 priorités hautes n'y est robuste), alors que le 08 a validé la variante qui sert au diagnostic (les 7 priorités hautes robustes) : elle doit être affichée à côté (décision P13 du 08).
- ✅ (29/09/2026) **C12** : sur Diagnostic, le chiffre clé « Facteurs répétés : 1/4 » est faux : 4 facteurs sur 10 se répètent (6 ou 7 préfectures sur 7) ; le code ne compte que « 7 sur 7 ». Le constat répète en dur « 39 % » et « 6 % » au lieu de les lire dans la table.
- ✅ (29/09/2026) **C13** : en anglais, les valeurs des tables restent en français sur Diagnostic (classe, confiance, moteur, statut, signal), Recommandations (cible, territoires, nature, horizon), Priorités (classes) et Estimations et projections (cibles, horizons).
- ✅ (29/09/2026) **C14** : des numéros et des codes internes s'affichent : « R1 » à « R10 » dans le tableau des cibles (le plan 11 dit « les titres, jamais les numéros ») ; « O1-02 », « O1-05 », « P19 » dans le tableau « ce qui n'est pas recommandé ».
- ✅ (29/09/2026) **C15** : sur Estimations et projections, la couverture théorique « 88,4 % » est écrite en dur, pas lue dans une table.

### C. Les autres pages : Synthèse nationale, Carte, Sources et méthode

| # | Analyse ou traitement | Source | Proposition | Priorité | À ajouter ? | Statut |
| - | --- | --- | --- | --- | --- | --- |
| 23 | Sigles et noms de sources sur toutes les pages hors Sources et méthode | demande du 28/09/2026 (4 pages d'objectifs) | même traitement que les 4 pages : Synthèse nationale (IMF, DAB, UIT, BCEAO, « guichet », « point formel »), Priorités, Diagnostic, Recommandations, Estimations et projections (« point formel », « guichet », DAB, IMF, UIT). Les institutions nommées comme **acteurs** d'une recommandation (ARCEP, BCEAO dans « Qui agit ? ») restent nommées : ce sont des acteurs, pas des sources | haute : la Synthèse est la première page lue | oui || ✅ (29/09/2026) |
| 24 | Carte : les indicateurs de l'objectif 4 qui manquent | 07, O4-02 et O4-03 ; 06, carte 5 | ajouter « points mobile money par agence financière » (classes du 02), « points pour 10 000 adultes » et « part des points mobile money à plus de 10 km d'une agence » | moyenne | oui || ✅ (29/09/2026) |
| 25 | Sources et méthode : les décisions prises en cours de projet | plan 11, page 10 | la liste des décisions validées (variantes, conventions) avec leur date ; aujourd'hui, seules les conventions sont affichées | basse | en option || non fait (option) |

**Corrections** :

- ✅ (29/09/2026) **C16** : sur Sources et méthode, le tableau des 27 indicateurs affiche des astérisques de mise en forme (« **39,48 % en 2024** » s'affiche avec ses astérisques) ; les retirer à la lecture. En anglais, ce tableau reste en français (il est lu dans le 07) : le dire dans une note.

**Règles de mise en œuvre** (rappel) : chaque visuel en français et en anglais ; aucun code ni numéro de document sur les pages (sauf Sources et méthode) ; aucun sigle ni nom de source sur les pages d'analyse ; chaque visuel porte son constat et sa limite ; les tables sont lues telles quelles, sans recalcul ; phrases de lecture en bleu foncé, chiffres d'un constat dans la couleur de leur série, noms de région en couleur.

**Points à valider** :

| # | Question | Proposition |
| --- | --- | --- |
| V14 | Structure de la page Population et offre, qui n'a pas d'onglets | **Proposé** : 4 sous-onglets, comme les pages des objectifs 1 à 3 (structure ci-dessous). Autre choix : garder une seule page. **Validé (28/09/2026)** |
| V15 | Structure des pages de l'objectif 5 | **Proposé** : des sous-onglets pour les trois pages qui s'allongent : Priorités (Vue synthèse, Classement, Poids et robustesse, Comparateur) ; Diagnostic (Vue d'ensemble, Fiche de préfecture, Communes signalées) ; Recommandations (Les 12 actions, Par thème, Par territoire, Ordre d'action et acteurs). Estimations et projections reste d'un seul tenant (seul le tableau des cibles change). **Validé (28/09/2026)** |
| V16 | Sigles et sources hors des 4 pages d'objectifs (item 23) | **Proposé** : étendre le traitement à toutes les pages sauf Sources et méthode, où les codes et les noms restent permis. **Validé (28/09/2026)** |
| V17 | Périmètre | Les items de priorité haute et moyenne (1 à 7, 11 à 17, 19, 20, 22 à 24) ; les items 8 à 10, 18, 21 et 25 en option. **Validé (28/09/2026)** |
| V18 | Corrections C8 à C16 | Les faire en même temps. **Validé (28/09/2026)** |
| V19 | Ordre de mise en œuvre (le travail est plus gros que pour les objectifs précédents) | **Proposé** : trois étapes, chacune testée, capturée et cochée avant la suivante : 1) objectif 4 (items 1 à 10, C8 à C10, item 24) ; 2) objectif 5 (items 11 à 22, C11 à C15) ; 3) autres pages (items 23 et 25, C16). **Validé (28/09/2026)** |

**Structure proposée pour la page « Population et offre »** (si V14 est validé) :

| Onglet | Contenu | Items |
| --- | --- | --- |
| Vue synthèse | les 4 chiffres clés actuels (en langage clair) ; le constat ; une synthèse chiffrée (« 66 communes, 65,4 % de la population : le mobile money y remplace presque les agences ») qui renvoie à chaque onglet | — |
| Habitants par point de service | les deux cartes, agences et mobile money, en classes du 02 (seuils des agences toujours déplaçables) ; répartition de la population par classe ; densité et repère UEMOA | 3, 5, 6 |
| Agents par guichet et mobile money seul | la carte des agents par guichet ; les 22 communes avec leur distance au guichet ; la distance par région | 1, 2, 4 |
| Statut et couverture | la carte du statut d'accès, avec sa variante ; la matrice et les 8 communes en cellule critique ; les communes qui divergent de leur préfecture | 7 à 10 |

Question de la page, inchangée : « Combien d'habitants par point, et où le mobile money est-il seul ? ».

### ✅ (29/09/2026) Mise en œuvre, étape 1 : objectif 4

Tout est validé le 28/09/2026 (V14 à V19). Étape 1 construite le 29/09/2026 ; les options 8 à 10, peu coûteuses (deux phrases et une ligne de chiffres), sont faites avec elle.

- **Page « Population et offre »** (`dashboard/views/population.py`, refaite) : quatre sous-onglets. Question inchangée.
  - **Vue synthèse** : les 4 chiffres clés en langage clair (22 communes sans agence, dont 17 à plus de 10 km d'une agence ; 66 communes où le mobile money supplée, 65,4 % de la population ; 3 communes au maillage insuffisant ; 8 communes à double fragilité) ; constat « le mobile money est partout, l'agence financière non ; la préfecture cache les communes » ; synthèse chiffrée « 66 communes », une puce par onglet.
  - **Habitants par point de service** (items 3, 5, 6) : la carte des habitants par agence (seuils toujours déplaçables) et, à côté, celle des habitants par point mobile money en classes (dense, acceptable, insuffisant), chacune avec la répartition de la population par classe ; le Togo face à l'UEMOA (4,38 agences bancaires pour 100 000 adultes contre 3,52 ; 6,93 distributeurs contre 5,15), toujours avec « mais 21 préfectures sur 39 sont en dessous » ; tableau des densités par région (le Grand Lomé a 39 à 137 fois plus d'agences au km²).
  - **Agents par agence et mobile money seul** (items 1, 2, 4) : la carte des points mobile money par agence en 4 classes, les 66 communes en violet et les 22 en rouge comme sur la carte du statut ; part des points mobile money à plus de 5 et 10 km d'une agence, par région ; le tableau des 22 communes où le mobile money est seul, de la plus éloignée (Kpendjal 1, 37,8 km) à la moins éloignée, avec la commune de l'agence la plus proche et les voisines dotées.
  - **Statut et couverture** (items 7 à 10) : la carte du statut, avec sa variante ; les 8 communes à double fragilité, avec leur couverture et les 3 valeurs douteuses ; la matrice statut × couverture ; les communes qui divergent de leur préfecture, avec leur nombre par mesure (58, 41, 27 ; 77 sur 117) ; les phrases sur la diversité des types (11 communes ont les 4 types), le mobile money qui complète plus qu'il ne remplace (lien de 0,50) et la variante avec la Poste (Kpendjal 1 et Kozah 4).
- **Filtres (C8)** : cartes et tableaux suivent les filtres de région, de priorité et de milieu, et la maille de la barre latérale.
- **Deux langues (C9)** : une fonction `valeur()` dans `dashboard/i18n.py` donne un libellé en clair des valeurs des tables (classes, statuts, couverture, priorités, confiance, nature, horizon), en français et en anglais ; elle servira aux étapes 2 et 3. La page Carte l'utilise aussi (statut, classe de priorité).
- **Matrice (C10)** : colonnes « couverte (plus de 85 %) », « partielle (50 à 85 %) », « zone blanche (moins de 50 %) », « inconnue », au lieu des libellés « (proxy) » et « (A13) ».
- **Page Carte** (item 24) : trois indicateurs, « agents mobile money par agence financière » (4 classes), « points mobile money pour 10 000 adultes » et « points mobile money à plus de 10 km d'une agence » (commune seulement, la seule maille mesurée).
- **Vérifié** : un test de la page (4 onglets, deux langues, deux mailles, chiffres attendus, aucun sigle, nom de source ni code, aucune valeur restée en français en anglais, nombre de territoires sur chaque carte, filtre des Savanes, variante, seuil déplacé) ; un test de la Carte (7 indicateurs, deux mailles, deux langues) ; suite complète (11 pages, 4 + 5 + 4 + 4 onglets), tests du Marché, de l'Offre financière, de lisibilité et de la variante : tout passe. Captures d'écran des 4 onglets. Défauts vus sur les captures et corrigés : tableau des densités par région coupé (passé en pleine largeur) ; colonnes coupées du tableau des 22 communes et de la liste des 8 communes (en-têtes raccourcis, carte du statut rétrécie : le Togo est étroit) ; légende posée sur une barre ; tableau des communes divergentes coupé (colonne de la préfecture retirée : le nom de la commune la porte).

### ✅ (29/09/2026) Mise en œuvre, étape 2 : objectif 5

Construite le 29/09/2026. L'option 18 (une phrase) est faite ; l'option 21 (filtres de priorité et de région, ligne « aujourd'hui → cible » sur chaque carte) ne l'est pas : la vue par territoire (item 20) répond déjà à « quelles actions ici ? ».

- **Priorités** (`dashboard/views/priorites.py`, refaite) : 4 sous-onglets.
  - **Vue synthèse** : 4 chiffres clés (7 priorités hautes ; 3 non classées, nommées ; 5 préfectures dont la classe dépend de la couverture, nommées ; robustesse 7/7 dans la lecture retenue, 0/7 à la lettre de la règle) ; carte avec une bascule « sans la couverture théorique » ; les 5 préfectures qui dépendent de la couverture, avec leur classe avec et sans elle (item 13).
  - **Classement** (items 11 et 12) : ce qui place les 7 priorités hautes en tête (position sur chaque mesure, score à côté du nom ; « Akébou a le pire accès aux agences, Blitta le mobile money le plus mince, Kéran la plus forte part hors couverture ») ; le tableau des 39 préfectures dans l'ordre de la règle (classe, score, position sur les trois mesures en barres, confiance, habitants, communes signalées) ; les 3 non classées à part.
  - **Poids et robustesse** : les curseurs de poids et leur carte ; la répartition des classes avec les deux lectures de la robustesse, la phrase qui les explique ; les tests en clair (« poids des agences doublé », « autre échelle (écrase les scores) », « sans le territoire extrême »), avec une « ressemblance » de 0 à 1.
  - **Comparateur** : deux préfectures, valeurs en clair.
- **Diagnostic** (`dashboard/views/diagnostic.py`, refaite) : 3 sous-onglets.
  - **Vue d'ensemble** : 4 chiffres clés, dont « 4 facteurs sur 10 se répètent » (C12) ; la carte d'identité des 10 préfectures (item 15), un tableau coloré des 3 mesures du classement et des 10 facteurs, foncé = parmi les plus défavorisées ; ce qui se répète (item 17) ; ce que le marché apporte (item 18) ; nature du manque et leviers (item 16) ; usage d'Internet par région.
  - **Fiche de préfecture** : la phrase de diagnostic en tête (item 14), réécrite dans le vocabulaire des décideurs et traduite ; les chiffres en clair ; les leviers possibles ; les communes signalées.
  - **Communes signalées** : les deux situations (isolement dans les préfectures prioritaires, 12,8 à 37,8 km ; agence dans la commune voisine ailleurs, 6,4 à 16,6 km) ; la carte, les autres communes en gris ; la liste, de la plus éloignée à la moins éloignée.
- **Recommandations** (`dashboard/views/recommandations.py`, refaite) : 4 sous-onglets. **Les 12 actions** (cartes : titres, cibles et territoires réécrits et traduits, chiffres lus dans les tables) ; **Par thème** (item 19 : les 22 communes et leur ordre, les 10 préfectures et les agences à ajouter, le maillage mobile money, les 14 communes à mesurer, l'extension du réseau, la fibre, les prix et frais, les compétences, l'investissement) ; **Par territoire** (item 20 : toutes les actions d'une préfecture, ex. Dankpen : une agence à Dankpen 2 et 3, +119 points mobile money, +39 397 habitants dans la couverture) ; **Ordre d'action et acteurs** (les 4 rangs avec les titres, jamais les numéros ; qui agit ; ce qui n'est pas recommandé, sans codes).
- **Estimations et projections** : le suivi des cibles (item 22 : 16 lignes, aujourd'hui, cible, horizon, « réussi si ») remplace le tableau qui ne donnait que la cible et les numéros R1 à R10 (C14) ; noms des scénarios et des repères traduits ; une couleur fixe par scénario (décocher un scénario ne repeint plus les autres) ; la couverture « 88,4 % » écrite en dur remplacée par ce que dit la table : 86 communes sur 117 couvertes à plus de 85 % (C15).
- **Deux langues (C13)** : `valeur()` (dans `dashboard/i18n.py`) reçoit les signaux des communes, les dimensions du score, les leviers, la lecture des facteurs, les classes des scénarios ; aucune valeur de table ne reste en français sur ces pages en anglais.
- **Codes (C11, C14)** : plus de « D1 », « D2 », « D3 », « P13 », « min-max », « rho », « R1 »… ni de « O1-02 » sur ces pages.
- **Mise en forme des tableaux** : `formater()` (dans `dashboard/composants.py`) donne aux tableaux sans colonne de région les nombres au format de la langue ; les années restent sans séparateur. Les tableaux de phrases (ordre d'action, acteurs, pistes non retenues, suivi des cibles) sont statiques : leur texte revient à la ligne.
- **Vérifié** : un test des 4 pages (chaque onglet, deux langues, chiffres attendus, aucun sigle, nom de source ni code, aucune valeur restée en français en anglais) ; les 7 thèmes et les 22 territoires de la page Recommandations ; suite complète (11 pages, 4 + 5 + 4 + 4 + 4 + 3 + 4 onglets) et tous les tests précédents : tout passe. Captures d'écran de chaque onglet. Défauts vus sur les captures et corrigés : « None None None » affiché au-dessus de la carte d'identité (une ligne de code lue comme un tuple par Streamlit) ; carte d'identité aux en-têtes inclinés (transposée) ; étiquettes de score posées sur les points ; colonnes coupées dans 9 tableaux (cartes rétrécies, colonnes fusionnées, tableaux statiques) ; nombres bruts (« 76652 », « 12.8 ») ; « Non classée » avec une majuscule ; « +1 agences » ; carte des communes signalées sans le contour du pays.

### ✅ (29/09/2026) Mise en œuvre, étape 3 : les autres pages

- **Synthèse nationale** (item 23) : même vocabulaire que les pages d'objectifs. « Agence financière » pour le point formel et le guichet (chiffre clé « Agences financières (2021/2022) », « Mobile money et agences », « Agence rare ») ; « microfinance » et « distributeur de billets » au lieu d'IMF et de DAB ; « estimation internationale » et « définition de la banque centrale » au lieu de l'UIT et de la BCEAO ; les actions nommées sans numéro, leurs territoires lus dans les tables et leurs horizons traduits.
- **Page Carte** : la limite de la couverture dit « estimation », plus « proxy ». Les autres pages (objectif 5) ont reçu ce traitement à l'étape 2.
- **Sources et méthode** (C16) : plus d'astérisques dans le tableau des 27 indicateurs ; en anglais, une note dit que ce tableau est lu tel quel dans le document des indicateurs, écrit en français. Les codes et les noms des sources y restent : c'est la page où ils sont expliqués.
- **Non fait** : l'option 25 (la liste des décisions du projet sur la page Sources et méthode).
- **Vérifié** : un test de l'étape (Synthèse nationale, les 13 indicateurs de la Carte, Sources et méthode ; deux langues ; aucun sigle, nom de source ni code hors de Sources et méthode ; aucune valeur restée en français en anglais) ; toutes les suites précédentes : tout passe. Capture d'écran de la Synthèse nationale.

La demande de la section « Pages des objectifs : sigles et noms de sources » (plus haut) couvre donc désormais toutes les pages : la mention « la Synthèse nationale garde ses sigles » n'est plus vraie depuis le 29/09/2026.

---

## Déploiement et archive de soumission

Demande du 29/09/2026 : créer les workflows de déploiement comme dans le projet du défi 1 et générer le fichier zip. Le dossier `workspace/` et le fichier 11 restent hors du zip, qui ne doit pas dépasser 20 Mo.

- ✅ (29/09/2026) **Chaîne CI/CD** reprise du défi 1 (`.github/workflows/ci-cd.yml`) : lint (ruff) et concordance des dépendances ; tests (pytest) ; construction de l'image Docker et test de fumée (santé, 11 routes, données embarquées, ni données brutes ni secrets) ; déploiement Heroku sur un push dans `main` seulement. Branches : `dev` et les PR vers `main` valident, `main` déploie.
- ✅ (29/09/2026) **Fichiers ajoutés** : `Dockerfile` et `.dockerignore` (liste blanche : l'image ne reçoit que `dashboard/`, les tables de `data/analysis/`, les contours et `07_indicators.md`) ; `requirements.txt` (tout le projet) et `requirements-runtime.txt` (tableau de bord seul) ; `pyproject.toml` ; `scripts/check_requirements_sync.py` ; `tests/test_pages.py` (67 tests : 11 pages et tous leurs onglets, deux langues, vocabulaire, tables lues) ; `README.md` réécrit.
- ✅ (29/09/2026) **Archive** : `scripts/make_submission.sh` construit `Togo-Defi2-EconomieNumerique.zip` (12 Mo, 310 fichiers) par liste blanche et échoue au-delà de 20 Mo. Absents : `workspace/`, le 11, `tmp/`, `_PROJECT.txt`, `.github/`, `.env`, `.git/`, `data/raw/` (491 Mo, dont des micro-données non redistribuables). Le zip est ignoré par git.
- **Vérifié** : lint et concordance des dépendances ; 67 tests ; image construite avec Podman et démarrée comme dans la CI (santé, 11 routes en 200, 137 tables et les contours embarqués, pages rendues) ; archive décompressée dans un dossier vierge, où les 67 tests passent aussi.
- **Corrigé au passage** : 5 erreurs de lint (imports morts, une variable inutilisée, un f-string sans variable) ; un « point formel » resté dans une note de la page Marché.
- ✅ (29/09/2026) **README destiné au jury** : la section sur le déploiement est retirée et remplacée par « Vérifier » (lancer les tests) ; plus de mention de la production. La présentation figure dans le tableau des documents.
- ✅ (29/09/2026) **Présentation dans l'archive** : `Togo-Economie-Numerique-Defi2.pptx` (524 Ko) ajouté à la liste blanche de `scripts/make_submission.sh`. Archive reconstruite : 13 Mo, 312 entrées, contrôle des exclusions passé.
- **À faire par l'utilisateur** : commiter et pousser ; dans le dépôt GitHub, poser le secret `HEROKU_API_KEY` et la variable `HEROKU_APP_NAME` (`togo-econum-finance-defi2`, d'après le remote `heroku`) ; fusionner `dev` dans `main` pour déclencher le déploiement.

