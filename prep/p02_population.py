"""Étape 2 — Population par territoire (04, section 4 : R6 et R7).

Entrées : RG2 (national, régions, préfectures) et RG3 (communes), transcriptions des livrets du RGPH-5 ;
D6 en contrôle seulement (R4).
Sortie : data/interim/population_territoires.csv
Décisions appliquées : R2, R4 (RG2 / RG3 source des objectifs 3 et 4), S5 (âge non déclaré au prorata),
strates de O3-02 (seuil 50 %, variante 75 %).
"""
import pandas as pd

from commun import EXTRA, INTERIM, RAW, Etape, ecrire_csv, norm

ET = Etape(2, "population")
D = EXTRA / "obj4" / "RG_rgph5_livrets"
rg2 = pd.read_csv(D / "RG2_rgph5_population-age-milieu-sexe_national-regions-prefectures.csv")
rg3 = pd.read_csv(D / "RG3_rgph5_population-age-milieu-sexe_communes.csv")
ref = pd.read_csv(INTERIM / "referentiel_territoires.csv", dtype=str)

AGES_15_PLUS = ["15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64",
                "65-69", "70-74", "75-79", "80-84", "85 et +"]
AGES_DECLARES = ["0", "1-4", "5-9", "10-14"] + AGES_15_PLUS


def agreger(df: pd.DataFrame) -> pd.DataFrame:
    """Une ligne par unité : totaux, milieux, 15 ans et plus (déclaré, prorata, hors non déclarés)."""
    e = df[df["sexe"] == "Ensemble"]
    piv = e.pivot_table(index="unite", columns=["milieu", "groupe_age"], values="effectif", aggfunc="sum")
    out = pd.DataFrame(index=piv.index)
    out["pop_totale"] = piv[("Total", "Total")]
    out["pop_urbaine"] = piv[("Urbain", "Total")]
    out["pop_rurale"] = piv[("Rural", "Total")]
    out["pop_age_nd"] = piv[("Total", "ND")]
    out["pop_ages_declares"] = piv[[("Total", a) for a in AGES_DECLARES]].sum(axis=1)
    out["pop15_hors_nd"] = piv[[("Total", a) for a in AGES_15_PLUS]].sum(axis=1)
    # S5 : l'âge non déclaré est réparti au prorata de la structure par âge déclarée (convention).
    out["pop15_prorata"] = (out["pop15_hors_nd"] * out["pop_totale"] / out["pop_ages_declares"]).round(0).astype(int)
    return out.reset_index()


com = agreger(rg3)
pref = agreger(rg2[rg2["type_unite"] == "Préfecture"])
autres = agreger(rg2[rg2["type_unite"] != "Préfecture"])

# --- Contrôles de structure de la transcription
for nom, t in (("communes", com), ("préfectures", pref), ("autres niveaux", autres)):
    ok_age = (t["pop_ages_declares"] + t["pop_age_nd"] == t["pop_totale"]).all()
    ok_mil = (t["pop_urbaine"] + t["pop_rurale"] == t["pop_totale"]).all()
    ET.controle(f"ST-age-{nom}", f"{nom} : âges déclarés + non déclarés = total", "toutes", ok_age, ok_age)
    ET.controle(f"ST-milieu-{nom}", f"{nom} : urbain + rural = total", "toutes", ok_mil, ok_mil)

# --- Jointure aux codes du référentiel par le nom normalisé (sans correction attendue)
def joindre(t: pd.DataFrame, niveau: str) -> pd.DataFrame:
    r = ref[ref["niveau"] == niveau][["code", "nom_norm"]]
    t = t.assign(nom_norm=t["unite"].map(norm)).merge(r, on="nom_norm", how="left")
    manquants = t[t["code"].isna()]["unite"].tolist()
    ET.controle(f"R6-{niveau}", f"{niveau}s de RG joints au référentiel sans correction", len(r),
                f"{t['code'].notna().sum()} (non joints : {manquants})", not manquants and len(t) == len(r))
    return t


com = joindre(com, "commune").assign(niveau="commune")
pref = joindre(pref, "prefecture").assign(niveau="prefecture")
CODES_AUTRES = {"TOGO": ("pays", "TG"), "Maritime": ("region", "A"), "Plateaux": ("region", "B"),
                "Centrale": ("region", "C"), "Kara": ("region", "D"), "Savanes": ("region", "E"),
                "Grand Lomé (DAGL)": ("unite_regionale", "GL"), "Maritime sans Grand Lomé": ("unite_regionale", "A_HGL")}
autres["niveau"] = autres["unite"].map(lambda u: CODES_AUTRES[u][0])
autres["code"] = autres["unite"].map(lambda u: CODES_AUTRES[u][1])
# Plateaux, Centrale, Kara, Savanes sont aussi des unités régionales (mêmes effectifs)
ur_bcde = autres[autres["code"].isin(list("BCDE"))].assign(niveau="unite_regionale")
pop = pd.concat([autres, ur_bcde, pref, com], ignore_index=True)

