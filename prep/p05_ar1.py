"""Étape 5 — Extraction des observatoires trimestriels de l'ARCEP (AR1 ; 04, SN2 et DD5 ; décisions P4, P5, S6, A2).

Entrées : 34 PDF (T1 2018 à T2 2026, 3 mises en page).
Sorties : data/interim/ar1_brut.csv (toutes les lignes lues, toutes publications) ;
          data/interim/ar1_toutes_publications.csv (lignes reconnues, toutes publications) ;
          data/interim/ar1_trimestriel.csv (une valeur par série et par trimestre : la publication la plus récente).
Seuls les tableaux sont lus ; les graphiques ne le sont pas (ar1_extraction.py).
"""
import re

import pandas as pd

from ar1_extraction import extraire_pdf
from commun import EXTRA, INTERIM, Etape, ecrire_csv, norm

ET = Etape(5, "ar1")
DOSSIER = EXTRA / "obj1" / "AR1_arcep_observatoire"

# --- 1. Lecture de tous les numéros
lignes = []
for f in sorted(DOSSIER.glob("AR1_*.pdf")):
    lignes += extraire_pdf(f)
brut = pd.DataFrame(lignes)
brut["libelle"] = brut["libelle"].fillna("").str.replace(r"\s*[-+]?\d+(?:,\d+)?\s?%", "", regex=True).str.strip()
brut["section"] = [c if str(c).startswith("Tableau") else t for c, t in zip(brut["contexte"], brut["titre_page"])]
ET.controle("AR1-numeros", "numéros lus", 34, brut["numero"].nunique(), brut["numero"].nunique() == 34)
ET.sortie(ecrire_csv(brut, INTERIM / "ar1_brut.csv"))
for _, r in brut[brut["note"] != ""].iterrows():
    ET.anomalie("AR1", f"{r.numero} p.{r.page}", r.libelle, "valeur corrigée", "corrigé", "extraction",
                r.note, f"{r.trimestre} : {r.valeur}")


# --- 2. Reconnaissance des séries (indicateur, opérateur, technologie)
def operateur(lib: str, fixe: bool) -> str | None:
    if re.search(r"\bTOTAL\b.*\bMOBILE\b|\bMOBILE\b.*\bTOTAL\b", lib) and not re.search(r"DATA|INTERNET|ABONNES", lib):
        return "total_mobile"
    if re.search(r"\bTOTAL\b.*\bFIXE\b", lib) and not re.search(r"ABONNES", lib):
        return "total_fixe"
    if re.search(r"\bTOTAL\b.*\bSECTEUR\b", lib):
        return "total_secteur"
    if "TOGO TELECOM" in lib:
        return "togo_telecom"
    if re.search(r"TOGO CELLULAIRE|TOGOCEL|\bTGC\b|\bMIXX\b|T ?MONEY", lib):
        return "togocom"
    if re.search(r"\bYAS\b", lib):
        return "togo_telecom" if fixe else "togocom"
    if re.search(r"\bMOOV\b|ATLANTIQUE|\bMAT\b|\bFLOOZ\b", lib):
        return "moov"
    if re.search(r"\bCAFE\b|INFORMATIQUE", lib):
        return "cafe"
    if re.search(r"\bTEOLIS\b", lib):
        return "teolis"
    if re.search(r"\bGVA\b", lib):
        return "gva"
    if re.search(r"\bTOTAL\b", lib):
        return "ensemble"
    return None


def techno_mobile(lib: str) -> str | None:
    if re.search(r"GPRS|EDGE", lib):
        return "2G"
    if re.search(r"\b3 ?G? ?ET 4G\b|\bET 4G\b", lib):
        return "3G+4G"  # Moov : 3G et 4G réunies jusqu'au T3 2019 (03, section 2)
    for t in ("5G", "4G", "3G"):
        if re.search(rf"\b{t}\b", lib):
            return t
    if "HAUT DEBIT" in lib:
        return "haut_debit"
    if re.search(r"\bTOTAL\b", lib):
        return "total"
    return None


