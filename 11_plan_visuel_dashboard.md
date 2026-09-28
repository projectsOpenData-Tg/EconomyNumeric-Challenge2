# 11 — Plan visuel du tableau de bord

*Quelles pages, quels visuels, quels filtres, et comment chaque résultat du projet est montré à un décideur, avant d'écrire la moindre ligne de code.*

**Objet** : construire le plan de l'interface qui permet au décideur d'explorer tous les résultats du projet (documents 05 à 10), clairement et sans connaissance technique. Ce document correspond à l'étape 12 de la procédure (« dashboard / data story »). Il est un plan : le code viendra après sa validation.

**Point de départ** : la version initiale de ce fichier (conservée dans `tmp/_11_plan_visuel_dashboard_original.md`), qui fixait les règles d'affichage et proposait une page Recommandations. Ce document la complète avec le plan de pages validé en principe le 27/09/2026 (P29 du 10), et la corrige là où les chiffres ou les règles ne tenaient pas (section 10). Mise à jour du 27/09/2026 : une dixième page, « Estimations et projections » (section 9).

**Sources de méthode** : le référentiel du défi 1 (`REFERENTIEL_dashboard-territorial.md`), le bilan après le défi 1 et les captures des deux projets primés, la grille de notation (`tmp/_SCORING_OF_PROJECT.txt`), la procédure (étape 12) et les consignes d'affichage (`_GARDRAILS_DASHBOARD.txt`).

---

## Sommaire

1. Ce qui est noté, et ce qu'on en tire
2. Ce que font les deux projets primés
3. Règles d'affichage
4. Architecture : 11 pages
5. Gabarit commun à toutes les pages
6. Filtres et seuils manipulables
7. Les pages, une par une
8. La page Recommandations
9. La page Estimations et projections
10. Corrections apportées au plan initial
11. Mise en œuvre technique
12. Points à valider

---

## 1. Ce qui est noté, et ce qu'on en tire

| Critère                                        | Points | Note du défi 1 | Ce que le plan doit apporter                                                                                                 |
| ----------------------------------------------- | ------ | --------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| C1 — Ergonomie, clarté visuelle, navigation   | 4      | 2,5             | une navigation en sections, un gabarit identique sur chaque page, des titres qui sont des questions                          |
| C2 — Pertinence des analyses, conclusions      | 8      | 5               | chaque visuel porte son constat et sa limite ; les conclusions du 05 au 10 sont visibles, pas enfouies                       |
| C3 — Interactions, filtres, fluidité          | 4      | **2**     | le point faible du défi 1 : filtres globaux, seuils et poids déplaçables, comparateur, sélecteurs de territoire, exports |
| C4 — Rapport : structure, méthode, rédaction | 4      | 2,5             | hors de ce document ; le rapport sera généré par script à partir des mêmes tables                                       |

**Conséquence** : C1 et C3 valent 8 points sur 20, et c'est là que le défi 1 en a perdu le plus (3,5 sur 8). Le plan donne donc autant de soin à la navigation et aux interactions qu'aux visuels.

---

## 2. Ce que font les deux projets primés

**Projet 1 (application web)** :

- menu latéral en trois groupes (« Principal », « Données », « Pilotage »), fil d'Ariane, recherche globale, bouton d'export ;
- 4 chiffres clés en cartes, chacune avec une petite barre de contexte ;
- un bloc « Lecture des écarts » : trois phrases qui interprètent les indices ;
- une page Recommandations en **cartes**, avec des filtres de priorité en pastilles (haute, moyenne, faible), des onglets par catégorie, un tri par impact et un export CSV.

**Projet 2 (Streamlit, comme nous)** :

- 11 vues en onglets, un en-tête bandeau ;
- une barre latérale de **8 filtres**, dont deux changent l'analyse : le **seuil de zone blanche** (50 %) et la **population minimale** ;
- sur chaque vue, trois bandeaux : « Constat analytique » à côté du graphique, « Analyse data » en bas (un chiffre-titre et 3 puces), « Précision méthodologique » en jaune ;
- un export CSV sur plusieurs vues ; des recommandations en 5 piliers.

**Ce qu'on reprend** : le menu en groupes et les cartes de recommandation du projet 1 ; les trois bandeaux, les filtres latéraux et les seuils déplaçables du projet 2.

**Ce qu'on ne reprend pas** : les cartes du projet 1 affichent en « habitants concernés » la population entière du territoire (8 095 498 pour une action nationale, 500 032 pour Zio), et additionnent des populations qui se recoupent. Notre page Recommandations sépare le chiffre de la cible (points à ajouter, habitants à couvrir) du nombre d'habitants concernés, et n'additionne jamais des populations qui se recoupent (section 8).

---

## 3. Règles d'affichage

### 3.1 Ne pas afficher dans les pages

- noms des fichiers CSV ;
- noms des scripts Python ;
- références aux étapes et aux documents (05, 06, 07, 08, 09, 10) ;
- familles A, B, A×B ;
- détails de recalcul ;
- détails techniques de maille ;
- contrôles d'exhaustivité ;
- noms internes des variables ;
- codes (L1 à L4, O4-01, P9, A13…) lorsqu'ils ne sont pas compréhensibles pour le décideur ; un code n'apparaît qu'avec son intitulé en clair ;
- références techniques du pipeline.

### 3.2 À afficher à la place

Les informations sont reformulées en langage décisionnel :

- KPI clés ;
- écarts territoriaux ;
- déficits ;
- territoires concernés ;
- population exposée ;
- niveau de priorité ;
- niveau de confiance ;
- réserve méthodologique lorsque nécessaire ;
- horizon ;
- action recommandée ;
- conclusion stratégique.

### 3.3 Règles de forme

