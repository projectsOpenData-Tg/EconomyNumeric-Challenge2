"""Étape 9 — Contrôles transversaux, registre des anomalies et journal (04, sections 7 et 8).

Sorties : data/processed/_registre_anomalies.csv, _controles.csv, _journal_preparation.csv.
"""
import json

import pandas as pd

from commun import JOURNAL_DIR, PROCESSED, REGISTRE_DIR, Etape, ecrire_csv

ET = Etape(9, "controles")
TABLES = ["dim_territoire", "points_service", "terr_commune", "terr_prefecture", "terr_region", "serie_nationale",
          "enquetes_region", "benchmark", "chronologie"]
t = {n: pd.read_csv(PROCESSED / f"{n}.csv", low_memory=False) for n in TABLES}
for n, df in t.items():
    ET.controle("OUT", f"table {n} présente et non vide", "> 0 ligne", len(df), len(df) > 0)

# Codes : tout code utilisé existe dans le référentiel
dim = t["dim_territoire"]
codes = set(dim.code.astype(str))
pts = t["points_service"]
for col in ("canton_code", "commune_code", "prefecture_code"):
    manq = (~pts[col].astype(str).isin(codes)).sum()
    ET.controle("GE2-codes", f"points_service.{col} présents dans dim_territoire", 0, manq, manq == 0)
for n in ("terr_commune", "terr_prefecture", "terr_region"):
    manq = (~t[n].code.astype(str).isin(codes)).sum()
    ET.controle("GE1-codes", f"{n} : codes présents dans dim_territoire", 0, manq, manq == 0)

# ST3 : aucun 0 issu d'un manquant
d5 = pts[pts.source == "D5"]
ET.controle("ST3-op", "D5 : opérateur non renseigné resté NA (jamais 0)", 1348,
            int(d5.op_moov.isna().sum()), int(d5.op_moov.isna().sum()) == 1348 and int(d5.op_togocom.isna().sum()) == 1348)
for n in ("terr_commune", "terr_prefecture"):
    df = t[n]
    nd = df[df.couv_20km_motif == "non_determinable"]
    ET.controle("ST3-couv", f"{n} : couverture non déterminable laissée en NA", "NA partout", nd.couv_20km_pct.isna().all(),
                nd.couv_20km_pct.isna().all())
    zeros = df[(df.n_formels == 0)]
    ET.controle("A13-zero", f"{n} : les zéros de points formels ont une enquête prouvée", "tous",
                bool((zeros.enquete_prouvee == 1).all()), (zeros.enquete_prouvee == 1).all())

# TE1 et TE4 : millésimes
ET.controle("TE1", "croisement points (PRISE 2021/2022) × population (RGPH 2022)", "écart ≤ 1 an",
            f"{t['terr_commune'].millesime_points.unique().tolist()} × {t['terr_commune'].source_population.unique().tolist()}",
            t["terr_commune"].millesime_points.eq("2021/2022 (PRISE)").all())
ET.controle("TE4", "D5 libellé comme stock 2021/2022", "tous", d5.millesime.unique().tolist(),
            d5.millesime.eq("2021/2022 (campagne PRISE)").all())

# Niveau de preuve renseigné partout où la table le porte
for n, col in (("points_service", "niveau_preuve"), ("serie_nationale", "niveau_preuve"),
               ("enquetes_region", "niveau_preuve"), ("benchmark", "niveau_preuve"), ("chronologie", "niveau_preuve")):
    ET.controle("PREUVE", f"{n} : niveau de preuve renseigné", "100 %", f"{100 * t[n][col].notna().mean():.0f} %",
                t[n][col].notna().all())

# Registre, contrôles et journal consolidés
reg = pd.concat([pd.read_csv(f) for f in sorted(REGISTRE_DIR.glob("*.csv")) if f.stat().st_size > 0], ignore_index=True)
reg.insert(0, "id", [f"AN{i:05d}" for i in range(1, len(reg) + 1)])
journaux = [json.loads(f.read_text()) for f in sorted(JOURNAL_DIR.glob("*.json")) if not f.name.startswith("09_")]
ctrl = pd.DataFrame([dict(etape=j["etape"], **c) for j in journaux for c in j["controles"]] +
                    [dict(etape="09_controles", **c) for c in ET.controles])
jr = pd.DataFrame([dict(etape=j["etape"], date=j["date"], n_controles=len(j["controles"]),
                        n_ecarts=sum(c["resultat"] != "OK" for c in j["controles"]),
                        n_echecs_bloquants=sum(c["resultat"] != "OK" and c["bloquant"] for c in j["controles"]),
                        n_anomalies=j["n_anomalies"],
                        effectifs=" | ".join(f"{e['objet']} : {e['avant']} → {e['transformation']} → {e['apres']}"
                                             for e in j["effectifs"]),
                        sorties=", ".join(j["sorties"])) for j in journaux])
bloquants = int(jr.n_echecs_bloquants.sum())
ET.controle("BLOQUANTS", "aucun contrôle bloquant en échec sur les étapes 1 à 8", 0, bloquants, bloquants == 0)
ET.sortie(ecrire_csv(reg, PROCESSED / "_registre_anomalies.csv"))
ET.sortie(ecrire_csv(ctrl, PROCESSED / "_controles.csv"))
ET.sortie(ecrire_csv(jr, PROCESSED / "_journal_preparation.csv"))
ET.effectif("registre", "9 étapes", "consolidation", f"{len(reg)} lignes")
ET.effectif("contrôles", "9 étapes", "consolidation", f"{len(ctrl)} contrôles, {int((ctrl.resultat != 'OK').sum())} écarts signalés")
ET.fin()
