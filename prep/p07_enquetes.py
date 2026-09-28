"""Étape 7 — Enquêtes par région (04, EQ1 et EQ2) → data/processed/enquetes_region.csv.

Sources : EHCVM 2018/19 et 2021/22 (micro-données, W2), MICS6 2017 (tableaux transcrits, W1),
Afrobaromètre vagues 5 à 10 (micro-données, W4), Findex 2025 (base publiée, W3).
Chaque estimation garde sa source, sa population de référence et sa définition : elles ne se fusionnent pas.
Décisions appliquées : R5 (EHCVM sur les 6 domaines, libellé « Lomé » signalé), Q6 (réception déclarée du réseau).
"""
import numpy as np
import pandas as pd
import pyreadstat

from commun import EXTRA, PROCESSED, Etape, ecrire_csv

ET = Etape(7, "enquetes")
W = EXTRA / "obj1"
L: list[dict] = []
UR = {"Grand Lomé": "GL", "Lomé commune": "GL", "Maritime": "A_HGL", "Plateaux": "B", "Centrale": "C", "Kara": "D",
      "Savanes": "E"}


def ligne(source, vague, domaine_type, domaine, indicateur, pop_ref, est, bas=None, haut=None, n=None, code=None,
          niveau="B", note="", se=None):
    # CV : le 02 (O3-05, et O1-05 par renvoi) n'affiche une estimation d'échantillon que si CV < 30 %
    cv = None if se is None or est == 0 else round(100 * se / est, 1)
    L.append(dict(source=source, vague=vague, domaine_type=domaine_type, domaine=domaine,
                  unite_regionale_code=code, indicateur=indicateur, population_reference=pop_ref,
                  estimation_pct=round(est, 2), ic95_bas=None if bas is None else round(bas, 2),
                  ic95_haut=None if haut is None else round(haut, 2), cv_pct=cv,
                  affichable_cv30=None if cv is None else int(cv < 30), n_obs=n, niveau_preuve=niveau, note=note))


def proportion_plan(y, w, dom, strate, grappe):
    """Proportion pondérée dans un domaine et IC 95 % par linéarisation (grappes dans strates)."""
    wd = w * dom
    tot = wd.sum()
    p = (wd * y).sum() / tot
    z = pd.Series(wd * (y - p) / tot)
    zc = z.groupby([strate, grappe]).sum()
    var = 0.0
    for _, g in zc.groupby(level=0):
        nh = len(g)
        if nh > 1:
            var += nh / (nh - 1) * ((g - g.mean()) ** 2).sum()
    se = np.sqrt(var)
    return 100 * p, 100 * max(0, p - 1.96 * se), 100 * min(1, p + 1.96 * se), int(dom.sum()), 100 * se


# --- EQ1 : EHCVM, individus (fichier harmonisé)
VAGUES = {"2018/19": ("2018-19", "ehcvm_individu_tgo2018.dta", "alfab"),
          "2021/22": ("2021-22", "ehcvm_individu_tgo2021.dta", "alfa")}
