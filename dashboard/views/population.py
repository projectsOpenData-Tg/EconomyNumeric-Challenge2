"""Page 4 — Population et offre : « Combien d’habitants par point, et où le mobile money est-il seul ? » (objectif 4 ; plan
visuel, section 7, page 4).

Refaite le 28/09/2026 (relevé des objectifs 4 et 5, `workspace/conding-progress.md`, décisions V14 à V19, étape 1) : quatre
sous-onglets, comme les pages des objectifs 1 à 3. Une « Vue synthèse », puis un onglet par composante de l’objectif :
habitants par point de service ; agents mobile money par agence et territoires où le mobile money est seul ; statut d’accès
croisé avec la couverture. Le seuil d’habitants par agence reste déplaçable (section 6) : bascule d’un seuil déjà calculé,
pas un recalcul de l’indicateur.

Les cartes et les tableaux par territoire suivent les filtres de la barre latérale, maille comprise (correction C8). Les
valeurs des tables (classes, statuts, couverture) passent par `valeur()` : elles s’affichent en anglais (correction C9).
"""
import html

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from composants import (ariane, carte_kpi, carte_valeur, colorer_regions, constat, couleur_region, entete, export_csv, habiller,
                        limite, note, onglets, pct, pied, rangee_kpi, synthese, titre_bloc, tracer)
from donnees import REGIONS, communes, contours, filtrer_communes, filtrer_prefectures, lire, nombre, prefectures
from i18n import bi, langue, region, t, valeur
from theme import BLEUS, CATEGORIELLE, OCRE, STATUT_O4_05

FR = langue() == "fr"
ROUGE_FONCE = "#8a1c1b"

# ----------------------------------------------------------------- Filtres de la barre latérale (correction C8)
f = {"regions": st.session_state.f_regions, "priorites": st.session_state.f_priorites, "milieux": st.session_state.f_milieux}
maille = st.session_state.get("f_maille") or "Préfecture"
par_commune = maille == "Commune"
maille_txt = bi(maille.lower(), {"Commune": "commune", "Préfecture": "prefecture"}[maille])
cle_maille = "commune" if par_commune else "préfecture"
C = communes()
Cf = filtrer_communes(C, f)
Pf = filtrer_prefectures(prefectures(), f)
regions_vues = f["regions"] or REGIONS

# ----------------------------------------------------------------- Tables (lectures en cache, aucun recalcul d’indicateur)
o4p = lire("07_indicateurs", "o4_prefectures")
o4r = lire("07_indicateurs", "o4_unites_regionales")
classes = lire("07_indicateurs", "o4_synthese_classes")
uemoa = lire("07_indicateurs", "o4_02_national_uemoa")
densites = lire("07_indicateurs", "o4_02_densites")
dens_reg = lire("06_spatial", "s3_unites_regionales").set_index("code")
cellules = lire("07_indicateurs", "o4_06_cellules")
couv = lire("07_indicateurs", "o2_06_couverture")
matrice = lire("07_indicateurs", "o4_06_matrice_communes")
div = lire("07_indicateurs", "p2_divergence_communes")
div_synth = lire("07_indicateurs", "p2_divergence_synthese").set_index("indicateur")
dist22 = lire("06_spatial", "s5_communes_sans_guichet_distance")
voisins = lire("06_spatial", "s7_communes_sans_guichet_voisinage").set_index("code")
dist_reg = lire("06_spatial", "s5_distances_unites").set_index("code")
diversite = lire("05_eda", "s5_diversite_types")
spearman = lire("05_eda", "s6_correlations_spearman")

# ----------------------------------------------------------------- Chiffres partagés entre onglets
og, fg = bi("« ", "“"), bi(" »", "”")
sans_agence = C[C.n_formels == 0]
suppl = C[C.classe_O4_03 == "suppléance quasi totale"]
insuffisant = C[C.classe_O4_04 == "maillage insuffisant"]
crit = C[C.cellule_critique]


def classe(maille_: str, ind: str, cl: str) -> pd.Series:
    return classes[(classes.maille == maille_) & (classes.indicateur == ind) & (classes.classe == cl)].iloc[0]


suppl_c = classe("commune", "O4_03", "suppléance quasi totale")
seul_c = classe("commune", "O4_01", "non défini et critique (0 point)")
loin = dist22[dist22.mediane_km_guichet > 10]
agences_uemoa = uemoa[uemoa.mesure.str.startswith("Agences")].iloc[0]
dab_uemoa = uemoa[uemoa.mesure.str.startswith("DAB")].iloc[0]
banques_p = densites[(densites.maille == "préfecture") & (densites.type == "banques")]
sous_uemoa = int((banques_p.pour_10k_adultes < banques_p.repere_uemoa_10k).sum())
nat_dist = dist_reg.loc["national"]
divergentes = div_synth.loc["au_moins_une"]


def en(coul: str, txt: str) -> str:
    return f'<strong style="color:{coul}">{txt}</strong>'


def etiquette_region(nom: str) -> str:
    return f'<span style="color:{couleur_region(nom)}"><b>{html.escape(region(nom))}</b></span>'


