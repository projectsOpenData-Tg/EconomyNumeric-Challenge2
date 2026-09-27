# data/raw/_extradatas

Jeux de données complémentaires validés le 26/09/2026 : décisions D-1 à D-18, puis points P1 à P8, Q1 à Q12, R1 à R6 et S1 à S10 de `_RECHERCHE_donnees_manquantes.md` (sections 6, 8, 10 à 14). Ils comblent des manques relevés par `03_data_understanding.md`.

- **Un dossier par objectif** (`obj1` à `obj5`). Chaque fichier n'est rangé qu'une fois, dans son objectif principal. Les autres objectifs qu'il sert sont indiqués ci-dessous et dans le manifeste.
- **Préfixe = référence de recherche** : `BM`, `IN`, `MS`, `AR`, `W`, `CH`, `AS`, `IT`, `BC`, `TF`, `RG`, `CO`, `GD` renvoient aux sections du fichier de recherche (BM1, IN1, AR1, W1…) ; `C5` et `C5b` renvoient au point C5 de la section 11 du 03 (benchmark externe par l'API de la Banque mondiale).
- **`_MANIFEST.csv`** : pour chaque fichier, objectifs, description, URL et page source, date de téléchargement, taille, SHA-256, statut, et `type_fichier` (source ou dérivé). Pour les couches geodata, l'« URL » est la requête POST d'export.
- **Fichiers sources** : tels que publiés, non modifiés. Les pages web (AR5, TF1) sont des instantanés HTML datés.
- **Fichiers dérivés** (compilés par nous, contrôles décrits dans le manifeste) :
  - `obj1/W1_…_par-region.csv` : transcription de tableaux du rapport MICS6 ;
  - `obj1/CH1_chronologie-evenements.csv` : chronologie compilée ;
  - `obj1/C5b_…csv` et `obj4/C5_…csv` : séries extraites de l'API de la Banque mondiale (repères de O1-01 et de O4-02) ;
  - `obj4/RG_rgph5_livrets/RG2_…csv` et `RG3_…csv` : transcription des livrets 02 et 03 du RGPH-5 ;
  - `obj4/RG_rgph5_livrets/RG_rgph5_ecarts-internes-livrets.csv` : écarts internes des livrets, relevés et non corrigés.
- **Micro-données de la Banque mondiale** (`obj1/W2_ehcvm/`, `obj1/W3_findex2025/microdonnees/`) : obtenues le 26/09/2026 sur le compte de l'utilisateur, après acceptation des conditions d'utilisation (usage statistique agrégé, pas de redistribution, pas d'identification des répondants, citation de la source). **Ces deux dossiers sont ignorés par git** : ne jamais les partager. Chaque archive `.zip` est gardée telle quelle ; son contenu est décompressé dans le sous-dossier `donnees/`.

## Contenu par objectif

| Dossier | Fichiers | Sert aussi |
| ------- | -------- | ---------- |
| `obj1/` | BM1-BM3 (accès à l'électricité), BM7 (croissance du PIB par habitant), IN1 (projections démographiques 2011-2031), IN2 et IN3a/b (indices de prix), MS1 (datacenters), AR1 (34 observatoires trimestriels ARCEP, 2018 T1 - 2026 T2), AR2 (rapport d'activité 2017), AR3 (registre ARCEP), AR4 (3 décisions tarifaires), AS1 (annuaire statistique national 2024), W1 (MICS6 2017 : rapport et transcription), W2 (micro-données EHCVM 2018/19 et 2021/22, avec documentation), W3 (Findex 2025 : base par pays et micro-données Togo), W4 (Afrobaromètre, vagues 5 à 10), CH1 (chronologie), C5b (usage d'Internet : Afrique subsaharienne et 8 pays de l'UEMOA, repère de O1-01) | AR1 → obj2 (abonnés, CA et investissement par opérateur) et obj3 (comptes, points de vente et transactions mobile money) ; IN1 → obj2 et obj4 (dénominateur) ; IN2, IN3, AR4 → obj2 (tarifs) ; AS1 → obj2, obj3 ; W2 → obj2 (couverture captée par localité, dépense Internet) et obj3 (comptes, tontines) ; W3, W4 → obj3 (comptes, mobile money) |
| `obj2/` | AR2 (rapport d'activité 2025 : sites et cellules par opérateur), AR5 (page des tarifs, septembre 2023), AR6 (9 études ARCEP : QoS, QoE, tarifs, satisfaction), IT1 (paniers de prix TIC de l'UIT, 2008-2025) | IT1 → obj1 (chronologie des prix) |
| `obj3/` | BC1 (BCEAO, services financiers numériques 2024), TF1 (grilles tarifaires mobile money, instantanés du 26/09/2026), GD1 (agences de la Poste, 95 points) | BC1 → obj4 ; GD1 → obj4 (test de sensibilité, point Q5) |
| `obj4/` | IN4 (électricité par préfecture, 2018-2021), RG1 à RG3 (livrets 01 à 03 du RGPH-5) et leurs transcriptions, CO1 (OCHA, population 2021 par préfecture : contrôle), AS2 (annuaires régionaux 2024 : Maritime, Centrale, Kara, Savanes), BC2 (BCEAO, inclusion financière 2024 : rapport et tableau de bord), C5 (agences et DAB pour 100 000 adultes, 8 pays de l'UEMOA, repère de O4-02) | IN4 → obj5 ; RG → obj3 (milieu urbain / rural) et obj1 (15 ans et plus) ; BC2 → obj3 |
| `obj5/` | GD2 : lieux candidats de geodata (1 078 marchés, 15 454 établissements scolaires, 2 271 formations sanitaires, 1 576 établissements administratifs de 21 ministères) | — |

## Non obtenus

| Élément | Raison | Suite |
| ------- | ------ | ----- |
| AR6 : campagne nationale QoS du 2e semestre 2023 | Lien mort sur arcep.tg (erreur 404) | Signalé dans le manifeste (statut « échec ») |
| AS2 : annuaire 2024 de la région des Plateaux | Non publié (dernier annuaire des Plateaux : 2020) | Aucune ; RG2 donne la population 2022 par préfecture |
| TF1 : grille officielle des frais de retrait Mixx by Yas | Non publiée sur yas.tg (seules les conditions du transfert y figurent) | Grille de l'agrégateur momocalc gardée en contrôle, niveau C |
| W1 : micro-données MICS6 | Compte requis sur mics.unicef.org | Abandonnées (décision S9) : les tableaux régionaux transcrits suffisent |
| W6 : tableaux d'équipement TIC du RGPH-5 | Non publiés en ligne | Demande à l'INSEED à faire par l'utilisateur, hors du chemin critique (D-17, S9) |
| W7 : Ookla | Écarté (décision S9) | O2-09, optionnel dans le 02, n'a pas de mesure couvrant tous les territoires |
| OC1 : OpenCellID | Écarté (décision S9) | O2-06 reste une couverture théorique ou déclarée |
| GD3 : indicateurs geodata (électricité, villages, écoles équipées) | Reporté (décision S8) | À télécharger à l'étape de préparation |
| BM8 : revenu par habitant en PPA | Écarté (décision S8) | IT1 donne le coût de 1 Go en % du RNB |
| RG1 : transcription | Reportée (décision S10) : le 02 s'arrête à la commune | Livret téléchargé ; à transcrire à l'étape 11 si le ciblage descend au canton |