for vague, (dossier, fichier, alfa) in VAGUES.items():
    d = pd.io.stata.StataReader(W / "W2_ehcvm" / dossier / "donnees" / fichier).read()
    n0 = len(d)
    d = d[d["resid"] == "Oui"]
    ET.effectif(f"EHCVM {vague}", n0, "résidents seulement", len(d))
    d["region"] = d["region"].astype(str)
    strate = d["region"] + "_" + d["milieu"].astype(str)
    grappe = d["grappe"].astype(int)
    w = d["hhweight"].astype(float)
    adulte = (d["age"] >= 15).astype(float)
    tout = pd.Series(1.0, index=d.index)
    variables = {"acces_internet_declare": ("internet", "accès à Internet déclaré (« individu a accès à Internet »)"),
                 "telephone_portable": ("telpor", "possède un téléphone portable"),
                 "compte_banque_ou_autre": ("bank", "compte en banque ou autre (variable harmonisée : réunit les 5 types de compte du module 6, mobile banking compris)"),
                 "alphabetisation": (alfa, "sait lire et écrire (variable harmonisée de la vague)")}
    domaines = [("national", "Togo", tout, None)] + \
               [("milieu", m, (d["milieu"].astype(str) == m).astype(float), None) for m in ("Urbain", "Rural")] + \
               [("region", r, (d["region"] == r).astype(float), UR.get(r)) for r in sorted(d["region"].unique())]
    for ind, (var, lib) in variables.items():
        y = (d[var].astype(str) == "Oui").astype(float)
        for pop_lib, filtre in (("individus de 15 ans et plus", adulte), ("tous les individus", tout)):
            if ind != "acces_internet_declare" and pop_lib == "tous les individus":
                continue
            for typ, nom, dom, code in domaines:
                p, b, h, n, se = proportion_plan(y, w, dom * filtre, strate, grappe)
                ligne("EHCVM (W2, micro-données)", vague, typ, nom, ind, pop_lib, p, b, h, n, code, se=se,
                      note=lib + (" ; libellé « Lomé commune » en 2018/19, mêmes grappes que « Grand Lomé » (R5)"
                                  if nom in ("Lomé commune", "Grand Lomé") else ""))
    reg = sorted(d["region"].unique())
    ET.controle(f"EQ1-{vague}", f"EHCVM {vague} : 6 domaines régionaux", 6, len(reg), len(reg) == 6)

    # Module 6 (adultes) : mobile banking. 2018/19 : « possède un compte dans un Mobile Banking » ;
    # 2021/22 : « fait du Mobile Banking ». Libellés différents : deux indicateurs, jamais mis en série.
    s6 = pd.io.stata.StataReader(W / "W2_ehcvm" / dossier / "donnees" /
                                 fichier.replace("ehcvm_individu", "s06_me")).read()
    menages = d.groupby(["grappe", "menage"])[["hhweight", "region", "milieu"]].first().reset_index()
    s6 = s6.merge(menages, on=["grappe", "menage"], how="left")
    valide = s6["s06q01__4"].astype(str).isin(["Oui", "Non"]) & s6["hhweight"].notna()
    s6 = s6[valide]
    ind6, lib6 = (("compte_mobile_banking", "possède un compte dans un Mobile Banking (module 6)") if vague == "2018/19"
                  else ("usage_mobile_banking", "fait du Mobile Banking (module 6)"))
    y6 = (s6["s06q01__4"].astype(str) == "Oui").astype(float)
    st6 = s6["region"].astype(str) + "_" + s6["milieu"].astype(str)
    for typ, nom, dom in [("national", "Togo", pd.Series(1.0, index=s6.index))] + \
            [("milieu", m, (s6["milieu"].astype(str) == m).astype(float)) for m in ("Urbain", "Rural")] + \
            [("region", r, (s6["region"].astype(str) == r).astype(float)) for r in reg]:
        p, b, h, n, se = proportion_plan(y6, s6["hhweight"].astype(float), dom, st6, s6["grappe"].astype(int))
        ligne("EHCVM (W2, micro-données)", vague, typ, nom, ind6, "répondants du module 6 (15 ans et plus)", p, b, h, n,
              UR.get(nom) if typ == "region" else None, se=se,
              note=lib6 + " ; « mobile banking » au sens du questionnaire UEMOA, sans nom d'opérateur")
    ET.effectif(f"EHCVM {vague}, module 6", "individus", "réponses valides à la question mobile banking", int(valide.sum()))

    # EQ2 : réception déclarée du réseau mobile dans les localités du module communautaire (540 grappes)
    co = pd.io.stata.StataReader(W / "W2_ehcvm" / dossier / "donnees" /
                                 fichier.replace("ehcvm_individu", "s01_co")).read()
    poids_g = (d.groupby("grappe")["hhweight"].sum()).rename("poids")
    info_g = d.groupby("grappe")[["region", "milieu"]].first()
    co = co.merge(info_g, left_on="grappe", right_index=True, how="left").merge(poids_g, left_on="grappe",
                                                                                right_index=True, how="left")
    ET.controle(f"EQ2-{vague}", f"EHCVM {vague} : localités du module communautaire rattachées à une région", 540,
                int(co["region"].notna().sum()), int(co["region"].notna().sum()) == 540)
    for k in (1, 2, 3):
        col = f"s01q13__{k}"
        ok = co[col].astype(str).isin(["Oui", "Non"])
        y = (co[col].astype(str) == "Oui").astype(float)
        for typ, nom, m in [("national", "Togo", ok)] + [("region", r, ok & (co.region == r)) for r in reg]:
            if m.sum() == 0:
                continue
            p_pop = 100 * (y[m] * co.poids[m]).sum() / co.poids[m].sum()
            p_loc = 100 * y[m].mean()
            ligne("EHCVM (W2, module communautaire)", vague, typ, nom, f"reseau_{k}_bien_capte",
                  "population des localités enquêtées", p_pop, n=int(m.sum()), code=UR.get(nom) if typ == "region" else None,
                  note=f"réception déclarée « Réseau {k} » (opérateur non nommé dans le fichier) ; part des localités : "
                       f"{p_loc:.1f} % ; déclaratif, jamais une mesure (Q6)")