def reconnaitre(section: str, entete: str, libelle: str):
    s, e, l = norm(section), norm(entete), norm(libelle)
    ctx = f"{s} {e}"
    if re.search(r"TAUX|PENETRATION|TELEDENSITE|PART DE MARCHE", l) or re.search(r"TAUX|PENETRATION|PART DE MARCHE", s):
        return None
    # Mobile money
    if re.search(r"MOBILE MONEY|TRANSACTIONS|POINT DE SERVICE", ctx + " " + l):
        if re.search(r"VALEUR", ctx + " " + l):
            ind, unite = "mm_valeur_transactions", "Md FCFA"
        elif re.search(r"VOLUME|NOMBRE DE TRANSACTIONS|NOMBRE TOTAL DE TRANSACTIONS", ctx + " " + l):
            ind, unite = "mm_nombre_transactions", "millions"
        elif re.search(r"PDV|POINTS? DE (VENTE|SERVICE)", ctx + " " + l):
            ind, unite = "mm_points_de_vente", "points de vente"
        elif re.search(r"ABONNES|COMPTES", ctx + " " + l):
            ind, unite = "mm_comptes", "comptes"
        else:
            return None
        op = "ensemble" if re.search(r"\bTOTALE?\b", l) else operateur(l, fixe=False)
        return (ind, op, "", unite) if op in ("moov", "togocom", "ensemble") else None
    # Chiffre d'affaires et investissement (CA « data » exclu : autre périmètre)
    if "CHIFFRE" in ctx and "DATA" not in s:
        if re.search(r"\bDATA FIXE\b", l):
            return None
        op = operateur(l, fixe=True if "TELECOM" in l else False)
        return ("ca", op, "", "Md FCFA") if op else None
    if "INVESTISSEMENT" in ctx:
        op = operateur(l, fixe=True if "TELECOM" in l else False)
        return ("investissement", op, "", "Md FCFA") if op else None
    # Téléphonie
    if "TELEPHONIE MOBILE" in ctx or "ABONNES ACTIFS" in ctx:
        if re.search(r"^TOTAL ABONNES", l):
            return ("abonnes_telephonie_mobile", "ensemble", "total", "abonnés")
        if l in ("PREPAID", "POSTPAID"):
            return ("abonnes_telephonie_mobile", "ensemble", l.lower(), "abonnés")
        return None
    if "TELEPHONIE FIXE" in ctx and re.search(r"^TOTAL ABONNES", l):
        return ("abonnes_telephonie_fixe", "ensemble", "total", "abonnés")
    # Internet mobile (abonnés data)
    if re.search(r"INTERNET MOBILE|MOBILES PAR TYPE", ctx):
        op = operateur(l, fixe=False)
        tech = techno_mobile(l)
        if op is None and tech in ("total", "haut_debit"):
            op = "ensemble"
        if re.search(r"^TOTAL ABONNES DATA MOBILE 2G|^TOTAL DATA MOBILE|^TOTAL ABONNES MOBILE INTERNET$", l):
            op, tech = "ensemble", "total"
        if "HAUT DEBIT" in l:
            tech = "haut_debit"
            op = op if op in ("togocom", "moov") else "ensemble"
        if op in ("togocom", "moov", "ensemble") and tech:
            return ("abonnes_data_mobile", op, tech, "abonnés")
        return None
    # FTTH par opérateur (depuis 2022)
    if s == "ABONNES FTTH":
        op = operateur(l, fixe=True)
        return ("abonnes_ftth", op, "FTTH", "abonnés") if op in ("togo_telecom", "gva", "ensemble") else None
    # Internet fixe de Togo Telecom par type d'accès
    if "TOGO TELECOM PAR TYPE" in s:
        for t in ("ADSL", "FTTH", "WIMAX", "LS", "EV DO", "CDMA"):
            if l.startswith(t) or f" {t}" in f" {l}":
                return ("abonnes_internet_fixe_acces", "togo_telecom", t.replace("EV DO", "EvDo").title()
                        if t not in ("ADSL", "FTTH", "LS", "CDMA") else t, "abonnés")
        if l.startswith("TOTAL"):
            return ("abonnes_internet_fixe_acces", "togo_telecom", "total", "abonnés")
        return None
    # Internet fixe par opérateur
    if re.search(r"INTERNET FIXE PAR OPERATEUR|^INTERNET FIXE$", s):
        op = operateur(l, fixe=True)
        return ("abonnes_internet_fixe", op, "total", "abonnés") if op in (
            "togo_telecom", "cafe", "teolis", "gva", "ensemble") else None
    return None


