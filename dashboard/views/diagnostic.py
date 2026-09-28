"""Page 7 — Diagnostic : « Pourquoi ces territoires ? » (plan visuel, section 7, page 7).

Refaite le 29/09/2026 (relevé des objectifs 4 et 5, `workspace/conding-progress.md`, étape 2) : trois sous-onglets.
« Vue d’ensemble » (carte d’identité des 10 préfectures, ce qui se répète, nature du déficit et leviers, usage d’Internet
par région) ; « Fiche de préfecture » (la phrase de diagnostic, puis les chiffres) ; « Communes signalées ».

La phrase de chaque fiche reprend la synthèse du 09 (section 7.1), réécrite dans le vocabulaire des décideurs (agence
financière, pas « point formel » ni « guichet » ; pas de sigle) et traduite. Les valeurs des tables passent par `valeur()`.
"""
import html

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from composants import (ariane, carte_kpi, carte_valeur, colorer_regions, constat, entete, export_csv, formater,
                        habiller, limite, note, onglets, pct, pied, rangee_kpi, titre_bloc, tracer)
from donnees import communes, contours, lire, nombre, prefectures
from i18n import bi, frein, region, t, valeur
from theme import BLEUS, HORS_SELECTION, STATUT_O4_05

fiches = lire("09_diagnostic", "fiches_prefectures")
signalees = lire("09_diagnostic", "communes_signalees")
internet_reg = lire("09_diagnostic", "internet_regions")
fac = lire("09_diagnostic", "facteurs_repetition").set_index("colonne")
leviers = lire("09_diagnostic", "leviers_possibles")
S = prefectures().set_index("code")

og, fg = bi("« ", "“"), bi(" »", "”")
dist = fac.loc["part_points_mm_plus_10km_guichet_pct"]
repetes = fac[fac.lecture == "se répète"]
p1_fiches = fiches[fiches.classe_retenue == "priorité 1"]