ET.effectif("EHCVM", "2 vagues", "estimations pondérées, IC par linéarisation", f"{len(L)} lignes")

# --- MICS6 2017 : tableaux publiés, transcrits (W1)
m = pd.read_csv(W / "W1_mics6_2017" / "W1_mics6-togo-2017_tic-alphabetisation_par-region.csv")
n_avant = len(L)
for _, r in m[m["unite"] == "%"].iterrows():
    typ = {"Total": "national", "Milieu": "milieu", "Région": "region"}[r.type_domaine]
    nom = "Togo" if r.domaine == "Total" else r.domaine
    code = UR.get(nom) if typ == "region" and nom in ("Plateaux", "Centrale", "Kara", "Savanes") else None
    ligne("MICS6 2017 (W1, tableaux publiés)", "2017", typ, nom, r.indicateur, r.population, r.valeur, code=code,
          niveau="C", note=f"tableau {r.tableau}, p. {r.page_pdf} du rapport"
          + (" ; domaine propre à la MICS6, sans équivalent exact dans nos unités" if typ == "region" and code is None else ""))
ET.effectif("MICS6", len(m), "valeurs en %", len(L) - n_avant)

# --- Afrobaromètre, vagues 5 à 10 : usage d'Internet (toute fréquence) ; compte mobile money (vague 9)
AB = {5: ("q91b", "withinwt"), 6: ("q92b", "withinwt"), 7: ("Q91B", "withinwt"), 8: ("Q92I", "withinwt"),
      9: ("Q90I", "withinwt_hh"), 10: ("Q90J", "withinwt_hh")}