rec = [reconnaitre(s, e, l) for s, e, l in zip(brut["section"], brut["entete"].fillna(""), brut["libelle"])]
brut["indicateur"] = [r[0] if r else None for r in rec]
brut["operateur"] = [r[1] if r else None for r in rec]
brut["technologie"] = [r[2] if r else None for r in rec]
brut["unite"] = [r[3] if r else None for r in rec]
series = brut[brut["indicateur"].notna() & brut["valeur"].notna()].copy()

# Moov jusqu'au T4 2019 : la valeur publiée « 3G » réunit la 3G et la 4G (4G « ND » ; 03, section 2)
moov_3g = series.indicateur.eq("abonnes_data_mobile") & series.operateur.eq("moov") & series.technologie.eq("3G") \
    & (series.trimestre.str[:4].astype(int) * 4 + series.trimestre.str[-1].astype(int) <= 2019 * 4 + 4)
series.loc[moov_3g, "technologie"] = "3G+4G"
ET.effectif("AR1, Moov « 3G » jusqu'au T4 2019", int(moov_3g.sum()), "requalifiées 3G+4G (4G non publiée)", "3G+4G")

# Montants publiés en FCFA (numéro du T3 2020) : ramenés en milliards
fcfa = series["unite"].eq("Md FCFA") & (series["valeur"] > 1e5)
series.loc[fcfa, "valeur"] = series.loc[fcfa, "valeur"] / 1e9
ET.effectif("AR1, montants publiés en FCFA", int(fcfa.sum()), "divisés par 10⁹", "Md FCFA")
# Nombre de transactions publié en unités jusqu'en 2022, en millions ensuite : ramené en millions
unites = series["indicateur"].eq("mm_nombre_transactions") & (series["valeur"] > 1e4)
series.loc[unites, "valeur"] = series.loc[unites, "valeur"] / 1e6
ET.effectif("AR1, nombres de transactions publiés en unités", int(unites.sum()), "divisés par 10⁶", "millions")
ET.effectif("AR1, lignes lues", len(brut), "reconnaissance des séries utiles", len(series))
ET.sortie(ecrire_csv(series, INTERIM / "ar1_toutes_publications.csv"))

# --- 2 bis. Totaux incohérents avec la somme de leurs opérateurs dans un même numéro (CA, investissement) :
# ex. numéros de 2019, « CA Total Fixe » de 2018 publié en cumul depuis janvier. Le total est écarté pour ce numéro ;
# la publication cohérente la plus récente fait alors foi (DD5).
FIXES, MOBILES = ["togo_telecom", "cafe", "teolis", "gva"], ["togocom", "moov"]
a_ecarter = set()
for ind in ("ca", "investissement"):
    piv = series[series.indicateur == ind].pivot_table(index=["numero", "trimestre"], columns="operateur",
                                                      values="valeur", aggfunc="first")
    for (num, q), r in piv.iterrows():
        mauvais = set()
        for tot, ops in (("total_fixe", FIXES), ("total_mobile", MOBILES)):
            if pd.notna(r.get(tot)) and r[tot] > 0:
                somme = sum(r[o] for o in ops if o in r and pd.notna(r[o]))
                if somme > 0 and abs(somme - r[tot]) / r[tot] > 0.10:
                    mauvais |= {tot, "total_secteur"}
                    ET.anomalie("AR1", num, f"{ind}/{tot}", "total incohérent avec ses opérateurs", "écarté pour ce numéro",
                                "DD5", "la publication cohérente précédente fait foi",
                                f"{q} : total {r[tot]:g}, somme des opérateurs {somme:g}")
        for op in mauvais:
            a_ecarter.add((ind, op, num, q))
masque = [(i, o, n, q) in a_ecarter for i, o, n, q in zip(series.indicateur, series.operateur, series.numero, series.trimestre)]
ET.effectif("AR1, totaux incohérents avec leurs opérateurs", int(sum(masque)), "écartés du numéro concerné",
            "publication cohérente retenue")
series = series[[not m for m in masque]]