# La phrase de diagnostic de chaque préfecture (09, section 7.1), dans le vocabulaire des décideurs
PHRASE = {
    "Dankpen": ("Cumule les trois déficits ; toutes les agences sont à Dankpen 1 (41 % des habitants) ; 45 % des points mobile money sont à plus de 10 km d’une agence.",
                "Combines all three deficits; all branches are in Dankpen 1 (41% of residents); 45% of mobile money points are over 10 km from a branch."),
    "Est-Mono": ("Aucune banque, 3 agences de microfinance ; un réseau mobile money plus dense, mais loin des agences à Est-Mono 2.",
                 "No bank, 3 microfinance branches; a denser mobile money network, but far from branches in Est-Mono 2."),
    "Blitta": ("Le réseau mobile money le plus mince des préfectures classées ; un accès aux agences moyen ; Blitta 3 sans agence ni couverture fiable.",
               "The thinnest mobile money network of the ranked prefectures; average access to branches; Blitta 3 has no branch and no reliable coverage."),
    "Oti-Sud": ("Cumule les trois déficits, la couverture en tête (41 % des habitants hors couverture) ; Oti-Sud 2 couverte à 20 %.",
                "Combines all three deficits, coverage first (41% of residents outside coverage); Oti-Sud 2 covered at 20%."),
    "Kéran": ("En tête par la couverture (78,6 % des habitants hors couverture), sur des valeurs fragiles ; plus de banques que la médiane, toutes à Kéran 1.",
              "First on coverage (78.6% of residents outside coverage), on fragile values; more banks than the median, all in Kéran 1."),
    "Kpendjal-Ouest": ("Aucune banque pour une population dense ; les agences manquent, pas la proximité ; forme un bloc avec Kpendjal.",
                       "No bank for a dense population; branches are missing, not proximity; forms a block with Kpendjal."),
    "Akébou": ("Une seule agence pour 73 830 habitants ; Akébou 2 est à 30 km d’une agence.",
               "A single branch for 73,830 residents; Akébou 2 is 30 km from a branch."),
    "Kpendjal": ("Aucune agence financière ; tous les points mobile money à plus de 10 km d’une agence ; couverture inconnue ; priorité absolue.",
                 "No financial branch; all mobile money points over 10 km from a branch; coverage unknown; absolute priority."),
    "Mô": ("Réseau mobile money mince, à moitié tenu par Togocom seul ; 2 agences de microfinance ; couverture inconnue.",
           "Thin mobile money network, half served by Togocom alone; 2 microfinance branches; coverage unknown."),
    "Tchamba": ("Beaucoup d’agences de microfinance, une banque ; réseau mobile money mince à Tchamba 1, agences éloignées à Tchamba 2 (29 km) ; couverture inconnue.",
                "Many microfinance branches, one bank; thin mobile money network in Tchamba 1, distant branches in Tchamba 2 (29 km); coverage unknown."),
}
# Nature du déficit (09, section 7.3), leviers et actions recommandées (titres de la page Recommandations)
NATURE = [
    (bi("Cumul des trois manques", "All three gaps combined"), ["Dankpen", "Oti-Sud", "Kpendjal-Ouest"],
     bi("agences, agents mobile money, réseau (après mesure)", "branches, mobile money agents, network (after measurement)")),
    (bi("Agences d’abord : peu ou pas d’agences", "Branches first: few or no branches"), ["Akébou", "Est-Mono", "Kpendjal"],
     bi("ouvrir des agences financières, d’abord dans les communes sans agence", "open financial branches, first in communes with none")),
    (bi("Réseau mobile money mince", "Thin mobile money network"), ["Blitta", "Mô", "Tchamba"],
     bi("étendre le réseau d’agents mobile money", "extend the mobile money agent network")),
    (bi("Couverture d’abord, sur une estimation fragile", "Coverage first, on a fragile estimate"), ["Kéran"],
     bi("mesurer la couverture réelle, puis étendre le réseau ; les agences n’attendent pas", "measure actual coverage, then extend the network; branches need not wait")),
]
FACTEUR = {"part_urbaine_pct": (bi("part urbaine (%)", "urban share (%)"), 1),
           "densite_hab_km2": (bi("densité (hab./km²)", "density (people/km²)"), 0),
           "types_formels_presents": (bi("types d’établissement (sur 4)", "types of institution (of 4)"), 0),
           "banques_pour_10k_adultes": (bi("agences bancaires pour 10 000 adultes", "bank branches per 10,000 adults"), 2),
           "concentration_points_formels_pts": (bi("concentration des agences dans une commune (points)", "concentration of branches in one commune (points)"), 1),
           "part_points_mm_plus_10km_guichet_pct": (bi("mobile money à plus de 10 km d’une agence (%)", "mobile money over 10 km from a branch (%)"), 1),
           "part_points_mm_togocom_seul_pct": (bi("mobile money tenu par Togocom seul (%)", "mobile money served by Togocom alone (%)"), 1),
           "part_points_mm_deux_operateurs_pct": (bi("mobile money servi par les deux opérateurs (%)", "mobile money served by both operators (%)"), 1),
           "pct_hab_5km_agence_togocom": (bi("habitants à moins de 5 km d’une boutique Togocom (%)", "people within 5 km of a Togocom shop (%)"), 1),
           "km_fibre_enterree": (bi("fibre enterrée recensée (km)", "recorded buried fibre (km)"), 0)}
COUL_SIGNAL = {valeur("sans point formel et cellule critique"): "#e34948", valeur("sans point formel"): "#eda100",
               valeur("cellule critique"): STATUT_O4_05["mobile money dominant"]}


def deficits(txt: str) -> str:
    """« accès formel (91), couverture (proxy) (86) » → « agences financières (91), couverture (estimation) (86) »."""
    for fr_ in ("maillage mobile money", "couverture (proxy)", "accès formel"):
        txt = str(txt).replace(fr_, valeur(fr_))
    return txt.replace(" et ", bi(" et ", " and ")).replace("à égalité", bi("à égalité", "equally"))