# --- GE4 : emboîtement communes → préfectures → unités régionales → national
ref_com = ref[ref["niveau"] == "commune"].set_index("code")
com_ = com.assign(prefecture_code=com["code"].map(ref_com["prefecture_code"]),
                  ur=com["code"].map(ref_com["unite_regionale_code"]))
cols = ["pop_totale", "pop_urbaine", "pop15_hors_nd", "pop_age_nd"]
s_pref = com_.groupby("prefecture_code")[cols].sum()
ecart_pref = (s_pref - pref.set_index("code")[cols]).abs().sum().sum()
ET.controle("GE4-pref", "somme des communes = préfecture (écart absolu cumulé)", 0, ecart_pref, ecart_pref == 0)
s_ur = com_.groupby("ur")[cols].sum()
ur_rg = pop[pop["niveau"] == "unite_regionale"].set_index("code")[cols]
ecart_ur = (s_ur - ur_rg.loc[s_ur.index]).abs().sum().sum()
ET.controle("GE4-ur", "somme des communes = unité régionale", 0, ecart_ur, ecart_ur == 0)
nat = int(pop.query("niveau=='pays'").pop_totale.iloc[0])
ET.controle("GE4-nat", "population nationale = somme des communes", 8095498, f"{nat} / {int(com.pop_totale.sum())}",
            nat == 8095498 and int(com.pop_totale.sum()) == nat)
gl = int(pop.query("code=='GL'").pop_totale.iloc[0])
ET.controle("GE6", "population du Grand Lomé", "2 188 376 (27,0 %)", f"{gl} ({100 * gl / nat:.1f} %)", gl == 2188376)

# --- GE7 : RG2 / RG3 égaux à D6 (D6 fusionne Danyi 1 et Danyi 2)
d6 = pd.read_csv(RAW / "D6_rgph.csv")
valeurs_d6 = set(d6["Value"].astype(int))
danyi = com[com["unite"].str.startswith("Danyi")]
attendus = [v for u, v in zip(com["unite"], com["pop_totale"]) if not u.startswith("Danyi")]
attendus += list(pref["pop_totale"]) + [int(danyi["pop_totale"].sum())]
absents = [v for v in attendus if int(v) not in valeurs_d6]
ET.controle("GE7", "totaux RG2 / RG3 présents dans D6 (Danyi 1 + 2 sommées)", 0, len(absents), not absents)

# --- R7 : strates urbaines par commune (O3-02)
com["part_urbaine"] = (com["pop_urbaine"] / com["pop_totale"]).round(4)
gl_com = set(ref_com[ref_com["unite_regionale_code"] == "GL"].index)
for seuil, col in ((0.50, "strate_50"), (0.75, "strate_75")):
    com[col] = [("grand_lome" if c in gl_com else "autres_villes" if p >= seuil else "rural")
                for c, p in zip(com["code"], com["part_urbaine"])]
n50 = com["strate_50"].value_counts().reindex(["grand_lome", "autres_villes", "rural"]).tolist()
n75 = com["strate_75"].value_counts().reindex(["grand_lome", "autres_villes", "rural"]).tolist()
ET.controle("R7", "strates (Grand Lomé / autres villes / rural), seuil 50 %", [13, 13, 91], n50, n50 == [13, 13, 91])
ET.controle("R7-75", "strates, variante au seuil de 75 %", [13, 2, 102], n75, n75 == [13, 2, 102])

# --- Sortie
pop = pd.concat([pop[pop["niveau"] != "commune"], com], ignore_index=True)
pop["pop15_ecart_variante_pct"] = (100 * (pop["pop15_prorata"] - pop["pop15_hors_nd"]) / pop["pop15_prorata"]).round(2)
pop["source_population"] = "RGPH-5 2022 (RG2, RG3)"
cols = ["niveau", "code", "unite", "pop_totale", "pop_urbaine", "pop_rurale", "part_urbaine", "pop15_prorata",
        "pop15_hors_nd", "pop15_ecart_variante_pct", "pop_age_nd", "strate_50", "strate_75", "source_population"]
pop = pop.reindex(columns=cols).rename(columns={"unite": "libelle_rgph"})
ET.sortie(ecrire_csv(pop, INTERIM / "population_territoires.csv"))
n = pop.query("niveau=='pays'").iloc[0]
ET.effectif("15 ans et plus (national)", f"{int(n.pop15_hors_nd)} déclarés + {int(n.pop_age_nd)} âge ND au total",
            "prorata (S5)", f"{int(n.pop15_prorata)} (variante hors ND : -{n.pop15_ecart_variante_pct} %)")
ET.effectif("unités avec population", "RG2 + RG3", "jointure au référentiel", len(pop))
ET.fin()