# --- 3. DD5 : une valeur par série et par trimestre, celle de la publication la plus récente
cle = ["indicateur", "operateur", "technologie", "trimestre"]
series = series.sort_values(["numero", "page"])
# Même série lue deux fois dans un numéro (tableau repris plus loin, ou en-tête mal hérité) :
# la première occurrence dans l'ordre des pages est gardée ; l'écart entre les deux lectures est qualifié.
grp = series.groupby(cle + ["numero"]).valeur
ecart_lect = ((grp.transform("max") - grp.transform("min")) / grp.transform("max").abs().clip(lower=1e-9))
series["conflit_meme_numero"] = 0
multi = series.duplicated(cle + ["numero"], keep=False)
for (k, g) in series[multi].groupby(cle + ["numero"]):
    e = (g.valeur.max() - g.valeur.min()) / max(abs(g.valeur.max()), 1e-9)
    type_ = ("doublon de lecture (valeurs égales)" if e == 0 else "doublon de lecture (arrondi)" if e < 1e-3
             else "conflit entre deux tableaux du même numéro")
    ET.anomalie("AR1", k[-1], "/".join(str(x) for x in k[:3]), type_, "première occurrence gardée (ordre des pages)",
                "DD5", "aucun" if e < 1e-3 else f"écart {100 * e:.1f} %",
                f"{k[3]} : " + " / ".join(f"{v:g} (p.{pg})" for v, pg in zip(g.valeur, g.page)))
    if e >= 1e-3:
        series.loc[g.index, "conflit_meme_numero"] = 1
series = series.drop_duplicates(cle + ["numero"], keep="first")
agg = series.groupby(cle).agg(n_publications=("valeur", "size"), valeur_min=("valeur", "min"),
                              valeur_max=("valeur", "max"))
derniere = series.groupby(cle).tail(1).set_index(cle)[["valeur", "unite", "numero", "page", "libelle", "conflit_meme_numero"]]
trim = derniere.join(agg).reset_index().rename(columns={"numero": "numero_source", "libelle": "libelle_source"})
trim["ecart_revision_pct"] = (100 * (trim["valeur_max"] - trim["valeur_min"]) / trim["valeur"].abs()).round(2)
trim["revise"] = (trim["ecart_revision_pct"] > 0.05).astype(int)
ET.effectif("AR1, valeurs trimestrielles (toutes publications)", len(series), "DD5 : dernière publication", len(trim))
grosses = trim[trim.ecart_revision_pct >= 5]
for _, r in grosses.iterrows():
    ET.anomalie("AR1", f"{r.indicateur}/{r.operateur}/{r.technologie}", r.trimestre, "révision",
                "dernière publication retenue", "P4 / DD5", f"écart entre publications : {r.ecart_revision_pct} %",
                f"{r.valeur_min:.0f} à {r.valeur_max:.0f} ; retenu {r.valeur:.0f} ({r.numero_source})")


# --- 4. Contrôles
def rang(q):
    return int(q[:4]) * 4 + int(q[-1])


attendus = [f"{a}T{t}" for a in range(2018, 2027) for t in range(1, 5) if rang(f"{a}T{t}") <= rang("2026T2")]
for ind, op, tech in (("abonnes_data_mobile", "ensemble", "total"), ("abonnes_telephonie_mobile", "ensemble", "total"),
                      ("ca", "total_secteur", ""), ("investissement", "total_secteur", ""),
                      ("abonnes_data_mobile", "togocom", "total"), ("abonnes_data_mobile", "moov", "total")):
    presents = set(trim.query("indicateur==@ind and operateur==@op and technologie==@tech").trimestre)
    manque = [q for q in attendus if q not in presents]
    ET.controle("TE2", f"{ind}/{op}/{tech} : trimestres T1 2018 - T2 2026", "34, aucun manquant",
                f"{34 - len(manque)} (manquants : {manque})", not manque, bloquant=ind in ("abonnes_data_mobile", "ca"))
mm = set(trim.query("indicateur=='mm_points_de_vente' and operateur=='ensemble'").trimestre)
ET.controle("TE2-mm", "mobile money (points de vente) : premier trimestre publié", "T4 2021 au plus tard",
            min(mm) if mm else "aucun", bool(mm) and rang(min(mm)) <= rang("2021T4"), bloquant=False)

piv = trim.pivot_table(index=["indicateur", "trimestre"], columns=["operateur", "technologie"], values="valeur")


