# 03 — Data Understanding

*Les données disponibles permettent-elles réellement de mesurer ce que demandent le sujet, le cadrage (01) et la matrice de décision (02) ?*

Ce document examine **jeu de données par jeu de données** les fichiers de `data/raw/` : ceux des liens de `_PROJECT.txt` (D1 à D6), puis les compléments trouvés le 25/09/2026 en parcourant tout le catalogue d'opendata.gouv.tg et la plateforme geodata.gouv.tg (1b, 2b à 2e, 3b à 3i, 4b à 4j, 5b, 5c, 6b). La numérotation est celle de l'inventaire complet, `_INVENTORY_datasets.txt`. Les sources complémentaires validées le 26/09/2026 sont dans `data/raw/_extradatas/` ; leurs fiches sont en section 12, sous la référence de recherche (AR1, IN1, W2, RG2…), et chaque section de D1 à D6 se termine par la liste de ceux qui la complètent, pour quel objectif. Ce document ne produit aucune carte ni aucun indicateur. Il établit ce que chaque fichier contient, ce qu'il permet de calculer, avec quelle fiabilité, et ce qu'il ne permet pas de calculer.

**Périmètre des informations utilisées :**

- Cadrage : `_PROJECT.txt`, `01_problem_definition.md`, `02_decision_matrix.xlsx`.
- Portails publics : fichiers et métadonnées publiés sur opendata.gouv.tg et geodata.gouv.tg ; API de la Banque mondiale.
- **Élargissement validé le 26/09/2026** (décisions D-6 et D-13 de `_RECHERCHE_donnees_manquantes.md`) :
  - Autorités : site de l'ARCEP, site de l'INSEED (annuaires, livrets du RGPH-5), BCEAO, UIT, OCHA (HDX) ;
  - Enquêtes auprès des ménages : rapport MICS6, micro-données EHCVM et Findex (Banque mondiale), Afrobaromètre ;
  - Grilles tarifaires des opérateurs ;
  - Presse, pour dater des événements de la chronologie seulement (niveau C).

  Le détail des recherches et des décisions est dans `_RECHERCHE_donnees_manquantes.md` ; la traçabilité des fichiers (URL, date, SHA-256), dans `data/raw/_extradatas/_MANIFEST.csv`.

Les informations manquantes et les choix à faire sont listés en section 11, **pour validation avant l'étape suivante**.

**Référence du projet (26/09/2026)** : le but est de répondre aux 5 objectifs de `_PROJECT.txt`. Le 02 est figé et n'est jamais réécrit, mais on peut s'en écarter quand une de ses règles empêche de répondre à un objectif, à quatre conditions : l'écart est écrit ici ou dans les livrables suivants ; il est décidé avant de voir le résultat qu'il change, pour une raison tirée des données ; la règle d'origine reste affichée à côté quand c'est possible ; il sert un objectif du projet. Écarts déclarés à ce jour : classe « ralentissement » de O1-02 (section 1) ; lecture de O3-02 par l'indice de concentration et le gradient (section 10).

**Niveau de preuve** (repris de la procédure du projet) : **A** = mesuré (comptage direct, recalculable), **B** = calculé (dérivé d'une formule maîtrisée), **C** = estimé (valeur pré-calculée par la source, proxy ou méthode non documentée).

---

## Mise à jour du 26/09/2026

Le périmètre des sources est élargi (ARCEP, INSEED, BCEAO, UIT, enquêtes auprès des ménages) : 133 fichiers dans `data/raw/_extradatas/obj1` à `obj5`, décrits en section 12. Ce qui change pour l'analyse :

- **D1 est presque entièrement une estimation.** D'après les notes de l'API de la Banque mondiale, toutes les années 2000-2016 et 2018-2023 sont des « ITU estimate » ; seule 2017 vient de l'INSEED. Les accélérations et ralentissements de D1 décrivent donc surtout le modèle de l'UIT. Les points **mesurés** par enquête (MICS6 2017, EHCVM 2018/19 et 2021/22, enquête EIPT 2020, Findex 2024, Afrobaromètre 2012-2024) servent à les vérifier (section 1).
- **Stagnation : écart déclaré au 02.** Avec le seuil du 02 (|g| < 2 %), aucune année n'est une stagnation : la plus faible croissance de D1 est de +4,5 % (2021). L'objectif 1 demandant ces périodes, O1-02 y répond par un écart déclaré : aucune stagnation au sens strict, et des périodes de **ralentissement** (croissance < moyenne − 1 écart-type), calculées à l'étape d'analyse, d'abord sur les points mesurés (sections 1, 10 et 11). **Tant que ce calcul n'est pas fait, cette partie de l'objectif 1 reste ouverte.**
- **Technologies après 2019** : l'observatoire trimestriel de l'ARCEP (AR1) prolonge les abonnements par technologie et par opérateur jusqu'au T2 2026. Les séries annuelles raccordent D2 / 2b (jusqu'en 2017) et AR1 (à partir de 2018) par la **valeur du T4, une convention et non une moyenne**, testée en sensibilité (sections 2 et 9).
- **Corrections du 03** :
  - la baisse de 2019 chez Togocel (D2) n'existe pas chez l'ARCEP ;
  - la « 3G Atlantique Telecom » de 2018-2019 réunit la 3G et la 4G de Moov ;
  - l'ARCEP a révisé toute l'année 2021 (section 2) ;
  - le CA et l'investissement par opérateur existent (AR1, section 3) ;
  - la population de 15 ans et plus et le milieu existent par territoire (RGPH-5, section 6).
- **Usage par territoire et freins** : par région, grâce à la MICS6 et aux deux vagues de l'EHCVM ; smartphone au niveau national (Findex 2024).
- **Objectif 2** : CA et investissement par opérateur (AR1), coût de 1 Go rapporté au revenu (UIT), sites radio par opérateur et par technologie au niveau national (ARCEP), qualité de service au niveau national seulement (ARCEP : QoE par opérateur, campagne 2024 dans 94 localités).
- **Objectifs 3 et 4** :
  - 15 ans et plus et milieu urbain / rural par préfecture et par commune (livrets 02 et 03 du RGPH-5, transcrits et contrôlés) ;
  - comptes, points de vente et transactions mobile money par opérateur (ARCEP) et par pays de l'UEMOA (BCEAO) ;
  - mobile money par région (Afrobaromètre) ;
  - grilles tarifaires (instantané daté) ;
  - agences de la Poste.
- **Les trois couches de la procédure** sont présentes : demande (enquêtes), benchmark (repère Afrique subsaharienne et UEMOA de O1-01, C5b ; repère UEMOA de O4-02, C5 ; UIT, BCEAO, Findex tous pays) et lieux candidats (geodata, `obj5/`), conservés mais **non requis par les 5 objectifs** (26/09/2026).
- **Dénominateurs** : trois bases coexistent (Banque mondiale, IN1, RGPH). Elles ne se mélangent pas dans un même indicateur (encadré de la section 9).
- **Couverture du 02** : 18 indicateurs ✅, 13 ⚠️ et 0 ❌ (5, 19 et 7 le 25/09/2026). **Attentes du 01** : environ 95 % (section 10).
- **Section 11** : A1, A15 et A16 sont tranchés, la partie B est mise à jour, et deux parties sont ajoutées : D (décisions du 26/09/2026) et E (décisions R1 à R6, validées le même jour, avec les précisions de l'utilisateur).
- **R1 à R6, validés** : le repère UEMOA de O4-02 utilise désormais le FAS (C5, téléchargé) plutôt que le taux de la BCEAO ; RG2 et RG3 deviennent la source de population des objectifs 3 et 4 ; O3-06 est calculable pour Flooz, partiel pour Mixx ; Q12 est comparé sur les 6 domaines ; O1-02 sur les abonnements n'est classé que si les deux conventions concordent.
- **Sections 1 à 6** : chaque jeu se termine par un bloc « Données complémentaires téléchargées » : quels fichiers de `_extradatas` le complètent, pour quels objectifs et indicateurs, avec quel niveau de preuve, et ce qui reste non résolu.
- **Parties A et C de la section 11 tranchées** (partie G) : règles de comptage (A6 à A9), date de référence (A10), zéros (A13), CA sans raccord entre 2b et AR1 (A4)… ; C1 et C7 écartés ; GD2 conservé mais non requis par les 5 objectifs. Chaque décision porte son impact sur la phase 4. **A2, A5, le seuil urbain de O3-02 et le contenu de O2-05 sont tranchés aussi** : libellés d'opérateurs confirmés par l'ARCEP ; ARPU recalculé depuis AR1 (O2-05a), à côté du coût de 1 Go (O2-05b) ; communes « autres villes » à partir de 50 % d'urbains. Le Grand Lomé pèse 27,0 % de la population (RGPH-5), au-dessus du plafond de 25 % de la règle de O3-02 du 02 : **décision**, la règle est appliquée telle quelle, ses deux critères affichés séparément, et la lecture repose sur l'indice de concentration et le gradient (section 10). **Aucune décision de la section 11 n'est en attente.**
- **S1 à S10, validés** (partie F de la section 11) :
  - **repère Afrique subsaharienne de O1-01 téléchargé** (C5b) : le Togo passe au-dessus de la moyenne régionale en 2020 et la dépasse de 5,9 points en 2024 (39,5 % contre 33,6 %), deux estimations de l'UIT ;
  - O4-02 : moyenne UEMOA, repère limité à ce qui est comparable (agences ; DAB au niveau national seulement), échelle ramenée à 10 000 adultes ;
  - âge non déclaré réparti au prorata ; rupture ARCEP du T1 2020 traitée comme rupture de série ; saut de l'indice des prix en 2020 non lu comme une hausse ;
  - **O2-09 n'est pas couvert** par une mesure de qualité de service sur tous les territoires (Ookla écarté) ; O2-06 reste une couverture théorique ou déclarée ;
  - BM8, MICS6 (micro-données), OpenCellID écartés ; GD3 reporté à la préparation ; RG1 non transcrit (étape 11 si besoin).

---

## Mise à jour du 25/09/2026

L'inventaire compte 22 fiches de plus (2b à 2e, 3b à 3i, 4c à 4j, 5c, 6b). Ce qui change pour l'analyse :

- **Séries nationales prolongées.** Abonnements Internet par opérateur, télédensités, chiffre d'affaires du secteur et mobile money jusqu'en 2022 (2b) ; abonnés fixe et mobile jusqu'en 2024 (3f) ; inflation annuelle (4g). Toujours rien après 2019 pour le détail par technologie, les parts de marché de la téléphonie, l'investissement et l'ARPU.
- **Les ATM existent** : 184 sites de DAB géolocalisés (4c). La version « par type » de O4-01 et la règle 5 de O4-05 deviennent calculables.
- **La date de collecte est connue** : « Campagne de collecte PRISE - 2021/2022 » pour D4, 4c et D5, d'après geodata.gouv.tg. L'écart avec le RGPH 2022 tombe à un an au plus.
- **Une couverture mobile par territoire, mais en proxy** : part des habitants à moins de 20 km d'une tour (3i), sans distinction 2G / 3G / 4G, en niveau C, avec des valeurs impossibles (0 % à Mô et à Kpendjal).
- **Une clé territoriale codée** : geodata publie des codes de la région au canton, et les noms de D4, 4c et D5 y correspondent à 100 % (section 7).
- **Les contours des territoires sont téléchargés** (6b, après validation). Ils rendent possibles les cartes choroplèthes et la superficie (56 654,6 km² au total, O4-02 par km²). Ils confirment aussi la position des points : 100 % des points de D4 et de 4c sont dans le polygone de leur unité déclarée, de 99,63 à 99,75 % pour D5 (sections 6 et 7).
- **Une source de demande pour l'inclusion financière**, au niveau national : Findex 2011-2024 (4g, 4h).
- **Une même grandeur a souvent plusieurs valeurs** selon la source, surtout à cause des dénominateurs de population (section 9).
- **Couverture du 02** : 5 indicateurs ✅, 19 ⚠️ et 7 ❌, contre 3, 17 et 11 avant les compléments (section 10).
- **Attentes du 01** : environ 83 % des livrables obligatoires sont réalisables avec les données actuelles, de 67 % (objectif 2) à 100 % (objectif 4) (section 10).
- **Points à valider (section 11)** : A15 à A21, B11, B12 et toute la partie C sont nouveaux ; A1, A2, A4, A5, A9 à A11, A13 et A14 sont révisés ; la partie B indique désormais ce que la recherche a trouvé pour chaque donnée manquante. B2 et C3 sont réglés par 6b.

---

## Sommaire

1. D1 — Individus utilisant Internet (% de la population) : 1, 1b ; données complémentaires téléchargées (objectif 1)
2. D2 — Abonnés Internet par type d'accès : 2, compléments 2b à 2e ; données complémentaires téléchargées (objectifs 1 et 2)
3. D3 — Récapitulatif segment téléphonie et GSM : 3, compléments 3b à 3i ; données complémentaires téléchargées (objectif 2)
4. D4 — Établissements financiers : 4, compléments 4b à 4j ; données complémentaires téléchargées (objectifs 3 et 4)
5. D5 — Agents mobile money : 5, compléments 5b, 5c et page geodata.gouv.tg ; données complémentaires téléchargées (objectifs 3 et 4)
6. D6 — Recensement général de la population (RGPH 2022) : 6, complément 6b (limites administratives) ; données complémentaires téléchargées (dénominateurs)
7. Jointures entre fichiers : le référentiel territorial
8. Millésimes
9. Une même grandeur, plusieurs sources
10. Couverture des indicateurs du 02
11. Informations à valider
12. Sources complémentaires (`data/raw/_extradatas/`)

---

## 1. D1 — Individus utilisant Internet (% de la population)

```
Dataset       : Individus utilisant Internet (% de la population)
Fichiers      : D1_individus-utilisant-internet.csv (opendata.gouv.tg)
                D1_worldbank-api.json (1b : API Banque mondiale, lien « source » du projet)
Source        : Banque mondiale (WDI) ; donnée d'origine UIT
Période       : 1960-2022 renseignée dans le CSV ; 1960-2024 dans l'API
Unité d'obs.  : pays x année
Granularité   : National
Fréquence     : Annuelle
Lignes        : 64 (CSV) ; 66 (API)
```

**Colonnes :** `indicator`, `country`, `countryiso3code`, `date`, `value`, `unit`, `obs_status`, `decimal`. Seules `date` et `value` sont informatives.

**Variables principales**

| Variable  | Contenu                                                                 | Preuve                                                       |
| --------- | ----------------------------------------------------------------------- | ------------------------------------------------------------ |
| `date`  | Année                                                                  | A                                                            |
| `value` | % de la population ayant utilisé Internet au cours des 3 derniers mois | C (pré-calculé, numérateur et dénominateur non publiés ; estimation de l'UIT pour 2000-2016 et 2018-2023) |

**Utilité**

- → Objectif 1 : série principale de l'usage d'Internet (O1-01), base des taux de croissance et des ruptures (O1-02), terme « utilisateurs » de l'écart avec les abonnements (O1-03).

**Qualité**

- Pas de doublon d'année, pas de problème de format.
- 13 années vides sur 64 : 1961-1964, 1966-1969, 1971-1974 et 2023.
- Valeurs à 0 de 1960 à 1995 : des zéros déclarés, pas des cases vides. Aucune année de rupture n'est calculable sur une base nulle.
- **Deux versions de la même série.** La version API (mise à jour le 13/07/2026) révise 2021 (30,34 contre 32,51) et 2022 (35,61 contre 37,62), et ajoute 2023 (37,57) et 2024 (39,48). Les années antérieures à 2021 sont identiques. **Version retenue : l'API** (11.A1, tranché le 26/09/2026). Seule 2021 change vraiment la lecture : +4,5 % avec l'API, +12,0 % avec le CSV.
- **Presque entièrement estimée** (constat du 26/09/2026). Les notes de l'API de la Banque mondiale (`footnote=y`) qualifient d'« ITU estimate » toutes les années 2000-2016 et 2018-2023. Seule 2017 (12,36 %) est attribuée à l'INSEED ; 2024 n'a pas de note. Le champ `obs_status` du fichier est vide partout et ne permet pas de le voir. Les pas réguliers des années 2000-2014 (+0,2 point par an de 2006 à 2009, +0,5 de 2011 à 2013) en sont la trace.

**Limites**

- Seul le taux est publié : on ne peut pas recalculer le nombre d'utilisateurs ni changer de dénominateur. La formule de O1-01 (utilisateurs / population) est donc fournie toute faite par la source.
- **Le dénominateur n'est pas celui du recensement.** Les séries UIT de 3f (nombre d'abonnements et taux pour 100 personnes) impliquent une population de 9,09 M en 2022, soit 12 % de plus que le RGPH 2022 (8,10 M). D1 vient de la même source et a vraisemblablement le même dénominateur, ce qu'on ne peut pas vérifier sans le numérateur. Il ne se compare donc à aucun taux calculé avec IN1 ou le RGPH (encadré de la section 9).
- **Les ruptures de D1 décrivent surtout le modèle d'estimation de l'UIT.** Décision D-15 : D1 garde la tendance, marquée « estimation UIT » année par année, et une accélération n'est lue que si les points mesurés par enquête la confirment (section 12, W1 à W4 et AS1). Ces points ont chacun leur définition (âge, « a utilisé » ou « a accès », période) : ils ne se relient pas entre eux.
- **La stagnation n'est pas repérable avec le seuil du 02.** Le 02 définit la stagnation par |g| < 2 %. Aucune année ne l'atteint : la croissance la plus faible est +4,5 % (2021, version API). Les ralentissements nets (2017 : +9,3 % ; 2021 : +4,5 % ; 2023 et 2024 : +5,5 % et +5,1 %) n'entrent dans aucune classe. Le 01 demande pourtant les périodes où l'usage « a ralenti, stagné ou reculé ». Le 02 n'est pas modifié. **Écart déclaré (26/09/2026)**, parce que l'objectif 1 de `_PROJECT.txt` demande ces périodes : O1-02 répond « aucune stagnation au sens strict (|g| < 2 %) » et repère les **ralentissements** (croissance < moyenne − 1 écart-type) à l'étape d'analyse, d'abord sur les points mesurés (11.D, P2). **Tant que ce calcul n'est pas fait, cette partie de l'objectif 1 reste ouverte.**
- Aucune ventilation territoriale ni par âge. Par sexe, une seule année, dans 3g : 8,6 % des femmes et 16,3 % des hommes en 2017. L'usage par territoire vient des enquêtes (section 12).

### Données complémentaires téléchargées : objectif 1

*Fichiers de `data/raw/_extradatas/`, retenus par le journal de recherche (décisions entre parenthèses). Profils complets : section 12.*

| Réf. | Fichier (dossier) | Ce qu'il apporte face aux limites de D1 | Indicateurs du 02 | Preuve |
| ---- | ----------------- | --------------------------------------- | ----------------- | ------ |
| C5b | `obj1/C5b_worldbank-uit-internet-afrique-subsaharienne-uemoa.csv` | Repère exigé par le 02 : moyenne Afrique subsaharienne de l'année, et les 8 pays de l'UEMOA. Le Togo passe au-dessus de la moyenne régionale en 2020 (S1) | O1-01 | C |
| W1 | `obj1/W1_mics6_2017/` (rapport, transcription) | Point **mesuré** 2017, avec la définition de l'UIT (15-49 ans) ; usage, compétences TIC et alphabétisation par région (7 domaines) | O1-01 (point), O1-05, O1-06 | C |
| W2 | `obj1/W2_ehcvm/` (micro-données sous conditions) | Points mesurés 2018/19 et 2021/22 (« a accès », 15 ans et plus), par région et milieu ; portable ; alphabétisation (R5) | O1-01 (points), O1-05, O1-06 | B |
| W3 | `obj1/W3_findex2025/` | Point mesuré 2024 (15 ans et plus) : Internet 43,7 %, smartphone 45,1 %, freins (coût, lecture, couverture) ; national, urbain / rural | O1-01 (point), O1-06 | C |
| W4 | `obj1/W4_afrobarometre/` (vagues 5 à 10) | Points mesurés 2012 à 2024 (fréquence d'usage), pour vérifier les ruptures de D1 (D-15) ; région en petits effectifs | O1-01, O1-02 | C |
| AS1 | `obj1/AS1_inseed_annuaire-statistique-national-2024.pdf` | Point mesuré 2020 (enquête EIPT, **ménages**) : 43,7 % des ménages connectés | O1-01 (point ménage) | A à C |
| CH1 | `obj1/CH1_chronologie-evenements.csv` (dérivé de AR2, AR3, AR4, MS1, IN2, IN3 et de la presse) | 40 événements datés (technologies, opérateurs, tarifs, crise sanitaire) pour annoter les ruptures, jamais pour les expliquer (D-16) | O1-02 | A ou C |
| IN2, IN3 | `obj1/IN2_*`, `obj1/IN3a_*`, `obj1/IN3b_*` | Prix mensuels de la connexion Internet et de la communication, 2010-2024 ; le saut de 2020 n'est pas lu comme une hausse (S7) | O1-02 (annotation) | C |
| IN1 | `obj1/IN1_*` | Population annuelle 2011-2031 : variante 15 ans et plus de O1-03 ; D1 garde son propre dénominateur (P3, R2) | O1-03 | C |
| BM1-BM3, BM7 | `obj1/BM*` | Accès à l'électricité (total, urbain, rural) et croissance du PIB par habitant : contexte des ruptures | Contexte | C |

Les abonnements par technologie après 2019 (AR1), qui servent aussi O1-02 à O1-04, sont décrits avec D2.

**Ce que ces compléments règlent** : le repère régional de O1-01 ; des points mesurés pour confirmer ou non les accélérations de la série estimée (D-15) ; l'usage par région (O1-05) à plusieurs dates ; les freins (O1-06), smartphone compris ; la datation des ruptures (O1-02).

**Ce qui reste non résolu** :
- **Stagnation** : aucune donnée ne corrige cela, c'est le seuil du 02 (|g| < 2 %) qui ne se déclenche jamais (P2, V2). Réponse prévue par un écart déclaré : classe « ralentissement », calculée à l'étape d'analyse ; **non faite à ce jour**.
- D1 reste une estimation de l'UIT (niveau C) : les enquêtes la contrôlent, elles ne la remplacent pas. Leurs points ne se relient pas entre eux (définitions, âges et périodes différents).
- Rien sous la région : aucun usage par préfecture ni par commune.
- Le dénominateur de D1 (Banque mondiale, +12 % par rapport au RGPH) reste invérifiable.

---

## 2. D2 — Abonnés Internet par type d'accès

```
Dataset       : Abonnés Internet par type d'accès au Togo
Fichier       : D2_abonnes-internet-type-acces.csv
Source        : INSEED (publication opendata.gouv.tg)
Période       : 2013-2019
Unité d'obs.  : indicateur x année (format long)
Granularité   : National ; opérateur pour une partie des indicateurs
Fréquence     : Annuelle
Lignes        : 160 (25 indicateurs x 7 ans, 15 couples absents)
```

**Colonnes :** `indicateur`, `Unit` (toujours « Nombre », même pour les taux en %), `Date`, `Value`.

**Structure des 25 indicateurs.** La hiérarchie a été vérifiée : chaque total est exactement la somme de ses composantes, pour les 7 années.

| Niveau             | Indicateurs                                                                                          | Contrôle                                                             |
| ------------------ | ---------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| Total              | `T abonnés Internet Fixe et Mobile (Toutes technologies)`                                         | = mobile toutes technologies + fixe (Togo Telecom, CAFE, GVA, TEOLIS) |
| Mobile             | `T abonnés Internet mobiles (Toutes technologies)`                                                | =`T Atlantique Telecom` + `T Togo Cellulaire`                     |
| Opérateur mobile  | `T Atlantique Telecom`, `T Togo Cellulaire`                                                      | = GPRS/EDGE + 3G + 4G de l'opérateur                                 |
| Technologie mobile | `Abonnés GPRS/EDGE …`, `Nombre de clients 3G …`, `Nombre de clients 4G …` (par opérateur) | —                                                                    |
| Mobile haut débit | `T abonnés Internet mobiles (Haut débit)`                                                        | = somme des 3G + 4G                                                   |
| Fixe               | `T Abonnés Internet Togo Telecom`                                                                 | = ADSL + FTTH + Wimax + LS Internet                                   |
| Autres accès      | `EvDo`, `Illiconet`, `LS point à point`, `CAFE`, `GVA`, `TEOLIS`                        | —                                                                    |
| Taux               | `Taux de pénétration Internet (Toutes technologies) (%)`, `… haut débit (%)`                 | = abonnés / population implicite (6,64 M en 2013, 7,62 M en 2019)    |

**Utilité**

- → Objectif 1 : terme « abonnements » de O1-03 et part par technologie (O1-04 : 2G = GPRS/EDGE, 3G, 4G, fibre = FTTH).
- → Objectif 2 : abonnements fibre (O2-07, FTTH : 92 en 2017, 2 068 en 2018, 6 888 en 2019) ; parts de marché sur le segment data par opérateur (variante de O2-01).

**Qualité**

- Aucun doublon ni aucune valeur manquante dans les lignes présentes.
- **15 couples indicateur x année absents** : EvDo 2018-2019, Illiconet 2015-2019, LS point à point 2014-2019, 4G Atlantique Telecom 2018-2019. Un couple absent n'est pas un zéro. **Correction du 26/09/2026** : la 4G d'Atlantique Telecom n'est pas inconnue en 2018-2019. Elle est **comprise dans la ligne « 3G Atlantique Telecom »**, car l'ARCEP publie « clients 3G et 4G de Moov » ensemble (633 580 au T4 2019, la valeur de D2). La 4G de Moov n'est séparée qu'à partir du T4 2019 (99 013 abonnés).
- **Ruptures à vérifier avant toute interprétation :**
  - `Abonnés GPRS/EDGE Atlantique Telecom` : 381 711 en 2015, 68 615 en 2016, 577 380 en 2017. La baisse de 2016 coïncide avec l'apparition de la 3G du même opérateur (294 508) : reclassement probable.
  - `T Togo Cellulaire` : 2 085 898 en 2018, puis 1 417 858 en 2019 (la 3G passe de 1 932 767 à 1 242 250). Le total national baisse en 2019 alors que l'usage (D1) augmente. **Correction du 26/09/2026 : cette baisse n'existe pas chez l'ARCEP** (AR1). Au T4 2019, l'ARCEP compte 2 373 589 abonnés 3G, 315 044 4G et 20 494 GPRS chez Togocel (D2 : 1 242 250, 174 474 et 1 134), soit une 3G en hausse de 22,8 % sur un an. L'origine des valeurs 2019 de D2 est inconnue ; elles sont écartées (11.A15).
- **Accord avec l'ARCEP jusqu'en 2018** : la 3G de Togocel est identique dans D2 et à l'ARCEP au T4 (1 610 821 en 2017, 1 932 767 en 2018). Au raccord, l'écart est nul en 2018 et de 786 abonnés en 2017 (3G de Moov, 0,03 %).
- La colonne `Unit` vaut « Nombre » pour les taux en %.

**Limites**

- **La description du jeu annonce des accès 5G et Wi-Fi et une ventilation urbain / rural : rien de cela n'est dans le fichier, ni dans 2b.**
- Le taux de pénétration est un taux d'**abonnements** (49,55 % en 2018, alors que D1 donne 15,5 % d'**utilisateurs**). Il ne se substitue jamais à O1-01, comme le prévoit le 02.
- **Série arrêtée en 2019.** 2b prolonge les abonnements par opérateur jusqu'en 2022, mais sans le détail par technologie. **Depuis le 26/09/2026, l'observatoire de l'ARCEP (AR1, section 12) prolonge le détail par technologie et par opérateur jusqu'au T2 2026.** Règle retenue (11.A15, P4) : D2 / 2b jusqu'en 2017, AR1 à partir de 2018.
  - **Valeur du T4 pour l'annuel : c'est une convention, pas une moyenne.** L'année est représentée par son stock de fin d'année, comme le font l'UIT et l'INSEED : les valeurs annuelles de 2b sont celles du T4 de l'ARCEP. Pour O1-04 et O2-01, l'année est donc représentée par son dernier trimestre.
  - **La moyenne des 4 trimestres est testée en sensibilité.** Le premier contrôle (abonnements data mobile, 2018-2025) ne montre pas de pic saisonnier au T4, mais les deux conventions donnent des croissances différentes certaines années (section 9).
  - Pour chaque trimestre, on prend la publication la plus récente, car l'ARCEP révise ses séries.
- Les libellés mélangent technologies (ADSL, FTTH, Wimax) et fournisseurs (CAFE, GVA, TEOLIS, Illiconet) dont la technologie n'est pas précisée.

### Compléments : 2b à 2e

| #  | Fichier                                   | Source                | Période                      | Apport                                                                                            |
| -- | ----------------------------------------- | --------------------- | ---------------------------- | ------------------------------------------------------------------------------------------------- |
| 2b | `D2_communications-electroniques.csv`    | INSEED                | 2010-2022                    | Abonnements Internet par opérateur, télédensités, large bande fixe, mobile money, CA du secteur |
| 2c | `D2_haut-debit-fixe.csv`                 | Banque mondiale (UIT) | 2007-2023                    | Abonnements au haut débit fixe pour 100 personnes                                                |
| 2d | `D2_worldbank-api-haut-debit-fixe.json`  | API Banque mondiale   | 2007-2024                    | Même série que 2c, version la plus récente                                                        |
| 2e | `train-full.csv`, `test.csv` (non téléchargés, écartés) | MESPTN          | 2024 d'après les métadonnées | Jeu ménage préparé pour l'apprentissage automatique                                              |

**2b — Communications électroniques (INSEED)**

160 lignes (14 séries x 13 ans, 22 couples absents), format long : `indicateur`, `type-operateur`, `operateur`, `Unit`, `Date`, `Value`.

| Série                                                      | Détail                                                | Période                                | Preuve                                        |
| ---------------------------------------------------------- | ----------------------------------------------------- | -------------------------------------- | --------------------------------------------- |
| Abonnements Internet mobile                                | Togo Cellulaire, Moov Africa Togo, total              | 2010-2022                              | A                                             |
| Abonnements Internet fixe                                  | Togo Telecom, CAFE Informatique, TEOLIS, GVA, total   | 2010-2022 (TEOLIS et GVA : 2018-2022)  | A                                             |
| Lignes fixes, abonnés mobiles, large bande fixe            | pour 100 habitants                                    | 2010-2022                              | C (population non publiée)                   |
| Abonnés actifs mobile money ; valeur des transactions     | national                                              | 2013-2022                              | A ; définition d'« actif » non publiée      |
| Chiffre d'affaires du secteur                             | FCFA                                                  | 2010-2022                              | C (périmètre, net ou brut non documentés)   |

- **Utilité**
  - → Objectif 1 : abonnements Internet mobile jusqu'en 2022 (O1-02, O1-03).
  - → Objectif 2 : parts de marché du segment data sur 2010-2022 (O2-01) ; CA du secteur sur 2010-2022 (O2-03).
  - → Objectif 3 : seule série d'abonnés actifs et de valeur des transactions mobile money (O3-04, au niveau national).
- **Qualité**
  - Identique à D2 sur 2013-2019, opérateur par opérateur : « Moov Africa Togo » y porte les valeurs d'« Atlantique Telecom » (11.A2). Total fixe = total D2 − mobile D2.
  - Les opérateurs somment exactement aux totaux sur 2010-2022. Aucun doublon, aucune valeur vide. TEOLIS et GVA n'ont aucune ligne avant 2018 (D2 : 0). Les taux « pour 100 habitants » ont Unit = « Nombre ».
  - **Rupture du mobile money** : 3 152 999 abonnés actifs en 2019, 2 438 561 en 2020, alors que la valeur des transactions passe de 909,5 à 1 446,4 Md FCFA. Changement de définition d'« actif » possible, non documenté (11.A20, validé : série entière, rupture signalée, aucune correction). Sur toute la période : 83 452 abonnés actifs et 0,75 Md FCFA de transactions en 2013 ; 3 005 048 et 2 865,7 Md en 2022.
  - **Face à l'ARCEP (AR1)** : les abonnements data mobile de 2b sont ceux du T4 de l'ARCEP en 2018 (3 660 055), 2020 (4 891 899) et 2022 (4 870 282), et les abonnés mobile money de 2022 aussi (3 005 048). Deux écarts :
    - **2021** : 2b (4 651 596) reprend la valeur **révisée** par l'ARCEP. Le numéro du T4 2021 annonçait 5 906 003, mais les numéros de 2022 révisent les 4 trimestres de 2021, de -13 à -21 % (révision méthodologique) ;
    - **2019** : la valeur de 2b (3 379 910) n'apparaît dans aucune publication de l'ARCEP (T4 2019 : 4 671 179). Même constat que pour D2 : origine inconnue.
- **Limites**
  - Pas de ventilation par technologie (2G, 3G, 4G, ADSL, FTTH) ni de taux de pénétration Internet : AR1 la donne à partir de 2018.
  - Pas d'abonnés à la téléphonie par opérateur : les parts de marché de la téléphonie s'arrêtent en 2019 dans D3 ; AR1 les prolonge jusqu'en 2026.
  - La description annonce la télévision numérique, une ventilation urbain / rural et les infrastructures (fibre, 4G, 5G) : absentes.
  - Télédensités, large bande fixe et CA diffèrent des autres sources (section 9).

**2c et 2d — Haut débit fixe pour 100 personnes (Banque mondiale)**

- Indicateur IT.NET.BBND.P2, taux seulement (C). 2c renseigne 2007-2023 ; 2d est identique sur cette période et ajoute 2024 (1,42).
- **Utilité** : contexte de O2-07. C'est le haut débit fixe toutes technologies, pas la seule fibre (FTTH).
- **Qualité** : creux en 2013-2014 (0,09 et 0,17, entre 0,58 en 2012 et 0,86 en 2015), rupture ou erreur probable. Le nombre d'abonnements correspondant (IT.NET.BBND, dans 3g) est lui aussi heurté : 66 100 en 2015, 26 200 en 2018, 114 000 en 2023. Diffère de la série INSEED de 2b (section 9).

**2e — Pénétration Internet (MESPTN) : train-full.csv et test.csv**

**Écarté définitivement le 26/09/2026 (11.C1)** : ni téléchargé ni utilisé dans la suite du projet. Le profil ci-dessous reste pour mémoire.

- Jeu préparé pour l'apprentissage automatique : prédire l'accès d'un ménage à Internet (fibre à domicile). train : 30 558 lignes x 4 043 colonnes ; test : 13 097 x 4 042 (sans la cible). **Non téléchargé** (3,26 Go) : profilé en flux le 25/09/2026, sans enregistrement, empreintes conformes au portail.
- Variables : type de logement, éclairage, énergie de cuisson, taille du ménage, 33 variables Oui / Non (codes H17 à H21, sans dictionnaire), opérateur (`Connexion`), 4 000 variables numériques sans nom (vraisemblablement des variables satellitaires MOSAIKS, non confirmé), cible `Accès internet` (0 / 1). Accents perdus à l'export.
- **Ce qu'il ne permet pas de dire**
  - Aucune date ni localisation : aucun croisement possible avec les séries annuelles ni avec le découpage administratif.
  - Cible équilibrée par construction (48,8 % de 1 dans train) : **il ne mesure pas un taux de pénétration**.
  - `Connexion` vide ⇒ cible à 0 sur les 10 508 lignes concernées : la variable contient la réponse.
- **Utilité pour le 02** : aucune directe. C'était la seule source ménage (demande) sur Internet des portails, mais elle est inutilisable pour O1-05 et O1-06, faute de lieu et de dictionnaire. Depuis le 26/09/2026, ces indicateurs reposent sur les enquêtes MICS6 et EHCVM (section 12). Téléchargement complet : décision en attente (11.C1).

### Données complémentaires téléchargées : objectifs 1 et 2

*Fichiers de `data/raw/_extradatas/`, retenus par le journal de recherche (décisions entre parenthèses). Profils complets : section 12.*

| Réf. | Fichier (dossier) | Ce qu'il apporte face aux limites de D2 | Indicateurs du 02 | Preuve |
| ---- | ----------------- | --------------------------------------- | ----------------- | ------ |
| AR1 | `obj1/AR1_arcep_observatoire/` (34 PDF) | Prolonge la série arrêtée en 2019 : abonnés data 2G, 3G, 4G et 5G par opérateur, Internet fixe et FTTH par opérateur, **du T1 2018 au T2 2026**, sans trimestre manquant. Raccord : D2 / 2b jusqu'en 2017, AR1 ensuite (P4) ; valeur du T4 par convention, moyenne des 4 trimestres en sensibilité (V1, R6) | O1-03, O1-04, O2-01, O2-07 | A |
| IN1 | `obj1/IN1_*` | Dénominateur des taux d'abonnements pour 100 habitants (P3, R2) | O1-03 (variante), O2-07 | C |
| AS1 | `obj1/AS1_inseed_annuaire-statistique-national-2024.pdf` | Séries télécom de l'INSEED prolongées jusqu'en 2024, au niveau national : contrôle de 2b et de AR1 | Contrôle | A à C |
| CH1 | `obj1/CH1_chronologie-evenements.csv` | Dates de lancement des technologies (3G de Moov en 2016, FTTH en 2017, 4G en 2018, premiers abonnés 5G au T2 2026) | O1-04 (lecture) | A ou C |

**Ce que ces compléments règlent** : les technologies après 2019 (O1-04), la 5G, la FTTH par opérateur (O2-07) et les parts de marché data jusqu'en 2026. Ils expliquent aussi deux anomalies de D2 : la baisse de Togocel en 2019 n'existe pas chez l'ARCEP, et la « 3G Atlantique Telecom » de 2018-2019 réunit la 3G et la 4G de Moov.

**Ce qui reste non résolu** :
- **Rupture du T1 2020** (S6) : la 3G de Togocel recule de 58 % et le total data mobile de 6,6 %, sans explication publiée. Aucune évolution par technologie n'est calculée à travers.
- Les valeurs 2019 de D2 et de 2b ont une origine inconnue : elles sont écartées par la règle de raccord (P4), pas expliquées.
- Toujours rien par territoire, ni urbain / rural, ni Wi-Fi.
- Des abonnements, jamais des utilisateurs : aucune de ces séries ne remplace O1-01.
- L'extraction des 34 PDF en table reste à faire (P5, étape de préparation) ; la technologie des fournisseurs fixes (CAFE, GVA, TEOLIS…) reste inconnue : ils sont classés « Fixe, technologie non précisée » (11.A3, validé).

---

## 3. D3 — Récapitulatif segment téléphonie et GSM

```
Dataset       : Récapitulation segment téléphonie et GSM au Togo
Fichier       : D3_recap-telephonie-gsm.csv
Source        : INSEED (publication opendata.gouv.tg)
Période       : 2013-2019
Unité d'obs.  : indicateur x année (format long)
Granularité   : National ; opérateur pour les parts de marché
Fréquence     : Annuelle
Lignes        : 70 (10 indicateurs x 7 ans, complet)
```

**Colonnes :** `indicateur`, `Unit` (Nombre, %, Francs CFA), `Date`, `Value`.

**Variables principales**

| Indicateur                                                 | Unité | Preuve | Contrôle                                     |
| ---------------------------------------------------------- | ------ | ------ | --------------------------------------------- |
| `Le nombre total d'abonnés fixe et mobile`              | Nombre | A      | = fixe + mobile GSM, exact sur 7 ans          |
| `Le nombre total d'abonnées mobiles GSM`                | Nombre | A      | —                                            |
| `Le nombre total d'abonnés fixe`                        | Nombre | A      | —                                            |
| `Part de marché Atlantique Telecom Togo (en abonnées)` | %      | C      | somme des 2 parts = 100,00 chaque année      |
| `Part de marché Togo Cellulaire (en abonnées) en %`    | %      | C      | idem                                          |
| `Chiffres d'Affaires`                                    | FCFA   | C      | 177 à 200 milliards selon l'année           |
| `Investissement`                                         | FCFA   | C      | 19 à 69 milliards selon l'année             |
| `ARPU segment mobile GSM`                                | FCFA   | C      | **anomalie d'échelle** (voir Qualité) |
| `Télédensité mobile GSM`, `Télédensité fixe`     | %      | C      | population implicite identique à celle de D2 |

**Utilité**

- → Objectif 2 : parts de marché et HHI (O2-01, 2 opérateurs), chiffre d'affaires du secteur et sa croissance (O2-03), taux d'investissement Investissement / CA (O2-04, classé optionnel dans le 02 mais **renseigné ici**).
- → Objectif 1 : contexte de pénétration mobile (télédensité).

**Qualité**

- Complet : 10 indicateurs x 7 ans, aucun doublon.
- **ARPU** : les valeurs vont de 2,4·10¹³ à 3,3·10¹³ FCFA, soit plus de 100 fois le chiffre d'affaires annuel. C'est impossible pour un revenu par abonné. Le ratio CA / abonnés mobiles / 12 donne 2 400 à 4 000 FCFA par mois, ce qui suggère un facteur 10¹⁰ (3 267 FCFA pour 2013). **Décision 11.A5 (26/09/2026)** : l'ARPU de D3 est écarté, sans correction ; l'ARPU est recalculé depuis AR1 (CA / abonnés moyens / 12, niveau B, 2018-2026) : c'est O2-05a (section 10).
- Les noms d'opérateurs du fichier (Atlantique Telecom, Togo Cellulaire) diffèrent de ceux de la description du jeu (Moov Africa, Togocom). 2b confirme la première correspondance : ses valeurs de « Moov Africa Togo » sont celles d'« Atlantique Telecom » dans D2 (11.A2). **Décision 11.A2 (26/09/2026)** : libellés « Moov Africa (Atlantique Telecom) » et « Togocom (Togo Cellulaire) ». La seconde correspondance est confirmée par l'ARCEP (AR1) : « Togocel » (abonnés) et « Togo Cellulaire » (CA) en 2018, « YAS Togo (Togo Cellulaire) » en 2026 pour le mobile ; « YAS Togo (Togo Telecom) » est l'opérateur fixe.

**Limites**

- **La description annonce des tarifs (appels, SMS, Internet mobile) et la qualité de service (couverture, débit) : rien de cela n'est dans le fichier.** Recherche dans tout le catalogue : aucun jeu de tarifs ; la couverture n'existe qu'en agrégat calculé par geodata (3i), les tours étant privées (3h). Hors catalogue (section 12) : paniers de prix de l'UIT (IT1), relevé et analyse des tarifs de l'ARCEP (AR5, AR6), campagnes de qualité de service de l'ARCEP (AR6).
- Le chiffre d'affaires et l'investissement ne sont **pas ventilés par opérateur** ici. **Correction du 26/09/2026** : l'observatoire de l'ARCEP (AR1) les ventile par opérateur, trimestre par trimestre, depuis 2018. O2-02 et O2-04 deviennent calculables sur 2018-2026 (section 12). Ce sont des flux : l'annuel est la somme des 4 trimestres, jamais la valeur du T4. L'investissement est très concentré en fin d'année (T4 2025 : 55 % de l'année).
- Le périmètre du CA et de l'investissement n'est pas documenté : secteur entier ou segment téléphonie / GSM ? CA net ou brut de taxes ? Le ratio de O2-04 n'a de sens que si les deux portent sur le même périmètre. Indice : 2b publie un « Chiffre d'affaires du secteur » qui s'écarte de celui de D3 de -1,3 % à +3,1 % selon l'année (2013-2019). Le CA de D3 couvre donc vraisemblablement tout le secteur (11.A4).
- **Série arrêtée en 2019.** Prolongements : abonnés fixe et mobile jusqu'en 2024 (3b à 3f), CA du secteur jusqu'en 2022 (2b), revenus et investissement jusqu'en 2010 vers le passé (3g). **Depuis le 26/09/2026**, AR1 couvre 2018-2026 pour les parts de marché de la téléphonie, le CA et l'investissement par opérateur ; l'ARPU se recalcule (CA / abonnés, 11.A5). **11.A4, validé le 26/09/2026** : 2b reste la série nationale du CA (2010-2022) et AR1 couvre 2018-2026, sans raccord, car 2b dépasse la somme des trimestres de l'ARCEP de 2,8 % en 2021 et de 3,7 % en 2022.

