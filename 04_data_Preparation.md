# 04 — Data Preparation et Data Quality

*Comment passer des fichiers bruts aux tables qui portent les décisions, sans perdre, doubler ni inventer une valeur ?*

Ce document suit le 03. Le 03 décrit ce que contient chaque fichier, ce qu'il permet de mesurer, et tranche les choix de traitement (section 11 : décisions A, P, Q, R, S). Le 04 ne les réexplique pas : il les **applique**, dans un ordre fixé, et **contrôle** chaque transformation. Il couvre les étapes 05 (qualité et validation) et 06 (tables de décision) de la procédure.

La référence est la liste des 5 objectifs de `_PROJECT.txt`, lus comme dans le 01. Le 02 fixe les indicateurs, et tout écart au 02 est déclaré (intro du 03).

**État au 26/09/2026 : exécutée.** Les 9 scripts de `prep/` produisent les tables de `data/processed/` en 13 secondes (`python3 prep/executer_tout.py`). **138 contrôles, aucun bloquant en échec, 2 écarts signalés** (DD3, SN4) ; 2 151 lignes au registre. Deux corrections de l'étape 5 viennent de l'exploration (05) : totaux de l'ARCEP incohérents avec leurs opérateurs, écartés (DD5) ; rupture de périmètre du CA fixe (GVA, SN5). Les effectifs « attendus » venaient du 03 ; la colonne « constaté » de la section 7 donne le résultat. Les constats de l'exécution (V4 à V7) sont tranchés le 26/09/2026, y compris la source de O3-05 : **aucun point n'est en attente**.

---

## Principes appliqués à chaque étape

1. **Les fichiers de `data/raw/` ne sont jamais modifiés.** Chaque transformation est un script qui lit `raw` et écrit dans `interim` ou `processed`.
2. **Un NULL ne devient jamais un 0.** Trois états restent distincts : une valeur, un zéro vérifié, un manquant avec son motif.
3. **Le niveau de preuve (A, B, C) suit chaque variable** dans une colonne, jusqu'au tableau de bord.
4. **Une source par série et par période.** Pas de raccord sans égalité au point de jonction (P4).
5. **Toute convention a sa variante de sensibilité**, préparée dans la même table.
6. **Les bases de population ne se mélangent pas** : une colonne dit laquelle sert de dénominateur (encadré de la section 9 du 03).
7. **Chaque étape suit le même parcours** : avant → transformation → contrôle → résultat, avec les effectifs à chaque flèche.
8. **Ni ratio, ni classement, ni score ici.** Les tables portent les numérateurs et les dénominateurs ; les indicateurs du 02 sont calculés à l'étape suivante (procédure : aucun score avant l'étape 09).

## Sommaire

1. Organisation et ordre d'exécution
2. Nettoyage : valeurs manquantes et modalités
3. Dédoublonnage
4. Référentiel territorial et jointures
5. Séries nationales et enquêtes
6. Tables analytiques
7. Contrôles qualité
8. Registre des anomalies et journal de préparation
9. Points de validation

---

## 1. Organisation et ordre d'exécution

```
data/
├── raw/          sources, jamais modifiées (_INVENTORY_datasets.txt ; _extradatas/_MANIFEST.csv)
├── interim/      jeux nettoyés, AR1 extrait (toutes publications), rattachements
└── processed/    tables analytiques (section 6), contours, registre des anomalies
prep/             un script par étape (p01 à p09), commun.py (chemins, normalisation, registre, journal),
                  ar1_extraction.py (lecture des PDF de l'ARCEP), executer_tout.py (lance les 9 étapes)
```