- **Nom du projet** : « Togo Digital & Financial Inclusion », le même partout : barre du haut, barre latérale, titre de l'onglet du navigateur.
- **Barre du haut**, reprise du tableau de bord du défi 1, fixe en haut de chaque page, en trois zones :
  - à gauche, les armoiries de la République togolaise (l'écu seul) et le nom du ministère : « Ministère de l'Efficacité du Service Public et de la Transformation Numérique » (en anglais : « Ministry of Public Service Efficiency and Digital Transformation »). C'est l'intitulé de l'en-tête de numerique.gouv.tg, pour le ministère créé avec le gouvernement du 8 octobre 2025 (journal de recherche, section 19). Le défi 1 écrivait à tort « Transformation Digitale » ;
  - au centre, le nom du projet, précédé du drapeau, et un sous-titre (« Accès numérique et inclusion financière au Togo ») ;
  - à droite, le sélecteur de langue et la carte du logo Togo AI Lab ;
  - **un fichier à fournir** : le logo Togo AI Lab (`logo_togo_ai_lab.png`) manque aussi dans le défi 1, qui affichait à la place le texte « TOGO AI LAB » ; il se télécharge depuis datalab.gouv.tg. Les armoiries viennent du dossier du défi 1 (licence CC BY-SA 4.0 : l'auteur est cité sur la page Méthodologie) ;
  - le sélecteur de langue du défi 1 (FR, EN) est repris : le tableau de bord est bilingue, en français et en anglais (règles ci-dessous, « Deux langues »).
- **Pied de page**, repris du défi 1, identique sur chaque page, sous la mention des sources : « Togo AI Lab — Data Challenge | Économie numérique — Défi 2 », puis « Diagnostic territorial et aide à la décision pour l'accès numérique et l'inclusion financière au Togo ».
- **Sources** : une mention générale en pied de page (« Données : portail national de données géographiques du Togo et sources institutionnelles complémentaires ») ; le détail va sur la page Méthodologie.
- **Quatre questions par page**, dans cet ordre : quelle est la situation ? où sont les problèmes ? pourquoi ces territoires ? quelle action engager ?
- **Règle des dix secondes** : un message, trois chiffres, une action par page.
- **Aucun chiffre retapé** : tout vient des tables du projet.
- **Couleurs** : palettes déjà validées pour les figures du projet (catégorielle bleu, orange, vert ; rampe bleue pour les classes de priorité ; palette des statuts rouge, ambre, violet, bleu). Une légende pour deux séries ou plus ; jamais deux axes verticaux ; aucune couleur seule pour porter une information (toujours un libellé).
- **Libellés imposés par les analyses** :
  - « Accès déclaré à Internet » (enquête EHCVM) et « Usage d'Internet, toute fréquence » (Afrobaromètre) restent deux libellés distincts ;
  - « couverture théorique » pour la couverture réseau ;
  - « sans fibre recensée » ou « non raccordée » au sens défini, jamais « sans Internet » ;
  - « points de service », jamais « agents », pour le mobile money ;
  - DAB et assurances affichés à part, bien que les recommandations les regroupent avec les banques et les IMF.
- **Deux langues** (français, anglais ; décision du 27/09/2026) :
  - la langue choisie est conservée d'une page à l'autre, comme les filtres ; le français est la langue par défaut ;
  - tous les textes (titres, phrases des cartes, constats, réserves, libellés des classes et des statuts) viennent d'un dictionnaire unique : aucun texte n'est écrit en dur dans une page ;
  - les noms de lieux ne sont pas traduits (Grand Lomé, Savanes, Kéran) ; « Maritime hors Grand Lomé » devient « Maritime excluding Greater Lomé » ; les sigles suivent la langue (UIT / ITU, IMF / MFI, DAB / ATM), BCEAO, ARCEP et EHCVM restent tels quels ;
  - les nombres suivent la langue : 39,5 % et 759 599 en français, 39.5% et 759,599 en anglais ;
  - les libellés imposés ont un équivalent anglais fixé, le même partout :

    | Français | Anglais |
    | -------- | ------- |
    | Accès déclaré à Internet | Self-reported Internet access |
    | Usage d'Internet, toute fréquence | Internet use, any frequency |
    | couverture théorique | theoretical coverage |
    | sans fibre recensée | no recorded fibre |
    | points de service (jamais « agents ») | service points (never "agents") |
    | priorité haute, moyenne, faible | high, medium, low priority |
    | priorité absolue | absolute priority |
    | non classée | not ranked |

  - les exports CSV sont dans la langue choisie ;
  - pied de page en anglais : « Togo AI Lab — Data Challenge | Digital Economy — Challenge 2 ».

---

## 4. Architecture : 11 pages

Le plan concilie trois demandes : les **trois niveaux** validés pour le tableau de bord (chiffres de tête, une page par objectif, le détail), les **7 vues** de la procédure (vue nationale, comparaison territoriale, analyse détaillée, carte, priorités, recommandations, méthodologie) et la page Recommandations de la version initiale.

| #  | Page                        | Groupe du menu | Ce qu'elle montre                                                                                                                                                                                   | Niveau               | Vue de la procédure                            |
| -- | --------------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- | ----------------------------------------------- |
| 1  | Synthèse nationale         | Principal      | les 8 chiffres de tête, chacun avec sa réserve ; trois phrases de lecture                                                                                                                         | 1                    | vue nationale                                   |
| 2  | Usage d'Internet (jusqu'au 28/09/2026 : « Internet : usage et marché ») | Analyses       | usage d'Internet et repère Afrique subsaharienne ; croissance et ruptures (5 à 7 événements) ; accès et freins par région ; le Togo dans l'UEMOA | 2 (objectif 1) | analyse détaillée                             |
| 2 bis | Marché des télécoms (ajoutée le 28/09/2026) | Analyses | parts de marché et concentration ; chiffre d'affaires et investissement ; sites radio ; technologies (2G, 3G, 4G) et fibre ; prix de la data ; couverture théorique et réception déclarée | 2 (objectif 2) | analyse détaillée |
| 3  | Offre financière           | Analyses       | points formels par type (banques, IMF, assurances, DAB à part) ; points mobile money ; opérateurs                                                                                                 | 2 (objectif 3)       | analyse détaillée                             |
| 4  | Population et offre         | Analyses       | habitants par point ; statut d'accès (règle et variante) ; matrice statut × couverture ; communes qui divergent de leur préfecture                                                              | 2 (objectif 4)       | analyse détaillée                             |
| 5  | Carte                       | Analyses       | explorateur : un indicateur, une maille (commune, préfecture, région)                                                                                                                             | 2                    | carte                                           |
| 6  | Priorités                  | Pilotage       | score de priorité décomposé ;**poids modifiables** ; robustesse ; 3 préfectures non classées ; **comparateur de deux préfectures**                                                | 2 (objectif 5)       | priorités, comparaison territoriale            |
| 7  | Diagnostic                  | Pilotage       | une fiche par préfecture prioritaire, avec sélecteur ; 25 communes signalées ; usage d'Internet par région                                                                                      | 2                    | analyse détaillée                             |
| 8  | Recommandations             | Pilotage       | 12 recommandations en cartes ; vues par thème, par territoire, par type d'action ; ordre d'action ; qui agit ; ce qui n'est pas recommandé                                                        | 2 (objectif 5)       | recommandations                                 |
| 9  | Estimations et projections  | Pilotage       | où va-t-on si rien ne change ; scénarios d'usage à 2030 ; cibles à 1, 3 et 5 ans ; trajectoires de référence (Afrique subsaharienne, UEMOA)                                                   | 2 (objectif 5)       | recommandations (scénario prospectif chiffré) |
| 10 | Méthodologie               | Méthodologie  | sources, conventions, les 27 indicateurs avec classes et limites, glossaire des codes                                                                                                               | 3                    | méthodologie                                   |

**Navigation** : menu latéral en quatre groupes (Principal, Analyses, Pilotage, Méthodologie), comme le projet 1. Sur chaque page, un fil d'Ariane et un lien « aller à la page suivante », qui suit l'ordre des quatre questions :

| Question | Pages |
| -------- | ----- |
| 1. Quelle est la situation ? | 1 (Synthèse nationale) |
| 2. Où sont les problèmes ? | 2, 2 bis, 3, 4, 5 (Usage d'Internet ; Marché des télécoms ; Offre financière ; Population et offre ; Carte) |
| 3. Pourquoi ces territoires ? | 6, 7 (Priorités ; Diagnostic) |
| 4. Quelle action engager ? | 8, 9 (Recommandations ; Estimations et projections) |

Le lien « page suivante » va donc de la page 1 à la page 9, dans l'ordre du menu ; la page 9 renvoie à la Synthèse. La page 10 (Méthodologie) est transverse : accessible à tout moment depuis le menu, elle n'est pas dans cette suite.

---

## 5. Gabarit commun à toutes les pages

Chaque page suit le même gabarit, de haut en bas. C'est la réponse à C1 : le lecteur sait où regarder, d'une page à l'autre.

| Zone                                         | Contenu                                                                                                     | Règle                                                                                                                                                                                                                                              |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Barre du haut                                | armoiries et ministère ; nom du projet ; logo Togo AI Lab                                                  | identique sur chaque page (section 3.3)                                                                                                                                                                                                             |
| En-tête                                     | titre sous forme de question (« Où les guichets manquent-ils ? ») ; une phrase de réponse               | la conclusion d'abord                                                                                                                                                                                                                               |
| Chiffres clés                               | 3 ou 4 cartes : valeur, libellé en clair, comparaison (au national, à un seuil, à l'année précédente) | règle des dix secondes                                                                                                                                                                                                                             |
| Visuel principal                             | carte ou graphique, avec infobulle au survol                                                                | une légende, des libellés directs                                                                                                                                                                                                                 |
| **Bandeau « Constat »**              | à côté du visuel : une phrase en termes de décision                                                     | jamais un graphique sans lecture                                                                                                                                                                                                                    |
| Visuel secondaire                            | tableau ou graphique de détail, triable                                                                    | export CSV sous le bloc                                                                                                                                                                                                                             |
| **Bandeau « Synthèse chiffrée »**  | en bas : un chiffre-titre et 3 puces                                                                        | reprise des constats du document source                                                                                                                                                                                                             |
| **Bandeau « Limite de cette page »** | jaune : la réserve propre à ce qui est affiché                                                           | la limite voyage avec l'analyse, elle n'est pas renvoyée à la page Méthodologie. Exception, la Synthèse : ses réserves sont déjà sous chaque chiffre, son bandeau devient « Ce que cette page ne montre pas », discret (section 7, page 1) |
| Pied de page                                 | mention générale des sources ; date des données ; cadre d'identité « Togo AI Lab — Data Challenge »  | aucun nom de fichier ; identique sur chaque page                                                                                                                                                                                                    |

---

## 6. Filtres et seuils manipulables

C'est la réponse à C3. Trois familles d'interactions.

**Filtres globaux** (barre latérale, en pastilles, conservés d'une page à l'autre) :

| Filtre              | Valeurs                                                                                   | Effet                                       |
| ------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------- |
| Région             | les 6 unités (Grand Lomé, Maritime hors Grand Lomé, Plateaux, Centrale, Kara, Savanes) | restreint cartes, tableaux et chiffres      |
| Préfecture         | liste des 39, avec recherche                                                              | idem                                        |
| Maille              | commune, préfecture, région                                                             | change la maille des cartes et des tableaux |
| Classe de priorité | haute, moyenne, faible, non classée, priorité absolue                                   | restreint aux territoires de la classe      |
| Type de milieu      | Grand Lomé, autres villes, rural                                                         | idem                                        |

**Seuils et paramètres qui changent l'analyse** (sur la page concernée, avec la valeur du document rappelée à côté) :

| Paramètre                                  | Page                        | Valeur de référence                 | Ce qui change                                                                                    |
| ------------------------------------------- | --------------------------- | ------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Poids des trois dimensions du score         | Priorités                  | 1/3 chacune                           | score, rang et classe de chaque préfecture ; la classe de référence reste affichée à côté |
| Lecture du score avec ou sans la couverture | Priorités                  | avec (3 dimensions)                   | les 5 préfectures dont la classe change sont signalées                                         |
| Seuil de couverture                         | Population et offre ; Carte | 50 % (zone blanche) et 85 % (couvert) | territoires en zone blanche, cellules critiques                                                  |
| Seuils d'habitants par point formel         | Population et offre         | 10 000 et 30 000                      | classes bien desservi, tendu, sous-desservi                                                      |
| Règle du statut d'accès                   | Population et offre         | règle de référence                 | bascule vers la variante (6 communes et la préfecture de Golfe changent de statut)              |
| Ordre des 22 communes prioritaires          | Recommandations             | par population                        | par isolement (distance au guichet)                                                              |
| Scénario d'usage d'Internet                | Estimations et projections  | les trois                             | affiche un scénario ou les trois                                                                |

Chaque paramètre déplacé affiche un bandeau « Vous regardez une variante : la référence est … ». Le score recalculé utilise la même règle que le document de priorisation (rang percentile, moyenne pondérée) ; aucune autre valeur n'est recalculée dans l'interface.

**Outils de lecture** : recherche globale (territoire ou indicateur) ; **comparateur** de deux préfectures, face à face sur cinq mesures (habitants par point formel, habitants par point mobile money, couverture théorique, score, population) ; infobulles au survol ; **export CSV par bloc** ; lien « voir la fiche » d'un territoire vers la page Diagnostic.

**Blocs exportables** (un bouton « Exporter (CSV) » sous le bloc ; l'export suit les filtres actifs) :

| Page | Bloc exporté |
| ---- | ------------ |
| 1 — Synthèse nationale | préfectures avec leur classe de priorité, leurs habitants et leurs communes sans guichet (déjà en place) |
| 2 — Internet : usage et marché | série annuelle de l'usage d'Internet ; séries du marché (parts, chiffre d'affaires, investissement, sites radio) |
| 3 — Offre financière | points par préfecture et par type (banques, IMF, assurances, DAB à part, mobile money) |
| 4 — Population et offre | ratios par commune (habitants par point formel et par point mobile money, statut d'accès) |
| 5 — Carte | valeurs de l'indicateur affiché, à la maille choisie |
| 6 — Priorités | score par préfecture, ses trois dimensions et sa classe (avec les poids choisis par le lecteur, s'il les a changés) |
| 7 — Diagnostic | les 25 communes signalées |
| 8 — Recommandations | les 12 recommandations ; le tableau du thème affiché (section 8.3) |
| 9 — Estimations et projections | les cibles à 1, 3 et 5 ans ; les scénarios d'usage |
| 10 — Méthodologie | les 27 indicateurs (définition, classe, limite) |

Les pages 1, 5, 7 et 10 complètent la liste proposée le 27/09/2026, qui s'arrêtait à six pages : chaque page a au moins un bloc exportable.

---

## 7. Les pages, une par une

Chaque page indique ses chiffres clés, ses visuels, son constat principal et sa limite. Les visuels existent déjà dans les documents du projet : ils sont reconstruits en version interactive, avec les mêmes données.

### Page 1 — Synthèse nationale : « Le numérique et l'inclusion financière au Togo : où en est-on ? »

Titre retenu le 27/09/2026 : l'ancien titre (« Où en est le Togo ? ») ne disait pas de quoi il parlait. La version longue est gardée, plus claire pour un décideur qui découvre le tableau de bord.

- **Chiffres de tête** (8, en deux rangées). Chaque carte se lit comme une phrase : le chiffre, puis son libellé en clair juste dessous. Viennent ensuite le contexte (seuil ou comparaison) et, en bas, la réserve. L'étiquette colorée est sur la ligne du titre de la carte, pour ne pas séparer le chiffre de sa phrase. Les couleurs des étiquettes restent celles de la palette des statuts (section 3.3).

| # | Chiffre     | Libellé en clair                                                   | Contexte                                                                                                      | Réserve affichée                                                                                            | Étiquette        |
| - | ----------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ----------------- |
| 1 | 39,5 %      | de la population utilise Internet                                   | seuil de 40 % ; Afrique subsaharienne : 33,6 %                                                                | estimation internationale (UIT) ; les enquêtes auprès des ménages en confirment la tendance, pas le niveau | Sous le seuil     |
| 2 | 81,3 %      | des abonnements data mobile sont en 3G ou 4G                        | passage au haut débit acquis en 2025 (seuil : 80 %)                                                          | un abonnement n'est pas une personne : un usager peut avoir plusieurs cartes SIM                              | Seuil franchi     |
| 3 | Duopole     | deux opérateurs se partagent le marché                            | Togocom (YAS) : 64,4 % des abonnés data ; indice de concentration au-dessus de 5 000 chaque année           | aucune                                                                                                        | Très concentré  |
| 4 | 5,30 %      | du revenu mensuel pour 1 Go de data mobile                          | seuil d'accessibilité international : 2 %                                                                    | revenu moyen par habitant, pas revenu médian : pour un ménage modeste, la part est plus lourde              | Non abordable     |
| 5 | 48,3 %      | des comptes mobile money sont actifs                                | la moitié des comptes ouverts dort ; chiffre national                                                        | compte actif : au moins une transaction en 90 jours (définition de la BCEAO)                                 | Usage faible      |
| 6 | 22 communes | n'ont ni banque, ni IMF, ni assurance                               | 759 599 habitants, toutes rurales ; aucun DAB non plus : le mobile money y est seul                           | point formel : banque, institution de microfinance (IMF) ou assurance, recensés en 2021/2022                 | Priorité absolue |
| 7 | 66 communes | où le mobile money remplace presque tous les guichets              | 65,4 % de la population ; plus de 20 points de service pour un guichet ; en plus des 22 communes sans guichet | on compte des points de service, pas des agents                                                               | Guichet rare      |
| 8 | 8 communes  | cumulent mobile money seul ou dominant et couverture réseau faible | 368 534 habitants ; couverture sous 50 % ; mobile money seul dans 5, dominant dans 3                          | couverture théorique (rayon de 20 km autour des antennes), à confirmer par des mesures                      | À confirmer      |

- **Visuel principal** : carte des préfectures colorées par classe de priorité, avec les 22 communes prioritaires en surimpression. Le sous-titre de la carte précise « couverture théorique », puisque le score en dépend.
- **Constat** : « Le déficit est rural et hors du Maritime : 7 préfectures en priorité haute, 989 617 habitants. »
- **Lecture des écarts** : trois phrases (usage national, accès financier rural, prix).
- **Bandeau du bas, « Ce que cette page ne montre pas »** : discret (un filet gris, pas le bandeau jaune), car les réserves sont déjà sous chaque chiffre. Texte : « Les usages : Internet et mobile money ne sont mesurés que pour le pays et les régions, pas commune par commune. L'état actuel des points de service : ils ont été recensés en 2021/2022. Le détail est sur les pages "Internet : usage et marché", "Offre financière" et "Sources et méthode". »

**Corrections apportées à la proposition du 27/09/2026** :

| Dans la proposition                                                            | Problème                                                                                                                                                                                                                                                               | Correction                                                                                                                                                   |
| ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 81,3 % « des abonnements mobiles sont en 3G ou 4G »                          | le dénominateur est celui des abonnements**data** mobile (6 346 056 en 2025), pas de tous les abonnements mobiles, qui comptent aussi la voix seule                                                                                                              | « des abonnements data mobile »                                                                                                                            |
| 8 communes « cumulent mobile money dominant et couverture réseau faible »   | 5 des 8 ont le mobile money**seul** (Agou 2, Akébou 2, Blitta 3, Dankpen 2, Kéran 2), 3 l'ont dominant (Anié 2, Kpendjal-Ouest 1, Oti-Sud 2)                                                                                                                   | « mobile money seul ou dominant » ; la répartition 5 et 3 est affichée                                                                                   |
| Réserve de l'usage d'Internet : « confirmée par les enquêtes ménages »   | les enquêtes confirment la tendance (le ralentissement depuis 2021), pas le niveau : en 2024, 43,7 % (Findex, 15 ans et plus, 3 derniers mois) et 60,8 % (Afrobaromètre, 18 ans et plus, toute fréquence) ; l'accès déclaré de l'EHCVM est de 35,3 % en 2021/2022 | « les enquêtes auprès des ménages en confirment la tendance, pas le niveau »                                                                            |
| Réserve du coût de 1 Go : « seuil d'accessibilité internationale : 2 % »  | c'est un seuil de comparaison, pas une réserve ; la réserve réelle porte sur le revenu (moyen, pas médian)                                                                                                                                                          | seuil dans le contexte ; réserve sur le revenu gardée                                                                                                      |
| 66 communes : « 65,4 % de la population » en réserve                        | c'est un chiffre, pas une réserve                                                                                                                                                                                                                                      | chiffre dans le contexte ; ajout de « en plus des 22 communes sans guichet » (les deux groupes ne se recoupent pas : on peut les additionner, 88 communes) |
| Bandeau du bas : « l'Internet est mesuré à la région, pas à la commune » | l'usage d'Internet est aussi mesuré pour le pays (série de l'UIT) ; l'usage du mobile money est lui aussi régional                                                                                                                                                   | « Internet et mobile money ne sont mesurés que pour le pays et les régions »                                                                             |
| 22 communes « n'ont ni banque, ni IMF, ni assurance »                        | exact ; ces communes n'ont pas non plus de DAB                                                                                                                                                                                                                          | ajout de « aucun DAB non plus » dans le contexte                                                                                                           |

### Page 2 — Usage d'Internet : « L'usage progresse-t-il, et à quel prix ? »

*Depuis le 28/09/2026, la page ne porte plus que l'objectif 1 : le marché et les technologies (objectif 2) ont leur page, la 2 bis. Les chiffres clés, visuels et sites radio décrits ci-dessous pour le marché s'y trouvent désormais.*

- **Chiffres clés** : usage 39,48 % ; accès déclaré dans les Savanes 14,3 % contre 66,7 % dans le Grand Lomé ; 1 Go = 5,30 % du revenu ; investissement 16,3 % du chiffre d'affaires.
- **Visuels** : courbe de l'usage avec repère Afrique subsaharienne et seuil de 40 % ; croissance annuelle en barres (accélération, ralentissement, rupture), 5 à 7 événements annotés ; carte de l'accès déclaré par région ; tableau des freins par région ; parts de marché et concentration ; chiffre d'affaires et investissement (deux graphiques, jamais deux axes) ; **sites radio** ; fibre par préfecture (8 sans fibre recensée).
- **Sites radio** (ajouté le 27/09/2026 : l'indicateur de l'objectif 2 sur le déploiement physique du réseau n'avait aucun visuel) :
  - ajouts nets par an, en barres empilées par opérateur (Moov Africa, YAS) : 215 en 2022, 114 en 2023, 84 en 2024, 21 en 2025 (dont −1 pour YAS) ;
  - repère à 50 : c'est le seuil de veille fixé par la recommandation sur les sites radio. Le cadrage ne donne aucun seuil externe, seulement la règle du « gel » (des ajouts nets proches de zéro deux années de suite) ;
  - le stock de sites (1 406 en 2021, 1 840 en 2025) figure dans le titre du graphique, pas sur un second axe ;
  - la série a 5 années de stock mais 4 années d'ajouts nets : 2021 est la première année connue, elle n'a pas d'ajout net. Les sites ne sont pas ventilés par technologie : les barres par technologie prévues au cadrage ne sont pas faisables ;
  - constat : « Les ajouts nets tombent de 215 à 21 en trois ans ; 2025 est la première année sous le seuil de veille. »
- **Constat** : « L'usage ralentit depuis 2021 ; les Savanes cumulent l'accès le plus faible et l'alphabétisation la plus faible. »
- **Limite** : série d'usage estimée ; accès déclaré n'est pas usage ; événements = coïncidences, pas causes ; marché national seulement ; un site compte une fois, quelle que soit sa technologie.
- **Lien** : « Scénarios à 2030 » vers la page Estimations et projections (section 9).
- **Organisation en sous-onglets** (décidée le 27/09/2026 ; relevé des analyses de l'objectif 1 absentes du tableau de bord, `workspace/conding-progress.md`) :

  | Onglet | Contenu | Source |
  | ------ | ------- | ------ |
  | Vue synthèse | 4 chiffres clés (usage, écart d'accès entre le Grand Lomé et les Savanes, rang dans l'UEMOA, prix de 1 Go) ; courbe de l'usage **depuis 1996**, avec le repère Afrique subsaharienne et les années d'accélération et de ralentissement ; « accélération ou stagnation ? » ; synthèse chiffrée qui renvoie à chaque onglet | 05, figure 4 ; 07, O1-02 |
  | Évolution de l'usage | croissance annuelle classée et 5 événements ; usage selon les enquêtes auprès des ménages ; croissance des abonnements data ; abonnements par utilisateur | 05, figure 4 ; 07, figure 2 et O1-03 |
  | Accès et freins par région | cartes de l'accès déclaré (2018/19, 2021/22) ; carte de l'alphabétisation ; tableau des freins | 06, cartes 9 et 12 ; 07, O1-06 |
  | Le Togo dans l'UEMOA | courbes des 8 pays, une couleur par pays, légende triée avec la valeur de 2024 (28/09/2026), un pays à mettre en évidence au choix ; rang du Togo, écrit sur chaque phase ; classement | 05, figure 11 |
  | ~~Technologies~~ | déplacé le 28/09/2026 sur la page 2 bis, onglet « Technologies et fibre » | 05, figure 5 ; 07, O1-04 |
  | ~~Marché des télécoms~~ | devenu la page 2 bis le 28/09/2026 | 07 |

  La Vue synthèse résume sans dupliquer : un visuel détaillé dans un autre onglet n'y est qu'annoncé. La courbe de l'usage commençait en 2010 dans la première version : un choix de construction, pour la caler sur la période de référence des classes de croissance, jamais écrit dans ce plan ; elle part désormais des premiers utilisateurs (1996), comme la figure 4 du 05.

### Page 2 bis — Marché des télécoms : « Qui tient le marché, et investit-il encore ? »

Ajoutée le 28/09/2026 (relevé de l'objectif 2 dans `workspace/conding-progress.md`, décisions V6 à V9) : l'onglet « Marché des télécoms » de la page 2 n'avait que 3 chiffres clés et 2 visuels, alors que le 05 et le 07 tracent l'évolution des parts de marché, du chiffre d'affaires et de l'investissement. Le menu passe à 11 pages (retour sur la décision V5 du 27/09/2026).

- **Chiffres clés** : Togocom 64,4 % des abonnés data (indice de concentration 5 418) ; chiffre d'affaires 264,9 Md FCFA en 2025, stagnation (+1,0 %) ; investissement 16,3 % du chiffre d'affaires ; fibre jusqu'au domicile 1,74 abonnement pour 100 habitants.
- **Synthèse chiffrée** : 16,3 % du chiffre d'affaires investi en 2025, contre 36,9 % en 2018, à 1,3 point du seuil de sous-investissement.
- **Organisation en sous-onglets** :

  | Onglet | Contenu | Source |
  | ------ | ------- | ------ |
  | Vue synthèse | 4 chiffres clés ; constat ; synthèse chiffrée qui renvoie à chaque onglet | 05 ; 07 |
  | Parts de marché | part de Togocom selon trois mesures (abonnés data, chiffre d'affaires mobile, téléphonie), 2020 marqué comme rupture ; indice de concentration par segment ; positionnement (part du chiffre d'affaires moins part des abonnés) | 05, figure 6 ; 07, O2-01 et O2-02 |
  | Chiffre d'affaires et investissement | chiffre d'affaires classé face à l'inflation (ARCEP en barres, INSEED en ligne, jamais raccordés) ; taux d'investissement classé, seuils de 15 et 25 % ; sites radio, stock dans le titre ; revenu moyen par abonnement | 05, figure 7 ; 07, O2-03, O2-04, O2-05a, O2-08 |
  | Technologies et fibre | 4 chiffres clés ; mix 2G, 3G, 4G ; Internet fixe et fibre par trimestre ; carte des communes sans fibre recensée ; préfectures sans fibre recensée | 05, figures 5 et 13 ; 06, carte 11 ; 07, O1-04 et O2-07 |
  | Prix et couverture | prix de la data par panier, seuil de 2 % ; couverture théorique face à la réception déclarée, par région ; qualité de service non mesurée par territoire | 05, section 4.3 ; 07, O2-05b, O2-06, O2-09 |

- **Limite** : marché mesuré au niveau national seulement ; segments jamais mélangés ; deux sources du chiffre d'affaires jamais raccordées ; couverture théorique, qualité de service non mesurée par territoire.

### Page 3 — Offre financière : « Où sont les établissements financiers ? »

- **Chiffres clés** : points formels (656) ; points mobile money (19 788) ; communes sans assurance (105 sur 117) ; DAB (184, dans 36 communes), affichés à part.
- **Visuels** : carte des points par type, avec un sélecteur de type (banque, IMF, assurance, DAB) ; carte des points mobile money ; carte des opérateurs (deux opérateurs, Togocom seul, Moov seul, non renseigné) ; tableau par préfecture et par type.
- **Les DAB, un type à part** (précisé le 27/09/2026) :
  - dans le sélecteur, les DAB sont un type comme les autres, mais ils ne comptent pas dans les points formels : un DAB installé dans une banque n'est pas un second guichet ;
  - quand le lecteur choisit « DAB », un badge « Type à part : hors des points formels » s'affiche au-dessus de la carte ;
  - le sous-titre rappelle que les 22 communes où le mobile money est seul n'ont pas de DAB non plus (chiffre 6 de la Synthèse) ;
  - une seule carte avec son sélecteur, plutôt qu'une carte des DAB séparée.
- **Constat** : « L'écart oppose les villes aux campagnes, bien plus que Lomé aux autres villes. »
- **Limite** : recensement 2021/2022 ; des lieux, pas des agents ; opérateur non renseigné jusqu'à 23 % des points dans la région de Kara.
- **Ajout du 27/09/2026** : « Offre et usage du mobile money, par région » : carte de l'usage du mobile banking (06, carte 12, moitié droite) et tableau offre face à usage (05, figure 9).

### Page 4 — Population et offre : « Combien d'habitants par point, et où le mobile money est-il seul ? »

- **Chiffres clés** : 22 communes sans point formel ; 66 communes où le mobile money supplée ; 3 communes au maillage mobile money insuffisant ; 8 cellules critiques.
- **Visuels** : cartes des habitants par point formel et par point mobile money (seuils déplaçables) ; carte du statut d'accès (règle de référence, variante à la demande) ; matrice statut × couverture ; liste des communes qui ne sont pas dans la classe de leur préfecture (77 sur 117).
- **Constat** : « Deux communes sur trois ne sont pas dans la classe de leur préfecture : la préfecture cache les communes. »
- **Limite** : population résidente, pas fréquentation (Grand Lomé) ; couverture théorique.

### Page 5 — Carte : « Que voit-on, commune par commune ? »

- **Commandes** : indicateur (habitants par point formel, par point mobile money, couverture, statut d'accès, classe de priorité, fibre, opérateurs) ; maille ; seuil de couverture. La fibre est construite depuis le 28/09/2026 : fibre enterrée et fibre aérienne recensées (km), deux indicateurs jamais additionnés, comme la carte 11 du 06.
- **Visuel** : une carte pleine largeur ; infobulle avec les valeurs du territoire et le lien vers sa fiche.
- **Limite** : celle de l'indicateur choisi, affichée sous la carte.

### Page 6 — Priorités : « Par quels territoires commencer ? »

- **Chiffres clés** : 7 préfectures en priorité haute (989 617 habitants) ; 3 non classées, en priorité haute sur deux dimensions ; 5 préfectures dont la classe dépend de la couverture.
- **Visuels** : classement décomposé (trois dimensions séparées, la couverture marquée comme estimation) ; classe sous chaque test de robustesse ; carte des priorités avec et sans couverture ; **curseurs de poids** ; comparateur de deux préfectures.
- **Constat** : « Les 7 préfectures en priorité haute le restent sous tous les poids testés. »
- **Limite** : un rang est relatif ; la préfecture cache des communes (8 communes sans point formel dans des préfectures en priorité faible).

### Page 7 — Diagnostic : « Pourquoi ces territoires ? »

- **Commandes** : sélecteur de préfecture (les 10 fiches) ; bascule « communes signalées ».
- **Visuels** : fiche de la préfecture (phrase de diagnostic, nature du déficit, offre, communes, réseau et opérateurs, contexte régional) ; carte d'identité des 10 préfectures (tableau coloré) ; carte des 25 communes signalées ; tableau de l'usage d'Internet par région.
- **Constat** : « Le trait commun est la distance au guichet : 39 % des points mobile money à plus de 10 km d'un guichet, contre 6 % ailleurs. »
- **Limite** : associations, pas causes ; distances à vol d'oiseau.

### Page 8 — Recommandations : « Quelle action engager ? »

Voir la section 8.

### Page 9 — Estimations et projections : « Où va le Togo si l'on agit, et si rien ne change ? »

Voir la section 9.

### Page 10 — Méthodologie

Sources et millésimes ; conventions (seuils, règles de classe, variantes) ; les 27 indicateurs avec leur définition, leur classe, leur limite ; glossaire des codes ; décisions prises en cours de projet ; crédits (armoiries : restitution d'Edem Fiadjoe, licence CC BY-SA 4.0, Wikimedia Commons ; logo Togo AI Lab). C'est la seule page où apparaissent les codes internes, toujours avec leur intitulé.

---

## 8. La page Recommandations

Reprend et corrige la proposition de la version initiale, avec les informations du document des recommandations.

**Les 12 recommandations affichées** (les numéros servent au suivi du projet ; la page montre les titres, jamais les numéros) :

| #   | Titre affiché                                                                               | Thème                      | Nature                        | Horizon       |
| --- | -------------------------------------------------------------------------------------------- | --------------------------- | ----------------------------- | ------------- |
| R1  | Un premier guichet formel dans chacune des 22 communes où le mobile money est seul          | points formels              | immédiate, priorité absolue | 1 an          |
| R2  | Des guichets formels dans les 10 préfectures prioritaires                                   | points formels              | immédiate                    | 3 ans         |
| R3  | Des points de service mobile money là où le réseau est mince (8 préfectures, 3 communes) | mobile money                | immédiate                    | 3 ans         |
| R4a | Mesurer la couverture réelle dans 14 communes                                               | couverture réseau          | immédiate, préalable        | 1 an          |
| R4b | Étendre le réseau dans 6 préfectures prioritaires                                         | couverture réseau          | conditionnelle                | 5 ans         |
| R5  | Ramener les frais du petit retrait sous 3 %                                                  | prix et frais               | immédiate, nationale         | 5 ans         |
| R6  | Ramener le coût de 1 Go sous 2 % du revenu                                                  | prix et frais               | immédiate, nationale         | 5 ans         |
| R7  | Relever les compétences numériques dans les Savanes et les Plateaux                        | compétences et équipement | immédiate, régionale        | 5 ans         |
| R7b | Réduire le frein de coût sur le smartphone                                                 | compétences et équipement | immédiate, nationale         | 5 ans         |
| R8  | Garder l'investissement au-dessus de 15 % du chiffre d'affaires                              | investissement (veille)     | veille                        | chaque année |
| R9  | Étendre la fibre aux 8 préfectures non raccordées                                         | fibre                       | immédiate                    | 5 ans         |
| R10 | Relancer les ajouts nets de sites radio (50 par an au moins)                                 | investissement (veille)     | veille                        | 1 à 3 ans    |

### 8.1 Organisation en 4 niveaux

**Niveau 1 — Filtres en haut** (en pastilles) :

| Filtre    | Valeurs                                                                                                                                                       |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Thème    | points formels (banques, IMF, assurances) ; mobile money ; couverture réseau ; fibre ; prix et frais ; compétences et équipement ; investissement (veille) |
| Priorité | priorité absolue (communes « mobile money uniquement ») ; haute ; moyenne ; faible ; non classée                                                          |
| Nature    | immédiate ; conditionnelle ; veille                                                                                                                          |
| Horizon   | 1 an ; 3 ans ; 5 ans                                                                                                                                          |
| Région   | les 6 unités                                                                                                                                                 |
| Maille    | commune ; préfecture ; région ; national                                                                                                                    |

Le type de point (banque, IMF, assurance, DAB) n'est pas un filtre de cette page : les recommandations visent les points formels sans en choisir le type. Il reste un filtre de la page Offre financière.

**Niveau 2 — Vue d'ensemble** (une ligne) :

```text
12 recommandations | 22 communes en priorité absolue (759 599 habitants) | 10 préfectures prioritaires (1 331 015 habitants) | 1 action conditionnelle | 2 veilles
```

Les habitants ne sont jamais additionnés d'une recommandation à l'autre : les territoires se recoupent (les 22 communes sont en partie dans les 10 préfectures).

**Niveau 3 — Cartes** : une carte par recommandation et par territoire.

| Zone               | Contenu                                                                                                                                         |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| En-tête           | thème et titre de l'action                                                                                                                     |
| Chiffre principal  | **la cible chiffrée** : points à ajouter, habitants à faire entrer dans la couverture, ou valeur à atteindre, selon la recommandation |
| Chiffre secondaire | habitants concernés : ceux du territoire visé, pas un gain                                                                                    |
| Description        | 2 phrases : le déficit constaté, la cible                                                                                                     |
| Situation et cible | valeur aujourd'hui → valeur visée, avec le seuil qui la justifie                                                                              |
| Badges             | priorité du territoire ; confiance ; nature (immédiate, conditionnelle, veille) ; horizon                                                     |
| Localisation       | région, préfecture, communes concernées                                                                                                      |
| Liens              | « Voir la fiche du territoire » (page Diagnostic) ; « Voir sur la carte »                                                                   |

**Niveau 4 — Vue carte** : en bas de page, une carte du Togo avec les territoires colorés par priorité, restreinte au thème sélectionné.

**Blocs complémentaires** (sous les cartes, repliables) : ordre d'action (4 rangs) ; qui agit (grille des acteurs et des recommandations, avec le fondement de chaque rôle) ; ce qui n'est pas recommandé, et pourquoi. Le suivi des cibles et les scénarios sont sur la page Estimations et projections (section 9) : la page Recommandations passe de six blocs à quatre.

### 8.2 Exemples de cartes

Une recommandation territoriale, chiffrée en points :

```text
┌──────────────────────────────────────────────────────────────┐
│ Mobile money · Densifier le réseau de points à Blitta        │
├──────────────────────────────────────────────────────────────┤
│   +74 points mobile money          163 272 habitants         │
│   à ajouter                         concernés                 │
│                                                              │
│   Aujourd'hui : 1 814 habitants par point, le réseau le plus │
│   mince des préfectures classées                             │
│   Cible : moins de 1 000 habitants par point (maillage dense)│
│   Dont Blitta 2 (+1) et Blitta 3 (+4), au maillage insuffisant│
├──────────────────────────────────────────────────────────────┤
│ Priorité haute │ Confiance moyenne │ Immédiate │ 3 ans       │
│ Centrale · Blitta · Blitta 2, Blitta 3                       │
│ [Voir la fiche du territoire]  [Voir sur la carte]           │
└──────────────────────────────────────────────────────────────┘
```

Une recommandation conditionnelle, chiffrée en habitants :

```text
┌──────────────────────────────────────────────────────────────┐
│ Couverture réseau · Étendre le réseau à Kéran                │
├──────────────────────────────────────────────────────────────┤
│   36 856 habitants                 128 687 habitants         │
│   à faire entrer dans la           concernés                  │
│   couverture                                                 │
│                                                              │
│   Aujourd'hui : 21,4 % de couverture théorique (zone blanche)│
│   Cible : 50 % (couverture partielle)                        │
│   Condition : confirmer la couverture réelle avant d'agir    │
│   (valeurs douteuses ou inconnues dans Kéran 2 et Kéran 3)   │
├──────────────────────────────────────────────────────────────┤
│ Priorité haute │ Confiance moyenne │ Conditionnelle │ 5 ans  │
│ Kara · Kéran                                                 │
│ [Voir la fiche du territoire]  [Voir sur la carte]           │
└──────────────────────────────────────────────────────────────┘
```

**Correspondance des badges** : « priorité haute, moyenne, faible » = classes 1, 2, 3 du score de priorité de la préfecture ; « priorité absolue » = commune « mobile money uniquement » ; « confiance » = niveau de confiance du score (élevée, moyenne, faible) ; pour les actions nationales, ni priorité territoriale ni confiance, mais la mention « national ».

### 8.3 Vue « par thème »

Quand le décideur choisit un thème, il voit le tableau des territoires concernés, puis les cartes correspondantes. Un tableau par thème, pour les 12 recommandations.

**Points formels** (un premier guichet dans les 22 communes, puis les 10 préfectures prioritaires) :

| Préfecture    | Habitants | Points formels (dont banques) | Cible                              | Points à ajouter | dont apportés par les 22 communes | Priorité                       |
| -------------- | --------- | ----------------------------- | ---------------------------------- | ----------------- | ---------------------------------- | ------------------------------- |
| Est-Mono       | 164 460   | 3 (0)                         | 30 000 habitants par point au plus | +3                | 0                                  | haute                           |
| Kpendjal-Ouest | 123 330   | 3 (0)                         | 30 000 au plus                     | +2                | 0                                  | haute                           |
| Akébou        | 73 830    | 1 (0)                         | 30 000 au plus                     | +2                | 1                                  | haute                           |
| Blitta         | 163 272   | 10 (3)                        | moins de 10 000                    | +7                | 1                                  | haute                           |
| Kéran         | 128 687   | 7 (4)                         | moins de 10 000                    | +6                | 2                                  | haute                           |
| Dankpen        | 185 662   | 6 (2)                         | 30 000 au plus                     | +1                | 1                                  | haute                           |
| Oti-Sud        | 150 376   | 5 (1)                         | 30 000 au plus                     | +1                | 0                                  | haute                           |
| Tchamba        | 200 585   | 12 (1)                        | moins de 10 000                    | +9                | 0                                  | non classée                    |
| Kpendjal       | 88 365    | 0 (0)                         | 30 000 au plus                     | +3                | 2                                  | non classée, priorité absolue |
| Mô            | 52 448    | 2 (0)                         | moins de 10 000                    | +4                | 0                                  | non classée                    |

Les 22 communes « mobile money uniquement » s'affichent au-dessus de ce tableau, avec leur ordre (par population, ou par isolement si le lecteur le choisit).

**Mobile money** (points de service à ajouter) :

| Territoire           | Habitants | Points de service | Habitants par point | Cible                             | Points à ajouter | Priorité du territoire |
| -------------------- | --------- | ----------------- | ------------------- | --------------------------------- | ----------------- | ----------------------- |
| Blitta 2 (commune)   | 46 515    | 9                 | 5 168               | 5 000 au plus                     | +1                | haute                   |
| Blitta 3 (commune)   | 45 218    | 6                 | 7 536               | 5 000 au plus                     | +4                | haute                   |
| Kpendjal 2 (commune) | 40 462    | 5                 | 8 092               | 5 000 au plus                     | +4                | non classée            |
| Dankpen              | 185 662   | 190               | 977                 | 602 (médiane, ordre de grandeur) | +119              | haute                   |
| Blitta               | 163 272   | 90                | 1 814               | moins de 1 000                    | +74               | haute                   |
| Oti-Sud              | 150 376   | 159               | 946                 | 602 (médiane, ordre de grandeur) | +91               | haute                   |
| Kéran               | 128 687   | 139               | 926                 | 602 (médiane, ordre de grandeur) | +75               | haute                   |
| Kpendjal-Ouest       | 123 330   | 129               | 956                 | 602 (médiane, ordre de grandeur) | +76               | haute                   |
| Kpendjal             | 88 365    | 41                | 2 155               | moins de 1 000                    | +48               | non classée            |
| Mô                  | 52 448    | 32                | 1 639               | moins de 1 000                    | +21               | non classée            |
| Tchamba              | 200 585   | 205               | 978                 | 602 (médiane, ordre de grandeur) | +129              | non classée            |

Les 490 points de la médiane (Dankpen, Oti-Sud, Kéran, Kpendjal-Ouest, Tchamba) portent la mention « ordre de grandeur » : ces préfectures sont déjà dans la meilleure classe ; les 152 autres points franchissent un seuil.

**Couverture réseau, étape 1 : mesurer** (immédiate, 1 an) :

| Commune         | Préfecture | Habitants         | Couverture aujourd'hui | Raison de la mesure         |
| --------------- | ----------- | ----------------- | ---------------------- | --------------------------- |
| Tchamba 1       | Tchamba     | 82 451            | inconnue               | inconnue                    |
| Anié 2         | Anié       | 79 413            | 5,2 %                  | valeur douteuse             |
| Tchamba 2       | Tchamba     | 64 930            | inconnue               | inconnue                    |
| Sotouboua 2     | Sotouboua   | 64 187            | inconnue               | inconnue                    |
| Kéran 2        | Kéran      | 53 305            | 1,5 %                  | valeur douteuse             |
| Tchamba 3       | Tchamba     | 53 204            | inconnue               | inconnue                    |
| Kpendjal 1      | Kpendjal    | 47 903            | inconnue               | inconnue                    |
| Sotouboua 1     | Sotouboua   | 46 907            | 14,5 %                 | préfecture en zone blanche |
| Blitta 3        | Blitta      | 45 218            | 9,9 %                  | valeur douteuse             |
| Kpendjal 2      | Kpendjal    | 40 462            | inconnue               | inconnue                    |
| Kéran 3        | Kéran      | 30 983            | inconnue               | inconnue                    |
| Mô 1           | Mô         | 30 522            | inconnue               | inconnue                    |
| Sotouboua 3     | Sotouboua   | 27 770            | 94,5 %                 | préfecture en zone blanche |
| Mô 2           | Mô         | 21 926            | inconnue               | inconnue                    |
| **Total** |             | **689 181** |                        |                             |

**Couverture réseau, étape 2 : étendre** (conditionnelle : après la mesure, 5 ans) :

| Préfecture     | Habitants | Couverture théorique | Cible | Hors couverture aujourd'hui | À faire entrer dans la couverture | Priorité |
| --------------- | --------- | --------------------- | ----- | --------------------------- | ---------------------------------- | --------- |
| Dankpen         | 185 662   | 63,8 %                | 85 %  | 67 247                      | 39 397                             | haute     |
| Est-Mono        | 164 460   | 74,5 %                | 85 %  | 41 872                      | 17 203                             | haute     |
| Oti-Sud         | 150 376   | 58,6 %                | 85 %  | 62 271                      | 39 714                             | haute     |
| Kéran          | 128 687   | 21,4 %                | 50 %  | 101 199                     | 36 856                             | haute     |
| Kpendjal-Ouest  | 123 330   | 64,0 %                | 85 %  | 44 423                      | 25 924                             | haute     |
| Akébou         | 73 830    | 58,2 %                | 85 %  | 30 854                      | 19 779                             | haute     |
| **Total** |           |                       |       | **347 866**           | **178 873**                  |           |

**Fibre** (étendre le réseau de transport, 5 ans) :

| Préfecture     | Région                   | Habitants         | Priorité    |
| --------------- | ------------------------- | ----------------- | ------------ |
| Kpendjal-Ouest  | Savanes                   | 123 330           | haute        |
| Akébou         | Plateaux                  | 73 830            | haute        |
| Kpendjal        | Savanes                   | 88 365            | non classée |
| Mô             | Centrale                  | 52 448            | non classée |
| Yoto            | Maritime hors Grand Lomé | 174 851           | moyenne      |
| Bas-Mono        | Maritime hors Grand Lomé | 94 860            | moyenne      |
| Moyen-Mono      | Plateaux                  | 90 505            | moyenne      |
| Danyi           | Plateaux                  | 40 240            | faible       |
| **Total** |                           | **738 429** |              |

**Prix et frais** (national, 5 ans) :

| Action                                         | Aujourd'hui              | Cible                 | Habitants concernés                                                                             |
| ---------------------------------------------- | ------------------------ | --------------------- | ------------------------------------------------------------------------------------------------ |
| Frais d'un retrait de 1 000 FCFA chez un agent | 75 FCFA (7,5 %)          | 30 FCFA au plus (3 %) | national ; d'abord les 6 054 427 habitants des communes où le mobile money est seul ou dominant |
| Coût de 1 Go de data mobile                   | 5,30 % du revenu mensuel | 2 % au plus           | national ; au rythme 2023-2025, vers 2037                                                        |

**Compétences et équipement** (5 ans) :

| Territoire | Aujourd'hui                                                                         | Cible                                                  | Habitants concernés |
| ---------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------ | -------------------- |
| Savanes    | alphabétisation 41,2 % ; compétences numériques 0,4 % (femmes) et 4,1 % (hommes) | sortir du quart le plus faible : 62,05 %, 1,3 %, 5,3 % | 591 519 adultes      |
| Plateaux   | compétences numériques 1,0 % (femmes) et 4,0 % (hommes)                           | 1,3 % et 5,3 %                                         | 917 528 adultes      |
| National   | 32,1 % des adultes privés de smartphone par son coût                              | baisse (pas de seuil fixé)                            | 1 514 288 adultes    |

**Investissement (veille)** (chaque année) :

| Mesure                             | Aujourd'hui                         | Seuil d'alerte | Si le seuil est franchi                                                         |
| ---------------------------------- | ----------------------------------- | -------------- | ------------------------------------------------------------------------------- |
| Investissement des opérateurs     | 16,3 % du chiffre d'affaires (2025) | 15 %           | mobiliser le fonds du service universel                                         |
| Sites radio ajoutés dans l'année | 21 (2025)                           | 50             | deux années de suite sous le seuil : gel de l'investissement réseau constaté |

### 8.4 Vue « par territoire »

Quand le décideur choisit une préfecture (par exemple Dankpen, Kara, 185 662 habitants, priorité haute, confiance élevée), il voit toutes les actions qui la concernent :

| Thème                      | Action                                                              | Cible                                                                  | Nature         | Horizon |
| --------------------------- | ------------------------------------------------------------------- | ---------------------------------------------------------------------- | -------------- | ------- |
| Points formels, communes    | un point formel à Dankpen 2 et un à Dankpen 3 (priorité absolue) | sortir du statut « mobile money uniquement »                         | immédiate     | 1 an    |
| Points formels, préfecture | +1 point, déjà apporté par l'action sur les communes             | 30 000 habitants par point au plus                                     | immédiate     | 3 ans   |
| Mobile money                | +119 points                                                         | 602 habitants par point (médiane des préfectures, ordre de grandeur) | immédiate     | 3 ans   |
| Couverture réseau          | +39 397 habitants dans la couverture                                | 85 %                                                                   | conditionnelle | 5 ans   |
| Prix et frais               | actions nationales (prix de la data, frais du petit retrait)        | nationales                                                             | immédiate     | 5 ans   |

Dankpen n'a pas d'action « fibre » (une fibre aérienne y est recensée) ni « compétences » (la région de Kara n'a pas de frein de capacité présumé).

### 8.5 Vue « par type d'action »

| Type d'action                                   | Territoires                                                          | Habitants concernés               |
| ----------------------------------------------- | -------------------------------------------------------------------- | ---------------------------------- |
| Ouvrir un premier point formel                  | 22 communes « mobile money uniquement »                            | 759 599                            |
| Ajouter des points formels                      | 10 préfectures prioritaires (31 points après ceux des 22 communes) | 1 331 015                          |
| Ajouter des points mobile money                 | 8 préfectures et 3 communes au maillage insuffisant                 | 1 092 725                          |
| Mesurer la couverture réelle                   | 14 communes, dont Mô, Kpendjal, Tchamba et Sotouboua entières      | 689 181                            |
| Étendre le réseau (après la mesure)          | 6 préfectures prioritaires sous 85 %                                | 347 866 hors couverture théorique |
| Étendre la fibre                               | 8 préfectures non raccordées                                       | 738 429                            |
| Agir sur les prix et les frais                  | national                                                             | national                           |
| Compétences numériques                        | Savanes, Plateaux                                                    | 1 509 047 adultes                  |
| Équipement en smartphone                       | national                                                             | 1 514 288 adultes citant le coût  |
| Veiller sur l'investissement et les sites radio | national                                                             | national                           |

---

## 9. La page Estimations et projections

Ajoutée le 27/09/2026 : la page Recommandations portait six blocs, c'était trop. Les deux pages se partagent désormais le travail :

- **Recommandations** : ce qu'on fait, maintenant ;
- **Estimations et projections** : où on va, si l'on agit ou si rien ne change.

Question de la page : « Où va le Togo si l'on agit, et si rien ne change ? »

### 9.1 Chiffres clés

Trois cartes, chacune avec la valeur d'aujourd'hui, la valeur au rythme actuel, et la cible :

| Carte                          | Aujourd'hui                         | Au rythme actuel                    | Cible                                                   |
| ------------------------------ | ----------------------------------- | ----------------------------------- | ------------------------------------------------------- |
| Usage d'Internet               | 39,48 % (2024)                      | 51,1 % en 2030                      | 60 % (usage généralisé) : vers 2035 au rythme actuel |
| Coût de 1 Go                  | 5,30 % du revenu mensuel (2025)     | 3,9 % en 2030                       | 2 % : vers 2037 au rythme actuel                        |
| Investissement des opérateurs | 16,3 % du chiffre d'affaires (2025) | pas de projection : série cyclique | 15 % au moins (seuil d'alerte)                          |

### 9.2 Où va-t-on si rien ne change ?

| Indicateur            | Dernière valeur                                | 2030 au rythme actuel                       | Lecture                                                                                                                                                                                              |
| --------------------- | ----------------------------------------------- | ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Usage d'Internet      | 39,48 % (2024)                                  | 51,1 %                                      | le seuil de 40 % est franchi dès 2025 ; 60 % attend 2035                                                                                                                                            |
| Coût de 1 Go         | 5,30 % (2025)                                   | 3,9 %                                       | pour atteindre 2 % en 2030, il faudrait aller 2,4 fois plus vite                                                                                                                                     |
| Investissement        | 16,3 % (2025)                                   | pas de projection                           | la série monte et descend (20,1 % en 2020, 32,1 % en 2023) ; si la baisse de 2025 se répétait, 13,3 % en 2026, sous le seuil                                                                      |
| Couverture théorique | 88,4 % de la population (recensement 2021/2022) | pas de projection : un seul point de mesure | l'extension prévue ferait entrer 178 873 habitants de plus dans la couverture de 6 préfectures ; aucun taux national n'est recalculé, car les deux chiffres n'ont pas la même base de population |

### 9.3 Scénarios d'usage d'Internet à 2030

| Scénario                                         | Rythme             | Usage en 2030 | 60 % atteint en |
| ------------------------------------------------- | ------------------ | ------------- | --------------- |
| Tendanciel (rythme 2023-2024)                     | +1,9 point par an  | 51,1 %        | 2035            |
| Accéléré (rythme 2019-2024)                    | +4,0 points par an | 63,5 %        | 2030            |
| Ambitieux (années d'accélération 2016 et 2020) | +6,2 points par an | 77,0 %        | 2028            |

- **Visuel** : la courbe observée depuis 2010, prolongée par les trois scénarios en pointillés, avec les seuils de 40 % et de 60 % ; le lecteur affiche un scénario ou les trois.
- **Constat** : « Le seuil de 40 % est à portée dès 2025 ; au rythme actuel, l'usage généralisé (60 %) attend 2035. »

### 9.4 Cibles à 1, 3 et 5 ans

Une ligne par recommandation : la valeur de départ, la cible (le seuil de la classe supérieure), l'horizon et ce qui compte comme un succès. Sous le tableau, des jauges « aujourd'hui → cible ».

| Action                                         | Aujourd'hui                                                      | Cible                                          | Horizon       | Succès                                 |
| ---------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------- | ------------- | --------------------------------------- |
| Premier guichet dans les 22 communes           | aucun guichet (2021/2022)                                        | au moins 1 par commune                         | 1 an          | la commune n'a plus que le mobile money |
| Guichets dans les 10 préfectures prioritaires | de 16 327 à 73 830 habitants par point ; Kpendjal : aucun point | 30 000 au plus pour 6 ; moins de 10 000 pour 4 | 3 ans         | la préfecture change de classe         |
| Points de service mobile money                 | de 926 à 8 092 habitants par point                              | 5 000, 1 000 ou 602 selon le territoire        | 3 ans         | seuil franchi                           |
| Mesure de la couverture                        | inconnue ou douteuse dans 14 communes                            | couverture mesurée                            | 1 an          | une valeur dans chaque commune          |
| Extension du réseau                           | de 21,4 % à 74,5 % (théorique)                                 | 50 % à Kéran, 85 % ailleurs                  | 5 ans         | seuil franchi sur la couverture réelle |
| Frais du petit retrait                         | 7,5 % (1 000 FCFA)                                               | 3 % au plus                                    | 5 ans         | 30 FCFA au plus                         |
| Coût de 1 Go                                  | 5,30 % du revenu                                                 | 2 % au plus                                    | 5 ans         | seuil d'accessibilité franchi          |
| Compétences numériques                       | alphabétisation 41,2 % (Savanes) ; compétences 0,4 à 4,1 %    | sortir du quart le plus faible                 | 5 ans         | seuil franchi                           |
| Équipement en smartphone                      | 32,1 % des adultes privés par le coût                          | baisse                                         | 5 ans         | baisse mesurée à l'enquête suivante  |
| Investissement                                 | 16,3 % du chiffre d'affaires                                     | 15 % au moins                                  | chaque année | rester au-dessus du seuil               |
| Fibre                                          | 8 préfectures sans fibre recensée                              | chaque préfecture raccordée                  | 5 ans         | fibre recensée                         |
| Sites radio                                    | 21 ajouts nets (2025)                                            | 50 au moins par an                             | 1 à 3 ans    | pas deux années de suite sous le seuil |

### 9.5 Trajectoires de référence

Chaque série est prolongée avec la même règle que le scénario tendanciel du Togo : la moyenne des deux dernières variations annuelles, depuis la dernière année observée.

| Territoire                 | Dernière valeur                         | Rythme récent    | 2030 au même rythme |
| -------------------------- | ---------------------------------------- | ----------------- | -------------------- |
| Togo                       | 39,48 % (2024), 3e des 8 pays de l'UEMOA | +1,9 point par an | 51,1 %               |
| Afrique subsaharienne      | 35,7 % (2025)                            | +1,7 point par an | 44,2 %               |
| UEMOA, médiane des 8 pays | 35,4 % (2024)                            | +1,3 point par an | 43,0 %               |

- **Visuel** : les trois courbes observées, puis prolongées en pointillés ; le Sénégal (60,1 % en 2024) en repère.
- **Constat** : « Au rythme actuel, le Togo garde son avance sur l'Afrique subsaharienne, sans rattraper le Sénégal. »

### 9.6 Ce qui est incertain

Bandeau « Limite de cette page » :

- la série d'usage du Togo est une estimation de l'UIT ;
- les prolongements sont linéaires : ce sont des ordres de grandeur, pas des prévisions ;
- aucune donnée ne dit quelle action produit quel rythme : les événements passés sont des coïncidences, pas des causes ;
- le coût de 1 Go n'a que trois points de série (2023 à 2025).

### 9.7 Chiffres corrigés dans la proposition

| Dans la proposition                                                                                            | Problème                                                                                                                                                                          | Correction                                                            |
| -------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| Coût de 1 Go en 2030, tendanciel : environ 4,5 %                                                              | au rythme 2023-2025 (−0,275 point par an), 5,30 − 5 × 0,275 = 3,9 %                                                                                                             | 3,9 %                                                                 |
| Investissement en 2030, tendanciel : environ 13 %                                                              | 13,3 % est la valeur de 2026 si la baisse de 2025 se répétait ; prolongée à 2030, la même règle donnerait 1,3 %, ce qui n'a pas de sens pour une série qui monte et descend | pas de projection à 2030 ; alerte pour 2026                          |
| Couverture : 88,4 % en 2024-2025, 95 % si l'extension est faite                                                | 88,4 % date du recensement 2021/2022 ; 95 % ne vient d'aucun calcul ; ajouter les habitants de l'extension à un taux national mélangerait deux bases de population               | 88,4 % (2021/2022) ; l'extension est exprimée en habitants (178 873) |
| Afrique subsaharienne en 2030 : environ 40 %                                                                   | la série a une valeur 2025 (35,7 %) ; avec la même règle que le Togo, elle atteint 44,2 %                                                                                       | 44,2 %, calculé                                                      |
| Colonne « ambitieux » pour le coût (« 2 % si action ») et l'investissement (« plus de 15 % si veille ») | ce sont des cibles, pas des scénarios                                                                                                                                             | colonne « cible » séparée (section 9.1)                           |

---

## 10. Corrections apportées au plan initial

| Dans la version initiale                                                                                                                            | Problème                                                                                                                                                                                                                                                 | Correction                                                                                               |
| --------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| « 8 recommandations\| 12,3 M habitants concernés \| 3 priorités hautes \| 5 moyennes »                                                          | 12 recommandations depuis le 27/09/2026 ; 12,3 millions dépasse la population du Togo (8,1 millions) : des populations qui se recoupent ont été additionnées ; les nombres de priorités ne correspondent à aucune règle                            | ligne refaite sans addition (section 8.1)                                                                |
| Carte « Renforcer le réseau mobile money à Zio »                                                                                                | reprise d'une carte du projet primé ; Zio (priorité moyenne) n'est dans aucune de nos recommandations ; « 214 850 habitants à couvrir » et « 56 points » ne viennent pas de nos données ; « 39,89 points » est un écart en habitants par point | deux exemples réels : Blitta et Kéran (section 8.2)                                                    |
| « Population à couvrir (le gain réel) » comme chiffre principal de toutes les cartes                                                            | ce chiffre n'existe que pour la couverture réseau ; ajouter des points ne « couvre » pas des habitants mesurables                                                                                                                                      | chiffre principal = la cible propre à chaque recommandation                                             |
| Badges « Priorité (08), confiance (08) », lien « fiche diagnostic (09) », « priorité 2 au score O5-01 », « Indicateur : O4-04 »           | les numéros de documents et les codes sont exclus des pages (section 3.1)                                                                                                                                                                                | libellés en clair                                                                                       |
| Filtres par thème « IMF / Assurance / Banque / DAB »                                                                                             | les recommandations ne choisissent pas le type de point ; les DAB sont hors du compte des points formels                                                                                                                                                  | thèmes alignés sur les recommandations ; le type de point reste un filtre de la page Offre financière |
| Vue par thème « IMF » : Est-Mono « points IMF 3 → 6 »                                                                                         | la cible porte sur l'ensemble des points formels, pas sur les IMF                                                                                                                                                                                         | tableau des points formels (section 8.3)                                                                 |
| Vue par territoire Dankpen : « Mobile money : priorité moyenne » ; « Compétences : alphabétisation > 62 %, +20,9 points »                    | Dankpen est en priorité haute ; l'écart de 20,9 points est celui des Savanes ; Kara n'a pas de frein de capacité présumé                                                                                                                             | tableau refait (section 8.4)                                                                             |
| Vue par type d'action « Ouvrir une IMF » : 22 communes, 5 préfectures sans banque, 3 communes au maillage insuffisant, 8 préfectures sans fibre | mélange de quatre actions différentes (points formels, points mobile money, fibre)                                                                                                                                                                      | un type d'action par ligne (section 8.5)                                                                 |

---

## 11. Mise en œuvre technique

**État au 27/09/2026** (11 pages depuis le 28/09/2026) : les 10 pages sont construites, bilingues (français, anglais) et testées (chiffres clés comparés aux tables ; filtres par région, maille, priorité et milieu ; interactions propres à chaque page). Barre du haut et pied de page en place (section 3.3) ; sélecteur de langue fonctionnel. Lancement : `streamlit run dashboard/app.py`.

- **Page 1 (Synthèse nationale)** : nouveau titre, cartes lues comme des phrases (étiquette sur la ligne du titre, cartes d'une rangée à hauteur égale), bandeau discret « Ce que cette page ne montre pas ».
- **Page 2 bis (Marché des télécoms, 28/09/2026)** : `dashboard/views/marche.py`, 5 sous-onglets (fiche de la page 2 bis, section 7) ; l'onglet des technologies et le marché quittent la page 2. Corrections faites au passage : « sans fibre recensée » au lieu de « non raccordées » ; stock de sites radio dans le titre du graphique ; mention « qualité de service non mesurée par territoire » ; séparateur de milliers dans le tableau des préfectures sans fibre. Page 5 (Carte) : indicateurs de la fibre enterrée et aérienne.
- **Page 2 (Usage d'Internet)** : 6 sous-onglets depuis le 27/09/2026, 4 depuis le 28/09/2026 (Technologies et Marché partis sur la page 2 bis) (fiche de la page 2, section 7) ; seul l'onglet ouvert s'exécute ; l'onglet choisi est gardé au changement de langue. Ajouts du 28/09/2026 (contrôle croisé avec le 05, le 06 et le 08) : les classes de croissance qui dépendent de la période de référence sont marquées (cercle vide, pointillés), seules 2016 et 2021 étant sûres ; constat « accès et couverture ne vont pas ensemble » ; dépassement de l'Afrique subsaharienne depuis 2020.
- **Page 3 (Offre financière)** : carte par type de point avec sélecteur (DAB marqué « type à part »), carte mobile money, carte de la catégorie dominante d'opérateur par commune, offre et usage du mobile money par région (ajouté le 27/09/2026), tableau par préfecture.
- **Page 4 (Population et offre)** : seuil d'habitants par point formel déplaçable (bascule d'affichage, pas un recalcul de la table de référence), bascule de la variante P9, matrice statut × couverture, communes divergentes.
- **Page 5 (Carte)** : explorateur à un indicateur et une maille, avec la bonne table source par indicateur (score, o4, ou couverture).
- **Page 6 (Priorités)** : poids du score déplaçables (seule exception au « pas de recalcul », même formule que le 08), tests de robustesse, comparateur de deux préfectures. Ajout du 28/09/2026 : bandeau « Ce classement ne porte pas sur l'usage d'Internet » (08, sections 1 et 8.1), sous les chiffres clés.
- **Page 7 (Diagnostic)** : fiche des 10 préfectures prioritaires, carte des 25 communes signalées, usage d'Internet par région. Corrigé le 27/09/2026 : le frein présumé s'affichait tel qu'écrit dans la table (en français dans les deux langues, avec « la règle du 02 ») ; il passe par un libellé en clair, le même que sur la page 2.
- **Page 8 (Recommandations)** : 12 cartes filtrables par thème, nature et horizon ; vue d'ensemble sans addition de populations qui se recoupent ; ordre d'action, acteurs, ce qui n'est pas recommandé.
- **Page 9 (Estimations et projections)** : scénarios d'usage, trajectoires de référence, cibles à 1/3/5 ans ; correction apportée en le construisant : la population à faire entrer dans la couverture (R4b) ne compte que les 6 préfectures déjà prioritaires, pas Sotouboua (hors R4b, décision P24 du 10).
- **Page 10 (Méthodologie)** : les 27 indicateurs lus directement dans le tableau du 07 (jamais retapés), sources et millésimes, conventions, glossaire, crédits.

- **Outil** : Streamlit (installé : 1.61), graphiques Plotly, cartes Plotly ou Folium sur les contours du projet.
- **Organisation** : `dashboard/app.py` (point d'entrée, thème, menu `st.navigation` en groupes) ; les pages dans `dashboard/views/`, **jamais `pages/`** : ce dossier fait basculer Streamlit sur sa navigation héritée (piège vérifié au défi 1) ; `dashboard/donnees.py` lit les tables de `data/analysis/` avec cache, sans les recalculer.
- **Seule exception au « pas de recalcul »** : le score de priorité sous des poids choisis par le lecteur, avec la fonction du document de priorisation, et la bascule des seuils de classe (application d'un seuil à une valeur déjà calculée).
- **Composants partagés** : carte de chiffre clé, bandeau « Constat », bandeau « Synthèse chiffrée », bandeau « Limite », carte de recommandation, bouton d'export CSV ; depuis le 27/09/2026, barre de sous-onglets (`onglets()`, réutilisable sur les autres pages) et carte des 6 régions en classes fixes (`carte_regions()`) ; depuis le 28/09/2026, les aides des graphiques des pages d'analyse (`titre_bloc()`, `habiller()`, `tracer()`, `note()`, `pct()`, `BLEU_FONCE`), sorties de la page 2 pour servir aussi la page 2 bis.
- **Deux langues** (section 3.3), sur le modèle du défi 1 :
  - un module de dictionnaire (`dashboard/i18n.py`) : une clé par texte, deux valeurs (français, anglais) ;
  - une table de correspondance pour les libellés venus des tables (classes, statuts, régions) ;
  - une fonction de format des nombres selon la langue ;
  - la langue est gardée dans l'état de session, comme les filtres.
- **Étape ajoutée avant la page 8** (P38) : barre du haut, pied de page et dictionnaire. La page 1, écrite en français seulement, passe au dictionnaire à cette étape ; les pages suivantes sont écrites directement avec lui. Coût : chaque texte est écrit deux fois, et chaque test de page est lancé dans les deux langues.
- **Pièges Streamlit connus** (référentiel du défi 1) : `showSidebarNavigation = false` masque aussi le menu ; un tableau Streamlit n'affiche pas de HTML dans ses cellules ; les tests automatiques (`AppTest`) ne rejouent pas le point d'entrée lors d'un changement de page. Vus le 27/09/2026 : en 1.61, les onglets ne sont plus construits avec BaseWeb mais avec React Aria (le style vise `[role="tablist"]` et `[data-testid="stTab"]`) ; `AppTest` échoue sur une liste déroulante dont les libellés passent par `format_func` quand la page est rejouée (libellés directs à la place).
- **Contrôle** : un test automatique par page (la page s'ouvre, les chiffres clés égalent ceux des tables) ; vérification visuelle à chaque page terminée ; l'étape 13 de la procédure (validation) recoupe l'interface, les tables et les documents.

---

## 12. Points à valider

| #   | Question                                        | Proposition                                                                                                                                                                                                                                                                                                                                                             |
| --- | ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| P30 | Architecture                                    | Les 9 pages de la section 4, en 4 groupes de menu.**Validé (27/09/2026)**, puis 10 pages (P35)                                                                                                                                                                                                                                                                   |
| P31 | Interactions                                    | Les filtres globaux et les 7 paramètres de la section 6, dont les poids du score et le seuil de couverture.**Validé (27/09/2026)**                                                                                                                                                                                                                              |
| P32 | Libellés de priorité                          | « haute, moyenne, faible » pour les classes 1, 2, 3 du score, « priorité absolue » pour les 22 communes, « non classée » pour les 3 préfectures.**Validé (27/09/2026)**                                                                                                                                                                                 |
| P33 | Page Recommandations                            | Les 4 niveaux et les cartes corrigées de la section 8 ; aucune addition d'habitants entre recommandations.**Validé (27/09/2026)**                                                                                                                                                                                                                               |
| P34 | Ordre de construction                           | Gabarit et composants partagés, puis pages 1, 8, 6, 7 (le cœur décisionnel), puis 2, 3, 4, 5, 9.**Validé (27/09/2026)**, révisé avec P35 : pages 1, 8, 9, 6, 7, puis 2, 3, 4, 5, 10                                                                                                                                                                         |
| P35 | Page Estimations et projections                 | Dixième page, dans le groupe Pilotage ; le suivi des cibles et les scénarios quittent la page Recommandations.**Validé (27/09/2026)**                                                                                                                                                                                                                          |
| P36 | Chiffres de la page Estimations et projections  | Les corrections de la section 9.7 : coût de 1 Go à 3,9 % en 2030 ; pas de projection d'investissement à 2030 ; couverture datée de 2021/2022, extension en habitants ; Afrique subsaharienne à 44,2 %, calculée avec la même règle que le Togo. **Validé (27/09/2026)** |
| P37 | Barre du haut et pied de page repris du défi 1 | Nom « Togo Digital & Financial Inclusion » ; logo Togo AI Lab à télécharger depuis datalab.gouv.tg (absent du défi 1) ; attribution des armoiries sur la page Méthodologie ; sélecteur de langue repris, tableau de bord bilingue. **Validé (27/09/2026)**. Nom du ministère vérifié le même jour sur numerique.gouv.tg : « Ministère de l'Efficacité du Service Public et de la Transformation Numérique » (journal de recherche, section 19). La formulation « Ministère de l'Économie numérique » est écartée : c'est l'intitulé d'avant octobre 2025, pas un nom neutre |
| P38 | Mise en œuvre des deux langues | Dictionnaire unique et équivalents anglais fixés (section 3.3) ; étape ajoutée avant la page 8 : barre du haut, pied de page, dictionnaire, passage de la page 1 (section 11). Ordre de construction : pages 1 (faite), étape des deux langues, puis 8, 9, 6, 7, puis 2, 3, 4, 5, 10 |