### Compléments : 3b à 3i

| #        | Fichier                                   | Source                             | Période                 | Apport                                                                                                    |
| -------- | ----------------------------------------- | ---------------------------------- | ----------------------- | --------------------------------------------------------------------------------------------------------- |
| 3b à 3e | 4 CSV `D3_abonnements-*`, `D3_telephonie-*` | Banque mondiale (UIT)           | 1960-2023               | Abonnements mobile et fixe, en nombre et pour 100 personnes                                              |
| 3f       | `D3_worldbank-api-*.json` (4 fichiers)   | API Banque mondiale                | 1960-2024               | Mêmes séries, valeurs exactes et révisées                                                               |
| 3g       | `D3_hdx-infrastructures.csv`             | HDX (indicateurs Banque mondiale)  | 1960-2023               | 47 indicateurs, dont 25 TIC : revenus et investissement télécoms, bande passante, haut débit fixe, usage par sexe |
| 3h       | `D3_metadonnees-tours-telecoms.csv`      | MESPTN                             | —                       | Schéma des tours télécoms ; données privées                                                             |
| 3i       | `D3_geodata-*.json` (30 fichiers)        | geodata.gouv.tg                    | Couches PRISE 2021/2022 | Couverture mobile, réseau fixe et agences Togocom, par unité administrative                              |

**3b à 3f — Abonnements mobile et fixe (Banque mondiale)**

- Nombre d'abonnements (A) et taux pour 100 personnes (C), séries annuelles nationales. 3f ajoute 2024 : 7 688 649 abonnements mobiles (80,80 pour 100) et 78 576 fixes (0,826 pour 100).
- **Utilité** : abonnés au-delà de 2019 (contexte de O1-02 et O2-01) ; population annuelle implicite (11.B5).
- **Qualité**
  - Les CSV du portail sont arrondis (abonnements mobiles à la dizaine de milliers depuis 2007, taux fixe à 3 chiffres significatifs) ; l'API (3f) donne les valeurs exactes.
  - 3f révise le taux mobile depuis 2000 (2019 : 73,72 contre 75,69 dans 3c) et les abonnements fixes de 2023 (69 808 contre 66 516).
  - Face à D3 : abonnés mobiles identiques en 2017-2019, plus nombreux en 2013-2016 (2013 : 4 262 993 contre 3 713 908) ; abonnés fixes identiques en 2014 et 2017-2019.
  - Nombre / taux donne la population utilisée par la source, la même pour le mobile et le fixe : 7,29 M en 2013, 8,46 M en 2019, 9,09 M en 2022, 9,52 M en 2024 (section 9).
- **Limites** : national ; aucun détail par opérateur ni par technologie.

**3g — Infrastructures (HDX)**

1 165 lignes, 47 indicateurs, format long ; la 2e ligne (balises HXL) est à écarter. 22 indicateurs (eau, routes, transport aérien, ports, énergie) sont hors sujet. Séries absentes des autres fichiers :

| Indicateur                                     | Code                                  | Période   | Usage                                               |
| ---------------------------------------------- | ------------------------------------- | --------- | --------------------------------------------------- |
| Revenus des services télécoms (FCFA)         | IT.TEL.REVN.CN                        | 1965-2010 | Historique de O2-03                                 |
| Investissement télécoms (FCFA ; % des revenus) | IT.TEL.INVS.CN, IT.TEL.INVS.RV.ZS   | 1981-2010 | Historique de O2-04                                 |
| Bande passante Internet internationale         | IT.NET.BNDW                           | 1998-2011 | Contexte ; ce n'est pas une qualité de service mesurée |
| Abonnements haut débit fixe (nombre)          | IT.NET.BBND                           | 2007-2023 | O2-07 (toutes technologies)                         |
| Utilisateurs d'Internet par sexe               | IT.NET.USER.FE.ZS, IT.NET.USER.MA.ZS  | 2017      | Contexte de O1-01                                   |

- **Qualité** : les séries de 3b à 3e y figurent, identiques. Revenus 2010 : 149,0 Md FCFA, contre 155,0 Md dans 2b (périmètre ou révision différents).
- **Limites** : indicateurs pré-calculés (C). Revenus et investissement s'arrêtent en 2010 : ils prolongent D3 vers le passé, jamais au-delà de 2019.

**3h — Tours télécoms : schéma seulement**

- 56 champs décrits : localisation, opérateur, propriétaire, hauteur, date de construction, équipements (GSM et son type, fibre, VSAT, faisceau radio), énergie, dates de collecte. Les données sont « privées, accessibles uniquement sur demande » auprès du MESPTN. Même situation pour les tours Moov et Togocom, les bâtiments des tours et le réseau téléphonique enterré et aérien.
- **Conséquence** : O2-08 (sites radio) reste impossible **par territoire**, comme une couverture par technologie (O2-06). Seule voie : une demande au producteur (11.C6). **Au niveau national**, le rapport d'activité 2025 de l'ARCEP donne le nombre de sites BTS par opérateur et par technologie, 2021-2025 (section 12).

**3i — Indicateurs geodata.gouv.tg : réseau et couverture**

6 indicateurs calculés par la plateforme, chacun à 5 niveaux (pays, 5 régions, 39 préfectures, 117 communes, 396 cantons), soit 558 lignes par indicateur, avec les codes territoriaux de la section 7.

| Indicateur                                                  | Calcul de la plateforme            | Valeur nationale | Preuve                                  |
| ----------------------------------------------------------- | ---------------------------------- | ---------------- | --------------------------------------- |
| Part des habitants à moins de 20 km d'une tour télécom   | `percentagePopulationTargetBuffer` | 88,37 %          | C                                       |
| Longueur de fibre enterrée                                 | `lineLength`                       | 2 162 km         | C                                       |
| Longueur de fibre aérienne                                 | `lineLength`                       | 3 071 km         | C                                       |
| Longueur de réseau ADSL et cuivre enterré                 | `lineLength`                       | 433 km           | C                                       |
| Nombre d'agences ou franchises Togocom                      | `count`                            | 62               | C (recomptable sur une couche ouverte) |
| Part des habitants à moins de 5 km d'une agence Togocom    | `percentagePopulationTargetBuffer` | 49,46 %          | C                                       |

- **Utilité**
  - Seule mesure territoriale de la couverture mobile : proxy de O2-06 et, par lui, de O4-06 et de la 3e dimension de O5-01 (11.A17).
  - Linéaire de fibre par territoire pour O2-07 ; gaps territoriaux d'infrastructure pour O5-02.
- **Qualité**
  - Cohérent d'un niveau à l'autre : la somme des régions donne la valeur nationale, à quelques mètres près pour les longueurs.
  - Couverture par région : de 57,68 % (Centrale) à 98,97 % (Maritime). 10 préfectures sont à 100 %.
  - **Valeurs impossibles : 0 % à Mô et à Kpendjal, 0,05 % à Tchamba.** D5 y compte 32, 41 et 205 points mobile money, qui ne fonctionnent pas sans réseau. La couche des tours est donc incomplète, au moins là. **Décision 11.A13 (26/09/2026)** : ces trois préfectures sont « Non déterminable » pour la couverture, jamais 0 %, sur les cartes comme dans O2-06, O4-06 et O5-01.
  - Fibre enterrée répartie entre les 5 régions (374 à 481 km) ; fibre aérienne à 85 % en Maritime (2 622 km) ; ADSL et cuivre : 285 km sur 433 en Maritime.
- **Limites**
  - Couverture théorique : rayon fixe de 20 km autour de toute tour, sans distinction 2G / 3G / 4G ni opérateur. Ce n'est pas la « population couverte en 3G et en 4G » que demande le 02.
  - Méthode et base de population non documentées (≈ 8,14 M d'habitants, d'après 4j et 5c) ; date de calcul inconnue.
  - Fibre : réseau de transport et réseau d'accès ne sont pas distingués, alors que le 02 interdit de les additionner. Stock sans date : pas de « km ajoutés ».
  - Aucun indicateur équivalent pour Moov.

### Données complémentaires téléchargées : objectif 2

*Fichiers de `data/raw/_extradatas/`, retenus par le journal de recherche (décisions entre parenthèses). Profils complets : section 12.*

