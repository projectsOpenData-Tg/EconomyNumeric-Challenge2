"""Outils communs aux scripts de préparation (04_data_Preparation.md).

Chemins, normalisation des noms pour les jointures, registre des anomalies,
journal d'étape et contrôles. Les fichiers de data/raw/ ne sont jamais écrits.
"""
from __future__ import annotations

import json
import re
import unicodedata
from datetime import date
from pathlib import Path

import pandas as pd

RACINE = Path(__file__).resolve().parents[1]
RAW = RACINE / "data" / "raw"
EXTRA = RAW / "_extradatas"
INTERIM = RACINE / "data" / "interim"
PROCESSED = RACINE / "data" / "processed"
GEO = PROCESSED / "geo"
REGISTRE_DIR = INTERIM / "registre"
JOURNAL_DIR = INTERIM / "journal"

for _d in (INTERIM, PROCESSED, GEO, REGISTRE_DIR, JOURNAL_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# Projection à surfaces égales pour les superficies (Lambert azimutale centrée sur le Togo).
CRS_SURFACE = "+proj=laea +lat_0=8.6 +lon_0=0.9 +datum=WGS84 +units=m +no_defs"

# Unités régionales (A12) : le Grand Lomé = préfectures Golfe (A04) et Agoè-Nyivé (A01).
PREFECTURES_GRAND_LOME = ("A01", "A04")


def norm(texte) -> str:
    """Forme de jointure : majuscules, sans accents, ponctuation et espaces unifiés."""
    if texte is None or (isinstance(texte, float) and pd.isna(texte)):
        return ""
    t = unicodedata.normalize("NFKD", str(texte)).encode("ascii", "ignore").decode()
    t = re.sub(r"[^A-Za-z0-9]+", " ", t).upper()
    return " ".join(t.split())


def ecrire_csv(df: pd.DataFrame, chemin: Path) -> Path:
    chemin.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(chemin, index=False, encoding="utf-8")
    return chemin


class Etape:
    """Journal, registre et contrôles d'une étape de préparation.

    - `controle` enregistre un contrôle ; un contrôle bloquant qui échoue arrête l'étape.
    - `anomalie` ajoute une ligne au registre des anomalies et exclusions.
    - `effectif` trace les effectifs (avant → transformation → après).
    """

    def __init__(self, numero: int, nom: str):
        self.numero, self.nom = numero, nom
        self.controles: list[dict] = []
        self.anomalies: list[dict] = []
        self.effectifs: list[dict] = []
        self.sorties: list[str] = []

    def effectif(self, objet: str, avant, transformation: str, apres) -> None:
        self.effectifs.append(dict(objet=objet, avant=avant, transformation=transformation, apres=apres))
        print(f"  [effectif] {objet} : {avant} → {transformation} → {apres}")

    def controle(self, code: str, libelle: str, attendu, constate, ok: bool, bloquant: bool = True) -> bool:
        self.controles.append(dict(code=code, libelle=libelle, attendu=str(attendu), constate=str(constate),
                                   resultat="OK" if ok else "ÉCHEC", bloquant=bloquant))
        etat = "OK " if ok else ("ÉCHEC BLOQUANT" if bloquant else "écart signalé")
        print(f"  [{code}] {etat} : {libelle} | attendu {attendu} | constaté {constate}")
        if bloquant and not ok:
            self.fin()
            raise SystemExit(f"Contrôle bloquant {code} en échec : {libelle}")
        return ok

    def anomalie(self, jeu: str, id_source, variable: str, type_: str, decision: str, regle: str,
                 effet: str, detail: str = "") -> None:
        self.anomalies.append(dict(jeu=jeu, id_source=id_source, variable=variable, type=type_,
                                   decision=decision, regle=regle, effet=effet, detail=detail,
                                   etape=f"{self.numero:02d}_{self.nom}"))

    def sortie(self, chemin: Path) -> None:
        self.sorties.append(str(chemin.relative_to(RACINE)))

    def fin(self) -> None:
        tag = f"{self.numero:02d}_{self.nom}"
        reg = pd.DataFrame(self.anomalies, columns=["jeu", "id_source", "variable", "type", "decision",
                                                    "regle", "effet", "detail", "etape"])
        reg.to_csv(REGISTRE_DIR / f"{tag}.csv", index=False, encoding="utf-8")
        journal = dict(etape=tag, date=date.today().isoformat(), effectifs=self.effectifs,
                       controles=self.controles, sorties=self.sorties, n_anomalies=len(self.anomalies))
        (JOURNAL_DIR / f"{tag}.json").write_text(json.dumps(journal, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        n_ko = sum(c["resultat"] != "OK" for c in self.controles)
        print(f"== Étape {tag} : {len(self.controles)} contrôles ({n_ko} écart(s)), "
              f"{len(self.anomalies)} ligne(s) au registre, {len(self.sorties)} sortie(s)")