ariane(t("page.diagnostic"))
entete(t("page.diagnostic"), bi("Pourquoi ces territoires ?", "Why these territories?"),
       bi(f"Le trait commun est la distance à l’agence : <strong>{pct(dist.mediane_priorite_1, 0)}</strong> des points mobile money "
          f"des préfectures en priorité haute sont à plus de 10 km d’une agence financière, contre {pct(dist.mediane_autres_classees, 0)} ailleurs.",
          f"The common trait is distance to a branch: <strong>{pct(dist.mediane_priorite_1, 0)}</strong> of mobile money points in "
          f"high-priority prefectures are over 10 km from a financial branch, against {pct(dist.mediane_autres_classees, 0)} elsewhere."))

LIBELLES = [bi("Vue d’ensemble", "Overview"), bi("Fiche de préfecture", "Prefecture profile"), bi("Communes signalées", "Flagged communes")]
o_ensemble, o_fiche, o_communes = onglets("diagnostic_onglets", LIBELLES)

# =================================================================== 1. Vue d’ensemble
if o_ensemble.open is not False:
    with o_ensemble:
        rangee_kpi(bi("Le diagnostic en quatre chiffres", "The diagnosis in four figures"), [
            carte_kpi(bi("Préfectures diagnostiquées", "Prefectures diagnosed"), str(len(fiches)),
                      bi(f"{len(p1_fiches)} en priorité haute et {len(fiches) - len(p1_fiches)} non classées",
                         f"{len(p1_fiches)} high priority and {len(fiches) - len(p1_fiches)} unranked"),
                      bi(f"{nombre(int(fiches.pop_totale.sum()))} habitants", f"{nombre(int(fiches.pop_totale.sum()))} people"), "", None, "neutre"),
            carte_kpi(bi("Communes signalées", "Flagged communes"), str(len(signalees)),
                      bi("sans agence, ou avec un réseau faible", "with no branch, or with a weak network"),
                      bi(f"{nombre(int(signalees.pop_totale.sum()))} habitants ; toutes rurales", f"{nombre(int(signalees.pop_totale.sum()))} people; all rural"),
                      "", None, "critique"),
            carte_kpi(bi("Facteurs qui se répètent", "Recurring factors"), f"{len(repetes)}/{len(fac)}",
                      bi("se retrouvent dans 6 ou 7 des 7 priorités hautes", "found in 6 or 7 of the 7 high priorities"),
                      bi("distance, faible part urbaine, faible densité, peu de types d’établissement",
                         "distance, low urban share, low density, few institution types"), "", None, "neutre"),
            carte_kpi(bi("Distance à l’agence", "Distance to a branch"), pct(dist.mediane_priorite_1, 0),
                      bi("des points mobile money à plus de 10 km d’une agence", "of mobile money points over 10 km from a branch"),
                      bi(f"contre {pct(dist.mediane_autres_classees, 0)} dans les autres préfectures", f"against {pct(dist.mediane_autres_classees, 0)} in other prefectures"),
                      bi("Médianes ; distances à vol d’oiseau.", "Medians; distances as the crow flies."), bi("Écart marqué", "Marked gap"), "alerte"),
        ])
        st.write("")
        constat(bi(f"Le trait commun est la distance, pas l’absence de mobile money : les 10 préfectures en ont toutes, mais "
                   f"{pct(dist.mediane_priorite_1, 0)} de leurs points sont loin de toute agence, contre {pct(dist.mediane_autres_classees, 0)} ailleurs.",
                   f"The common trait is distance, not a lack of mobile money: all 10 prefectures have it, but {pct(dist.mediane_priorite_1, 0)} "
                   f"of their points are far from any branch, against {pct(dist.mediane_autres_classees, 0)} elsewhere."))

        with st.container(border=True):
            titre_bloc(bi("Carte d’identité des 10 préfectures", "Identity card of the 10 prefectures"),
                       bi("Chaque case : la valeur de la préfecture ; plus elle est foncée, plus la préfecture est parmi les plus défavorisées des 39 "
                          "sur cette mesure. Les trois premières lignes sont celles du classement.",
                          "Each cell: the prefecture’s value; the darker, the more it ranks among the least favoured of the 39 on this measure. "
                          "The first three rows are those of the ranking."))
            # Mesures en lignes (libellés lisibles, horizontaux), préfectures en colonnes
            dims = [("D1", bi("habitants par agence", "people per branch"), 0),
                    ("D2", bi("habitants par point mobile money", "people per mobile money point"), 0),
                    ("D3", bi("habitants hors couverture (estimation, %)", "people outside coverage (estimate, %)"), 1)]
            lignes_y = [lib for _, lib, _ in dims] + [lib for lib, _ in FACTEUR.values()]
            z, texte, survol = [], [], []
            for d, lib, dec in dims:
                # Préfectures non classées : leur position parmi les 39, lue à deux mesures (couverture inconnue)
                rangs = [(S.loc[c, f"{d}_rang_pct"] if not pd.isna(S.loc[c, f"{d}_rang_pct"]) or d == "D3" else S.loc[c, f"sans_couv_{d}_rang_pct"])
                         if c in S.index else None for c in fiches.code]
                valeurs = [bi("aucune agence", "no branch") if (d == "D1" and n == 0) else ("—" if pd.isna(v) else nombre(v, dec))
                           for v, n in zip(fiches[d], fiches.n_banque + fiches.n_imf + fiches.n_assurance)]
                z.append([None if r is None or pd.isna(r) else r for r in rangs])
                texte.append(valeurs)
                survol.append([f"{n} · {lib} : {v}" for n, v in zip(fiches.nom, valeurs)])
            for c, (lib, dec) in FACTEUR.items():
                valeurs = ["—" if pd.isna(v) else nombre(v, dec) for v in fiches[c]]
                z.append(list(fiches[f"{c}_rang_defavorable"]))
                texte.append(valeurs)
                survol.append([f"{n} · {lib} : {v}" for n, v in zip(fiches.nom, valeurs)])
            fig = go.Figure(go.Heatmap(z=z, x=list(fiches.nom), y=lignes_y, colorscale=[[0, "#f4f8fe"], [0.5, BLEUS[1]], [1, BLEUS[4]]],
                                       zmin=0, zmax=100, showscale=False, xgap=2, ygap=2, customdata=survol,
                                       hovertemplate="%{customdata}<extra></extra>"))
            for i_l, ligne in enumerate(texte):
                for j_c, val in enumerate(ligne):
                    zz = z[i_l][j_c]
                    fig.add_annotation(x=fiches.nom.iloc[j_c], y=lignes_y[i_l], text=val, showarrow=False,
                                       font=dict(size=10, color="#ffffff" if (zz is not None and not pd.isna(zz) and zz >= 70) else "#141413"))
            fig.add_hline(y=2.5, line_color="#ffffff", line_width=6)
            tracer(habiller(fig, 560, yaxis=dict(autorange="reversed", gridcolor="#ffffff", tickfont=dict(size=11)),
                            xaxis=dict(side="top", tickfont=dict(size=11), gridcolor="#ffffff", tickangle=0),
                            margin=dict(l=10, r=10, t=40, b=10)), "carte_identite")
            note(bi("« — » : couverture inconnue (Kpendjal, Mô, Tchamba). Foncé ne veut pas dire « en cause » : c’est une association, pas une explication.",
                    "“—”: coverage unknown (Kpendjal, Mô, Tchamba). Dark does not mean “the cause”: it is an association, not an explanation."))
            export_csv(fiches, "fiches_prefectures.csv", "export_fiches")

        st.write("")
        with st.container(border=True):
            titre_bloc(bi("Ce qui se répète", "What recurs"),
                       bi("Médiane des 7 priorités hautes face aux 29 autres préfectures classées ; « se répète » = du côté défavorable dans 6 ou 7 des 7.",
                          "Median of the 7 high priorities against the 29 other ranked prefectures; “recurs” = on the unfavourable side in 6 or 7 of the 7."))
            ft = fac.reset_index()
            tab = pd.DataFrame({bi("facteur", "factor"): ft.colonne.map(lambda c: FACTEUR[c][0] if c in FACTEUR else c),
                                bi("priorités hautes", "high priorities"): [nombre(v, FACTEUR.get(c, ("", 1))[1]) for v, c in zip(ft.mediane_priorite_1, ft.colonne)],
                                bi("autres", "others"): [nombre(v, FACTEUR.get(c, ("", 1))[1]) for v, c in zip(ft.mediane_autres_classees, ft.colonne)],
                                bi("du côté défavorable", "unfavourable side"): ft.priorite_1_du_cote_defavorable.str.replace("sur", bi("sur", "of")),
                                bi("lecture", "reading"): ft.lecture.map(valeur)})
            st.dataframe(tab, hide_index=True, use_container_width=True, height=35 * (len(tab) + 1) + 3)
            fib, tg = fac.loc["km_fibre_enterree"], fac.loc["pct_hab_5km_agence_togocom"]
            note(bi(f"Les infrastructures des opérateurs y sont plus rares : {nombre(fib.mediane_priorite_1, 0)} km de fibre enterrée en médiane, "
                    f"contre {nombre(fib.mediane_autres_classees, 0)} ailleurs ; {pct(tg.mediane_priorite_1)} des habitants à moins de 5 km d’une "
                    f"boutique Togocom, contre {pct(tg.mediane_autres_classees)}. La concurrence, elle, ne se mesure pas par territoire.",
                    f"Operators’ infrastructure is scarcer there: {nombre(fib.mediane_priorite_1, 0)} km of buried fibre in median, against "
                    f"{nombre(fib.mediane_autres_classees, 0)} elsewhere; {pct(tg.mediane_priorite_1)} of residents within 5 km of a Togocom shop, "
                    f"against {pct(tg.mediane_autres_classees)}. Competition cannot be measured by territory."))
            export_csv(fac.reset_index(), "facteurs_repetition.csv", "export_facteurs")
        st.write("")
        with st.container(border=True):
            titre_bloc(bi("Nature du manque et leviers", "Nature of the gap and levers"),
                       bi("Le manque n’a pas la même nature partout : c’est ce qui oriente l’action (page Recommandations).",
                          "The gap is not the same everywhere: that is what guides action (Recommendations page)."))
            tab = pd.DataFrame({bi("nature du manque", "nature of the gap"): [n for n, _, _ in NATURE],
                                bi("préfectures", "prefectures"): [", ".join(p) for _, p, _ in NATURE],
                                bi("levier", "lever"): [l for _, _, l in NATURE]})
            st.table(tab.set_index(bi("nature du manque", "nature of the gap")))
            note(bi("À surveiller hors des fiches : Anié (priorité moyenne ; Anié 2, 79 413 habitants, a un réseau faible) ; Tandjoaré et "
                    "Moyen-Mono, en priorité haute si l’on retire la couverture.",
                    "To watch outside the profiles: Anié (medium priority; Anié 2, 79,413 people, has a weak network); Tandjoaré and "
                    "Moyen-Mono, high priority if coverage is removed."))

        st.write("")
        with st.container(border=True):
            titre_bloc(bi("Usage d’Internet par région", "Internet use by region"),
                       bi("Le classement ne mesure pas l’usage d’Internet : il n’est connu que pour les 6 régions.",
                          "The ranking does not measure Internet use: it is only known for the 6 regions."))
            ir = internet_reg[["region", "acces_internet_2021_22_pct", "alphabetisation_2021_22_pct", "lecture_O1_06"]].rename(columns={
                "region": bi("région", "region"), "acces_internet_2021_22_pct": bi("accès déclaré à Internet (%)", "self-reported Internet access (%)"),
                "alphabetisation_2021_22_pct": bi("alphabétisation (%)", "literacy (%)"), "lecture_O1_06": bi("frein présumé", "presumed barrier")})
            ir[bi("région", "region")] = ir[bi("région", "region")].map(region)
            ir[bi("frein présumé", "presumed barrier")] = ir[bi("frein présumé", "presumed barrier")].map(frein)
            st.dataframe(colorer_regions(ir, bi("région", "region")), hide_index=True, use_container_width=True)
            export_csv(internet_reg, "internet_regions.csv", "export_internet_regions")
        limite(bi("Ce sont des associations, pas des causes démontrées. Les distances sont mesurées à vol d’oiseau, pas par la route. La "
                  "couverture est une estimation.",
                  "These are associations, not demonstrated causes. Distances are measured as the crow flies, not by road. Coverage is "
                  "an estimate."))