NOM_AB = {1140: "Lomé commune", 1141: "Maritime", 1142: "Plateaux", 1143: "Centrale", 1144: "Kara", 1145: "Savanes"}
n_avant = len(L)
for vg, (q, wv) in AB.items():
    df, meta = pyreadstat.read_sav(W / "W4_afrobarometre" / f"W4_afrobarometre_tog_r{vg}.sav")
    regc = [c for c in df.columns if c.lower() == "region"][0]
    datec = [c for c in df.columns if c.lower() == "dateintr"][0]
    annee = str(pd.to_datetime(df[datec], errors="coerce").dt.year.mode().iloc[0])
    indicateurs = [(q, "usage_internet_toute_frequence", lambda s: s.isin([1, 2, 3, 4]), lambda s: s.isin([0, 1, 2, 3, 4]))]
    if vg == 9:
        indicateurs.append(("Q90H_TOG", "compte_mobile_money_personnel", lambda s: s == 2, lambda s: s.isin([0, 1, 2])))
    for var, ind, oui, valide in indicateurs:
        ok = valide(df[var])
        y, w = oui(df[var]).astype(float)[ok], df[wv][ok]
        for typ, nom, dom in [("national", "Togo", pd.Series(True, index=y.index))] + \
                [("region", NOM_AB[k], df[regc][ok] == k) for k in NOM_AB]:
            yy, ww = y[dom], w[dom]
            p = (yy * ww).sum() / ww.sum()
            n_eff = ww.sum() ** 2 / (ww ** 2).sum()
            se = np.sqrt(p * (1 - p) / n_eff)
            code = UR.get(nom) if nom in ("Plateaux", "Centrale", "Kara", "Savanes") else None
            ligne(f"Afrobaromètre R{vg} (W4, micro-données)", annee, typ, nom, ind, "adultes de 18 ans et plus",
                  100 * p, 100 * max(0, p - 1.96 * se), 100 * min(1, p + 1.96 * se), int(dom.sum()), code,
                  niveau="C", se=100 * se,
                  note="IC approximatif (effectif efficace de Kish, grappes non modélisées)"
                       + ("" if code or typ != "region" else " ; domaine Afrobaromètre sans équivalent exact"))
ET.effectif("Afrobaromètre", "6 vagues", "usage d'Internet (+ mobile money en R9)", len(L) - n_avant)

# --- Findex 2025 (base publiée) : Togo, comptes (national et ventilations publiées)
f = pd.read_csv(W / "W3_findex2025" / "W3_GlobalFindexDatabase2025.csv", low_memory=False)
t = f[f["codewb"] == "TGO"]
n_avant = len(L)
for _, r in t.iterrows():
    for col, ind in (("account_t_d", "compte_total"), ("mobileaccount_t_d", "compte_mobile_money"),
                     ("fiaccount_t_d", "compte_institution_financiere"),
                     ("internet", "usage_internet_3_mois"), ("con9a", "smartphone_telephone_principal"),
                     ("con31a", "sans_smartphone_cause_cout"), ("con31b", "sans_smartphone_cause_cout_data")):
        if pd.notna(r[col]):
            dom = "Togo" if str(r["group"]).lower() == "all" else f"{r['group']} : {r['group2']}"
            ligne("Findex 2025 (W3, base publiée)", str(int(r["year"])), "national" if dom == "Togo" else "ventilation",
                  dom, ind, "adultes de 15 ans et plus", 100 * float(r[col]) if float(r[col]) <= 1 else float(r[col]),
                  niveau="C", note="tel que publié par la Banque mondiale")
ET.effectif("Findex", len(t), "Togo, toutes vagues et ventilations publiées", len(L) - n_avant)

eq = pd.DataFrame(L)
f24 = eq[(eq.source.str.startswith("Findex")) & (eq.vague == "2024") & (eq.domaine == "Togo") & (eq.indicateur == "compte_total")]
ET.controle("EQ-Findex", "Findex 2024, détention d'un compte (03 : 57,4 %)", 57.4,
            round(f24.estimation_pct.iloc[0], 1) if len(f24) else "absent", len(f24) == 1 and round(f24.estimation_pct.iloc[0], 1) == 57.4,
            bloquant=False)
ET.controle("EQ-IC", "toute estimation calculée sur micro-données a un IC 95 %", 0,
            int(eq[(eq.niveau_preuve == "B") & (~eq.source.str.contains("communautaire")) & eq.ic95_bas.isna()].shape[0]),
            eq[(eq.niveau_preuve == "B") & (~eq.source.str.contains("communautaire"))].ic95_bas.notna().all())
ET.sortie(ecrire_csv(eq, PROCESSED / "enquetes_region.csv"))
ET.fin()