def repartition(ind: str, ordre: list[str]) -> str:
    """« Communes : maillage dense 87 (78,9 % de la population) · … » pour la maille de la barre latérale, lu dans la table."""
    lignes = classes[(classes.maille == cle_maille) & (classes.indicateur == ind)].set_index("classe")
    morceaux = [bi(f"{valeur(c)} : {int(lignes.loc[c, 'territoires'])} ({pct(lignes.loc[c, 'part_population_pct'])} de la population)",
                   f"{valeur(c)}: {int(lignes.loc[c, 'territoires'])} ({pct(lignes.loc[c, 'part_population_pct'])} of the population)")
                for c in ordre if c in lignes.index]
    return bi(f"Au niveau national, {'communes' if par_commune else 'préfectures'} : ", f"Nationally, {'communes' if par_commune else 'prefectures'}: ") + " · ".join(morceaux)


def territoires() -> tuple[dict, pd.DataFrame]:
    """Contours et table des indicateurs de l’objectif 4 à la maille de la barre latérale, filtrés."""
    if par_commune:
        return contours("communes"), C[C.code.isin(Cf.code)].copy()
    return contours("prefectures"), o4p[o4p.code.isin(Pf.code)].copy()


# Classes en couleur : bien servi en bleu foncé, manque en ocre, absence en rouge ; les 66 communes « mobile money dominant »
# ont la même couleur (violet) sur la carte des agents par agence et sur celle du statut, les 22 « mobile money seul » aussi (rouge)
CL_O4_01 = ["bien desservi", "tendu", "sous-desservi", "non défini et critique (0 point)"]
CL_O4_03 = ["réseaux comparables", "mobile money prépondérant", "suppléance quasi totale", "mobile money uniquement (0 point formel)"]
COUL_O4_03 = dict(zip(CL_O4_03, [CATEGORIELLE[0], OCRE, STATUT_O4_05["mobile money dominant"], STATUT_O4_05["mobile money uniquement"]]))
CL_O4_04 = ["maillage dense", "acceptable", "maillage insuffisant"]
COUL_O4_04 = dict(zip(CL_O4_04, [BLEUS[4], BLEUS[2], OCRE]))
CL_O4_05 = ["desserte diversifiée", "desserte faible", "mobile money dominant", "mobile money uniquement"]

# ----------------------------------------------------------------- En-tête (commun aux onglets)
ariane(t("page.population"))
entete(t("page.population"), bi("Combien d’habitants par point, et où le mobile money est-il seul ?",
                                "How many people per service point, and where is mobile money the only option?"),
       bi(f"<strong>{len(sans_agence)} communes</strong> n’ont aucune agence financière (banque, microfinance ou assurance) ; "
          f"<strong>{len(suppl)} communes</strong> n’ont presque que le mobile money.",
          f"<strong>{len(sans_agence)} communes</strong> have no financial branch at all (bank, microfinance or insurance); "
          f"<strong>{len(suppl)} communes</strong> have almost only mobile money."))
st.markdown(f'<div class="filtres-actifs">{html.escape(bi(f"Les cartes et les tableaux par territoire suivent les filtres de la barre latérale, maille comprise (ici : {maille_txt}). Les chiffres clés et la comparaison avec l’UEMOA sont nationaux.", f"Maps and tables by territory follow the sidebar filters, scale included (here: {maille_txt}). Key figures and the WAEMU comparison are national."))}</div>',
            unsafe_allow_html=True)

LIBELLES = [bi("Vue synthèse", "Overview"), bi("Habitants par point de service", "People per service point"),
            bi("Agents par agence et mobile money seul", "Agents per branch and mobile money only"),
            bi("Statut et couverture", "Status and coverage")]
o_synth, o_hab, o_agents, o_statut = onglets("population_onglets", LIBELLES)


def renvoi(i: int) -> str:
    return f" <i>({bi('détail : onglet', 'details: tab')} {og}{LIBELLES[i]}{fg})</i>"


