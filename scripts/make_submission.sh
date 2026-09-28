#!/usr/bin/env bash
# Construit l'archive à soumettre au jury (même principe qu'au défi 1).
#
# ⚠️ **Liste blanche, pas liste noire.** Chaque élément à inclure est nommé explicitement :
# ce qui n'y figure pas ne peut pas se retrouver dans l'archive par oubli.
#
# Volontairement absents :
#   • data/raw/ (491 Mo) — les jeux de données d'origine et les sources complémentaires,
#     publiés sur leurs portails (liste, URL et empreintes : data/raw/_extradatas/_MANIFEST.csv,
#     documenté dans 03_data_understanding.md, section 12). Les micro-données d'enquête de la
#     Banque mondiale ne se redistribuent pas ;
#   • workspace/, 11_plan_visuel_dashboard.md — documents de travail personnels ;
#   • tmp/, .github/, _PROJECT.txt — notes internes, chaîne de déploiement, énoncé du défi ;
#   • .env et .git/ — identifiants et historique.
#
# Taille maximale de l'archive : 20 Mo (contrainte de soumission). Le script échoue au-delà.
#
# Usage : bash scripts/make_submission.sh   (depuis n'importe où)

set -euo pipefail

ARCHIVE="Togo-Defi2-EconomieNumerique.zip"
TAILLE_MAX_OCTETS=$((20 * 1024 * 1024))
cd "$(dirname "$0")/.."

rm -f "$ARCHIVE"

zip -r -q "$ARCHIVE" \
  README.md LICENSE \
  requirements.txt requirements-runtime.txt pyproject.toml \
  Dockerfile .dockerignore .streamlit \
  dashboard prep analyse tests scripts \
  data/processed data/interim data/analysis \
  01_problem_definition.md 02_decision_matrix.csv 02_decision_matrix_legende.csv \
  02_decision_matrix_seuils.csv 02_decision_matrix.xlsx \
  03_data_understanding.md 04_data_Preparation.md 05_data_analysis.md \
  06_data_spatial_analysis.md 07_indicators.md 08_prioritization.md \
  09_diagnostic.md 10_recommendations.md \
  Togo-Economie-Numerique-Defi2.pptx \
  -x '*/__pycache__/*' '*.pyc' '*/.pytest_cache/*' '*/.ruff_cache/*' '*/.DS_Store'

# Contrôle : l'archive ne doit contenir aucun des éléments écartés.
for motif in '^workspace/' '^11_plan' '^tmp/' '\.github/' '_PROJECT' '(^|/)\.env$' '^\.git/' '^data/raw/'; do
  if unzip -Z1 "$ARCHIVE" | grep -qE "$motif"; then
    echo "ERREUR : l'archive contient « $motif »." >&2
    exit 1
  fi
done

taille=$(stat -c %s "$ARCHIVE")
if [ "$taille" -gt "$TAILLE_MAX_OCTETS" ]; then
  echo "ERREUR : l'archive pèse $(du -h "$ARCHIVE" | cut -f1), au-delà des 20 Mo autorisés." >&2
  exit 1
fi

echo "$ARCHIVE — $(unzip -Z1 "$ARCHIVE" | wc -l) entrées, $(du -h "$ARCHIVE" | cut -f1)"