def somme(ind, parts, total, tol=0.6):
    d = piv.loc[ind]
    ok_all, pires = True, []
    for q, r in d.iterrows():
        vals = [r.get(p) for p in parts]
        if any(pd.isna(v) for v in vals) or pd.isna(r.get(total)):
            continue
        e = 100 * abs(sum(vals) - r[total]) / r[total]
        if e > tol:
            ok_all = False
            pires.append(f"{q} ({e:.1f} %)")
    return ok_all, pires


ok, p = somme("abonnes_data_mobile", [("togocom", "total"), ("moov", "total")], ("ensemble", "total"))
ET.controle("AR1-somme-data", "data mobile : Togocom + Moov = total", "écart ≤ 0,6 %", p or "aucun écart", ok, bloquant=False)
for op in ("togocom", "moov"):
    parts = [(op, t) for t in ("2G", "3G", "4G", "5G", "3G+4G")]
    d = piv.loc["abonnes_data_mobile"]
    ecarts = []
    for q, r in d.iterrows():
        v = [r.get(pp) for pp in parts if pd.notna(r.get(pp))]
        if v and pd.notna(r.get((op, "total"))) and abs(sum(v) - r[(op, "total")]) / r[(op, "total")] > 0.006:
            ecarts.append(f"{q} ({100 * (sum(v) - r[(op, 'total')]) / r[(op, 'total')]:+.1f} %)")
    ET.controle("AR1-somme-techno", f"data mobile {op} : somme des technologies = total", "écart ≤ 0,6 %",
                ecarts or "aucun écart", not ecarts, bloquant=False)
ok, p = somme("ca", [("togocom", ""), ("moov", "")], ("total_mobile", ""))
ET.controle("AR1-somme-ca-mobile", "CA : Togocom + Moov = total mobile", "écart ≤ 0,6 %", p or "aucun écart", ok, bloquant=False)
# Périmètre du CA fixe : trimestres où le total publié exclut GVA (total = Togo Telecom + CAFE + TEOLIS)
cf = piv.loc["ca"]
hors_gva = []
for q, r in cf.iterrows():
    s3 = sum(r.get((o, "")) for o in ("togo_telecom", "cafe", "teolis") if pd.notna(r.get((o, ""))))
    if int(q[:4]) >= 2018 and pd.notna(r.get(("total_fixe", ""))) and abs(s3 - r[("total_fixe", "")]) <= 0.01 * r[("total_fixe", "")]:
        hors_gva.append(q)
ET.controle("AR1-perimetre-gva", "trimestres dont le CA fixe publié exclut GVA (rupture de périmètre)", "signalés",
            hors_gva, True, bloquant=False)
ok, p = somme("ca", [("togo_telecom", ""), ("cafe", ""), ("teolis", ""), ("gva", "")], ("total_fixe", ""), tol=2)
p = [x for x in p if x.split(" ")[0] not in hors_gva]
ET.controle("AR1-somme-ca-fixe", "CA : Togo Telecom + CAFE + TEOLIS + GVA = total fixe (hors trimestres publiés sans GVA)",
            "écart ≤ 2 %", p or "aucun écart", not p, bloquant=False)
ok, p = somme("ca", [("total_mobile", ""), ("total_fixe", "")], ("total_secteur", ""))
ET.controle("AR1-somme-ca", "CA : mobile + fixe = secteur", "écart ≤ 0,6 %", p or "aucun écart", ok, bloquant=False)
ok, p = somme("investissement", [("total_mobile", ""), ("total_fixe", "")], ("total_secteur", ""))
ET.controle("AR1-somme-inv", "investissement : mobile + fixe = secteur", "écart ≤ 0,6 %", p or "aucun écart", ok, bloquant=False)
ok, p = somme("mm_points_de_vente", [("moov", ""), ("togocom", "")], ("ensemble", ""))
ET.controle("AR1-somme-mm", "mobile money, points de vente : Moov + Togocom = total", "écart ≤ 0,6 %", p or "aucun écart",
            ok, bloquant=False)
v = trim.query("indicateur=='mm_points_de_vente' and operateur=='ensemble' and trimestre=='2021T4'").valeur
ET.controle("AR1-pdv-2021T4", "points de vente mobile money au T4 2021 (03 : 33 924)", 33924,
            int(v.iloc[0]) if len(v) else "absent", len(v) == 1 and int(v.iloc[0]) == 33924, bloquant=False)