# =================================================================== 1. Vue synthèse
if o_synth.open is not False:
    with o_synth:
        rangee_kpi(bi("L’accès aux points de service en quatre chiffres (national)", "Access to service points in four figures (national)"), [
            carte_kpi(bi("Sans agence financière", "No financial branch"), str(len(sans_agence)),
                      bi("communes sans banque, microfinance ni assurance : le mobile money y est seul",
                         "communes with no bank, microfinance or insurer: mobile money is the only option there"),
                      bi(f"{nombre(int(sans_agence.pop_totale.sum()))} habitants ; {len(loin)} à plus de 10 km d’une agence",
                         f"{nombre(int(sans_agence.pop_totale.sum()))} people; {len(loin)} over 10 km from a branch"), "",
                      t("priorite.absolue"), "critique"),
            carte_kpi(bi("Le mobile money supplée", "Mobile money fills the gap"), str(len(suppl)),
                      bi("communes où le mobile money remplace presque les agences", "communes where mobile money almost replaces branches"),
                      bi(f"plus de 20 points mobile money par agence financière ; {pct(suppl_c.part_population_pct)} de la population",
                         f"over 20 mobile money points per financial branch; {pct(suppl_c.part_population_pct)} of the population"),
                      bi("Des lieux, pas des agents : le nombre d’agents est plus élevé.", "Places, not agents: the number of agents is higher."),
                      None, "alerte"),
            carte_kpi(bi("Trop peu de points mobile money", "Too few mobile money points"), str(len(insuffisant)),
                      bi("communes où un point mobile money sert plus de 5 000 habitants", "communes where one mobile money point serves over 5,000 people"),
                      ", ".join(insuffisant.nom), "", None, "alerte"),
            carte_kpi(bi("Mobile money et réseau faible", "Mobile money and weak network"), str(len(crit)),
                      bi("communes où le mobile money est seul ou dominant et le réseau faible",
                         "communes where mobile money is alone or dominant and the network weak"),
                      t("lib.couverture_theorique").capitalize() + bi(" du réseau sous 50 %", " of the network below 50%"),
                      bi("À confirmer : la couverture est estimée, pas mesurée.", "To confirm: coverage is estimated, not measured."),
                      bi("À confirmer", "To confirm"), "neutre"),
        ])
        st.write("")
        constat(bi("Le mobile money est partout, l’agence financière non. Et la préfecture cache les communes : deux communes sur trois ne "
                   "sont pas dans la classe de leur préfecture.",
                   "Mobile money is everywhere, the financial branch is not. And the prefecture hides the communes: two communes out of "
                   "three are not in their prefecture’s class."))
        synthese(str(len(suppl)), bi(f"communes, {pct(suppl_c.part_population_pct)} de la population : le mobile money y remplace presque les agences",
                                     f"communes, {pct(suppl_c.part_population_pct)} of the population: mobile money almost replaces branches there"), [
            bi(f"{len(sans_agence)} communes n’ont aucune agence ({pct(seul_c.part_population_pct)} de la population) ; le mobile money a un "
               f"maillage dense pour {pct(classe('commune', 'O4_04', 'maillage dense').part_population_pct)} des habitants. Le Togo dépasse la "
               f"moyenne de l’UEMOA en agences bancaires, mais {sous_uemoa} préfectures sur 39 sont en dessous.",
               f"{len(sans_agence)} communes have no branch ({pct(seul_c.part_population_pct)} of the population); mobile money has a dense "
               f"network for {pct(classe('commune', 'O4_04', 'maillage dense').part_population_pct)} of residents. Togo exceeds the WAEMU "
               f"average in bank branches, but {sous_uemoa} prefectures out of 39 fall below it.") + renvoi(1),
            bi(f"Dans {len(loin)} des {len(dist22)} communes sans agence ({nombre(int(loin.pop_totale.sum()))} habitants), les points mobile "
               f"money sont à plus de 10 km d’une agence ; jusqu’à {nombre(dist22.mediane_km_guichet.max(), 1)} km ({dist22.loc[dist22.mediane_km_guichet.idxmax(), 'nom']}).",
               f"In {len(loin)} of the {len(dist22)} communes with no branch ({nombre(int(loin.pop_totale.sum()))} people), mobile money points "
               f"are over 10 km from a branch; up to {nombre(dist22.mediane_km_guichet.max(), 1)} km ({dist22.loc[dist22.mediane_km_guichet.idxmax(), 'nom']}).") + renvoi(2),
            bi(f"{len(crit)} communes cumulent mobile money seul ou dominant et réseau faible ({nombre(int(crit.pop_totale.sum()))} habitants, à "
               f"confirmer) ; {int(divergentes.communes_divergentes)} communes sur {len(C)} ne sont pas dans la classe de leur préfecture.",
               f"{len(crit)} communes combine mobile money alone or dominant with a weak network ({nombre(int(crit.pop_totale.sum()))} people, "
               f"to confirm); {int(divergentes.communes_divergentes)} communes out of {len(C)} are not in their prefecture’s class.") + renvoi(3),
        ])
        limite(bi("Recensement de 2021/2022 et population de 2022 : des lieux, pas des agents. Population résidente, pas fréquentation : le "
                  "Grand Lomé attire, de jour, plus de monde qu’il n’en loge. La couverture est théorique.",
                  "2021/2022 survey and 2022 population: places, not agents. Resident population, not footfall: Greater Lomé draws more "
                  "people by day than it houses. Coverage is theoretical."))

