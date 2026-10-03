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
#   • .env et .git/ — identifiants et historique ;
#   • tests/ — tests de fumée et de l'alerte de visite : ils servent à l'intégration continue,
#     pas au jury, qui ouvre le tableau de bord ;
#   • le rapport .pptx — il se dépose dans son propre champ du formulaire ; le mettre aussi dans
#     l'archive alourdissait d'autant l'envoi, qui porte les deux fichiers à la fois ;
#   • data/interim/ — étapes intermédiaires de prep/, qui ne se rejoue pas sans data/raw/ ;
#   • data/processed/geo/cantons.geojson et regions.geojson — lus par aucun code du tableau de
#     bord, des analyses ni des scripts.
#
# Figures des documents d'analyse (data/analysis/**/*.png) : ajoutées en palette de 256 couleurs,
# identiques à l'œil, trois fois plus légères (8,2 Mo → 2,9 Mo le 29/09/2026). Les originaux du
# dépôt ne sont pas modifiés ; `python3 analyse/figures_0X.py` et `analyse/cartes_06.py` les
# régénèrent à partir de ce que contient l'archive.
#
# Taille : la page de soumission annonce 20 Mo par fichier, mais le 29/09/2026 le support a jugé
# trop lourde une archive de 12,1 Mo. La limite réelle n'est pas connue (à confirmer auprès du
# support) : le script refuse toute archive de plus de 8 Mo, pour garder de la marge avec le
# rapport envoyé dans la même requête.
#
# Usage : bash scripts/make_submission.sh   (depuis n'importe où)

set -euo pipefail

ARCHIVE="Togo-Defi2-EconomieNumerique.zip"
TAILLE_MAX_OCTETS=$((8 * 1024 * 1024))
cd "$(dirname "$0")/.."

rm -f "$ARCHIVE"

# 1. Code, tables et documents — sans les figures PNG, ajoutées compressées à l'étape 2.
zip -r -q "$ARCHIVE" \
  README.md LICENSE \
  requirements.txt requirements-runtime.txt pyproject.toml \
  Dockerfile .dockerignore .streamlit \
  dashboard prep analyse scripts \
  data/processed data/analysis \
  01_problem_definition.md 02_decision_matrix.csv 02_decision_matrix_legende.csv \
  02_decision_matrix_seuils.csv 02_decision_matrix.xlsx \
  03_data_understanding.md 04_data_Preparation.md 05_data_analysis.md \
  06_data_spatial_analysis.md 07_indicators.md 08_prioritization.md \
  09_diagnostic.md 10_recommendations.md \
  -x '*/__pycache__/*' '*.pyc' '*/.pytest_cache/*' '*/.ruff_cache/*' '*/.DS_Store' \
     'data/analysis/*.png' 'data/processed/geo/cantons.geojson' 'data/processed/geo/regions.geojson'

# 2. Figures des documents d'analyse, en palette de 256 couleurs, aux mêmes chemins.
python3 - "$ARCHIVE" <<'PYTHON'
import io
import sys
import time
import zipfile
from pathlib import Path

from PIL import Image

with zipfile.ZipFile(sys.argv[1], "a", compression=zipfile.ZIP_DEFLATED) as archive:
    for chemin in sorted(Path("data/analysis").rglob("*.png")):
        image = Image.open(chemin)
        if image.mode in ("RGBA", "LA", "P"):
            image = image.convert("RGBA")
            fond = Image.new("RGB", image.size, "white")
            fond.paste(image, mask=image.getchannel("A"))
            image = fond
        image = image.convert("RGB").quantize(colors=256, method=Image.Quantize.MEDIANCUT,
                                              dither=Image.Dither.NONE)
        tampon = io.BytesIO()
        image.save(tampon, format="PNG", optimize=True)
        entree = zipfile.ZipInfo(chemin.as_posix(), date_time=time.localtime(chemin.stat().st_mtime)[:6])
        entree.external_attr = 0o644 << 16
        entree.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(entree, tampon.getvalue())
PYTHON

# Contrôle : l'archive ne doit contenir aucun des éléments écartés.
for motif in '^workspace/' '^11_plan' '^tmp/' '\.github/' '_PROJECT' '(^|/)\.env$' '^\.git/' '^data/raw/' \
             '^tests/' '\.pptx$' '^data/interim/' 'geo/(cantons|regions)\.geojson$'; do
  if unzip -Z1 "$ARCHIVE" | grep -qE "$motif"; then
    echo "ERREUR : l'archive contient « $motif »." >&2
    exit 1
  fi
done

# Contrôle : chaque figure du dépôt est bien dans l'archive (étape 2).
figures_depot=$(find data/analysis -name '*.png' | wc -l)
figures_archive=$(unzip -Z1 "$ARCHIVE" | grep -c '^data/analysis/.*\.png$' || true)
if [ "$figures_depot" -ne "$figures_archive" ]; then
  echo "ERREUR : $figures_archive figures dans l'archive, $figures_depot dans le dépôt." >&2
  exit 1
fi

taille=$(stat -c %s "$ARCHIVE")
if [ "$taille" -gt "$TAILLE_MAX_OCTETS" ]; then
  echo "ERREUR : l'archive pèse $(du -h "$ARCHIVE" | cut -f1), au-delà des 8 Mo retenus." >&2
  exit 1
fi

echo "$ARCHIVE — $(unzip -Z1 "$ARCHIVE" | wc -l) entrées, $(du -h "$ARCHIVE" | cut -f1)"
