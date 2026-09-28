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
