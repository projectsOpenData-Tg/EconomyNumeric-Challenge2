# 01 — Problem Definition

- Sujet:
    Le mobile s'est imposé au Togo, mais moins de 4 personnes sur 10 utilisent Internet et les banques restent concentrées dans les villes. 
Le mobile money est devenu, pour beaucoup de ménages, la principale porte d'entrée vers les services financiers.

    À partir des données ouvertes sur l'usage d'Internet, le marché des télécoms, les établissements financiers, les agents mobile money et la population, construisez un tableau de bord qui mesure l'adoption du numérique et le rôle du mobile money dans l'inclusion financière. 
Proposez des recommandations pour accélérer l'usage d'Internet et étendre l'accès aux services financiers numériques.


**Objectif du document :** établir une compréhension claire du projet, de ses attentes et de sa logique de traitement à travers un plan structuré.

---

## 1. Contexte du projet

Le mobile s’est largement imposé au Togo, mais moins de 4 personnes sur 10 utilisent Internet. Le projet part de l’**hypothèse** que l’offre de services financiers formels est géographiquement concentrée et que le mobile money joue un rôle important dans l’accès aux services financiers dans les territoires moins dotés en infrastructures financières physiques.

Ces constats de départ ne sont pas des conclusions : ils constituent des **hypothèses à vérifier par les données**. Le projet vise précisément à les mesurer, les nuancer ou les infirmer.

Dans ce contexte, le projet cherche à mesurer deux dynamiques complémentaires :

- **l’adoption du numérique** : usage d’Internet, couverture réseau, marché télécom, technologies disponibles ;
- **le rôle du mobile money dans l’inclusion financière** : présence des établissements financiers, réseau d’agents mobile money, accessibilité réelle pour la population.

Le projet vise donc à construire un **tableau de bord** à partir de données ouvertes (usage d’Internet, marché des télécoms, établissements financiers, agents mobile money, population) et à en tirer des **recommandations ciblées** pour accélérer l’usage d’Internet et étendre l’accès aux services financiers numériques.

---

## 2. Problème global

Le Togo connaît une forte pénétration du mobile, mais cette diffusion ne se traduit pas automatiquement par un usage massif d’Internet ni par une inclusion financière équilibrée sur tout le territoire.

Trois constats structurent le problème, à vérifier par les données :

1. **Un déficit d’usage d’Internet** : moins de 4 personnes sur 10 utilisent Internet, avec des écarts possibles entre milieux urbains et ruraux.
2. **Une concentration géographique possible des services financiers formels** : les banques pourraient être majoritairement implantées dans les villes, laissant de nombreux territoires dépendants du mobile money.
3. **Un manque de visibilité consolidée** : les données existent (ARCEP, BCEAO, INSEED, opérateurs), mais elles sont dispersées et rarement croisées avec la population pour révéler les zones sous-desservies.

**Question centrale du projet :**  
Comment mesurer l’adoption du numérique et le rôle du mobile money dans l’inclusion financière au Togo, afin d’identifier les territoires les moins bien servis et de proposer des recommandations ciblées ?

---

## 3. Explication des objectifs

### Objectif 1 — Retracer l’évolution de l’usage d’Internet au Togo

**Description :**  
Retracer l’évolution de l’usage d’Internet au Togo et repérer les périodes d’accélération ou de stagnation.

**Compréhension :**  
Montrer, sur une période donnée, comment l’usage d’Internet a évolué au Togo. Il s’agit de faire ressortir les moments où l’utilisation a progressé fortement (accélération) et ceux où elle a ralenti, stagné ou reculé (stagnation/régression). Cela implique de construire des séries temporelles fiables et de les rattacher à des événements identifiables : lancement de la 3G/4G, arrivée d’un opérateur, réformes tarifaires, crise sanitaire, etc.

**Points à produire :**
- Séries temporelles sur l’usage d’Internet.
- Taux de pénétration Internet.
- Analyse de l’évolution des indicateurs Internet et, **lorsque les données le permettent**, évolution de la contribution des différentes technologies (3G, 4G, fibre, etc.).
- Identification des périodes d’accélération et de stagnation.

