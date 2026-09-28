#!/usr/bin/env python3
"""Vérifie que requirements-runtime.txt ne diverge pas de requirements.txt.

Le déploiement installe `requirements-runtime.txt` — un sous-ensemble des dépendances du
projet, restreint à ce que le tableau de bord importe réellement. Deux fichiers de versions
valent deux occasions de se tromper : monter pandas d'un côté seulement, et la production
ne tourne plus sur les versions avec lesquelles les scripts `prep/` et `analyse/` ont
produit les tables que le tableau de bord lit.

Ce script est la contrepartie du découpage. Il impose deux règles :

  1. tout paquet de requirements-runtime.txt figure aussi dans requirements.txt ;
  2. les deux fichiers lui donnent exactement le même spécificateur de version.

L'inverse n'est pas vérifié : requirements.txt contient légitimement des paquets absents du
runtime — PyMuPDF, openpyxl et pyreadstat ne servent qu'à la préparation (`prep/`),
matplotlib et scipy qu'aux figures et aux analyses (`analyse/`), pytest et ruff qu'à la CI.

    python scripts/check_requirements_sync.py     # 0 si tout concorde, 1 sinon
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJET = ROOT / "requirements.txt"
RUNTIME = ROOT / "requirements-runtime.txt"

# Bornes des noms de paquets dans une ligne d'exigence. `==` en tête : c'est la forme
# utilisée par le dépôt, et la seule qui garantisse la reproductibilité revendiquée.
SEPARATEURS = ("==", ">=", "<=", "~=", "!=", ">", "<")


def lire(chemin):
    """Retourne {nom_normalisé: (spécificateur, numéro de ligne)} pour un fichier pip.

    Les commentaires et les lignes vides sont ignorés. Les deux fichiers du dépôt sont de
    simples listes épinglées — ni `-r`, ni extras, ni marqueurs d'environnement — donc on
    ne cherche pas à réimplémenter la grammaire complète de PEP 508 : on signale ce qu'on
    ne sait pas lire plutôt que de le laisser passer en silence.
    """
    paquets = {}
    for numero, brut in enumerate(chemin.read_text(encoding="utf-8").splitlines(), start=1):
        ligne = brut.split("#", 1)[0].strip()
        if not ligne:
            continue
        for sep in SEPARATEURS:
            if sep in ligne:
                nom, version = ligne.split(sep, 1)
                paquets[normaliser(nom)] = (f"{sep}{version.strip()}", numero)
                break
        else:
            # Dépendance sans version : refusée, elle contourne l'épinglage.
            paquets[normaliser(ligne)] = (None, numero)
    return paquets


def normaliser(nom):
    """PEP 503 : `python-pptx`, `python_pptx` et `Python.PPTX` désignent le même paquet."""
    return nom.strip().lower().replace("_", "-").replace(".", "-")


def main():
    for chemin in (PROJET, RUNTIME):
        if not chemin.exists():
            print(f"ERREUR : {chemin.relative_to(ROOT)} est introuvable.")
            return 1

    projet = lire(PROJET)
    runtime = lire(RUNTIME)
    problemes = []

    for nom, (version_runtime, ligne_runtime) in sorted(runtime.items()):
        origine = f"requirements-runtime.txt:{ligne_runtime}"

        if version_runtime is None:
            problemes.append(f"{origine} — « {nom} » n'est pas épinglé (attendu : ==x.y.z).")
            continue

        if nom not in projet:
            problemes.append(
                f"{origine} — « {nom} » est absent de requirements.txt. Le runtime ne peut "
                f"pas dépendre d'un paquet que le projet ne déclare pas : ajoutez-le à "
                f"requirements.txt, ou retirez-le du runtime."
            )
            continue

        version_pipeline, ligne_pipeline = projet[nom]
        if version_runtime != version_pipeline:
            problemes.append(
                f"{origine} — « {nom} » diverge : {version_runtime} ici, "
                f"{version_pipeline} en requirements.txt:{ligne_pipeline}. "
                f"Alignez les deux sur la version avec laquelle le projet a été vérifié."
            )

    if problemes:
        print(f"Désynchronisation des dépendances — {len(problemes)} problème(s) :\n")
        for probleme in problemes:
            print(f"  • {probleme}")
        print(
            "\nLes deux fichiers doivent rester alignés : la production tourne sur "
            "requirements-runtime.txt, mais les chiffres du dépôt ont été produits avec "
            "requirements.txt."
        )
        return 1

    print(
        f"Dépendances synchronisées : les {len(runtime)} paquets du runtime portent le même "
        f"pin qu'en requirements.txt."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