# =================================================================== 2. Habitants par point de service
if o_hab.open is not False:
    with o_hab:
        constat(bi(f"Le mobile money est dense presque partout ; l’agence financière manque d’abord dans les campagnes : "
                   f"{len(sans_agence)} communes n’en ont aucune.",
                   f"Mobile money is dense almost everywhere; financial branches are missing first in the countryside: "
                   f"{len(sans_agence)} communes have none."))
        gauche, droite = st.columns(2, gap="large")
        with gauche:
            with st.container(border=True):
                titre_bloc(bi("Habitants par agence financière", "People per financial branch"),
                           bi(f"Par {maille_txt} : moins de 10 000 = bien desservi ; 10 000 à 30 000 = tendu ; plus de 30 000 = sous-desservi.",
                              f"Per {maille_txt}: under 10,000 = well served; 10,000 to 30,000 = stretched; over 30,000 = under-served."))
                s1, s2 = st.slider(bi("Seuils (valeur de référence : 10 000 et 30 000)", "Thresholds (reference: 10,000 and 30,000)"),
                                   1000, 60000, (10000, 30000), step=1000, key="seuil_formel")
                COUL_SEUIL = [BLEUS[4], BLEUS[2], OCRE, ROUGE_FONCE]

                def classer(x):
                    if pd.isna(x):
                        return 3
                    return 0 if x <= s1 else (1 if x <= s2 else 2)
                geo, terr = territoires()
                terr["_rang"] = terr.hab_par_point_formel.map(classer)
                lib_cl, lib_hab = bi("classe", "class"), bi("habitants par agence", "people per branch")
                terr[lib_cl] = terr._rang.map(lambda i: valeur(CL_O4_01[i]))
                terr[lib_hab] = terr.hab_par_point_formel.round(0)
                carte_valeur(geo, terr.sort_values("_rang"), f"carte_hab_formel_{maille}", lib_cl, lib_cl, categorique=True, hauteur=560,
                             couleurs_categorie={valeur(c): coul for c, coul in zip(CL_O4_01, COUL_SEUIL)}, hover_extra={lib_hab: ":,.0f"})
                if (s1, s2) != (10000, 30000):
                    note(bi(f"Vous regardez une variante : la référence est 10 000 et 30 000 (médiane des communes : "
                            f"{nombre(C.hab_par_point_formel.median(), 0)} habitants par agence).",
                            f"You are viewing a variant: the reference is 10,000 and 30,000 (commune median: "
                            f"{nombre(C.hab_par_point_formel.median(), 0)} people per branch)."))
                else:
                    note(repartition("O4_01", CL_O4_01))
                export_csv(terr[["code", "nom", "hab_par_point_formel", "classe_O4_01"]], f"habitants_par_agence_{cle_maille}.csv", "export_hab_formel")
        with droite:
            with st.container(border=True):
                titre_bloc(bi("Habitants par point mobile money", "People per mobile money point"),
                           bi(f"Par {maille_txt} : moins de 1 000 = maillage dense ; 1 000 à 5 000 = acceptable ; plus de 5 000 = insuffisant.",
                              f"Per {maille_txt}: under 1,000 = dense network; 1,000 to 5,000 = acceptable; over 5,000 = insufficient."))
                geo, terr = territoires()
                lib_mm = bi("habitants par point mobile money", "people per mobile money point")
                terr[lib_cl] = terr.classe_O4_04.map(valeur)
                terr[lib_mm] = terr.hab_par_point_mm.round(0)
                terr["_rang"] = terr.classe_O4_04.map(CL_O4_04.index)
                carte_valeur(geo, terr.sort_values("_rang"), f"carte_hab_mm_{maille}", lib_cl, lib_cl, categorique=True, hauteur=560,
                             couleurs_categorie={valeur(c): coul for c, coul in COUL_O4_04.items()}, hover_extra={lib_mm: ":,.0f"})
                note(repartition("O4_04", CL_O4_04))
                export_csv(terr[["code", "nom", "hab_par_point_mm", "classe_O4_04"]], f"habitants_par_point_mm_{cle_maille}.csv", "export_hab_mm")

        st.write("")
        with st.container(border=True):
            titre_bloc(bi("Densité : le Togo face à l’UEMOA, et les régions face au Grand Lomé", "Density: Togo against WAEMU, and the regions against Greater Lomé"),
                       bi("Agences bancaires et distributeurs de billets pour 100 000 adultes (2024), repère des 8 pays de l’UEMOA ; points par "
                          "région rapportés aux adultes et à la superficie.",
                          "Bank branches and cash machines per 100,000 adults (2024), benchmark of the 8 WAEMU countries; points by region "
                          "relative to adults and to area."))
            # Repère UEMOA sur une rangée, puis le tableau des régions en pleine largeur
            rangee_kpi("", [
                carte_kpi(bi("Agences bancaires", "Bank branches"), nombre(agences_uemoa.togo, 2),
                          bi("pour 100 000 adultes au Togo", "per 100,000 adults in Togo"),
                          bi(f"moyenne de l’UEMOA : {nombre(agences_uemoa.moyenne_uemoa, 2)}", f"WAEMU average: {nombre(agences_uemoa.moyenne_uemoa, 2)}"),
                          bi("Banques seulement : aucun repère pour la microfinance ni les assurances.",
                             "Banks only: no benchmark for microfinance or insurers."),
                          bi("Au-dessus", "Above") if agences_uemoa.togo > agences_uemoa.moyenne_uemoa else bi("En dessous", "Below"), "ok"),
                carte_kpi(bi("Distributeurs de billets", "Cash machines"), nombre(dab_uemoa.togo, 2),
                          bi("pour 100 000 adultes au Togo", "per 100,000 adults in Togo"),
                          bi(f"moyenne de l’UEMOA : {nombre(dab_uemoa.moyenne_uemoa, 2)}", f"WAEMU average: {nombre(dab_uemoa.moyenne_uemoa, 2)}"),
                          bi("Des appareils, pas des sites.", "Machines, not sites."),
                          bi("Au-dessus", "Above") if dab_uemoa.togo > dab_uemoa.moyenne_uemoa else bi("En dessous", "Below"), "ok"),
            ])
            note(bi(f"Mais {sous_uemoa} préfectures sur 39 ont moins d’agences bancaires par adulte que ce repère.",
                    f"But {sous_uemoa} prefectures out of 39 have fewer bank branches per adult than this benchmark."), forte=True)
            lignes = [c for c in dens_reg.index if dens_reg.loc[c, "nom"] in regions_vues]
            c_reg = bi("région", "region")
            tab = pd.DataFrame({
                c_reg: [region(dens_reg.loc[c, "nom"]) for c in lignes],
                bi("agences pour 1 000 km²", "branches per 1,000 km²"): [round(dens_reg.loc[c, "formels_pour_1000_km2"], 1) for c in lignes],
                bi("points mobile money pour 1 000 km²", "mobile money points per 1,000 km²"): [int(round(dens_reg.loc[c, "mm_pour_1000_km2"])) for c in lignes],
                bi("points mobile money pour 10 000 adultes", "mobile money points per 10,000 adults"): [round(dens_reg.loc[c, "mm_pour_10k_adultes"], 1) for c in lignes],
                bi("distributeurs pour 100 000 adultes", "cash machines per 100,000 adults"): [round(dens_reg.loc[c, "dab_pour_100k_adultes"], 2) for c in lignes]})
            st.dataframe(colorer_regions(tab, c_reg), hide_index=True, use_container_width=True,
                         column_config={c_reg: st.column_config.TextColumn(c_reg, width="medium")})
            gl, autres = dens_reg.loc["GL"], dens_reg.drop(index="GL")
            note(bi(f"Le Grand Lomé a {nombre(gl.formels_pour_1000_km2 / autres.formels_pour_1000_km2.max(), 0)} à "
                    f"{nombre(gl.formels_pour_1000_km2 / autres.formels_pour_1000_km2.min(), 0)} fois plus d’agences au km² que les autres régions. "
                    "Rapporté aux adultes, le mobile money de Kara et de la Centrale égale ou dépasse le sien.",
                    f"Greater Lomé has {nombre(gl.formels_pour_1000_km2 / autres.formels_pour_1000_km2.max(), 0)} to "
                    f"{nombre(gl.formels_pour_1000_km2 / autres.formels_pour_1000_km2.min(), 0)} times more branches per km² than the other regions. "
                    "Relative to adults, mobile money in Kara and Centrale matches or exceeds its level."))
            export_csv(densites, "densites_points.csv", "export_densites")
        limite(bi("Population résidente, pas fréquentation. Le repère de l’UEMOA ne porte que sur les agences bancaires et les distributeurs "
                  "(appareils), au niveau national ; ailleurs, les distributeurs sont comptés en sites. Des lieux, pas des agents.",
                  "Resident population, not footfall. The WAEMU benchmark only covers bank branches and cash machines (machines), nationally; "
                  "elsewhere, cash machines are counted as sites. Places, not agents."))