> **Précision méthodologique :** il convient de distinguer soigneusement *usage Internet*, *abonnements Internet*, *abonnements mobile data*, *couverture réseau*, *technologie disponible* et *technologie effectivement utilisée*. On ne peut pas conclure, par exemple, que « 30 % des utilisateurs Internet sont en 4G » si la source ne fournit pas cette information.

---

### Objectif 2 — Analyser le marché des télécommunications

**Description :**  
Analyser le marché des télécommunications : parts de marché des opérateurs, chiffre d’affaires, investissements et passage aux nouvelles technologies (3G, 4G, fibre).

**Compréhension :**  
Faire un constat structuré du marché télécom togolais et en déduire ce qui ressort de :
- la répartition du marché entre opérateurs (parts de marché par abonnés et par chiffre d’affaires) ;
- l’évolution du chiffre d’affaires du secteur ;
- les investissements réalisés, lorsque les données sont disponibles ;
- le passage aux nouvelles technologies (3G, 4G, fibre) ;
- la couverture réseau, lorsque les données sont disponibles.

L’objectif est de comprendre la dynamique de l’offre : qui domine, qui investit, vers quelles technologies le marché se dirige, et si cette dynamique favorise l’accès du plus grand nombre.

**Points à produire :**
- Parts de marché des opérateurs.
- Chiffre d’affaires et abonnés.
- Investissements **lorsque disponibles**.
- Évolution des technologies (3G, 4G, fibre).
- Couverture réseau **lorsque disponible**.

> **Précision méthodologique :** l’ARPU et le CAPEX sont des indicateurs pertinents, mais ils ne doivent pas être considérés comme des livrables obligatoires avant d’avoir vérifié leur disponibilité. Ils seront conservés comme **indicateurs optionnels**, à confirmer dans la matrice de disponibilité des données.

---

### Objectif 3 — Cartographier les établissements financiers et les agents mobile money

**Description :**  
Cartographier les établissements financiers (banques, microfinance, assurances) et les agents mobile money par région, préfecture et commune, **lorsque la localisation des données sources le permet**.

**Compréhension :**  
Sur une carte du Togo, faire apparaître les installations et présences dans chaque région, préfecture et commune :
- les banques ;
- les institutions de microfinance ;
- les assurances ;
- les agents mobile money.

Il s’agit de produire une cartographie fine de l’offre financière, permettant de visualiser les zones densément couvertes et celles qui sont absentes ou très faiblement desservies.

**Points à produire :**
- Cartes à points par type d’établissement.
- Cartes choroplèthes de densité par région, préfecture, commune (selon granularité disponible).
- Tableaux de présence/absence par territoire.

> **Précision méthodologique :** le niveau géographique effectivement atteignable dépendra de la précision des sources. Certaines données peuvent n’être disponibles qu’au niveau régional ou préfectoral, ou avec une adresse approximative. Il ne faut donc pas promettre une carte communale si les données ne le permettent pas.

---

### Objectif 4 — Rapporter ces points d’accès à la population

**Description :**  
Rapporter ces points d’accès à la population : nombre d’habitants par point de service, nombre d’agents mobile money par guichet financier, territoires desservis uniquement par le mobile money.

**Compréhension :**  
À partir des analyses de l’objectif 3, croiser la présence des établissements financiers avec la population afin de mesurer l’accessibilité réelle. Il s’agit de calculer :
- le nombre d’habitants par point de service (banque, microfinance, assurance, ATM) ;
- le nombre d’agents mobile money par guichet financier ;
- les territoires desservis uniquement par le mobile money.

**Cet objectif est le cœur analytique du projet.** C’est lui qui transforme une simple cartographie en véritable outil d’aide à la décision.

**Chaîne logique renforcée :**

> Points de service → Population → Accessibilité → Gap territorial → Dépendance au mobile money

