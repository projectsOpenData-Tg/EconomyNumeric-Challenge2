"""Étape 8 — Repères externes et chronologie (04, section 6) → data/processed/benchmark.csv, chronologie.csv.

Repères repris tels que publiés, sans moyenne ni médiane (calculées à l'étape des indicateurs, décisions S2 à S4) :
C5 (FAS, 8 pays de l'UEMOA), C5b (usage d'Internet, Afrique subsaharienne et UEMOA), IT1 (paniers data mobile,
pays de l'UEMOA), BC2 (TGPSFd et TGPSFg de la BCEAO : repère de la variante « tous points de service », R1).
"""
import re
import subprocess

import pandas as pd

from commun import EXTRA, PROCESSED, Etape, ecrire_csv

ET = Etape(8, "references")
UEMOA = {"BEN": "Bénin", "BFA": "Burkina Faso", "CIV": "Côte d'Ivoire", "GNB": "Guinée-Bissau", "MLI": "Mali",
         "NER": "Niger", "SEN": "Sénégal", "TGO": "Togo"}
L: list[dict] = []


def ajouter(source, iso3, pays, annee, indicateur, valeur, unite, niveau="C", note=""):
    if pd.notna(valeur):
        L.append(dict(source=source, iso3=iso3, pays=pays, annee=int(annee), indicateur=indicateur,
                      valeur=float(valeur), unite=unite, niveau_preuve=niveau, note=note))


# C5 : agences et DAB pour 100 000 adultes (O4-02, décisions R1, S2 à S4)
c5 = pd.read_csv(EXTRA / "obj4" / "C5_worldbank-fas-uemoa_agences-dab-100000-adultes.csv")
for _, r in c5.iterrows():
    ajouter("C5 (FAS, Banque mondiale)", r.iso3, UEMOA.get(r.iso3, r.pays), r.annee, r.code, r.valeur,
            "pour 100 000 adultes", note=r.indicateur + " ; appareils (A19)" if "ATM" in r.code else r.indicateur)
ET.controle("C5", "pays de C5", 8, c5.iso3.nunique(), c5.iso3.nunique() == 8)

# C5b : usage d'Internet, Afrique subsaharienne (agrégat) et UEMOA (O1-01, décision S1)
c5b = pd.read_csv(EXTRA / "obj1" / "C5b_worldbank-uit-internet-afrique-subsaharienne-uemoa.csv")
for _, r in c5b.iterrows():
    ajouter("C5b (UIT, Banque mondiale)", r.iso3, r.pays, r.annee, "usage_internet_pct_population", r.valeur,
            "% de la population", note="estimations UIT" + (f" ; {r.note_source}" if isinstance(r.note_source, str) else ""))
tg_ssa = c5b[(c5b.iso3 == "SSF") & (c5b.annee == 2024)].valeur
ET.controle("C5b", "Afrique subsaharienne 2024 (03 : 33,6 %)", 33.6, tg_ssa.iloc[0] if len(tg_ssa) else "absent",
            len(tg_ssa) == 1 and round(tg_ssa.iloc[0], 1) == 33.6, bloquant=False)

# IT1 : paniers data mobile en % du RNB mensuel, pays de l'UEMOA (repère de O2-05b)
it1 = pd.read_excel(EXTRA / "obj2" / "IT1_uit_paniers-prix-tic_2008-2025.xlsx", sheet_name="economies_2008-2025")
sel = it1[it1.IsoCode.isin(UEMOA) & (it1.Unit == "GNIpc") & it1.Code.isin(["i271mb_1GB_GNI", "i271mb_2GB_GNI"])]
for _, r in sel.iterrows():
    for an in [c for c in it1.columns if isinstance(c, int)]:
        ajouter("IT1 (UIT)", r.IsoCode, UEMOA[r.IsoCode], an, r.Code, r[an], "% du RNB mensuel par habitant",
                note=r["Basket name"])

# BC2 : TGPSFd (points pour 10 000 adultes) et TGPSFg (points pour 1 000 km²), 2014-2024, lus dans le PDF
txt = subprocess.run(["pdftotext", "-layout", str(EXTRA / "obj4" / "BC2_bceao_tableau-de-bord-inclusion-financiere-uemoa-2024.pdf"),
                      "-"], capture_output=True, text=True, check=True).stdout.splitlines()
debut = next(i for i, l in enumerate(txt) if "1.1- Taux global de pénétration démographique" in l)
fin = next(i for i, l in enumerate(txt) if i > debut and l.strip().startswith("1.2-"))
rx = re.compile(r"^\s*(\D+?)\s+((?:\d+\s+){10}\d+)\s+(\D+?)\s+((?:\d+\s+){10}\d+)\s*$")
lus = 0
for l in txt[debut:fin]:
    m = rx.match(l)
    if not m:
        continue
    nom = m.group(1).strip()
    iso = {v: k for k, v in UEMOA.items()}.get(nom, {"Burkina": "BFA", "UEMOA": "UEMOA"}.get(nom))
    if iso is None:
        continue
    for code, vals, unite in (("TGPSFd", m.group(2), "points de service pour 10 000 adultes"),
                              ("TGPSFg", m.group(4), "points de service pour 1 000 km²")):
        for an, v in zip(range(2014, 2025), vals.split()):
            ajouter("BC2 (BCEAO, tableau de bord 2024)", iso, UEMOA.get(iso, "UEMOA"), an, code, v, unite,
                    note="mobile money compris (≈ 98-99 % des points) : repère de la variante « tous points de service » "
                         "seulement, jamais de O4-02 (R1)")
    lus += 1
ET.controle("BC2", "lignes pays de BC2 lues (8 pays + UEMOA)", 9, lus, lus == 9, bloquant=False)
tg = [x for x in L if x["source"].startswith("BC2") and x["iso3"] == "TGO" and x["annee"] == 2024]
ET.controle("BC2-Togo", "Togo 2024 : TGPSFd / TGPSFg (03 : 116 / 1 094)", "116 / 1094",
            " / ".join(str(int(x["valeur"])) for x in tg), [int(x["valeur"]) for x in tg] == [116, 1094], bloquant=False)

bm = pd.DataFrame(L)
ET.sortie(ecrire_csv(bm, PROCESSED / "benchmark.csv"))
ET.effectif("benchmark", "C5, C5b, IT1, BC2", "tels que publiés", f"{len(bm)} lignes")

# Chronologie (CH1) : reprise telle quelle, contrôlée
ch = pd.read_csv(EXTRA / "obj1" / "CH1_chronologie-evenements.csv")
ET.controle("CH1", "événements datés, avec source et niveau de preuve", 40,
            f"{len(ch)} ({ch.source.notna().sum()} sources, {ch.niveau_preuve.notna().sum()} niveaux)",
            len(ch) == 40 and ch.source.notna().all() and ch.niveau_preuve.notna().all())
ET.sortie(ecrire_csv(ch, PROCESSED / "chronologie.csv"))
ET.fin()