# =================================================================== 3. Agents par agence et mobile money seul
if o_agents.open is not False:
    with o_agents:
        constat(bi(f"Dans {len(suppl)} communes ({pct(suppl_c.part_population_pct)} de la population), il y a plus de 20 points mobile money "
                   f"par agence financière. Dans les {len(dist22)} communes sans agence, le mobile money est seul, et souvent loin de toute "
                   f"agence : à plus de 10 km en médiane dans {len(loin)} d’entre elles.",
                   f"In {len(suppl)} communes ({pct(suppl_c.part_population_pct)} of the population), there are over 20 mobile money points "
                   f"per financial branch. In the {len(dist22)} communes with no branch, mobile money is alone, and often far from any "
                   f"branch: over 10 km in median in {len(loin)} of them."))
        gauche, droite = st.columns([1.15, 1], gap="large")
        with gauche:
            with st.container(border=True):
                titre_bloc(bi("Agents mobile money par agence financière", "Mobile money agents per financial branch"),
                           bi(f"Points mobile money par agence, par {maille_txt} : moins de 5 = réseaux comparables ; 5 à 20 = mobile money "
                              "prépondérant ; plus de 20 = le mobile money supplée presque tout ; aucune agence = mobile money seul.",
                              f"Mobile money points per branch, per {maille_txt}: under 5 = comparable networks; 5 to 20 = mobile money "
                              "predominant; over 20 = mobile money almost fully substitutes; no branch = mobile money only."))
                geo, terr = territoires()
                lib_cl, lib_r = bi("classe", "class"), bi("points mobile money par agence", "mobile money points per branch")
                terr[lib_cl] = terr.classe_O4_03.map(valeur)
                terr[lib_r] = terr.mm_par_point_formel.round(1)
                terr["_rang"] = terr.classe_O4_03.map(CL_O4_03.index)
                carte_valeur(geo, terr.sort_values("_rang"), f"carte_mm_par_agence_{maille}", lib_cl, lib_cl, categorique=True, hauteur=560,
                             couleurs_categorie={valeur(c): coul for c, coul in COUL_O4_03.items()}, hover_extra={lib_r: ":.1f"})
                note(repartition("O4_03", CL_O4_03))
                note(bi(f"Les 6 régions sont dans la même classe : de {nombre(o4r.mm_par_point_formel.min(), 1)} à "
                        f"{nombre(o4r.mm_par_point_formel.max(), 1)} points mobile money par agence. La seule commune aux « réseaux comparables », "
                        "Blitta 2, l’est parce que son mobile money est mince, pas parce qu’elle a beaucoup d’agences.",
                        f"All 6 regions are in the same class: from {nombre(o4r.mm_par_point_formel.min(), 1)} to "
                        f"{nombre(o4r.mm_par_point_formel.max(), 1)} mobile money points per branch. The only commune with “comparable networks”, "
                        "Blitta 2, is so because its mobile money is thin, not because it has many branches."))
                export_csv(terr[["code", "nom", "mm_par_point_formel", "classe_O4_03"]], f"agents_par_agence_{cle_maille}.csv", "export_mm_agence")
        with droite:
            with st.container(border=True):
                titre_bloc(bi("Points mobile money loin d’une agence, par région", "Mobile money points far from a branch, by region"),
                           bi("Part des points mobile money dont l’agence financière la plus proche est à plus de 5 km, puis à plus de 10 km "
                              "(à vol d’oiseau).",
                              "Share of mobile money points whose nearest financial branch is over 5 km, then over 10 km away (as the crow flies)."))
                lignes = [c for c in dist_reg.index if c != "national" and dist_reg.loc[c, "nom"] in regions_vues]
                lignes = sorted(lignes, key=lambda c: dist_reg.loc[c, "part_plus_10km_guichet_pct"])
                fig = go.Figure()
                for col, lib, coul in (("part_plus_5km_guichet_pct", bi("à plus de 5 km", "over 5 km"), BLEUS[1]),
                                       ("part_plus_10km_guichet_pct", bi("à plus de 10 km", "over 10 km"), BLEUS[4])):
                    fig.add_bar(y=[etiquette_region(dist_reg.loc[c, "nom"]) for c in lignes], x=[dist_reg.loc[c, col] for c in lignes],
                                orientation="h", name=lib, marker_color=coul, marker_line_color="#ffffff", marker_line_width=2,
                                text=[pct(dist_reg.loc[c, col]) for c in lignes], textposition="outside", textfont=dict(size=10, color="#3a3935"),
                                customdata=[region(dist_reg.loc[c, "nom"]) for c in lignes],
                                hovertemplate="%{customdata} : %{x:.1f} %<extra>" + lib + "</extra>")
                tracer(habiller(fig, 380, barmode="group", xaxis=dict(ticksuffix=" %", gridcolor="#efece4", range=[0, dist_reg.part_plus_5km_guichet_pct.max() * 1.25]),
                                yaxis=dict(gridcolor="#ffffff"), margin=dict(l=10, r=10, t=10, b=10),
                                legend=dict(orientation="h", y=-0.12, yanchor="top", x=0, traceorder="normal")), "distance_regions")
                note(bi(f"Au niveau national, {pct(nat_dist.part_plus_10km_guichet_pct)} des points mobile money sont à plus de 10 km d’une agence : "
                        f"là, le mobile money est de fait le seul accès proche. {pct(nat_dist.part_plus_10km_dab_pct)} sont à plus de 10 km d’un "
                        "distributeur de billets.",
                        f"Nationally, {pct(nat_dist.part_plus_10km_guichet_pct)} of mobile money points are over 10 km from a branch: there, mobile "
                        f"money is in practice the only nearby access. {pct(nat_dist.part_plus_10km_dab_pct)} are over 10 km from a cash machine."), forte=True)
                export_csv(dist_reg.reset_index(), "distance_agence_regions.csv", "export_distance_regions")

        st.write("")
        with st.container(border=True):
            titre_bloc(bi(f"Les {len(dist22)} communes où le mobile money est seul", f"The {len(dist22)} communes where mobile money is the only option"),
                       bi("Aucune agence de banque, de microfinance ni d’assurance, et aucun distributeur de billets. Triées de la plus éloignée "
                          "d’une agence à la moins éloignée ; les communes des filtres de la barre latérale.",
                          "No bank, microfinance or insurance branch, and no cash machine. Sorted from the farthest from a branch to the "
                          "nearest; communes in the sidebar filters."))
            d = dist22[dist22.code.isin(Cf.code)].sort_values("mediane_km_guichet", ascending=False)
            c_reg = bi("région", "region")
            tab = pd.DataFrame({
                bi("commune", "commune"): d.nom, bi("préfecture", "prefecture"): d.prefecture, c_reg: d.unite_regionale.map(region),
                bi("habitants", "people"): d.pop_totale.astype(int), bi("points mobile money", "mobile money points"): d.n_mm.astype(int),
                bi("agence (km)", "branch (km)"): d.mediane_km_guichet,
                bi("au plus (km)", "at most (km)"): d.max_km_guichet,
                bi("agence à", "branch in"): d.commune_du_guichet_le_plus_proche,
                bi("voisines dotées", "served neighbours"): [bi(f"{int(voisins.loc[c, 'voisines_avec_guichet'])} sur {int(voisins.loc[c, 'voisines'])}",
                                                                                f"{int(voisins.loc[c, 'voisines_avec_guichet'])} of {int(voisins.loc[c, 'voisines'])}")
                                                                             for c in d.code]})
            st.dataframe(colorer_regions(tab, c_reg), hide_index=True, use_container_width=True,
                         column_config={c_reg: st.column_config.TextColumn(c_reg, width="medium")})
            note(bi("« Agence (km) » : distance médiane des points mobile money de la commune à l’agence la plus proche ; « au plus » : "
                    "celle du point le plus éloigné ; « agence à » : commune où se trouve cette agence, le plus souvent.",
                    "“Branch (km)”: median distance from the commune’s mobile money points to the nearest branch; “at most”: that of the "
                    "farthest point; “branch in”: commune where that branch usually is."))
            note(bi(f"{len(loin)} communes sur {len(dist22)} ({nombre(int(loin.pop_totale.sum()))} habitants) ont leurs points mobile money à plus "
                    "de 10 km d’une agence en médiane. Une voisine dotée peut rester loin : Kéran 2 a 4 voisines dotées sur 5, et une agence à "
                    f"{nombre(dist22.set_index('nom').loc['Kéran 2', 'mediane_km_guichet'], 1)} km.",
                    f"{len(loin)} communes out of {len(dist22)} ({nombre(int(loin.pop_totale.sum()))} people) have their mobile money points over "
                    "10 km from a branch in median. A served neighbour can still be far: Kéran 2 has 4 served neighbours out of 5, and a "
                    f"branch {nombre(dist22.set_index('nom').loc['Kéran 2', 'mediane_km_guichet'], 1)} km away."), forte=True)
            export_csv(d, "communes_mobile_money_seul.csv", "export_mm_seul")
        limite(bi("Des lieux, pas des agents : un lieu peut accueillir un agent de chaque opérateur, le ratio en agents est donc plus élevé. "
                  "Distances à vol d’oiseau : le trajet réel est plus long, surtout en saison des pluies. Recensement de 2021/2022.",
                  "Places, not agents: one place can host an agent of each operator, so the ratio in agents is higher. Distances as the "
                  "crow flies: the actual journey is longer, especially in the rainy season. 2021/2022 survey."))