**Variable conceptuelle à créer : Statut d’accès financier du territoire**

Catégories proposées :
- **Desserte financière diversifiée** : présence de banques, IMF, assurances et agents mobile money.
- **Desserte financière faible** : présence limitée de points de service formels.
- **Mobile money dominant** : quelques points formels, mais le mobile money est le principal canal.
- **Mobile money uniquement** : aucun point de service formel, seuls des agents mobile money.
- **Aucune donnée / non déterminable**.

**Exemple de tableau attendu :**

| Territoire | Population | Banques | IMF | Assurances | Agents MM | Habitants / point financier | Situation |
|---|---:|---:|---:|---:|---:|---:|---|
| A | 85 000 | 0 | 1 | 0 | 32 | 85 000 | MM dominant |
| B | 120 000 | 4 | 6 | 2 | 80 | 10 000 | Bien desservi |
| C | 50 000 | 0 | 0 | 0 | 8 | — | MM seul |

**Points à produire :**
- Ratios habitants / point de service.
- Ratio agents mobile money / guichet financier.
- Liste des territoires uniquement couverts par le mobile money.
- Classification des territoires selon leur statut d’accès financier.

---

### Objectif 5 — Proposer des recommandations ciblées

**Description :**  
Proposer des recommandations ciblées pour accélérer l’usage d’Internet et renforcer l’inclusion financière numérique dans les territoires les moins bien servis.

**Compréhension :**  
Se mettre dans la peau d’un décideur et formuler des recommandations opérationnelles en deux volets :
1. **Accélérer l’usage d’Internet** : identifier les failles à corriger pour permettre à toute la population d’utiliser Internet.
2. **Faciliter l’inclusion financière numérique** : identifier les failles à corriger dans les territoires les moins bien servis.

**Principe directeur :**  
Les recommandations devront être **dérivées des gaps effectivement observés** et pourront porter, **selon les résultats**, sur l’infrastructure, l’accessibilité tarifaire, les compétences numériques, l’énergie, la couverture territoriale, le réseau d’agents, l’interopérabilité ou les partenariats.

Ainsi, **les données déterminent la recommandation, et non l’inverse**. Aucune solution n’est présupposée avant l’analyse.

**Points à produire :**
- Recommandations par volet (Internet / inclusion financière).
- Priorisation par territoire.
- Feuille de route et indicateurs de suivi.

---

## 4. Ordre de traitement

L’ordre logique de traitement est le suivant :

1. **Objectif 1 — Évolution de l’usage d’Internet**  
   Point de départ : mesurer la demande numérique et son évolution.

2. **Objectif 2 — Marché des télécommunications**  
   Comprendre l’offre qui rend possible cette demande : opérateurs, investissements, technologies.

3. **Objectif 3 — Cartographie des établissements financiers et agents mobile money**  
   Localiser l’offre d’inclusion financière sur le territoire.

4. **Objectif 4 — Rapport à la population**  
   Croiser l’offre localisée avec la population pour mesurer l’accessibilité réelle et identifier les gaps.

5. **Objectif 5 — Recommandations ciblées**  
   Synthétiser les constats et proposer des actions priorisées pour les territoires les moins bien servis.

> **Remarque :** les objectifs 1 et 2 peuvent être traités en parallèle, de même que les objectifs 3 et 4. L’objectif 5 ne peut être finalisé qu’après consolidation des objectifs 1 à 4.

---

## 5. Matrice de disponibilité des données

Avant de figer les livrables, une **matrice de disponibilité des données** devra être établie pour trancher ce qui est réellement exploitable.

