# Togo Digital & Financial Inclusion — Data Challenge, Économie numérique, Défi 2

Le mobile s'est imposé au Togo, mais moins de 4 personnes sur 10 utilisent Internet et les agences financières restent
concentrées dans les villes. Ce projet mesure l'adoption du numérique et le rôle du mobile money dans l'inclusion financière,
territoire par territoire, et en tire des recommandations chiffrées pour les territoires les moins bien servis.

Le livrable principal est un **tableau de bord Streamlit bilingue (français, anglais)** de 11 pages, construit sur des tables
déjà calculées : il restitue les analyses, il ne recalcule rien (seule exception : les poids du score de priorité, que le
lecteur peut déplacer, avec la même formule que le document de priorisation).

## Lancer le tableau de bord

```bash
pip install -r requirements-runtime.txt
streamlit run dashboard/app.py          # depuis la racine du dépôt
```

Ou dans un conteneur :

```bash
docker build -t togo-econum-defi2 .
docker run -p 8501:8501 togo-econum-defi2      # puis http://localhost:8501
```

## Les 11 pages

| Groupe | Page | Question |
| --- | --- | --- |
| Principal | Synthèse nationale | Le numérique et l'inclusion financière au Togo : où en est-on ? |
| Analyses | Usage d'Internet (objectif 1) | L'usage progresse-t-il, et à quel prix ? |
| | Marché des télécoms (objectif 2) | Qui tient le marché, et investit-il encore ? |
| | Offre financière (objectif 3) | Où sont les établissements financiers ? |
| | Population et offre (objectif 4) | Combien d'habitants par point, et où le mobile money est-il seul ? |
| | Carte | Que voit-on, commune par commune ? |
| Pilotage | Priorités (objectif 5) | Par quels territoires commencer ? |
| | Diagnostic | Pourquoi ces territoires ? |
| | Recommandations | Quelle action engager ? |
| | Estimations et projections | Où va le Togo si l'on agit, et si rien ne change ? |
| Méthodologie | Sources et méthode | Les données du défi, le rôle des sources externes, les 27 indicateurs, les conventions |

Chaque page d'analyse est découpée en sous-onglets (une vue synthèse, puis une vue par analyse), porte son constat et sa
limite, et suit les filtres de la barre latérale (région, maille commune ou préfecture, priorité, milieu).

## La démarche, document par document

| Document | Étape |
| --- | --- |
| `01_problem_definition.md` | le problème, les 5 objectifs, l'ordre de traitement |
| `02_decision_matrix.*` | la matrice de décision : indicateurs, règles de classe et seuils, fixés avant tout calcul |
| `03_data_understanding.md` | les 6 jeux de données du défi, leurs manques, les sources complémentaires |
| `04_data_Preparation.md` | la préparation : référentiel territorial, population, points de service, séries |
| `05_data_analysis.md` | l'exploration : offre, population, séries nationales, disparités, contradictions |
| `06_data_spatial_analysis.md` | l'analyse spatiale : cartes, voisinage, distances |
| `07_indicators.md` | les 27 indicateurs des objectifs 1 à 4, avec leurs classes et leurs limites |
| `08_prioritization.md` | le score de priorité des 39 préfectures, sa robustesse |
| `09_diagnostic.md` | le diagnostic des 10 préfectures prioritaires et des 25 communes signalées |
| `10_recommendations.md` | 12 recommandations chiffrées, leur ordre, leurs acteurs, le suivi des cibles |
| `Togo-Economie-Numerique-Defi2.pptx` | la présentation des résultats, pour le décideur |

## Organisation du dépôt

```
dashboard/          tableau de bord (app.py, pages dans views/, composants, dictionnaire des deux langues)
prep/               préparation des données (python prep/executer_tout.py) → data/interim/, data/processed/
analyse/            analyses et figures (p05 à p10, figures_*, cartes_06) → data/analysis/
data/processed/     tables préparées et contours administratifs (data/processed/geo/)
data/interim/       tables intermédiaires et journal de la préparation
data/analysis/      tables et figures des documents 05 à 10 — ce que le tableau de bord lit
tests/              test de fumée : 11 pages et tous leurs onglets, deux langues
scripts/            génération de la présentation, contrôle des dépendances, construction de l'archive
```

**Données brutes non incluses** (`data/raw/`, 491 Mo) : les jeux de données du défi et les sources complémentaires sont
publics, sauf les micro-données d'enquête de la Banque mondiale, obtenues sous conditions et non redistribuables. Leur liste
(URL, date, empreinte, objectifs servis) est dans `03_data_understanding.md`, section 12. Rejouer la préparation et les
analyses demande de les retélécharger ; le tableau de bord, lui, n'en a pas besoin.

## Vérifier

```bash
pip install -r requirements.txt
pytest                                  # depuis la racine du dépôt
```

Les tests affichent chaque page et chaque sous-onglet, en français et en anglais, et échouent si l'un d'eux lève une erreur,
si un sigle, un nom de source ou un code interne apparaît hors de la page Sources et méthode, ou si une table lue par le
tableau de bord manque.

## Licence

MIT (voir `LICENSE`). Armoiries de la République togolaise : restitution d'Edem Fiadjoe, Wikimedia Commons, CC BY-SA 4.0.
