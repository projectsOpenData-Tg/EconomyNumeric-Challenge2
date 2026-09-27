"""Extraction des tableaux trimestriels des observatoires de l'ARCEP (AR1), par la position des mots.

Chaque tableau a un en-tête de trimestres (« 2025 T2 », « 2019T3 »…). Chaque nombre est rattaché à la
colonne du trimestre la plus proche ; les fragments de libellé coupés au-dessus ou au-dessous d'une ligne
de chiffres sont rattachés à la ligne de chiffres la plus proche verticalement.
Les graphiques ne sont pas lus : seules les lignes situées sous un en-tête de trimestres le sont.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import fitz  # PyMuPDF

RE_ANNEE = re.compile(r"^(20[12]\d)$")
RE_TRIM = re.compile(r"^T([1-4])$")
RE_ANNEE_TRIM = re.compile(r"^(20[12]\d)T([1-4])$")
RE_NOMBRE = re.compile(r"^-?\d+(?:,\d+)?$")
RE_VIDE = re.compile(r"^(?:-|ND|nd|N/D)$")
MOTS_EXCLUS = ("Graphique", "Variation", "©", "OBSERVATOIRE", "Source")


@dataclass
class Mot:
    x0: float
    y0: float
    x1: float
    y1: float
    t: str

    @property
    def xc(self) -> float:
        return (self.x0 + self.x1) / 2

    @property
    def yc(self) -> float:
        return (self.y0 + self.y1) / 2


def lignes_de_la_page(page) -> list[list[Mot]]:
    mots = [Mot(w[0], w[1], w[2], w[3], w[4]) for w in page.get_text("words")]
    mots.sort(key=lambda m: (round(m.yc, 0), m.x0))
    lignes: list[list[Mot]] = []
    for m in sorted(mots, key=lambda m: m.yc):
        if lignes and abs(lignes[-1][0].yc - m.yc) <= 2.5:
            lignes[-1].append(m)
        else:
            lignes.append([m])
    return [sorted(l, key=lambda m: m.x0) for l in lignes]


def trimestres_entete(lignes, i) -> list[tuple[str, float, float]] | None:
    """Trimestres (libellé, centre x, bord droit) lus sur la ligne i, complétée par la suivante si l'en-tête est coupé."""
    suite = i + 1 < len(lignes) and abs(lignes[i + 1][0].yc - lignes[i][0].yc) < 14
    bande = list(lignes[i]) + (list(lignes[i + 1]) if suite else [])
    trims = []
    for k, m in enumerate(bande):
        if "/" in m.t:
            continue
        a = RE_ANNEE_TRIM.match(m.t)
        if a:
            trims.append((f"{a.group(1)}T{a.group(2)}", m.xc, m.x1, m.yc))
            continue
        a = RE_ANNEE.match(m.t)
        if a:
            # T associé : sur la même ligne juste à droite, ou juste en dessous (en-tête coupé)
            cands = [n for n in bande if RE_TRIM.match(n.t) and (
                (abs(n.yc - m.yc) < 2.5 and 0 <= n.x0 - m.x1 < 12) or (0 < n.yc - m.yc < 14 and abs(n.xc - m.xc) < 25))]
            if cands:
                n = min(cands, key=lambda n: abs(n.x0 - m.x1) + abs(n.yc - m.yc))
                if not any("/" in o.t for o in bande if abs(o.yc - n.yc) < 2.5 and 0 <= o.x0 - n.x1 < 3):
                    trims.append((f"{a.group(1)}T{RE_TRIM.match(n.t).group(1)}", (m.x0 + n.x1) / 2 if n.yc - m.yc < 2.5 else m.xc,
                                  max(m.x1, n.x1), m.yc))
    if len(trims) < 3:
        return None
    trims.sort(key=lambda t: t[1])
    # plus longue suite de trimestres consécutifs, de gauche à droite
    def rang(q):
        return int(q[:4]) * 4 + int(q[-1])
    meilleure, courante = [], [trims[0]]
    for t in trims[1:]:
        if rang(t[0]) == rang(courante[-1][0]) + 1:
            courante.append(t)
        else:
            meilleure = max(meilleure, courante, key=len)
            courante = [t]
    meilleure = max(meilleure, courante, key=len)
    if len(meilleure) < 3:
        return None
    y_t = [y for _, _, _, y in meilleure]
    fin = i + 1 if suite and any(abs(lignes[i + 1][0].yc - y) < 2.5 for y in y_t) else i
    return [(q, xc, x1) for q, xc, x1, _ in meilleure], fin


def valeur(texte: str):
    if RE_VIDE.match(texte):
        return None
    return float(texte.replace(" ", "").replace(",", "."))