# =================================================================== 2. Fiche de préfecture
if o_fiche.open is not False:
    with o_fiche:
        noms = fiches.nom.tolist()
        with st.container(border=True):
            titre_bloc(bi("Fiche de préfecture", "Prefecture profile"))
            choix = st.selectbox(bi("Préfecture", "Prefecture"), noms, key="diag_prefecture")
            fi = fiches[fiches.nom == choix].iloc[0]
            phrase = PHRASE.get(fi.nom)
            if phrase:
                constat(html.escape(bi(*phrase)))
            classe = valeur(fi.classe_retenue)
            conf = valeur("non déterminable (couverture)") if str(fi.confiance_P13).startswith("non classée") else valeur(fi.confiance_P13)
            couv = bi("inconnue", "unknown") if pd.isna(fi.couverture_proxy_pct) else pct(fi.couverture_proxy_pct)
            st.markdown(
                f'<div class="reponse"><strong>{html.escape(fi.nom)}</strong> ({html.escape(region(fi.unite_regionale))}, '
                f'{nombre(int(fi.pop_totale))} {bi("habitants", "people")}) — {html.escape(classe)}, {bi("confiance", "confidence")} {html.escape(conf)}.<br>'
                f'{bi("Moteur du manque", "Main driver")} : <strong>{html.escape(valeur(fi.moteur))}</strong> ; '
                f'{bi("manques marqués", "marked gaps")} : {html.escape(deficits(fi.deficits_marques))}.<br>'
                f'{bi("Statut d’accès", "Access status")} : {html.escape(valeur(fi.statut_O4_05))} ; {bi("couverture théorique", "theoretical coverage")} {couv}.<br>'
                f'{bi("Offre", "Services")} : {fi.n_banque} {bi("banques", "banks")}, {fi.n_imf} {bi("agences de microfinance", "microfinance branches")}, '
                f'{fi.n_assurance} {bi("assurances", "insurers")}, {fi.n_dab} {bi("distributeurs de billets", "cash machines")}, '
                f'{nombre(fi.n_mm)} {bi("points mobile money", "mobile money points")}.<br>'
                f'{bi("Points mobile money à plus de 10 km d’une agence", "Mobile money points over 10 km from a branch")} : '
                f'{pct(fi.part_points_mm_plus_10km_guichet_pct)} ; {bi("fibre enterrée", "buried fibre")} : {nombre(fi.km_fibre_enterree)} km.</div>',
                unsafe_allow_html=True)
            lv = leviers[leviers.territoire == fi.nom]
            if len(lv):
                note(bi("Leviers possibles : ", "Possible levers: ") + " ; ".join(dict.fromkeys(valeur(x) for x in lv.levier_possible))
                     + bi(" (actions chiffrées : page Recommandations, onglet « Par territoire »).",
                          " (costed actions: Recommendations page, “By territory” tab)."), forte=True)
            export_csv(fiches[fiches.nom == choix], f"fiche_{fi.code}.csv", "export_fiche")
        st.write("")
        with st.container(border=True):
            pf = signalees[signalees.prefecture == choix]
            titre_bloc(bi(f"Communes signalées de {choix}", f"Flagged communes of {choix}"),
                       bi("Communes sans agence, ou avec une agence mais un réseau faible.", "Communes with no branch, or with a branch but a weak network."))
            if len(pf):
                st.dataframe(formater(pd.DataFrame({bi("commune", "commune"): pf.nom, bi("signal", "flag"): pf.signal.map(valeur),
                                           bi("habitants", "people"): pf.pop_totale.map(lambda v: nombre(v)),
                                           bi("agence la plus proche (km)", "nearest branch (km)"): pf.km_guichet_le_plus_proche_mediane.map(lambda v: nombre(v, 1)),
                                           bi("couverture théorique", "theoretical coverage"): pf.couverture_commune_pct.map(lambda v: "—" if pd.isna(v) else pct(v))})),
                             hide_index=True, use_container_width=True)
            else:
                note(bi("Aucune commune signalée dans cette préfecture.", "No flagged commune in this prefecture."))
        limite(bi("La fiche décrit ; elle n’établit pas de cause. La couverture est une estimation ; une préfecture non classée a une "
                  "couverture inconnue.", "The profile describes; it does not establish a cause. Coverage is an estimate; an unranked "
                  "prefecture has unknown coverage."))