# =================================================================== 4. Statut et couverture
if o_statut.open is not False:
    with o_statut:
        constat(bi("Deux communes sur trois ne sont pas dans la classe de leur préfecture : la préfecture cache les communes.",
                   "Two communes out of three are not in their prefecture’s class: the prefecture hides the communes."))
        gauche, droite = st.columns([0.85, 1.15], gap="large")  # le Togo est étroit : la carte cède de la largeur au tableau
        with gauche:
            with st.container(border=True):
                titre_bloc(bi("Statut d’accès financier", "Financial access status"),
                           bi(f"Par {maille_txt}. Règle en cascade : aucune agence = mobile money seul ; plus de 20 points mobile money par agence "
                              "= mobile money dominant ; les 4 types et moins de 10 000 habitants par agence = desserte diversifiée ; sinon, "
                              "desserte faible.",
                              f"Per {maille_txt}. Cascading rule: no branch = mobile money only; over 20 mobile money points per branch = mobile "
                              "money dominant; all 4 types and under 10,000 people per branch = diversified service; otherwise, weak service."))
                variante = st.toggle(bi("Variante : la desserte diversifiée l’emporte sur le mobile money dominant",
                                        "Variant: diversified service takes precedence over mobile money dominant"), key="variante_p9",
                                     help=bi("Règle de référence : une commune qui a plus de 20 points mobile money par agence financière est « mobile money "
                                             "dominant », même si elle a les 4 types (banque, microfinance, assurance, distributeur de billets) et "
                                             "moins de 10 000 habitants par agence. La variante la classe alors en « desserte diversifiée ».",
                                             "Reference rule: a commune with more than 20 mobile money points per financial branch is “mobile money "
                                             "dominant”, even if it has all 4 types (bank, microfinance, insurer, cash machine) and fewer than 10,000 "
                                             "people per branch. The variant then classes it as “diversified service”."))
                colonne = "statut_O4_05_variante_P9" if variante else "statut_O4_05"
                geo, terr = territoires()
                lib_st = bi("statut", "status")
                terr[lib_st] = terr[colonne].map(valeur)
                terr["_rang"] = terr[colonne].map(CL_O4_05.index)
                carte_valeur(geo, terr.sort_values("_rang"), f"carte_statut_{colonne}_{maille}", lib_st, lib_st, categorique=True, hauteur=560,
                             couleurs_categorie={valeur(k): v for k, v in STATUT_O4_05.items()})
                if variante:
                    bascule = C[(C.statut_O4_05 == "mobile money dominant") & (C.statut_O4_05_variante_P9 == "desserte diversifiée")]
                    note(bi(f"Variante décidée après avoir vu le résultat : affichée à côté, jamais à la place de la règle de référence. "
                            f"{len(bascule)} communes passent de « mobile money dominant » à « desserte diversifiée » "
                            f"({nombre(int(bascule.pop_totale.sum()))} habitants) : {', '.join(bascule.nom)}.",
                            f"Variant decided after seeing the result: shown alongside, never instead of the reference rule. "
                            f"{len(bascule)} communes move from “mobile money dominant” to “diversified service” "
                            f"({nombre(int(bascule.pop_totale.sum()))} people): {', '.join(bascule.nom)}."))
                else:
                    note(repartition("O4_05", CL_O4_05))
                dv = diversite[diversite.maille == "commune"].set_index("nb_types")
                note(bi(f"Seules {int(dv.loc[4, 'territoires'])} communes ont les 4 types ({pct(dv.loc[4, 'part_pop_pct'])} de la population) ; "
                        f"un habitant sur trois ({pct(dv.loc[[0, 1], 'part_pop_pct'].sum())}) vit dans une commune qui en a au plus un.",
                        f"Only {int(dv.loc[4, 'territoires'])} communes have all 4 types ({pct(dv.loc[4, 'part_pop_pct'])} of the population); "
                        f"one resident in three ({pct(dv.loc[[0, 1], 'part_pop_pct'].sum())}) lives in a commune with one type at most."))
                rho = spearman[(spearman.maille == "commune") & (spearman.x == "formels_pour_10k_hab") & (spearman.y == "mm_pour_10k_adultes")].rho_spearman.iloc[0]
                poste = C[(C.statut_O4_05 == "mobile money uniquement") & (C.statut_O4_05_variante_poste != "mobile money uniquement")]
                note(bi(f"Le mobile money complète les agences plus qu’il ne les remplace : là où il y a plus d’agences par habitant, il y a aussi "
                        f"plus de points mobile money par adulte (lien modéré, {nombre(rho, 2)} sur une échelle de 0 à 1). Si l’on comptait la "
                        f"Poste comme une agence, {' et '.join(poste.nom)} quitteraient « mobile money seul ».",
                        f"Mobile money complements branches more than it replaces them: where there are more branches per resident, there are "
                        f"also more mobile money points per adult (moderate link, {nombre(rho, 2)} on a 0 to 1 scale). If the Post Office counted "
                        f"as a branch, {' and '.join(poste.nom)} would leave “mobile money only”."))
                export_csv(terr[["code", "nom", "statut_O4_05", "statut_O4_05_variante_P9"]], f"statut_acces_{cle_maille}.csv", "export_statut")
        with droite:
            with st.container(border=True):
                titre_bloc(bi(f"Les {len(crit)} communes à double fragilité", f"The {len(crit)} doubly fragile communes"),
                           bi("Mobile money seul ou dominant, et couverture théorique sous 50 % : toujours à confirmer par une mesure.",
                              "Mobile money alone or dominant, and theoretical coverage below 50%: always to be confirmed by a measurement."))
                cc = cellules[(cellules.maille == "commune") & cellules.cellule_O4_06.str.startswith("critique") & cellules.code.isin(Cf.code)]
                cv = couv[couv.maille == "commune"].set_index("code").couverture_proxy_pct
                c_reg, c_cv = bi("région", "region"), bi("couverture (%)", "coverage (%)")
                tab = pd.DataFrame({bi("commune", "commune"): cc.nom, c_reg: cc.unite_regionale.map(region),
                                    bi("mobile money", "mobile money"): cc.statut_O4_05.map(lambda v: bi("seul", "only") if v == "mobile money uniquement" else bi("dominant", "dominant")),
                                    c_cv: cc.code.map(cv).round(1),
                                    bi("douteuse", "doubtful"): cc.couverture_douteuse_P6.map(lambda x: bi("oui", "yes") if x is True or x == "True" else ""),
                                    bi("habitants", "people"): cc.pop_totale.astype(int)})
                st.dataframe(colorer_regions(tab.sort_values(c_cv), c_reg), hide_index=True, use_container_width=True)
                note(bi("« Douteuse » : la couverture théorique est sous 10 % alors que des points mobile money y fonctionnent.",
                        "“Doubtful”: theoretical coverage is below 10% although mobile money points operate there."))
                export_csv(cc, "communes_double_fragilite.csv", "export_critiques")

        st.write("")
        with st.container(border=True):
            titre_bloc(bi("Statut et couverture théorique (communes)", "Status and theoretical coverage (communes)"),
                       bi("Habitants par case : statut d’accès en ligne, couverture théorique du réseau en colonne.",
                          "People per cell: access status in rows, theoretical network coverage in columns."))
            ordre_couv = ["territoire couvert (proxy)", "couverture partielle (proxy)", "zone blanche prioritaire (proxy)", "non déterminable (A13)"]
            m = matrice.set_index("statut_O4_05").loc[CL_O4_05, ordre_couv]
            mat = pd.DataFrame({bi("statut", "status"): [valeur(s) for s in m.index]})
            for col in ordre_couv:
                mat[valeur(col)] = [nombre(int(v)) for v in m[col]]
            st.dataframe(mat, hide_index=True, use_container_width=True)
            export_csv(matrice, "matrice_statut_couverture.csv", "export_matrice")

        st.write("")
        with st.container(border=True):
            titre_bloc(bi("Communes qui ne sont pas dans la classe de leur préfecture", "Communes not in their prefecture’s class"),
                       bi("Sur au moins une des trois mesures : habitants par agence, points mobile money par agence, habitants par point mobile money.",
                          "On at least one of the three measures: people per branch, mobile money points per branch, people per mobile money point."))
            noms_ind = {"O4_01": bi("habitants par agence", "people per branch"), "O4_03": bi("points mobile money par agence", "mobile money points per branch"),
                        "O4_04": bi("habitants par point mobile money", "people per mobile money point")}
            note(bi(f"{int(divergentes.communes_divergentes)} communes sur {len(C)} ({nombre(divergentes.population / 1e6, 2)} millions d’habitants) : ",
                    f"{int(divergentes.communes_divergentes)} communes out of {len(C)} ({nombre(divergentes.population / 1e6, 2)} million people): ")
                 + " · ".join(f"{noms_ind[k]} {int(div_synth.loc[k, 'communes_divergentes'])}" for k in noms_ind), forte=True)
            dv = div[div.diverge_au_moins_une & div.code.isin(Cf.code)]
            divt = pd.DataFrame({bi("commune", "commune"): dv.nom,
                                 bi("agences : commune", "branches: commune"): dv.classe_O4_01_commune.map(valeur),
                                 bi("agences : préfecture", "branches: prefecture"): dv.classe_O4_01_prefecture.map(valeur),
                                 bi("mobile money par agence : commune", "mobile money per branch: commune"): dv.classe_O4_03_commune.map(valeur),
                                 bi("mobile money par agence : préfecture", "mobile money per branch: prefecture"): dv.classe_O4_03_prefecture.map(valeur)})
            st.dataframe(divt, hide_index=True, use_container_width=True, height=280)
            export_csv(div, "divergence_communes_prefectures.csv", "export_divergence")
        limite(bi("Population résidente, pas fréquentation (sous-estimée pour le Grand Lomé). Couverture théorique : un rayon de 20 km autour "
                  "des antennes, toutes technologies. La classe par seuil déplaçable est une application d’affichage : elle ne remplace pas "
                  "la classe de référence. Une divergence est mesurée ; sa cause reste une hypothèse.",
                  "Resident population, not footfall (understated for Greater Lomé). Theoretical coverage: a 20 km radius around antennas, "
                  "all technologies. The movable-threshold class is a display-only application: it does not replace the reference class. "
                  "A divergence is measured; its cause remains a hypothesis."))
pied()