def extraire_pdf(chemin: Path) -> list[dict]:
    numero = re.search(r"AR1_(\d{4}T\d)", chemin.name).group(1)
    doc = fitz.open(chemin)
    sortie = []
    for p, page in enumerate(doc, start=1):
        lignes = lignes_de_la_page(page)
        titre_page = next((" ".join(m.t for m in l) for l in lignes[:6]
                           if not any(x in " ".join(m.t for m in l) for x in MOTS_EXCLUS) and len(l) <= 8), "")
        i = 0
        while i < len(lignes):
            res = trimestres_entete(lignes, i)
            if not res:
                i += 1
                continue
            cols, i_fin = res
            # Texte libre de l'en-tête (ex. « Comptes de mobile money », « (en milliards de Fcfa) »)
            x_debut = cols[0][1] - 40
            entete_txt = " ".join(m.t for k in range(max(0, i - 1), min(len(lignes), i_fin + 2))
                                  for m in lignes[k] if abs(lignes[k][0].yc - lignes[i_fin][0].yc) < 12
                                  and m.x1 < x_debut and not re.search(r"\d", m.t) and m.t != "Variation")
            # Contexte : titre du tableau (ligne « Tableau … » ou titre de section) au-dessus de l'en-tête
            contexte = ""
            for l in reversed(lignes[max(0, i - 6):i]):
                txt = " ".join(m.t for m in l)
                if txt.startswith("Tableau") or (len(l) <= 6 and not any(c.isdigit() for c in txt)
                                                 and not any(x in txt for x in MOTS_EXCLUS)):
                    contexte = txt
                    break
            y_entete = max(m.yc for m in lignes[i_fin])
            xs = [c[1] for c in cols]
            ecart = min(b - a for a, b in zip(xs, xs[1:])) if len(xs) > 1 else 60
            x_min_col = xs[0] - 0.6 * ecart
            x_max_col = xs[-1] + 0.6 * ecart
            j = i_fin + 1
            rangs, textes = [], []
            while j < len(lignes):
                if trimestres_entete(lignes, j):
                    break
                l = lignes[j]
                txt = " ".join(m.t for m in l)
                if txt.startswith(("Tableau", "Graphique")) or l[0].yc - y_entete > 400:
                    break
                if abs(l[0].yc - y_entete) < 14 and ("Variation" in txt or "/" in txt):
                    j += 1
                    continue
                nums = [m for m in l if (RE_NOMBRE.match(m.t) or RE_VIDE.match(m.t)) and x_min_col <= m.xc <= x_max_col]
                intercales = nums and any(not (RE_NOMBRE.match(m.t) or RE_VIDE.match(m.t) or m.t.endswith("%"))
                                          and m.x0 > min(n.x0 for n in nums) and m.xc <= x_max_col for m in l)
                if nums and not intercales:
                    texte = [m for m in l if m.x1 < min(n.x0 for n in nums) and not RE_NOMBRE.match(m.t)]
                    par_col: dict[int, list[Mot]] = {}
                    for n in nums:
                        k = min(range(len(cols)), key=lambda k: abs(cols[k][1] - n.xc))
                        par_col.setdefault(k, []).append(n)
                    rangs.append(dict(y=l[0].yc, texte=texte, cols=par_col))
                elif not any(x in txt for x in MOTS_EXCLUS):
                    textes.append((l[0].yc, txt))
                j += 1
            # Fragments de libellé rattachés à la ligne de chiffres la plus proche (|dy| <= 11)
            for yt, txt in textes:
                if not rangs:
                    break
                r = min(rangs, key=lambda r: abs(r["y"] - yt))
                if abs(r["y"] - yt) <= 11:
                    r.setdefault("frag", []).append((yt, txt))
            for r in rangs:
                morceaux = [(r["y"], " ".join(m.t for m in r["texte"]))] + r.get("frag", [])
                libelle = " ".join(t for _, t in sorted(morceaux) if t).strip()
                if not r["texte"] and (len(r["cols"]) < 3 or not libelle):
                    continue  # étiquettes de graphique : pas de libellé sur la ligne, ou moins de 3 colonnes
                for k, toks in r["cols"].items():
                    brut = " ".join(t.t for t in sorted(toks, key=lambda t: t.x0))
                    try:
                        v = valeur(brut)
                        note = ""
                    except ValueError:
                        v, note = None, "illisible"
                    # appel de note collé (ex. « 13 5201 ») : un groupe de milliers de 4 chiffres
                    groupes = brut.split(" ")
                    if len(groupes) > 1 and len(groupes[-1].split(",")[0]) == 4:
                        brut_corr = " ".join(groupes[:-1] + [groupes[-1][:3]])
                        v, note = valeur(brut_corr), f"appel de note retiré ({brut})"
                    sortie.append(dict(numero=numero, page=p, titre_page=titre_page, contexte=contexte, entete=entete_txt,
                                       libelle=libelle, trimestre=cols[k][0], valeur_brute=brut, valeur=v, note=note))
            i = j
    return sortie