**Dépendances** : pandas, geopandas, shapely, pyproj, PyMuPDF, openpyxl, pyreadstat (installé le 26/09/2026 pour lire l'Afrobaromètre), et `pdftotext` (poppler) pour le tableau de bord de la BCEAO. Une étape dont un contrôle bloquant échoue arrête la chaîne.

**Format de sortie** : CSV UTF-8, séparateur virgule, point décimal ; codes territoriaux en texte ; dates ISO. Le tableau de bord sera probablement fait en Python, plus rapide ici (V3) ; ces tables se liraient aussi dans Power BI, l'autre outil admis par `_PROJECT.txt`. Contours en GeoJSON.

| Étape | Script | Entrées | Sorties | Sections |
| ----- | ------ | ------- | ------- | -------- |
| 1 | `p01_referentiel` | 6b (contours), noms geodata (5c) | `interim/referentiel_territoires.csv`, contours reconstitués (`processed/geo/`) | 4 |
| 2 | `p02_population` | RG2, RG3 ; D6 en contrôle | `interim/population_territoires.csv` | 4 |
| 3 | `p03_points` | D4, 4c, D5, GD1 | `points_service` | 2, 3, 4 |
| 4 | `p04_territoires` | étapes 1 à 3 ; 3i ; 4j (contrôle) | `dim_territoire`, `terr_commune`, `terr_prefecture`, `terr_region` | 6 |
| 5 | `p05_ar1` | AR1 (34 PDF) | `interim/ar1_brut.csv`, `ar1_toutes_publications.csv`, `ar1_trimestriel.csv` | 3, 5 |
| 6 | `p06_series` | D1/1b, D2, 2b, D3, 3g, AR1, IT1, 4g, 4h, IN1, IN3 | `serie_nationale` | 5 |
| 7 | `p07_enquetes` | W1, W2, W3, W4 | `enquetes_region` | 5 |
| 8 | `p08_references` | C5, C5b, IT1, BC2 ; CH1 | `benchmark`, `chronologie` | 6 |
| 9 | `p09_controles` | toutes les sorties | `_registre_anomalies`, `_controles`, `_journal_preparation` | 7, 8 |

Les étapes 1 à 4 servent les objectifs 3 et 4 ; les étapes 5 à 8, les objectifs 1 et 2 et le volet national de l'objectif 3. Les deux blocs sont indépendants, comme le prévoit l'ordre de traitement du 01. **Non préparés** (décisions du 03) : GD2 (étape 11 seulement), 2e (C1), C7, BM8, RG1 (S10), micro-données MICS6 (S9) ; GD3, non téléchargé (V2) ; IN2 (postes de l'indice des prix jusqu'en 2017), BC1 (rapport sans tableau exploitable).

---

## 2. Nettoyage : valeurs manquantes et modalités

### 2.1 Valeurs manquantes

Chaque manquant devient `NA`, avec un motif dans une colonne `<variable>_motif`. Aucun n'est remplacé par 0.

| Jeton brut | Où | Devient | Motif |
| ---------- | -- | ------- | ----- |
| `Nsp`, `Nsp ` (espace final), `Néant`, `N/a` | D4 (`activite_statut`, `etab_adresse`), D5 (`operateur`), 4c (`etab_nom`) | `NA` | `non_renseigne` |
| cellule vide, `NULL` | tous les CSV | `NA` | `non_renseigne` |
| couple indicateur × année absent (15 dans D2) | D2 | ligne absente, jamais 0 | `non_publie` |
| champ masqué « N/A » | couches geodata | non repris | `non_publie` |
| 0 % à Mô et à Kpendjal, 0,05 % à Tchamba ; par extension, toute unité sous 1 % où D5 compte des points (Sotouboua 2, Kéran 3 : V4) | 3i (couverture à 20 km) | `NA` | `non_determinable` (A13) |

**Zéro vérifié** : une unité sans établissement (D4) ou sans DAB (4c) reçoit 0, justifié par la colonne `enquete_prouvee = 1` : D5 prouve que chaque commune a été enquêtée (A13 ; constaté : 117 communes sur 117). Cela concerne 22 communes et la préfecture de Kpendjal pour les points formels en service. Sans preuve d'enquête, le comptage serait `NA`.

`Autre` (7 lignes du statut de D4) est une modalité, pas un manquant : elle rejoint les statuts inconnus de A6.

### 2.2 Modalités

La valeur d'origine est toujours conservée à côté de la valeur harmonisée.

| Jeu | Variable | Transformation | Règle |
| --- | -------- | -------------- | ----- |
| D4 | `activite_statut` | espaces retirés ; « Utilise » → « Utilisé » ; regroupement : en service (660), hors service (17 : fermé, en construction, abandonné, inachevé, en réfection, sans local, location), inconnu (61 : Néant, Nsp, N/a, Autre) | A6 |
| D4 | `activite_categorie` | « Micro-Finace » → « Micro-Finance » ; « Mutuelle » (9) → type IMF | A7 |
| D4 | `etab_nom`, `nom_localite` | espaces retirés ; forme normalisée calculée à la volée pour les comparaisons, jamais stockée à la place du nom | — |
| D4 | `etab_jour`, `etab_adresse`, `toilette_type` | non repris : hors sujet ou inutilisables | 03, section 4 |
| D5 | `operateur` | éclaté en `op_moov`, `op_togocom` (1 / 0 / NA) et `nb_operateurs` ; « Nsp » → NA pour les deux | A8 |
| GD1 | statut | même regroupement que D4 : 84 agences en service sur 95 | Q5 |
| D2 | type d'accès | nomenclature mobile (GPRS/EDGE, 3G, 4G, 5G) / fixe ; EvDo, CAFE, GVA, TEOLIS, Illiconet, LS → « Fixe, technologie non précisée » | A3 |
| Tous | opérateurs | « Moov Africa (Atlantique Telecom) », « Togocom (Togo Cellulaire) » ; l'ARCEP écrit « YAS Togo (Togo Cellulaire) » en 2026 | A2 |
| Tous | noms de territoires | forme normalisée pour la jointure seulement (majuscules, sans accents, tirets et espaces unifiés) ; libellé affiché = celui de geodata | 03, section 7 |
| D4, 4c, D5, GD1 | `geometry` | WKT `POINT (lon lat)` → `lon`, `lat` numériques (WGS 84) | — |

---

## 3. Dédoublonnage

Le 03 ne trouve aucun doublon de ligne ni d'identifiant dans D4, 4c et D5. Le risque est ailleurs : **compter deux fois un même lieu ou une même valeur**, parce qu'un point sert deux opérateurs, qu'un trimestre est publié plusieurs fois, ou que deux sources donnent la même grandeur.

| #   | Cas | Risque | Règle | Fondement |
| --- | --- | ------ | ----- | --------- |
| DD1 | D4 : 18 paires de même catégorie à moins de 30 m | un établissement compté deux fois | présélection automatique, puis contrôle visuel de chaque paire (V1) ; la ligne secondaire n'est jamais supprimée, elle reçoit un `doublon_de` | 02, O3-01 : « dédoublonnage siège / agence » |
| DD2 | D5 : 12 649 points « Moov, Togocom » | additionner les points par opérateur donne 31 089 pour 19 788 lieux | on compte des lieux ; toute vue par opérateur est marquée « non additive » | A8 ; 02, O3-03 ; contrôle bloquant de la procédure |
| DD3 | D5 : points à environ 11 m d'un autre (03 : 974, dont 509 en surplus ; constaté : 972 et 508, cellules de coordonnées arrondies à 4 décimales, méthode du 03 non documentée) | doublons ou kiosques voisins, impossibles à distinguer | aucun dédoublonnage ; colonne `cellule_11m_partagee` ; sans effet sur les comptages | A8 |
| DD4 | Jeux du portail par catégorie (banques, microfinances, assurances, mutuelles) et « Établissements de Finance » | copies exactes de lignes de D4, avec un `FID` différent | jamais combinés avec D4 ; D4 est la seule source | 03, section 4 |
| DD5 | AR1 : chaque numéro couvre 5 trimestres ; certains numéros donnent deux fois la même série | un trimestre publié jusqu'à 5 fois, parfois révisé ; deux tableaux d'un même numéro qui se contredisent | une valeur par trimestre, celle de la publication la plus récente ; dans un même numéro, la première occurrence (ordre des pages). Constaté : 94 révisions d'au moins 5 % ; 428 doubles lectures, dont 340 égales, 57 écarts d'arrondi et 31 vrais conflits (en-tête mal hérité au T3 2023, deux tableaux de l'internet fixe au T2 2021) ; 6 valeurs retenues viennent d'un numéro en conflit (colonne `conflit_meme_numero`). **Ajout du 26/09/2026 (exploration)** : dans chaque numéro, un total de CA ou d'investissement qui s'écarte de plus de 10 % de la somme de ses opérateurs est écarté (28 valeurs) ; la publication cohérente précédente fait foi. Cas trouvé : les numéros de 2019 publient le CA fixe de 2018 en cumul depuis janvier, ce qui portait le CA de 2018 à 238,1 Md FCFA au lieu de 185,6 | P4 |
| DD6 | Grandeurs données par plusieurs sources | deux valeurs pour une même année | Internet : D2 / 2b jusqu'en 2017, AR1 ensuite ; CA : 2b et AR1 côte à côte, sans raccord ; population : RG2 / RG3, D6 en contrôle | A15, P4, A4, R4 |
| DD7 | DAB (4c) et agences bancaires (D4) | un DAB installé dans une banque compté comme un second point formel | les DAB restent un type à part : hors de l'agrégat des points formels, comptés dans la diversité et dans la version « par type » | 02, O4-01 ; A9 |
| DD8 | Agences de la Poste (GD1) | les ajouter aux points formels du calcul principal | comptées à part, en variante de sensibilité | Q5 |

**DD1 en détail (V1, validé).** La règle a deux temps :

1. **Présélection automatique** : paires de même catégorie (Mutuelle comptée en IMF) à moins de 30 m, soit 18 paires, toutes en service. Liste : `data/interim/D4_paires_meme-categorie_moins-30m.csv`.
2. **Contrôle visuel de chaque paire** : doublon si les deux noms désignent la même institution au même endroit. La décision de chaque paire est écrite au registre.

**Pourquoi pas un seuil de similarité.** Sur ces 18 paires, la correspondance exacte après normalisation ne retrouve aucun des 4 doublons, et un seuil de Levenshtein à 0,9 non plus (ECOBANK Akodessewa / ECOBANK d'Akodessewa : 0,900 exactement). Aucun seuil ne sépare les deux groupes : deux banques différentes, BTCI et IB Bank Agbalépédogan, obtiennent 0,714, plus que deux vrais doublons (COOPEC-AD Ramco : 0,682 ; FINAM Madiba : 0,429). Le nom du quartier, commun aux deux lignes, fait monter le score. La similarité est donc affichée comme aide à la lecture, pas comme critère.

**Fusion.** Dans chaque doublon, la première ligne du fichier devient la ligne principale ; ses champs vides sont complétés par ceux de la seconde, qui reste dans `points_service` avec `doublon_de` = ligne principale et sort des comptages. « 660 → 656 » veut donc dire : 4 lignes marquées `doublon_de`, fusionnées dans 4 lignes principales ; aucune ligne supprimée.

Résultat du contrôle visuel (26/09/2026) :

| Paire | Distance | Commune | Lecture |
| ----- | -------- | ------- | ------- |
| ECOBANK Akodessewa / ECOBANK d'Akodessewa | 3,9 m | Golfe 1 | doublon probable |
| COOPEC Grace plus Amadahomé / COOPEC Grâce plus Aménopé | 4,6 m | Golfe 5 | doublon probable |
| COOPEC-AD Ramco / COOPEC AD Agence Ramco | 24,3 m | Golfe 3 | doublon probable |
| FINAM Agence Madiba / Microfinance FINAM Adidogome Madiba | 25,6 m | Golfe 5 | doublon probable |
| FUCEC Togo Bè / COOPEC Maturité | 2,3 m | Golfe 1 | ambigu : faîtière et caisse locale au même endroit (cas « siège / agence ») |
| FUCEC Togo Afagnan / COOPEC Afagnan | 5,8 m | Bas-Mono 1 | ambigu : même cas |
| 12 autres paires (ex. BOA Lomé Port / ECOBANK Rond Point Port) | 12 à 28 m | — | institutions différentes dans un même lieu : gardées |

Effet : 660 points formels en service → 656 (4 doublons fusionnés, calcul principal) → 654 (2 cas ambigus fusionnés aussi, variante). Cinq des six paires sont dans le Grand Lomé ; l'effet sur sa part (O3-02) est faible, mais il existe.

---

## 4. Référentiel territorial et jointures

```
point (D4, 4c, D5, GD1)
   │  noms déclarés (_bdd), normalisés                        (A21)
   ▼
canton ............ 396 codes geodata
   ▼
commune ........... 117   ← population RG3 ; strate urbaine
   ▼
préfecture ........ 39    ← population RG2 ; contours reconstitués par fusion des communes
   ▼
région ............ 5 codes geodata  →  6 unités : Grand Lomé = Golfe + Agoè-Nyivé   (A12)
```

La clé est le **code geodata** à chaque niveau (A14). Le 03 a vérifié les jointures par les noms (section 7 : 100 % pour D4, 4c et D5 ; RG2 et RG3 sans correction). Le 04 les exécute :

| #  | Transformation | Attendu | Règle |
| -- | -------------- | ------- | ----- |
| R1 | Construire `dim_territoire` à partir des codes geodata : code, libellé, niveau, codes parents | 5 régions, 39 préfectures, 117 communes, 396 cantons | A14 |
| R2 | Corriger d'après leur position les codes de 5 cantons (Kati, Djemegni, Takpamba, Kpaha, Anima) ; garder et signaler 3 autres (Agome-Glozou, Akpakpakpé, Yokélé) | 8 lignes au registre | A21 |
| R3 | Reconstituer les contours des préfectures par fusion des communes de 6b ; ajouter les unités Grand Lomé et « Maritime hors Grand Lomé » | 3 débordements supprimés (Haho 1, Oti 2, Lacs 3) ; régions inchangées | A21, A12 |
| R4 | Calculer les superficies sur les contours reconstitués, avec la méthode du 03 | total 56 654,6 km² | 03, section 6 |
| R5 | Rattacher chaque point par ses noms déclarés au code du canton, puis aux niveaux supérieurs. La position ne sert que de contrôle | 100 % rattachés ; 49 points frontaliers et 47 points d'écart de contour signalés, jamais déplacés | A21 |
| R6 | Joindre la population : RG3 (communes), RG2 (préfectures, régions) : total, 15 ans et plus, urbain, rural. Âge non déclaré (24 180 personnes) réparti au prorata ; variante « hors non déclarés » | 8 095 498 habitants ; totaux égaux à D6 | R2, R4, S5 |
| R7 | Classer chaque commune dans une strate : Grand Lomé ; « autres villes » (50 % d'urbains ou plus) ; rural. Variante au seuil de 75 % | 13 / 13 / 91 communes ; variante 13 / 2 / 102 | décision du 26/09/2026 (O3-02) |

**Pourquoi pas de table par canton.** Le canton reste dans le référentiel et sur chaque point, mais il n'a pas de table analytique :
- il n'a pas de population utilisable : RG1 n'est pas transcrit (S10), D6 n'est joignable qu'à 318 cantons sur 375 hors Grand Lomé, et ses 222 quartiers du Grand Lomé ne correspondent pas aux 13 cantons de geodata ;
- `_PROJECT.txt` demande la région, la préfecture et la commune.

Une table par canton, limitée aux comptages, sera construite à l'étape 11 si le ciblage descend jusque-là (S10).

**Pourquoi pas de raster de population.** La procédure le recommande pour les tampons et l'optimisation. Nous n'avons que des tableaux de recensement : aucune opération par distance autour des points n'est donc prévue.

---

## 5. Séries nationales et enquêtes

| #   | Série | Sources | Transformation | Conventions et ruptures | Objectifs |
| --- | ----- | ------- | -------------- | ----------------------- | --------- |
| SN1 | Usage d'Internet | D1 / 1b (API) dans `serie_nationale` ; enquêtes dans `enquetes_region` (lignes nationales et régionales) | une série par source, jamais fusionnées ; note « estimation UIT » pour toutes les années sauf 2017 (INSEED) ; EIPT 2020 non préparée (valeur de l'annuaire AS1, à reprendre à la main si besoin) | chaque enquête garde sa population de référence | O1-01, O1-02, O1-03 |
| SN2 | Extraction de AR1 | 34 PDF, 3 mises en page | lecture par la position des mots (les séparateurs de milliers rendent le texte ambigu) ; seuls les tableaux sont lus, jamais les graphiques ; 13 140 lignes lues, 1 755 valeurs trimestrielles retenues (12 indicateurs, T1 2017 à T2 2026) ; montants publiés en FCFA (T3 2020) et transactions publiées en unités (jusqu'en 2022) ramenés à une seule unité ; Moov « 3G » jusqu'au T4 2019 requalifiée 3G+4G. Aucune note de méthode trouvée pour la rupture du T1 2020 | contrôles : somme des opérateurs = total, somme des technologies = total par opérateur, mobile + fixe = secteur (tous sans écart) ; rupture du T1 2020 retrouvée (-6,6 %) | P5, S6 |
| SN3 | Abonnements Internet, par opérateur et par technologie | D2 / 2b jusqu'en 2017, AR1 ensuite | annuel = valeur du T4 (**convention**), variante moyenne des 4 trimestres ; valeurs 2019 de D2 et 2b écartées | rupture du T1 2020 (S6) : aucune évolution calculée à travers | O1-02, O1-04, O2-07 |
| SN4 | Téléphonie, parts de marché | D3 (2013-2019), AR1 | total des abonnés : D3 jusqu'en 2017, AR1 ensuite (raccord vérifié : écart nul en 2018). **Parts par opérateur : D3 seulement (2013-2019)**, car l'ARCEP ne publie les abonnés à la téléphonie par opérateur que dans des graphiques (V5) | convention du T4 | O2-01 |
| SN5 | CA et investissement | AR1 (par opérateur), 2b (CA national 2010-2022), D3 (ratio 2013-2019), 3g (historique) | flux : annuel = somme des 4 trimestres ; 2b et AR1 gardés séparés (écarts de 2,8 % et 3,7 %) | ruptures : T2 2025 (Togo Telecom, fixe), T2 2026 (mobile money de YAS non déclaré). **Périmètre** : le CA fixe publié exclut GVA en 2018-2019 (6 trimestres) et du T1 2021 au T1 2023 ; signalé sur les totaux fixe et secteur. Le CA de GVA en 2021 (5,7 Md FCFA) explique l'essentiel de l'écart entre 2b et l'ARCEP (6,2 Md FCFA) | O2-02 à O2-04 |
| SN6 | Composantes de O2-05 | AR1 ; IT1 | O2-05a : CA mobile et abonnés à la téléphonie mobile, **au niveau national** (abonnés par opérateur publiés en graphique seulement, V5) ; abonnés moyens = moyenne des 4 stocks (**convention** ; variante T4). O2-05b : panier « 1 Go, data seule » **2023-2025 seulement** ; les autres paniers (1 Go postpayé sur ordinateur 2013-2017, 1,5 Go 2018-2020, 2 Go 2021-2025, 5 Go 2022-2025) sont des séries distinctes, jamais enchaînées (V6) | 2026 : un semestre seulement | O2-05 |
| SN7 | Mobile money, national | AR1 (depuis le T2 2020), 2b (2013-2022), 4h (Findex) ; BC2 dans `benchmark` | comptes, points de vente, valeur et nombre de transactions par opérateur ; Findex repris tel que publié | rupture 2019-2020 de 2b signalée, non corrigée (A20) ; **comptes AR1 : rupture au T1 2021** (révision de l'ARCEP, comptes Moov ramenés de 3,35 à 1,31 million ; T3-T4 2020 sur l'ancienne base) | O3-04 |
| SN8 | Dénominateurs annuels | IN1 | population totale et 15 ans et plus par année | base IN1 pour nos taux nationaux ; D1 garde la sienne | P3, R2 |
| SN9 | Prix | IN3a (2010-2022), IN3b (2014-2024), 4g (inflation 1967-2022) | indices mensuels de la fonction « Communication » et de l'ensemble ; inflation annuelle | saut de décembre 2019 à décembre 2020 : +15,2 %, signalé, non lu comme une hausse ; cause toujours non vérifiée (S7) | O2-03 (en réel) |
| EQ1 | Enquêtes par région | W2 (micro-données EHCVM), W1 (tableaux MICS6), W4 (Afrobaromètre, 6 vagues), W3 (base Findex) | EHCVM (15 ans et plus) : accès à Internet **déclaré** (la variable dit « a accès », pas « utilise »), téléphone portable, compte « banque ou autre », alphabétisation ; IC 95 % par linéarisation (grappes, strates région × milieu). Afrobaromètre : usage d'Internet (toute fréquence) et, en vague 9 seulement, compte mobile money ; IC approximatif. MICS6 : 590 valeurs publiées (compétences TIC ODD 4.4.1, équipement). **Module 6 de l'EHCVM** : mobile banking des 15 ans et plus (2018/19 : « possède un compte » ; 2021/22 : « fait du mobile banking »), deux indicateurs distincts. Findex 2024 : usage d'Internet sur 3 mois, smartphone principal, freins liés au coût. Coefficient de variation dans `cv_pct`, et colonne `affichable_cv30` (règle du 02) | EHCVM sur les 6 domaines, libellé « Lomé » signalé (R5) ; poids calés sur deux bases différentes ; domaines MICS6 et Afrobaromètre sans équivalent exact pour Lomé et Maritime (code d'unité laissé vide) | O1-05, O1-06, O3-05 |
| EQ2 | Réception déclarée | W2 (module communautaire, 540 localités par vague) | « réseau bien capté » pour les réseaux 1, 2 et 3 (le fichier ne nomme pas l'opérateur), par région : part de la population des localités enquêtées, et part des localités | déclaratif, jamais une mesure ; confrontée au proxy 3i (Q6) | O2-06 |

---

## 6. Tables analytiques

Une table = une maille (procédure, étape 06). Toutes sont dans `data/processed/`.

| Table | Maille (lignes attendues) | Clé | Contenu | Objectifs |
| ----- | ------------------------- | --- | ------- | --------- |
| `dim_territoire` | région, unité régionale, préfecture, commune, canton (5 + 6 + 39 + 117 + 396 = 563) | `code` | libellé, niveau, codes parents, drapeau Grand Lomé, strate urbaine 50 % et 75 % (commune), superficie, drapeau des 8 codes de canton | 3, 4, 5 |
| `points_service` | un point (738 + 184 + 19 788 + 95 = 20 805) | `source` + `id_source` (+ `ligne_source`) | type (banque, IMF, assurance, DAB, mobile money, Poste), statut, `en_service`, colonnes de comptage (principal et variantes), opérateurs, codes territoriaux, lon / lat, `doublon_de`, écart de position, niveau de preuve | 3 (cartes à points), 4 |
| `terr_commune` | commune (117) | code | comptages par type, principal et variantes ; population totale, 15 ans et plus, urbaine ; superficie ; strate ; `enquete_prouvee` ; couverture 3i | 3, 4 |
| `terr_prefecture` | préfecture (39) | code | mêmes colonnes ; couverture à 20 km de 3i (niveau C ; NA pour Mô, Kpendjal, Tchamba) | 3, 4, 5 (plancher de O5-01) |
| `terr_region` | unité régionale (6) | code | mêmes colonnes ; couverture 3i publiée pour les 4 régions sans Grand Lomé seulement (NA pour Grand Lomé et Maritime hors Grand Lomé : 3i ne les distingue pas) | 3, 4 |
| `serie_nationale` | indicateur × période × opérateur × technologie × source (format long ; 3 261 lignes, 27 indicateurs) | combinaison | valeur, unité, fréquence (trimestriel, annuel, semestriel pour 2026, mensuel), convention (T4, moyenne des 4 trimestres, somme), variante (principal, sensibilité, contrôle, historique, panier distinct), rupture, niveau de preuve, base de population | 1, 2, 3 (O3-04) |
| `enquetes_region` | domaine (national, milieu, région) × vague × indicateur × source (979 lignes) | combinaison | estimation, intervalle de confiance, coefficient de variation, effectif, population de référence, code d'unité régionale quand le périmètre est identique | 1, 3, 5 |
| `benchmark` | pays ou agrégat × année × indicateur (698 lignes) | combinaison | C5, C5b, IT1 (pays de l'UEMOA), BC2 (TGPSFd, TGPSFg 2014-2024), tels que publiés | 1 (O1-01), 2 (O2-05b), 4 (O4-02) |
| `chronologie` | événement (40) | date | CH1 tel quel, avec son niveau de preuve | 1 (O1-02) |
| `_registre_anomalies`, `_controles`, `_journal_preparation` | anomalie, contrôle, étape | `id`, `code`, `etape` | section 8 | traçabilité |
| `geo/*.geojson` | régions, unités régionales, préfectures reconstituées, communes, cantons | `code` | contours WGS 84, superficie | cartes |

**Variantes préparées dans les tables territoriales** (une colonne chacune, à côté du calcul principal) :

| Colonne | Principal | Variante | Règle |
| ------- | --------- | -------- | ----- |
| points formels | statut « Utilisé », doublons probables fusionnés | + statuts inconnus ; + fusion des cas ambigus | A6, DD1 |
| Poste | non comptée | comptée | Q5 |
| 15 ans et plus | âge non déclaré au prorata | hors non déclarés | S5 |
| strate urbaine | seuil 50 % | seuil 75 % | O3-02 |

Les tables territoriales ont les numérateurs (points par type, points mobile money) et les dénominateurs (population, superficie) des indicateurs O3-01 à O4-05. Les ratios, le statut d'accès financier (O4-05) et le score (O5-01) se calculent à partir d'elles à l'étape des indicateurs. Pour O4-01, le 02 impose : 0 point formel → résultat « non défini », jamais 0.

---

## 7. Contrôles qualité

Les quatre familles de la procédure : structure (ST), géographie (GE), temps (TE), croisements entre jeux (CX). **Bloquant** : si le contrôle échoue, la table n'est pas publiée tant que l'écart n'est pas expliqué.

**Parcours des effectifs** (attendu du 03, confirmé à l'exécution) :

```
D4   738 lignes
      ├─ statut (A6) ............ 660 en service ; 78 au registre (17 hors service, 61 inconnus → variante)
      ├─ doublons (DD1) ......... 656 : 4 lignes marquées doublon_de, fusionnées dans 4 lignes principales ; 654 en variante (FUCEC / COOPEC)
      └─ rattachement (R5) ...... 100 % à un canton
4c   184 sites ................... 184 : aucun filtre ; hors de l'agrégat formel (DD7)
D5   19 788 points ............... 19 788 : ni filtre ni dédoublonnage (A8) ; 1 348 sans opérateur ; 508 proches signalés (DD3)
GD1  95 agences .................. 84 en service, en variante (Q5)
Référentiel .................... 5 régions (6 unités), 39 préfectures, 117 communes, 396 cantons, en entrée comme en sortie
```

| #   | Famille | Contrôle | Attendu | Bloquant | Constaté |
| --- | ------- | -------- | ------- | -------- | -------- |
| ST1 | Structure | effectifs lus = effectifs bruts | D4 738, 4c 184, D5 19 788, GD1 95 | oui | **738 / 184 / 19 788 / 95** |
| ST2 | Structure | entrée = sortie + lignes du registre, à chaque étape | aucun écart | oui | **20 805 en entrée, 20 805 en sortie ; aucune ligne supprimée** |
| ST3 | Structure | aucun 0 issu d'un manquant : NA avant = NA et motifs après | égalité | oui | **1 348 opérateurs restés NA ; couvertures non déterminables en NA ; tout zéro de points formels a une enquête prouvée** |
| ST4 | Structure | statuts de D4 après A6 | 660 + 17 + 61 = 738 | oui | **660 / 17 / 61** |
| ST5 | Structure | opérateurs de D5 | 12 649 + 4 773 + 1 018 + 1 348 = 19 788 | oui | **12 649 / 4 773 / 1 018 / 1 348** |
| GE1 | Géographie | nombre d'entités par maille = découpage officiel | 5 (6), 39, 117, 396 | oui (procédure) | **5 / 39 / 117 / 396 ; tables : 117 / 39 / 6** |
| GE2 | Géographie | points rattachés à tous les niveaux | 100 % | oui | **100 % ; préfecture et région déclarées toujours égales aux parents du canton** |
| GE3 | Géographie | point dans le polygone de son unité déclarée | D4 et 4c : 100 %. D5 : ≥ 99,63 % avant R3 ; 96 écarts au registre, sous trois types : 49 **hors frontière** (hors du Togo) ; 22 **débordements de contour** (dans le Togo, mais dans la zone où une commune déborde de sa préfecture, attendus résolus par R3) ; 25 **cantons rattachés à une autre commune** (dans le polygone de leur canton, signalés) | non | **D4, 4c et GD1 : 0 écart. D5 : 49 / 22 / 25, comme attendu ; après R3, plus aucun écart à la préfecture hors frontière** |
| GE4 | Géographie | emboîtement : communes = préfecture = région = national, pour les points et la population | 8 095 498 habitants | oui | **aucun écart ; 8 095 498 habitants à chaque niveau ; 656 points formels, 184 DAB, 19 788 points mobile money, 84 agences de la Poste** |
| GE5 | Géographie | superficies ; préfectures sans débordement | 56 654,6 km² | oui | **56 654,5 km² (56 654,6 avant fusion des contours)** |
| GE6 | Géographie | Grand Lomé | 13 communes, 2 188 376 habitants (27,0 %) | oui | **13 communes, 2 188 376 habitants (27,0 %)** |
| GE7 | Géographie | RG2 et RG3 égaux à D6 aux niveaux préfecture et commune | totaux égaux | oui | **tous les totaux présents dans D6 (Danyi 1 + 2 sommées)** |
| TE1 | Temps | millésimes des croisements : points 2021/2022, population 2022 | écart ≤ 1 an | oui (A10) | **vérifié** |
| TE2 | Temps | AR1 : trimestres du T1 2018 au T2 2026, une seule valeur chacun | 34 trimestres, aucun manquant | oui | **34 trimestres sur 34 pour 6 séries clés ; mobile money depuis le T2 2020** |
| TE3 | Temps | ruptures signalées dans `serie_nationale`, jamais corrigées | T1 2020, T2 2025, T2 2026, 2b 2019-2020, IN3 2020 | non | **toutes signalées ; T1 2020 : -6,6 % ; IN3 : +15,2 % ; ajout : comptes mobile money au T1 2021** |
| TE4 | Temps | D5 libellé « stock 2021/2022 », jamais « état actuel » | libellé présent | non | **vérifié** |
| CX1 | Croisement | vues par opérateur jamais additionnées en total ; total = lieux | 19 788 | oui (procédure) | **19 788 lieux ; 31 089 points-opérateurs hors Nsp, jamais présentés en total** |
| CX2 | Croisement | aucune couverture nationale à 0 % ni à 100 % (3i) ; Mô, Kpendjal, Tchamba en NA | vérifié | oui (procédure) | **88,37 % ; NA : Mô, Tchamba, Kpendjal et leurs 7 communes, plus Sotouboua 2 et Kéran 3 (V4)** |
| CX3 | Croisement | raccord D2 / AR1 | écart nul en 2018, 0,03 % en 2017 | oui (P4) | **3G de Togocel égale en 2017 et 2018 ; total data mobile : +0,030 % (2017), 0 (2018)** |
| CX4 | Croisement | D5 face à l'ARCEP au T4 2021 : points-opérateurs (un point « Moov, Togocom » = 2) | 31 089 si les 1 348 points sans opérateur sont exclus ; 32 437 s'ils comptent pour un (le « ≈ 32 400 » du 03) ; 33 785 s'ils comptent pour deux. ARCEP : 33 924, soit un écart de 8,4 %, 4,4 % ou 0,4 % | non | **31 089 / 32 437 / 33 785 ; écarts 8,4 / 4,4 / 0,4 %** |
| CX5 | Croisement | recomptages face aux indicateurs pré-calculés de geodata (4j, 5c) | écarts expliqués (4j compte toutes les lignes) | non (A18) | **banques 247, microfinances 412, assurances 69, DAB 184, Poste 95 : identiques** |
| CX6 | Croisement | CA de 2b face à la somme des 4 trimestres de AR1 | +2,8 % (2021), +3,7 % (2022), documentés | non (A4) | **+2,8 % / +3,7 %** ; en 2021, l'écart (6,2 Md FCFA) tient surtout au CA de GVA, exclu par l'ARCEP (5,7 Md FCFA) |
| CX7 | Croisement | une seule base de population par indicateur | colonne `base_population` unique | oui | **vérifié** |

---

## 8. Registre des anomalies et journal de préparation

**Registre** (`data/processed/_registre_anomalies.csv`) : une ligne par anomalie ou exclusion.

| Colonne | Contenu |
| ------- | ------- |
| `id` | identifiant de l'anomalie |
| `jeu`, `id_source` | fichier et ligne concernés |
| `variable` | variable en cause |
| `type` | statut exclu, doublon (fusionné ou variante), hors frontière, débordement de contour, canton rattaché à une autre commune, code corrigé, manquant, rupture, révision |
| `decision` | gardé, exclu, fusionné (avec la ligne principale), corrigé, signalé |
| `regle` | A6, DD1, A21… |
| `effet` | effet sur l'effectif ou la valeur |
| `etape` | script qui l'a traité |

Entrées connues avant l'exécution, décrites dans le 03 : 78 statuts de D4 hors calcul principal ; 4 lignes fusionnées et 2 paires ambiguës (DD1), plus les 12 paires gardées avec leur décision ; 49 points hors frontière, 22 débordements de contour et 25 points de cantons rattachés à une autre commune (D5) ; 8 codes de canton ; 3 préfectures sans couverture déterminable (3i) ; 15 couples absents de D2 ; valeurs 2019 de D2 et 2b écartées ; révisions et ruptures de AR1.

Constaté : **2 151 lignes** (1 394 manquants signalés, 89 statuts exclus de D4 et GD1, 96 écarts de position, 18 décisions de doublons, 8 codes de canton, 12 couvertures non déterminables, 533 lignes de l'ARCEP : doubles lectures, révisions, totaux incohérents écartés, valeurs corrigées).

**Journal** (26/09/2026 ; détail dans `_journal_preparation.csv` et `_controles.csv`) :

| Étape | Entrée (n) | Transformation | Sortie (n) | Contrôles | Résultat |
| ----- | ---------- | -------------- | ---------- | --------- | -------- |
| 1 référentiel | 5 + 39 + 117 + 396 contours | noms geodata, 8 codes de canton, préfectures reconstituées, superficies | 563 unités | 13 | aucun écart ; 8 lignes au registre |
| 2 population | RG2 (8 883 lignes), RG3 (22 113) | agrégation, jointure sans correction, prorata des âges, strates | 168 unités peuplées | 15 | aucun écart |
| 3 points | 738 + 184 + 19 788 + 95 | nettoyage, A6, DD1, rattachement par les noms, contrôle par la position | 20 805 points, dont 656 formels en service | 17 | 1 écart signalé (DD3) ; 1 598 lignes au registre |
| 4 territoires | 20 805 points, 168 unités | agrégation, zéros vérifiés, couverture 3i, contrôle geodata | 117 + 39 + 6 lignes ; `dim_territoire` (563) | 18 | aucun écart ; 12 lignes au registre |
| 5 ARCEP | 34 PDF, 13 140 lignes lues | reconnaissance des séries, unités, totaux incohérents écartés, DD5 | 1 755 valeurs trimestrielles | 21 | aucun écart ; 533 lignes au registre |
| 6 séries | 11 sources | format long, raccords, conventions, paniers IT1 | 3 261 lignes, 27 indicateurs | 15 | 1 écart signalé (SN4 : téléphonie par opérateur) |
| 7 enquêtes | EHCVM (2 vagues, modules individu, 6 et communautaire), MICS6, Afrobaromètre (6 vagues), Findex | estimations pondérées, IC 95 %, CV | 979 lignes | 6 | aucun écart |
| 8 repères | C5, C5b, IT1, BC2, CH1 | tels que publiés | 698 + 40 lignes | 5 | aucun écart |
| 9 contrôles | 9 tables | contrôles transversaux, consolidation | registre, contrôles, journal | 28 | aucun écart ; aucun bloquant en échec sur les étapes 1 à 8 |

---

## 9. Points de validation

« Objectif concerné » renvoie aux 5 objectifs de `_PROJECT.txt` et aux indicateurs du 02. « Impact » dit ce que l'objectif attend (01) et ce que la décision y change.

| #  | Question | Objectif concerné | Impact sur l'attendu de l'objectif | Décision |
| -- | -------- | ----------------- | ---------------------------------- | -------- |
| V1 | Doublons de D4 (DD1) | **3** (cartographier les établissements financiers) et **4** (rapporter les points à la population) : O3-01, O3-02, O4-01, O4-03, O4-05 | Les cartes et les ratios comptent 656 établissements au lieu de 660 (-0,6 %). Seules 4 communes changent, d'un ou deux points : Golfe 1, 3 et 5, qui gardent de 31 à 55 établissements, et Bas-Mono 1 en variante (3 → 2). Aucun territoire ne tombe à zéro point formel, donc aucun ne devient « mobile money uniquement ». La part du Grand Lomé dans les points formels passe de 40,3 % à 39,9 % : le test de concentration de O3-02 (plus de 50 %) donne la même réponse | **Validé** : présélection (même catégorie, moins de 30 m) et contrôle visuel des 18 paires ; pas de seuil de similarité (section 3). 4 doublons fusionnés dans le calcul principal (660 → 656) ; 2 paires FUCEC / COOPEC gardées, signalées, fusionnées en variante (654) |
| V2 | GD3 (électricité, villages par territoire), reporté « à la préparation » par S8 | **5** (recommandations ciblées) : levier « énergie » cité par le 01 | L'objectif 5 attend des recommandations tirées des écarts observés ; le 01 cite l'énergie parmi les leviers possibles. Sans GD3, aucun écart d'électricité n'est mesuré dans le découpage actuel : une recommandation sur l'énergie ne s'appuierait que sur le contexte (IN4 par préfecture, ancien découpage ; BM1 à BM3 au niveau national). Objectifs 1 à 4 : aucun effet | **Validé** : non téléchargé, aucun indicateur du 02 ne l'utilise. Il ne le serait que si l'objectif 5 met en évidence un frein énergétique, comme écart déclaré au 02 |
| V3 | Outil du tableau de bord | **Livrable** de `_PROJECT.txt` (tableau de bord interactif, .zip) : tous les objectifs | Aucun effet sur le contenu : les tables sont les mêmes quel que soit l'outil. Python demande seulement des contours en GeoJSON, déjà produits | **Validé** : Python probablement, pour aller plus vite ; les contours restent en GeoJSON |
| V4 | 3i donne aussi 0 % à Sotouboua 2 et à Kéran 3, hors des 3 préfectures de A13, alors que D5 y compte 107 et 10 points mobile money | **2** (couverture réseau, « lorsque disponible » : O2-06), **4** (O4-06, statut × couverture) et **5** (priorisation : 3e dimension de O5-01) | Deux communes (95 000 habitants) apparaissent « non déterminable » sur la carte communale de la couverture, au lieu de 0 %. Elles ne sont donc pas classées parmi les moins couvertes, à tort. Le score de priorité (O5-01) et O4-06 se calculent à la préfecture : Sotouboua (27,0 %) et Kéran (21,4 %) ne changent pas | **Validé (26/09/2026)** : critère de A13 étendu à Sotouboua 2 et Kéran 3 ; tracé au registre comme « A13 (critère étendu, à confirmer) », distinct de A13 strict (qui visait 3 préfectures). Couverture « non déterminable » : 3 préfectures et 9 communes (les 7 communes de Mô, Tchamba et Kpendjal, plus Sotouboua 2 et Kéran 3), soit 436 568 habitants au niveau communal, contre 341 398 avant l'extension |
| V5 | L'ARCEP ne publie les abonnés à la téléphonie mobile par opérateur que dans des graphiques (parts arrondies), sur les 34 numéros | **2** (parts de marché des opérateurs, chiffre d'affaires, abonnés) : O2-01, O2-02 ; O2-05a (ARPU, optionnel pour le 01) | L'objectif 2 attend les parts de marché des opérateurs. Elles restent mesurables jusqu'au T2 2026 en abonnés data mobile et en chiffre d'affaires, dans les tableaux de l'ARCEP. Seules les parts en abonnés à la téléphonie s'arrêtent en 2019 (D3). O2-02 (part du chiffre d'affaires face à la part des abonnés) se fait avec les abonnés data. L'ARPU n'est calculable qu'au niveau national, sans comparaison entre opérateurs | **Validé (26/09/2026)** : O2-05a au niveau national seulement (niveau B). Parts de marché en abonnés à la téléphonie par opérateur : D3, 2013-2019 (parts publiées par l'INSEED, niveau C) ; parts en abonnés data et en CA par opérateur : ARCEP, 2018-2026 (niveau A). Graphiques non lus : ce serait une estimation visuelle, et le 02 écarte toute estimation qui remplace une donnée absente (règle écrite pour O1-04 et O2-04). **Affichage** : « Parts en abonnés à la téléphonie : 2013-2019 (D3). Parts en abonnés data et en chiffre d'affaires : 2018-2026 (ARCEP). » |
| V6 | Le panier « 1 Go » de l'UIT n'existe que de 2023 à 2025 ; la série 2013-2025 du 03 enchaînait quatre paniers différents | **2** (accessibilité tarifaire : O2-05b, optionnel) et **5** (levier « tarification » : O5-02, O5-03) | Le test du seuil de 2 % ne porte que sur 3 années : 5,85 % (2023), 5,45 % (2024), 5,30 % (2025). La conclusion « service non abordable » tient, mais sans tendance longue sur un même panier. L'évolution depuis 2013 se lit panier par panier (2 Go : 11,37 % en 2021, 5,68 % en 2025). La recommandation tarifaire de l'objectif 5 reste appuyée sur un écart chiffré (5,30 % contre 2 %) | **Validé (26/09/2026)** : O2-05b = « 1 Go, data seule », 2023-2025 (5,85 %, 5,45 %, 5,30 %), seul soumis au seuil de 2 %. Paniers distincts, jamais enchaînés : 1 Go postpayé sur ordinateur (2013-2017 : 73,6 %, puis 21,3 % à 16,9 %), 1,5 Go (2018-2020 : 16,6 % à 15,1 %), 2 Go (2021-2025 : 11,4 % à 5,7 %), 5 Go (2022-2025 : 13,6 % à 9,5 %). **Affichage** : un tableau par panier, jamais une courbe unique ; la recommandation tarifaire s'appuie sur l'écart 5,30 % / 2 %, pas sur une tendance 2013-2025 |
| V7 | L'EHCVM mesure un **accès** déclaré à Internet, pas un usage. **Correction du 26/09/2026** : son module 6 porte bien sur le mobile banking (15 ans et plus : « possède un compte » en 2018/19, « fait du mobile banking » en 2021/22) ; le 04 et le 03 affirmaient à tort le contraire | **1** (usage d'Internet : O1-05 par territoire, optionnel ; O1-06, freins), **3 et 4** (rôle du mobile money : O3-05, optionnel) et **5** (volet Internet par région) | Objectif 1 : le taux national (O1-01) ne change pas (D1) ; Findex 2024 donne en plus un point mesuré selon la même définition (43,7 % des 15 ans et plus, 3 derniers mois). Par région, l'EHCVM donne un accès déclaré précis (2 vagues, IC de ± 2 à 5 points), mais pas un usage ; l'usage par région vient de l'Afrobaromètre 2024 (de 43 % dans la Centrale à 88 % à Lomé, IC de ± 4 à 10 points) et de la MICS6 2017 (15-49 ans). Mobile money : grâce au module 6, la demande est mesurée par région sur deux vagues, avec la précision de l'EHCVM (2021/22 : de 19,9 % dans la Centrale à 57,4 % dans le Grand Lomé ; CV de 3 à 10 %). Sous la région, le rôle du mobile money se lit par l'offre (points de D5), jamais par l'usage | **Validé (26/09/2026)**. O1-05 et O1-06 : « Accès déclaré à Internet (EHCVM) », 23,7 % (2018/19) puis 35,3 % (2021/22), 15 ans et plus ; « Usage d'Internet, toute fréquence (Afrobaromètre) » ; MICS6 2017 ; Findex 2024 au national. Freins : alphabétisation et portable (EHCVM), compétences TIC (MICS6), smartphone principal (Findex 2024 : 45,1 %, national). **O3-05 (validé le 26/09/2026 après correction)** : source principale EHCVM 2021/22, « fait du mobile banking » (15 ans et plus ; national 36,9 % ; par région, de 19,9 % à 57,4 %). EHCVM 2018/19 (« possède un compte ») affichée à part, jamais en tendance avec 2021/22 : les questions diffèrent. Afrobaromètre 2022 (compte mobile money personnel, 77,9 %) en complément, jamais mêlé. **Affichage** : un libellé par source, jamais sur une même courbe ; O3-05 affiché seulement si CV < 30 % (colonne `affichable_cv30`) |

Rappel, sans effet sur la préparation : la période de référence de la classe « ralentissement » de O1-02 est à fixer avant son calcul (03, section 10).
