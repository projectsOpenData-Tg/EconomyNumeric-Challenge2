"""08 — Priorisation (étape 09 de la procédure) : score O5-01 par préfecture.

Lit les tables du 07 (indicateurs) et du 06 (contrôle), écrit des tables dans data/analysis/08_priorisation/.

Règles, fixées avant le calcul (02, ligne O5-01 ; A11, A13 et H6 ; décisions du 27/09/2026) :
- maille : les 39 préfectures (02). Population RGPH 2022 affichée à côté du score, jamais dedans ;
- trois dimensions, orientées « plus haut = plus mal servi » :
  D1 accès formel = habitants par point formel (O4-01 ; banques, IMF, assurances ; DAB exclus) ;
  D2 maillage mobile money = habitants par point mobile money (O4-04) ;
  D3 couverture = part de la population hors couverture, 100 - proxy 3i (O2-06, niveau C) ;
- normalisation : rang percentile, 100 * (rang moyen - 1) / (n - 1), 100 = le plus mal servi ; base = les
  préfectures classées ; 0 point formel = rang le plus défavorable (règle, pas estimation) ;
- donnée manquante : Mô, Kpendjal et Tchamba ont une couverture « non déterminable » (A13). Elles sont hors du
  classement à 3 dimensions (02 : jamais 0) et lues avec le score à 2 dimensions, affiché à côté ;
- H6 (validé) : corrélation de rang de D3 avec D1 et avec D2 sur les préfectures classées. Si l'une dépasse 0,7,
  D3 est fusionnée avec cette dimension (moyenne de leurs deux rangs) et le score n'a plus que 2 dimensions ;
- score = moyenne pondérée, poids égaux (02) ; classes : >= 70 priorité 1, 40 à moins de 70 priorité 2,
  < 40 priorité 3, sur la valeur non arrondie ;
- sensibilité (02) : chaque poids doublé tour à tour ; min-max au lieu du rang percentile ; retrait du
  territoire extrême = celui dont une valeur brute s'écarte le plus de la médiane, en écarts interquartiles
  (0 point formel = écart infini). Classe « robuste » si elle ne change sous aucun de ces tests, sinon
  « instable » ; le territoire retiré n'est jugé que sur les autres tests ;
- A11 (validé) : la couverture reste la 3e dimension, affichée à part ; score sans elle (D1 et D2, les 39
  préfectures) comme lecture de sensibilité. « Dépend de la couverture » si la classe y change ;
- confiance : faible si instable ; moyenne si robuste mais dépendante de la couverture, ou si la couverture
  de la préfecture contient une commune douteuse (P6) ou non déterminable ; élevée sinon ;
- ordre final : classe, puis population décroissante (02 : à classe égale, la population exposée départage).

Variante P13, décidée APRÈS avoir vu le résultat, donc affichée à côté et jamais à la place : le min-max compresse
l'échelle (aucun score min-max n'atteint 70), si bien que les seuils du 02 y font changer de classe presque tous les
territoires sans que l'ordre bouge. La variante lit le test min-max en rang : les n1 premiers du classement min-max
sont en priorité 1, les n2 suivants en priorité 2 (n1 et n2 = effectifs du score principal). Les autres tests
sont inchangés.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "prep"))
from commun import PREFECTURES_GRAND_LOME, PROCESSED, RACINE  # noqa: E402

IND = RACINE / "data" / "analysis" / "07_indicateurs"
SPA = RACINE / "data" / "analysis" / "06_spatial"
SORTIE = RACINE / "data" / "analysis" / "08_priorisation"
SORTIE.mkdir(parents=True, exist_ok=True)
R: dict[str, pd.DataFrame] = {}

SEUIL_H6 = 0.7
DIMS = {"D1": "accès formel", "D2": "maillage mobile money", "D3": "couverture (proxy)"}
lire = lambda d, n: pd.read_csv(d / f"{n}.csv")  # noqa: E731

# ----------------------------------------------------------------- Données (tables du 07)
pref = lire(IND, "o4_prefectures")
couv = lire(IND, "o2_06_couverture")
cel = lire(IND, "o4_06_cellules")
com = lire(IND, "o4_communes").merge(pd.read_csv(PROCESSED / "terr_commune.csv")[["code", "prefecture_code"]], on="code")
tp = pd.read_csv(PROCESSED / "terr_prefecture.csv").set_index("code")

t = pref[["code", "nom", "unite_regionale", "pop_totale", "n_formels", "n_mm", "hab_par_point_formel", "hab_par_point_mm",
          "statut_O4_05", "statut_O4_05_variante_P9"]].copy()
cp = couv[couv.maille == "préfecture"].set_index("code")
t["couverture_proxy_pct"] = t.code.map(cp.couverture_proxy_pct)
t["cellule_O4_06"] = t.code.map(cel[cel.maille == "préfecture"].set_index("code").cellule_O4_06)
t["densite_hab_km2"] = t.code.map(tp.pop_totale / tp.superficie_km2)
t["D1"] = np.where(t.n_formels == 0, np.inf, t.hab_par_point_formel)
t["D2"] = t.hab_par_point_mm
t["D3"] = 100 - t.couverture_proxy_pct
t["couverture_nd"] = t.D3.isna()
t["avertissement_P2"] = t.code.isin(PREFECTURES_GRAND_LOME)

# Signaux communaux par préfecture (S1 du 06 : le déficit est local, la préfecture le cache)
cc = couv[couv.maille == "commune"].set_index("code")
com["cellule_O4_06"] = com.code.map(cel[cel.maille == "commune"].set_index("code").cellule_O4_06)
com["couv_douteuse"] = com.code.map(cc.valeur_douteuse_P6).astype(bool)
com["couv_nd"] = com.code.map(cc.classe_02).str.startswith("non déterminable")
g = com.groupby("prefecture_code")
noms = lambda m: g.apply(lambda x: ", ".join(sorted(x.nom[m.loc[x.index]])), include_groups=False)  # noqa: E731
crit = com.cellule_O4_06.str.startswith("critique")
sansf = com.n_formels == 0
t = t.set_index("code")
t["communes_critiques_O4_06"] = noms(crit)
t["pop_communes_critiques"] = com[crit].groupby("prefecture_code").pop_totale.sum()
t["communes_sans_point_formel"] = g.apply(lambda x: int((x.n_formels == 0).sum()), include_groups=False)
t["noms_communes_sans_point_formel"] = noms(sansf)
t["pop_communes_sans_point_formel"] = com[sansf].groupby("prefecture_code").pop_totale.sum()
t["communes_couverture_douteuse_P6"] = noms(com.couv_douteuse)
t["communes_couverture_nd"] = noms(com.couv_nd)
t = t.reset_index()
for c in ("pop_communes_critiques", "pop_communes_sans_point_formel"):
    t[c] = t[c].fillna(0).astype(int)


# ----------------------------------------------------------------- Outils
def pct(x: pd.Series) -> pd.Series:
    """Rang percentile, 100 = le plus mal servi ; ex aequo au rang moyen ; inf = rang le plus défavorable."""
    return 100 * (x.rank(method="average") - 1) / (x.notna().sum() - 1)


def minmax(x: pd.Series) -> pd.Series:
    f = x.replace(np.inf, np.nan)
    v = 100 * (x - f.min()) / (f.max() - f.min())
    return v.where(x != np.inf, 100.0)


def classe(s):
    return np.select([s >= 70, s >= 40], ["priorité 1", "priorité 2"], "priorité 3").astype(object)


def score(df, dims, poids=None, norm=pct, fusion=None):
    """Moyenne pondérée des dimensions normalisées. fusion = (Da, Db) : une seule dimension, moyenne des deux."""
    n = {d: norm(df[d]) for d in dims}
    if fusion:
        a, b = fusion
        n[f"{a}+{b}"] = (n.pop(a) + n.pop(b)) / 2
    poids = poids or {k: 1 for k in n}
    return sum(poids[k] * v for k, v in n.items()) / sum(poids.values()), list(n)


def extreme(df, dims):
    ecarts = {}
    for d in dims:
        x = df[d]
        f = x.replace(np.inf, np.nan)
        iqr = f.quantile(.75) - f.quantile(.25)
        ecarts[d] = ((x - f.median()).abs() / iqr).replace(np.nan, 0)
    e = pd.DataFrame(ecarts)
    i = e.max(axis=1).idxmax()
    return i, e.loc[i].idxmax()


def evaluer(df, dims, fusion=None, prefixe=""):
    """Score principal, classe, tests de sensibilité du 02 et robustesse, sur la base df."""
    out = pd.DataFrame(index=df.index)
    s, dims_f = score(df, dims, fusion=fusion)
    out[f"{prefixe}score"] = s
    out[f"{prefixe}classe"] = classe(s)
    out[f"{prefixe}rang_score"] = s.rank(ascending=False, method="min").astype(int)
    tests = {}
    for k in dims_f:
        p = {j: (2 if j == k else 1) for j in dims_f}
        nm = f"poids {k} doublé"
        sp, _ = score(df, dims, poids=p, fusion=fusion)
        tests[nm] = sp
    tests["min-max"], _ = score(df, dims, norm=minmax, fusion=fusion)
    ix, dx = extreme(df, dims)
    sx, _ = score(df.drop(index=ix), dims, fusion=fusion)
    tests[f"sans {df.loc[ix, 'nom']}"] = sx.reindex(df.index)
    change = pd.DataFrame(index=df.index)
    for nm, v in tests.items():
        out[f"{prefixe}classe_test_{nm}"] = pd.Series(classe(v), index=v.index).where(v.notna())
        change[nm] = out[f"{prefixe}classe_test_{nm}"].notna() & (out[f"{prefixe}classe_test_{nm}"] != out[f"{prefixe}classe"])
    out[f"{prefixe}robustesse"] = np.where(change.any(axis=1), "instable", "robuste")
    out[f"{prefixe}tests_qui_changent_la_classe"] = change.apply(lambda r: ", ".join(r.index[r]), axis=1)
    meta = [dict(test=nm, territoires=int(v.notna().sum()), classes_changees=int(change[nm].sum()),
                 rho_avec_principal=round(v.corr(s, method="spearman"), 3)) for nm, v in tests.items()]
    # Variante P13 (après le résultat) : min-max lu en rang, mêmes effectifs par classe que le score principal
    sm = tests["min-max"]
    n = pd.Series(out[f"{prefixe}classe"]).value_counts()
    n1, n2 = n.get("priorité 1", 0), n.get("priorité 2", 0)
    o = sm.rank(ascending=False, method="first")
    cl = pd.Series(np.select([o <= n1, o <= n1 + n2], ["priorité 1", "priorité 2"], "priorité 3"), index=sm.index)
    out[f"{prefixe}classe_test_min-max lu en rang (P13)"] = cl
    out[f"{prefixe}ecart_de_rang_min_max"] = (sm.rank(ascending=False, method="min") - out[f"{prefixe}rang_score"]).astype(int)
    ch = change.drop(columns="min-max").assign(**{"min-max lu en rang": cl != out[f"{prefixe}classe"]})
    out[f"{prefixe}robustesse_P13"] = np.where(ch.any(axis=1), "instable", "robuste")
    out[f"{prefixe}tests_qui_changent_la_classe_P13"] = ch.apply(lambda r: ", ".join(r.index[r]), axis=1)
    meta.append(dict(test="min-max lu en rang (variante P13)", territoires=len(cl), classes_changees=int(ch["min-max lu en rang"].sum()),
                     rho_avec_principal=meta[-2]["rho_avec_principal"]))
    return out, dims_f, meta, (df.loc[ix, "nom"], dx)


# ----------------------------------------------------------------- H6 : corrélations sur les préfectures classées
base3 = t[~t.couverture_nd].set_index("code")
paires = [("D3", "D1"), ("D3", "D2"), ("D1", "D2"), ("D3", "densite_hab_km2")]
cor = []
for a, b in paires:
    rho = base3[a].corr(base3[b], method="spearman")
    cor.append(dict(dimension_a=f"{a} {DIMS.get(a, '')}".strip(), dimension_b=f"{b} {DIMS.get(b, 'densité de population')}",
                    rho_spearman=round(rho, 3), prefectures=len(base3),
                    regle_H6=("fusion" if rho > SEUIL_H6 else "pas de fusion") if b in ("D1", "D2") and a == "D3" else "information"))
R["h6_correlations"] = pd.DataFrame(cor)
fus = [(a, b) for a, b in paires[:2] if base3[a].corr(base3[b], method="spearman") > SEUIL_H6]
FUSION = None
if fus:
    FUSION = max(fus, key=lambda p: base3[p[0]].corr(base3[p[1]], method="spearman"))[::-1]

# ----------------------------------------------------------------- Score principal (3 dimensions, 36 préfectures)
p3, dims3, meta3, ext3 = evaluer(base3, ["D1", "D2", "D3"], fusion=FUSION)
for d in ("D1", "D2", "D3"):
    p3[f"{d}_rang_pct"] = pct(base3[d])
# Lecture sans couverture (A11 c) : D1 et D2, les 39 préfectures
base2 = t.set_index("code")
p2, dims2, meta2, ext2 = evaluer(base2, ["D1", "D2"], prefixe="sans_couv_")
for d in ("D1", "D2"):
    p2[f"sans_couv_{d}_rang_pct"] = pct(base2[d])

s = base2.join(p3).join(p2)
s["depend_de_la_couverture"] = s.classe.notna() & (s.classe != s.sans_couv_classe)
s["classe_retenue"] = s.classe.fillna("non déterminable (couverture)")
s["lecture"] = np.where(s.couverture_nd, "2 dimensions seulement : couverture non déterminable (A13)", "3 dimensions")
doute = (s.communes_couverture_douteuse_P6 != "") | (s.communes_couverture_nd != "")
s["confiance"] = np.select(
    [s.couverture_nd, s.robustesse == "instable", s.depend_de_la_couverture | doute],
    ["non classée (lecture à 2 dimensions)", "faible", "moyenne"], "élevée")
s["confiance_P13"] = np.select(
    [s.couverture_nd, s.robustesse_P13 == "instable", s.depend_de_la_couverture | doute],
    ["non classée (lecture à 2 dimensions)", "faible", "moyenne"], "élevée")
ordre = {"priorité 1": 1, "priorité 2": 2, "priorité 3": 3}
s["_o"] = s.classe.map(ordre).fillna(4)
s = s.sort_values(["_o", "pop_totale"], ascending=[True, False])
s["ordre_final"] = pd.array(np.arange(1, len(s) + 1), dtype="Int64")
s.loc[s.couverture_nd, "ordre_final"] = pd.NA
s = s.drop(columns="_o").reset_index()

COLS = (["ordre_final", "code", "nom", "unite_regionale", "pop_totale", "classe_retenue", "score", "rang_score", "robustesse",
         "tests_qui_changent_la_classe", "confiance", "robustesse_P13", "tests_qui_changent_la_classe_P13", "confiance_P13",
         "ecart_de_rang_min_max", "lecture", "D1", "D1_rang_pct", "D2", "D2_rang_pct", "D3", "D3_rang_pct",
         "couverture_proxy_pct", "sans_couv_D1_rang_pct", "sans_couv_D2_rang_pct", "sans_couv_score", "sans_couv_classe", "sans_couv_robustesse",
         "sans_couv_tests_qui_changent_la_classe", "sans_couv_robustesse_P13", "sans_couv_tests_qui_changent_la_classe_P13",
         "depend_de_la_couverture", "statut_O4_05", "statut_O4_05_variante_P9",
         "cellule_O4_06", "communes_critiques_O4_06", "pop_communes_critiques", "communes_sans_point_formel", "noms_communes_sans_point_formel",
         "pop_communes_sans_point_formel", "communes_couverture_douteuse_P6", "communes_couverture_nd", "avertissement_P2",
         "densite_hab_km2"]
        + [c for c in s if c.startswith("classe_test_") or c.startswith("sans_couv_classe_test_")])
out = s[COLS].copy()
out["D1"] = out.D1.replace(np.inf, np.nan)  # 0 point formel : rang le plus défavorable, pas de valeur
R["score_prefectures"] = out.round(2)

# ----------------------------------------------------------------- Synthèses
syn = []
for lec, col, base in (("3 dimensions", "classe", s[~s.couverture_nd]), ("sans couverture", "sans_couv_classe", s)):
    for k, gg in base.groupby(col):
        pre = "" if lec == "3 dimensions" else "sans_couv_"
        syn.append(dict(lecture=lec, classe=k, prefectures=len(gg), robustes=int((gg[f"{pre}robustesse"] == "robuste").sum()),
                        robustes_P13=int((gg[f"{pre}robustesse_P13"] == "robuste").sum()),
                        communes_sans_point_formel=int(gg.communes_sans_point_formel.sum()),
                        pop_communes_sans_point_formel=int(gg.pop_communes_sans_point_formel.sum()),
                        communes_critiques_O4_06=int(gg.communes_critiques_O4_06.fillna("").map(lambda v: len(v.split(", ")) if v else 0).sum()),
                        pop_communes_critiques=int(gg.pop_communes_critiques.sum()),
                        population=int(gg.pop_totale.sum()), part_population_pct=round(100 * gg.pop_totale.sum() / base.pop_totale.sum(), 1),
                        prefectures_noms=", ".join(gg.nom)))
R["synthese_classes"] = pd.DataFrame(syn)
R["sensibilite_tests"] = pd.concat([pd.DataFrame(meta3).assign(lecture="3 dimensions", extreme_retire=f"{ext3[0]} ({ext3[1]})"),
                                    pd.DataFrame(meta2).assign(lecture="sans couverture", extreme_retire=f"{ext2[0]} ({ext2[1]})")])
R["regles_score"] = pd.DataFrame([
    dict(regle="dimensions du score principal", valeur=" ; ".join(dims3)),
    dict(regle="fusion H6", valeur="aucune (aucune corrélation au-dessus de 0,7)" if FUSION is None else f"{FUSION[0]} + {FUSION[1]}"),
    dict(regle="préfectures classées (3 dimensions)", valeur=str(len(base3))),
    dict(regle="préfectures hors classement (couverture non déterminable, A13)", valeur=", ".join(t[t.couverture_nd].nom)),
    dict(regle="territoire extrême retiré (3 dimensions)", valeur=f"{ext3[0]} ({ext3[1]})"),
    dict(regle="territoire extrême retiré (sans couverture)", valeur=f"{ext2[0]} ({ext2[1]})")])

# ----------------------------------------------------------------- Contrôle : communes signalées par le 06 (section 9)
dist = lire(SPA, "s5_communes_sans_guichet_distance")
lisa = lire(SPA, "s7_lisa_communes")
faibles = set(lisa[lisa.grappe == "faible entouré de faibles"].code)
cumul = dist[(dist.mediane_km_guichet > 10) & dist.code.isin(faibles)]
assert sorted(cumul.nom) == ["Akébou 2", "Dankpen 2", "Kpendjal 1", "Kpendjal 2", "Kéran 2"], sorted(cumul.nom)
ctl = pd.concat([cumul[["code", "nom"]].assign(signal="cumul de trois signaux (06, section 9)"),
                 com[crit][["code", "nom"]].assign(signal="cellule critique O4-06 (07)")])
ctl = ctl.merge(com[["code", "prefecture_code", "pop_totale"]], on="code").merge(
    s[["code", "nom", "classe_retenue", "robustesse", "sans_couv_classe"]].rename(columns={"code": "prefecture_code", "nom": "prefecture"}),
    on="prefecture_code")
R["controle_communes_signalees"] = ctl.drop(columns="prefecture_code")

for nom, df in R.items():
    df.to_csv(SORTIE / f"{nom}.csv", index=False, encoding="utf-8")
print(f"{len(R)} tables écrites dans {SORTIE.relative_to(RACINE)}")
