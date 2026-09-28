# Recherche des données manquantes — Objectif 1

*Journal de recherche. Sections 0 à 5 et 9 : recherches ; sections 6, 8, 10, 12 et 13 : décisions ; section 14 : relecture complète ; section 15 : mise en œuvre de S1 à S10 ; section 16 : restructuration du 03 ; section 17 : décisions sur les parties A et C du 03 et sur GD2, puis impact de chacune sur la phase 4, A2, A5, seuil de O3-02 et O2-05. Règle de O3-02 du 02 (Grand Lomé à 27,0 % de la population, plafond à 25 %) tranchée aussi : aucune décision en attente. **État au 26/09/2026** : toutes les propositions soumises (D-1 à D-18, P1 à P8, Q1 à Q12, V1 à V3, R1 à R6) sont validées et reportées dans le 03 et dans `_INVENTORY_datasets.txt`. La relecture complète a relevé dix points restés sans décision (S1 à S10, section 14), **validés le 26/09/2026** avec deux nuances (S8, S9) et mis en œuvre (section 15) : le repère Afrique subsaharienne de O1-01 est téléchargé (C5b). Les jeux retenus sont dans `data/raw/_extradatas/` (sections 7, 11 et 12).*

**Objet :** chercher, organisation par organisation, les données qui manquent à l'objectif 1 du 01 (« Retracer l'évolution de l'usage d'Internet au Togo et repérer les périodes d'accélération ou de stagnation ») d'après le 03.

**Méthode :** catalogue complet de chaque organisation par l'API du portail (`https://opendata.gouv.tg/api/1/datasets/?organization=<id>`), filtrage par mots-clés sur les titres puis sur les descriptions, puis lecture des fichiers candidats dans un dossier temporaire pour vérifier les années réellement renseignées. Les périodes annoncées par le catalogue (souvent « 1960-2023 ») ne sont pas fiables : seules les années lues dans les fichiers sont reportées ici.

**Manques de l'objectif 1 (d'après le 03) :**

| Réf.            | Manque                                                                   | Indicateur du 02 |
| --------------- | ------------------------------------------------------------------------ | ---------------- |
| B6              | Chronologie datée des événements (3G/4G, opérateurs, tarifs, COVID)      | O1-02            |
| B5, B1, A16     | Population annuelle ; population de 15 ans et plus                       | O1-03            |
| B7              | Abonnements par technologie après 2019                                   | O1-04            |
| —               | Usage d'Internet par territoire                                          | O1-05            |
| B10             | Alphabétisation des 15 ans et plus, compétences TIC, smartphones         | O1-06            |
| B11             | Benchmark Afrique subsaharienne                                          | O1-01 (repère)   |

---

## 0. Constats sur la question de l'objectif 1 (25/09/2026)

La question est traitable au niveau national avec D1 / 1b : la série est retraçable et ses changements de rythme sont calculables. Elle ne l'est ni par territoire, ni avec une explication par les événements. Trois points ne figurent pas dans le 03 :

1. **Avec les seuils du 02, aucune année n'est une « stagnation ».** Le seuil de stagnation est |g| < 2 % (`02_decision_matrix_seuils.csv`). La croissance annuelle la plus faible de 1b est +4,5 % (2021). Les ralentissements de 2017 (+9,3 %), 2021 (+4,5 %) et 2023-2024 (+5,5 %, +5,1 %) n'entrent dans aucune classe. Les accélérations dépendent de la période de calcul (moyenne + 1 écart-type) : 2016, 2019 et 2020 sur 2001-2024 ; 2016 et 2020 sur 2011-2024.
2. **La lecture de 2021 dépend de la version retenue (11.A1).** API : +4,5 % (30,34 après 29,02), un ralentissement net. CSV : +12,0 % (32,51 après 29,02), un rythme ordinaire.
3. **Les valeurs de 2000 à 2014 ressemblent à des estimations.** Une seule décimale et des pas réguliers : +0,2 point par an de 2006 à 2009, +0,5 point de 2011 à 2013. Le champ `obs_status` est vide partout : rien ne permet de distinguer mesures et estimations.
   **Confirmé et élargi le 26/09/2026 (section 5)** : les notes de l'API de la Banque mondiale (`footnote=y`) qualifient d'« ITU estimate » **toutes les années 2000-2016 et 2018-2023**. Seule 2017 (12,36 %) est attribuée à l'INSEED ; 2024 n'a pas de note. Les accélérations et ralentissements de D1 / 1b décrivent donc surtout le modèle d'estimation de l'UIT, pas des mesures.