# =================================================================== 3. Communes signalées
if o_communes.open is not False:
    with o_communes:
        sans = signalees[signalees.n_formels == 0]
        prio = sans[sans.classe_prefecture_08.isin(["priorité 1", "non déterminable (couverture)"])]
        autres = sans[sans.classe_prefecture_08.isin(["priorité 2", "priorité 3"])]
        constat(bi(f"Deux situations parmi les {len(sans)} communes sans agence. Dans les préfectures prioritaires, l’isolement : une agence à "
                   f"{nombre(prio.km_guichet_le_plus_proche_mediane.min(), 1)} à {nombre(prio.km_guichet_le_plus_proche_mediane.max(), 1)} km. "
                   f"Ailleurs ({len(autres)} communes), l’agence est souvent dans la commune voisine : {nombre(autres.km_guichet_le_plus_proche_mediane.min(), 1)} "
                   f"à {nombre(autres.km_guichet_le_plus_proche_mediane.max(), 1)} km, et le réseau est là.",
                   f"Two situations among the {len(sans)} communes with no branch. In priority prefectures, isolation: a branch "
                   f"{nombre(prio.km_guichet_le_plus_proche_mediane.min(), 1)} to {nombre(prio.km_guichet_le_plus_proche_mediane.max(), 1)} km away. "
                   f"Elsewhere ({len(autres)} communes), the branch is often in the neighbouring commune: {nombre(autres.km_guichet_le_plus_proche_mediane.min(), 1)} "
                   f"to {nombre(autres.km_guichet_le_plus_proche_mediane.max(), 1)} km, and the network is there."))
        gauche, droite = st.columns([0.9, 1.1], gap="large")
        with gauche:
            with st.container(border=True):
                titre_bloc(bi(f"Les {len(signalees)} communes signalées", f"The {len(signalees)} flagged communes"))
                lib_s = bi("signal", "flag")
                # Les autres communes en gris clair, pour garder le contour du pays
                autres_c = communes()[~communes().code.isin(signalees.code)][["code", "nom"]].assign(**{lib_s: bi("autres communes", "other communes")})
                carte = pd.concat([signalees[["code", "nom"]].assign(**{lib_s: signalees.signal.map(valeur)}), autres_c])
                carte_valeur(contours("communes"), carte, "carte_signalees", lib_s, lib_s, categorique=True, hauteur=560,
                             couleurs_categorie={**COUL_SIGNAL, bi("autres communes", "other communes"): HORS_SELECTION})
                export_csv(signalees, "communes_signalees.csv", "export_signalees")
        with droite:
            with st.container(border=True):
                titre_bloc(bi("La liste", "The list"), bi("De la plus éloignée d’une agence à la moins éloignée.", "From farthest from a branch to nearest."))
                c_reg = bi("région", "region")
                sg = signalees.sort_values("km_guichet_le_plus_proche_mediane", ascending=False, na_position="last")
                tab = pd.DataFrame({bi("commune", "commune"): sg.nom, c_reg: sg.unite_regionale.map(region), bi("signal", "flag"): sg.signal.map(valeur),
                                    bi("habitants", "people"): sg.pop_totale.astype(int),
                                    bi("agence (km)", "branch (km)"): sg.km_guichet_le_plus_proche_mediane})
                st.dataframe(colorer_regions(tab, c_reg), hide_index=True, use_container_width=True, height=520)
                note(bi("Les communes sans agence sont en priorité absolue, quelle que soit la priorité de leur préfecture.",
                        "Communes with no branch are an absolute priority, whatever their prefecture’s priority."), forte=True)
        limite(bi("Distances à vol d’oiseau, en médiane des points mobile money de la commune. Réseau faible : couverture théorique sous 50 %, à "
                  "confirmer par une mesure.", "Distances as the crow flies, median of the commune’s mobile money points. Weak network: theoretical "
                  "coverage below 50%, to be confirmed by a measurement."))
pied()