v = trim.query("indicateur=='abonnes_data_mobile' and operateur=='ensemble' and technologie=='total'")
t19, t20 = v.set_index("trimestre").valeur.get("2019T4"), v.set_index("trimestre").valeur.get("2020T1")
ET.controle("S6", "rupture T4 2019 → T1 2020 du total data mobile (03 : -6,6 %)", "-6,6 %",
            f"{100 * (t20 - t19) / t19:.1f} %", round(100 * (t20 - t19) / t19, 1) == -6.6, bloquant=False)
ET.controle("AR1-revisions", "valeurs révisées d'au moins 5 % entre publications", "signalées au registre",
            len(grosses), True, bloquant=False)

# --- 5. Sortie : noms d'opérateurs (A2), ruptures signalées
NOMS = {"togocom": "Togocom (Togo Cellulaire)", "moov": "Moov Africa (Atlantique Telecom)",
        "togo_telecom": "Togo Telecom (YAS, fixe)", "cafe": "CAFE Informatique", "teolis": "TEOLIS", "gva": "GVA Togo",
        "ensemble": "Ensemble", "total_mobile": "Total mobile", "total_fixe": "Total fixe", "total_secteur": "Secteur"}
trim["operateur_libelle"] = trim["operateur"].map(NOMS)
trim["rupture"] = ""
trim.loc[trim.indicateur.eq("abonnes_data_mobile") & trim.trimestre.eq("2020T1"), "rupture"] = \
    "S6 : reclassement 3G / 4G de Togocel, non documenté ; aucune évolution par technologie calculée à travers"
trim.loc[trim.indicateur.eq("ca") & trim.operateur.isin(["togo_telecom", "total_fixe", "total_secteur"])
         & trim.trimestre.eq("2025T2"), "rupture"] = "périmètre du CA de Togo Telecom changé (voix et data fixes intégrées)"
trim.loc[trim.indicateur.eq("ca") & trim.operateur.isin(["togocom", "total_mobile", "total_secteur"])
         & trim.trimestre.eq("2026T2"), "rupture"] = "CA mobile money de YAS Togo non déclaré"
trim.loc[trim.technologie.eq("3G+4G"), "rupture"] = "3G et 4G de Moov réunies jusqu'au T4 2019"
sel = trim.indicateur.eq("ca") & trim.operateur.isin(["total_fixe", "total_secteur"]) & trim.trimestre.isin(hors_gva)
trim.loc[sel, "rupture"] = (trim.loc[sel, "rupture"].where(trim.loc[sel, "rupture"] == "", trim.loc[sel, "rupture"] + " ; ")
                            + "périmètre : CA de GVA non inclus dans le total publié")
trim.loc[trim.indicateur.eq("mm_comptes") & trim.trimestre.eq("2021T1"), "rupture"] = \
    "révision de l'ARCEP (comptes Moov du T1 2021 : 3,35 M puis 1,31 M) ; T3-T4 2020 sur l'ancienne base, non comparables"
trim["niveau_preuve"] = "A"
trim["source"] = "AR1 (ARCEP, observatoire trimestriel)"
cols = ["indicateur", "operateur", "operateur_libelle", "technologie", "trimestre", "valeur", "unite", "numero_source",
        "n_publications", "revise", "ecart_revision_pct", "conflit_meme_numero", "rupture", "niveau_preuve", "source",
        "libelle_source"]
ET.controle("DD5-conflits", "valeurs retenues venant d'un numéro où deux tableaux se contredisent", "signalées",
            int(trim.conflit_meme_numero.sum()), True, bloquant=False)
ET.sortie(ecrire_csv(trim[cols].sort_values(["indicateur", "operateur", "technologie", "trimestre"]),
                     INTERIM / "ar1_trimestriel.csv"))
non_rec = brut[brut["indicateur"].isna()].groupby(["section", "libelle"]).size()
ET.effectif("AR1, libellés non retenus (trafic, taux, parts de marché, CA data…)", int(non_rec.sum()), "hors séries utiles",
            f"{len(non_rec)} libellés distincts")
ET.fin()
