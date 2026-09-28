"""Exécute les 9 étapes de préparation dans l'ordre (04_data_Preparation.md, section 1).

Usage : python3 prep/executer_tout.py
Un contrôle bloquant en échec arrête la chaîne à l'étape concernée.
"""
import subprocess
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
ETAPES = ["p01_referentiel", "p02_population", "p03_points", "p04_territoires", "p05_ar1", "p06_series",
          "p07_enquetes", "p08_references", "p09_controles"]

for e in ETAPES:
    print(f"\n######## {e}")
    r = subprocess.run([sys.executable, str(ICI / f"{e}.py")], cwd=ICI)
    if r.returncode != 0:
        sys.exit(f"Arrêt : l'étape {e} a échoué (code {r.returncode}).")
print("\nPréparation terminée : tables dans data/processed/, registre et journal consolidés.")