| Indicateur | Source pressentie | Disponible ? | Granularité | Période couverte | Commentaire |
|---|---|---|---|---|---|
| Utilisateurs Internet | ARCEP / ITU / INSEED | À vérifier | National | À vérifier | |
| Abonnés mobile data | ARCEP | À vérifier | National | À vérifier | |
| Répartition par technologie | ARCEP | À vérifier | National | À vérifier | Souvent partielle |
| Parts de marché opérateurs | ARCEP | À vérifier | National | À vérifier | |
| Chiffre d’affaires secteur | ARCEP / opérateurs | À vérifier | National | À vérifier | |
| CAPEX | Opérateurs / ARCEP | Optionnel | National | À vérifier | Souvent non public |
| ARPU | Opérateurs | Optionnel | National | À vérifier | Souvent non public |
| Couverture 3G/4G/fibre | ARCEP / opérateurs | À vérifier | Régional ? | À vérifier | |
| Banques | BCEAO / Commission bancaire | À vérifier | Préfecture ? Commune ? | À vérifier | |
| IMF | BCEAO / APSFD | À vérifier | Préfecture ? Commune ? | À vérifier | |
| Assurances | Ministère / autorité | À vérifier | Préfecture ? Commune ? | À vérifier | |
| Agents mobile money | Opérateurs | À vérifier | Commune ? | À vérifier | |
| Population | INSEED | Disponible | Région / préfecture | À vérifier | Projections |

Cette matrice permettra de valider, avant l’analyse, ce qui peut être produit et à quel niveau de granularité.

---

## 6. Résultats attendus du projet

À l’issue du projet, les livrables suivants sont attendus :

1. **Un tableau de bord** mesurant l’adoption du numérique et le rôle du mobile money dans l’inclusion financière.
2. **Des séries temporelles** sur l’évolution de l’usage d’Internet, avec identification des périodes d’accélération et de stagnation.
3. **Une analyse du marché télécom** : parts de marché, chiffre d’affaires, abonnés, investissements (lorsque disponibles), migration technologique, couverture (lorsque disponible).
4. **Une cartographie** des banques, microfinances, assurances et agents mobile money par région, préfecture et commune (selon granularité disponible).
5. **Des indicateurs d’accessibilité** : habitants par point de service, agents mobile money par guichet, territoires uniquement couverts par le mobile money.
6. **Un statut d’accès financier par territoire** : desserte diversifiée, desserte faible, mobile money dominant, mobile money uniquement, non déterminable.
7. **Des recommandations ciblées et priorisées** pour accélérer l’usage d’Internet et renforcer l’inclusion financière numérique dans les territoires les moins bien servis, dérivées des gaps effectivement observés.

---

## 7. Synthèse

Ce document sert de cadre de référence pour aligner la compréhension du projet, clarifier chaque objectif, définir l’ordre de traitement et encadrer méthodologiquement les livrables.

**Principes directeurs retenus :**
- Les affirmations du sujet sont traitées comme **hypothèses à vérifier**, non comme faits.
- Les livrables sont **conditionnés à la disponibilité réelle des données** (matrice de disponibilité).
- L’objectif 4 est identifié comme **le cœur analytique** du projet.
- Une variable de **statut d’accès financier** est créée pour qualifier chaque territoire.
- Les recommandations sont **dérivées des gaps observés**, et non prédéfinies.


## Trois dimensions analytiques du projet

### Dimension A — Adoption numérique
Population
     ↓
Accès réseau
     ↓
Abonnements / usage Internet
     ↓
Adoption Internet
     ↓
Évolution temporelle

### Dimension B — Offre télécom

Opérateurs
   ↓
Parts de marché
   ↓
CA / investissements
   ↓
Technologies
   ↓
Infrastructure / couverture


###  Dimension C — Inclusion financière

Population
      ↓
Banques / IMF / assurances
      +
Agents Mobile Money
      ↓
Accessibilité territoriale
      ↓
Densité / ratios
      ↓
Territoires sous-desservis
      ↓
Dépendance au Mobile Money

### Conclusion :
A + B + C
   ↓
DIAGNOSTIC TERRITORIAL
   ↓
RECOMMANDATIONS

--- 
Next : 
La prochaine étape logique est vraiment le 02_decision_matrix : pour chaque objectif, on doit définir question décisionnelle → indicateur → données nécessaires → niveau géographique → temporalité → méthode de calcul → visualisation → décision possible.