**Décisions à prendre :** version API ou CSV (A1) ; seuil de stagnation du 02 (tel quel, ou ajout d'une classe « ralentissement ») ; chronologie (source extérieure, ou ruptures non annotées).

---

## 1. Organisation « Banque mondiale » (25/09/2026)

Page : https://opendata.gouv.tg/fr/organizations/banque-mondiale/ — **733 jeux** parcourus.

**Résultat : aucun jeu ne comble un manque de l'objectif 1 tel que le 02 le définit.**

| Réf.   | Résultat                                                                                                          |
| ------ | ----------------------------------------------------------------------------------------------------------------- |
| B6     | ❌ Seul candidat, « Investissements PPP dans les TIC » : fichier vide                                             |
| B5, B1 | ❌ Aucune série de population (seulement la croissance urbaine et rurale en %)                                    |
| B7     | ❌ Aucune série 3G / 4G / fibre ; haut débit fixe déjà en 2c / 2d                                                 |
| O1-05  | ❌ Tout est national                                                                                               |
| B10    | ❌ Ni alphabétisation des adultes (SE.ADT.LITR.ZS absent), ni compétences TIC, ni smartphones                    |
| B11    | ❌ Tous les jeux portent sur le Togo seul                                                                          |

**Séries de contexte trouvées (hors 02)**

| #    | Jeu                                                                                                                                                                                                                           | Années renseignées           | Dernière valeur | Usage possible                                         |
| ---- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- | --------------- | ------------------------------------------------------ |
| BM1  | [Accès à l'électricité (% population totale)](https://opendata.gouv.tg/fr/datasets/donnees-ouvertes-sur-acces-a-lelectricite-population-totale-au-togo/) (EG.ELC.ACCS.ZS)                                                     | 1998-2022                    | 57,2 % (2022)   | Frein matériel à l'usage, national                     |
| BM2  | [Accès à l'électricité, milieu urbain](https://opendata.gouv.tg/fr/datasets/donnees-ouvertes-sur-acces-a-lelectricite-en-milieu-urbain-population-urbaine-au-togo/)                                                           | 1998-2022                    | 96,5 % (2022)   | Écart ville / campagne, national                       |
| BM3  | [Accès à l'électricité, milieu rural](https://opendata.gouv.tg/fr/datasets/donnees-ouvertes-sur-acces-a-lelectricite-en-milieu-rural-population-rurale-au-togo/)                                                              | 1998-2022                    | 25,0 % (2022)   | Idem                                                   |
| BM4  | [Inscriptions scolaires, secondaire (% brut)](https://opendata.gouv.tg/fr/datasets/donnees-ouvertes-sur-inscriptions-scolaires-secondaire-brut/)                                                                              | 38 années entre 1971 et 2023 | 65,3 % (2023)   | Proxy de compétences ; pas l'alphabétisation adulte    |
| BM5  | [Inscriptions scolaires, supérieur (% brut)](https://opendata.gouv.tg/fr/datasets/donnees-ouvertes-sur-les-inscriptions-scolaires-enseignement-superieur-brut-au-togo/)                                                       | 38 années entre 1971 et 2020 | 15,1 % (2020)   | Idem                                                   |
| BM6  | [Élèves sous le niveau minimum en lecture, fin du primaire](https://opendata.gouv.tg/fr/datasets/donnees-ouvertes-sur-les-eleves-en-dessous-du-niveau-minimum-de-competence-en-lecture-a-la-fin-du-primaire-seuil-gaml-bas-au-togo/) | 2014, 2019          | 80,6 % (2019)   | Compétences, 2 points seulement                        |
| BM7  | [Croissance du PIB par habitant (% annuel)](https://opendata.gouv.tg/fr/datasets/donnees-ouvertes-croissance-du-pib-par-habitant-annuel-au-togo-1/)                                                                           | 1961-2023                    | +4,0 % (2023)   | Lecture des ruptures (2020 : -0,4 % ; usage +8,3 pts)  |

**Écartés :** Investissements PPP dans les TIC (vide) ; importations de biens TIC et exportations de services TIC (déjà dans 3g, identiques) ; consommation d'électricité par habitant (s'arrête en 2014) ; secondaire % net (4 années) ; croissance du RNB par habitant (redondant avec BM7) ; variantes par sexe et indices de parité des inscriptions.

**Proposition :** garder BM1 à BM3 et BM7 comme contexte ; écarter BM4 à BM6 (scolarisation, pas compétences numériques des adultes).

---

## 2. Organisation « INSEED » (25/09/2026)

Page : https://opendata.gouv.tg/fr/organizations/institut-national-de-la-statistique-et-des-etudes-economiques-et-demographiques/ — **479 jeux** parcourus. D2, D3 et 2b en viennent déjà.

**Résultat : deux manques sont comblés en partie (population annuelle, datation des baisses de prix).**

| Réf.   | Résultat                                                                                                  |
| ------ | --------------------------------------------------------------------------------------------------------- |
| B5     | ✅ Population annuelle 2011-2031 (IN1)                                                                     |
| B1     | ⚠️ 15 ans et plus au niveau national seulement (IN1) ; rien par territoire                                  |
| B6     | ⚠️ Les baisses de tarifs sont datées au mois près (IN2, IN3) ; pas de chronologie d'événements proprement dite |
| B7     | ❌ Rien au-delà de D2 et 2b                                                                                 |
| O1-05  | ❌                                                                                                          |
| B10    | ❌                                                                                                          |

**Jeux retenus pour validation**

| #   | Jeu                                                                                                                                                                                                  | Contenu vérifié                                                                                                                              | Apport                                                                                                                                                                                                                                                  | Qualité                                                                                                    |
| --- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| IN1 | [Projections démographiques 2011-2031](https://opendata.gouv.tg/fr/datasets/donnees-ouvertes-sur-les-projections-demographiques-du-togo-de-2011-a-2031/)                                             | 18 tranches d'âge x 3 sexes x 21 ans (1 134 lignes), national                                                                              | Dénominateur annuel de O1-03. 2022 : 8 068 000, soit -0,3 % par rapport au RGPH (8 095 498) ; la Banque mondiale est à +12 %. 15 ans et plus : 5 032 000 en 2022 (62,4 %)                                                                                  | C (projection). Tranches = total à 2 000 près                                                              |
| IN2 | [IHPC-Poste](https://opendata.gouv.tg/fr/datasets/donnees-ouvertes-ihpc-poste-au-togo/)                                                                                                             | 126 postes, mensuel, 2010-01 à 2017-04 ; dont « Frais de connexion internet et assimilés », « Communication téléphonique », « Matériel de téléphonie et de télécopie » | Connexion Internet : indice 100 → 63,6 (-36 %), baisses en 2010-07, 2010-12, 2013-01, 2014-02, 2014-10, 2017-01. Matériel de téléphonie : -28 % entre janvier 2013 et janvier 2014. Appels : quasi stables (100 → 101)                                    | C. 86 des 88 mois en double, sous deux formats de date (`2010M1` et `01/01/2010`), valeurs identiques     |
| IN3 | [Indice des fonctions de consommation de l'INHPC](https://opendata.gouv.tg/fr/datasets/donnee-ouvertes-sur-levolution-de-lindice-des-fonctions-de-consommation-de-linhpc-au-togo/) (2010-01 à 2022-12) et [Indices des prix](https://opendata.gouv.tg/fr/datasets/donnees-ouvertes-sur-l-indices-des-prix-au-togo/) (2014-01 à 2024-04) | Fonction « Communication » (téléphone, Internet, matériel, poste), mensuelle. Les deux fichiers sont identiques sur les 108 mois communs | Prolonge IN2 jusqu'en 2024, en agrégé. Décembre : 96,9 (2016), 92,7 (2017), 88,4 (2019), 101,8 (2020)                                                                                                                                                 | C. **+15 % entre décembre 2019 et décembre 2020** : hausse réelle ou changement de méthode, à vérifier |
| IN4 | [Taux d'accès à l'électricité par préfecture](https://opendata.gouv.tg/fr/datasets/donnees-ouvertes-sur-le-taux-dacces-a-lelectricite-par-prefecture-au-togo/) (hors objectif 1)                     | Taux d'accès et abonnés basse tension, 2018-2021, 40 unités                                                                                  | Seule série territoriale trouvée : Kpendjal 1,9 %, Lomé 98,6 % (2021) ; national 57,8 %. Pour les objectifs 4 et 5                                                                                                                                         | Ancien découpage, préfectures regroupées (« Ogou + Anié », « Kpendjal + Kpendjal Ouest »…)                 |

**Ce que IN2 et IN3 permettent, avec les données déjà en main :** trois des quatre types d'événements cités par le 01 deviennent datables sans source extérieure :
- **Technologies** (D2) : 3G de Moov en 2016, FTTH en 2017, 4G de Togocom en 2018.
- **Arrivée d'opérateurs** (2b) : TEOLIS et GVA sur l'Internet fixe en 2018.
- **Tarifs** : IN2, IN3.

La crise sanitaire n'est dans aucune donnée. Ces dates permettent de placer les ruptures sur une même frise, pas d'établir une cause.

**Autres jeux notés (hors objectif 1) :** [population résidente 2022 par milieu](https://opendata.gouv.tg/fr/datasets/donnees-ouvertes-sur-leffet-de-la-population-residente-en-2022-au-togo/) (national : 3 473 792 urbains, soit 42,9 % ; ne règle pas B3, qui demande le milieu par territoire) ; [taux de pauvreté et revenus](https://opendata.gouv.tg/fr/datasets/donnees-ouvertes-sur-le-taux-de-pauvrete-et-revenus-au-togo/) (2006, 2011, 2015, 2017-2019 ; contexte de O2-05).

**Écartés :**
- Autres indices de prix : IHPC FMI base 2014 (redondant avec IN3), inflation mensuelle par fonction, indice national global.
- Indicateurs de l'EDS : santé et éducation, rien sur les TIC.
- Indicateurs mensuels supplémentaires : aucune série télécom.
- Effectif total de population par année : doublon de IN1.
- « Projection 2011-2021 » et « Population et statistiques de l'état civil » : même contenu, couvert par IN1.
- Pyramides 2010 : nationales malgré le titre.
- Population 2010 par subdivision : ancien recensement.
- Taux brut de scolarisation au lycée par région : pas l'alphabétisation des adultes.
- Apprenants des centres d'alphabétisation : des effectifs, pas un taux.
- Radios, télévisions et HAAC : hors sujet.

**Correction à prévoir dans le 03 :** la section 6 (« Aucun complément ne comble ces manques ») et les lignes B1 et B5 de la section 11 sont contredites par IN1, au niveau national. Réserve pour O1-03 : D1 repose sur la population de la Banque mondiale et ne se recalcule pas avec celle de l'INSEED sans le nombre d'utilisateurs. Le choix A16 reste ouvert.

**Proposition :** télécharger IN1, IN2, IN3 (un seul des deux fichiers suffit pour 2014-2022) et IN4.

---

## 3. Organisation « MESPTN » (25/09/2026)

Page : https://opendata.gouv.tg/fr/organizations/ministere-de-lefficacite-du-service-public-et-de-la-transformation-numerique/ — **25 jeux** et 1 service de données (l'API du portail elle-même) parcourus.

**Résultat : rien de nouveau pour l'objectif 1.**

| Jeux                                                                                                           | Constat                                                                                  |
| -------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Pénétration Internet (2e)                                                                                      | Déjà profilé : ni date ni lieu, échantillon équilibré (inchangé depuis le 26/12/2024)    |
| Agents mobile money (D5) et son dictionnaire (5b)                                                              | Déjà en main                                                                             |
| 17 fiches : tours télécoms (x 3), bâtiments des tours (x 3), réseau enterré et aérien (x 9), datacenters énergies et bâtiments, agents Moov et Togocom | Métadonnées seules, données privées (mises à jour le 28/05/2026, toujours sans données) |
| Datacenters, établissements                                                                                    | 3 sites avec année de création : E-Gouv NOC (2016), Cloud & Racks (2021), Lomé Data Center (2022). Apport mineur à la chronologie |
| Susceptibilité et risque d'inondation ; trait de côte (publiés le 10/07/2026)                                  | Hors sujet                                                                               |

---

## 4. Site de l'ARCEP : https://arcep.tg (25/09/2026)

**Hors du périmètre actuel du 03** (« Aucune autre source n'a été consultée ») : l'utiliser suppose de l'élargir (décision D-6).

Le site n'est pas un portail de données. Il publie des PDF (observatoires, rapports, décisions, études), une page HTML de tarifs et un registre au format xlsx.

**Résultat : c'est la source qui manquait pour O1-04 après 2019, et elle apporte une bonne partie de la chronologie.**

| Réf.   | Résultat                                                                                                                                         |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| B7     | ✅ Abonnés data par technologie (2G, 3G, 4G, 5G) et par opérateur, **trimestriels, du T4 2017 au T2 2026** (AR1)                                  |
| B6     | ⚠️ Chronologie en partie reconstituable : licences datées (AR3), lancements (AR1, AR2), décisions tarifaires datées (AR4). Voir le tableau ci-dessous |
| B5     | Confirme IN1 : l'ARCEP calcule ses taux avec les projections de l'INSEED (8 811 993 habitants au T2 2026 ; IN1 : 8 812 000 en 2026)            |
| O1-05  | ❌ Observatoires nationaux. Les campagnes de qualité de service sont localisées (84 localités, 36 préfectures) mais mesurent la qualité, pas l'usage. *84 localités : campagnes de 2025 ; celle de 2024 en compte 94 (15.3)* |
| O1-06  | ❌ Les enquêtes de satisfaction (2023, 2024) mesurent la perception des clients, pas l'équipement ni les compétences                             |
| B11    | Non vérifié : l'« analyse comparative des indicateurs clés » (avril 2024) cite la zone UEMOA                                                    |

**Documents**

| #   | Document                                                                                                                                                  | Contenu vérifié                                                                                                                                                                                                                                                                                                  | Apport                                                                                                                         |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| AR1 | [Observatoire des marchés, trimestriel](https://arcep.tg/observatoire-2/activites/evolutions-du-marche-des-communications-electroniques/) : 34 PDF          | 2018 T1-T4 (« Évolution du secteur »), 2019 T1-2021 T4 (« Tableau de bord »), 2022 T1-2026 T2 (« Obs-marchés ») : aucun trimestre manquant. Chaque numéro couvre 5 trimestres. Abonnés data 2G / 3G / 4G / 5G par opérateur ; Internet fixe et FTTH par opérateur ; trafic data (depuis le T4 2017) ; data par jour et par abonné (vue en 2025-2026) ; CA et investissement **par opérateur** ; mobile money | O1-04 après 2019 ; intensité d'usage (trafic, Mo par abonné) ; objectif 2 : O2-02 (CA par opérateur), O2-04, O3-04           |
| AR2 | [Rapports d'activité](https://arcep.tg/observatoire-2/activites/rapports-dactivite/) : 20 PDF                                                              | Exercices 2007-2017 et 2020-2025 ; **2018 et 2019 absents**. RA 2017 : « commercialisation de la 3G depuis août 2016 » (Moov), « licences 4G » attendues en 2018. RA 2025 : cellules 2G / 3G / 4G, campagnes de qualité de service, 6 808 localités éligibles au titre des zones blanches | Chronologie (B6) ; contexte de couverture. Aucune couverture de la population par technologie trouvée (seulement une obligation de 95 % du territoire) |
| AR3 | [Registre des communications électroniques](https://arcep.tg/professionnels/registre-des-communications-electroniques-et-des-postes/) : xlsx, 6 versions du 30/07/2024 au 26/06/2026 | Feuille « Licences » : date de l'arrêté de chaque opérateur                                                                                                                                                                                                                                                      | Chronologie (B6)                                                                                                              |
| AR4 | [Décisions réglementaires](https://arcep.tg/regulation/reglementation/communication-electronique/) : 82 documents                                           | Décisions tarifaires, qualité de service, fréquences, avec numéro et date                                                                                                                                                                                                                                          | Chronologie des réformes tarifaires (B6)                                                                                       |
| AR5 | [Relevé des tarifs](https://arcep.tg/observatoire-2/tarifs-2/) : page HTML                                                                                   | Offres mobiles (mixtes, data, voix) et Internet fixe des opérateurs, septembre 2023                                                                                                                                                                                                                               | Hors objectif 1 : coût de 1 Go (O2-05), à une date                                                                             |
| AR6 | [Études et enquêtes](https://arcep.tg/observatoire-2/activites/etudes-enquetes/) : 10 PDF                                                                   | Campagnes QoS (2e semestre 2023, 2024), QoE data et FTTH (2025, 2026), analyse des tarifs (avril 2023), analyse comparative (avril 2024), satisfaction client (2023, 2024)                                                                                                                                       | Hors objectif 1 : O2-09, O2-05                                                                                                 |

**Chronologie reconstituable à partir des données (B6)**

| Date                  | Événement                                                                          | Source                  |
| --------------------- | ---------------------------------------------------------------------------------- | ----------------------- |
| 12/10/2001            | Licence de CAFE Informatique                                                        | AR3                     |
| 02/05/2009            | Arrêté de licence de Togo Telecom                                                   | AR3                     |
| 2013 au plus tard     | 3G de Togocel (130 019 clients en 2013)                                            | D2                      |
| Août 2016             | Lancement commercial de la 3G de Moov                                               | AR2 (RA 2017)           |
| 2016                  | Datacenter E-Gouv NOC                                                               | MESPTN                  |
| 07/06/2017            | Licences de GVA et de TEOLIS                                                        | AR3                     |
| 2017                  | Premiers abonnés FTTH (92)                                                          | D2                      |
| 12/06/2018            | Licences de Togocel et de Moov (les « licences 4G » annoncées par le RA 2017)      | AR3, AR2                |
| T3 2018               | Premiers abonnés 4G de Togocel (48 799)                                             | AR1                     |
| 2018                  | Premiers abonnés de GVA et de TEOLIS                                                | 2b                      |
| 2010-2017 (mensuel)   | Baisses de l'indice « Frais de connexion internet » : 2010-07, 2010-12, 2013-01, 2014-02, 2014-10, 2017-01 | IN2 |
| 23/11/2020            | Décision fixant les plafonds des tarifs USSD                                        | AR4                     |
| Janvier 2021          | Décision 011 : principes tarifaires des communications électroniques (date de mise en ligne) | AR4           |
| Juin 2021             | Centre de supervision des réseaux mobiles de l'ARCEP                                | Page « Mesures QoS »    |
| 2021, 2022            | Datacenters Cloud & Racks, puis Lomé Data Center                                    | MESPTN                  |
| 12/02/2024            | Licence d'IDS Technologie                                                           | AR3                     |
| 16/01/2025            | Plafonds tarifaires des offres de gros                                              | AR4, RA 2025            |
| T2 2026               | Premiers abonnés 5G de YAS Togo (3 951)                                             | AR1                     |

Absents des données : la crise sanitaire et tout événement propre à Moov avant 2016.

**Qualité et recoupements**

- **Format** : tout est en PDF (exports Word ou PowerPoint), avec trois mises en page successives. Il faudra extraire les tableaux des 34 numéros. Les chevauchements (5 trimestres par numéro) permettront de repérer les révisions.
- **D2 = ARCEP au T4 pour 2017 et 2018** : 3G de Togocel, 1 610 821 et 1 932 767 dans les deux sources.
- **D2 2019 ne correspond pas à l'ARCEP pour Togocel** : D2 donne 1 242 250 (3G), 174 474 (4G), 1 134 (GPRS) ; l'ARCEP au T4 2019, 2 373 589, 315 044 et 20 494. **La baisse de 2019 signalée par le 03 (section 2) n'existe pas chez l'ARCEP**, qui affiche +22,8 % sur un an pour la 3G de Togocel. L'origine des valeurs 2019 de D2 est inconnue.
- **Dans D2, la « 3G Atlantique Telecom » de 2018-2019 est en fait la 3G et la 4G de Moov réunies** : l'ARCEP publie « clients 3G et 4G de Moov » (633 580 au T4 2019, la valeur de D2). La 4G de Moov n'est séparée qu'à partir du T4 2019 (99 013). Cela explique la 4G de Moov « absente » en 2018-2019 dans D2.
- **Rupture chez l'ARCEP entre le T4 2019 et le T1 2020** : 3G de Togocel, de 2 373 589 à 1 057 232 (-58 %), pendant que la 4G progresse. Reclassement probable, à documenter.
- La page « [Le secteur en chiffres](https://arcep.tg/observatoire-2/le-secteur-en-chiffres/) » n'affiche que des valeurs de gabarit (5 000 000, 50, 0) : à ne pas utiliser.
- **Abonnements, pas utilisateurs** : pénétration data mobile de 79,2 % au T2 2026, contre 39,5 % d'utilisateurs (1b, 2024). AR1 ne se substitue jamais à O1-01.

---

## 5. Recherche sur le web (26/09/2026)

**Hors du périmètre actuel du 03**, comme l'ARCEP (décision D-6 et D-13).

**Méthode :** recherches web ciblées par manque, puis vérification directe des sources prometteuses : lecture du rapport MICS6 (608 pages), listes de variables des enquêtes EHCVM par l'API du catalogue de micro-données de la Banque mondiale, notes de l'API de la Banque mondiale sur D1. Rien n'a été téléchargé dans le projet. Les micro-données (MICS, EHCVM, Findex, Afrobaromètre) demandent un compte gratuit : c'est à toi de les récupérer.

**Résultat : l'usage par territoire (O1-05) et une partie des freins (O1-06) existent dans des enquêtes auprès des ménages. Et la série D1 se révèle presque entièrement estimée.**

| Réf.            | Résultat                                                                                                                                                                                  |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| O1-01, O1-02    | ⚠️ **D1 est une série estimée** (voir section 0, point 3). Les seuls points mesurés viennent des enquêtes W1 à W4 : 2017, 2018/19, 2021/22, 2024, avec des définitions différentes             |
| O1-05           | ✅ **Par région** : MICS6 2017 (W1, vérifié) ; EHCVM 2018/19 et 2021/22 (W2, variables vérifiées)                                                                                           |
| O1-06           | ⚠️ Compétences TIC ODD 4.4.1 (W1, 2017, par région) ; alphabétisation (W1 : 15-49 ans ; W2 : tous âges, donc 15 ans et plus calculable) ; téléphone portable (W1, W2) ; **smartphone : seulement Findex 2025, au niveau national (W3, non vérifié)** |
| B6              | ⚠️ Complétée par la presse : voir le tableau des événements ci-dessous                                                                                                                      |
| B7              | Rien de plus que l'ARCEP (AR1)                                                                                                                                                             |
| B11             | Non traité : l'API de la Banque mondiale suffit (agrégats Afrique subsaharienne, UEMOA), proposition C5 du 03                                                                             |

**Sources trouvées**

| #   | Source                                                                                                                                                                                                  | Contenu vérifié                                                                                                                                                                                                                                                                                                                                                                  | Apport                                                                                          | Réserves                                                                                                                                                  |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| W1  | **MICS6 Togo 2017** (INSEED, UNICEF) : [rapport PDF](https://washdata.org/report/togo-2017-mics-report-v2) ; micro-données sur mics.unicef.org (compte)                                                   | Tableaux SR.9.2 (TIC et Internet des ménages), SR.9.3W / SR.9.3M (usage de l'ordinateur, du portable et d'Internet), SR.9.4 (compétences TIC), SR.6.1 (alphabétisation), **par région (7 domaines : Maritime, Plateaux, Centrale, Kara, Savanes, Lomé commune, Golfe urbain), milieu, âge, instruction**. Internet au cours des 3 derniers mois : femmes 14,1 % (Lomé commune 36,0 ; Golfe urbain 31,7 ; Savanes 1,4 ; urbain 27,0 ; rural 2,4), hommes 27,6 %. Ménages avec Internet à la maison : 26,5 % (Lomé commune 53,7 ; Savanes 10,2). Compétences TIC (15-49 ans) : femmes 3,7 %, hommes 11,2 %. Portable possédé : femmes 56,6 %, hommes 78,3 % | O1-05 (2017, par région) ; O1-06 (compétences, alphabétisation, portable)                        | Une seule date ; 15-49 ans seulement ; 7 domaines qui ne correspondent pas exactement aux 5 régions (Lomé commune et Golfe urbain à part) ; pas de smartphone |
| W2  | **EHCVM 2018/19** ([catalogue 4298](https://microdata.worldbank.org/index.php/catalog/4298)) et **EHCVM 2021/22** ([catalogue 6279](https://microdata.worldbank.org/index.php/catalog/6279)), Banque mondiale, UEMOA et INSEED, accès « public » (compte gratuit) | Variables lues dans le dictionnaire, identiques dans les deux éditions : `s01q36` possession d'un portable ; `s01q39__1` à `__5` accès à Internet (téléphone, bureau, cybercafé, domicile, école) ; `s02q01` sait lire (français, langue locale) ; `s11q45` / `s11q46` ménage connecté ; `s11q48` / `s11q49` type de connexion ; `s11q47a` / `s11q48a` dépense Internet ; variables harmonisées `internet`, `telpor`, `alfa`, `ordin`. Géographie : région, préfecture, commune (2021/22) et milieu. Environ 6 100 ménages en 2021/22 | O1-05 à **deux dates**, par région ; O1-06 (alphabétisation des 15 ans et plus calculable, portable) ; hors objectif 1 : dépense Internet (O2-05) | « A accès à Internet » n'est pas « a utilisé Internet au cours des 3 derniers mois » (définition UIT) ; représentativité à confirmer dans la documentation (région x milieu attendu) ; la préfecture n'est pas un niveau représentatif. *Confirmé le 26/09/2026 : strates région x milieu, mêmes 540 grappes aux deux vagues (12.4)* |
| W3  | **Global Findex 2025** (données 2024) : [catalogue 7986, Togo](https://microdata.worldbank.org/index.php/catalog/7986)                                                                                  | Nouvelles séries annoncées : possession d'un portable et d'un **smartphone**, usage d'Internet (15 ans et plus)                                                                                                                                                                                                                                                                   | Seule source trouvée pour le smartphone (O1-06) ; point mesuré 2024 pour O1-01                  | Contenu pour le Togo non vérifié ; national seulement. *Vérifié le 26/09/2026 (section 7) ; micro-données : urbain / rural, pas de région (section 11)*                                                                                                     |
| W4  | **Afrobaromètre** Togo : vague 8 (2021), vague 9 (2022, [catalogue 6754](https://microdata.worldbank.org/index.php/catalog/6754)), vague 10 (14-30 novembre 2024, [résumé](https://www.afrobarometer.org/publication/togo-round-10-resume-des-resultats/)) | 1 200 adultes par vague ; fréquence d'usage d'Internet (question standard). Le Togo figure parmi les plus fortes hausses de l'usage des médias numériques (+39 points, dépêche AD800)                                                                                                                                                                            | Points mesurés 2021, 2022, 2024 pour O1-01 / O1-02                                               | Variables non vérifiées ; 1 200 personnes : régions trop imprécises. *Variables vérifiées le 26/09/2026 (section 7 et 9.5, W4+)*                                                                                      |
| W5  | **EDS-IV Togo** (EDST-IV) : [lancée le 13/03/2026](https://inseed.tg/lancement-officiel-de-la-quatrieme-enquete-demographique-et-de-sante-au-togo-edst-iv/)                                            | En cours de collecte ; les EDS récentes interrogent sur l'usage d'Internet et la possession d'un portable                                                                                                                                                                                                                                                                        | Futur point mesuré, par région                                                                  | Pas de résultats avant la fin de l'enquête                                                                                                                |
| W6  | **RGPH-5 (2022)** : [résultats définitifs](https://inseed.tg/resultats-definitifs-du-rgph-5-novembre-2022/)                                                                                             | Le recensement a relevé les équipements des ménages ; aucun tableau TIC par région trouvé en ligne                                                                                                                                                                                                                                                                             | Serait la source exhaustive de O1-05 / O1-06 (équipement) jusqu'à la commune                   | À demander à l'INSEED ou à chercher dans les rapports thématiques                                                                                        |
| W7  | **Ookla open data** : [dépôt](https://github.com/teamookla/ookla-open-data), [AWS](https://registry.opendata.aws/speedtest-global-performance/)                                                       | Tuiles d'environ 610 m, trimestrielles, mobile et fixe : débits, latence, nombre de tests et d'appareils                                                                                                                                                                                                                                                                       | Hors objectif 1 : qualité de service mesurée par territoire (O2-09)                              | Nombre d'appareils = utilisateurs de Speedtest : biaisé, pas une mesure de l'usage                                                                       |

**Écartés :** [DataReportal](https://datareportal.com/reports/digital-2025-togo) (agrégateur : 3,56 M d'internautes, soit 37,0 % en janvier 2025, dérivés des séries de l'UIT) ; indice de connectivité mobile de la GSMA (pas de données par pays en libre accès) ; [ITU DataHub](https://datahub.itu.int/data/?e=TGO) (accès refusé, erreur 403 : à réessayer depuis un navigateur).

**Événements trouvés sur le web (à fusionner avec la chronologie de la section 4)**

| Date                    | Événement                                                                                                               | Source                                                                                                                                                                                                  |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2017                    | Création de la holding Togocom (fusion de Togo Telecom et Togo Cellulaire)                                              | [Jeune Afrique](https://www.jeuneafrique.com/852701/economie/togo-axian-et-emerging-capital-partners-prennent-le-controle-de-togocom/)                                                                 |
| 11/06/2018 ; juin 2018  | Licences 4G de Togocel et de Moov (arrêté du 12/06/2018 dans AR3) ; lancement de la 4G à Lomé par les deux opérateurs   | [Togo First](https://www.togofirst.com/en/telecom/0207-1146-togocel-launches-4g-for-its-20th-anniversary)                                                                                              |
| Novembre 2019           | Privatisation : 51 % de Togocom cédés à Agou Holding (Axian et ECP)                                                     | [République togolaise](https://www.republiquetogolaise.com/telecoms/0711-3747-le-gouvernement-cede-51-de-togocom-au-consortium-international-agou-holding)                                              |
| 06/03/2020              | Premier cas de Covid-19                                                                                                  | [Wikipédia](https://fr.wikipedia.org/wiki/Pand%C3%A9mie_de_Covid-19_au_Togo)                                                                                                                            |
| 01/04/2020              | État d'urgence sanitaire (couvre-feu, bouclage du Grand Lomé)                                                           | [Wikipédia](https://fr.wikipedia.org/wiki/Pand%C3%A9mie_de_Covid-19_au_Togo)                                                                                                                            |
| 08/04/2020              | Lancement de Novissi (transferts sociaux par mobile money)                                                              | [AFD](https://www.afd.fr/fr/actualites/togo-novissi-la-solidarite-au-temps-du-covid-19)                                                                                                                 |
| 30/11/2020              | Togocom lance la 5G à Lomé avec Nokia, une première en Afrique de l'Ouest. Premiers abonnés 5G comptés par l'ARCEP : T2 2026 | [Nokia](https://www.nokia.com/about-us/news/releases/2020/11/30/nokia-and-togocom-deploy-first-5g-network-in-west-africa/), [Togo First](https://www.togofirst.com/en/itc/0711-17492-as-4g-soars-togos-pioneering-5g-network-remains-largely-untapped) |
| Décembre 2020           | Fin des différenciations tarifaires ; décision de janvier 2021 imposant des offres transparentes et comparables (Décision 011, AR4) | [CIO Mag](https://cio-mag.com/togo-une-baisse-des-tarifs-internet-mobile-saluee-par-larcep/)                                                                                                 |
| Début 2021              | Moov Togo devient Moov Africa                                                                                            | [Togo First](https://www.togofirst.com/fr/telecoms/0401-7055-moov-togo-devient-moov-africa-avec-une-nouvelle-identite-visuelle)                                                                        |
| T1 2021 → avril 2023    | Forfaits data de Moov : -71,4 % d'après l'analyse tarifaire de l'ARCEP (document AR6 d'avril 2023)                      | [CIO Mag](https://cio-mag.com/togo-une-baisse-des-tarifs-internet-mobile-saluee-par-larcep/)                                                                                                            |
| 18/03/2022              | Inauguration à Lomé du câble sous-marin Equiano (Google), premier atterrissage africain                                  | [Togo First](https://www.togofirst.com/fr/tic/1803-9620-togo-faure-gnassingbe-a-linauguration-du-cable-sous-marin-equiano-de-google)                                                                   |
| Novembre 2024           | Togocom devient YAS Togo                                                                                                 | [Togo First](https://www.togofirst.com/en/telecom/2911-15288-togocom-rebrands-as-yas)                                                                                                                  |

Les dates de presse ont un niveau de preuve C. Elles servent à annoter, jamais à établir une cause.

**Ce que cela change pour l'objectif 1 :** la question de l'objectif 1 se traite mieux avec deux couches distinctes :
1. La série estimée de l'UIT (D1 / 1b), pour la tendance d'ensemble.
2. Les points mesurés par enquête (W1 à W4), pour vérifier les ruptures et descendre au niveau régional.

Les définitions diffèrent entre les deux : âge (15-49 ans, 15 ans et plus, tous âges), notion (« a utilisé au cours des 3 derniers mois » ou « a accès »), période. Chaque point doit être libellé avec la sienne, sans relier les points entre eux.

---

## 6. Décisions (validées le 26/09/2026)

| #    | Objet                                               | Proposition                                                                                                                  | Décision |
| ---- | --------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | -------- |
| D-1  | BM1, BM2, BM3, BM7                                  | Télécharger, comme contexte de l'objectif 1                                                                                   | Validé le 26/09/2026 |
| D-2  | BM4, BM5, BM6                                       | Écarter                                                                                                                       | Validé le 26/09/2026 |
| D-3  | IN1 (projections démographiques)                    | Télécharger ; dénominateur annuel de référence, cohérent avec le RGPH et utilisé par l'ARCEP                                  | Validé le 26/09/2026 |
| D-4  | IN2, IN3 (indices de prix)                          | Télécharger                                                                                                                   | Validé le 26/09/2026 |
| D-5  | IN4 (électricité par préfecture)                    | Télécharger, pour les objectifs 4 et 5                                                                                        | Validé le 26/09/2026 |
| D-6  | Élargir le périmètre des sources à arcep.tg         | Oui : seule source des technologies après 2019 et du CA par opérateur                                                         | Validé le 26/09/2026 |
| D-7  | AR1 (34 observatoires)                              | Télécharger les PDF bruts, puis les extraire en une table trimestrielle opérateur x technologie x trimestre, avec contrôle des révisions | Validé le 26/09/2026 |
| D-8  | AR3 (registre)                                      | Télécharger la version du 26/06/2026                                                                                          | Validé le 26/09/2026 |
| D-9  | AR2, AR4                                            | Ne pas tout télécharger : relever les événements datés dans une table de chronologie (source, page), à compléter            | Validé le 26/09/2026 |
| D-10 | AR5, AR6                                            | Hors objectif 1 : à examiner avec l'objectif 2 (O2-05, O2-09)                                                                 | Validé le 26/09/2026 |
| D-11 | Seuil de stagnation ; A1 ; A16                      | Voir section 0                                                                                                                | Validé le 26/09/2026 |
| D-12 | Corrections du 03                                   | B1 et B5 (IN1) ; D2 2019 pour Togocel et « 3G Atlantique » = 3G + 4G de Moov (AR1) ; O1-04 et O2-02 à reclasser si D-6 est accepté ; D1 presque entièrement estimée (section 0, point 3) | Validé le 26/09/2026 |
| D-13 | Élargir le périmètre aux enquêtes auprès des ménages (W1 à W4) | Oui : seule voie vers O1-05 et O1-06. Priorité : EHCVM 2018/19 et 2021/22 (W2, deux dates, région x milieu), puis MICS6 2017 (W1 ; ses tableaux régionaux peuvent être transcrits du rapport sans les micro-données), puis Findex 2025 (W3, smartphone) | Validé le 26/09/2026 |
| D-14 | Micro-données à récupérer (compte gratuit)          | Toi : créer un compte sur microdata.worldbank.org (W2, W3, W4) et sur mics.unicef.org (W1)                                     | Validé le 26/09/2026 |
| D-15 | Série d'usage de l'objectif 1                       | Garder 1b pour la tendance, marquée « estimation UIT » année par année ; ajouter les points mesurés W1 à W4 avec leur définition ; ne lire une accélération que si les points mesurés la confirment | Validé le 26/09/2026 |
| D-16 | Chronologie                                         | Fusionner les tableaux des sections 4 et 5 en une table unique (date, événement, type, source, niveau de preuve)                | Validé le 26/09/2026 |
| D-17 | W5, W6                                              | EDS-IV : à suivre. RGPH-5 : demander à l'INSEED les tableaux d'équipement des ménages (téléphone, ordinateur, Internet) par région, préfecture et commune | Validé le 26/09/2026 |
| D-18 | W7 (Ookla)                                          | Hors objectif 1 : à examiner avec O2-09                                                                                       | Validé le 26/09/2026 |

---

## 7. Mise en œuvre (26/09/2026)

**Rangement :** `data/raw/_extradatas/obj1` à `obj4`, un fichier par objectif principal. Voir `data/raw/_extradatas/README.md` et `_MANIFEST.csv` (URL, date, taille, SHA-256, objectifs servis, fichier source ou dérivé). **71 fichiers, 139 Mo.** Le 03 et l'inventaire ne sont pas encore modifiés.

| Décision | Réalisé                                                                                                                         | Écart par rapport à la proposition                                                                                         |
| -------- | ------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| D-1      | BM1, BM2, BM3, BM7 → `obj1/`                                                                                                    | —                                                                                                                          |
| D-3, D-4 | IN1, IN2, IN3a (2010-2022), IN3b (2014-2024) → `obj1/`                                                                          | Les deux fichiers IN3 sont gardés : ensemble, ils couvrent 2010-2024                                                       |
| D-5      | IN4 → `obj4/`                                                                                                                   | —                                                                                                                          |
| D-7      | AR1 : 34 PDF → `obj1/AR1_arcep_observatoire/`, nommés par trimestre (`AR1_2018T1_…` à `AR1_2026T2_…`)                          | Extraction en table : pas encore faite (voir point P5)                                                                     |
| D-8      | AR3 (registre du 26/06/2026) → `obj1/`                                                                                           | —                                                                                                                          |
| D-9      | AR2 (rapport 2017) et AR4 (3 décisions citées) → `obj1/`                                                                        | Seules les pièces citées dans la chronologie                                                                               |
| D-10     | AR5 (instantané HTML des tarifs) et AR6 (9 études) → `obj2/`                                                                    | **1 étude AR6 non obtenue** : campagne QoS du 2e semestre 2023, lien mort (404) sur arcep.tg                                |
| D-13     | W1 : rapport MICS6 + **transcription des 7 tableaux régionaux** (660 valeurs) ; W3 : base Findex 2025 + glossaire ; W4 : Afrobaromètre | **Afrobaromètre : vagues 5, 6 et 7 ajoutées** (même source, points 2012, 2014, 2017) en plus des vagues 8, 9 et 10 validées |
| D-14     | —                                                                                                                               | EHCVM (W2) : micro-données non téléchargées, compte requis                                                                  |
| D-16     | `obj1/CH1_chronologie-evenements.csv` : 40 événements (date, précision, type, opérateur, source, niveau de preuve)             | —                                                                                                                          |
| —        | MS1 (datacenters) → `obj1/`, pour la traçabilité de la chronologie                                                              | Ajout mineur                                                                                                               |

**Vérifications faites pendant le téléchargement**

- **Types de fichiers** : 49 PDF, 11 CSV, 2 xlsx, 6 SPSS, 1 HTML, tous conformes (aucune page d'erreur enregistrée à la place d'un fichier).
- **W1, transcription MICS6** : pour chaque tableau, le total est égal, à 0,25 point près, à la moyenne pondérée des 7 régions et à celle des 2 milieux ; les effectifs somment au total. Les valeurs nationales concordent avec le tableau des indicateurs du rapport (Internet au cours des 3 derniers mois : femmes 14,1 %, hommes 27,6 % ; compétences TIC : 3,7 % et 11,2 %). Le rapport contient aussi des tableaux d'erreurs d'échantillonnage (annexe), utiles pour la règle du coefficient de variation de O1-05.
- **W3, Findex 2025, Togo, 15 ans et plus, 2024** (vérifié ; ces séries n'existent pas avant 2024) : possède un portable 82,5 % ; téléphone principal = smartphone 45,1 % ; a utilisé Internet au cours des 3 derniers mois 43,7 % (tous les jours : 22,4 %) ; achète des forfaits data 35,2 %. Sans smartphone à cause du coût : 32,1 % (raison principale « manque d'argent » : 27,5 %) ; à cause de la difficulté à lire ou écrire sur un smartphone : 13,3 % ; à cause de la couverture : 8,4 %. **C'est une mesure nationale de l'équipement et des freins (O1-06).**
- **W4, Afrobaromètre** : 1 200 répondants par vague ; terrain en décembre 2012 (vague 5), octobre 2014 (6), novembre 2017 (7), décembre 2020 - janvier 2021 (8), mars 2022 (9), novembre 2024 (10). Question sur la fréquence d'usage d'Internet dans les 6 vagues ; « le téléphone a-t-il accès à Internet » depuis la vague 7 (approximation du smartphone) ; variable région dans toutes les vagues.
- **AR4, décision 011** : datée du **19/01/2021** (signature, p. 4). Ses visas ajoutent la loi n° 2012-018 du 17/12/2012 sur les communications électroniques (intégrée à la chronologie).
- **AR1 et 2b, abonnements data mobile** : 2b est égal à la valeur du T4 de l'ARCEP pour 2018 (3 660 055), 2020 (4 891 899) et 2022 (4 870 282). Il en diffère :
  - pour **2021** : le numéro du T4 2021 (fichier intitulé « Mode de comptabilité ») annonce 5 906 003, mais les numéros de 2022 révisent toute l'année 2021 (T4 : 4 651 596, la valeur de 2b). **Révision méthodologique de l'ARCEP** : pour chaque trimestre, il faut prendre la publication la plus récente ;
  - pour **2019** : 2b donne 3 379 910, valeur absente de toutes les publications de l'ARCEP (T4 2019 : 4 671 179). Même constat que pour D2 en 2019 : l'origine des valeurs 2019 de l'INSEED est inconnue.

---

## 8. Points à trancher avant la mise à jour du 03 (26/09/2026)

| #   | Question                                                                                                              | Options                                                                                                                                                                                   | Proposition                                                                                                                                                                                                                                        |
| --- | --------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| P1  | Version de D1 (11.A1)                                                                                                 | CSV du portail ; API                                                                                                                                                                      | **API**, chaque année marquée « estimation UIT » sauf 2017 (INSEED). Seule 2021 change vraiment la lecture (+4,5 % avec l'API, +12,0 % avec le CSV)                                                                                             |
| P2  | Seuil de stagnation de O1-02 (\|g\| < 2 %), jamais atteint                                                             | Garder le 02 et consigner l'écart dans le 03 ; ajouter une classe « ralentissement » au 02 maintenant                                                                                   | **Consigner dans le 03** (le 02 n'est pas modifié à l'étape 03) ; proposer pour l'étape d'analyse une classe « ralentissement » (croissance < moyenne - 1 écart-type), appliquée d'abord aux points mesurés. **Vigilance V2 (26/09/2026)** : le 03 doit dire en toutes lettres que la stagnation n'est pas traitée avec le seuil actuel, sinon un lecteur croira cette partie de l'objectif résolue. Le 01 parle pourtant des périodes où l'usage « a ralenti, stagné ou reculé » |
| P3  | Dénominateur de population (11.A16)                                                                                   | Population implicite de la Banque mondiale (proposition actuelle du 03) ; IN1 (INSEED)                                                                                                    | **IN1 pour tous les taux que nous calculons** (cohérent avec le RGPH à 0,3 % près et avec l'ARCEP). D1 garde son propre dénominateur. Pour O1-03, comparer des **nombres** (utilisateurs = taux D1 x population Banque mondiale, niveau C) plutôt que des taux à dénominateurs différents. **Vigilance V3 (26/09/2026)** : l'écart de 12 % n'est pas un détail. D1 (O1-01 : 39,5 % en 2024) et un taux d'abonnements pour 100 habitants calculé avec IN1 ne sont pas comparables. Le 03 ajoute un encadré « Dénominateurs : trois bases coexistent » (Banque mondiale, IN1, RGPH) ; O1-03 compare strictement des nombres |
| P4  | Source des abonnements Internet et par technologie (11.A15 à réviser)                                                  | D2 / 2b partout où ils existent ; AR1 à partir de 2018                                                                                                                                    | **D2 / 2b jusqu'en 2017, AR1 à partir de 2018** (valeur du T4 pour l'annuel, dernière publication pour chaque trimestre). Au point de raccord, les deux sources sont identiques en 2018 et quasi identiques en 2017 (786 abonnés d'écart sur la 3G de Moov, soit 0,03 %) : pas de rupture de raccord. On écarte ainsi les valeurs 2019 et 2021 d'origine inconnue ou non révisée. **Vigilance V1 (26/09/2026)** : la valeur du T4 est retenue **par convention** (stock de fin d'année, celle de l'UIT, et celle de l'INSEED, dont les valeurs annuelles de 2b sont celles du T4 de l'ARCEP) ; ce n'est pas une moyenne. Pour O1-04 et O2-01, l'année est représentée par son dernier trimestre : à documenter dans le 03. La saisonnalité est à vérifier, et la **moyenne des 4 trimestres sera testée en sensibilité**. La convention ne vaut que pour les stocks (abonnés, comptes, points de vente) : les flux (CA, investissement, trafic, transactions) s'additionnent sur les 4 trimestres. Premier contrôle : section 12.1 |
| P5  | Quand extraire AR1 en table (D-7)                                                                                      | Avant la mise à jour du 03 ; à l'étape de préparation des données                                                                                                                         | **À l'étape de préparation** : le 03 décrit le contenu, les ruptures et les révisions (déjà vérifiés sur échantillon)                                                                                                                              |
| P6  | Portée de la mise à jour du 03                                                                                        | Mettre à jour le 03 maintenant (objectif 1, plus les effets déjà connus sur les objectifs 2 à 4) ; mener d'abord la même recherche pour les manques des objectifs 2 à 4, puis une seule mise à jour | **Rechercher d'abord les objectifs 2 à 4** : plusieurs manques y ont des pistes probables (couverture 3G/4G et tarifs dans les documents de l'ARCEP, milieu urbain / rural et 15 ans et plus par territoire, usage du mobile money par région dans l'EHCVM et le Findex). Une seule mise à jour du 03 évite de le reprendre deux fois |
| P7  | EHCVM (D-14) : attendre les micro-données ?                                                                            | Attendre ; documenter sans elles                                                                                                                                                         | **Ne pas attendre** : les variables sont vérifiées dans le dictionnaire ; le 03 les décrit comme « identifiées, à récupérer »                                                                                                                     |
| P8  | Vagues 5 à 7 de l'Afrobaromètre, ajoutées sans validation explicite                                                    | Garder ; retirer                                                                                                                                                                          | **Garder** : même source, trois points mesurés de plus (2012, 2014, 2017)                                                                                                                                                                          |

**Décision (26/09/2026) : P1 à P5, P7 et P8 validés** (P6 l'était déjà), avec les vigilances V1 à V3 notées dans P2, P3 et P4. Mise en œuvre : section 12.

---

## 9. Recherche pour les objectifs 2 à 5 (26/09/2026)

Option validée au point P6 : chercher les manques des objectifs 2 à 4 avant de mettre à jour le 03. Sources parcourues : les 42 organisations d'opendata.gouv.tg, geodata.gouv.tg, les documents ARCEP, la bibliothèque de micro-données de la Banque mondiale et le web. **Rien n'a été téléchargé dans `data/raw/`** ; les fichiers examinés sont restés dans un dossier temporaire.

**Manques visés (d'après le 03) :**

| Obj. | Manque (réf. 03)                                                       | Indicateurs          |
| ---- | ---------------------------------------------------------------------- | -------------------- |
| 2    | CA par opérateur ; investissement après 2019                           | O2-02, O2-04         |
| 2    | Tarifs, coût de 1 Go, revenu par habitant (B10)                         | O2-05                |
| 2    | Couverture 3G/4G par territoire (B4) ; sites radio                     | O2-06, O2-08         |
| 2    | Qualité de service mesurée                                             | O2-09                |
| 3    | Milieu urbain / rural par territoire (B3)                              | O3-02, O4-01, O4-05  |
| 3    | Agents actifs ; comptes et transactions mobile money                   | O3-03, O3-04         |
| 3    | Usage du mobile money par territoire ; coût du mobile money (B10)      | O3-05, O3-06         |
| 4    | Population de 15 ans et plus par territoire (B1) ; repère UEMOA (B11)  | O4-02, O4-04         |
| 5    | Lieux candidats (B12)                                                   | étape 11             |

### 9.1 Micro-données de la Banque mondiale (compte du `.env`)

- **Connexion non obtenue.** Le `.env` contient `firstanme`, `lastname` et `password`, mais **pas d'adresse e-mail**, alors que microdata.worldbank.org se connecte par e-mail. L'étape de l'e-mail a été passée avec l'adresse git de l'utilisateur (le site affiche « Log in cartersedmund@gmail.com »). En revanche, la soumission du mot de passe renvoie une page vide sans ouvrir de session. Arrêt après une seule tentative, pour ne pas risquer un blocage du compte. **Point Q1.** **Mise à jour du 26/09/2026 : réglé, voir section 11.**
- **Ce que le dictionnaire public de l'EHCVM 2021/22 apporte en plus pour les objectifs 2 à 4** (vérifié par l'API, sans compte) :
  - Module individuel, section 6 : compte en banque, à la poste, en IMF (`s06q01__1..3`) ; tontine ou association d'entraide (`s06q07`) ; crédit (`s06q03` à `s06q19`). **Pas de question sur le compte mobile money.**
  - Section 13 : mode principal des transferts reçus (`s13q21`).
  - **Module communautaire, par village ou quartier enquêté** : « le réseau de téléphonie mobile est-il bien capté ? » pour chacun des 3 réseaux (`s01q13__1..3`) ; réseau électrique (`s01q11`) ; bureau de poste (`s02q01_9`), banque ou IMF (`s02q01_12`), marchés (`s02q01_13`, `_14`). C'est une **mesure de terrain de la couverture** sur l'échantillon de grappes (O2-06, O4-06).

### 9.2 opendata.gouv.tg : tout le catalogue (42 organisations, 1 562 jeux)

Les 325 jeux des 39 autres organisations, et les 1 237 déjà vus, ont été refiltrés avec les mots-clés des objectifs 2 à 4.

| #    | Jeu                                                                                                                                                                                                                                                                  | Constat                                                                                                                                                                                                                                                                                                                                  | Apport                                                                        |
| ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| CO1  | [Statistiques de population infranationales (OCHA, COD-PS)](https://opendata.gouv.tg/fr/datasets/donnees-ouvertes-sur-les-statistiques-de-la-population-infranationale-au-togo-selon-les-donnees-de-locha-office-for-the-coordination-of-humanitarian-affairs-bureau-de-la-coordination-des-affaires-humanitaires/) (HDX) | Sur le portail : régions seulement. La source sur HDX ([cod-ps-tgo](https://data.humdata.org/dataset/cod-ps-tgo)) contient aussi **37 préfectures (ancien découpage) x sexe x tranches de 5 ans, 2021** : projection de l'INSEED sur la base du recensement de 2010. 15 ans et plus : 61,1 % | B1 par préfecture, **supplanté par RG2** (9.5) ; utile en contrôle |
| BM8  | [Consommation moyenne ou revenu par habitant ($ PPA 2017 par jour)](https://opendata.gouv.tg/fr/datasets/donnees-ouvertes-sur-la-consommation-moyenne-ou-revenu-par-habitant-et-population-totale-ppa-2017-par-jour-au-togo/) (SI.SPR.PCAP) | 4,18 $ PPA par jour en 2021 (EHCVM) ; années d'enquête seulement                                                                                                                                                                                                                                                                        | Variante du revenu pour O2-05                                                 |
| —    | Ministère du Commerce : Marchés ; Enseignement : établissements scolaires ; Santé : formations sanitaires ; « Établissements administratifs »                                                                                                                          | Mêmes couches PRISE que geodata (9.3)                                                                                                                                                                                                                                                                                                   | Lieux candidats (B12)                                                         |

**Écartés :** « Secteur bancaire de l'UEMOA » (Kaggle : ratios financiers de banques 2013-2019, pas des points d'accès) ; jeux MEF « Banques », « Microfinances », « Assurances », « Mutuelles », « DAB » (copies de D4 et 4c, déjà constaté par le 03) ; bilans et comptes de résultat des banques (INSEED, agrégats sans territoire) ; services d'épargne postale (= 4i) ; « Développement urbain » et « Science et technologie » (HDX : indicateurs nationaux de la Banque mondiale).

### 9.3 geodata.gouv.tg (177 couches et 239 indicateurs ouverts ; 277 couches et 130 indicateurs non ouverts)

| #   | Élément                                                                                                                                                                   | Apport                                                                                                                              |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| GD1 | Couches ouvertes « Agences - Moov », « Agences - Togocom », « Agences - Télécom », « Agences - La Poste »                                                              | Présence des opérateurs par territoire (objectif 2) ; **La Poste comme type de point financier formel** (O3-01, point Q5)            |
| GD2 | Couches ouvertes « Marchés », « Établissements scolaires » (et sous-couches), « Formations sanitaires », « Administration - Établissements » (22 ministères)          | **Lieux candidats (B12, C4 du 03)** pour l'étape 11                                                                                 |
| GD3 | Indicateurs ouverts : longueur des réseaux électriques BT, MT, HT ; « part des habitants à moins de 50 m du réseau BT » ; « nombre de villages (chefs de village) » ; « proportion d'écoles avec une salle informatique » | Électricité par territoire (complète IN4) ; indice indirect du caractère rural ; contexte de l'objectif 1                          |

**Rien sur geodata** pour l'âge de la population, le milieu urbain / rural ou la couverture par technologie. Les tours télécoms, les agents mobile money par opérateur et les mini-réseaux sont dans des couches **non ouvertes**.

### 9.4 Documents ARCEP (déjà téléchargés en AR1, ou lus dans le rapport 2025)

- **AR1, mobile money (au moins depuis le T4 2021)** : comptes, **points de vente (PDV) par opérateur** (33 924 au T4 2021, 64 540 au T2 2026) et valeur des transactions par opérateur. Également le CA et l'investissement par opérateur (O2-02, O2-04), la FTTH par opérateur (O2-07). **Recoupements** :
  - Les 19 788 points de D5, recomptés par opérateur (les 12 649 points « Moov, Togocom » comptés deux fois), donnent environ 32 400, proches des 33 924 PDV de l'ARCEP au T4 2021 : D5 est cohérent avec l'ARCEP à la date PRISE.
  - Les abonnés mobile money de 2b en 2022 (3 005 048) sont égaux à ceux de l'ARCEP au T4 2022.
- **Rapport d'activité 2025** (non téléchargé à cette date, car D-9 ne retenait que les pièces de la chronologie ; *téléchargé le 26/09/2026 dans `obj2/`, Q11*) :
  - **nombre de sites par opérateur et par technologie, 2021-2025** (2025 : Moov 718, YAS 1 122), et nombre de cellules 2G/3G/4G → **O2-08 au niveau national** ;
  - étude sur les fréquences IMT dans 142 localités : « forte disparité régionale », Maritime la mieux desservie, Savanes la moins ;
  - 6 808 localités éligibles au plan de couverture, dont 88 zones blanches (2021).
- **AR6** : campagnes QoS dans 84 localités de 36 préfectures (O2-09, qualité mesurée par localité) *(corrigé en 15.3 : 84 localités en 2025, 94 dans la campagne 2024 téléchargée, résultats sans valeur par localité)* ; analyse des tarifs d'avril 2023 (O2-05).

### 9.5 Web

| #    | Source                                                                                                                                                                                                                         | Contenu vérifié                                                                                                                                                                                                                                                                                                                              | Apport                                                                                                     |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| RG1  | **RGPH-5, livret 01** : distribution spatiale de la population par sexe ([téléchargement INSEED 6616](https://inseed.tg/download/6616/), 102 p.)                                                                             | Population résidente 2022 par commune et **par canton**, par sexe                                                                                                                                                                                                                                                                            | Population des cantons (niveau que D6 ne rattache pas bien, section 7 du 03)                               |
| RG2  | **RGPH-5, livret 02** : population par groupe d'âge aux niveaux national, régional et préfectoral ([6619](https://inseed.tg/download/6619/), 87 p.)                                                                          | **Par préfecture : groupes d'âge x milieu (urbain / rural) x sexe**, recensement 2022                                                                                                                                                                                                                                                       | **B1 (15 ans et plus) et B3 (milieu) par préfecture**, source officielle                                   |
| RG3  | **RGPH-5, livret 03** : population des communes par groupe d'âge ([6622](https://inseed.tg/download/6622/), 236 p.)                                                                                                         | **Par commune (117 tableaux) : groupes d'âge x milieu x sexe**                                                                                                                                                                                                                                                                              | **B1 et B3 par commune**                                                                                   |
| AS1  | **Annuaire statistique national 2024** ([7668](https://inseed.tg/download/7668/), 776 p.)                                                                                                                                    | Chapitre 24 : séries télécom de l'INSEED prolongées jusqu'en 2024 (national ; 2021 = valeur révisée de l'ARCEP) ; tableau 4.17 : **ménages équipés en 2020 (enquête EIPT)** : connexion Internet 43,7 % (urbain 65,9, rural 25,2), portable 88 %, ordinateur 10 % ; privations multidimensionnelles EHCVM 2018 et 2021 (compte bancaire, électricité, alphabétisation des adultes) par milieu | Point mesuré 2020 pour l'objectif 1 ; contexte                                                             |
| AS2  | **Annuaires statistiques régionaux 2024** (Centrale, Maritime, Savanes… ; exemple Savanes : [7811](https://inseed.tg/download/7811/))                                                                                       | Population estimée au 1er janvier de chaque année **par préfecture** ; rien sur les télécoms ou la finance par préfecture                                                                                                                                                                                                                  | Dénominateur annuel par préfecture                                                                          |
| IT1  | **Paniers de prix TIC de l'UIT, 2008-2025** ([fichier xlsx](https://www.itu.int/en/ITU-D/Statistics/Documents/ICT_Prices/ITU_ICTPriceBaskets_2008-2025.xlsx))                                                              | Togo, en % du RNB mensuel par habitant : **data mobile 1 Go : 5,85 % (2023), 5,45 % (2024), 5,30 % (2025)** ; 2 Go : 11,37 % (2021) à 5,68 % (2025) ; 1,5 Go : 16,6 % (2018-2019) ; panier postpayé 1 Go : 73,6 % (2013), 21,3 % (2014). RNB mensuel par habitant : 52 829 FCFA (2024) | **O2-05 (coût de 1 Go rapporté au revenu)**, national ; chronologie des prix (objectif 1)                   |
| BC1  | **BCEAO, rapport annuel sur les services financiers numériques dans l'UEMOA 2024** ([PDF](https://www.bceao.int/fr/publications/rapport-annuel-sur-les-services-financiers-numeriques-dans-luemoa-2024), 40 p.)            | Comparaisons par pays (comptes, transactions, émetteurs). D'après la presse, pour le Togo en 2024 : 12,55 M de comptes ouverts, plus de 6 M actifs, plus de 81 000 points de service (**à vérifier dans le rapport**). *Vérifié le 26/09/2026 (12.4)*                                                                                                                      | O3-03, O3-04 ; repère UEMOA                                                                                 |
| BC2  | **BCEAO, rapport annuel sur la situation de l'inclusion financière 2024** et tableau de bord 2024 ([page](https://www.bceao.int/fr/publications/tableau-de-bord-de-linclusion-financiere-dans-luemoa-au-titre-de-lannee-2024)) | Taux global de pénétration démographique : **points de service pour 10 000 adultes, par pays** (UEMOA : 193 en 2024) ; le Togo en tête des progressions (+131). Non téléchargé (délai dépassé). *Téléchargé le 26/09/2026 ; le « +131 » est la pénétration géographique, et la définition des points inclut le mobile money (12.4, R1)*                                                                                                                                             | **Repère UEMOA de O4-02 (B11)**, à condition de vérifier que la définition des points est comparable      |
| TF1  | **Grilles tarifaires du mobile money** : pages de Moov Africa Togo ([retrait](https://moov-africa.tg/moov-money/retrait-flooz/), [transfert](https://moov-africa.tg/moov-money/transfert-flooz/)) ; agrégateur [momocalc](https://momocalc.com/fr/togo) | Frais par tranche de montant (Flooz ; Mixx de YAS à rechercher, *sans grille de retrait officielle d'après la vérification du 26/09/2026, 12.4*) ; taxe de 10 % sur les frais ; transferts UEMOA gratuits depuis octobre 2025 (PI-SPI de la BCEAO)                                                                                                                                                                           | **O3-06**, instantané daté                                                                                  |
| GH1  | **GHSL, degré d'urbanisation** (GHS-DUC R2023A, unités GADM) ; WorldPop, degré d'urbanisation 1 km 2026-2027                                                                                                               | Classement urbain / rural par modélisation                                                                                                                                                                                                                                                                                                  | Alternative à B3, **supplantée par RG2 et RG3**                                                             |
| OC1  | **OpenCellID** ([téléchargements](https://opencellid.org/downloads.php))                                                                                                                                                     | Antennes observées (GSM, UMTS, LTE) avec coordonnées, par collecte participative ; clé API gratuite requise                                                                                                                                                                                                                                   | Indice indirect de O2-06 et O2-08 par territoire (biais de collecte)                                        |
| W4+  | **Afrobaromètre** (déjà en `obj1/W4_afrobarometre/`)                                                                                                                                                                         | Vague 9 (2022) : compte bancaire (`Q90E`), en IMF (`Q90G_TOG`), **mobile money** (`Q90H_TOG`) ; vague 10 (2024) : compte bancaire (`Q90E`), **mobile money** (`Q90G`) ; région ; présence d'une banque ou d'une IMF dans la zone d'enquête (`EA_FAC_F`, vagues 7 à 10)                                                                  | **O3-05 par région** (1 200 personnes : précision à contrôler avec la règle du coefficient de variation)   |

### 9.6 Résultat par manque

| Manque                                   | Résultat                                                                                                                  | Source proposée                                              |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| O2-02, O2-04 : CA et investissement par opérateur | ✅ 2018-2026, trimestriel                                                                                       | AR1                                                          |
| O2-05 : coût de 1 Go et revenu           | ✅ National, 2013-2025                                                                                                     | IT1 ; AR5, AR6 ; BM8 en variante                             |
| O2-06 : couverture par territoire        | ⚠️ Toujours un proxy : 3i ; mesure de terrain sur l'échantillon de l'EHCVM ; OpenCellID                                  | 3i, W2 (communautaire), OC1                                  |
| O2-08 : sites radio                      | ⚠️ National par opérateur et technologie, 2021-2025 ; territorial seulement via OpenCellID                                | Rapport d'activité ARCEP 2025 ; OC1                          |
| O2-09 : qualité de service               | ⚠️ 84 localités (campagnes ARCEP) ; Ookla (W7)                                                                            | AR6 ; W7                                                     |
| B3 : milieu urbain / rural par territoire | ✅ **Par préfecture et par commune, 2022**                                                                               | RG2, RG3                                                     |
| O3-03, O3-04 : points de vente, comptes, transactions | ✅ Par opérateur, trimestriel (ARCEP) ; annuel et comparable UEMOA (BCEAO) ; « agents actifs » toujours absents | AR1 ; BC1                                                    |
| O3-05 : usage du mobile money par territoire | ⚠️ Par région, petit échantillon                                                                                      | W4 (vagues 9 et 10)                                          |
| O3-06 : coût du mobile money             | ⚠️ Instantané 2026 des grilles des opérateurs                                                                             | TF1                                                          |
| B1 : 15 ans et plus par territoire       | ✅ **Par préfecture et par commune, 2022**                                                                                | RG2, RG3 (CO1 en contrôle)                                   |
| B11 : repère UEMOA de O4-02              | ⚠️ Points de service pour 10 000 adultes par pays ; définition à comparer                                                 | BC2                                                          |
| B12 : lieux candidats                    | ✅ Couches ouvertes                                                                                                       | GD2                                                          |

---

## 10. Points à trancher (26/09/2026, avant la mise à jour du 03)

**Restent ouverts depuis la section 8 :** P1 à P5, P7 et P8 (seul P6 a été validé). *Validés depuis, le 26/09/2026.*

| #   | Question                                                                                         | Proposition                                                                                                                                                                                                                             |
| --- | ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Q1  | Compte de micro-données de la Banque mondiale | **Réglé le 26/09/2026** : e-mail ajouté au `.env`, connexion réussie, micro-données téléchargées (section 11) |
| Q2  | Télécharger et transcrire les livrets du RGPH-5                                                   | **Oui** : RG2 (39 préfectures) et RG3 (117 communes), en tables âge x milieu x sexe, avec les mêmes contrôles que pour MICS6 (les groupes d'âge et les milieux somment au total) ; RG1 (cantons) en second temps. Rangement : `obj4/` (B1) |
| Q3  | Source des 15 ans et plus par territoire (B1)                                                     | **RG2 et RG3** (recensement 2022, officiel, même base que D6) ; CO1 (projection 2021) seulement en contrôle                                                                                                                             |
| Q4  | Source du milieu urbain / rural (B3)                                                              | **RG2 et RG3** (définition du recensement) ; GH1 écarté                                                                                                                                                                                 |
| Q5  | Agences de La Poste (GD1) comme type de point financier formel (O3-01, O4-01)                    | Les compter à part, en test de sensibilité : la Poste offre des services d'épargne et de mandats (4i), mais elle n'est ni banque ni IMF                                                                                                 |
| Q6  | Couverture par territoire (O2-06)                                                                 | Garder le proxy 3i (A17) ; le confronter au module communautaire de l'EHCVM (réseau bien capté, par grappe) ; OpenCellID seulement si l'utilisateur crée une clé                                                                        |
| Q7  | Sources du mobile money (O3-03, O3-04)                                                            | ARCEP (AR1) pour les séries par opérateur ; BCEAO (BC1) pour la comparaison UEMOA ; afficher l'écart de définition (comptes ARCEP ≠ comptes ouverts ou actifs BCEAO)                                                                   |
| Q8  | Coût du mobile money (O3-06)                                                                      | Instantané daté des grilles officielles de Moov (Flooz) et de YAS (Mixx), niveau C ; l'agrégateur momocalc seulement en contrôle                                                                                                       |
| Q9  | Repère UEMOA de O4-02 (B11)                                                                       | Télécharger BC2 et vérifier ce que la BCEAO compte comme « point de service » avant toute comparaison                                                                                                                                  |
| Q10 | Lieux candidats (GD2, objectif 5)                                                                 | Créer `data/raw/_extradatas/obj5/` et y télécharger les couches ouvertes, ou attendre l'étape 11                                                                                                                                       |
| Q11 | Nouveaux téléchargements dans `_extradatas`                                                       | `obj2/` : IT1, rapport ARCEP 2025 (sites) ; `obj3/` : BC1, TF1 (instantané HTML) ; `obj4/` : RG1 à RG3, CO1, AS2, BC2 ; `obj1/` : AS1 (point 2020) ; `obj5/` : GD2 (si Q10)                                                          |

**Décision (26/09/2026) : Q2 à Q11 validés.** Pour Q10, l'option retenue est « créer `obj5/` et y télécharger les couches ouvertes » (cohérente avec C4 du 03 et avec Q11). Mise en œuvre : section 12.

---

## 11. Micro-données de la Banque mondiale récupérées (26/09/2026)

**Connexion** : réussie avec l'e-mail ajouté au `.env` (le compte n'utilise pas l'adresse git : c'est ce qui bloquait la première tentative).

**Demandes d'accès** : les jeux EHCVM sont en « Public Use ». Chaque téléchargement exige une demande (description de l'usage et acceptation des conditions de la Banque mondiale). **Avec l'accord explicite de l'utilisateur**, les demandes ont été soumises le 26/09/2026 avec le texte ci-dessous ; l'accès a été accordé immédiatement. Pour le Findex 2025, seule l'acceptation des conditions était demandée.

> Academic data-engineering challenge (EconomyNumeric, Togo). Objective: measure digital and financial inclusion in Togo (Internet access, mobile phone ownership, literacy, access to financial services: bank, postal and MFI accounts, savings groups) by region and urban/rural area, and compare these survey-based indicators with administrative data (ARCEP subscriptions, geolocated financial service points, 2022 census). Methods: weighted descriptive statistics at region x urban/rural level; the community module is used to assess mobile network reception by surveyed locality. Outputs: aggregated indicators, tables and maps in a project report. No individual-level data will be published or redistributed; the dataset will be cited as required.

**Conditions à respecter** : usage statistique et résultats agrégés seulement ; aucune redistribution ; aucune tentative d'identifier les répondants ni de lier des jeux de données dans ce but ; citation de la source. **Les dossiers `obj1/W2_ehcvm/` et `obj1/W3_findex2025/microdonnees/` ont été ajoutés au `.gitignore`.**

| Fichier (sous `data/raw/_extradatas/obj1/`)                              | Contenu                                                                                                                  |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| `W2_ehcvm/2021-22/TGO_2021_EHCVM-2_v01_M_STATA14.zip` (+ `donnees/`)     | EHCVM 2021/22, Stata 14 : 57 fichiers (sections ménage `s00` à `s20`, communautaires `s00_co` à `s04_co`, fichiers harmonisés `ehcvm_individu`, `ehcvm_menage`, `ehcvm_welfare`, `ehcvm_ponderations`) |
| `W2_ehcvm/2021-22/` : document d'information de base, questionnaires ménage (vagues 1 et 2), documentation du catalogue | Plan de sondage et pondérations ; libellés des questions                                                                |
| `W2_ehcvm/2018-19/TGO_2018_EHCVM_v02_M_Stata.zip` (+ `donnees/`)         | EHCVM 2018/19, Stata : 52 fichiers, dont **`grappe_gps_tgo2018.dta` (coordonnées GPS des grappes)**                     |
| `W2_ehcvm/2018-19/` : document d'information de base, questionnaires ménage et communautaire, nomenclature, documentation du catalogue | Idem                                                                                                                     |
| `W3_findex2025/microdonnees/TGO_2024_FINDEX_v02_M_STATA14.zip` (+ `donnees/`) | Findex 2025 Togo (données 2024) : 1 000 répondants ; variables `urbanicity` et `wgt` ; **pas de variable région**   |

**Vérifications** (lecture des fichiers, estimations nationales pondérées par `hhweight`, individus de 15 ans et plus ; simples contrôles de cohérence, pas encore des indicateurs du projet) :

| Variable harmonisée                  | EHCVM 2018/19 | EHCVM 2021/22 | Repères                                                        |
| ------------------------------------ | ------------- | ------------- | -------------------------------------------------------------- |
| `internet` (a accès à Internet)      | 23,7 %        | 35,4 %        | UIT (population totale, estimé) : 15,5 % en 2018, 30,3 % en 2021 ; Findex (15 ans et plus, 3 derniers mois) : 43,7 % en 2024 |
| `telpor` (possède un portable)       | 60,3 %        | 64,9 %        | Findex 2024 : 82,5 %                                           |
| `alfa` (sait lire et écrire)         | absente du fichier harmonisé (à reconstruire depuis `s02q01`) | 70,8 %        | —                                                              |

- Individus : 27 482 (2018/19), 28 815 (2021/22). Module communautaire : 540 localités par vague, variables `s01q13__1` à `__3` (réseau mobile bien capté) présentes dans les deux vagues.
- **Domaines régionaux différents d'une vague à l'autre** : « Lomé commune » en 2018/19, « Grand Lomé » en 2021/22, plus les 5 régions. Une comparaison régionale entre les deux vagues demande de traiter Lomé à part (point Q12).
- **Findex** : pas de variable région, seulement urbain / rural (`urbanicity`). Pour O3-05, il ne donne donc qu'un écart ville / campagne.

**Point ajouté :**

| #   | Question                                                                                  | Proposition                                                                                                                                                      |
| --- | ----------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Q12 | Comparabilité régionale des deux EHCVM (Lomé commune en 2018/19, Grand Lomé en 2021/22)   | Comparer les deux vagues au niveau national et par milieu ; au niveau régional, seulement pour les 5 régions hors Lomé, avec Lomé présenté à part et la différence de périmètre signalée |

**Décision (26/09/2026) : Q12 validé.** La vérification faite ensuite montre que la précaution n'est pas nécessaire : **mêmes grappes, seul le libellé change** (section 12.4). Révision proposée au point R5.

---

## 12. Validation, points de vigilance et mise en œuvre (26/09/2026)

**Décision de l'utilisateur :** toutes les propositions des sections 8, 10 et 11 sont validées (P1 à P5, P7, P8 ; Q2 à Q12), avec trois points de vigilance (V1 à V3). Pour Q10, l'option retenue est la création de `obj5/`.

### 12.1 Points de vigilance

| #  | Point                                                                   | Application                                                                                                                                                                                                                          |
| -- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| V1 | P4 : la valeur du T4 pour l'annuel est une convention, pas une moyenne | Documentée dans le 03 (sections 2, 8, 9 et 11). Contrôle de saisonnalité ci-dessous. Variante « moyenne des 4 trimestres » en test de sensibilité à l'étape d'analyse. Convention limitée aux stocks ; les flux s'additionnent        |
| V2 | P2 : la stagnation reste non traitée                                    | Le 03 dit en toutes lettres (sections 1, 10 et 11) que la stagnation n'est pas repérée avec le seuil actuel et que cette partie de l'objectif 1 n'est pas résolue. La classe « ralentissement » sera proposée à l'étape d'analyse ; le 02 n'est pas modifié |
| V3 | P3 : l'écart de 12 % entre D1 et le RGPH                                | Encadré « Dénominateurs : trois bases coexistent » en section 9 du 03 ; O1-03 compare des nombres                                                                                                                                  |

**V1 — contrôle sur les abonnements data mobile** (total 2G/3G/4G de l'ARCEP, dernière publication de chaque trimestre ; extraction limitée à cette série, l'extraction complète de AR1 restant à l'étape de préparation, P5) :

| Année | T4        | Moyenne des 4 trimestres | T4 / moyenne | Croissance (T4) | Croissance (moyenne) |
| ----- | --------- | ------------------------ | ------------ | --------------- | -------------------- |
| 2018  | 3 660 055 | 3 251 284                | +12,6 %      | —               | —                    |
| 2019  | 4 671 179 | 4 365 978                | +7,0 %       | +27,6 %         | +34,3 %              |
| 2020  | 4 891 899 | 4 587 932                | +6,6 %       | +4,7 %          | +5,1 %               |
| 2021  | 4 651 596 | 4 561 199                | +2,0 %       | -4,9 %          | -0,6 %               |
| 2022  | 4 870 282 | 4 783 747                | +1,8 %       | +4,7 %          | +4,9 %               |
| 2023  | 5 281 504 | 5 029 816                | +5,0 %       | +8,4 %          | +5,1 %               |
| 2024  | 5 624 336 | 5 622 894                | +0,0 %       | +6,5 %          | +11,8 %              |
| 2025  | 6 346 056 | 6 126 342                | +3,6 %       | +12,8 %         | +9,0 %               |

- **Pas de pic saisonnier systématique au T4.** Rapporté à la moyenne du T3 et du T1 suivant, le T4 va de -2,9 % (2024) à +6,9 % (2020) ; il est inférieur 4 années sur 8 (2018, 2023, 2024, 2025).
- **Les deux conventions ne donnent pourtant pas la même lecture.** Le T4 dépasse la moyenne annuelle de 0 à 12,6 %, parce que le stock croît en cours d'année. Les croissances divergent en 2021 (-4,9 % contre -0,6 % : régression d'un côté, |g| < 2 % de l'autre), 2023, 2024 et 2025. Le test de sensibilité est donc nécessaire. Proposition pour l'étape d'analyse : une année n'est classée que si les deux conventions concordent, sinon elle est signalée « dépend de la convention » (point R6).
- **Le 02 autorise un calcul trimestriel de O1-02** (« trimestriel si la donnée l'est ») : à partir de 2018, un glissement annuel trimestre par trimestre (T / T-4) évite toute convention annuelle.
- **Flux.** Dans AR1, le CA et l'investissement sont trimestriels (CA du secteur : 67,46 Md FCFA au T4 2025). L'annuel est la somme des 4 trimestres, jamais le T4. L'investissement est très concentré en fin d'année : 23,6 Md FCFA au T4 2025, soit 55 % de l'année (43,1 Md). Pour un flux, le T4 serait donc trompeur.
- **Révision ARCEP de 2021** confirmée sur les 4 trimestres : de -13,4 % (T2) à -21,2 % (T4) entre la première publication et celle de 2022.
- **Rupture de périmètre** : à partir du T2 2025, le CA de Togo Telecom intègre la voix fixe et la data fixe, et exclut la location d'infrastructures (note de l'observatoire du T4 2025).

**V3 — les dénominateurs**

| Base                                                        | Population 2022 | Écart au RGPH | 15 ans et plus en 2022                                                              | Usage                                                                                   |
| ----------------------------------------------------------- | --------------- | ------------- | ----------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Banque mondiale (implicite de 3f ; base vraisemblable de D1) | 9,09 M          | +12 %         | —                                                                                   | D1 tel que publié ; taux de l'UIT                                                       |
| IN1 (projections de l'INSEED)                               | 8 068 000       | -0,3 %        | 5 032 000 (62,4 %)                                                                  | Taux nationaux annuels calculés par nous ; base des taux de l'ARCEP                      |
| RGPH-5 (D6, RG2, RG3)                                       | 8 095 498       | —             | 4 707 386 hors âge non déclaré (58,3 % des âges connus ; environ 4 721 000 si les 24 180 « ND » sont répartis) | Tous les ratios territoriaux (objectifs 3 et 4) ; 15 ans et plus par préfecture et commune |

- **IN1 est juste sur le total, pas sur la structure par âge** : ses 15 ans et plus dépassent le recensement de **6,6 %** en 2022. Un ratio « par adulte » calculé avec IN1 n'est pas comparable à un ratio calculé avec le RGPH (point R2).
- Deux autres bases existent, sans servir de dénominateur : l'implicite INSEED de D2 et D3 (7,62 M en 2019) et la base des indicateurs geodata (environ 8,14 M).
- Les taux d'enquête sont calculés dans l'échantillon pondéré. Les poids de l'EHCVM 2021/22 totalisent 8,095 M, calés sur le RGPH-5 (Grand Lomé : 2,188 M, contre 2 188 376 au recensement) ; ceux de 2018/19 totalisent 7,663 M.

### 12.2 Téléchargements (Q11) : 44 fichiers, aucun échec

| Dossier | Fichiers                                                                                                                                                                                                                                 |
| ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `obj1/` | AS1 : annuaire statistique national 2024 (776 p.)                                                                                                                                                                                         |
| `obj2/` | IT1 : paniers de prix TIC de l'UIT 2008-2025 (xlsx) ; AR2 : rapport d'activité ARCEP 2025 (sites BTS par opérateur et par technologie, tableau 12)                                                                                          |
| `obj3/` | BC1 : BCEAO, services financiers numériques 2024 ; TF1 : 5 instantanés HTML du 26/09/2026 (retrait et transfert Flooz, page Mixx by Yas, grilles momocalc en contrôle) ; GD1 : agences de la Poste (95 points)                          |
| `obj4/` | RG1 à RG3 : livrets 01 à 03 du RGPH-5 ; CO1 : OCHA, population 2021 par préfecture (contrôle) ; AS2 : annuaires régionaux 2024 (Maritime, Centrale, Kara, Savanes ; **celui des Plateaux n'est pas publié**) ; BC2 : BCEAO, rapport sur l'inclusion financière 2024 et tableau de bord 2024 (le second via le lien WeTransfer publié par la BCEAO) |
| `obj5/` | GD2 : 1 078 marchés (polygones), 15 454 établissements scolaires, 2 271 formations sanitaires, 1 576 établissements administratifs de 21 ministères (dont 903 pour le MATDDT, avec les centres d'état civil)                              |

Types vérifiés (PDF, xlsx, HTML, GeoJSON lisibles). Manifeste : 132 lignes (131 « ok » ; 1 échec déjà connu, AR6). `data/raw/_extradatas/README.md` mis à jour.

### 12.3 Transcription des livrets 02 et 03 du RGPH-5 (Q2)

| Fichier dérivé (`obj4/RG_rgph5_livrets/`)                                 | Contenu                                                                                                                       |
| ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `RG2_rgph5_population-age-milieu-sexe_national-regions-prefectures.csv`   | 47 tableaux (national ; Maritime avec et sans Grand Lomé ; Grand Lomé ; 4 autres régions ; 39 préfectures) x 21 lignes d'âge x 9 colonnes : 8 883 lignes |
| `RG3_rgph5_population-age-milieu-sexe_communes.csv`                       | 117 communes, avec leur préfecture et leur région : 22 113 lignes                                                              |
| `RG_rgph5_ecarts-internes-livrets.csv`                                    | Écarts internes relevés par les contrôles                                                                                     |

**Contrôles**

- **Hiérarchie exacte** : les préfectures somment exactement à leur région, les régions au national (8 095 498), et les communes à leur préfecture, cellule par cellule.
- **Égalité avec D6** : 39 préfectures sur 39. Les 117 communes aussi, une fois corrigées les anomalies de libellés de D6, ce qui **confirme** les corrections d'Amou 3 et d'Est-Mono 3 déduites de l'ordre des lignes (11.A14) et « BINAH2 ».
- **Danyi** : RG3 sépare Danyi 1 (25 820) et Danyi 2 (14 420), fusionnées dans D6 (40 240).
- **Écarts internes** : 24 cellules, écart de 1 ou 2 personnes. Ils viennent **tous d'une seule erreur de saisie**, les hommes ruraux de 25-29 ans et de 85 ans et plus de la commune de Doufelgou 3 (1 personne chacun), propagée à la préfecture, à la Kara et au national. Les valeurs sont transcrites telles que publiées, sans correction.
- **Titre erroné** : le tableau 100 du livret 03 est intitulé « Binah 2 », mais la page annonce « Commune de Binah 1 » et son total (44 039) est celui de Binah 1 dans D6. Il est transcrit sous le nom de Binah 1.
- **Jointure** : les 117 communes et les 39 préfectures se joignent aux noms de geodata (D4, 4c, D5) sans aucune correction.
- **Repères** : 15 ans et plus : 4 707 386 hors âge non déclaré ; part urbaine : 42,9 %. Un « - » du livret est transcrit 0 : les contrôles urbain + rural = total le confirment.
- RG1 (cantons) est téléchargé ; sa transcription vient en second temps (Q2).

### 12.4 Vérifications

- **Q9, définition BCEAO** : taux global de pénétration démographique (TGPSFd) = nombre total de points de services financiers / population adulte x 10 000. Les points comptés sont les guichets bancaires, de microfinance, de la Poste, du Trésor et des caisses d'épargne, **plus les points de services de monnaie électronique actifs** (y compris TPE et GAB/DAB), soit **99 % du total** dans l'UEMOA.
  - Togo : 116 pour 10 000 adultes en 2024 (UEMOA : 193) ; série 2014-2024 (4, 8, 11, 35, 33, 37, 50, 67, 75, 104, 116). Le « +131 » cité par la presse (section 9.5, BC2) est en fait la pénétration **géographique** (963 puis 1 094 points pour 1 000 km², plus forte hausse de l'UEMOA en 2024) ; la pénétration démographique du Togo progresse de 12 points.
  - **Non comparable à O4-02**, qui ne compte que des points formels.
  - Le tableau de bord ventile pourtant par pays : Togo, 629 points bancaires, 625 points de microfinance, 81 137 points de monnaie électronique dont 65 043 actifs (80,2 %). Point R1.
  - Ordre de grandeur : les points de D4, 4c et D5 (ces derniers comptés par opérateur, environ 32 400), rapportés aux 15 ans et plus du RGPH, donnent environ 71 pour 10 000 adultes, entre les valeurs 2021 (67) et 2022 (75) de la BCEAO, cohérent avec la date PRISE 2021/2022.
- **BC1** : les chiffres de la presse sont confirmés pour le Togo en 2024 : 12 553 441 comptes ouverts ; 6 069 075 actifs à 90 jours (48,35 %) ; 81 137 points de service, dont 65 043 actifs.
- **TF1, grilles** :
  - Retrait Flooz (officiel) : 14 tranches, de 50 F (jusqu'à 500 F) à 1 000 F (de 50 001 à 100 000 F), puis en fourchette au-delà.
  - Transfert Flooz : gratuit jusqu'au 3e transfert national.
  - Mixx : 6 premiers transferts du jour gratuits, puis 1 % ; **aucune grille de retrait officielle publiée**. momocalc donne 50 F (jusqu'à 500 F), 100 F (501 à 5 000 F), 300 F (5 001 à 20 000 F), 600 F (20 001 à 50 000 F), et une taxe de 10 % sur les frais depuis le 01/01/2024 (à vérifier). Point R3.
- **GD1** : 95 agences de la Poste, dont 84 « Utilisé », dans 38 préfectures ; même effectif que l'indicateur geodata de 4j.
- **GD2** : les marchés sont des **polygones**, pas des points (centroïde à calculer). Les établissements scolaires comprennent 8 165 écoles primaires, 4 277 jardins d'enfants, 2 304 collèges et 708 lycées. Toutes les couches ont les noms de la région au canton (campagne PRISE).
- **EHCVM, Q12** : les 540 grappes sont **identiques** dans les deux vagues (panel de grappes, document d'information de base 2021/22) et gardent leur région. Les 98 grappes « Lomé commune » de 2018/19 sont exactement les 98 grappes « Grand Lomé » de 2021/22 : **seul le libellé change**. Les poids sont calés sur deux bases différentes (7,663 M et 8,095 M). Strates : région x milieu ; erreur relative de 2,8 à 5,1 % par région (consommation). Point R5.

### 12.5 Nouveaux points à trancher

| #  | Question                                             | Proposition                                                                                                                                                                                                                                                  |
| -- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| R1 | Repère UEMOA de O4-02 (B11), après Q9                | Le TGPSFd de la BCEAO compte surtout du mobile money : ne pas l'utiliser pour O4-02. Repère des points formels : FAS (agences et DAB pour 100 000 adultes) des 8 pays de l'UEMOA par l'API de la Banque mondiale (C5 du 03), qui est le standard cité par le 02. Le TGPSFd sert seulement de repère à une variante « tous points de service, mobile money compris » |
| R2 | Dénominateur « adultes » (IN1 : +6,6 % sur les 15 ans et plus en 2022) | RGPH-5 (RG2, RG3) pour tout ratio par adulte en 2022 et pour tout ratio territorial ; IN1 seulement pour les séries nationales annuelles, jamais dans le même tableau que le RGPH. Findex et BCEAO : taux repris tels que publiés, avec leur propre base |
| R3 | Coût du mobile money (O3-06) sans grille officielle de retrait pour Mixx | O3-06 calculé sur la grille officielle de Flooz. Mixx : « grille officielle non publiée » ; la grille momocalc n'apparaît qu'en note, en contrôle (Q8)                                                                                                     |
| R4 | Population des communes : RG3 ou D6 ?                | **RG3 et RG2** comme source de population des objectifs 3 et 4 : mêmes totaux que D6, Danyi 1 et 2 séparées, noms joints sans correction, âge et milieu disponibles. D6 garde un rôle de contrôle. Cela modifie 11.A14 : Danyi n'a plus à être regroupée |
| R5 | Q12 révisé                                           | Comparer les deux EHCVM sur les 6 domaines, Grand Lomé compris, en signalant le changement de libellé et le calage des poids sur deux bases                                                                                                             |
| R6 | Lecture de O1-02 sur les abonnements (V1)            | Classer une année seulement si la convention du T4 et la moyenne des 4 trimestres concordent ; sinon, « dépend de la convention ». À partir de 2018, ajouter le glissement trimestriel (T / T-4), que le 02 autorise                                   |

**Décision (26/09/2026) : R1 à R6 validés**, avec les précisions de l'utilisateur (section 13).

---

## 13. Décisions R1 à R6 et report dans le 03 et l'inventaire (26/09/2026)

### 13.1 Décisions

| #  | Décision                                                                                                                                                                                                                                                                                  | Justification retenue                                                                                                                                                                                                                                                                                             | À tracer dans le 03                                                                                                                                                                  |
| -- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| R1 | **O4-02 utilise le FAS** (agences et DAB pour 100 000 adultes) des 8 pays de l'UEMOA, par l'API de la Banque mondiale (C5 du 03). Le taux de la BCEAO (TGPSFd) sert seulement de repère à une variante « tous points de service, mobile money compris », qui **n'est pas O4-02** | Le TGPSFd compte les points de monnaie électronique actifs : 99 % des points dans l'UEMOA, et environ 98 % pour le Togo en 2024 (65 043 points actifs, face à 629 points bancaires et 625 de microfinance). O4-02 ne compte que des points formels : le comparer au TGPSFd serait une erreur de définition | La distinction entre les deux définitions, et pourquoi O4-02 utilise le FAS : sections 9 et 10 (O4-02), fiche BC2 (section 12), section 11 (B11, C5)                    |
| R2 | **RGPH-5 (RG2, RG3)** pour tout ratio par adulte en 2022 et pour tout ratio territorial ; **IN1** seulement pour les séries nationales annuelles, là où le RGPH n'existe pas ; **Findex et BCEAO** repris tels que publiés, avec leur propre base | IN1 dépasse le RGPH de 6,6 % sur les 15 ans et plus en 2022 (5 032 000 contre environ 4 721 000), alors qu'il est juste sur le total (-0,3 %). Deux ratios « par adulte » calculés sur ces deux bases ne sont pas comparables                                                                           | L'encadré « Dénominateurs » (section 9) énonce la règle, pas seulement les trois bases ; section 6 (D6), section 11 (A16)                                                         |
| R3 | **O3-06 est calculé sur la grille officielle de Flooz** (14 tranches). Pour Mixx, il est partiel : conditions de transfert officielles (6 transferts gratuits par jour, puis 1 %), mais **grille officielle de retrait non publiée** ; la grille de momocalc n'apparaît qu'en note, en contrôle | Q8 : sources officielles seulement, l'agrégateur en contrôle. Le libellé de l'indicateur doit dire « Flooz : calculable ; Mixx : partiel, grille de retrait non publiée »                                                                                                                                  | Section 10 (O3-06), fiche TF1 (section 12), section 11                                                                                                                                 |
| R4 | **RG2 et RG3 sont la source de population des objectifs 3 et 4** ; D6 garde un rôle de contrôle. **11.A14 est révisé** : Danyi 1 et Danyi 2 ne sont plus regroupées                                                                                                             | Totaux identiques à D6 (contrôle exact) ; Danyi séparées (D6 les fusionne) ; noms joints sans correction (D6 en demande) ; âge et milieu disponibles (D6 n'a que le total)                                                                                                                          | Section 6 (D6), section 7 (jointures), section 10 (dénominateurs des indicateurs des objectifs 3 et 4), section 11 (A14)                                                        |
| R5 | **Q12 est révisé** : les deux vagues de l'EHCVM se comparent sur les **6 domaines**, Grand Lomé compris, en signalant le changement de libellé et le calage des poids sur deux bases (7,663 M et 8,095 M)                                                                            | Les 540 grappes sont identiques d'une vague à l'autre et gardent leur région ; les 98 grappes « Lomé commune » de 2018/19 sont exactement les 98 grappes « Grand Lomé » de 2021/22                                                                                                                   | Section 11 (Q12 révisé, avec la justification) ; fiche W2 (section 12)                                                                                                              |
| R6 | **O1-02 sur les abonnements** : une année n'est classée que si les deux conventions (valeur du T4, moyenne des 4 trimestres) concordent ; sinon, elle est marquée « dépend de la convention ». À partir de 2018, le glissement trimestriel (T / T-4), que le 02 autorise, s'ajoute | Le contrôle V1 montre que les deux conventions divergent en 2021, 2023, 2024 et 2025. Classer une année sans vérifier la concordance serait fragile                                                                                                                                                  | Section 8 (temporalité) : règle pour O1-02 ; section 10 (O1-02) ; section 11                                                                                                          |

**Précision sur R1.** Le chiffre de 81 137 cité à la validation est le total des points de monnaie électronique du Togo, actifs ou non. Le TGPSFd ne compte que les points **actifs** (65 043). La conclusion ne change pas : pour le Togo, environ 98 % des points comptés par la BCEAO sont des points de monnaie électronique.

### 13.2 Corrections relevées à la relecture (26/09/2026)

- **03, section 12 (IN1)** : « les tranches somment au total à 1 000 près » est inexact. L'écart va de -2 000 à +2 000 selon l'année (section 2 : « à 2 000 près »). *Corrigé le 26/09/2026.*
- **Ce journal, sections 5 et 9** : les mentions « à vérifier », « non vérifié » et « non téléchargé » portent désormais un renvoi vers la vérification faite (sections 7, 11 et 12.4).

### 13.3 Report dans le 03 et l'inventaire (feu vert donné et réalisé le 26/09/2026)

**Réalisé le 26/09/2026**, selon le plan ci-dessous, avec deux écarts : les micro-données MICS6 (W1) sont déclarées « non obtenues » dans la fiche W1, pas dans la liste des statuts « Partiel » du récapitulatif ; le repère de O1-01 que C5 devait aussi couvrir n'a pas été téléchargé (point S1, section 14).

**Dans `03_data_understanding.md`**, qui intègre déjà les décisions jusqu'à la section 12 de ce journal :

- R1 à R6 : passer la partie 11.E de « à valider » à « validé le 26/09/2026 », et reporter chaque décision aux endroits listés en 13.1 ;
- la correction d'IN1 (13.2).

**Dans `_INVENTORY_datasets.txt`**, qui ne couvre aujourd'hui que les fichiers de `data/raw/` hors `_extradatas` :

- **En-tête** : ajouter les compléments hors portail (`data/raw/_extradatas/`, validés le 26/09/2026) et leur traçabilité (`_MANIFEST.csv`, SHA-256). Réviser la convention « Aucune source extérieure au projet n'a été consultée, sauf l'API de la Banque mondiale », que D-6 et D-13 rendent caduque.
- **Récapitulatif** : un second bloc, avec une ligne par référence (BM1 à GD2, soit environ 30 lignes, pas 131), sa famille de données du 02, son nombre de lignes et de colonnes quand le fichier est tabulaire, et son statut (Disponible, Partiel, Absent).
- **Fiches** : une fiche par référence, au format des fiches existantes (source, famille, description, format, période, niveau géographique, lignes, colonnes, millésime, licence, statut, remarques, URL). Pour une référence à plusieurs fichiers (AR1 : 34 PDF), l'empreinte renvoie au manifeste.
- **Statut « Absent »** : campagne QoS du 2e semestre 2023 (AR6), annuaire 2024 des Plateaux (AS2), grille de retrait officielle de Mixx (TF1), micro-données MICS6 (W1).
- **Micro-données** (W2, W3) : fichiers listés, avec la mention des conditions d'utilisation et du `.gitignore`. Aucune variable individuelle n'est reproduite.

---

## 14. Relecture complète : bilan et points encore ouverts (26/09/2026)

### 14.1 Bilan

- **Décisions** : chaque point soumis dans ce journal a reçu une décision (D-1 à D-18, P1 à P8, Q1 à Q12, V1 à V3, R1 à R6). Les points A2 à A13, A18 à A21, C1, C2, C6 et C7 sont dans la section 11 du 03, pas dans ce journal : ils restent au stade de proposition.
- **Inventaire** : les 30 références du manifeste (133 fichiers) ont chacune une ligne dans le récapitulatif et une fiche. Pour les références à plusieurs fichiers (AR1, AR6, W2, W4, GD2), la fiche décrit le lot et renvoie au manifeste pour le détail, fichier par fichier.

**Correspondance manque → jeux retenus → inventaire**

| Obj. | Manque                                                    | Jeux retenus                                                   | Inventaire |
| ---- | --------------------------------------------------------- | -------------------------------------------------------------- | ---------- |
| 1    | Chronologie (B6, O1-02)                                   | CH1, construit à partir de AR2, AR3, AR4, MS1, IN2, IN3        | ✅          |
| 1    | Population annuelle ; 15 ans et plus national (B5, B1)    | IN1                                                            | ✅          |
| 1    | Abonnements par technologie après 2019 (B7, O1-04)        | AR1                                                            | ✅          |
| 1    | Usage par territoire (O1-05)                              | W1, W2, W4                                                     | ✅          |
| 1    | Alphabétisation, compétences, smartphone (O1-06)          | W1, W2, W3                                                     | ✅          |
| 1    | Point mesuré 2020 ; contexte                              | AS1 ; BM1 à BM3, BM7                                           | ✅          |
| 1    | **Repère Afrique subsaharienne (B11, O1-01)**             | **Aucun** : C5 n'a porté que sur le FAS                        | ❌ (S1)     |
| 2    | CA et investissement par opérateur (O2-02, O2-04)         | AR1                                                            | ✅          |
| 2    | Coût de 1 Go (O2-05)                                      | IT1, AR5, AR6                                                  | ✅          |
| 2    | Couverture par territoire (O2-06)                         | Proxy 3i ; W2 (module communautaire) ; OC1 non téléchargé (Q6) | ✅ (proxy)  |
| 2    | Sites radio (O2-08)                                       | AR2 (rapport 2025), national                                   | ✅          |
| 2    | Qualité de service (O2-09)                                | AR6 (une étude manquante) ; W7 non téléchargé (D-18)           | Partiel    |
| 3    | Milieu urbain / rural par territoire (B3)                 | RG2, RG3                                                       | ✅          |
| 3    | La Poste comme point formel (O3-01, Q5)                   | GD1                                                            | ✅          |
| 3    | Points de vente, comptes, transactions (O3-03, O3-04)     | AR1, BC1                                                       | ✅          |
| 3    | Mobile money par territoire (O3-05)                       | W4 (vagues 9 et 10), W3 (urbain / rural)                       | ✅          |
| 3    | Coût du mobile money (O3-06)                              | TF1 (Mixx partiel, R3)                                         | Partiel    |
| 4    | 15 ans et plus par territoire (B1)                        | RG2, RG3 ; CO1 et AS2 en contrôle                              | ✅          |
| 4    | Repère UEMOA (B11, O4-02)                                 | C5 ; BC2 pour la variante « tous points » (R1)                 | ✅          |
| 4    | Électricité par préfecture                                | IN4                                                            | ✅          |
| 5    | Lieux candidats (B12)                                     | GD2                                                            | ✅          |

### 14.2 Erreurs corrigées à la relecture

- **Fiche C5** (03, section 12 ; inventaire) : le Togo est **2e sur 8** pour les agences en 2024, pas 4e ; la médiane des agences est de 3,82, pas 3,83. La **moyenne** des 8 pays (3,52 agences, 5,15 DAB) est ajoutée, puisque le 02 demande « la moyenne UEMOA ».
- **03, section 11, B11** : « Le repère UEMOA de O4-02 reste à choisir » était périmé depuis R1 (report prévu en 13.1 et oublié). Remplacé, avec la mention que le repère de O1-01 n'est pas en main.
- **03, section 10, O1-01** : « Repère Afrique subsaharienne : 11.C5 » laissait croire le repère disponible. Remplacé par « pas encore en main ».

### 14.3 Points restés sans décision

| #   | Question                                        | Constat                                                                                                                                                                                                                                                  | Proposition                                                                                                                                                                                                                                                  |
| --- | ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| S1  | Repère Afrique subsaharienne de O1-01 (B11)     | Le 02 compare O1-01 à « la moyenne Afrique subsaharienne de l'année ». C5 prévoyait d'interroger l'API sur les codes déjà utilisés, mais seul le FAS a été téléchargé. La méthode (étape 03) exige le benchmark externe ici, « jamais plus tard ». W3 contient l'agrégat « Sub-Saharan Africa », pour 2024 seulement et avec la définition du Findex (15 ans et plus) | Télécharger par l'API IT.NET.USER.ZS pour l'agrégat Afrique subsaharienne (SSF) et les 8 pays de l'UEMOA : même source et même estimation UIT que 1b. W3 en complément pour 2024, libellé avec sa définition. **Nouveau fichier : à valider** |
| S2  | O4-02 : moyenne ou médiane de l'UEMOA           | Le 02 dit « moyenne UEMOA » ; le 03 n'affichait que la médiane                                                                                                                                                                                           | La moyenne, comme le 02 (3,52 agences, 5,15 DAB pour 100 000 adultes en 2024) ; la médiane en complément                                                                                                                                                     |
| S3  | O4-02 : périmètre du repère UEMOA                | Le FAS compte des agences bancaires et des **appareils** DAB. D4 compte des **sites** de DAB, et A19 (proposition du 03) exclut toute comparaison directe avec des appareils. IMF, assurances et Poste n'ont aucun repère FAS                           | Territoires comparés au repère UEMOA pour les agences bancaires seulement. DAB : comparaison UEMOA au niveau national (appareils contre appareils : 4f contre C5), territoires comparés à la médiane nationale. IMF, assurances, Poste : médiane nationale, « pas de repère UEMOA » |
| S4  | O4-02 : échelle                                 | FAS pour 100 000 adultes ; 02 pour 10 000                                                                                                                                                                                                                | Diviser par 10 à l'affichage, l'échelle d'origine en note                                                                                                                                                                                                    |
| S5  | Âge non déclaré dans les 15 ans et plus         | 24 180 personnes ; le 03 donne deux valeurs (4 707 386 hors non déclarés ; environ 4 721 000 avec répartition) sans règle                                                                                                                              | Convention : répartir les non déclarés au prorata, dans chaque territoire ; variante « hors non déclarés » en test de sensibilité (écart national : 0,3 %)                                                                                                    |
| S6  | Rupture ARCEP entre le T4 2019 et le T1 2020    | 3G de Togocel : -58 %, pendant que la 4G progresse ; « reclassement probable, non documenté »                                                                                                                                                             | O1-04 : traiter comme une rupture de série, aucune évolution par technologie calculée à travers ; chercher la note de méthode pendant l'extraction de AR1 (P5)                                                                                                |
| S7  | IN3 : +15 % entre décembre 2019 et décembre 2020 | Hausse réelle ou changement de méthode, jamais vérifié                                                                                                                                                                                                  | Vérifier à l'étape de qualité (documentation de l'INSEED) ; en attendant, ne pas annoter 2020 comme une hausse des prix dans la chronologie                                                                                                                  |
| S8  | GD3 et BM8, jamais soumis au vote               | GD3 (section 9.3) : électricité et villages par territoire, dans le découpage actuel, alors que IN4 suit l'ancien découpage avec des préfectures regroupées. BM8 (section 9.2) : revenu par habitant en PPA                                        | GD3 : télécharger (contexte des objectifs 4 et 5). BM8 : écarter, IT1 donne déjà le coût de 1 Go en % du RNB                                                                                                                                                  |
| S9  | Actions validées mais non faites                | D-14 : micro-données MICS6 (compte mics.unicef.org). D-17 : tableaux d'équipement du RGPH-5 à demander à l'INSEED ; EDS-IV à suivre. D-18 : Ookla « à examiner avec O2-09 ». Q6 : OpenCellID si une clé est créée                                     | MICS6 : abandonner, la transcription des tableaux régionaux suffit. RGPH-5 : demande à faire par toi, hors du chemin critique. EDS-IV : à suivre. Ookla et OpenCellID : ne pas les ajouter ; O2-09 et O2-06 restent ⚠️ et le 03 le dit                        |
| S10 | RG1 (cantons)                                   | Transcription prévue « en second temps » (Q2)                                                                                                                                                                                                           | Inutile pour les étapes 04 à 10 (le 02 s'arrête à la commune) ; à reprendre à l'étape 11 seulement si le ciblage descend au canton                                                                                                                            |

**Hors de ce vote** (déjà décidés, avec une étape fixée) : extraction de AR1 en table (P5, préparation) ; classe « ralentissement » (P2, analyse) ; A11 (étape du score).

**Décision (26/09/2026) : S1 à S10 validés**, avec deux nuances : **S8**, GD3 est téléchargé à l'étape de préparation, pas maintenant (BM8 écarté définitivement) ; **S9**, le 03 doit dire en toutes lettres que O2-09 (optionnel) n'est pas couvert et pourquoi. S1 est à traiter avant de figer le 03. Mise en œuvre : section 15.

---

## 15. Mise en œuvre de S1 à S10 (26/09/2026)

### 15.1 S1 : repère Afrique subsaharienne téléchargé (C5b)

- **Fichier** : `data/raw/_extradatas/obj1/C5b_worldbank-uit-internet-afrique-subsaharienne-uemoa.csv` (221 lignes, 7 colonnes, 25 649 octets, SHA-256 `65b243b6…`), ajouté au manifeste (134 lignes : 133 « ok », 1 échec connu).
- **Requête** : IT.NET.USER.ZS pour l'agrégat SSF et les 8 pays de l'UEMOA, 2000-2025, avec les notes de source (`footnote=y`). Base WDI mise à jour le 13/07/2026. Méthode d'agrégation : moyenne pondérée (métadonnées de la Banque mondiale).
- **Contrôle** : la série du Togo est identique, année par année, à celle de D1 (version API, P1).
- **Résultat** :

| Année | Togo    | Afrique subsaharienne | Écart (points) |
| ----- | ------- | --------------------- | -------------- |
| 2015  | 7,12 %  | 16,2 %                | -9,1           |
| 2017  | 12,36 % | 20,0 %                | -7,6           |
| 2019  | 20,73 % | 24,4 %                | -3,7           |
| 2020  | 29,02 % | 26,7 %                | +2,3           |
| 2022  | 35,61 % | 31,1 %                | +4,5           |
| 2024  | 39,48 % | 33,6 %                | +5,9           |

- Le Togo passe au-dessus de la moyenne régionale en 2020, l'année du saut de +8,3 points de son estimation. Les deux séries sont des estimations de l'UIT : c'est une comparaison de niveau C, à lire avec les points mesurés (D-15). UEMOA : Togo 6e sur 8 en 2017, 4e en 2020, 3e en 2024 (moyenne simple des 8 pays en 2024 : 35,7 %).

### 15.2 Report des autres décisions

| #   | Où                                                                                                                                                                  |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| S1  | 03 : bandeau, section 10 (O1-01, trois couches), 11.B11, 11.C5, 12 (fiche C5b, vue d'ensemble) ; inventaire : en-tête, récapitulatif, fiche C5b ; README ; manifeste |
| S2 à S4 | 03 : section 9 (tableau des sources), section 10 (O4-02), 11.A19, 12 (C5) ; inventaire : fiche C5                                                                                               |
| S5  | 03 : encadré « Dénominateurs » (section 9), section 10 (O4-02, O4-04), 12 (population)                                                                               |
| S6  | 03 : section 10 (O1-04), 12 (AR1)                                                                                                                                   |
| S7  | 03 : section 12 (prix, contexte) ; CH1 : l'événement IN3 de 2020 passe du type « tarif » au type « statistique », libellé revu (8 188 octets, SHA-256 `44231aaa…`, manifeste mis à jour) ; inventaire : fiches IN3 et CH1 |
| S8  | 03 : partie F de la section 11 ; README (GD3 reporté, BM8 écarté)                                                                                                    |
| S9  | 03 : section 10 (O2-06, O2-09, « ce qui ne bouge pas »), 12 (enquêtes, réseau) ; inventaire : fiche W1 ; README                                                      |
| S10 | 03 : section 12 (population), 11.D (Q2 à Q4) ; inventaire : fiche RG1 ; README                                                                                      |

Le 03 a une partie F (« Décisions S1 à S10 ») dans sa section 11, sur le modèle de la partie E.

### 15.3 Constats et corrections faits pendant le report

- **Campagnes QoS de l'ARCEP : 84 ou 94 localités.** Les « 84 localités de 36 préfectures » (sections 4 et 9.4 de ce journal, puis le 03 et l'inventaire) sont celles des **deux campagnes de 2025**, connues seulement par le rapport d'activité 2025. La campagne 2024 téléchargée (AR6) porte sur **94 localités** (dont les 39 chefs-lieux de préfecture, région des Savanes exclue). Elle publie des taux de conformité pour le Grand Lomé et le reste du pays, sans valeur par localité. Les analyses QoE (nPerf) sont nationales, par opérateur. **O2-09 n'est donc couvert qu'au niveau national**, ce qui confirme S9. Corrigé dans le 03 et l'inventaire.
- **Module communautaire de l'EHCVM** : la réception du réseau y est **déclarée** par les informateurs de la localité, pas mesurée. Le 03 disait « réception mesurée » à trois endroits : corrigé.
- **Rupture du T1 2020 (S6)** : le total data mobile recule lui aussi au même trimestre (4 671 179 au T4 2019, 4 362 555 au T1 2020, -6,6 %), seul recul trimestriel de 2018-2020. La rupture ne se limite donc peut-être pas à un reclassement entre technologies. Le 03 le signale, sans l'interpréter.
- **O2-09 selon le 02** : si O2-09 est indisponible, « la couverture reste théorique et le tableau de bord l'affiche en toutes lettres », et un territoire sans mesure est « Non déterminable ». Le 03 reprend ces deux règles (O2-06, O2-09).
- **Nuance sur la validation de S9** : les campagnes de l'ARCEP sont de vraies mesures (drive tests), mais elles ne donnent pas de valeur par territoire. Ce qui manque est une mesure **territoriale**, pas toute mesure.

### 15.4 État après report

- **Plus aucun point de ce journal n'est ouvert.**
- **Restent dans la section 11 du 03**, au stade de proposition : A2 à A13, A18, A20, A21, C1, C2, C6, C7. A19 est appliqué à O4-02 par S3.
- **Décidés, avec une étape fixée** : extraction de AR1 (P5, préparation) ; GD3 (S8, préparation) ; vérification du saut de IN3 (S7, étape 05) ; classe « ralentissement » (P2, analyse) ; A11 (étape du score) ; RG1 (S10, étape 11 si besoin) ; demande à l'INSEED (S9, utilisateur).

---

## 16. Restructuration du 03 à la demande de l'utilisateur (26/09/2026)

**Demande** : dans chaque section de D1 à D6, ajouter après les limites les données complémentaires téléchargées, et pour quel objectif, sans perdre le plan initial ; clarifier la partie C de la section 11, qui semblait annoncer des téléchargements encore à faire.

### 16.1 Blocs « Données complémentaires téléchargées » (sections 1 à 6 du 03)

- **Placement** : à la fin de chaque section, après les dernières limites (celles du jeu et de ses compléments du portail) : le plan initial est inchangé. Sommaire, bandeau et introduction mis à jour.
- **Contenu de chaque bloc** : un tableau (référence, fichier ou dossier dans `_extradatas`, ce qu'il apporte face aux limites du jeu, indicateurs du 02, niveau de preuve), puis deux listes : « Ce que ces compléments règlent » et « **Ce qui reste non résolu** ».
- **Répartition** : D1 → objectif 1 (C5b, W1 à W4, AS1, CH1, IN1 à IN3, BM) ; D2 → objectifs 1 et 2 (AR1, IN1, AS1, CH1) ; D3 → objectif 2 (AR1, AR2, IT1, AR5, AR6, IN2, IN3, W2 communautaire) ; D4 → objectifs 3, 4 et 5 (GD1, RG2, RG3, C5, BC2, W2, W4, IN4, GD2) ; D5 → objectifs 3 et 4 (AR1, BC1, BC2, TF1, W3, W4, RG2, RG3) ; D6 → dénominateurs (RG1 à RG3, IN1, CO1, AS2). Les 31 références du manifeste figurent toutes dans au moins un bloc.
- **Écart avec la demande** : l'intitulé ne dit pas « affiner à 100 % la résolution ». Aucun objectif n'est résolu à 100 % : la stagnation (objectif 1), la couverture mesurée et la qualité de service par territoire (objectif 2), les agents actifs par territoire (objectif 3) restent non résolus. Chaque bloc le dit dans sa dernière liste.

### 16.2 Partie C de la section 11

- **Constat** : aucun téléchargement décidé n'est en attente. C3, C4 et C5 sont faits. Les quatre lignes restantes datent du 25/09/2026 et n'ont jamais été soumises dans ce journal : C1 propose de **ne pas** télécharger ; C2 porte sur des fichiers **déjà téléchargés** (4h : `D4_worldbank-api-findex-*.json`) ; C6 est une **demande** au MESPTN ; C7 est un indicateur geodata facultatif. L'intitulé « qui attendent ton accord » laissait croire à des téléchargements en suspens : il devient « bilan au 26/09/2026 », avec une introduction qui le dit.
- **Correction** : GD2 compte 24 fichiers GeoJSON, pas 25 couches (C4).

### 16.3 Points à trancher

| #  | Question                                   | Proposition                                                                                                                                                  |
| -- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| C1 | 2e (`train-full.csv`, `test.csv`, 3,26 Go) | Ne pas télécharger : ni date ni lieu, aucun apport au 02                                                                                                     |
| C2 | 4h (3 séries Findex de l'API, déjà en main) | Conserver : ces séries prolongent 4g jusqu'à la vague 2024 de la détention d'un compte ; W3 donne le même point en détail                                      |
| C6 | Tours télécoms (3h) : demande au MESPTN    | Même traitement que W6 (S9) : demande à faire par l'utilisateur, hors du chemin critique ; sans ces données, O2-06 reste un proxy et O2-08 reste national     |
| C7 | Indicateur geodata « élèves dans une école connectée à Internet » | Le rattacher à GD3, téléchargé à l'étape de préparation (S8)                                                                                 |

**Décision (26/09/2026)** : C1 écarté définitivement ; C2 conservé ; C6 laissé à l'appréciation de l'utilisateur, hors du chemin critique ; **C7 hors périmètre** (et non rattaché à GD3, contrairement à la proposition). Voir section 17.

---

## 17. Décisions sur les parties A et C du 03, et sur GD2 (26/09/2026)

**Validés par l'utilisateur**, avec les propositions du 03 :

- **Partie A** : A3, A4, A5, A6, A7, A8, A9, A10, A11 (tranché à l'étape du score), A12, A13, A18, A20, A21.
- **Partie C** : C1 écarté définitivement ; C2 conservé ; C6 à l'appréciation de l'utilisateur, hors du chemin critique ; C7 hors périmètre.
- **GD2** : conservé dans `obj5/` sans traitement ; **non requis par les 5 objectifs** ; utilisé seulement si l'étape 11 va jusqu'à l'optimisation de localisation. La procédure prévoit elle-même cette optimisation « si la couche de candidats du 03 existe » : la couche a été cherchée à l'étape 03 comme elle le demande, et elle est conservée.
- **GD3** : reporté à l'étape de préparation (S8, inchangé).

**Constat fait pendant le report de A4** (« AR1 pour 2018-2026 ») : le CA du secteur de 2b et la somme des 4 trimestres de l'ARCEP (dernière publication) **ne se raccordent pas**.

| Année | 2b (Md FCFA) | ARCEP, somme des 4 trimestres (Md FCFA) | Écart de 2b |
| ----- | ------------ | --------------------------------------- | ----------- |
| 2021  | 222,89       | 216,72 (54,05 + 53,17 + 55,23 + 54,27)  | +2,8 %      |
| 2022  | 229,28       | 221,19 (55,87 + 54,48 + 55,96 + 54,88)  | +3,7 %      |

Selon la logique de P4 (raccord seulement si les sources sont égales au point de jonction), 2b et AR1 sont donc **affichées côte à côte, sans raccord** : 2b pour la série nationale 2010-2022, AR1 pour 2018-2026 (CA par opérateur et CA du secteur), D3 pour le ratio Investissement / CA 2013-2019. Toute croissance se calcule dans une même source. L'origine de l'écart (périmètre, CA net ou brut, révisions) n'est pas documentée.

**Report dans le 03** : partie G de la section 11 (tableau des décisions et de leurs emplacements) ; parties A et C annotées ; sections 2 (fiche 2e, 2b), 3 (limites, ARPU, bloc), 4 (statuts, Mutuelle, zéros, bloc), 5 (bloc, rattachement), 6 (Grand Lomé), 8 (date PRISE), 9 (A4), 10 (O1-04, O2-03, O2-05, O3-01, O3-03, O3-04, O4-01, O4-03, O4-05, O5-01, trois couches, taux de résolution), 11 (B12, C4), 12 (GD2) ; bandeau et sommaire. Le bloc de D4 porte désormais sur les objectifs 3 et 4 (GD2 n'y sert plus l'objectif 5).

**Impact sur la phase 4** : précisé par l'utilisateur pour chaque décision, reporté en colonne dans la partie G. En le vérifiant, quatre décisions manquaient là où leur impact les rend nécessaires ; elles sont reportées : A8 (O4-04 : points, pas agents), A12 (O3-02 : 6e unité), A13 (fiche 3i, O2-06, O4-06 : « Non déterminable »), A21 (sections 6 et 7 : préfectures reconstituées, 5 codes de canton corrigés, 3 signalés). GD2 : « utilisé seulement si l'étape 11 est atteinte », pour l'optimisation de localisation.

**Décisions complémentaires (validées le 26/09/2026)** :

| #           | Décision | Vérification faite avant report |
| ----------- | -------- | ------------------------------- |
| A2          | Libellés « Moov Africa (Atlantique Telecom) » et « Togocom (Togo Cellulaire) » | L'ARCEP confirme la seconde correspondance : « Togocel » (abonnés) et « Togo Cellulaire » (CA) en 2018, « YAS Togo (Togo Cellulaire) » au T2 2026 |
| A5          | ARPU de D3 écarté ; recalculé depuis AR1 (CA / abonnés / 12), 2018-2026, niveau B | CA par opérateur trimestriel jusqu'au T2 2026 : années complètes 2018-2025, 2026 sur un semestre. **Rupture** : YAS Togo n'a pas déclaré son CA mobile money au T2 2026 (-7 % sur un an). Abonnés moyens = moyenne des 4 stocks trimestriels, comme le dit le 02 (convention ; T4 en sensibilité) |
| Seuil O3-02 | 3 strates par commune (Grand Lomé / autres villes / rural) ; seuil 50 % d'urbains ; sensibilité 75 % | RG3 : à 50 %, 13 communes « autres villes » (16,0 % de la population), 91 rurales (56,9 %), Grand Lomé 13 communes (27,0 %). À 75 % : 2 communes seulement (Ogou 1 84,4 %, Kozah 1 81,6 % ; 3,8 %), Cinkassé 1 juste en dessous (74,8 %) |
| O2-05       | Deux composantes, libellés distincts : O2-05a ARPU recalculé (2018-2026) ; O2-05b coût de 1 Go (2013-2025) | Seul O2-05b est soumis au seuil de 2 % du 02 ; O2-05a n'a pas de seuil |

**Relevé en fixant le seuil de O3-02, puis validé le 26/09/2026** : la règle du 02 confirme la concentration urbaine si le Grand Lomé réunit plus de 50 % des points pour **moins de 25 % de la population**. Le Grand Lomé en pèse **27,0 %** (2 188 376 sur 8 095 498, RGPH-5) : la règle ne peut pas conclure « confirmée », quel que soit le nombre de points. Décision, comme P2 : 02 inchangé, écart consigné, deux critères affichés séparément, lecture fondée sur l'indice de concentration et le gradient.

**Principe validé le 26/09/2026** : la référence est `_PROJECT.txt` (5 objectifs) ; le 02 reste figé, et on peut s'en écarter à quatre conditions (écart écrit, décidé avant le résultat, règle d'origine affichée, au service d'un objectif). Reporté dans l'intro du 03. Premier cas : la stagnation de O1-02 (P2) n'est plus « non traitée » mais traitée par un écart déclaré (classe « ralentissement »), à calculer à l'étape d'analyse ; la période de référence de la moyenne et de l'écart-type reste à fixer avant ce calcul.

**GD3 (26/09/2026)** : non téléchargé (04, V2) ; aucun indicateur du 02 ne l'utilise ; écart déclaré au 02 seulement si l'objectif 5 met en évidence un frein énergétique.

**Exécution du 04 (26/09/2026)** : 9 scripts (`prep/`), 136 contrôles, aucun bloquant en échec. Quatre constats demandent une décision, détaillés en section 9 du 04 : V4 (couverture 3i non déterminable étendue à Sotouboua 2 et Kéran 3), V5 (abonnés à la téléphonie par opérateur publiés en graphique seulement : O2-05a national), V6 (panier « 1 Go » de l'UIT limité à 2023-2025 ; le 03 est corrigé), V7 (EHCVM : accès à Internet déclaré, pas d'usage ni de mobile money).

**Décisions V4 à V7 (26/09/2026)** : validées. Correction faite en les consignant : le module 6 de l'EHCVM porte sur le mobile banking (2018/19 : « possède un compte dans un mobile banking » ; 2021/22 : « fait du mobile banking »), contrairement à ce que disaient le 03 et le 04. Estimations ajoutées par région (CV de 3 à 13 %) ; source de O3-05 revalidée le même jour : EHCVM 2021/22, Afrobaromètre en complément (04, V7). Findex 2024 ajouté : usage d'Internet sur 3 mois (43,7 %), smartphone principal (45,1 %).

## 18. Rôles des acteurs des recommandations (P28 du 10, 27/09/2026)

**Demande** : P28 (validé) — confirmer, avant le tableau de bord, les rôles marqués « à confirmer » dans la section 8 du 10 (« Qui agit ? »). Recherche faite sur des sources publiques ; chaque rôle confirmé cite sa source. Rien n'entre dans un calcul : ces sources documentent des acteurs, pas des chiffres.

| Rôle | Ce que disent les sources | Source | Statut |
| ---- | ------------------------- | ------ | ------ |
| Fonds du service universel (R8, R4b) | Le décret n° 2018-070/PR crée un compte spécial « fonds du service universel » auprès de l'ARCEP, qui le gère (art. 10) ; ressources : contributions des opérateurs et exploitants titulaires de licences, dons, subventions, contribution de l'ARCEP (art. 11) ; emplois : notamment « la desserte des localités éligibles » et les actions de la stratégie nationale de service universel (art. 12) ; ordonnateur : le ministre chargé des communications électroniques ; comptes approuvés par le ministre des finances (art. 13) ; comité de gestion avec les ministères, les opérateurs et les fournisseurs d'accès (art. 14-15) ; l'ARCEP met en œuvre la stratégie (art. 16) | [Décret 2018-070 (ARCEP)](https://arcep.tg/wp-content/uploads/2020/11/Decret_n2018-070-PR_relatif_au_service_universel_des_communications_electroniques_du_21-01-19_n066.pdf), téléchargé : DS1 (`obj5/`) | **confirmé** |
| Monnaie électronique (R5) | La BCEAO agrée les établissements de monnaie électronique non bancaires et fixe les conditions d'exercice (instruction n° 008-05-2015) ; les banques peuvent en émettre après information de la BCEAO | [BCEAO, établissements de monnaie électronique](https://www.bceao.int/fr/documents/etablissements-de-monnaie-electronique) ; [instruction 008-05-2015](https://www.bceao.int/sites/default/files/2017-11/instruction_no008_05_2015_intranet.pdf) | **confirmé** (agrément et conditions d'exercice) ; aucun plafond de frais trouvé : les grilles restent fixées par les émetteurs |
| Banques (R1, R2) | Supervision par la Commission bancaire de l'UMOA, présidée par la BCEAO | [BCEAO, Commission bancaire](https://www.bceao.int/fr/content/presentation-de-la-commission-bancaire) | **confirmé** |
| IMF / systèmes financiers décentralisés (R1, R2) | Loi n° 2011-009 ; supervision par le ministère chargé des finances (cellule CAS-IMEC), la BCEAO et la Commission bancaire de l'UMOA | [MFW4A, Togo](https://www.mfw4a.org/country/togo) ; [Assemblée nationale](https://assemblee-nationale.tg/les-deputes-adoptent-en-premiere-lecture-la-loi-sur-la-reglementation-de-la-microfinance-au-togo/) ; [loi SFD de l'UMOA](https://www.cb-umoa.org/sites/default/files/2022-02/Loi%20portant%20reglementation%20des%20systemes%20financiers%20decentralises%20de%20l'UMOA.pdf) | **confirmé** |
| Assurances (R2) | Code CIMA ; contrôle par la Commission régionale de contrôle des assurances (CRCA) ; relais national : Direction nationale des assurances, au ministère de l'économie et des finances | [CIMA, DNA Togo](https://cima-afrique.org/dna-tgo-fr-2/?lang=en) ; [service-public.gouv.tg](https://service-public.gouv.tg/single-administration/61bb073366dc3337885b8d84) | **confirmé** |
| Fibre de transport (R9) | La Société d'infrastructures numériques (SIN), société d'État créée par le décret n° 2016-166/PR, détient la fibre et le réseau de l'administration ; la coentreprise CSquared Woezon (SIN 44 %, CSquared 56 %) déploie et exploite les réseaux métropolitains et le réseau national ; depuis janvier 2021, un décret impose de poser de la fibre, pour le compte de la SIN, dans les nouveaux travaux de génie civil | [Agence Ecofin](https://www.agenceecofin.com/gestion-publique/0212-42903-le-togo-cree-la-societe-d-infrastructures-numeriques-qui-detiendra-le-capital-telecoms-national) ; [SIN](https://sin.tg/) ; [Digital Business Africa](https://www.digitalbusiness.africa/togo-comprendre-le-decret-novateur-pour-lacceleration-du-deploiement-national-de-la-fibre-optique/) ; [Financial Afrik](https://www.financialafrik.com/2022/03/22/connectivite-haut-debit-le-togo-1er-pays-relie-par-le-cable-de-fibre-optique-equiano-sur-le-continent-africain/) | **confirmé** (presse et site de la SIN, niveau C) |
| Ministère chargé du numérique (R7, R7b, R8) | Ministère de l'Économie numérique et de la Transformation digitale en 2025, qui révise la stratégie « Togo Digital » pour 2025-2030 ; un intitulé différent apparaît sur numerique.gouv.tg : le document écrit « ministère chargé du numérique » | [Togo First](https://www.togofirst.com/fr/tic/2705-16429-togo-une-nouvelle-strategie-digitale-en-preparation) ; [numerique.gouv.tg](https://numerique.gouv.tg/adoption-du-decret-sur-le-service-universel-pour-garantir-un-acces-minimum-aux-communications-electroniques/) | **confirmé** ; intitulé figé le 27/09/2026 : « Ministère de l'Efficacité du Service Public et de la Transformation Numérique », depuis le 8 octobre 2025 (section 19) |
| Collectivités (R7) | Aucune source trouvée sur un rôle des communes dans les compétences numériques | — | **non confirmé** : retiré du tableau |

**Report** : 10, section 8 (colonne « fondement ») ; R8 (le fonds existe : le mobiliser plutôt que le créer) ; R4b (le fonds finance la desserte des localités éligibles).

## 19. Nom du ministère pour la barre du haut du tableau de bord (P37 du 11, 27/09/2026)

**Demande** : P37 — la barre du haut reprise du défi 1 affiche le nom du ministère. Le défi 1 écrit « Ministère de l'Efficacité du Service Public et de la Transformation Digitale » ; l'utilisateur propose « Ministère de l'Économie numérique » comme formulation neutre, ou une vérification sur numerique.gouv.tg.

| Source | Ce qu'elle dit | Statut |
| ------ | -------------- | ------ |
| [numerique.gouv.tg](https://numerique.gouv.tg/) (en-tête du site, consulté le 27/09/2026) | « Ministère de l'Efficacité du Service Public et de la Transformation Numérique » | **source officielle** |
| [Togo First](https://www.togofirst.com/fr/telecoms/0910-17282-togo-cina-lawson-a-la-tete-du-nouveau-ministere-de-l-efficacite-du-service-public-et-de-la-transformation-numerique) ; [KOACI](https://www.koaci.com/article/2025/10/09/togo/politique/togo-premier-gouvernement-de-la-5e-republique-27-ministres-des-precisions_190953.html) | ministère créé dans le premier gouvernement de la Ve République (8 octobre 2025), confié à Cina Lawson | **confirmé** (presse, niveau C) |
| [Wikidata Q139833512](https://www.wikidata.org/wiki/Q139833512) | intitulé anglais : « Ministry of Public Service Efficiency and Digital Transformation » | repère pour la version anglaise du tableau de bord |

**Conclusion** :
- Le nom à afficher est « Ministère de l'Efficacité du Service Public et de la Transformation Numérique ».
- Le défi 1 (« Transformation Digitale ») est inexact.
- « Ministère de l'Économie numérique » n'est pas une formulation neutre : c'est le nom d'avant octobre 2025 (« Ministère de l'Économie numérique et de la Transformation digitale »). Afficher un intitulé qui n'existe plus, sous les armoiries, ferait passer un nom périmé pour officiel.

**Report** :
- 11, section 3.3 et P37.
- Section 18 ci-dessus : l'intitulé du ministère chargé du numérique est désormais figé. Le 10 garde « ministère chargé du numérique », qui reste exact.