| Réf. | Fichier (dossier) | Ce qu'il apporte face aux limites de D3 | Indicateurs du 02 | Preuve |
| ---- | ----------------- | --------------------------------------- | ----------------- | ------ |
| AR1 | `obj1/AR1_arcep_observatoire/` (34 PDF) | CA et investissement **par opérateur**, trimestriels, 2018-2025 (flux : l'annuel est la somme des 4 trimestres) ; abonnés à la téléphonie par opérateur jusqu'au T2 2026 | O2-01, O2-02, O2-03, O2-04, O2-05a | A |
| AR2 | `obj1/AR2_*2017*`, `obj2/AR2_*2025*` | Rapport 2025 : sites BTS et cellules par opérateur et par technologie, 2021-2025 ; rapport 2017 : lancement de la 3G de Moov (chronologie) | O2-08 (national) | A |
| IT1 | `obj2/IT1_uit_paniers-prix-tic_2008-2025.xlsx` | Coût de 1 Go de data mobile en % du RNB mensuel par habitant, 2023-2025 (5,30 % en 2025) ; avant 2023, d'autres paniers (1 Go postpayé sur ordinateur 2013-2017, 1,5 Go 2018-2020, 2 Go 2021-2025), jamais enchaînés (04, V6) ; tous pays | O2-05 | C |
| AR5, AR6 | `obj2/AR5_*`, `obj2/AR6_arcep_etudes/` | Tarifs de septembre 2023 et analyse d'avril 2023 ; qualité de service : campagne 2024 (94 localités, taux de conformité pour le Grand Lomé et le reste du pays) et analyses QoE nationales par opérateur (2025, 2026) | O2-05, O2-09 (national) | A à C |
| IN2, IN3 | `obj1/IN2_*`, `obj1/IN3a_*`, `obj1/IN3b_*` | Indices de prix de la communication, mensuels, 2010-2024 | O2-03 (en réel), O2-05 (contexte) | C |
| W2 | `obj1/W2_ehcvm/` (module communautaire) | Réception du réseau de chaque opérateur **déclarée** dans 540 localités, à confronter au proxy de couverture 3i (Q6) | O2-06 (contrôle) | B |

**Ce que ces compléments règlent** : les parts de marché et le CA par opérateur (O2-01, O2-02), le taux d'investissement (O2-04), l'ARPU recalculé et le coût de 1 Go (O2-05a, O2-05b) et les sites radio au niveau national (O2-08). Les tarifs et la qualité de service annoncés par la description de D3 existent hors du portail.

**Ce qui reste non résolu** :
- **Couverture par territoire (O2-06)** : toujours le proxy 3i, théorique, confronté à une réception déclarée ; jamais mesurée. Le tableau de bord doit le dire. Mô, Kpendjal et Tchamba : « Non déterminable » (11.A13).
- **Qualité de service par territoire (O2-09, optionnel) : non couverte** (S9). Tous les territoires sont « Non déterminable ».
- Sites radio par territoire (O2-08) : impossibles, les tours sont privées (11.C6).
- Périmètre du CA (net ou brut, secteur ou segment) non documenté ; 2b et AR1 ne se raccordent pas (+2,8 % en 2021, +3,7 % en 2022) : deux séries côte à côte, sans série continue 2010-2026 (11.A4, validé). ARPU de D3 écarté (11.A5, validé), recalculé depuis AR1 (O2-05a). Deux ruptures du CA : périmètre de Togo Telecom (fixe) au T2 2025 ; mobile money de YAS Togo non déclaré au T2 2026, qui touche O2-02 et O2-05a.

---

## 4. D4 — Établissements financiers

```
Dataset       : Établissements financiers au Togo
Fichiers      : D4_etablissements-financiers.csv
                D4_metadonnees-etablissements-financiers.csv (4b : dictionnaire)
Source        : Ministère de l'Économie et des Finances
Période       : Stock ; collecte « PRISE 2021/2022 » d'après geodata.gouv.tg ; export du 06/01/2025
Unité d'obs.  : établissement (un point par établissement)
Granularité   : Point GPS ; région, préfecture, commune, canton, localité
Fréquence     : Ponctuelle
Lignes        : 738
```

**Colonnes publiées (13 sur les 107 du dictionnaire) :** `FID`, `region_nom_bdd`, `prefecture_nom_bdd`, `commune_nom_bdd`, `canton_nom_bdd`, `nom_localite`, `etab_nom`, `etab_adresse`, `etab_jour`, `activite_statut`, `activite_categorie`, `toilette_type`, `geometry`.

**Champs du dictionnaire utiles au 02 mais absents du fichier :** `gab_nbr` et `gab_fct_nbr` (nombre de GAB), `guichet_nbr` (nombre de guichets), `activite_categorie_banque`, `client_parti` (nombre de clients), `date_collecte`, `date_mise_a_jour_collecte`, `couverture` et `couverture_type` (réception Internet sur place).

**Variables principales**

| Variable                                     | Contenu                                                                       | Preuve |
| -------------------------------------------- | ----------------------------------------------------------------------------- | ------ |
| `activite_categorie`                       | Micro-Finance 412, Banque 247, Assurance 69, Mutuelle 9, « Micro-Finace » 1 | A      |
| `activite_statut`                          | Utilisé 658 (+2 « Utilise »), Néant 50, autres modalités 28              | A      |
| `region/prefecture/commune/canton_nom_bdd` | Rattachement administratif, renseigné pour 100 % des lignes                  | A      |
| `geometry`                                 | WKT`POINT (lon lat)`, 100 % renseigné, 100 % dans l'emprise du Togo        | A      |
| `etab_nom`, `nom_localite`               | Nom de l'établissement, localité                                            | A      |

**Identifiants territoriaux :** noms uniquement (suffixe `_bdd`), pas de code. Le dictionnaire prévoit un `canton_id_bdd`, qui n'est pas publié. Les noms correspondent en revanche à 100 % aux unités codées de geodata (section 7).

**Couverture :** 5 régions, **38 préfectures sur 39** (Kpendjal : 0 établissement), 95 communes sur 117, 130 cantons. Répartition : Maritime 416 points (dont 304 dans le Grand Lomé), Plateaux 112, Kara 85, Centrale 63, Savanes 62. **Aucune assurance en Centrale ni dans les Savanes.**

**Utilité**

- → Objectif 3 : points de service formels par type et par territoire (O3-01), part du Grand Lomé (O3-02).
- → Objectif 4 : dénominateur « points formels » de O4-01, O4-03 et O4-05, numérateur de O4-02.

**Qualité**

- Aucun doublon de ligne ni d'identifiant ; aucune coordonnée dupliquée ni nulle.
- **Coordonnées cohérentes avec les unités déclarées** : 100 % des points sont dans le polygone de leur région, préfecture, commune et canton (6b).
- **Modalités à harmoniser :** « Micro-Finace » (1 ligne) ; « Utilisé » et « Utilise » ; « Nsp » et « Nsp  » (espace final) ; « jeudi » et « Jeudi », avec un ordre des jours variable dans `etab_jour` ; `nom_localite` tantôt en majuscules, tantôt en minuscules, avec des espaces finaux.
- **Statut d'activité :** 658 points « Utilisé ». Les autres points sont fermés, en construction, abandonnés, inachevés, en réfection, sans local ou en location (17), de statut inconnu (Néant 50, Nsp 3, N/a 1, Autre 7), ou ont une variante orthographique de « Utilisé » (2). **Décision 11.A6 (26/09/2026)** : seuls les 660 points « Utilisé » (variantes orthographiques comprises) comptent comme points de service ; les autres statuts servent au test de sensibilité.
- **Catégorie « Mutuelle » :** 9 points, alors que 27 autres établissements nommés « Mutuelle… » sont classés Micro-Finance. Leur rattachement (IMF ou assurance) conditionne O4-01 par type. **Décision 11.A7 (26/09/2026)** : ils sont classés IMF.
- **38 paires de points à moins de 30 m.** Ce sont surtout des établissements différents dans le même bâtiment (ex. SUNU Bank et SUNU Assurance, à 10 m l'un de l'autre). Au moins un cas ressemble à un doublon (FUCEC Togo Afagnan et COOPEC Afagnan, à 6 m).
- `etab_adresse` inutilisable : « Néant » ou « Nsp » dans 275 cas sur 738.
- `toilette_type` : sans rapport avec le sujet.
- Les jeux MEF par catégorie (banques, microfinances, assurances, mutuelles) et « Établissements de Finance » du portail sont des copies exactes de lignes de D4 ; seul le `FID` change. Ce n'est donc pas un identifiant stable d'un export à l'autre.

**Limites**

- **Pas d'ATM dans ce fichier.** Ils sont dans 4c (184 sites) : la version « par type » de O4-01 et la règle 5 de O4-05 deviennent calculables.
- **Date de collecte non publiée sur opendata** (le champ existe dans le dictionnaire). geodata.gouv.tg déclare « Campagne de collecte PRISE - 2021/2022 » pour cette couche (11.A10).
- **Zéro ou absence de collecte ?** Rien dans le fichier ne permet de distinguer une commune sans établissement d'une commune non enquêtée. Cela touche 22 communes et la préfecture de Kpendjal. Kpendjal n'a pas non plus de DAB (4c), mais D5 y compte 41 points mobile money : le territoire a bien été parcouru par la collecte (11.A13, validé : vrai zéro avec avertissement).
- Un point = un établissement, sans nombre de guichets : on ne mesure pas la capacité d'accueil.
- Aucun jeu localisé d'agences de transfert d'argent, et aucun champ sur les services proposés, alors que la description du jeu les annonce. **Agences de la Poste** : absentes de D4, elles sont dans une couche ouverte de geodata, téléchargée le 26/09/2026 (GD1 : 95 agences, dont 84 « Utilisé »). Décision Q5 : elles sont comptées à part, en test de sensibilité (épargne et mandats, mais ni banque ni IMF).

### Compléments : 4b à 4j

| #  | Fichier                                              | Source                              | Période                  | Apport                                                                                          |
| -- | ---------------------------------------------------- | ----------------------------------- | ------------------------ | ----------------------------------------------------------------------------------------------- |
| 4b | `D4_metadonnees-etablissements-financiers.csv`     | MEF                                 | —                        | Dictionnaire de D4 (107 champs)                                                                 |
| 4c | `D4_distributeurs-de-billets.csv`                  | MEF                                 | Collecte PRISE 2021/2022 | 184 sites de DAB géolocalisés                                                                 |
| 4d | `D4_metadonnees-distributeurs-de-billets.csv`      | MEF                                 | —                        | Dictionnaire de 4c (26 champs)                                                                  |
| 4e | `D4_*-adultes.csv` (4 fichiers)                    | Banque mondiale (FMI, FAS)          | 2004-2022                | Agences et DAB pour 100 000 adultes, déposants et emprunteurs pour 1 000 adultes              |
| 4f | `D4_worldbank-api-*-adultes.json` (4 fichiers)     | API Banque mondiale                 | Jusqu'en 2024            | Mêmes séries, révisées                                                                        |
| 4g | `D4_hdx-secteur-financier.csv`                     | HDX (Banque mondiale, Findex, GFDD) | 1960-2023                | 135 indicateurs : détention et usage d'un compte, inflation, envois de fonds                 |
| 4h | `D4_worldbank-api-findex-*.json` (3 fichiers)      | API Banque mondiale (Findex)        | 2011-2024                | Détention d'un compte, dont la vague 2024                                                     |
| 4i | 3 CSV INSEED des services financiers postaux         | INSEED                              | 2010-2022                | Nombre d'opérations d'épargne, de chèques postaux et de mandats                              |
| 4j | `D4_geodata-*.json` (50 fichiers)                  | geodata.gouv.tg                     | Couches PRISE 2021/2022  | Comptages, habitants par agence, distances, par unité administrative                          |

**4c — Distributeurs automatiques de billets (MEF)**

```
Fichier       : D4_distributeurs-de-billets.csv (+ dictionnaire 4d)
Source        : Ministère de l'Économie et des Finances
Période       : Stock ; collecte « PRISE 2021/2022 » d'après geodata.gouv.tg ; export du 02/01/2025
Unité d'obs.  : site de DAB (un point par site, pas par appareil)
Granularité   : Point GPS ; région, préfecture, commune, canton, localité
Lignes        : 184 (10 colonnes sur les 26 du dictionnaire)
```

**Colonnes :** `FID`, `region_nom_bdd`, `prefecture_nom_bdd`, `commune_nom_bdd`, `canton_nom_bdd`, `nom_localite`, `dab_type`, `etab_nom`, `banque`, `geometry`.

| Variable     | Contenu                                                                                                      | Preuve |
| ------------ | ------------------------------------------------------------------------------------------------------------ | ------ |
| `dab_type` | Dans une banque 126, indépendant 53, dans un autre établissement 5                                        | A      |
| `banque`   | ECOBANK 41, ORABANK 34, UTB 30, Banque Atlantique 14, BTCI 11… ; « AUTRE » 5 ; SPT (la Poste) 4          | A      |
| `geometry` | WKT `POINT (lon lat)`, 100 % dans l'emprise du Togo, aucun doublon de position                             | A      |

- **Couverture** : Maritime 119 sites, dont 107 dans les préfectures de Golfe et d'Agoè-Nyivé (le Grand Lomé) ; 22 préfectures sur 39 ont au moins un site ; Kpendjal : 0.
- **Utilité** : ATM de O3-01 ; O4-01 par type et diversité des types ; règle 5 de O4-05 (11.A9) ; volet ATM de O4-02.
- **Qualité** : `etab_nom` vide ou « Nsp » pour 46 sites. Aucun site n'est à la même position qu'une banque de D4 : rattacher un DAB à une agence demandera une jointure par distance. 100 % des sites sont dans le polygone de leur unité déclarée (6b).
- **Limites** : une ligne = un site. Le nombre d'appareils (`dab_nbr`, `gab_nbr`) et le nombre d'appareils en service (`dab_fct_nbr`) ne sont pas publiés. Les sites ne se comparent donc pas aux « DAB pour 100 000 adultes » de 4e et 4f, qui comptent des appareils (11.A19).

**4b et 4d — Dictionnaires**

- Champs prévus mais non publiés : `guichet_nbr`, `gab_nbr`, `gab_fct_nbr`, `personnel_nbr`, `etab_heure`, `date_collecte` (4b) ; `dab_nbr`, `gab_nbr`, `dab_fct_nbr`, `dab_clos_nbr`, `date_collecte` (4d). Aucun champ sur les services proposés.
- 4b sert aussi de dictionnaire aux jeux MEF par catégorie et au jeu MINARM « Banques au Togo », dont les données sont privées.

**4e et 4f — Densité nationale pour les adultes (FMI, Financial Access Survey)**

- Indicateurs pré-calculés (C), nationaux : agences de banques commerciales et DAB pour 100 000 adultes ; déposants et emprunteurs pour 1 000 adultes.
- 4e (CSV du portail) : agences 2004-2022, DAB 2014-2021, déposants 2004-2022, emprunteurs 2019-2022. 4f (API) révise toutes les années à la baisse (de 2 à 3 % ; de 4 à 9 % pour les DAB) et va jusqu'en 2024 : 4,38 agences et 6,93 DAB pour 100 000 adultes, 197,2 déposants et 37,2 emprunteurs pour 1 000 adultes. Les agences reculent depuis 2020 (5,29).
- **Utilité** : seul repère national pour O4-02, que le 02 rapporte aux adultes (norme FAS). Il ne remplace pas la population de 15 ans et plus par territoire (11.B1).

**4g — Secteur financier (HDX)**

3 348 lignes, 135 indicateurs, format long ; la 2e ligne (balises HXL) est à écarter. Indicateurs pré-calculés ou issus d'enquêtes (C).

| Bloc                  | Contenu utile                                                                                                                                                   | Période                 |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| Findex (demande)      | Part des 15 ans et plus ayant un compte, mobile money compris : 10,19 % (2011), 18,25 % (2014), 45,29 % (2017), 49,61 % (2021) ; par sexe, revenu, âge, éducation | 2011, 2014, 2017, 2021  |
| GFDD (accès, usage)  | Compte dans une institution financière : 24,9 % (2021) ; téléphone utilisé pour envoyer de l'argent : 17,9 %, pour payer des factures : 7,0 % (2021)     | 2014-2021               |
| Prix                  | Inflation annuelle (prix à la consommation) ; déflateur du PIB                                                                                              | 1967-2022 ; 1990-2023   |
| Envois de fonds       | Envois reçus (USD) ; coût moyen d'un envoi vers le Togo (%)                                                                                                 | 1974-2023 ; 2016-2023   |
| Offre                 | Les 4 séries de 4e, identiques                                                                                                                                | 2004-2022               |

- **Utilité**
  - La **source de demande** que la procédure exige à l'étape 03, au niveau national : détention d'un compte pour O3-04.
  - L'**inflation** rend calculable la croissance réelle du CA de O2-03 (11.B6).
- **Qualité**
  - DAB pour 100 000 adultes selon la GFDD (GFDD.AI.25) différent de la série FAS (2017 : 3,98 contre 5,45).
  - Envois de fonds reçus : même valeur de 2020 à 2023 (650 385 610 USD), valeur reconduite probable.
  - Compte dans une institution financière : 34,1 % en 2017, 24,9 % en 2021, alors que la détention totale augmente. À vérifier avant usage.
- **Limites** : national. Le coût des envois de fonds porte sur les transferts internationaux, pas sur les frais domestiques du mobile money (O3-06). Pas de vague Findex 2024 (voir 4h).

**4h — Findex par l'API Banque mondiale**

- Trois codes de 4g interrogés dans leur version récente : détention d'un compte pour l'ensemble des adultes, les femmes et les 40 % les plus pauvres. Ajoute la vague 2024 : 57,4 % des adultes ont un compte (49,6 % en 2021) ; femmes 45,3 % (44,3 %) ; 40 % les plus pauvres 43,7 % (39,0 %).
- La page de 4g ne renvoie pas vers l'API : les codes viennent du fichier. Conservation validée le 26/09/2026 (11.C2).

**4i — Services financiers postaux (INSEED)**

- Nombre d'opérations par an : épargne (versements et paiements, 2010-2022), chèques postaux (2013-2019), mandats express internationaux (émissions et paiements, 2010-2022). Seuls les nombres sont publiés : les montants, comptes actifs et frais annoncés par les descriptions sont absents.
- **Qualité** : mandats émis de 1 837 (2016) à 0 (2022) ; paiements de 85 991 en 2010 à 11 754 en 2011, saut à vérifier.
- **Utilité** : contexte seulement (« autres structures » et transfert d'argent, dans la description de D4). Aucun indicateur du 02 ne l'utilise, et rien n'est localisé.

**4j — Indicateurs geodata.gouv.tg : établissements financiers**

10 indicateurs x 5 niveaux (558 lignes par indicateur), avec les mêmes codes territoriaux que 3i et 5c.

| Indicateur                                                                      | Calcul                               | Valeur nationale                           | Preuve                          |
| ------------------------------------------------------------------------------- | ------------------------------------ | ------------------------------------------ | ------------------------------- |
| Nombre d'agences bancaires / de microfinance / d'assurance                      | `count`                              | 247 / 412 / 69                             | C, égal à nos comptages (A)   |
| Nombre de DAB                                                                   | `count`                              | 184 (sites)                                | C, égal à 4c                  |
| Habitants par agence de microfinance / d'assurance                              | `popRatio`                           | 19 766 / 118 024                           | C                               |
| Habitants à plus de 10 km d'une banque, d'une microfinance ou d'une assurance   | `countPopulationTargetBuffer`        | 1 478 365                                  | C                               |
| Part des habitants à plus de 10 km d'une banque ou d'une microfinance          | `percentagePopulationTargetBuffer`   | 18,16 % (de 2,0 % en Maritime à 39,92 % en Kara) | C                         |
| Agences et franchises de la Poste ; part des habitants à moins de 5 km         | `count` ; `percentagePopulationTargetBuffer` | 95 ; 57,44 %                       | C                               |

- **Utilité** : contrôle de O3-01, O4-01 et O4-04 (11.A18). La distance à un établissement ajoute une lecture que le 02 ne prévoit pas (contexte de O4-05).
- **Qualité**
  - geodata compte **toutes** les lignes, quel que soit le statut d'activité : ses 247 banques incluent les 34 qui ne sont pas « Utilisé ». Ses 412 microfinances excluent « Micro-Finace » et les Mutuelles (11.A6, A7).
  - Base de population : habitants par agence x nombre d'agences = 8,14 M, comme pour 5c, proche du RGPH 2022 (8,10 M).
  - « Habitants par agence » est vide exactement là où il n'y a aucune agence : c'est une absence de valeur, pas un zéro.
  - Par préfecture : 17 sans DAB, 7 sans agence bancaire ; Kpendjal a 100 % de ses habitants à plus de 10 km d'un établissement.
- **Limites** : pas d'« habitants par agence bancaire » ni « par DAB » ; méthode, base de population et date de calcul non documentées.

### Données complémentaires téléchargées : objectifs 3 et 4

*Fichiers de `data/raw/_extradatas/`, retenus par le journal de recherche (décisions entre parenthèses). Profils complets : section 12.*

| Réf. | Fichier (dossier) | Ce qu'il apporte face aux limites de D4 | Indicateurs du 02 | Preuve |
| ---- | ----------------- | --------------------------------------- | ----------------- | ------ |
| GD1 | `obj3/GD1_*` (geodata) | Les 95 agences de la Poste (84 « Utilisé ») absentes de D4, comptées à part en test de sensibilité (Q5) | O3-01, O4-01 | A |
| RG2, RG3 | `obj4/RG_rgph5_livrets/` (transcriptions) | 15 ans et plus et milieu urbain / rural par préfecture et par commune, totaux égaux à D6 : source de population des objectifs 3 et 4 (R4, S5) | O3-02 (strate urbaine), O4-01, O4-02, O4-05 | A |
| C5 | `obj4/C5_worldbank-fas-uemoa_agences-dab-100000-adultes.csv` | Repère UEMOA des points formels : moyenne des 8 pays, agences comparées par territoire, DAB au niveau national seulement, échelle ramenée à 10 000 adultes (R1, S2 à S4) | O4-02 | C |
| BC2 | `obj4/BC2_*` (BCEAO) | Taux global de la BCEAO (mobile money compris) pour la variante « tous points de service », qui n'est pas O4-02 (R1) ; points bancaires (629) et de microfinance (625) du Togo en 2024 | Variante de O4-02 | C |
| W2, W4 | `obj1/W2_ehcvm/`, `obj1/W4_afrobarometre/` | Couche de **demande** : compte en banque, à la Poste ou en IMF, tontines (EHCVM) ; compte bancaire et présence d'une banque ou d'une IMF dans la zone (Afrobaromètre), par région | Contexte des objectifs 3 et 4 | B, C |
| IN4 | `obj4/IN4_*` | Accès à l'électricité par préfecture, 2018-2021 (ancien découpage) | Contexte des objectifs 4 et 5 | C |
| GD2 | `obj5/` (24 couches GeoJSON) | Lieux candidats : 1 078 marchés, 15 454 établissements scolaires, 2 271 formations sanitaires, 1 576 établissements administratifs. **Non requis par les 5 objectifs** : conservé sans traitement, pour un prolongement éventuel (11.G) | Aucun (étape 11, si besoin) | A |

**Ce que ces compléments règlent** : la Poste comme type de point formel ; le dénominateur « adultes » et la strate urbaine par territoire (O3-02, O4-02) ; le repère UEMOA de O4-02 ; les règles de comptage, validées le 26/09/2026 : statut « Utilisé » seul (A6), « Mutuelle » en IMF (A7), règle des 4 types avec les sites de DAB (A9), date de référence 2021/2022 (A10).

**Ce qui reste non résolu** :
- Zéro ou absence de collecte dans 22 communes et à Kpendjal : traité par convention (A13, validé : vrai zéro avec avertissement), sans preuve dans le fichier ; nombre de guichets et services proposés toujours non publiés (B8).
- Aucun repère UEMOA pour les IMF, les assurances et la Poste (S3) ; les DAB (sites) ne se comparent pas aux DAB du FAS (appareils).
- Aucune agence de transfert d'argent localisée ; date de collecte 2021/2022, un an au plus d'écart avec le RGPH (A10).

---

## 5. D5 — Agents mobile money

```
Dataset       : Agents Mobile Money au Togo
Fichiers      : D5_agents-mobile-money.csv
                D5_metadonnees-agents-mobile-money.csv (5b : dictionnaire)
Source        : Ministère de l'Efficacité du Service Public et de la Transformation Numérique
Période       : Stock ; collecte « PRISE 2021/2022 » d'après geodata.gouv.tg ; export du 19/12/2024
Unité d'obs.  : point de service (un point peut servir 1 ou 2 opérateurs)
Granularité   : Point GPS ; région, préfecture, commune, canton
Fréquence     : Ponctuelle
Lignes        : 19 788
```

**Colonnes publiées (7 sur 46) :** `FID`, `region_nom_bdd`, `prefecture_nom_bdd`, `commune_nom_bdd`, `canton_nom_bdd`, `operateur`, `geometry`.

**Champs du dictionnaire utiles au 02 mais absents du fichier :** `service` (type de service rendu), `agent_nbr` (nombre d'agents au point), `transfert_nbr`, `flooz` et `tmoney` (service de chaque opérateur), `date_collecte`, `lieu`.

**Variables principales**

| Variable                                     | Contenu                                                                                           | Preuve |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------- | ------ |
| `operateur`                                | « Moov, Togocom » 12 649 (64 %) ; Togocom 4 773 ; Moov 1 018 ; Nsp 1 348 (6,8 %)                | A      |
| `region/prefecture/commune/canton_nom_bdd` | 5 régions,**39 préfectures sur 39, 117 communes sur 117**, 372 cantons ; 100 % renseigné | A      |
| `geometry`                                 | WKT`POINT (lon lat)`, 100 % renseigné, 100 % dans l'emprise du Togo                            | A      |

**Répartition :** Maritime 8 986 points (dont 6 519 dans le Grand Lomé), Plateaux 3 079, Kara 2 951, Savanes 2 679, Centrale 2 093.

**Utilité**

- → Objectif 3 : points mobile money par territoire (O3-03).
- → Objectif 4 : numérateur de O4-03 (agents par guichet), O4-04 (habitants par agent), O4-05 (règles 2 et 3 : territoires desservis uniquement par le mobile money).
- → Contrôle de plausibilité des autres sources : la présence de points prouve qu'un territoire a été enquêté (11.A13) et qu'il reçoit un réseau mobile (3i).

**Qualité**

- Aucun doublon de ligne ni d'identifiant ; aucune coordonnée exactement dupliquée.
- **974 points partagent une cellule d'environ 11 m** avec un autre point (509 en surplus). Il peut s'agir de doublons ou de plusieurs kiosques côte à côte (marchés, gares routières). Rien dans le fichier ne permet de trancher.
- `operateur = Nsp` : 1 348 points, présents dans toutes les régions.
- **Coordonnées et unités déclarées (contrôle par 6b)** : de 99,63 % (commune) à 99,75 % (région, canton) des points sont dans le polygone de leur unité déclarée. Écarts :
  - 49 points hors du territoire (Cinkassé 36, Binah 8, Tône 3, Kpendjal 2), à 565 m de la frontière en médiane et 1,35 km au plus : des positions de bord de frontière ;
  - 22 points dans les zones où les contours des communes débordent de leur préfecture (Hahomégbé, Gbodjomé, Loko d'Oti 2) ;
  - 25 points dans 3 cantons que la base rattache à une autre commune que celle de leur polygone (Agome-Glozou, Akpakpakpé, Yokélé).
  Les 47 derniers tiennent aux contours et au rattachement des cantons, pas à la position des points : chacun est dans le polygone de son canton déclaré. Pour les 49 points frontaliers, rien ne dit si c'est le point ou le contour qui est en cause (11.A21, validé : rattachement par les noms déclarés, aucun point perdu).
- **Cohérence avec les sources nationales** (26/09/2026) :
  - l'ARCEP compte 33 924 points de vente mobile money au T4 2021 (AR1). D5 recompté par opérateur, un point « Moov, Togocom » valant deux points de vente et un point sans opérateur valant un, donne environ 32 400 (32 437 ; de 31 089 à 33 785 selon le sort des 1 348 points sans opérateur). D5 est donc cohérent avec l'ARCEP à la date PRISE ;
  - depuis, le réseau a presque doublé : 64 540 points de vente au T2 2026 (ARCEP) ; 81 137 points de monnaie électronique en 2024, dont 65 043 actifs, pour la BCEAO (BC2). **D5 est un stock de 2021/2022, à ne pas présenter comme l'état actuel.**

**Limites**

- **Une ligne est un point de service, pas un agent.** Un point « Moov, Togocom » est un seul lieu servant deux réseaux. Le nombre d'agents par point (`agent_nbr`) n'est pas publié. Les indicateurs du 02 qui parlent d'« agents » compteront donc des **points**, comme O4-04 l'avait prévu (« préciser si le comptage porte sur des agents ou sur des points de vente »).
- **Le périmètre dépasse peut-être le mobile money.** D'après les métadonnées, la liste couvre aussi des « points de recharge de crédit, de transfert d'argent, de paiement des factures ». Le champ `service`, qui permettrait d'isoler le mobile money, n'est pas publié.
- **Aucune distinction entre agents enregistrés et actifs**, contrairement à ce que demande O3-03. Seul repère, national : 80,2 % des points de monnaie électronique du Togo sont actifs (au moins une transaction en 90 jours) en 2024 (BCEAO, BC2).
- **Les champs manquants ne sont récupérables nulle part** : geodata.gouv.tg a les 46 champs, mais en masque les valeurs (« N/A »), et les couches par opérateur (Moov, Togocom) sont privées.
- Date de collecte non publiée sur opendata ; « Campagne de collecte PRISE - 2021/2022 » d'après geodata (11.A10).
- Pas de nom de localité, contrairement à D4.

### Compléments : 5b, 5c et page geodata.gouv.tg

**5b — Dictionnaire**

- 46 champs, la plupart sans libellé. `_PROJECT.txt` le présente comme la 2e « URL Data » du dataset 5 : c'est le dictionnaire, pas un fichier de données. C'est aussi le schéma des jeux privés « Agents Mobile Money MOOV » et « TOGOCOM ».

**5c — Indicateurs geodata.gouv.tg : mobile money**

| Indicateur                                         | Calcul                               | Valeur nationale | Par préfecture                          | Preuve |
| -------------------------------------------------- | ------------------------------------ | ---------------- | ---------------------------------------- | ------ |
| Habitants par point mobile money                   | `popRatio`                           | 412              | De 154 (Kozah) à 3 018 (Blitta)        | C      |
| Part des habitants à moins de 1 km d'un point     | `percentagePopulationTargetBuffer`   | 70,48 %          | De 36,48 % (Kpendjal) à 92,92 % (Golfe) | C      |

- **Utilité** : contrôle de O4-04, que l'on recalcule avec D5 et D6 (11.A18). La distance à un point est une lecture que le 02 ne prévoit pas.
- **Qualité**
  - Habitants par point x points de D5 = 8,14 M, proche du RGPH 2022 (8,10 M) ; écart par région de -9 % (Kara) à +3 % (Plateaux). geodata compte des points, comme D5, y compris les points « Nsp ».
  - 23 cantons sans valeur d'habitants par point (aucun point) : une absence de valeur, pas un zéro. De 0 à 5 % de leurs habitants sont à moins de 1 km d'un point.
- **Limites** : méthode et base de population non documentées ; date de calcul inconnue.

**Page geodata.gouv.tg du dataset 5 (fiche 7 de l'inventaire)**

- L'export de la couche est identique à D5 ligne à ligne (19 788 lignes, 7 colonnes ; seul le `FID` change) : **il n'existe pas de couche plus complète** (11.B9, résolu).
- Source de collecte déclarée : « Campagne de collecte PRISE - 2021/2022 », comme pour D4, 4c et les tours télécoms.
- La plateforme publie 177 couches ouvertes et 239 indicateurs (`data/raw/_metadata/geodata_open_data_config.json`). Les limites administratives ont été téléchargées depuis (6b), puis les lieux candidats et les agences de la Poste le 26/09/2026 (GD2, GD1 : section 12).

### Données complémentaires téléchargées : objectifs 3 et 4

*Fichiers de `data/raw/_extradatas/`, retenus par le journal de recherche (décisions entre parenthèses). Profils complets : section 12.*

| Réf. | Fichier (dossier) | Ce qu'il apporte face aux limites de D5 | Indicateurs du 02 | Preuve |
| ---- | ----------------- | --------------------------------------- | ----------------- | ------ |
| AR1 | `obj1/AR1_arcep_observatoire/` | Mobile money par opérateur depuis le T4 2021 : comptes, points de vente (33 924 au T4 2021, 64 540 au T2 2026) et valeur des transactions. Contrôle de D5 : ses points, recomptés par opérateur (environ 32 400), sont proches des 33 924 de l'ARCEP | O3-03 (contrôle), O3-04 | A |
| BC1 | `obj3/BC1_*` (BCEAO) | Togo 2024 : 12 553 441 comptes ouverts, dont 6 069 075 actifs à 90 jours ; 81 137 points de service, dont 65 043 actifs (80,2 %) : **seule mesure des actifs**, nationale (Q7) | O3-03, O3-04 | C |
| BC2 | `obj4/BC2_*` (BCEAO) | Mêmes grandeurs pour les 8 pays de l'UEMOA : repère régional | O3-04 (repère) | C |
| TF1 | `obj3/TF1_tarifs-mobile-money_2026-09-26/` (5 instantanés) | Frais de retrait et de transfert : grille officielle de Flooz ; Mixx partiel, sans grille officielle de retrait (R3) | O3-06 | C |
| W4 | `obj1/W4_afrobarometre/` (vagues 9 et 10) | Détention d'un compte mobile money par région (2022, 2024), 1 200 personnes par vague | O3-05 | C |
| W3 | `obj1/W3_findex2025/` | Détention d'un compte mobile money, 15 ans et plus, urbain / rural (2024) | O3-04, O3-05 | C |
| RG2, RG3 | `obj4/RG_rgph5_livrets/` | Population totale et 15 ans et plus par préfecture et par commune (R4, S5) | O4-04 (dont variante adultes), O4-05 | A |

**Ce que ces compléments règlent** : le stock de D5 est confirmé par l'ARCEP à la date de collecte ; les comptes et transactions (O3-04) ; une part d'actifs, nationale ; le coût du mobile money (O3-06, en partie) ; l'usage par région (O3-05, en partie) ; le ratio par adulte (O4-04).

**Ce qui reste non résolu** :
- Des **points**, jamais des agents : le nombre d'agents par point n'existe nulle part (11.A8, validé : on compte des points, sans dédoublonnage).
- Les agents actifs n'existent qu'au niveau national (80,2 %) : aucune part d'actifs par territoire (O3-03).
- Le périmètre des points (mobile money seul, ou aussi recharge et paiement de factures) reste inconnu : le champ `service` n'est pas publié.
- O3-05 repose sur de petits échantillons (coefficient de variation à contrôler région par région) ; O3-06 n'a ni grille officielle de retrait pour Mixx ni historique.

---

## 6. D6 — Recensement général de la population (RGPH 2022)

```
Dataset       : Recensement Général de la Population et de l'Habitat
Fichier       : D6_rgph.csv
Source        : INSEED
Période       : 2022
Unité d'obs.  : unité administrative (tous niveaux mélangés dans une colonne)
Granularité   : Pays -> région -> préfecture -> commune -> canton (quartier dans le Grand Lomé)
Fréquence     : Ponctuelle (recensement)
Lignes        : 759
```

**Colonnes :** `indicateur` (une seule valeur), `découpage-administratif`, `sexe` (toujours « Total »), `Unit`, `Date` (2022), `Value`.

**Structure reconstituée.** Aucune colonne n'indique le niveau administratif. Il se déduit de l'ordre des lignes, et l'emboîtement a été vérifié : chaque total est exactement la somme de ses composantes.

| Niveau         | Lignes                       | Remarque                                                                                                     |
| -------------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Pays           | 1                            | TOGO = 8 095 498 = somme des 6 unités de niveau région                                                     |
| Région        | 6                            | 5 régions +**« DAGL »** (District autonome du Grand Lomé, 2 188 376), sans ligne propre dans D4/D5 |
| Préfecture    | 39                           | dont l'en-tête d'Avé libellé**« TOTOAL AVE »**                                                    |
| Commune        | 116 lignes pour 117 communes | voir anomalies                                                                                               |
| Infra-communal | 597                          | cantons hors Grand Lomé ;**quartiers** dans le Grand Lomé (222 lignes)                               |

**Anomalies de libellés.** Elles sont toutes corrigeables, et les totaux restent justes.

- « BINAH2 » sans espace (Binah 2).
- « DANYI 1+DANYI 2 » : les deux communes de Danyi sont **fusionnées** sur une seule ligne (40 240 habitants).
- « AMOU 2 » apparaît deux fois (40 016 et 54 410) : le second est vraisemblablement Amou 3.
- « EST-MONO 1 » apparaît deux fois (34 652 et 27 942) : le second est vraisemblablement Est-Mono 3.
- Noms en majuscules sans accents. Certains noms désignent à la fois une préfecture et un canton (CINKASSE, BASSAR, TCHAMBA, SOTOUBOUA, ANIE), ou deux cantons différents (LOKO, GAME, KAMINA, ATSANVE, ANYIGBE, AGOTIME).

**Utilité**

- → Objectif 4 : dénominateur « population » de O4-01 et O4-04, pondération de O4-06 et de O5-01.
- → Objectif 3 : poids démographique du Grand Lomé (O3-02).

**Qualité**

- Aucune valeur manquante, aucun doublon de ligne.
- Contrôle croisé : une fois les libellés corrigés, les communes correspondent une à une aux communes codées de geodata, Danyi excepté (section 7). Cela confirme les corrections d'Amou 3 et d'Est-Mono 3. **Le livret 03 du RGPH-5 les confirme aussi** (26/09/2026) : ses 117 communes ont exactement les effectifs de D6 sous les noms corrigés (Amou 3 : 54 410 ; Est-Mono 3 : 27 942 ; Binah 2 : 40 160).
- Les indicateurs de geodata reposent sur une population de 8,14 M, 0,6 % au-dessus du RGPH : même ordre de grandeur, mais pas la même base.

**Limites**

- **Population totale uniquement.** Pas de ventilation par sexe malgré le libellé, **pas de population de 15 ans et plus** (dénominateur de O4-02, O4-04 variante adultes, O3-04), pas de ménages (O2-07), pas de milieu urbain / rural (strate de O3-02). **Correction du 26/09/2026** : la phrase « Aucun complément ne comble ces manques » ne tient plus. Les livrets 02 et 03 du RGPH-5 (RG2, RG3, section 12) donnent, **pour la même opération de recensement**, la population par groupe d'âges, milieu et sexe de chaque préfecture et de chaque commune. Leurs totaux sont égaux à ceux de D6. Les ménages restent absents. **Décision R4 (26/09/2026)** : RG2 et RG3 deviennent la **source de population des objectifs 3 et 4** (âge, milieu, tout ratio territorial), parce qu'ils apportent tout ce que D6 n'a pas, sans en perdre le contrôle : mêmes totaux, Danyi 1 et Danyi 2 séparées (D6 les fusionne), noms joints à geodata sans correction. **D6 garde un rôle de contrôle**, pour la population totale (11.A14).
- **Un seul millésime (2022)** : aucune population annuelle pour les séries nationales (dénominateurs de O1-03 et O2-07). **Correction du 26/09/2026** : les projections de l'INSEED (IN1) donnent la population annuelle 2011-2031 par âge et par sexe, au niveau national. En 2022, IN1 est à -0,3 % du RGPH sur le total, mais à **+6,6 % sur les 15 ans et plus** (encadré de la section 9). IN1 remplace la population implicite de la Banque mondiale pour les taux que nous calculons (11.A16, P3).
- Pas de superficie ni de contour des unités : ils sont fournis par 6b (ci-dessous).
- Communes de Danyi non séparables dans D6 : Danyi 1 et Danyi 2 y sont fusionnées. **RG3 les sépare** (25 820 et 14 420 habitants) : c'est le cas d'usage de la décision R4 (11.E). Danyi reste néanmoins fusionnée dans D6 lui-même : c'est une limite propre à D6, sans effet sur RG3, qui devient la source retenue.

### Complément : 6b — limites administratives (geodata.gouv.tg)

```
Fichiers      : D6_geodata-limites-regions.geojson, -prefectures, -communes, -cantons
Source        : geodata.gouv.tg, couches ouvertes « Limites administratives » ; collecte PRISE 2021/2022
Période       : Stock ; téléchargé le 25/09/2026, après validation (11.C3)
Unité d'obs.  : unité administrative (un contour par unité)
Granularité   : 5 régions (Grand Lomé dans Maritime), 39 préfectures, 117 communes, 396 cantons
Format        : GeoJSON, EPSG:4326, MultiPolygon
Objets        : 5 / 39 / 117 / 396
```

| Variable     | Contenu                                                                                          | Preuve |
| ------------ | ------------------------------------------------------------------------------------------------ | ------ |
| `id`       | Code hiérarchique, le même que dans les 90 fichiers d'indicateurs geodata : `regions.A`, `prefectures.A01`, `communes.A01001`, `cantons.A01001001` | A |
| `geometry` | Contour de l'unité ; toutes les géométries sont valides                                         | A      |
| Superficie   | Calculée par nous (calcul géodésique) : 56 654,6 km² au total, identique aux 4 niveaux         | B      |

**Attributs masqués.** Les métadonnées décrivent les noms, les codes parents et, pour les cantons, une **population**. Ces attributs ne figurent dans aucun export (JSON, CSV, Shapefile) et valent « N/A » dans l'aperçu public. Les noms se retrouvent par le code dans les fichiers d'indicateurs (3i, 4j, 5c). La population des cantons pourrait être la base des indicateurs geodata (≈ 8,14 M), mais elle n'est pas accessible.

**Superficies**

| Niveau     | Plus petite unité                         | Médiane    | Plus grande unité             |
| ---------- | ----------------------------------------- | ---------- | ----------------------------- |
| Région    | Maritime 6 372 km²                        | 11 390 km² | Plateaux 16 965 km²           |
| Préfecture | Agoè-Nyivé 193 km²                       | 1 215 km²  | Bassar 3 284 km²              |
| Commune    | Agoè-Nyivé 3 : 5,8 km²                   | 405 km²    | Blitta 3 : 1 597 km²          |
| Canton     | Agou-Nyogbo-Dzidjole 2,9 km²              | 94 km²     | Bassar 1 197 km²              |

Les trois autres régions : Centrale 13 391 km², Kara 11 390 km², Savanes 8 536 km².

**Utilité**

- → Objectif 3 : les cartes choroplèthes par région, préfecture et commune demandées par le 01 ; la densité de points au km².
- → Objectif 4 : le volet « pour 1 000 km² » de O4-02.
- → Référentiel territorial (prérequis du 02) : contours et codes des unités, et contrôle du rattachement des points par leurs coordonnées (étape 05 de la procédure).

**Qualité**

- Chevauchements et vides inférieurs à 0,2 km² par niveau.
- **Emboîtement** : les préfectures sont exactement dans leurs régions, les cantons exactement dans leurs communes. Mais 3 communes débordent de leur préfecture sur 150 km² : Haho 1 sur Kpélé (99,8 km²), Oti 2 sur Tandjoaré (48,5 km²), Lacs 3 sur Golfe (1,2 km²). Les régions ne changent pas : chaque débordement reste dans la même région.
- **8 codes de canton ne correspondent pas à la commune qui contient leur polygone**, dont les 3 déjà repérés en section 7 :
  - Kati, Djemegni et Takpamba : la commune de leur code n'existe pas ; D4 et D5 les déclarent dans la commune de leur polygone (Agou 1, Haho 2, Oti-Sud 2) ;
  - Kpaha et Anima : code de Doufelgou 1, polygone dans Doufelgou 2, commune que D5 déclare pour Kpaha ;
  - Agome-Glozou, Akpakpakpé et Yokélé : D5 les déclare dans la commune de leur code (Bas-Mono 2, Haho 4, Kloto 1), mais leur polygone est dans la commune voisine (Bas-Mono 1, Haho 3, Kloto 2). Ici, le contour ou le rattachement est faux, sans qu'on puisse dire lequel.
- **Rattachement des points** : 100 % pour D4 et 4c, de 99,63 à 99,75 % pour D5 (sections 4, 5 et 7).
- **Décision 11.A21 (26/09/2026)** : les points sont rattachés par leurs noms déclarés ; les préfectures sont reconstituées par fusion des communes, ce qui supprime les 3 débordements (les régions ne changent pas) ; les codes de Kati, Djemegni, Takpamba, Kpaha et Anima sont corrigés d'après la position de leur polygone ; ceux d'Agome-Glozou, Akpakpakpé et Yokélé sont gardés tels que déclarés et signalés.

**Limites**

- Pas de noms dans les fichiers : il faut les reprendre des indicateurs geodata par le code.
- Contours de la campagne PRISE 2021/2022 : aucune date de mise à jour, et aucune indication de source officielle du découpage.
- Le Grand Lomé n'est pas une unité : il se reconstitue par les préfectures Golfe et Agoè-Nyivé ; il forme la 6e unité régionale (11.A12, validé).

### Données complémentaires téléchargées : dénominateurs (objectifs 1, 3, 4 et 5)

*Fichiers de `data/raw/_extradatas/`, retenus par le journal de recherche (décisions entre parenthèses). Profils complets : section 12.*

| Réf. | Fichier (dossier) | Ce qu'il apporte face aux limites de D6 | Indicateurs du 02 | Preuve |
| ---- | ----------------- | --------------------------------------- | ----------------- | ------ |
| RG2, RG3 | `obj4/RG_rgph5_livrets/` (livrets 02 et 03 et leurs transcriptions) | Même recensement que D6, avec l'âge, le milieu et le sexe par préfecture (39) et par commune (117) ; Danyi 1 et 2 séparées ; noms joints sans correction. Source de population des objectifs 3 et 4 ; D6 devient un contrôle (R4) ; âge non déclaré réparti au prorata (S5) | O3-02, O4-01, O4-02, O4-04, O4-05 | A |
| IN1 | `obj1/IN1_*` | Population annuelle 2011-2031, nationale, par âge et sexe : dénominateur des séries nationales, jamais mêlé au RGPH (P3, R2) | O1-03, O2-07, O3-04 | C |
| RG1 | `obj4/RG_rgph5_livrets/` (livret 01) | Population par sexe jusqu'au canton : téléchargé, non transcrit (S10) | Étape 11, si besoin | A |
| CO1 | `obj4/CO1_*` (OCHA) | Population 2021 par préfecture (ancien découpage, base 2010) : contrôle | Contrôle | C |
| AS2 | `obj4/AS2_inseed_annuaires-regionaux-2024/` | Population estimée par préfecture pour Maritime, Centrale, Kara et Savanes (l'annuaire des Plateaux n'est pas publié) : contrôle | Contrôle | C |

**Ce que ces compléments règlent** : les 15 ans et plus et le milieu par territoire (11.B1, B3), la population annuelle nationale (B5), la séparation de Danyi.

**Ce qui reste non résolu** :
- Un seul millésime territorial (2022) : aucune population annuelle par préfecture ou par commune, sauf les estimations partielles de AS2.
- Les ménages restent absents partout (O2-07).
- L'âge non déclaré (24 180 personnes) est traité par convention, avec un test de sensibilité (S5).
- Trois bases de population coexistent (Banque mondiale, IN1, RGPH) : elles ne se mélangent jamais dans un même indicateur (encadré de la section 9).

---

## 7. Jointures entre fichiers : le référentiel territorial

Aucun fichier de points ne porte de code administratif : D4, 4c et D5 donnent des noms (suffixe `_bdd`), D6 des noms en majuscules sans accents. Les indicateurs de geodata.gouv.tg (3i, 4j, 5c) apportent le chaînon manquant : **un code hiérarchique pour chaque unité**, identique dans les 90 fichiers et dans les contours de 6b.

| Niveau     | Unités geodata                          | Exemple de code                 |
| ---------- | --------------------------------------- | ------------------------------- |
| Région    | 5 (le Grand Lomé est dans Maritime)    | `A` (Maritime)                |
| Préfecture | 39                                     | `A01` (Agoè-Nyivé)            |
| Commune    | 117                                     | `A01001` (Agoè-Nyivé 1)       |
| Canton     | 396                                     | `A01001001` (Agoè-Nyivé)      |

Jointure par les noms, après normalisation (majuscules, sans accents, tirets et espaces unifiés) :

| Niveau     | D4 → geodata | 4c → geodata | D5 → geodata | D6 → geodata                                  | Obstacle                                                                                             |
| ---------- | ------------- | ------------- | ------------- | ---------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Région    | 5/5           | 5/5           | 5/5           | 5/6                                            | « DAGL » (Grand Lomé) : unité à part dans D6, dans Maritime ailleurs                              |
| Préfecture | 38/38         | 22/22         | 39/39         | 39/39                                          | « TOTOAL AVE » à renommer                                                                         |
| Commune    | 95/95         | 36/36         | 117/117       | 115/116                                        | Après correction d'Amou 3, d'Est-Mono 3 et de Binah 2 ; reste « DANYI 1+DANYI 2 », fusionnées |
| Canton     | 130/130       | 37/37         | 372/372       | Hors Grand Lomé : 318/375 ; Grand Lomé : 4/222 | Orthographes divergentes ; dans le Grand Lomé, D6 donne 222 quartiers et geodata 13 cantons       |

Pour D6 au niveau du canton, on compte les couples commune + canton reconnus.

- **D4, 4c et D5 se rattachent sans perte** aux codes geodata : mêmes noms à tous les niveaux, ce qui est cohérent avec une base commune (la campagne PRISE).
- **D6 se rattache aux préfectures et aux communes** avec les corrections de libellés de la section 6. Danyi 1 et Danyi 2 doivent être regroupées côté geodata pour joindre D6 tel quel. **Depuis la décision R4, ce regroupement n'est plus nécessaire pour la population** : RG2 et RG3 (section 12), qui séparent déjà Danyi 1 et Danyi 2, sont la source retenue pour les objectifs 3 et 4, et se joignent à geodata sans aucune correction. D6 ne sert plus qu'au contrôle du total.
- **Cantons** : 318 unités de D6 sur 375 hors Grand Lomé retrouvent leur couple commune + canton ; les 57 autres demandent une table de correspondance manuelle. Dans le Grand Lomé, quartiers (D6) et cantons (geodata) ne se correspondent pas.
- **Particularités des codes geodata** : 8 cantons ont un code qui ne correspond pas à la commune où se trouve leur polygone. Pour 3 d'entre eux, la commune du code n'existe même pas (Kati `B01032079`, Djemegni `B02048134`, Takpamba `E06108355`) ; le détail est en section 6 (6b). Deux cantons s'appellent Loko, il faut donc joindre sur le couple commune + canton, jamais sur le nom seul. Geodata compte 383 cantons hors Grand Lomé, contre 375 unités dans D6.

**Contrôle par les coordonnées (contours de 6b).** Chaque point est comparé au polygone de l'unité qu'il déclare :

| Niveau     | D4 (738 points) | 4c (184 sites) | D5 (19 788 points) |
| ---------- | --------------- | -------------- | ------------------ |
| Région    | 100 %           | 100 %          | 99,75 %            |
| Préfecture | 100 %           | 100 %          | 99,64 %            |
| Commune    | 100 %           | 100 %          | 99,63 %            |
| Canton     | 100 %           | 100 %          | 99,75 %            |

Les écarts de D5 sont détaillés en section 5 : 49 points frontaliers hors du territoire, et 47 points placés dans des zones où les contours des communes et des préfectures, ou le rattachement de 3 cantons, ne concordent pas.

**Population par âge et milieu (RG2, RG3, 26/09/2026).** Les 39 préfectures et les 117 communes des livrets du RGPH-5 se joignent aux noms de geodata **sans aucune correction**, après la même normalisation. Danyi 1 et Danyi 2 y sont séparées. Le livret 03 ne descend pas au canton ; le livret 01 (RG1, téléchargé, non transcrit) donne la population par sexe jusqu'au canton.

**Conséquence :** le code geodata peut servir de **clé stable** au référentiel territorial que le 02 exige avant tout calcul (11.A14), et 6b en donne les contours. Les points et les indicateurs geodata s'y rattachent à tous les niveaux, la population (D6) aux niveaux préfecture et commune. Le canton reste inutilisable pour les ratios par habitant sans table manuelle, et impossible dans le Grand Lomé. Cela reste cohérent avec le plancher du 02 (préfecture, commune si disponible). **Rattacher les points par leurs noms déclarés plutôt que par leur position** évite de perdre les 49 points frontaliers et de déplacer les 47 autres (11.A21). **Construction du référentiel (11.A21, validé le 26/09/2026)** : les préfectures sont reconstituées par fusion des communes de 6b, pour que cartes, superficies et comptages portent sur le même territoire ; 5 codes de canton sont corrigés d'après la position, 3 gardés tels que déclarés et signalés (section 6, 6b).

---

## 8. Millésimes

| Fichiers        | Date de référence                                                              | Nature               |
| --------------- | -------------------------------------------------------------------------------- | -------------------- |
| D1, 1b          | 1960-2022 (CSV) ; 1960-2024 (API)                                                | Série annuelle      |
| D2              | 2013-2019                                                                        | Séries annuelles    |
| 2b              | 2010-2022 (mobile money : 2013-2022)                                             | Séries annuelles    |
| 2c, 2d          | 2007-2023 ; 2007-2024                                                            | Série annuelle      |
| 2e              | 2024 d'après les métadonnées ; aucune date dans les fichiers                    | Échantillon         |
| D3              | 2013-2019                                                                        | Séries annuelles    |
| 3b à 3e, 3f    | 1960-2023 ; 1960-2024                                                            | Séries annuelles    |
| 3g, 4g          | 1960-2023 selon l'indicateur (revenus télécoms : 1965-2010 ; Findex : 2011-2021) | Séries annuelles    |
| 4e, 4f          | 2004-2022 ; jusqu'en 2024                                                        | Séries annuelles    |
| 4h              | Findex 2011, 2014, 2017, 2021 et 2024                                            | Vagues d'enquête    |
| 4i              | 2010-2022 (chèques postaux : 2013-2019)                                          | Séries annuelles    |
| D4, 4c          | Collecte PRISE 2021/2022 (geodata) ; exports du 06/01/2025 et du 02/01/2025      | Stock                |
| D5              | Collecte PRISE 2021/2022 (geodata) ; export du 19/12/2024                        | Stock                |
| 3i, 4j, 5c      | Couches PRISE 2021/2022 ; date de calcul inconnue                                | Stock pré-calculé  |
| 6b              | Couches PRISE 2021/2022 ; téléchargées le 25/09/2026                            | Stock (contours)     |
| D6              | 2022                                                                             | Stock (recensement)  |
| *Sources complémentaires (section 12)* |                                                             |                      |
| AR1             | T1 2018 à T2 2026 (trafic depuis le T4 2017 ; mobile money au moins depuis le T4 2021) | Séries trimestrielles ; révisions d'un numéro à l'autre |
| IN1             | 2011-2031 (projections)                                                          | Séries annuelles    |
| IN2 ; IN3a, IN3b | 2010-01 à 2017-04 ; 2010-01 à 2022-12 et 2014-01 à 2024-04                     | Séries mensuelles   |
| IT1             | 2008-2025                                                                        | Série annuelle      |
| W1 (MICS6)      | 2017                                                                             | Enquête (point)      |
| W2 (EHCVM)      | 2018/19 et 2021/22 (mêmes grappes)                                                | Enquête (2 points)   |
| AS1 (EIPT)      | 2020                                                                             | Enquête (point)      |
| W3 (Findex)     | 2024 (vague 2025)                                                                | Enquête (point)      |
| W4 (Afrobaromètre) | Terrain 12/2012, 10/2014, 11/2017, 12/2020-01/2021, 03/2022, 11/2024           | Enquête (6 points)   |
| RG1 à RG3       | 2022 (même recensement que D6)                                                   | Stock (recensement)  |
| CO1             | 2021 (projection, base 2010)                                                     | Stock (contrôle)     |
| BC1, BC2        | 2014-2024                                                                        | Séries annuelles par pays |
| AR2 (rapport 2025) | Sites 2021-2025                                                               | Série annuelle      |
| AR6             | Campagnes QoS 2024 ; QoE 2025-2026 ; tarifs avril 2023                           | Mesures ponctuelles  |
| TF1             | Instantané du 26/09/2026                                                         | Stock (grille)       |
| GD1, GD2        | Couches PRISE 2021/2022 ; téléchargées le 26/09/2026                             | Stock                |
| CH1             | 2001-2026                                                                        | Événements datés     |

- **Objectifs 1-2 et 3-4 : les périodes se touchent désormais** (séries jusqu'en 2022-2026, stocks de 2021-2022), mais les séries restent nationales et les stocks territoriaux. La « Limite structurelle assumée » du 02 tient : aucun panel, aucun lien causal entre les deux blocs. Les enquêtes ajoutent des mesures régionales ponctuelles ; ce ne sont pas des séries.
- **Croisements des objectifs 3-4 :** points collectés en 2021/2022 (D4, 4c, D5), population de 2022 (D6). L'écart est d'un an au plus : le croisement est valide selon la règle des millésimes du 02, **la date PRISE étant retenue** (11.A10, validé le 26/09/2026). Seul geodata la déclare ; les exports d'opendata sont datés de fin 2024 et de début 2025.
- **O4-06 :** la couverture de 3i repose sur la couche des tours télécoms de la même campagne PRISE : même millésime que les points.
- **Objectif 1 :** l'écart utilisateurs / abonnements (O1-03) est calculable sur 2010-2024 (1b ; 2b jusqu'en 2017, AR1 ensuite) ; la part par technologie (O1-04) couvre 2013-2025 en annuel et 2018-2026 en trimestriel (D2 jusqu'en 2017, AR1 ensuite).
- **Annuel à partir de données trimestrielles (AR1)** :
  - **stocks** (abonnés, comptes, points de vente) : valeur du T4, par convention ; la moyenne des 4 trimestres est testée en sensibilité ;
  - **flux** (CA, investissement, trafic, transactions) : somme des 4 trimestres.
  Une année incomplète (2026) n'a pas de valeur annuelle.
- **Décision R6 (26/09/2026), lecture de O1-02 sur les abonnements** : les deux conventions ci-dessus (valeur du T4, moyenne des 4 trimestres) divergent certaines années (section 9). Une année n'est donc classée (accélération, ralentissement, régression) que si les **deux conventions concordent** ; sinon, elle est marquée « dépend de la convention ». À partir de 2018, le **glissement trimestriel** (T / T-4) s'ajoute à la lecture annuelle, puisque le 02 autorise un calcul trimestriel de O1-02.
- **Objectif 2 :** jusqu'au 25/09/2026, seuls les abonnés, les télédensités, le CA du secteur et le mobile money étaient prolongés au-delà de 2019. AR1 couvre désormais tout le marché jusqu'au T2 2026.
- **Enquêtes :** l'EHCVM 2021/22 (terrain 2021-2022) est contemporaine de la collecte PRISE et du RGPH-5, ce qui permet de croiser usage et offre par région selon la règle des millésimes du 02.

---

## 9. Une même grandeur, plusieurs sources

Les compléments recoupent D1 à D3, et les mêmes grandeurs y ont souvent des valeurs différentes.

| Grandeur                                        | Valeurs selon la source                                                                                                                                   | Remarque                                                                                   |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Télédensité mobile (pour 100 habitants), 2019 | D3 81,91 ; 3c 75,69 ; 3f 73,72 ; 2b 72,72                                                                                                                | D3 et 3f ont les mêmes abonnés (6 239 183) : tout l'écart vient du dénominateur        |
| Lignes fixes pour 100 habitants, 2013           | D3 0,97 ; 3e 0,858 ; 2b 5,48                                                                                                                              | D3 et 2b identiques en 2018-2019                                                           |
| Abonnés mobiles, 2013                          | D3 3 713 908 ; 3b et 3f 4 262 993                                                                                                                         | Identiques en 2017-2019                                                                    |
| Abonnés fixes, 2013                            | D3 64 493 ; 3d 62 537                                                                                                                                     | Identiques en 2014 et en 2017-2019                                                         |
| Large bande fixe pour 100 habitants             | 2013 : 2b 1,03, 2c 0,09 ; 2022 : 2b 1,16, 2c 1,04                                                                                                         | Creux suspect de 2c en 2013-2014                                                           |
| CA du secteur                                   | 2013-2019 : D3 et 2b à -1,3 % / +3,1 % l'un de l'autre ; 2010 : 3g 149,0 Md FCFA, 2b 155,0 Md                                                           | Périmètres non documentés                                                               |
| Individus utilisant Internet (%)                | 2021 : D1 32,51, 1b 30,34 ; 2022 : D1 37,62, 1b 35,61                                                                                                     | Révision de la source                                                                    |
| Agences et DAB pour 100 000 adultes             | 4f révise 4e de -2 à -9 % ; DAB 2017 : FAS 5,45, GFDD 3,98 (4g)                                                                                           | Deux bases de la Banque mondiale                                                           |
| Population totale                               | Implicite INSEED (D2, D3) : 6,64 M en 2013, 7,62 M en 2019. Implicite Banque mondiale (3f) : 7,29 M en 2013, 8,46 M en 2019, 9,09 M en 2022. RGPH : 8,10 M en 2022. IN1 : 8,07 M en 2022. Base geodata : ≈ 8,14 M | En 2022, la Banque mondiale est 12 % au-dessus du recensement ; IN1 est à -0,3 %          |
| *Ajouts du 26/09/2026 (sources de la section 12)* |                                                                                                                                                       |                                                                                            |
| Population de 15 ans et plus, 2022              | IN1 : 5 032 000 (62,4 %). RGPH-5 (RG2) : 4 707 386 hors âge non déclaré, soit environ 4 721 000 avec les 24 180 « ND » répartis (58,3 %). OCHA (CO1, 2021, base 2010) : 61,1 % | **IN1 dépasse le recensement de 6,6 %** sur les adultes, alors qu'il est juste sur le total |
| Abonnements data mobile                         | 2019 : 2b 3 379 910 ; ARCEP (T4) 4 671 179. 2021 : ARCEP 5 906 003 en première publication, 4 651 596 après révision, valeur reprise par 2b | 2019 : origine de 2b inconnue. 2021 : révision méthodologique de l'ARCEP. Égaux en 2018, 2020 et 2022 |
| Abonnés 3G de Togocel, 2019                     | D2 1 242 250 ; ARCEP (T4) 2 373 589                                                                                                                     | La baisse de 2019 de D2 n'existe pas chez l'ARCEP                                         |
| Points de service mobile money                  | D5 : 19 788 points (environ 32 400 par opérateur), 2021/2022. ARCEP : 33 924 points de vente (T4 2021), 64 540 (T2 2026). BCEAO : 81 137 points de monnaie électronique en 2024, dont 65 043 actifs | Cohérents à la date PRISE ; le réseau a presque doublé depuis                              |
| Comptes mobile money                            | 2b (« abonnés actifs ») et ARCEP (abonnés) : 3 005 048 en 2022. ARCEP : 5 104 779 au T4 2025. BCEAO : 12 553 441 comptes ouverts et 6 069 075 actifs à 90 jours en 2024 | Trois définitions : abonnés (ARCEP), comptes ouverts et comptes actifs (BCEAO). Chacune garde son libellé (décision Q7) |
| Usage d'Internet (%)                            | 1b : 30,34 (2021), 39,48 (2024), estimation UIT, population totale. EHCVM : 35,4 % des 15 ans et plus « ont accès » (2021/22). Findex : 43,7 % des 15 ans et plus l'ont utilisé au cours des 3 derniers mois (2024). EIPT : 43,7 % des **ménages** connectés (2020) | Définitions, âges et unités différents : jamais reliés en une série                       |
| Points de service pour 10 000 adultes, 2024     | BCEAO : 116 (UEMOA : 193), monnaie électronique comprise ; FAS (C5) : agences bancaires 4,38 et DAB 6,93 **pour 100 000 adultes** au Togo, au-dessus de la moyenne (3,52 et 5,15) et de la médiane des 8 pays de l'UEMOA (2024) | **Décision R1** : O4-02 utilise le FAS (points formels), pas le TGPSFd de la BCEAO (mobile money compris à 99 %) ; le TGPSFd sert seulement de repère à une variante « tous points de service ». **Précisé par S2 à S4** : repère = moyenne des 8 pays ; territoires comparés pour les agences seulement, DAB au niveau national (appareils) ; FAS divisé par 10 à l'affichage |

> **Dénominateurs : trois bases coexistent**
>
> | Base | Population 2022 | Écart au RGPH | 15 ans et plus (2022) | Sert à |
> | ---- | --------------- | ------------- | --------------------- | ------ |
> | **Banque mondiale** : population implicite des séries UIT (3f), base vraisemblable de D1 | 9,09 M | **+12 %** | — | D1 (O1-01), repris tel que publié ; taux « pour 100 » de 3b à 3f |
> | **IN1** : projections de l'INSEED, base RGPH 2010 ; base des taux de l'ARCEP | 8 068 000 | -0,3 % | 5 032 000 (**+6,6 %**) | Taux nationaux annuels que nous calculons : abonnements pour 100 habitants, O2-07, O3-04 |
> | **RGPH-5** : D6, RG2, RG3 | 8 095 498 | — | environ 4 721 000 | Tous les ratios territoriaux (objectifs 3 et 4), dont les 15 ans et plus par préfecture et commune |
>
> Règles (11.A16 et 11.D, P3) :
> - **Un taux ne se compare qu'à un taux de même base.** D1 (39,5 % d'utilisateurs en 2024, base Banque mondiale) et un taux d'abonnements pour 100 habitants calculé avec IN1 ne sont pas comparables. Rapprochés, ils fausseraient l'écart de O1-03 d'environ 12 %.
> - **O1-03 compare des nombres, pas des taux.** Utilisateurs = taux D1 x population Banque mondiale (niveau C), face aux abonnements publiés (niveau A).
> - **Adultes — décision R2 (26/09/2026)** : IN1 et le RGPH divergent de 6,6 % sur les 15 ans et plus en 2022. Règle retenue : **RGPH-5 (RG2, RG3)** pour tout ratio par adulte en 2022 et pour tout ratio territorial ; **IN1** seulement pour les séries nationales annuelles, là où le RGPH n'existe pas, et jamais dans le même tableau que le RGPH ; **Findex et BCEAO** repris tels que publiés, avec leur propre base d'adultes (non documentée par ces sources).
> - **Âge non déclaré — décision S5 (26/09/2026)** : le RGPH-5 compte 24 180 personnes d'âge non déclaré (4 707 386 adultes sans elles, environ 4 721 000 avec elles). **Convention** : elles sont réparties au prorata de la structure par âge de chaque territoire ; la variante « hors non déclarés » est testée en sensibilité (écart national : 0,3 %, peut-être plus dans les petites communes).
> - Les taux d'enquête (MICS6, EHCVM, Findex, Afrobaromètre) sont calculés dans l'échantillon pondéré, sans dénominateur extérieur. Les poids de l'EHCVM 2021/22 totalisent 8,095 M, calés sur le RGPH-5 ; ceux de 2018/19, 7,663 M.
> - Deux autres bases existent sans servir de dénominateur : l'implicite INSEED de D2 et D3, et la base des indicateurs geodata (≈ 8,14 M).
> - Chaque indicateur affiche sa base de population.

- **Aucune série ne se prolonge en raccordant une autre source** (les écarts dépassent souvent la variation d'une année), **sauf les abonnements Internet de D2 / 2b et de l'ARCEP** : au point de raccord (2017-2018), les deux sources sont égales, à 0,03 % près pour 2017 (11.A15, P4).
- **Année et trimestre (convention du T4).** Pour les stocks trimestriels de l'ARCEP, l'année est représentée par son T4. Premier contrôle, sur les abonnements data mobile 2018-2025 :
  - **pas de pic saisonnier systématique au T4** : face à la moyenne du T3 et du T1 suivant, il va de -2,9 % à +6,9 %, et il est inférieur 4 années sur 8 ;
  - **mais le T4 dépasse la moyenne annuelle** (de 0 à +12,6 %), parce que le stock croît en cours d'année ;
  - **la croissance annuelle change donc de lecture selon la convention** : 2021, -4,9 % avec le T4 contre -0,6 % avec la moyenne (régression d'un côté, |g| < 2 % de l'autre) ; 2023, +8,4 % contre +5,1 % ; 2024, +6,5 % contre +11,8 % ; 2025, +12,8 % contre +9,0 %.

  La moyenne des 4 trimestres est donc testée en sensibilité, et une année n'est classée que si les deux lectures concordent (proposition R6). Détail : `_RECHERCHE_donnees_manquantes.md`, section 12.1.
- **Un taux « pour 100 » ne se compare qu'à dénominateur égal** : voir l'encadré ci-dessus.
- **Les comptages de points ne divergent pas** : 4j retrouve exactement les effectifs de D4 et de 4c ; GD1 retrouve les 95 agences de la Poste de 4j.
- Choix 11.A1, A15 et A16 : tranchés le 26/09/2026 (section 11) ; A4 aussi : pour le CA, 2b et AR1 ne se raccordent pas (partie G).

---

## 10. Couverture des indicateurs du 02

**Légende :**

- ✅ calculable avec les données du projet ;
- ⚠️ calculable en partie ou sous condition ;
- ❌ non calculable avec les données du projet.

| ID    | Indicateur (résumé)                         | Fichiers                  | 25/09 | 26/09 | Ce qui manque ou conditionne                                                                                                                      |
| ----- | --------------------------------------------- | ------------------------- | ----- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| O1-01 | Pénétration Internet (utilisateurs)         | 1b ; points mesurés W1 à W4, AS1 ; C5b | ✅ | ✅     | Version API (11.A1, tranché). **Série estimée par l'UIT** sauf 2017 : chaque année porte ce libellé (D-15). Dénominateur Banque mondiale, 12 % au-dessus du RGPH (encadré de la section 9). **Repère Afrique subsaharienne, décision S1** (C5b) : agrégat de la Banque mondiale (moyenne pondérée par la population, 2005-2025), estimé par l'UIT comme 1b, donc comparaison d'estimation à estimation (niveau C). Le Togo est sous la moyenne jusqu'en 2019 (-3,7 points), au-dessus à partir de 2020 (29,0 % contre 26,7 %) ; 2024 : 39,5 % contre 33,6 %. 8 pays de l'UEMOA en complément (Togo 3e sur 8 en 2024) |
| O1-02 | Croissance et ruptures                        | 1b, D2, 2b, AR1, CH1      | ⚠️ | ⚠️   | **Stagnation : écart déclaré au 02** : avec le seuil du 02 (\|g\| < 2 %), aucune année n'en est une (section 1) ; l'objectif 1 est traité par une classe « ralentissement » (croissance < moyenne − 1 écart-type), à calculer à l'étape d'analyse (11.D, P2) ; **période de référence de la moyenne et de l'écart-type à fixer avant le calcul**. Accélérations de D1 : lues seulement si les points mesurés les confirment (D-15). **Abonnements (décision R6)** : classés seulement si la valeur du T4 et la moyenne des 4 trimestres concordent, sinon « dépend de la convention » ; glissement trimestriel T / T-4 à partir de 2018. Chronologie datée : CH1 (40 événements) |
| O1-03 | Écart abonnements / utilisateurs             | 1b, 2b, AR1, 3f, IN1      | ⚠️ | ⚠️   | 2010-2024. **Comparaison en nombres**, pas en taux (P3) : utilisateurs reconstitués = taux D1 x population Banque mondiale (niveau C). Variante 15 ans et plus : IN1, national |
| O1-04 | Part des abonnements par technologie          | D2, AR1                   | ⚠️ | ✅     | D2 jusqu'en 2017, AR1 ensuite (P4), jusqu'au T2 2026. **Rupture du T1 2020, décision S6** : la 3G de Togocel passe de 2 373 589 à 1 057 232 (-58 %) pendant que la 4G progresse, reclassement probable et non documenté. Elle est traitée comme une rupture de série : **aucune évolution par technologie n'est calculée entre le T4 2019 et le T1 2020**, et la note de méthode est à chercher pendant l'extraction de AR1 (P5). Le total data mobile recule aussi au même trimestre (-6,6 %, de 4 671 179 à 4 362 555, seul recul trimestriel de 2018-2020) : signalé, pas interprété. Autres ruptures : 3G et 4G de Moov réunies jusqu'au T3 2019. Accès fixes sans technologie connue : « Fixe, technologie non précisée » (11.A3, validé) |
| O1-05 | Usage d'Internet par territoire (optionnel)  | W1, W2, W3                | ❌ | ✅     | **Par région**, niveau représentatif des enquêtes : MICS6 2017 (7 domaines, 15-49 ans, « a utilisé au cours des 3 derniers mois », la définition de O1-01) ; EHCVM 2018/19 et 2021/22 (région x milieu, 15 ans et plus, « a accès ») ; Findex 2024 (urbain / rural seulement). Règle du coefficient de variation à appliquer. Aucune donnée par préfecture ou commune |
| O1-06 | Freins : alphabétisation, compétences TIC, smartphone | W1, W2, W3, W4 | ❌ | ✅    | Alphabétisation des 15 ans et plus par région (EHCVM 2021/22 ; 2018/19 à reconstruire) ; compétences TIC ODD 4.4.1 par région (MICS6 2017, 15-49 ans) ; smartphone au niveau national (Findex 2024 ; Afrobaromètre, par région, en approximation). Portable par région (EHCVM) |
| O2-01 | Parts de marché et HHI                       | D3, D2, 2b, AR1           | ✅ | ✅     | Parts en abonnés à la téléphonie par opérateur : D3, 2013-2019 seulement (l'ARCEP ne les publie qu'en graphique ; 04, V5) ; parts en abonnés data et en CA par opérateur : AR1, 2018-2026 ; convention du T4 ; noms d'opérateurs (11.A2, validé) |
| O2-02 | Part de CA contre part d'abonnés             | AR1                       | ❌ | ✅     | CA par opérateur, trimestriel, 2018-2026 : annuel = somme des 4 trimestres. Rupture de périmètre du CA de Togo Telecom au T2 2025 ; mobile money de YAS Togo non déclaré au T2 2026 |
| O2-03 | CA du secteur et croissance                   | D3, 2b, 3g, 4g, AR1       | ⚠️ | ⚠️   | CA jusqu'en 2025 (AR1) ; inflation (4g, IN3) ; **A4 validé** : 2b pour la série nationale (2010-2022), AR1 pour 2018-2026, **sans raccord** (même logique que P4 : 2b dépasse l'ARCEP de 2,8 % en 2021 et de 3,7 % en 2022) ; croissance calculée dans une même source ; net ou brut non documenté |
| O2-04 | Investissement / CA (optionnel)              | D3, 3g, AR1               | ⚠️ | ✅     | Investissement et CA par opérateur, même source, 2018-2025 (AR1) ; très concentré au T4. « Investissement mis en service » chez YAS : définition à noter |
| O2-05 | ARPU et coût de 1 Go                         | IT1, AR1, AR5, AR6        | ⚠️ | ✅     | **Deux composantes, libellés distincts (décision du 26/09/2026)**. **O2-05a**, « revenu moyen par abonnement mobile, tous services » : CA / abonnés moyens / 12, depuis AR1 (niveau B), **au niveau national** : l'ARCEP ne publie les abonnés à la téléphonie par opérateur qu'en graphique (04, V5) ; années complètes 2018-2025, 2026 sur le 1er semestre ; abonnés moyens = moyenne des 4 stocks trimestriels, comme le dit le 02 (**convention**, valeur du T4 en sensibilité) ; pas de seuil dans le 02 ; rupture au T2 2026 (mobile money de YAS Togo non déclaré). ARPU de D3 écarté (11.A5). **O2-05b**, coût de 1 Go en % du RNB mensuel par habitant, **2023-2025** (IT1, niveau C ; 5,30 % en 2025) : seule composante soumise au seuil de 2 % ; les paniers antérieurs restent des séries distinctes (04, V6) |
| O2-06 | Couverture 3G/4G par territoire               | 3i, W2 (communautaire)    | ⚠️ | ⚠️   | Toujours un proxy : 3i (niveau C, 11.A17), confronté à la réception **déclarée** dans les 540 localités du module communautaire de l'EHCVM (Q6). OpenCellID écarté (S9). **Couverture théorique ou déclarée, jamais mesurée** : faute de O2-09 par territoire, le tableau de bord l'affiche en toutes lettres, comme le prévoit le 02. Mô, Kpendjal et Tchamba : « Non déterminable », jamais 0 % (11.A13, validé) |
| O2-07 | Fibre                                         | D2, AR1, 3i               | ⚠️ | ⚠️   | FTTH par opérateur jusqu'en 2026 (AR1) ; km de fibre en stock (3i), sans date ni distinction transport / accès |
| O2-08 | Sites radio                                   | AR2 (rapport 2025)        | ❌ | ✅     | National, par opérateur et par technologie, 2021-2025 (5 années). Rien par territoire (tours privées, 11.C6) |
| O2-09 | Qualité de service mesurée (optionnel)       | AR6                       | ❌ | ⚠️   | **Non couvert par territoire (décision S9)**. AR6 ne donne que du national : débits et latence médians par opérateur (analyses QoE nPerf, 2023-2026) et taux de conformité de la campagne 2024 (94 localités, Savanes exclues), présentés pour le Grand Lomé et le reste du pays, sans valeur par localité. Ookla, seule mesure couvrant tous les territoires, est écarté. Tous les territoires sont donc « Non déterminable » (règle du 02) et la « couverture de façade » n'est pas calculable |
| O3-01 | Points formels par type et par territoire     | D4, 4c, GD1               | ✅ | ✅     | Règles 11.A6 et A7 (validées), A19 (appliquée par S3) ; Poste comptée à part en test de sensibilité (Q5) |
| O3-02 | Concentration urbaine                         | D4, 4c, D5, D6, RG3       | ⚠️ | ✅     | Milieu urbain / rural par commune (RG3) : strate « autres villes / rural » constructible. Grand Lomé présenté comme 6e unité régionale (Golfe + Agoè-Nyivé, 11.A12, validé). **Strates par commune (décision du 26/09/2026)** : Grand Lomé (13 communes, 27,0 % de la population) ; « autres villes » = 50 % d'urbains ou plus (13 communes, 16,0 %) ; rural = les autres (91 communes, 56,9 %). **Sensibilité à 75 %** : 2 communes seulement (Ogou 1, Kozah 1 : 3,8 %), Cinkassé 1 juste en dessous (74,8 %) ; la strate intermédiaire y devient très mince. **Règle du 02 (décision du 26/09/2026)** : elle exige un Grand Lomé à moins de 25 % de la population, et il en pèse 27,0 %, donc elle ne peut pas conclure « confirmée ». Elle est appliquée telle quelle, ses deux critères affichés séparément (part des points, part de la population), et la lecture repose sur l'indice de concentration et le gradient, que le 02 définit aussi (11.G) |
| O3-03 | Agents mobile money par territoire            | D5                        | ⚠️ | ⚠️   | Points et non agents ; actifs seulement au niveau national (BCEAO : 80,2 % en 2024) ; stock 2021/2022 (11.A8, validé : on compte des points) |
| O3-04 | Comptes et transactions mobile money          | 2b, AR1, BC1, BC2, W3, 4h | ⚠️ | ✅     | National : comptes ouverts et actifs, nombre et valeur des transactions (BCEAO, 2024 ; ARCEP par opérateur) ; détention des 15 ans et plus (Findex). Définitions à garder distinctes (Q7) ; rupture 2019-2020 des abonnés actifs de 2b signalée, sans correction (11.A20) |
| O3-05 | Usage du mobile money par territoire (optionnel) | W4, W3                | ❌ | ⚠️   | Par région avec l'Afrobaromètre (vagues 9 et 10, 1 200 personnes : coefficient de variation à contrôler) ; urbain / rural avec le Findex. **Correction du 26/09/2026** : l'EHCVM pose la question dans son module 6 (15 ans et plus, 2018/19 « possède un compte dans un mobile banking », 2021/22 « fait du mobile banking ») : par région, CV de 3 à 13 % ; **source principale de O3-05 : EHCVM 2021/22** (validé le 26/09/2026 ; 04, V7), Afrobaromètre en complément, jamais mêlé |
| O3-06 | Coût du mobile money                         | TF1                       | ❌ | ⚠️   | **Décision R3** : calculé sur la grille officielle de Flooz (instantané du 26/09/2026) ; **partiel pour Mixx**, sans grille officielle de retrait publiée (momocalc en note seulement, jamais en substitut). Pas d'historique |
| O4-01 | Habitants par point formel                    | D4, 4c, D6 ou RG2 / RG3   | ✅ | ✅     | Règles 11.A6, A7, A10 et A18, validées le 26/09/2026 ; A19 appliquée par S3 ; date PRISE 2021/2022 ; 4j en contrôle |
| O4-02 | Points pour 10 000 adultes et pour 1 000 km² | D4, 4c, RG2, RG3, 6b, C5  | ⚠️ | ✅     | 15 ans et plus par préfecture et par commune, **décision R4** (RG2, RG3). 15 ans et plus avec l'âge non déclaré réparti au prorata (S5). **Repère UEMOA, décision R1** : FAS (C5, 8 pays), pas le TGPSFd de la BCEAO, qui compte le mobile money à 99 %. **Précisé par S2 à S4** : **moyenne** des 8 pays, comme le 02 (2024 : 3,52 agences, 5,15 DAB pour 100 000 adultes), médiane en complément ; **périmètre** : territoires comparés au repère UEMOA pour les agences bancaires seulement ; DAB : comparaison UEMOA au niveau national, appareils contre appareils (4f contre C5), territoires (sites de 4c) comparés à la médiane nationale (A19) ; IMF, assurances, Poste : médiane nationale seule, « pas de repère UEMOA » ; **échelle** : FAS divisé par 10 à l'affichage (pour 10 000 adultes), échelle d'origine en note |
| O4-03 | Agents par guichet                            | D4, D5                    | ✅ | ✅     | Règles 11.A6 à A8, validées le 26/09/2026 |
| O4-04 | Habitants par agent                           | D5, D6 ou RG2 / RG3       | ⚠️ | ✅     | Variante adultes désormais calculable (RG2, RG3 ; âge non déclaré réparti au prorata, S5) ; 5c en contrôle (11.A18). Le 02 demande de préciser l'unité : **points de service, pas agents** (11.A8, validé), d'où le libellé « habitants par point de service mobile money » |
| O4-05 | Statut d'accès financier                     | D4, 4c, D5, RG3           | ⚠️ | ✅     | Règle 5 avec les sites de DAB de 4c (11.A9, validé) ; strate urbaine par commune (RG3) |
| O4-06 | Statut x couverture 3G/4G                     | D4, 4c, D5, D6, 3i        | ⚠️ | ⚠️   | Dépend du proxy de couverture (11.A17) ; Mô, Kpendjal et Tchamba « Non déterminable » (11.A13) |
| O5-01 | Score de priorité                            | D4, 4c, D5, D6, 3i        | ⚠️ | ⚠️   | 3e dimension seulement avec le proxy de 3i (11.A17) ; choix tranché à l'étape du score (11.A11) |
| O5-02 | Recommandations Internet                      | —                        | ⚠️ | ⚠️   | Usage et freins par région (enquêtes) ; couverture toujours en proxy |
| O5-03 | Recommandations inclusion financière         | —                        | ⚠️ | ✅     | Leviers « tarification » (O2-05, O3-06) et « compétences » (O1-06) désormais mesurés |
| O5-04 | Cibles chiffrées                             | —                        | ⚠️ | ⚠️   | Suit la disponibilité des indicateurs sources |

**Bilan au 26/09/2026 :** 18 indicateurs ✅, 13 ⚠️, 0 ❌ sur 31 (25/09/2026 : 5, 19 et 7 ; avant les compléments du 25/09 : 3, 17 et 11).

- **Ce qui a bougé :**
  - AR1 débloque O1-04, O2-02 et O2-04 ;
  - l'UIT (IT1) débloque O2-05 ;
  - le rapport d'activité 2025 de l'ARCEP débloque O2-08 au niveau national ;
  - les enquêtes débloquent O1-05 et O1-06 par région, et O3-05 en partie ;
  - les livrets du RGPH-5 débloquent O3-02, O4-02, O4-04 et O4-05 ;
  - la BCEAO et l'ARCEP complètent O3-04 ;
  - les grilles tarifaires rendent O3-06 partiel.
- **Ce qui ne bouge pas, et pourquoi :**
  - O1-02 : la stagnation n'est pas repérable avec le seuil du 02 (écart déclaré : classe « ralentissement », à calculer), et D1 est une estimation ;
  - O1-03 : comparaison en nombres, de niveau C ;
  - O2-06, O4-06 et O5-01 : la couverture reste un proxy ;
  - O2-09 (optionnel) : aucune mesure de qualité de service par territoire (Ookla écarté, S9) ;
  - O3-03 : des points et non des agents.
- **Un ✅ n'efface pas le niveau de preuve.** Plusieurs indicateurs ✅ reposent sur des données C (D1, IT1, enquêtes à petit échantillon) ou sur une convention (T4). Le niveau de preuve suit chaque variable (section 12).
- Le 02 n'est pas modifié. Ces écarts sont consignés ici pour la suite, comme le prévoit la procédure du projet.

### Taux de résolution par rapport aux attentes du 01

Le tableau ci-dessus mesure le plan complet du 02. Celui-ci mesure seulement ce que le 01 exige, objectif par objectif.

**Méthode :** chaque « point à produire » du 01, plus les deux hypothèses du sujet à vérifier, vaut ✅ = 1, ⚠️ = 0,5 ou ❌ = 0. Les éléments que le 01 marque « lorsque disponible » ou « optionnel » sont exclus du calcul. Le taux est la moyenne des livrables obligatoires de l'objectif. La colonne « Plan du 02 » applique la même notation aux indicateurs du 02 de l'objectif.

| Objectif | Livrables obligatoires du 01 (statut au 26/09/2026) | Attentes du 01 | Plan du 02 | Données obligatoires manquantes |
| -------- | --------------------------------------------------- | -------------- | ---------- | ------------------------------- |
| 1. Usage d'Internet | Séries ✅ ; taux de pénétration ✅ ; évolution des indicateurs ✅ ; **périodes d'accélération et de stagnation ⚠️** : accélérations repérables et datées (CH1), mais sur une série estimée ; **stagnation absente avec le seuil du 02 ; ralentissements à calculer par un écart déclaré (P2)** | 88 % (inchangé) | 83 % (42 %) | Aucune donnée : c'est le seuil du 02 qui bloque ; levé par l'écart déclaré, à calculer à l'étape d'analyse (P2) |
| 2. Marché télécom | Parts de marché en abonnés et en CA ✅ ; CA et abonnés ✅ ; évolution des technologies ✅ | 100 % (67 %) | 78 % (39 %) | Aucune |
| 3. Cartographie | Cartes à points ✅ ; cartes de densité par région, préfecture et commune ✅ ; présence / absence ✅ ; concentration des banques dans les villes ✅ (milieu par commune, RG3) | 100 % (88 %) | 75 % (42 %) | Aucune |
| 4. Rapport à la population | Habitants par point ✅ ; agents par guichet ✅ ; territoires servis uniquement par le mobile money ✅ ; statut d'accès financier ✅ | 100 % (inchangé) | 92 % (67 %) | Aucune ; décisions 11.A6 à A10 et A13 validées le 26/09/2026, A19 appliquée par S3 |
| 5. Recommandations | Volet Internet ✅ (usage et freins par région) ; volet inclusion financière ✅ ; priorisation par territoire ⚠️ (couverture en proxy) ; feuille de route ✅ | 88 % (75 %) | 63 % (50 %) | Une couverture par technologie et par territoire (tours privées, 11.C6) |
| **Ensemble** | | **95 %** (83 %) | **79 %** (47 %) | |

Valeurs du 25/09/2026 entre parenthèses. **Le taux de l'objectif 1 ne bouge pas malgré la chronologie** : le livrable « périodes d'accélération et de stagnation » reste à moitié traité tant que la classe « ralentissement » n'est pas calculée (écart déclaré au 02, P2). Ce n'est pas un manque de données.

### Les trois couches que la procédure demande à l'étape 03

| Couche                                                        | Présente ?  | Où                                                                                                              | Conséquence                                                                              |
| ------------------------------------------------------------- | ------------ | ---------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Source de **demande** (enquête déclarative)                 | Oui, par région | MICS6 2017 et EHCVM 2018/19, 2021/22 (région, milieu) ; Findex 2011-2024 (national, urbain / rural) ; Afrobaromètre 2012-2024 (région, petit échantillon) ; EIPT 2020 (national) | O1-05, O1-06 par région ; O3-05 en partie. Rien sous la région |
| **Benchmark** externe (pays comparables)                      | Oui          | Usage d'Internet : Afrique subsaharienne et 8 pays de l'UEMOA (C5b, téléchargé le 26/09/2026) ; UIT (IT1, tous pays) ; Findex 2025 (tous pays) ; BCEAO (BC1, BC2 : 8 pays de l'UEMOA) ; FAS de la Banque mondiale, 8 pays de l'UEMOA (C5, téléchargé le 26/09/2026) | Repère de O1-01 : moyenne Afrique subsaharienne (C5b, décision S1). Repère UEMOA de O4-02 : le FAS (C5), pas le taux de la BCEAO, qui compte le mobile money (R1), limité aux agences et aux DAB au niveau national (S3) |
| **Lieux candidats** (marchés, écoles, mairies, dispensaires) | Oui, cherchée et conservée | GD2 (`obj5/`) : 1 078 marchés (polygones), 15 454 établissements scolaires, 2 271 formations sanitaires, 1 576 établissements administratifs | **Non requise par les 5 objectifs** (décision du 26/09/2026) : conservée sans traitement. Utilisée seulement si l'étape 11 va jusqu'à l'optimisation de localisation, que la procédure prévoit « si la couche de candidats du 03 existe » |

---

## 11. Informations à valider

Rien ci-dessous n'a été appliqué aux données. Les points nouveaux ou révisés le 25/09/2026 sont marqués comme tels. **Au 26/09/2026** : A1, A14, A15 et A16 sont tranchés, et les statuts des parties B et C sont mis à jour. Les décisions de ce jour sont en partie D ; **R1 à R6 (partie E) et S1 à S10 (partie F) sont validés**, avec les précisions de l'utilisateur, et reportés à l'endroit qu'ils concernent. A19 est appliqué à O4-02 par S3. **Les parties A et C sont tranchées le 26/09/2026** (partie G), A2 compris, ainsi que le seuil urbain de O3-02 et le contenu de O2-05. Le point relevé en fixant ce seuil (règle de O3-02 du 02, Grand Lomé à 27,0 % de la population) est tranché aussi (partie G) : **aucune décision n'est en attente**.

### A. Choix de traitement sur les données disponibles

| #   | Question                                                             | Options                                                                                                                                              | Proposition                                                                                        |
| --- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| A1 (révisé) | Quelle version des séries Banque mondiale utiliser (D1/1b, 2c/2d, 3b à 3e/3f, 4e/4f) ? | CSV du portail (arrondis, jusqu'en 2022 ou 2023) ou API (valeurs exactes, révisées, jusqu'en 2024) | API, en documentant les révisions (D1 : 2021-2022 ; 3c : depuis 2000 ; 4e : toutes les années) → **Tranché le 26/09/2026 : API** (P1). D1 : chaque année marquée « estimation UIT », sauf 2017 (INSEED) |
| A2 (révisé) | Atlantique Telecom = Moov Africa et Togo Cellulaire = Togocom ? | La première est confirmée par 2b (valeurs identiques à D2) ; la seconde ne repose que sur la description de D3 | Libeller « Moov Africa (Atlantique Telecom) » et « Togocom (Togo Cellulaire) », la seconde notée « d'après la description du jeu » → **Validé le 26/09/2026** ; la seconde correspondance est confirmée depuis par l'ARCEP (« YAS Togo (Togo Cellulaire) », AR1) : la note n'est plus nécessaire |
| A3  | Classement technologique des accès de D2                            | EvDo, CAFE, GVA, TEOLIS, Illiconet, LS : quelle technologie ?                                                                                        | « Fixe, technologie non précisée » faute d'information → **Validé le 26/09/2026** |
| A4 (révisé) | Source et périmètre du CA (O2-03, O2-04) | D3 (2013-2019) ; 2b (2010-2022, « du secteur ») ; 3g (1965-2010) ; net ou brut inconnu partout | 2b pour la série du CA ; D3 pour le ratio Investissement / CA (même fichier, même périmètre) ; 3g en historique séparé ; libeller « tel que publié, net ou brut non documenté » → **Validé le 26/09/2026, avec AR1 pour 2018-2026** : 2b reste la série nationale du CA (2010-2022) ; D3 donne le ratio Investissement / CA (2013-2019) ; AR1 donne le CA et l'investissement par opérateur, et le CA du secteur de 2018 à 2026. **Pas de raccord** entre 2b et AR1 (règle de P4 : égalité exigée au point de jonction) : 2b dépasse la somme des 4 trimestres de l'ARCEP de 2,8 % en 2021 et de 3,7 % en 2022. Les deux séries sont affichées côte à côte, et une croissance se calcule toujours dans une même source |
| A5 (révisé) | ARPU (D3)                                                    | Diviser par 10¹⁰ (≈ 3 267 FCFA par mois en 2013) ; l'écarter ; le recalculer (CA / abonnements / 12, niveau B)                                  | L'écarter : une correction non documentée ferait un niveau de preuve C. Un recalcul, s'il est fait, porte le libellé « revenu moyen par abonnement, tous services » → **Validé le 26/09/2026**, puis **précisé** : recalcul fait depuis AR1, 2018-2026 (O2-05a, section 10) |
| A6  | Quels statuts de D4 comptent comme points de service ?               | Utilisé seul (660) ; + Néant / Nsp / Autre (61) ; exclure Fermé, En construction, Abandonné, Inachevé, En réfection, Sans local, Location (17) | Utilisé seul pour le calcul ; les statuts inconnus en test de sensibilité. 4j comptant toutes les lignes, il ne contrôle que les effectifs avant filtrage → **Validé le 26/09/2026** |
| A7  | Catégorie « Mutuelle » (9 points)                                 | IMF ou assurance                                                                                                                                     | IMF (27 autres « Mutuelle… » y sont déjà classées) ; geodata les compte à part → **Validé le 26/09/2026** |
| A8  | Unité de comptage de D5                                             | Points (19 788) ; + règle pour les points à moins de 11 m (509) ; sort des points « Nsp » (1 348)                                                | Points, sans dédoublonnage, points « Nsp » conservés ; le libellé dit « points de service » ; 5c compte de la même façon → **Validé le 26/09/2026** |
| A9 (révisé) | Règle 5 de O4-05 (« 4 types présents ») | Telle quelle avec les sites de DAB de 4c (banque, IMF, assurance, DAB) ; ou 3 types sans DAB | Telle quelle, avec les sites de DAB. Aucune assurance en Centrale ni dans les Savanes ; 17 préfectures sans DAB → **Validé le 26/09/2026** |
| A10 (révisé) | Date de référence de D4, 4c et D5 | « Campagne PRISE 2021/2022 » déclarée par geodata (écart d'un an au plus avec D6) ; ou date d'export comme borne haute (jusqu'à 3 ans) | 2021/2022, avec sa source : croisements valides selon la règle des millésimes → **Validé le 26/09/2026** |
| A11 (révisé) | Score O5-01 : 3e dimension (couverture) | Proxy de 3i (niveau C) ; score à 2 dimensions ; classement par statut O4-05 seul | À trancher à l'étape du score, après A17 → **Validé le 26/09/2026 : tranché à l'étape du score** |
| A12 | Grand Lomé au niveau régional                                      | 6e unité (comme D6) ou dans Maritime (comme D4, D5 et geodata)                                                                                      | 6e unité, car c'est l'unité de test de O3-02 ; elle se reconstitue par les préfectures Golfe et Agoè-Nyivé → **Validé le 26/09/2026** |
| A13 (révisé) | Zéro ou non collecté | 22 communes et Kpendjal sans établissement (D4) ; Kpendjal sans DAB (4c) ; couverture de 3i à 0 % à Mô et Kpendjal, 0,05 % à Tchamba | Établissements et DAB : vrai zéro avec avertissement, car D5 prouve que ces territoires ont été enquêtés. Couverture de Mô, Kpendjal et Tchamba : « Non déterminable », car D5 y prouve la présence d'un réseau → **Validé le 26/09/2026** |
| A14 (révisé) | Référentiel territorial | Codes geodata comme clé (section 7) ; corrections de D6 (Avé, Binah 2, et Amou 3 et Est-Mono 3 déduits de l'ordre des lignes) ; Danyi 1 et 2 regroupées | Appliquer, et tracer chaque correction dans la table de correspondance → **26/09/2026** : le livret 03 du RGPH-5 confirme les corrections d'Amou 3, d'Est-Mono 3 et de Binah 2, et sépare Danyi 1 et Danyi 2. **Révisé par la décision R4** : Danyi n'a plus besoin d'être regroupée, puisque RG2 et RG3 (pas D6) sont désormais la source de population des objectifs 3 et 4 (section 6) |
| A15 (nouveau) | Quelle source retenir quand plusieurs donnent la même grandeur (section 9) ? | INSEED (D2, D3, 2b) ou Banque mondiale (2c/2d, 3b à 3f), indicateur par indicateur | Une seule source par série, jamais de raccord : 2b pour Internet par opérateur et le CA 2010-2022 ; 3f pour les abonnés à la téléphonie ; D2 pour les technologies 2013-2019 → **Révisé et tranché le 26/09/2026** (P4) : abonnements Internet par opérateur et par technologie = D2 / 2b jusqu'en 2017, **AR1 à partir de 2018** (raccord vérifié : écart nul en 2018, 0,03 % en 2017) ; valeurs 2019 de D2 et 2b écartées. Stocks : valeur du T4 **par convention**, moyenne des 4 trimestres testée en sensibilité (R6) ; flux : somme des 4 trimestres ; dernière publication pour chaque trimestre. CA : voir A4 |
| A16 (nouveau) | Dénominateur de population des séries nationales (O1-03, O2-07) | Implicite INSEED (2013-2019) ; implicite Banque mondiale (1960-2024) ; RGPH (2022 seulement) | Implicite Banque mondiale, base vraisemblable de D1 : l'écart de O1-03 garde ainsi un dénominateur unique. Niveau C, écart avec le RGPH affiché → **Tranché le 26/09/2026** (P3) : **IN1** pour tous les taux nationaux que nous calculons ; D1 garde son dénominateur ; **O1-03 compare des nombres**. Encadré « Dénominateurs » en section 9 ; adultes : R2 |
| A17 (nouveau) | Couverture de 3i comme proxy de O2-06 | L'accepter comme « couverture théorique toutes technologies, 20 km », niveau C ; ou abandonner O2-06 (règle du 02 : pas de valeur de substitution) | L'accepter sous ce libellé, avec Mô, Kpendjal et Tchamba en « Non déterminable » ; O4-06 et O5-01 qui en dépendent marqués « à confirmer » → **26/09/2026** (Q6) : proxy confronté à la réception déclarée dans le module communautaire de l'EHCVM (540 localités, 3 réseaux) ; OpenCellID écarté (S9) |
| A18 (nouveau) | Indicateurs pré-calculés de geodata (4j, 5c, agences Togocom de 3i) | Les afficher comme valeurs ; ou s'en servir comme contrôle seulement | Contrôle seulement : ratios recalculés à partir des points (A) et du RGPH (B) → **Validé le 26/09/2026** |
| A19 (nouveau) | Unité des DAB (4c) | Sites (184) ; appareils (non publiés) | « Sites de DAB » partout ; aucune comparaison directe avec les DAB pour 100 000 adultes de 4e et 4f, qui comptent des appareils → **26/09/2026 : appliqué à O4-02 par la décision S3** (repère UEMOA des DAB au niveau national seulement, appareils contre appareils) |
| A20 (nouveau) | Rupture 2019-2020 des abonnés actifs mobile money (2b) | Série entière, rupture signalée ; ou série arrêtée en 2019 | Série entière, rupture signalée, aucune correction → **Validé le 26/09/2026** |
| A21 (nouveau) | Rattachement des points et contours de 6b (sections 5, 6 et 7) | Rattacher les points par leurs noms déclarés ou par leur position ; utiliser la couche des préfectures telle quelle ou la reconstituer à partir des communes ; garder ou corriger les 8 codes de canton incohérents | Rattachement par les noms déclarés : aucun point perdu. Préfectures reconstituées par fusion des communes, pour que cartes, superficies et comptages portent sur le même territoire (les régions ne changent pas). Codes corrigés par la position pour Kati, Djemegni, Takpamba, Kpaha et Anima ; Agome-Glozou, Akpakpakpé et Yokélé gardés tels que déclarés et signalés → **Validé le 26/09/2026** |

### B. Données absentes des fichiers du projet

Faut-il les rechercher à l'étape suivante, ou abandonner les indicateurs qui en dépendent ? La colonne « Statut » donne le résultat de la recherche du 25/09/2026 dans tout le catalogue d'opendata.gouv.tg et sur geodata.gouv.tg.

| #   | Donnée manquante                                                                                          | Indicateurs bloqués                                     | Statut au 25/09/2026, puis au 26/09/2026                                                                                                                   | Effet si toujours absente                                                    |
| --- | ---------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| B1  | Population de 15 ans et plus par territoire                                                                | O4-02, variantes adultes de O4-04 et O3-04               | Toujours absente. Ratios nationaux par adulte seulement (4e, 4f, Findex) → **26/09/2026 : résolu** : 15 ans et plus par préfecture et par commune, RGPH-5 2022 (RG2, RG3) ; national annuel : IN1 | Population totale à la place, dénominateur signalé                         |
| B2  | Superficie des territoires                                                                                 | O4-02 (par km²)                                         | **Résolu** : superficies calculées à partir des contours de 6b (56 654,6 km² au total)                                            | —                                                                            |
| B3  | Milieu urbain / rural ou taille des localités                                                             | O3-02 (strates), filtre de O4-01 et O4-05                | Toujours absent : aucun classement ni sur opendata ni sur geodata → **26/09/2026 : résolu** : milieu urbain / rural par préfecture et par commune, définition du recensement (RG2, RG3) | Seule la part du Grand Lomé est testée                                      |
| B4  | Couverture 3G/4G par territoire                                                                            | O2-06, O4-06, 3e dimension de O5-01                      | En partie : proxy toutes technologies (3i). Données des tours privées (3h, 11.C6) → **26/09/2026** : toujours un proxy (3i) ; réception déclarée dans les 540 localités de l'EHCVM ; sites par opérateur et par technologie au niveau national seulement (rapport ARCEP 2025) | Voir 11.A17                                                                   |
| B5  | Population annuelle                                                                                        | O1-03, O2-07 (taux)                                      | Trouvée en niveau C : implicite Banque mondiale 1960-2024 (3f), implicite INSEED 2013-2019 (D2, D3) → **26/09/2026 : résolu** : IN1 (projections de l'INSEED 2011-2031, -0,3 % du RGPH en 2022) | Voir 11.A16                                                                   |
| B6  | Chronologie des événements du secteur ; inflation annuelle                                               | Annotations de O1-02 ; croissance réelle de O2-03       | Inflation trouvée (4g : 1967-2022). Chronologie toujours absente → **26/09/2026 : résolu** : chronologie CH1 (40 événements datés, sources et niveaux de preuve), indices de prix mensuels IN2 et IN3 | Ruptures non annotées                                                        |
| B7  | Séries télécom après 2019                                                                              | Objectif 2, O1-03 et O1-04 sur 2020-2024                 | En partie : 2b (jusqu'en 2022), 3f et 2d (jusqu'en 2024). Toujours absents : technologie, parts de marché de la téléphonie, investissement, ARPU → **26/09/2026 : résolu** : AR1, trimestriel 2018-2026 (technologies, opérateurs, CA, investissement, mobile money) | Ces indicateurs restent limités à 2013-2019                                |
| B8  | Champs non publiés de D4, 4c et D5 (guichets, nombre de DAB, service, agents par point)                   | O3-01, O4-01 par type, O3-03                             | Toujours non publiés, masqués aussi sur geodata (« N/A »). Date de collecte trouvée (PRISE 2021/2022)                            | Limites décrites en sections 4 et 5                                          |
| B9  | Page geodata.gouv.tg du dataset 5                                                                          | —                                                       | Résolu : même contenu que D5                                                                                                        | —                                                                            |
| B10 | Tarifs data et mobile money, revenu par habitant, usage déclaré par territoire, compétences, qualité de service | O1-05, O1-06, O2-05, O2-09, O3-05, O3-06           | Toujours absents. Usage déclaré au niveau national seulement (Findex, 4g et 4h) ; 2e n'a pas de lieu → **26/09/2026** : tarifs data et revenu (IT1, AR5, AR6) ; usage déclaré et compétences par région (W1, W2) ; qualité de service au niveau national seulement (AR6 ; O2-09 non couvert par territoire, S9) ; tarifs mobile money (TF1, Flooz seulement en officiel) | Indicateurs abandonnés ; leviers correspondants en « pistes à instruire » |
| B11 (nouveau) | Benchmark externe (Afrique subsaharienne, UEMOA)                                             | Repères de O1-01 et O4-02 ; couche exigée à l'étape 03 | Absent : tous les fichiers portent sur le Togo. Mêmes indicateurs disponibles pour d'autres pays par l'API Banque mondiale (11.C5) → **26/09/2026** : UIT (IT1), Findex (W3) et BCEAO (BC1, BC2) donnent des repères par pays. Repère UEMOA de O4-02 : tranché (R1, précisé par S2 à S4) et téléchargé (C5). Repère Afrique subsaharienne de O1-01 : **résolu le 26/09/2026** (décision S1, C5b) | Seuils absolus seulement                                                      |
| B12 (nouveau) | Lieux candidats (marchés, écoles, formations sanitaires, mairies)                           | Optimisation de localisation (étape 11) ; couche exigée à l'étape 03 | Absents des fichiers ; couches ouvertes sur geodata (11.C4) → **26/09/2026 : résolu** : GD2 dans `obj5/` (11.C4) ; **non requis par les 5 objectifs**, conservé pour un prolongement éventuel (partie G) | Recommandations sans liste de sites                                          |

### C. Téléchargements et demandes : bilan au 26/09/2026

**Tous les téléchargements décidés sont faits** : C3 (6b), C4 (GD2), C5 (C5 et C5b), et l'ensemble des jeux retenus par le journal de recherche (section 12 ; blocs « Données complémentaires téléchargées » des sections 1 à 6). **Aucune ligne de ce tableau n'est un téléchargement en attente, et tous les points sont tranchés depuis le 26/09/2026** (partie G). Les quatre derniers dataient du 25/09/2026 :

- C1 propose de **ne pas** télécharger ;
- C2 porte sur des fichiers **déjà téléchargés** (4h), à garder ou non ;
- C6 est une **demande** à une administration, pas un téléchargement ;
- C7 est un indicateur **facultatif**, hors du 02.

Aucun ne bloquait un indicateur. Décisions du 26/09/2026 : C1 écarté définitivement, C2 conservé, C6 laissé à l'appréciation de l'utilisateur hors du chemin critique, C7 hors périmètre.

| #  | Objet                                                                                                  | Apport                                                                                                            | Proposition                                           |
| -- | ------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| C1 | 2e : `train-full.csv` et `test.csv` (3,26 Go ; le serveur coupe vers 1,08 Go, reprise nécessaire)  | Aucun pour le 02 : pas de date, pas de lieu, échantillon équilibré                                            | Ne pas télécharger ; le profil de l'inventaire suffit → **Écarté définitivement le 26/09/2026** : ni téléchargé ni utilisé dans la suite du projet |
| C2 | 4h : conserver les 3 séries Findex de l'API (codes pris dans 4g, sans lien depuis la page)           | Vague 2024 de la détention d'un compte                                                                          | Conserver (fichiers déjà dans `data/raw/`) → **Validé le 26/09/2026** |
| C3 | geodata : couches ouvertes « Limites administratives » (régions, préfectures, communes, cantons)    | Superficie (B2) ; contrôle du rattachement des points par leurs coordonnées (étape 05) ; géométries du référentiel | **Validé et téléchargé le 25/09/2026 : 6b**        |
| C4 | geodata : couches ouvertes « Marchés », « Établissements scolaires », « Formations sanitaires », établissements administratifs | Couche de lieux candidats (B12)                                                     | Télécharger → **Validé et téléchargé le 26/09/2026 : GD2** (`data/raw/_extradatas/obj5/`, 24 fichiers GeoJSON). **26/09/2026 : non requis par les 5 objectifs** ; conservé sans traitement, utilisé seulement si l'étape 11 va jusqu'à l'optimisation de localisation |
| C5 | API Banque mondiale : agences et DAB pour 100 000 adultes (8 pays de l'UEMOA) ; usage d'Internet (Afrique subsaharienne et 8 pays de l'UEMOA) | Benchmark externe (B11) : repères de O4-02 (décision R1) et de O1-01 (décision S1)                                                                                           | Interroger, en se limitant aux codes déjà utilisés → **Fait le 26/09/2026** : `obj4/C5_worldbank-fas-uemoa_agences-dab-100000-adultes.csv`. Togo (2024) : 4,38 agences et 6,93 DAB pour 100 000 adultes, au-dessus de la moyenne et de la médiane des 8 pays. **Usage d'Internet fait le 26/09/2026** (S1) : `obj1/C5b_worldbank-uit-internet-afrique-subsaharienne-uemoa.csv` |
| C6 | Données des tours télécoms (3h) : demande au MESPTN                                                  | Seule voie vers O2-08 et vers une couverture par technologie                                                     | À ton appréciation : hors de portée d'un script → **Validé le 26/09/2026** : à l'appréciation de l'utilisateur, hors du chemin critique ; sans ces données, O2-06 reste un proxy et O2-08 reste national |
| C7 | geodata : indicateur « Proportion d'élèves dans une école connectée à internet »                   | Contexte de l'objectif 1, par territoire ; hors 02                                                               | Optionnel → **Hors périmètre (26/09/2026)** : contexte éducatif, ne sert aucun des 5 objectifs ; ni téléchargé ni rattaché à GD3 |

### D. Décisions du 26/09/2026

Validées par l'utilisateur à partir de `_RECHERCHE_donnees_manquantes.md` (sections 6, 8, 10 à 12), avec trois points de vigilance.

| #   | Objet                                           | Décision                                                                                                                                                                                                                                                   |
| --- | ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| D-6, D-13 | Périmètre des sources                     | Élargi à l'ARCEP et aux enquêtes auprès des ménages, puis aux autres sources de la section 12                                                                                                                                                         |
| P1  | Version de D1 (A1)                              | API ; chaque année marquée « estimation UIT », sauf 2017                                                                                                                                                                                                |
| P2  | Seuil de stagnation de O1-02                    | Le 02 n'est pas modifié ; l'écart est consigné ici. **Vigilance V2 : la stagnation n'est pas traitée avec le seuil actuel, et le 03 le dit (sections 1 et 10).** Une classe « ralentissement » (croissance < moyenne - 1 écart-type) sera proposée à l'étape d'analyse, appliquée d'abord aux points mesurés → **Précisé le 26/09/2026** : c'est un écart déclaré au 02, au service de l'objectif 1 (intro du 03) |
| P3  | Dénominateur (A16)                              | IN1 pour les taux nationaux que nous calculons ; D1 garde le sien ; O1-03 compare des nombres. **Vigilance V3 : encadré « Dénominateurs : trois bases coexistent » (section 9)**                                                                  |
| P4  | Abonnements Internet et par technologie (A15)   | D2 / 2b jusqu'en 2017, AR1 à partir de 2018 ; dernière publication pour chaque trimestre. **Vigilance V1 : valeur du T4 retenue par convention, pas comme une moyenne ; saisonnalité contrôlée ; moyenne des 4 trimestres testée en sensibilité** (sections 2 et 9 ; R6). Flux : somme des 4 trimestres |
| P5  | Extraction de AR1 en table                      | À l'étape de préparation des données ; ce document décrit le contenu, les ruptures et les révisions                                                                                                                                                      |
| P6  | Portée de la mise à jour du 03                  | Une seule mise à jour, après la recherche sur les objectifs 2 à 5 : c'est celle-ci                                                                                                                                                                      |
| P7  | EHCVM                                           | Ne pas attendre : micro-données obtenues le 26/09/2026 (W2)                                                                                                                                                                                             |
| P8  | Afrobaromètre, vagues 5 à 7                     | Gardées                                                                                                                                                                                                                                                   |
| Q2 à Q4 | 15 ans et plus et milieu par territoire (B1, B3) | Livrets 02 et 03 du RGPH-5, transcrits et contrôlés (RG2, RG3) ; CO1 en contrôle ; GHSL écarté ; livret 01 (cantons) non transcrit (S10 : étape 11 si besoin)                                                                                                           |
| Q5  | Agences de la Poste                             | Comptées à part, en test de sensibilité (GD1)                                                                                                                                                                                                           |
| Q6  | Couverture par territoire (O2-06)               | Proxy 3i confronté au module communautaire de l'EHCVM ; OpenCellID écarté (S9)                                                                                                                                                                          |
| Q7  | Mobile money (O3-03, O3-04)                     | ARCEP pour les séries par opérateur ; BCEAO pour la comparaison UEMOA ; écarts de définition affichés                                                                                                                                                  |
| Q8  | Coût du mobile money (O3-06)                    | Instantané daté des grilles officielles (niveau C) ; momocalc en contrôle seulement                                                                                                                                                                    |
| Q9  | Repère UEMOA de O4-02                           | BC2 téléchargé ; définition vérifiée : la BCEAO compte le mobile money (99 % des points), donc pas de comparaison directe (R1)                                                                                                                         |
| Q10, Q11 | Nouveaux téléchargements                   | Faits le 26/09/2026 (44 fichiers), dont `obj5/` pour les lieux candidats                                                                                                                                                                               |
| Q12 | Comparabilité régionale des deux EHCVM          | Validée avec la précaution « Lomé à part », puis levée par la vérification : mêmes grappes, seul le libellé change (R5)                                                                                                                                |

### E. Décisions R1 à R6 (validées le 26/09/2026)

Validées par l'utilisateur, avec les précisions ci-dessous. Chaque décision est reportée à l'endroit qu'elle concerne (dernière colonne).

| #  | Question                                                             | Décision                                                                                                                                                                                                                                                       | Reporté dans |
| -- | -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| R1 | Repère UEMOA de O4-02 (B11)                                          | **O4-02 utilise le FAS** (agences et DAB pour 100 000 adultes) des 8 pays de l'UEMOA, par l'API de la Banque mondiale — téléchargé (C5), standard cité par le 02. **Pas le taux de la BCEAO (TGPSFd)**, qui compte surtout du mobile money : ses points de monnaie électronique **actifs** (65 043) forment l'essentiel de ses 81 137 points recensés pour le Togo (le total de 81 137 cité à la validation compte aussi les points inactifs ; c'est bien le nombre de points actifs qui entre dans le TGPSFd, contre 629 agences bancaires et 625 de microfinance, soit environ 98-99 % de monnaie électronique dans les deux cas). Le TGPSFd sert seulement de repère à une variante « tous points de service, mobile money compris », qui n'est pas O4-02 | Sections 9, 10 (O4-02), 12 (BC2), 11.C (C5) |
| R2 | Dénominateur « adultes » : IN1 dépasse le RGPH de 6,6 % en 2022      | **RGPH-5 (RG2, RG3)** pour tout ratio par adulte en 2022 et pour tout ratio territorial ; **IN1** seulement pour les séries nationales annuelles, là où le RGPH n'existe pas, jamais dans le même tableau que le RGPH ; **Findex et BCEAO** repris tels que publiés, avec leur propre base               | Sections 6 (D6), 9 (encadré), 11.A16 |
| R3 | O3-06 sans grille officielle de retrait pour Mixx                    | O3-06 calculé sur la grille officielle de Flooz ; pour Mixx, **indicateur partiel** : conditions de transfert officielles connues, **grille officielle de retrait non publiée** ; la grille de momocalc reste en note, jamais en substitut                                                                                                                          | Section 10 (O3-06), 12 (TF1) |
| R4 | Population des communes : RG3 ou D6 ?                                | **RG2 et RG3 sont la source de population des objectifs 3 et 4** : mêmes totaux que D6 (contrôle exact), Danyi 1 et 2 séparées (D6 les fusionne), noms joints sans correction (D6 en demande), âge et milieu disponibles (D6 n'a que le total). **D6 garde un rôle de contrôle**, jamais de source principale pour ces objectifs. **A14 est révisé** : Danyi n'a plus à être regroupée                                        | Sections 6 (D6), 7 (jointures), 10 (O4-02, O4-04, O4-05), 11.A14 |
| R5 | Q12 révisé                                                           | Comparer les deux vagues de l'EHCVM sur les **6 domaines**, Grand Lomé compris, en signalant le changement de libellé (« Lomé commune » puis « Grand Lomé », mêmes 540 grappes) et le calage des poids sur deux bases (7,663 M puis 8,095 M = RGPH-5)                                                                                              | Section 12 (W2), 11.D (Q12) |
| R6 | Lecture de O1-02 sur les abonnements (V1)                            | Une année n'est classée (accélération, ralentissement, régression) que si la valeur du T4 et la moyenne des 4 trimestres **concordent** ; sinon, « dépend de la convention ». À partir de 2018, le **glissement trimestriel** (T / T-4), que le 02 autorise, s'ajoute à la lecture annuelle                                          | Sections 8 (millésimes), 9, 10 (O1-02) |


### F. Décisions S1 à S10 (validées le 26/09/2026)

Points relevés à la relecture complète du journal de recherche (section 14), validés par l'utilisateur avec deux nuances (S8, S9).

| #   | Question                                        | Décision                                                                                                                                                                                                                                                                       | Reporté dans |
| --- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------ |
| S1  | Repère Afrique subsaharienne de O1-01 (B11)     | **Téléchargé** (C5b) : IT.NET.USER.ZS par l'API de la Banque mondiale, agrégat Afrique subsaharienne (moyenne pondérée par la population, 2005-2025) et 8 pays de l'UEMOA (2000-2024). Série du Togo identique à 1b. Findex 2025 (W3) en complément pour 2024, avec sa propre définition (15 ans et plus) | Sections 10 (O1-01, trois couches), 11.B11, 11.C5, 12 (C5b) |
| S2  | O4-02 : moyenne ou médiane de l'UEMOA           | **Moyenne**, comme le 02 (2024 : 3,52 agences, 5,15 DAB pour 100 000 adultes) ; médiane en complément                                                                                                                                                                        | Sections 10 (O4-02), 12 (C5) |
| S3  | O4-02 : périmètre du repère UEMOA               | Territoires comparés au repère UEMOA pour les **agences bancaires** seulement. **DAB** : comparaison UEMOA au niveau national, appareils contre appareils (4f contre C5) ; territoires (sites de 4c) comparés à la médiane nationale (A19). **IMF, assurances, Poste** : médiane nationale seule, « pas de repère UEMOA » | Sections 10 (O4-02), 11.A19, 12 (C5) |
| S4  | O4-02 : échelle                                 | FAS divisé par 10 à l'affichage (pour 10 000 adultes, comme le 02), échelle d'origine en note                                                                                                                                                                                  | Sections 10 (O4-02), 12 (C5) |
| S5  | Âge non déclaré dans les 15 ans et plus         | **Convention** : les 24 180 personnes d'âge non déclaré sont réparties au prorata, dans chaque territoire. Variante « hors non déclarés » en test de sensibilité (écart national : 0,3 % ; plus marqué possible dans les petites communes)                                     | Sections 9 (encadré), 10 (O4-02, O4-04), 12 (population) |
| S6  | Rupture de l'ARCEP entre le T4 2019 et le T1 2020 | Rupture de série : aucune évolution par technologie calculée entre ces deux trimestres ; note de méthode à chercher pendant l'extraction de AR1 (P5). Le recul du total au même trimestre (-6,6 %) est signalé, pas interprété                                              | Sections 10 (O1-04), 12 (AR1) |
| S7  | IN3 : +15 % entre décembre 2019 et décembre 2020 | Non lu comme une hausse des prix tant que la cause n'est pas vérifiée (étape 05, documentation de l'INSEED). L'événement de CH1 est requalifié « statistique »                                                                                                                 | Section 12 (prix, contexte) ; CH1 |
| S8  | GD3 et BM8                                      | **BM8 écarté** (IT1 donne déjà le coût de 1 Go en % du RNB). **GD3 reporté** : à télécharger à l'étape de préparation, quand les besoins des objectifs 4 et 5 seront précis                                                                                                   | Ce tableau |
| S9  | Actions validées mais non faites                | Micro-données MICS6 **abandonnées** (les tableaux régionaux transcrits suffisent). Tableaux d'équipement du RGPH-5 : **demande à l'INSEED à faire par l'utilisateur**, hors du chemin critique. EDS-IV : à suivre. **Ookla et OpenCellID écartés** : O2-09 (optionnel) n'est pas couvert par territoire, et O2-06 reste une couverture théorique ou déclarée | Sections 10 (O2-06, O2-09), 12 (enquêtes, réseau) |
| S10 | RG1 (cantons)                                   | Téléchargé, **non transcrit** : le 02 s'arrête à la commune. À transcrire à l'étape 11 seulement si le ciblage descend au canton                                                                                                                                              | Section 12 (population) |


### G. Décisions du 26/09/2026 sur les parties A et C, et sur GD2

Validées par l'utilisateur sur les propositions des parties A et C, puis, le même jour, A2, le seuil urbain et la règle de O3-02, et le contenu de O2-05. Chaque décision est reportée à l'endroit qu'elle concerne. La colonne « Impact phase 4 » reprend la précision donnée à la validation : ce que chaque décision fixe pour la phase suivante.

| #   | Décision                                                                                                                                                                                  | Impact phase 4 | Reporté dans |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- | ------------ |
| A2  | Libellés « Moov Africa (Atlantique Telecom) » et « Togocom (Togo Cellulaire) » ; les deux correspondances sont confirmées par les données (2b ; ARCEP, AR1) | Fixe les noms d'opérateurs (O1-04, O2-01, O2-02, O2-05a) | Sections 3 (limites), 10 (O2-01) |
| A3  | Accès de D2 sans technologie connue (EvDo, CAFE, GVA, TEOLIS, Illiconet, LS) : « Fixe, technologie non précisée »                                                                         | Fixe la nomenclature de O1-04 et O2-07 | Sections 2 (bloc), 10 (O1-04) |
| A4  | 2b pour la série nationale du CA (2010-2022) ; D3 pour le ratio Investissement / CA (2013-2019) ; AR1 pour 2018-2026. **Sans raccord** : 2b dépasse l'ARCEP de 2,8 % (2021) et de 3,7 % (2022) | Détermine la série de CA utilisée | Sections 3 (limites, bloc), 10 (O2-03) |
| A5  | ARPU de D3 écarté (anomalie ×10¹⁰) ; recalculé depuis AR1 (CA / abonnés moyens / 12), 2018-2026, niveau B | O2-05 porte un ARPU (O2-05a) | Sections 3 (ARPU, bloc), 10 (O2-05) |
| A6  | Statut « Utilisé » seul (660 points) ; les autres statuts en test de sensibilité                                                                                                          | Fixe le comptage de O3-01 et O4-01 | Sections 4 (bloc), 10 (O3-01, O4-01, O4-03) |
| A7  | Catégorie « Mutuelle » (9 points) classée IMF, comme les 27 autres « Mutuelle… »                                                                                                          | Fixe O4-01 par type | Sections 4 (bloc), 10 (O3-01, O4-01) |
| A8  | D5 compté en points (19 788), sans dédoublonnage, points « Nsp » conservés ; libellé « points de service »                                                                               | Fixe O3-03, O4-03 et O4-04 | Sections 5 (bloc), 10 (O3-03, O4-03, O4-04) |
| A9  | Règle 5 de O4-05 telle quelle, avec les sites de DAB de 4c                                                                                                                                | Fixe la classification de O4-05 | Sections 4 (bloc), 10 (O4-05) |
| A10 | Date de référence de D4, 4c et D5 : 2021/2022 (campagne PRISE)                                                                                                                            | Fixe la règle des millésimes pour les croisements | Sections 4 (bloc), 8, 10 (O4-01) |
| A11 | 3e dimension du score (couverture) : tranchée à l'étape du score                                                                                                                          | Aucun | Section 10 (O5-01) |
| A12 | Grand Lomé : 6e unité régionale                                                                                                                                                           | Fixe la présentation de O3-02 | Sections 6 (6b), 10 (O3-02) |
| A13 | Vrai zéro avec avertissement pour D4 et 4c ; « Non déterminable » pour la couverture de 3i à Mô, Kpendjal et Tchamba                                                                      | Fixe l'affichage des cartes | Sections 3 (3i, bloc), 4 (bloc), 10 (O2-06, O4-06) |
| A18 | Indicateurs pré-calculés de geodata (4j, 5c, 3i) : contrôle seulement                                                                                                                     | Fixe la méthode de calcul des ratios | Section 10 (O4-01, O4-04) |
| A20 | Abonnés actifs mobile money de 2b : série entière, rupture 2019-2020 signalée, aucune correction                                                                                         | Fixe O3-04 | Sections 2 (2b), 10 (O3-04) |
| A21 | Points rattachés par leurs noms déclarés ; préfectures reconstituées par fusion des communes ; 5 codes de canton corrigés d'après la position, 3 gardés tels que déclarés et signalés   | Fixe la construction du référentiel territorial | Sections 6 (6b), 7 |
| Seuil O3-02 | 3 strates par commune : Grand Lomé / « autres villes » (50 % d'urbains ou plus, RG3) / rural ; sensibilité à 75 % | Fixe les strates de O3-02 | Section 10 (O3-02) |
| Règle O3-02 | Règle du 02 appliquée telle quelle : elle ne peut pas conclure « confirmée », le Grand Lomé pesant 27,0 % de la population (plafond : 25 %). Deux critères affichés séparément ; lecture par l'indice de concentration et le gradient | Fixe la lecture de O3-02 | Section 10 (O3-02) |
| O2-05 | Deux composantes, libellés distincts : O2-05a, ARPU recalculé (AR1, 2018-2026, niveau B) ; O2-05b, coût de 1 Go (IT1, 2023-2025 : le panier n'existe pas avant ; 04, V6), niveau C, seul soumis au seuil de 2 % | Fixe le contenu de O2-05 | Sections 3 (bloc), 10 (O2-05) |
| C1  | 2e **écarté définitivement** : ni téléchargé ni utilisé                                                                                                                                   | Aucun | Section 2 (fiche 2e) |
| C2  | Séries Findex de 4h conservées (déjà dans `data/raw/`)                                                                                                                                    | Aucun | Partie C |
| C6  | Demande au MESPTN sur les tours : à l'appréciation de l'utilisateur, hors du chemin critique                                                                                              | Aucun (O2-06 reste un proxy) | Partie C |
| C7  | **Hors périmètre** : contexte éducatif, ne sert aucun des 5 objectifs                                                                                                                     | Aucun | Partie C |
| GD2 | Conservé dans `obj5/` sans traitement ; **non requis par les 5 objectifs** ; utilisé seulement si l'étape 11 est atteinte, pour l'optimisation de localisation que la procédure y prévoit | Aucun | Bandeau ; sections 4 (bloc), 10 (trois couches), 11 (B12, C4), 12 (GD2) |
| GD3 | Reporté à l'étape de préparation (S8), puis **non téléchargé** (04, V2) : aucun indicateur du 02 ne l'utilise ; écart déclaré seulement si l'objectif 5 met en évidence un frein énergétique                                                                                                                                                     | Aucun | Partie F |

---

## 12. Sources complémentaires (`data/raw/_extradatas/`)

Validées le 26/09/2026 (décisions D-1 à D-18, P1 à P8, Q1 à Q12, R1 à R6, S1 à S10). Un dossier par objectif principal (`obj1` à `obj5`). Chaque fichier a une ligne dans `_MANIFEST.csv` : URL, date, taille, SHA-256, objectifs servis, fichier source ou dérivé. Les recherches sont détaillées dans `_RECHERCHE_donnees_manquantes.md`, sous la même référence.

**Micro-données de la Banque mondiale** (W2, et W3 pour les micro-données) : obtenues sur le compte de l'utilisateur, sous conditions (usage statistique agrégé, pas de redistribution, pas d'identification des répondants, citation de la source). Leurs dossiers sont ignorés par git.

### Vue d'ensemble

| Réf.     | Contenu                                                                    | Source                  | Période                  | Maille                          | Sert à                             | Preuve |
| -------- | -------------------------------------------------------------------------- | ----------------------- | ------------------------ | ------------------------------- | ---------------------------------- | ------ |
| AR1      | Observatoire trimestriel des marchés (34 numéros)                          | ARCEP                   | T1 2018 - T2 2026        | National, opérateur, technologie | O1-02 à O1-04, O2-01 à O2-07, O3-03, O3-04 | A (comptages publiés) ; taux : B |
| AR2      | Rapports d'activité 2017 et 2025                                           | ARCEP                   | 2016-2025                | National, opérateur             | Chronologie ; O2-08 (sites BTS)    | A      |
| AR3, AR4 | Registre des licences (26/06/2026) ; 3 décisions tarifaires               | ARCEP                   | 2001-2026                | —                               | Chronologie                        | A      |
| AR5, AR6 | Relevé des tarifs (09/2023) ; 9 études (QoS, QoE, tarifs, satisfaction)   | ARCEP                   | 2023-2026                | National ; 94 localités (QoS)   | O2-05, O2-09                       | A à C  |
| IN1      | Projections démographiques par âge et sexe                                 | INSEED                  | 2011-2031                | National                        | Dénominateur annuel (P3)           | C      |
| IN2, IN3 | Indices des prix : postes (dont connexion Internet) et fonction « Communication » | INSEED           | 2010-2024, mensuel       | National                        | Chronologie des prix ; O2-03 réel  | C      |
| IN4      | Accès à l'électricité par préfecture                                       | INSEED                  | 2018-2021                | Préfecture (ancien découpage)   | Contexte des objectifs 4 et 5      | C      |
| BM1-BM3, BM7 | Accès à l'électricité (total, urbain, rural) ; croissance du PIB par habitant | Banque mondiale  | 1961-2023                | National                        | Contexte                           | C      |
| MS1      | Datacenters avec année de création                                         | MESPTN                  | 2016-2022                | Établissement                   | Chronologie                        | A      |
| CH1      | Chronologie consolidée (40 événements)                                     | Compilée (dérivé)       | 2001-2026                | —                                | O1-02 (annotations)                | A (sources officielles) ou C (presse) |
| AS1      | Annuaire statistique national 2024                                         | INSEED                  | Jusqu'en 2024            | National, milieu                 | Point mesuré 2020 (EIPT)           | A à C  |
| AS2      | Annuaires régionaux 2024 (Maritime, Centrale, Kara, Savanes)              | INSEED                  | 2024                     | Préfecture                      | Population estimée par préfecture  | C      |
| RG1-RG3  | Livrets 01 à 03 du RGPH-5 ; transcriptions de RG2 et RG3                   | INSEED                  | 2022                     | Préfecture, commune (canton pour RG1) | B1, B3, O3-02, O4-02, O4-04, O4-05 | A |
| CO1      | Population 2021 par préfecture, sexe et âge                                | OCHA (HDX), base INSEED 2010 | 2021                | 37 préfectures (ancien découpage) | Contrôle de RG2                   | C      |
| W1       | MICS6 : rapport et transcription de 7 tableaux régionaux                  | INSEED, UNICEF          | 2017                     | 7 domaines, milieu               | O1-05, O1-06                       | C (enquête) |
| W2       | EHCVM 2018/19 et 2021/22 : micro-données et documentation                 | INSEED, UEMOA, Banque mondiale | 2018/19, 2021/22  | Région x milieu ; 540 localités | O1-05, O1-06, O2-06, O3 (comptes)  | B (calculé par nous sur échantillon) |
| W3       | Findex 2025 : base tous pays et micro-données Togo                        | Banque mondiale         | 2024                     | National, urbain / rural         | O1-01 (point), O1-06, O3-04, benchmark | C   |
| W4       | Afrobaromètre, vagues 5 à 10                                               | Afrobaromètre           | 2012-2024                | Région (1 200 personnes)         | O1-01 (points), O3-05              | C      |
| IT1      | Paniers de prix TIC                                                        | UIT                     | 2008-2025                | Pays (tous)                      | O2-05, benchmark                   | C      |
| BC1, BC2 | Services financiers numériques 2024 ; inclusion financière 2024 (rapport et tableau de bord) | BCEAO | 2014-2024        | Pays de l'UEMOA                  | O3-03, O3-04 ; benchmark de la variante « tous points de service » (décision R1)       | C      |
| C5       | FAS : agences bancaires et DAB pour 100 000 adultes                        | Banque mondiale (FMI)   | 2010-2024                 | 8 pays de l'UEMOA                | O4-02, benchmark (décisions R1, S2 à S4) | C      |
| C5b      | Individus utilisant Internet (% de la population)                          | Banque mondiale (UIT)   | 2000-2025                 | Afrique subsaharienne (agrégat) ; 8 pays de l'UEMOA | O1-01, benchmark (décision S1)     | C (estimations UIT) |
| TF1      | Grilles tarifaires du mobile money (5 instantanés)                         | Moov Africa, YAS ; momocalc en contrôle | 26/09/2026 | National                  | O3-06 (partiel pour Mixx, décision R3) | C      |
| GD1      | Agences de la Poste (95)                                                   | geodata (PRISE 2021/2022) | Stock                  | Point GPS, région à canton       | O3-01, O4-01 (sensibilité)         | A      |
| GD2      | Lieux candidats : marchés, écoles, formations sanitaires, administrations | geodata (PRISE 2021/2022) | Stock                  | Point ou polygone, région à canton | Prolongement éventuel (étape 11) ; non requis par les 5 objectifs | A      |

### AR1 — Observatoire trimestriel des marchés (ARCEP)

```
Fichiers      : obj1/AR1_arcep_observatoire/AR1_<année>T<n>_<type>.pdf (34 PDF)
Période       : T1 2018 à T2 2026, aucun trimestre manquant ; chaque numéro couvre 5 trimestres
Unité d'obs.  : opérateur x trimestre (et technologie pour les abonnés data)
Format        : PDF, trois mises en page (« Évolution du secteur » 2018, « Tableau de bord » 2019-2021, « Obs-marchés » depuis 2022)
```

- **Contenu** :
  - abonnés à la téléphonie mobile et fixe par opérateur ;
  - abonnés data 2G, 3G, 4G et 5G par opérateur ;
  - Internet fixe et FTTH par opérateur ;
  - trafic data (depuis le T4 2017) et consommation par abonné ;
  - **CA et investissement par opérateur** ;
  - mobile money, au moins depuis le T4 2021 : abonnés, points de vente et valeur des transactions par opérateur ;
  - taux de pénétration, calculés sur les projections de l'INSEED (base IN1).
- **Stocks et flux** : les abonnés, comptes et points de vente sont des stocks de fin de trimestre, et l'annuel est la valeur du T4, **par convention** (P4). Le CA, l'investissement, le trafic et les transactions sont des flux trimestriels, et l'annuel est la **somme** des 4 trimestres. L'investissement est très concentré en fin d'année : 23,6 Md FCFA au T4 2025, soit 55 % de l'année.
- **Révisions** : l'ARCEP révise ses séries d'un numéro à l'autre. Toute l'année 2021 a été révisée dans les numéros de 2022 (abonnements data mobile, de -13 % à -21 %). Pour chaque trimestre, on prend la publication la plus récente.
- **Ruptures à documenter** :
  - 3G et 4G de Moov réunies jusqu'au T3 2019 ;
  - 3G de Togocel : -58 % entre le T4 2019 et le T1 2020, pendant que la 4G progresse (reclassement probable, non documenté). **Décision S6** : rupture de série, aucune évolution par technologie calculée entre ces deux trimestres ; le total data mobile recule aussi au même trimestre (-6,6 %, de 4 671 179 à 4 362 555), signalé sans interprétation ;
  - CA de Togo Telecom : périmètre changé au T2 2025 (voix et data fixes intégrées, location d'infrastructures exclue) ;
  - CA de YAS Togo (Togo Cellulaire) : CA du mobile money non déclaré au T2 2026 (-7 % sur un an, d'après l'ARCEP), ce qui touche O2-02 et O2-05a ;
  - premiers abonnés 5G au T2 2026 (3 951, YAS).
- **Accord avec l'INSEED** : D2 et 2b reprennent les valeurs du T4 de l'ARCEP (2017, 2018, 2020, 2022, et 2021 révisée), sauf 2019, d'origine inconnue (section 2).
- **Limites** : national seulement ; abonnements, jamais utilisateurs (pénétration data mobile de 79,2 % au T2 2026 contre 39,5 % d'utilisateurs dans 1b en 2024) ; extraction des tableaux à faire à l'étape de préparation (P5). La page « Le secteur en chiffres » du site n'affiche que des valeurs de gabarit : elle n'est pas utilisée.

### Population : IN1, RG1 à RG3, CO1, AS2

- **IN1 (projections de l'INSEED)** :
  - 18 tranches d'âge x 3 sexes x 21 ans (1 134 lignes), national ; les tranches somment au total à 2 000 près selon l'année (correction du 26/09/2026 : la fiche précédente disait « à 1 000 près ») ;
  - 2022 : 8 068 000 habitants (-0,3 % du RGPH), mais 5 032 000 de 15 ans et plus (**+6,6 %** du RGPH) ;
  - l'ARCEP utilise la même base (8 811 993 habitants au T2 2026) ;
  - **Décision R2** : IN1 sert seulement aux séries nationales annuelles là où le RGPH n'existe pas (jamais dans le même tableau que le RGPH). Pour tout ratio par adulte en 2022 et pour tout ratio territorial, la source retenue est RG2 / RG3 (ci-dessous).
- **RG2 et RG3 (livrets 02 et 03 du RGPH-5, transcrits le 26/09/2026)** :
  - Contenu : population par 21 lignes d'âge (dont l'âge non déclaré) x milieu (urbain, rural) x sexe. RG2 : national, régions (Maritime avec et sans Grand Lomé, Grand Lomé à part) et 39 préfectures ; RG3 : 117 communes.
  - Contrôles :
    - hommes + femmes = ensemble, urbain + rural = total, somme des âges = total ;
    - préfectures = régions = national, communes = préfectures, cellule par cellule ;
    - totaux égaux à D6 pour les 39 préfectures et les 117 communes.
  - **Écarts relevés** : 24 cellules du livret ont un écart interne de 1 ou 2 personnes. Ils viennent tous d'une même erreur (hommes ruraux de 25-29 ans et de 85 ans et plus de Doufelgou 3), propagée à la préfecture, à la Kara et au national. Ces cellules sont transcrites telles que publiées, et listées dans `RG_rgph5_ecarts-internes-livrets.csv`.
  - Le titre du tableau 100 (« Binah 2 ») est corrigé en Binah 1, d'après l'en-tête de la page et D6.
  - Un « - » du livret vaut 0 (préfectures entièrement urbaines ou rurales).
  - Repères : 15 ans et plus, 4 707 386 hors âge non déclaré (24 180 personnes) ; part urbaine, 42,9 %.
  - **Décision S5** : l'âge non déclaré est réparti au prorata dans chaque territoire (convention) ; la variante « hors non déclarés » est testée en sensibilité.
  - **Limite** : un seul millésime (2022), et pas de ménages.
- **RG1 (livret 01)** : population par sexe jusqu'au canton ; téléchargé, **non transcrit** (décision S10) : le 02 s'arrête à la commune. À transcrire à l'étape 11 seulement si le ciblage descend au canton.
- **CO1 (OCHA, 2021)** : 37 préfectures de l'ancien découpage, projection sur la base du recensement de 2010 ; 15 ans et plus : 61,1 %. Contrôle seulement.
- **AS2 (annuaires régionaux 2024)** : population estimée au 1er janvier par préfecture, pour Maritime, Centrale, Kara et Savanes. L'annuaire 2024 des Plateaux n'est pas publié.

### Enquêtes auprès des ménages : W1 à W4, AS1

Chaque enquête a sa définition, son âge et sa période : **aucun point ne se relie à un autre en série**. La règle du 02 s'applique : un territoire n'est affiché que si son coefficient de variation est inférieur à 30 %.

| Réf. | Enquête | Population et définition | Résultats vérifiés (national) | Territoire | Limites |
| ---- | ------- | ------------------------ | ------------------------------ | ---------- | ------- |
| W1 | MICS6 2017 | 15-49 ans ; « a utilisé Internet au cours des 3 derniers mois » (la définition de l'UIT) | Internet : femmes 14,1 %, hommes 27,6 % ; compétences TIC (ODD 4.4.1) : 3,7 % et 11,2 % ; portable possédé : 56,6 % et 78,3 % ; ménages avec Internet à la maison : 26,5 % | 7 domaines (dont Lomé commune et Golfe urbain à part) et milieu. Femmes, Internet : de 1,4 % (Savanes) à 36,0 % (Lomé commune) | Une date ; 15-49 ans ; transcription des tableaux (660 valeurs, totaux contrôlés) ; micro-données abandonnées (décision S9) : les tableaux transcrits suffisent |
| W2 | EHCVM 2018/19 et 2021/22 | Tous âges, 15 ans et plus calculable ; « a accès à Internet » | 15 ans et plus, pondéré : Internet 23,7 % puis 35,4 % ; portable 60,3 % puis 64,9 % ; alphabétisation 70,8 % en 2021/22 (à reconstruire pour 2018/19) | Strates région x milieu (6 domaines) ; **mêmes 540 grappes aux deux vagues** ; 27 482 et 28 815 individus | « A accès » n'est pas « a utilisé » ; pas de question sur le compte mobile money ; les poids ne sont pas calés sur la même base (7,66 M, puis 8,10 M = RGPH-5). **Décision R5** : les deux vagues se comparent sur les **6 domaines**, Grand Lomé compris (« Lomé commune » puis « Grand Lomé » désignent les 98 mêmes grappes, seul le libellé change), en signalant le changement de libellé et le calage des poids sur deux bases |
| W2 | EHCVM, module communautaire | 540 localités par vague | Réseau mobile « bien capté », pour chacun des 3 réseaux (`s01q13__1` à `__3`) ; électricité, poste, banque ou IMF | Localité enquêtée | Réception **déclarée** par les informateurs de la localité, sur l'échantillon : ni une mesure ni une couverture exhaustive (Q6). Coordonnées GPS des grappes en 2018/19 : à n'utiliser que pour rattacher une grappe à un territoire, jamais à publier |
| W3 | Findex 2025 (données 2024) | 15 ans et plus, 1 000 répondants | Portable 82,5 % ; téléphone principal = smartphone 45,1 % ; Internet au cours des 3 derniers mois 43,7 % ; pas de smartphone à cause du coût 32,1 % | Urbain / rural seulement (pas de région) | Séries TIC nouvelles en 2024 ; national |
| W4 | Afrobaromètre, vagues 5 à 10 | 1 200 adultes par vague | Fréquence d'usage d'Internet (6 vagues) ; téléphone avec accès à Internet (depuis la vague 7) ; compte mobile money (vagues 9 et 10) | Région (petits effectifs) | Précision à contrôler région par région |
| AS1 | EIPT 2020 (annuaire national 2024, tableau 4.17) | **Ménages** | Connexion Internet 43,7 % (urbain 65,9 %, rural 25,2 %) ; portable 88 % ; ordinateur 10 % | Milieu | Ménages, pas individus ; micro-données non disponibles |

**Non retenus (décision S9)** : EDS-IV 2026 (W5), en cours de collecte, à suivre ; tableaux d'équipement TIC des ménages du RGPH-5 (W6), non publiés en ligne : demande à l'INSEED à faire par l'utilisateur, hors du chemin critique.

### Prix, revenu et coût : IN2, IN3, IT1, AR5, AR6, TF1

- **IN2 (IHPC par poste, 2010-01 à 2017-04)** : l'indice « Frais de connexion Internet » passe de 100 à 63,6, avec des baisses datées au mois (2010-07, 2010-12, 2013-01, 2014-02, 2014-10, 2017-01). Défaut : 86 des 88 mois sont en double, sous deux formats de date, avec des valeurs identiques.
- **IN3a et IN3b (fonction « Communication », 2010-2024)** : les deux fichiers sont identiques sur 108 mois communs. **+15 % entre décembre 2019 et décembre 2020** : hausse réelle ou changement de méthode, non vérifié. **Décision S7** : ce saut n'est pas lu comme une hausse des prix tant que la cause n'est pas vérifiée (étape 05, documentation de l'INSEED) ; dans CH1, l'événement est requalifié « statistique ».
- **IT1 (UIT)** : coût de 1 Go de data mobile en % du RNB mensuel par habitant : 5,85 % (2023), 5,45 % (2024), 5,30 % (2025), au-dessus du seuil de 2 % du 02. Panier de 2 Go : de 11,37 % (2021) à 5,68 % (2025). RNB mensuel par habitant : 52 829 FCFA (2024). Tous pays : sert aussi de repère.
- **AR5, AR6 (ARCEP)** : relevé des tarifs de septembre 2023 (instantané HTML) ; analyse des tarifs d'avril 2023 (forfaits data de Moov : -71,4 % entre le T1 2021 et avril 2023) ; analyse comparative d'avril 2024.
- **TF1 (grilles du mobile money, instantanés du 26/09/2026)** :
  - retrait Flooz, grille officielle en 14 tranches : 50 F jusqu'à 500 F ; 100 F de 1 001 à 5 000 F ; 1 000 F de 50 001 à 100 000 F ; en fourchette au-delà ;
  - transfert Flooz : gratuit jusqu'au 3e transfert national ;
  - Mixx : 6 premiers transferts du jour gratuits, puis 1 % ; **aucune grille de retrait officielle publiée** ;
  - momocalc, en contrôle : grille Mixx et taxe de 10 % sur les frais depuis 2024, à vérifier.
  **Décision R3** : O3-06 est calculé sur la grille officielle de Flooz ; pour Mixx, l'indicateur reste **partiel** (transfert calculable, retrait non publié) ; momocalc n'est qu'un contrôle, jamais un substitut. Niveau C ; aucun historique.

### Réseau et qualité de service : AR2, AR6

- **Rapport d'activité 2025 (AR2)** :
  - nombre de sites BTS par opérateur et par technologie, 2021-2025 (tableau 12 ; en 2025 : Moov 718, YAS 1 122), et nombre de cellules 2G, 3G et 4G → O2-08 au niveau national ;
  - étude des fréquences IMT dans 142 localités (« forte disparité régionale ») ;
  - 6 808 localités éligibles au plan de couverture, dont 88 zones blanches (2021).
- **Rapport d'activité 2017 (AR2)** : 3G de Moov commercialisée depuis août 2016 (chronologie).
- **Campagnes de qualité de service (AR6)** : première campagne 2024 dans 94 localités (dont les 39 chefs-lieux de préfecture, région des Savanes exclue), résultats en taux de conformité pour le Grand Lomé et le reste du pays, sans valeur par localité ; analyses QoE data et FTTH (2025, 2026, mesures nPerf) au niveau national, par opérateur. Les deux campagnes de 2025 (84 localités de 36 préfectures) ne sont connues que par le rapport d'activité 2025. → O2-09 au niveau national seulement (décision S9). La campagne du 2e semestre 2023 n'a pas pu être obtenue (lien mort). *Correction du 26/09/2026 : les versions précédentes attribuaient à 2024 les 84 localités des campagnes de 2025.*

### Finance : BC1, BC2, GD1

- **BC1 (BCEAO, services financiers numériques 2024)**, Togo : 12 553 441 comptes de monnaie électronique ouverts ; 6 069 075 actifs à 90 jours (48,35 %) ; 81 137 points de service, dont 65 043 actifs ; 66,2 millions de transactions.
- **BC2 (BCEAO, inclusion financière 2024)** : sept indicateurs par pays, 2014-2024.
  - Taux global de pénétration démographique = points de service / adultes x 10 000. Il compte les guichets bancaires, de microfinance, de la Poste, du Trésor et des caisses d'épargne, **plus les points de monnaie électronique actifs (99 % du total dans l'UEMOA)**.
  - Togo : 116 en 2024 (UEMOA : 193). Pénétration géographique : 1 094 points pour 1 000 km² (+131 en un an, plus forte hausse de l'UEMOA).
  - Le tableau de bord ventile par pays : Togo, 629 points bancaires et 625 de microfinance.
  - **Non comparable à O4-02 tel que défini par le 02** (R1). Le dénominateur « adultes » de la BCEAO n'est pas publié.
- **Décision R1** : O4-02 utilise le FAS (C5, ci-dessous) pour le repère UEMOA, pas le TGPSFd de la BCEAO. Le TGPSFd reste un repère pour une variante « tous points de service, mobile money compris », qui n'est pas O4-02 : ses points de monnaie électronique actifs (65 043 pour le Togo) pèsent l'essentiel des 81 137 points recensés, contre 629 agences bancaires et 625 de microfinance.
- **GD1 (agences de la Poste)** : 95 agences, dont 84 « Utilisé », dans 38 préfectures ; mêmes champs de rattachement que D4 (noms de la région au canton). Comptées à part (Q5).

### C5 et C5b — repères externes (Banque mondiale)

**C5 — FAS, repère UEMOA de O4-02**

```
Fichier       : obj4/C5_worldbank-fas-uemoa_agences-dab-100000-adultes.csv
Source        : API Banque mondiale (indicateurs FAS du FMI, FB.CBK.BRCH.P5 et FB.ATM.TOTL.P5)
Période       : 2010-2024 ; dernière année disponible pour chaque pays (2024 pour les 8)
Unité d'obs.  : pays x année x indicateur
Granularité   : 8 pays de l'UEMOA (Bénin, Burkina Faso, Côte d'Ivoire, Guinée-Bissau, Mali, Niger, Sénégal, Togo)
Lignes        : 215
```

- **Contenu** : agences bancaires commerciales et distributeurs automatiques de billets (DAB, en **appareils**), **pour 100 000 adultes** (échelle FAS ; **décision S4** : divisé par 10 à l'affichage, comme le « pour 10 000 adultes » du 02, échelle d'origine en note).
- **Togo, 2024** : 4,38 agences et 6,93 DAB pour 100 000 adultes. Dans l'UEMOA, la moyenne des 8 pays (repère prévu par le 02) est de 3,52 (agences) et 5,15 (DAB), la médiane de 3,82 et 5,26 : le Togo est au-dessus sur les deux indicateurs, 2e sur 8 pour les agences, 3e sur 8 pour les DAB.
- **Décision R1** : c'est ce repère, pas le TGPSFd de la BCEAO, qui sert de comparaison UEMOA à O4-02, parce qu'il ne compte que des points formels, comme O4-02.
- **Décisions S2 et S3** : le repère est la **moyenne** des 8 pays (médiane en complément). Les territoires ne s'y comparent que pour les **agences bancaires**. Pour les DAB, la comparaison UEMOA se fait au niveau national (appareils : 4f contre C5), et les territoires, comptés en sites (4c), se comparent à la médiane nationale (A19). IMF, assurances et Poste n'ont pas de repère UEMOA.
- **Limites** : mêmes indicateurs que 4e / 4f (Togo seul, déjà en main) ; national par pays, aucune ventilation territoriale ; le dénominateur « adultes » de la Banque mondiale n'est pas documenté, comme pour 4e / 4f.

**C5b — usage d'Internet, repère Afrique subsaharienne de O1-01** (décision S1)

```
Fichier       : obj1/C5b_worldbank-uit-internet-afrique-subsaharienne-uemoa.csv
Source        : API Banque mondiale (IT.NET.USER.ZS, base UIT ; base WDI mise à jour le 13/07/2026)
Période       : agrégat Afrique subsaharienne 2005-2025 ; 8 pays de l'UEMOA 2000-2024
Unité d'obs.  : pays ou agrégat x année
Colonnes      : indicateur, code, pays, iso3, annee, valeur, note_source (note de l'API pour chaque valeur)
Lignes        : 221
```

- **Contenu** : part de la population utilisant Internet ; l'agrégat est une **moyenne pondérée par la population** (méthode de la Banque mondiale), à une décimale.
- **Contrôle** : la série du Togo est identique, année par année, à 1b (version API, 11.A1).
- **Togo face à l'Afrique subsaharienne** : sous la moyenne de 2005 à 2019 (écart maximal : -9,1 points en 2015 ; -3,7 en 2019), au-dessus à partir de 2020 (29,0 % contre 26,7 %), puis +5,9 points en 2024 (39,5 % contre 33,6 %). Dans l'UEMOA, le Togo est 6e sur 8 en 2017, 4e en 2020 et 3e en 2024 (moyenne simple des 8 pays en 2024 : 35,7 %).
- **Niveau de preuve C** : les deux côtés sont des estimations de l'UIT (note « ITU estimate » pour la plupart des valeurs des pays ; aucune note pour l'agrégat). Le passage au-dessus de la moyenne en 2020 coïncide avec le saut de +8,3 points de l'estimation du Togo cette année-là : à lire avec les points mesurés (D-15), pas comme une date établie.
- **Limites** : national par pays ; pas de valeur 2025 pour le Togo ; le Findex 2025 (W3) donne un autre repère régional pour 2024 (15 ans et plus, définition du Findex), à ne jamais mélanger avec celui-ci.

### Lieux candidats : GD2 (`obj5/`)

**Disponible pour un prolongement éventuel, non requis par les 5 objectifs** (décision du 26/09/2026). Aucun des objectifs 1 à 4 n'en a besoin, et l'objectif 5 demande des recommandations dérivées des écarts observés, pas une liste de sites. GD2 est conservé dans `obj5/` sans être traité ; il ne sert que si l'étape 11 va jusqu'à l'optimisation de localisation.

| Couche | Objets | Champs utiles | Remarque |
| ------ | ------ | ------------- | -------- |
| Marchés | 1 078 | Nom, jours de marché, organisme gestionnaire | **Polygones** : centroïde à calculer |
| Établissements scolaires | 15 454 | Catégorie (8 165 écoles primaires, 4 277 jardins d'enfants, 2 304 collèges, 708 lycées), terrain de sport | Points |
| Formations sanitaires | 2 271 | Type (USP 1, USP 2, hôpitaux…), secteur (privé 1 121, public 770…), services | Points |
| Établissements administratifs | 1 576 (21 ministères) | Nom, jours d'ouverture ; MATDDT : 903 (dont les centres d'état civil) | Points |

Toutes les couches viennent de la campagne PRISE 2021/2022, avec les noms de la région au canton : elles se rattachent au référentiel territorial comme D4 et D5. Le rattachement par les coordonnées reste à contrôler (étape 05).

### Contexte : BM1 à BM3, BM7, IN4, MS1, CH1

- **BM1 à BM3** : accès à l'électricité en 2022 : 57,2 % de la population ; 96,5 % en milieu urbain ; 25,0 % en milieu rural.
- **BM7** : croissance du PIB par habitant, 1961-2023 (2020 : -0,4 %).
- **IN4** : taux d'accès à l'électricité par préfecture, 2018-2021, de 1,9 % (Kpendjal) à 98,6 % (Lomé) en 2021. Ancien découpage, avec des préfectures regroupées.
- **MS1** : 3 datacenters avec leur année de création (2016, 2021, 2022).
- **CH1 (chronologie)** : 40 événements datés de 2001 à 2026, avec pour chacun le type, l'opérateur, la source et le niveau de preuve. A pour les sources officielles et les données ; **C pour la presse**, qui sert à annoter une rupture, jamais à en établir la cause. Le saut de l'indice des prix de 2020 (IN3) y est classé « statistique », pas « tarif » (décision S7).
