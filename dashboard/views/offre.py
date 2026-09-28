"""Page 3 — Offre financière : « Où sont les établissements financiers ? » (objectif 3 ; plan visuel, section 7, page 3).

Refaite le 28/09/2026 (relevé de l’objectif 3, `workspace/conding-progress.md`, décisions V10 à V13) : quatre sous-onglets,
comme les pages Usage d’Internet et Marché des télécoms. Une « Vue synthèse », puis les trois vues que le 07 prévoyait pour
l’objectif 3 (offre, usage, coût), l’offre étant partagée entre les établissements financiers et le réseau mobile money.

Vocabulaire des décideurs (demande du 28/09/2026) : « agence financière » pour le point formel (agence ou guichet d’une
banque, d’une institution de microfinance ou d’une compagnie d’assurance), « distributeur de billets » pour le DAB, aucun
sigle ni nom de source sur la page (les sources et leur rôle sont sur la page Sources et méthode).

Les cartes et les tableaux par territoire suivent les filtres de la barre latérale, maille comprise (correction C5) ; les
chiffres clés, l’écart entre villes et campagnes, l’évolution du mobile money et les frais sont nationaux. Tout est lu dans
les tables du 05, du 06 et du 07, sans recalcul d’indicateur.
"""
import html

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from composants import (BLEU_FONCE, ariane, carte_kpi, carte_regions, carte_valeur, colorer_regions, constat, couleur_region, entete,
                        export_csv, habiller, limite, note, onglets, pct, pied, rangee_kpi, synthese, titre_bloc, tracer)
from donnees import REGIONS, communes, contours, filtrer_communes, filtrer_prefectures, lire, nombre, operateurs_communes, prefectures
from i18n import bi, langue, region, t
from theme import BLEUS, CATEGORIELLE, OCRE, TEXTE_CATEGORIELLE

FR = langue() == "fr"
GRIS = "#b9b6ad"
ROUGE = "#e34948"
VIOLET = "#4a3aa7"
VERT_TEXTE = "#008300"      # vert de la palette, en pas lisible sur fond blanc (celui du Maritime)
TOGOCOM_TEXTE = TEXTE_CATEGORIELLE[CATEGORIELLE[1]]   # Togocom en orange, Moov Africa en vert : les couleurs de leurs séries
MOOV_TEXTE = VERT_TEXTE
# Points mobile money : classes fixes, les mêmes aux deux mailles (une échelle continue était écrasée par Golfe, plus de
# 5 000 points) ; rampe orange, la couleur du mobile money sur la page
CLASSES_MM = [(50, bi("moins de 50", "under 50"), "#fde3cf"), (200, bi("50 à 199", "50 to 199"), "#f7b48a"),
              (500, bi("200 à 499", "200 to 499"), "#eb6834"), (1000, bi("500 à 999", "500 to 999"), "#b8460f"),
              (float("inf"), bi("1 000 et plus", "1,000 and over"), "#6e2a08")]
REPERE_FRAIS = 3            # frais d’un retrait, en % du montant : repère indicatif déclaré avant la lecture des grilles
SEUIL_DETENTION = 50        # adultes titulaires d’un compte mobile money : au-dessus, le mobile money est le canal principal

# ----------------------------------------------------------------- Filtres de la barre latérale (correction C5)
f = {"regions": st.session_state.f_regions, "priorites": st.session_state.f_priorites, "milieux": st.session_state.f_milieux}
maille = st.session_state.get("f_maille") or "Préfecture"
par_commune = maille == "Commune"
C = communes()
Cf = filtrer_communes(C, f)
Pf = filtrer_prefectures(prefectures(), f)
regions_vues = f["regions"] or REGIONS
maille_txt = bi(maille.lower(), {"Commune": "commune", "Préfecture": "prefecture"}[maille])

# ----------------------------------------------------------------- Tables (lectures en cache, aucun recalcul d’indicateur)
parts = lire("05_eda", "s2_parts_unites_regionales").set_index("code")        # parts de la population et des points, par région
strates = lire("07_indicateurs", "o3_02_strates")
s50 = strates[strates.strates.str.contains("50")].set_index("strate")         # lecture de référence : seuil de 50 % d’urbains
s75 = strates[strates.strates.str.contains("75")].set_index("strate")
regles = lire("07_indicateurs", "o3_02_regles").set_index("regle").verifiee
presence = lire("07_indicateurs", "o3_01_presence")
presence_c = lire("07_indicateurs", "o3_01_presence_communes")
presence_p = lire("07_indicateurs", "o3_01_presence_prefectures")
offre_p = lire("05_eda", "s2_offre_par_prefecture")
top = lire("05_eda", "s2_top_communes_formels")
moran = lire("06_spatial", "s7_moran_global").set_index("variable")
poles = lire("06_spatial", "s7_poles_urbains")
ops = lire("05_eda", "s2_mm_operateurs").set_index("code")
op_c = operateurs_communes()
dab = lire("05_eda", "s2_dab_emplacement").set_index("code")
mm_serie = lire("05_eda", "s4_mobile_money").set_index("annee")
findex = lire("05_eda", "s4_findex").set_index("vague")
mm_annuel = lire("07_indicateurs", "o3_04_arcep").set_index("annee")
bf = lire("07_indicateurs", "o3_04_bceao_findex").set_index("mesure").valeur
frais = lire("07_indicateurs", "o3_06_frais")
od = lire("05_eda", "s6_offre_demande_regions").set_index("code")
mb = lire("06_spatial", "s9_capacites_usage_regions")
mb = mb[mb.indicateur == "usage_mobile_banking"].copy()

# ----------------------------------------------------------------- Chiffres partagés entre onglets
og, fg = bi("« ", "“"), bi(" »", "”")
n_agences, n_mm, n_dab = int(C.n_formels.sum()), int(C.n_mm.sum()), int(C.n_dab.sum())
pop_totale = int(C.pop_totale.sum())
communes_dab = int((C.n_dab > 0).sum())
gl = parts.loc["GL"]
rural, villes, lome = s50.loc["rural"], s50.loc["autres_villes"], s50.loc["grand_lome"]
gradient_ok = bool(regles[regles.index.str.startswith("Gradient urbain : ")].iloc[0])
gradient_75_ok = bool(regles[regles.index.str.startswith("Gradient urbain, sensibilité")].iloc[0])
concentration_ok = bool(regles[regles.index.str.startswith("Concentration urbaine")].iloc[0])


def pres(maille_: str, type_: str, classe: str) -> pd.Series:
    return presence[(presence.maille == maille_) & (presence.type == type_) & (presence.classe_02 == classe)].iloc[0]


sans_assurance = pres("commune", "assurances", "absence")
sans_dab = pres("commune", "sites de DAB", "absence")
nat_dab = dab.loc["national"]
hors_gl_banque = nat_dab.dab_dans_une_banque - dab.loc["GL", "dab_dans_une_banque"]
hors_gl_total = nat_dab.total - dab.loc["GL", "total"]
part_hors_gl_banque = 100 * hors_gl_banque / hors_gl_total
mm_seul = C[C.n_formels == 0]
mm_seul_sans_dab = bool((mm_seul.n_dab == 0).all())
nat_op = ops.loc["national"]
a_bf = 2024  # comptes actifs à 90 jours : relevé de la banque centrale de 2024
taux_actifs = bf["Taux d'activité (%)"]
detention = bf[[i for i in bf.index if i.startswith("Détention")][0]]
v_fx = int(findex.index.max())
bascule_fx = int(findex[findex.compte_mobile_money > findex.compte_institution_financiere].index.min())
a_mm0, a_mm = int(mm_annuel.index.min()), int(mm_annuel.index.max())
pv = mm_serie.points_de_vente_T4.dropna()
a_pv0, a_pv = int(pv.index.min()), int(pv.index.max())
retraits = frais[frais.operation.str.startswith("retrait") & frais.montant_fcfa.notna()].sort_values("montant_fcfa")
petit, gros = retraits.iloc[0], retraits.iloc[-1]


def en(coul: str, txt: str) -> str:
    return f'<strong style="color:{coul}">{txt}</strong>'


def rg(nom: str) -> str:
    """Nom de région en couleur, dans la langue choisie."""
    return en(couleur_region(nom), html.escape(region(nom)))


def etiquette_region(nom: str) -> str:
    """Nom de région en couleur sur l’axe d’un graphique."""
    return f'<span style="color:{couleur_region(nom)}"><b>{html.escape(region(nom))}</b></span>'


STRATE = {"grand_lome": (t("milieu.Grand Lomé"), CATEGORIELLE[0], TEXTE_CATEGORIELLE[CATEGORIELLE[0]]),
          "autres_villes": (t("milieu.Autres villes"), CATEGORIELLE[1], TEXTE_CATEGORIELLE[CATEGORIELLE[1]]),
          "rural": (bi("Communes rurales", "Rural communes"), CATEGORIELLE[2], VERT_TEXTE)}

# ----------------------------------------------------------------- En-tête (commun aux onglets)
ariane(t("page.offre"))
entete(t("page.offre"), bi("Où sont les établissements financiers ?", "Where are the financial institutions?"),
       bi(f"<strong>{nombre(n_agences)} agences</strong> de banque, de microfinance ou d’assurance et <strong>{nombre(n_mm)} points "
          f"mobile money</strong>. Les communes rurales ont <strong>{pct(rural.part_points_pct)}</strong> des agences pour "
          f"{pct(rural.part_population_pct)} de la population.",
          f"<strong>{nombre(n_agences)} bank, microfinance or insurance branches</strong> and <strong>{nombre(n_mm)} mobile money "
          f"points</strong>. Rural communes have <strong>{pct(rural.part_points_pct)}</strong> of branches for "
          f"{pct(rural.part_population_pct)} of the population."))
st.markdown(f'<div class="filtres-actifs">{html.escape(bi(f"Les cartes et les tableaux par territoire suivent les filtres de la barre latérale, maille comprise (ici : {maille_txt}). Les chiffres clés, l’écart entre villes et campagnes, l’évolution du mobile money et ses frais sont nationaux.", f"Maps and tables by territory follow the sidebar filters, scale included (here: {maille_txt}). Key figures, the town-countryside gap, mobile money trends and fees are national."))}</div>',
            unsafe_allow_html=True)

LIBELLES = [bi("Vue synthèse", "Overview"), bi("Établissements financiers", "Financial institutions"),
            bi("Réseau mobile money", "Mobile money network"), bi("Usage et coût du mobile money", "Mobile money use and cost")]
o_synth, o_etab, o_reseau, o_usage = onglets("offre_onglets", LIBELLES)


def renvoi(i: int) -> str:
    return f" <i>({bi('détail : onglet', 'details: tab')} {og}{LIBELLES[i]}{fg})</i>"


def phrase_gradient() -> str:
    return bi(f"Rapportée à leur part de la population, la part des agences vaut {en(STRATE['grand_lome'][2], nombre(lome.indice_concentration, 2))} "
              f"dans le Grand Lomé, {en(STRATE['autres_villes'][2], nombre(villes.indice_concentration, 2))} dans les autres villes et "
              f"{en(STRATE['rural'][2], nombre(rural.indice_concentration, 2))} dans les communes rurales.",
              f"Relative to their share of the population, their share of branches is {en(STRATE['grand_lome'][2], nombre(lome.indice_concentration, 2))} "
              f"in Greater Lomé, {en(STRATE['autres_villes'][2], nombre(villes.indice_concentration, 2))} in other towns and "
              f"{en(STRATE['rural'][2], nombre(rural.indice_concentration, 2))} in rural communes.")


# =================================================================== 1. Vue synthèse
if o_synth.open is not False:
    with o_synth:
        rangee_kpi(bi("L’offre financière en quatre chiffres", "Financial services in four figures"), [
            carte_kpi(bi("Agences financières", "Financial branches"), nombre(n_agences),
                      bi("agences de banque, de microfinance ou d’assurance", "bank, microfinance or insurance branches"),
                      bi(f"{pct(gl.part_n_formels)} dans le Grand Lomé, pour {pct(gl.part_pop_totale)} de la population",
                         f"{pct(gl.part_n_formels)} in Greater Lomé, for {pct(gl.part_pop_totale)} of the population"),
                      bi("Recensement de 2021/2022.", "2021/2022 survey."), None, "neutre"),
            carte_kpi(bi("Points mobile money", "Mobile money points"), nombre(n_mm),
                      bi("lieux où un agent mobile money sert la clientèle", "places where a mobile money agent serves customers"),
                      bi(f"présents dans les {len(C)} communes", f"present in all {len(C)} communes"),
                      bi("Des lieux, pas des agents : un lieu peut accueillir un agent de chaque opérateur.",
                         "Places, not agents: one place can host an agent of each operator."), None, "neutre"),
            carte_kpi(bi("Assurances", "Insurance"), f"{int(sans_assurance.territoires)}/{len(C)}",
                      bi("communes sans aucune agence d’assurance", "communes with no insurance branch at all"),
                      bi(f"{nombre(sans_assurance.population / 1e6, 2)} millions d’habitants y vivent",
                         f"{nombre(sans_assurance.population / 1e6, 2)} million people live there"),
                      "", bi("Offre rare", "Scarce offer"), "alerte"),
            carte_kpi(bi("Distributeurs de billets", "Cash machines"), nombre(n_dab),
                      bi(f"dans {communes_dab} communes sur {len(C)}", f"in {communes_dab} out of {len(C)} communes"),
                      bi(f"hors du Grand Lomé, {pct(part_hors_gl_banque, 0)} sont dans une banque",
                         f"outside Greater Lomé, {pct(part_hors_gl_banque, 0)} are inside a bank"),
                      bi("Comptés à part : un distributeur dans une banque n’est pas une seconde agence.",
                         "Counted separately: a cash machine inside a bank is not a second branch."), bi("Type à part", "Separate type"), "neutre"),
        ])
        st.write("")
        constat(bi("L’écart oppose les villes aux campagnes, bien plus que Lomé aux autres villes. ",
                   "The gap sets towns against the countryside, far more than Lomé against other towns. ") + phrase_gradient())
        moran_f = moran.loc["points formels pour 10 000 habitants"]
        puces = [
            bi(f"Le Grand Lomé a {pct(gl.part_n_formels)} des agences et {pct(gl.part_n_dab)} des distributeurs de billets pour "
               f"{pct(gl.part_pop_totale)} de la population ; {int(sans_assurance.territoires)} communes n’ont aucune assurance.",
               f"Greater Lomé has {pct(gl.part_n_formels)} of branches and {pct(gl.part_n_dab)} of cash machines for "
               f"{pct(gl.part_pop_totale)} of the population; {int(sans_assurance.territoires)} communes have no insurer.") + renvoi(1),
            bi(f"Le mobile money est présent dans les {len(C)} communes. {pct(nat_op.part_mm_deux_operateurs_pct)} des points sont servis par "
               f"les deux opérateurs, mais {rg('Kara')} et la {rg('Centrale')} reposent surtout sur Togocom.",
               f"Mobile money is present in all {len(C)} communes. {pct(nat_op.part_mm_deux_operateurs_pct)} of points are served by both "
               f"operators, but {rg('Kara')} and {rg('Centrale')} rely mostly on Togocom.") + renvoi(2),
            bi(f"{pct(detention)} des adultes ont un compte mobile money, mais {pct(taux_actifs)} seulement des comptes servent ; "
               f"retirer {nombre(petit.montant_fcfa)} FCFA coûte {pct(petit.frais_pct_montant)} du montant.",
               f"{pct(detention)} of adults have a mobile money account, but only {pct(taux_actifs)} of accounts are used; "
               f"withdrawing {nombre(petit.montant_fcfa)} FCFA costs {pct(petit.frais_pct_montant)} of the amount.") + renvoi(3),
        ]
        if moran_f.p > 0.05:
            puces.insert(1, bi("Les agences ne forment pas de blocs régionaux : l’écart se joue entre chaque chef-lieu et ses campagnes, "
                               "d’où la lecture commune par commune.",
                               "Branches do not form regional blocks: the gap lies between each main town and its countryside, "
                               "hence the commune-by-commune reading.") + renvoi(1))
        synthese(pct(rural.part_points_pct),
                 bi(f"des agences financières pour {pct(rural.part_population_pct)} de la population : les communes rurales",
                    f"of financial branches for {pct(rural.part_population_pct)} of the population: rural communes"), puces)
        limite(bi("Recensement de 2021/2022 : des lieux, pas des agents ni des transactions. L’usage et le coût du mobile money ne sont "
                  "connus que pour le pays et les six régions, jamais commune par commune.",
                  "2021/2022 survey: places, not agents or transactions. Mobile money use and cost are only known for the country and "
                  "the six regions, never commune by commune."))

# =================================================================== 2. Établissements financiers
if o_etab.open is not False:
    with o_etab:
        constat(bi("L’écart oppose les villes aux campagnes, bien plus que Lomé aux autres villes. ",
                   "The gap sets towns against the countryside, far more than Lomé against other towns. ") + phrase_gradient())
        gauche, droite = st.columns([1.15, 1], gap="large")
        TYPES = {"n_banque": (bi("Banques", "Banks"), "banques"), "n_imf": (bi("Microfinance", "Microfinance"), "IMF"),
                 "n_assurance": (bi("Assurances", "Insurance"), "assurances"),
                 "n_dab": (bi("Distributeurs de billets", "Cash machines"), "sites de DAB")}
        CLASSES = {"absence": (bi("aucune", "none"), OCRE),
                   "présence marginale": (bi("1 ou 2", "1 or 2"), BLEUS[2]),
                   "présence établie": (bi("3 ou plus", "3 or more"), BLEUS[4])}
        with gauche:
            with st.container(border=True):
                titre_bloc(bi("Où sont les agences, type par type", "Where branches are, type by type"),
                           bi(f"Nombre par {maille_txt} : aucune, 1 ou 2 (présence marginale), 3 ou plus (présence établie).",
                              f"Count per {maille_txt}: none, 1 or 2 (marginal presence), "
                              "3 or more (established presence)."))
                choix = st.segmented_control(bi("Type d’établissement", "Type of institution"), list(TYPES), format_func=lambda k: TYPES[k][0],
                                             default="n_banque", key="offre_type") or "n_banque"
                if choix == "n_dab":
                    st.markdown(f'<span class="etiquette alerte">{html.escape(t("lib.type_a_part"))}</span>', unsafe_allow_html=True)
                    note(bi("Un distributeur dans une banque n’est pas une seconde agence."
                            + (f" Les {len(mm_seul)} communes où le mobile money est seul n’ont pas de distributeur non plus." if mm_seul_sans_dab else ""),
                            "A cash machine inside a bank is not a second branch."
                            + (f" The {len(mm_seul)} communes where mobile money is the only option have no cash machine either." if mm_seul_sans_dab else "")))
                if par_commune:
                    geo, terr = contours("communes"), presence_c[presence_c.code.isin(Cf.code)].copy()
                else:
                    geo, terr = contours("prefectures"), presence_p[presence_p.code.isin(Pf.code)].copy()
                lib_nb = bi("nombre", "count")
                lib_cl = bi("présence", "presence")
                terr[lib_nb] = terr[choix]
                terr[lib_cl] = terr[f"classe_{choix}"].map(lambda c: CLASSES[c][0])
                terr["_rang"] = terr[f"classe_{choix}"].map(list(CLASSES).index)
                carte_valeur(geo, terr.sort_values("_rang"), f"carte_presence_{choix}_{maille}", lib_cl, lib_cl, categorique=True,
                             couleurs_categorie={v[0]: v[1] for v in CLASSES.values()}, hover_extra={lib_nb: True}, hauteur=560)
                cle_maille = "commune" if par_commune else "préfecture"
                morceaux = []
                for c, (lib, _) in CLASSES.items():
                    r = pres(cle_maille, TYPES[choix][1], c)
                    morceaux.append(bi(f"{lib} : {int(r.territoires)} ({nombre(r.population / 1e6, 2)} M d’habitants)",
                                       f"{lib}: {int(r.territoires)} ({nombre(r.population / 1e6, 2)} M people)"))
                note(bi(f"Au niveau national, {'communes' if par_commune else 'préfectures'} : ", f"Nationally, {'communes' if par_commune else 'prefectures'}: ")
                     + " · ".join(morceaux))
                export_csv(terr.drop(columns=["_rang"]), f"presence_{cle_maille}.csv", "export_presence")

                if choix == "n_dab":
                    titre_bloc(bi("Où sont installés les distributeurs, par région", "Where cash machines are installed, by region"),
                               bi("Sites de distributeurs : dans une banque, indépendants, dans un autre établissement.",
                                  "Cash machine sites: inside a bank, stand-alone, inside another establishment."), marge=True)
                    lignes = [c for c in dab.index if c != "national" and dab.loc[c, "nom"] in regions_vues][::-1]
                    fig = go.Figure()
                    for col, lib, coul in (("dab_dans_une_banque", bi("dans une banque", "inside a bank"), BLEUS[3]),
                                           ("dab_independant", bi("indépendants", "stand-alone"), CATEGORIELLE[1]),
                                           ("dab_autre_etablissement", bi("autre établissement", "other establishment"), GRIS)):
                        fig.add_bar(y=[etiquette_region(dab.loc[c, "nom"]) for c in lignes], x=[dab.loc[c, col] for c in lignes],
                                    orientation="h", name=lib, marker_color=coul, marker_line_color="#ffffff", marker_line_width=2,
                                    customdata=[region(dab.loc[c, "nom"]) for c in lignes], hovertemplate="%{customdata} : %{x}<extra>" + lib + "</extra>")
                    tracer(habiller(fig, 300, barmode="stack", xaxis=dict(gridcolor="#efece4"), yaxis=dict(gridcolor="#ffffff"),
                                    legend=dict(orientation="h", y=1.15, x=0, traceorder="normal")), "dab_emplacement")
                    note(bi(f"Hors du Grand Lomé, {pct(part_hors_gl_banque, 0)} des distributeurs sont dans une banque : ils doublent l’agence "
                            "plus qu’ils n’étendent l’accès.",
                            f"Outside Greater Lomé, {pct(part_hors_gl_banque, 0)} of cash machines are inside a bank: they duplicate the branch "
                            "more than they extend access."), forte=True)
                    note(bi(f"{int(dab.loc['GL', 'dab_independant'])} des {int(nat_dab.dab_independant)} distributeurs indépendants sont dans le "
                            f"Grand Lomé. {int(sans_dab.territoires)} communes n’ont aucun distributeur ({pct(100 * sans_dab.population / pop_totale)} "
                            "de la population).",
                            f"{int(dab.loc['GL', 'dab_independant'])} of the {int(nat_dab.dab_independant)} stand-alone cash machines are in "
                            f"Greater Lomé. {int(sans_dab.territoires)} communes have no cash machine ({pct(100 * sans_dab.population / pop_totale)} "
                            "of the population)."))

        with droite:
            with st.container(border=True):
                titre_bloc(bi("Villes et campagnes : la part des agences face à la part de la population",
                              "Towns and countryside: share of branches against share of population"),
                           bi("Part des agences du pays divisée par la part de sa population. À 1, les agences suivent la population.",
                              "Share of the country’s branches divided by its share of the population. At 1, branches follow the population."))
                fig = go.Figure()
                cles = ["grand_lome", "autres_villes", "rural"]
                fig.add_bar(x=[STRATE[k][0] for k in cles], y=[s50.loc[k, "indice_concentration"] for k in cles],
                            marker_color=[STRATE[k][1] for k in cles], width=0.55,
                            text=[nombre(s50.loc[k, "indice_concentration"], 2) for k in cles], textposition="outside",
                            textfont=dict(size=13, color=[STRATE[k][2] for k in cles]),
                            customdata=[[pct(s50.loc[k, "part_points_pct"]), pct(s50.loc[k, "part_population_pct"])] for k in cles],
                            hovertemplate="%{x}<br>" + bi("agences : %{customdata[0]} ; population : %{customdata[1]}",
                                                         "branches: %{customdata[0]}; population: %{customdata[1]}") + "<extra></extra>")
                fig.add_hline(y=1, line_dash="dot", line_color="#8a8780", line_width=1)
                # Au-dessus de la barre la plus basse (les communes rurales), sous le trait : le libellé ne touche aucune barre
                fig.add_annotation(x=1, xref="paper", xanchor="right", y=0.97, yanchor="top", showarrow=False, align="right",
                                   font=dict(size=11, color=BLEU_FONCE),
                                   text=bi("1 = les agences<br>suivent la population", "1 = branches<br>follow the population"))
                tracer(habiller(fig, 330, showlegend=False, yaxis=dict(range=[0, 1.75], gridcolor="#efece4")), "gradient_urbain")
                note(bi(f"Écart entre villes et campagnes : {'confirmé' if gradient_ok else 'non confirmé'} "
                        f"({nombre(lome.indice_concentration, 2)} > {nombre(villes.indice_concentration, 2)} > {nombre(rural.indice_concentration, 2)})"
                        + (", aussi quand une commune n’est dite urbaine qu’au-delà de 75 % d’urbains." if gradient_75_ok else "."),
                        f"Town-countryside gap: {'confirmed' if gradient_ok else 'not confirmed'} "
                        f"({nombre(lome.indice_concentration, 2)} > {nombre(villes.indice_concentration, 2)} > {nombre(rural.indice_concentration, 2)})"
                        + (", also when a commune only counts as urban above 75% urban residents." if gradient_75_ok else ".")), forte=True)
                note(bi(f"Concentration dans le Grand Lomé : {'confirmée' if concentration_ok else 'non confirmée'}. Il a "
                        f"{pct(lome.part_points_pct)} des agences, sous le seuil de 50 %, et {pct(lome.part_population_pct)} de la population.",
                        f"Concentration in Greater Lomé: {'confirmed' if concentration_ok else 'not confirmed'}. It has "
                        f"{pct(lome.part_points_pct)} of branches, below the 50% threshold, and {pct(lome.part_population_pct)} of the population."))
                if moran.loc["points formels pour 10 000 habitants"].p > 0.05:
                    note(bi("Les agences ne forment pas de blocs régionaux : une commune bien dotée côtoie aussi souvent une commune vide "
                            "qu’une autre commune dotée. L’écart se joue entre chaque chef-lieu et ses campagnes.",
                            "Branches do not form regional blocks: a well-served commune borders an empty one as often as another "
                            "served one. The gap lies between each main town and its countryside."))
                export_csv(strates, "ecart_villes_campagnes.csv", "export_strates")

        st.write("")
        with st.container(border=True):
            titre_bloc(bi("Par région : la part des agences, des distributeurs et du mobile money face à la part de la population",
                          "By region: share of branches, cash machines and mobile money against share of the population"),
                       bi("En gris, la part de la population : une barre plus haute que la grise signale une région mieux dotée que son poids.",
                          "In grey, the share of the population: a bar taller than the grey one marks a region better served than its weight."))
            lignes = [c for c in parts.index if parts.loc[c, "nom"] in regions_vues]
            fig = go.Figure()
            for col, lib, coul in (("part_pop_totale", bi("population", "population"), GRIS),
                                   ("part_n_formels", bi("agences financières", "financial branches"), CATEGORIELLE[0]),
                                   ("part_n_dab", bi("distributeurs de billets", "cash machines"), VIOLET),
                                   ("part_n_mm", bi("points mobile money", "mobile money points"), CATEGORIELLE[1])):
                fig.add_bar(x=[etiquette_region(parts.loc[c, "nom"]) for c in lignes], y=[parts.loc[c, col] for c in lignes], name=lib,
                            marker_color=coul, marker_line_color="#ffffff", marker_line_width=2,
                            customdata=[region(parts.loc[c, "nom"]) for c in lignes],
                            hovertemplate="%{customdata} : %{y:.1f} %<extra>" + lib + "</extra>")
            tracer(habiller(fig, 360, " %", barmode="group", bargap=0.25), "parts_regions")
            imf_premier = all(parts.loc[c, "n_imf"] > max(parts.loc[c, "n_banque"], parts.loc[c, "n_assurance"]) for c in parts.index)
            regions_assurance = [c for c in parts.index if parts.loc[c, "n_assurance"] > 0]
            dix = top.head(10)
            note(bi(f"Les 10 communes les mieux dotées, dont {int((dix.unite_regionale_code == 'GL').sum())} du Grand Lomé, ont "
                    f"{pct(dix.part_cumulee_points_pct.iloc[-1])} des agences pour {pct(dix.part_cumulee_pop_pct.iloc[-1])} de la population.",
                    f"The 10 best-served communes, {int((dix.unite_regionale_code == 'GL').sum())} of them in Greater Lomé, have "
                    f"{pct(dix.part_cumulee_points_pct.iloc[-1])} of branches for {pct(dix.part_cumulee_pop_pct.iloc[-1])} of the population."), forte=True)
            note((bi("La microfinance est le premier type d’agence dans chaque région. ", "Microfinance is the leading branch type in every region. ")
                  if imf_premier else "")
                 + bi(f"Les assurances ne sont présentes que dans {len(regions_assurance)} régions : ", f"Insurers are only present in {len(regions_assurance)} regions: ")
                 + ", ".join(f"{region(parts.loc[c, 'nom'])} ({int(parts.loc[c, 'n_assurance'])})" for c in regions_assurance) + ".")
            c_reg = bi("région", "region")
            tab = pd.DataFrame({c_reg: [region(parts.loc[c, "nom"]) for c in lignes],
                                bi("population", "population"): [nombre(parts.loc[c, "pop_totale"]) for c in lignes],
                                bi("banques", "banks"): [int(parts.loc[c, "n_banque"]) for c in lignes],
                                bi("microfinance", "microfinance"): [int(parts.loc[c, "n_imf"]) for c in lignes],
                                bi("assurances", "insurance"): [int(parts.loc[c, "n_assurance"]) for c in lignes],
                                bi("agences financières", "financial branches"): [int(parts.loc[c, "n_formels"]) for c in lignes],
                                bi("distributeurs de billets", "cash machines"): [int(parts.loc[c, "n_dab"]) for c in lignes],
                                bi("points mobile money", "mobile money points"): [int(parts.loc[c, "n_mm"]) for c in lignes]})
            st.dataframe(colorer_regions(tab, c_reg), hide_index=True, use_container_width=True,
                         column_config={c_reg: st.column_config.TextColumn(c_reg, width="medium")})
            export_csv(parts.reset_index(), "parts_par_region.csv", "export_parts_regions")

        st.write("")
        with st.container(border=True):
            titre_bloc(bi("Par préfecture et par type", "By prefecture and type"),
                       bi("Les préfectures des filtres de la barre latérale.", "Prefectures in the sidebar filters."))
            pf = Cf.groupby(["prefecture", "unite_regionale"], as_index=False)[["n_banque", "n_imf", "n_assurance", "n_dab", "n_mm"]].sum()
            c_pref = bi("préfecture", "prefecture")
            pf = pf.rename(columns={"prefecture": c_pref, "unite_regionale": c_reg,
                                    "n_banque": bi("banques", "banks"), "n_imf": bi("microfinance", "microfinance"),
                                    "n_assurance": bi("assurances", "insurance"), "n_dab": bi("distributeurs de billets", "cash machines"),
                                    "n_mm": bi("points mobile money", "mobile money points")})
            pf[c_reg] = pf[c_reg].map(region)
            st.dataframe(colorer_regions(pf, c_reg), hide_index=True, use_container_width=True, height=320)
            export_csv(pf, "points_par_prefecture.csv", "export_pf_type")
        limite(bi("Recensement de 2021/2022 : l’état actuel peut différer. Des effectifs, pas des ratios : le rapport à la population est sur "
                  f"la page {og}{t('page.population')}{fg}. Une commune est dite urbaine quand plus de la moitié de ses habitants vivent en "
                  "ville ; Grand Lomé : population résidente, pas fréquentation.",
                  "2021/2022 survey: the current state may differ. Counts, not ratios: the ratio to the population is on the "
                  f"{og}{t('page.population')}{fg} page. A commune counts as urban when more than half of its residents live in a town; "
                  "Greater Lomé: resident population, not footfall."))

# =================================================================== 3. Réseau mobile money
if o_reseau.open is not False:
    with o_reseau:
        kara = ops.loc["D"]
        centrale = ops.loc["C"]
        constat(bi(f"Le mobile money est présent dans les {len(C)} communes. Deux points sur trois sont servis par les deux opérateurs, "
                   f"mais {rg('Kara')} et la {rg('Centrale')} reposent surtout sur {en(TOGOCOM_TEXTE, 'Togocom')} : "
                   f"{en(MOOV_TEXTE, 'Moov Africa')} n’y est présent que dans {en(MOOV_TEXTE, pct(kara.presence_moov_pct))} et "
                   f"{en(MOOV_TEXTE, pct(centrale.presence_moov_pct))} des points.",
                   f"Mobile money is present in all {len(C)} communes. Two points out of three are served by both operators, but "
                   f"{rg('Kara')} and {rg('Centrale')} rely mostly on {en(TOGOCOM_TEXTE, 'Togocom')}: {en(MOOV_TEXTE, 'Moov Africa')} is "
                   f"only present in {en(MOOV_TEXTE, pct(kara.presence_moov_pct))} and {en(MOOV_TEXTE, pct(centrale.presence_moov_pct))} of points."))
        gauche, droite = st.columns(2, gap="large")
        with gauche:
            with st.container(border=True):
                titre_bloc(bi("Points mobile money", "Mobile money points"),
                           bi(f"Nombre par {maille_txt}.", f"Count per {maille_txt}."))
                lib_mm = bi("points mobile money", "mobile money points")
                if par_commune:
                    geo, terr = contours("communes"), Cf[["code", "nom", "n_mm"]].copy()
                else:
                    geo, terr = contours("prefectures"), offre_p[offre_p.code.isin(Pf.code)][["code", "nom", "n_mm"]].copy()
                lib_cl_mm = bi("classe", "class")
                terr[lib_mm] = terr.n_mm
                terr["_rang"] = terr.n_mm.map(lambda n: next(i for i, (b, _, _) in enumerate(CLASSES_MM) if n < b))
                terr[lib_cl_mm] = terr._rang.map(lambda i: CLASSES_MM[i][1])
                carte_valeur(geo, terr.sort_values("_rang"), f"carte_mm_{maille}", lib_cl_mm, lib_mm, categorique=True,
                             couleurs_categorie={lib: coul for _, lib, coul in CLASSES_MM}, hover_extra={lib_mm: True}, hauteur=560)
                mini = C.loc[C.n_mm.idxmin()]
                note(bi(f"Aucune commune n’est sans point mobile money ; la moins dotée, {mini.nom}, en a {int(mini.n_mm)}.",
                        f"No commune lacks a mobile money point; the least served, {mini.nom}, has {int(mini.n_mm)}."))
                export_csv(terr[["code", "nom", "n_mm"]], f"points_mobile_money_{maille.lower()}.csv", "export_mm")
        with droite:
            with st.container(border=True):
                titre_bloc(bi("Opérateurs du mobile money", "Mobile money operators"),
                           bi(f"Catégorie la plus fréquente parmi les points de chaque {maille_txt}.",
                              f"Most frequent category among the points of each {maille_txt}."))
                CAT = {"deux": (bi("deux opérateurs", "both operators"), CATEGORIELLE[0]), "togocom": ("Togocom (YAS)", CATEGORIELLE[1]),
                       "moov": ("Moov Africa", CATEGORIELLE[2]), "nr": (bi("non renseigné", "not reported"), GRIS)}
                if par_commune:
                    op = op_c[op_c.code.isin(Cf.code)].copy()
                    cols = {"part_deux_operateurs_pct": "deux", "part_togocom_seul_pct": "togocom", "part_moov_seul_pct": "moov",
                            "part_operateur_non_renseigne_pct": "nr"}
                    geo = contours("communes")
                else:
                    op = offre_p[offre_p.code.isin(Pf.code)].copy()
                    cols = {"mm_deux_operateurs": "deux", "mm_togocom_seul": "togocom", "mm_moov_seul": "moov", "mm_operateur_non_renseigne": "nr"}
                    geo = contours("prefectures")
                lib_op = bi("opérateur", "operator")
                op[lib_op] = op[list(cols)].idxmax(axis=1).map(cols).map(lambda k: CAT[k][0])
                carte_valeur(geo, op, f"carte_operateurs_{maille}", lib_op, lib_op, categorique=True,
                             couleurs_categorie={v[0]: v[1] for v in CAT.values()}, hauteur=560)
                kara_c = op_c[op_c.unite_regionale == "Kara"].sort_values("part_operateur_non_renseigne_pct").iloc[-1]
                note(bi(f"Opérateur non renseigné pour {pct(kara.part_mm_operateur_non_renseigne_pct)} des points de la région de Kara, "
                        f"jusqu’à la moitié dans certaines communes ({kara_c.nom} : {pct(kara_c.part_operateur_non_renseigne_pct)}).",
                        f"Operator not reported for {pct(kara.part_mm_operateur_non_renseigne_pct)} of points in the Kara region, up to half "
                        f"in some communes ({kara_c.nom}: {pct(kara_c.part_operateur_non_renseigne_pct)})."))
                export_csv(op, f"operateurs_mobile_money_{maille.lower()}.csv", "export_operateurs")

        st.write("")
        with st.container(border=True):
            titre_bloc(bi("Qui sert les points mobile money, par région", "Who serves mobile money points, by region"),
                       bi("Part des points servis par les deux opérateurs, par un seul, ou sans opérateur renseigné (jamais réparti).",
                          "Share of points served by both operators, by one only, or with no reported operator (never split)."))
            lignes = ["national"] + [c for c in ops.index if c != "national" and ops.loc[c, "nom"] in regions_vues]
            noms = [bi("<b>Togo</b>", "<b>Togo</b>") if c == "national" else etiquette_region(ops.loc[c, "nom"]) for c in lignes][::-1]
            lignes = lignes[::-1]
            fig = go.Figure()
            for col, cle in (("part_mm_deux_operateurs_pct", "deux"), ("part_mm_togocom_seul_pct", "togocom"),
                             ("part_mm_moov_seul_pct", "moov"), ("part_mm_operateur_non_renseigne_pct", "nr")):
                vals = [ops.loc[c, col] for c in lignes]
                fig.add_bar(y=noms, x=vals, orientation="h", name=CAT[cle][0], marker_color=CAT[cle][1], marker_line_color="#ffffff",
                            marker_line_width=2, text=[pct(v, 0) if v >= 8 else "" for v in vals], textposition="inside",
                            insidetextanchor="middle", textfont=dict(color="#ffffff" if cle in ("deux", "togocom") else "#141413", size=11),
                            customdata=["Togo" if c == "national" else region(ops.loc[c, "nom"]) for c in lignes],
                            hovertemplate="%{customdata} : %{x:.1f} %<extra>" + CAT[cle][0] + "</extra>")
            tracer(habiller(fig, 340, barmode="stack", xaxis=dict(ticksuffix=" %", range=[0, 100], gridcolor="#efece4"),
                            yaxis=dict(gridcolor="#ffffff"), legend=dict(orientation="h", y=1.12, x=0, traceorder="normal")), "operateurs_regions")
            n_togocom = int((op_c.part_togocom_seul_pct >= 50).sum())
            note(bi(f"Dans {n_togocom} communes, Togocom seul sert la moitié des points ou plus, surtout autour de Sokodé et de Kara.",
                    f"In {n_togocom} communes, Togocom alone serves half of the points or more, mostly around Sokodé and Kara."), forte=True)
            VILLE = {"Tchaoudjo 1": "Sokodé", "Kozah 1": "Kara"}
            morceaux = [bi(f"{VILLE.get(r.pole, r.pole)} a {pct(r.part_points_mm_pct)} des points de sa préfecture pour {pct(r.part_population_pct)} de ses habitants",
                           f"{VILLE.get(r.pole, r.pole)} has {pct(r.part_points_mm_pct)} of its prefecture’s points for {pct(r.part_population_pct)} of its residents")
                        for r in poles.itertuples()]
            note(bi("Les villes hors de Lomé concentrent le mobile money de leur préfecture : ", "Towns outside Lomé concentrate their prefecture’s mobile money: ")
                 + " ; ".join(morceaux) + bi(". Les communes voisines en manquent.", ". Neighbouring communes lack it."))
            export_csv(ops.reset_index(), "operateurs_par_region.csv", "export_operateurs_regions")
        limite(bi("Recensement de 2021/2022 : des lieux, pas des agents. Un lieu servi par les deux opérateurs compte une fois ; les points "
                  "sans opérateur renseigné restent à part, jamais répartis. La catégorie affichée sur la carte ne dit pas qu’un seul "
                  "opérateur est présent, seulement laquelle est la plus fréquente.",
                  "2021/2022 survey: places, not agents. A place served by both operators counts once; points with no reported operator "
                  "stay separate, never split. The category on the map does not mean only one operator is present, only which one is "
                  "the most frequent."))

# =================================================================== 4. Usage et coût du mobile money
if o_usage.open is not False:
    with o_usage:
        constat(bi(f"Le mobile money est devenu le premier compte des adultes ({pct(detention)} en {v_fx}), sans être encore majoritaire. "
                   f"Mais la moitié des comptes ouverts dort, et le petit retrait coûte cher : "
                   f"{en(ROUGE, pct(petit.frais_pct_montant))} du montant pour {nombre(petit.montant_fcfa)} FCFA.",
                   f"Mobile money has become adults’ leading account ({pct(detention)} in {v_fx}), without yet being a majority. "
                   f"But half of opened accounts are dormant, and small withdrawals are expensive: "
                   f"{en(ROUGE, pct(petit.frais_pct_montant))} of the amount for {nombre(petit.montant_fcfa)} FCFA."))
        rangee_kpi(bi("Le mobile money en quatre chiffres (national)", "Mobile money in four figures (national)"), [
            carte_kpi(bi(f"Comptes actifs ({a_bf})", f"Active accounts ({a_bf})"), pct(taux_actifs),
                      bi("des comptes mobile money ont servi dans les 90 derniers jours", "of mobile money accounts were used in the last 90 days"),
                      bi(f"{nombre(bf[[i for i in bf.index if i.startswith('Comptes actifs')][0]] / 1e6, 2)} millions sur "
                         f"{nombre(bf[[i for i in bf.index if i.startswith('Comptes ouverts')][0]] / 1e6, 2)} millions de comptes ouverts",
                         f"{nombre(bf[[i for i in bf.index if i.startswith('Comptes actifs')][0]] / 1e6, 2)} million out of "
                         f"{nombre(bf[[i for i in bf.index if i.startswith('Comptes ouverts')][0]] / 1e6, 2)} million opened accounts"),
                      bi("Des comptes, pas des personnes : une personne peut en avoir plusieurs.",
                         "Accounts, not people: one person can hold several."),
                      bi("Usage faible", "Low activity") if taux_actifs < 50 else None, "alerte"),
            carte_kpi(bi(f"Adultes titulaires ({v_fx})", f"Adult account holders ({v_fx})"), pct(detention),
                      bi("des adultes ont un compte mobile money", "of adults have a mobile money account"),
                      bi(f"{pct(findex.loc[v_fx, 'compte_institution_financiere'])} ont un compte en banque ou en microfinance ; seuil : {SEUIL_DETENTION} %",
                         f"{pct(findex.loc[v_fx, 'compte_institution_financiere'])} have a bank or microfinance account; threshold: {SEUIL_DETENTION}%"),
                      bi("Enquête auprès des adultes de 15 ans et plus.", "Survey of adults aged 15 and over."),
                      bi("Sous le seuil", "Below threshold") if detention < SEUIL_DETENTION else bi("Canal principal", "Main channel"),
                      "alerte" if detention < SEUIL_DETENTION else "ok"),
            carte_kpi(bi(f"Transactions ({a_mm})", f"Transactions ({a_mm})"), nombre(mm_annuel.loc[a_mm, "valeur_md_fcfa"]),
                      bi("milliards de FCFA échangés par mobile money dans l’année", "billion FCFA exchanged through mobile money in the year"),
                      bi(f"× {nombre(mm_annuel.loc[a_mm, 'valeur_md_fcfa'] / mm_annuel.loc[a_mm0, 'valeur_md_fcfa'], 1)} depuis {a_mm0} ; "
                         f"{nombre(mm_annuel.loc[a_mm, 'transactions_millions'])} millions d’opérations",
                         f"× {nombre(mm_annuel.loc[a_mm, 'valeur_md_fcfa'] / mm_annuel.loc[a_mm0, 'valeur_md_fcfa'], 1)} since {a_mm0}; "
                         f"{nombre(mm_annuel.loc[a_mm, 'transactions_millions'])} million operations"),
                      bi("Une valeur totale, pas un revenu des ménages.", "A total value, not household income."), bi("En hausse", "Rising"), "ok"),
            carte_kpi(bi(f"Points de vente ({a_pv})", f"Points of sale ({a_pv})"), nombre(pv.loc[a_pv]),
                      bi("points de vente déclarés par les opérateurs", "points of sale reported by operators"),
                      bi(f"× {nombre(pv.loc[a_pv] / pv.loc[a_pv0], 1)} depuis {a_pv0}", f"× {nombre(pv.loc[a_pv] / pv.loc[a_pv0], 1)} since {a_pv0}"),
                      bi(f"Comptés par opérateur : autre mesure que les {nombre(n_mm)} lieux recensés en 2021/2022.",
                         f"Counted per operator: a different measure from the {nombre(n_mm)} places surveyed in 2021/2022."), None, "neutre"),
        ])
        st.write("")
        gauche, droite = st.columns(2, gap="large")
        with gauche:
            with st.container(border=True):
                titre_bloc(bi(f"Adultes titulaires d’un compte, {int(findex.index.min())}-{v_fx}", f"Adults holding an account, {int(findex.index.min())}-{v_fx}"),
                           bi("Adultes de 15 ans et plus, cinq vagues d’enquête ; un adulte peut avoir les deux comptes.",
                              "Adults aged 15 and over, five survey waves; an adult can hold both accounts."))
                fig = go.Figure()
                for col, lib, coul in (("compte_mobile_money", bi("compte mobile money", "mobile money account"), CATEGORIELLE[1]),
                                       ("compte_institution_financiere", bi("compte en banque ou en microfinance", "bank or microfinance account"), CATEGORIELLE[0])):
                    s = findex[col].dropna()
                    fig.add_scatter(x=list(s.index), y=list(s.values), mode="lines+markers", name=f"{lib} : {pct(s.iloc[-1])} ({int(s.index[-1])})",
                                    line=dict(color=coul, width=2), marker=dict(size=9, color=coul, line=dict(color="#ffffff", width=1.5)),
                                    hovertemplate="%{x} : %{y:.1f} %<extra>" + lib + "</extra>")
                fig.add_hline(y=SEUIL_DETENTION, line_dash="dot", line_color=ROUGE, line_width=1)
                fig.add_annotation(x=findex.index.min(), xanchor="left", y=SEUIL_DETENTION, yanchor="bottom", showarrow=False,
                                   font=dict(size=11, color=TEXTE_CATEGORIELLE[ROUGE]),
                                   text=bi(f"{SEUIL_DETENTION} % : le mobile money deviendrait le canal principal", f"{SEUIL_DETENTION}%: mobile money would become the main channel"))
                tracer(habiller(fig, 340, " %", legende_y=1.18, yaxis=dict(range=[0, 60], ticksuffix=" %", gridcolor="#efece4"),
                                xaxis=dict(tickvals=list(findex.index), gridcolor="#efece4")), "detention_comptes")
                note(bi(f"Depuis {bascule_fx}, plus d’adultes ont un compte mobile money qu’un compte en banque ou en microfinance.",
                        f"Since {bascule_fx}, more adults have a mobile money account than a bank or microfinance account."), forte=True)
                export_csv(findex.reset_index(), "detention_comptes.csv", "export_detention")
        with droite:
            with st.container(border=True):
                titre_bloc(bi(f"Valeur des transactions, {a_mm0}-{a_mm}", f"Transaction value, {a_mm0}-{a_mm}"),
                           bi("En milliards de FCFA par année ; comptes et nombre d’opérations au survol.",
                              "In billion FCFA per year; accounts and number of operations on hover."))
                fig = go.Figure()
                ans = list(mm_annuel.index)
                fig.add_bar(x=ans, y=list(mm_annuel.valeur_md_fcfa), marker_color=CATEGORIELLE[1], width=0.6,
                            text=[nombre(v) if a in (a_mm0, a_mm) else "" for a, v in zip(ans, mm_annuel.valeur_md_fcfa)], textposition="outside",
                            customdata=[[nombre(c / 1e6, 2), nombre(n)] for c, n in zip(mm_annuel.comptes_T4, mm_annuel.transactions_millions)],
                            hovertemplate="%{x} : %{y:,.0f} " + bi("milliards de FCFA", "billion FCFA") + "<br>"
                                          + bi("comptes : %{customdata[0]} millions ; opérations : %{customdata[1]} millions",
                                               "accounts: %{customdata[0]} million; operations: %{customdata[1]} million") + "<extra></extra>")
                tracer(habiller(fig, 340, showlegend=False, yaxis=dict(range=[0, mm_annuel.valeur_md_fcfa.max() * 1.18], tickformat=",.0f",
                                                                    gridcolor="#efece4"),
                                xaxis=dict(tickvals=ans, gridcolor="#ffffff")), "transactions_mm")
                note(bi(f"Les comptes passent de {nombre(mm_annuel.loc[a_mm0, 'comptes_T4'] / 1e6, 2)} à {nombre(mm_annuel.loc[a_mm, 'comptes_T4'] / 1e6, 2)} "
                        f"millions ; {nombre(mm_annuel.loc[a_mm, 'transactions_par_compte_an'], 0)} opérations par compte en {a_mm}.",
                        f"Accounts rise from {nombre(mm_annuel.loc[a_mm0, 'comptes_T4'] / 1e6, 2)} to {nombre(mm_annuel.loc[a_mm, 'comptes_T4'] / 1e6, 2)} "
                        f"million; {nombre(mm_annuel.loc[a_mm, 'transactions_par_compte_an'], 0)} operations per account in {a_mm}."))
                export_csv(mm_annuel.reset_index(), "transactions_mobile_money.csv", "export_transactions")

        # ------------------------------------------------------------- Offre et usage par région (déplacés de l’ancienne page)
        st.write("")
        pc = (lambda x: f"{nombre(x, 1)} %") if FR else (lambda x: f"{nombre(x, 1)}%")
        g_od, c_od = od.loc["GL"], od.loc["C"]
        with st.container(border=True):
            titre_bloc(bi("Offre et usage du mobile money, par région", "Mobile money supply and use, by region"),
                       bi(f"Adultes (15 ans et plus) faisant du mobile banking, enquête nationale auprès des ménages {mb.vague.iloc[0]}, avec la "
                          f"marge d’erreur à 95 % ; national : {pc(mb.national_pct.iloc[0])}.",
                          f"Adults (aged 15 and over) using mobile banking, national household survey {mb.vague.iloc[0]}, with the 95% margin "
                          f"of error; national: {pc(mb.national_pct.iloc[0])}."))
            carte_g, tableau_d = st.columns([1, 1.3], gap="large")
            with carte_g:
                mb["valeur"] = mb.estimation_pct
                marge = (mb.ic95_haut - mb.ic95_bas) / 2
                mb["etiquette"] = [f"{pc(v)}<br>(± {nombre(m, 1)})" for v, m in zip(mb.valeur, marge)]
                ic = bi("marge à 95 %", "95% margin")
                mb["survol"] = [f"<b>{region(n)}</b><br>{pc(v)} ({ic} : {nombre(lo, 1)} – {nombre(hi, 1)})"
                                for n, v, lo, hi in zip(mb.nom, mb.valeur, mb.ic95_bas, mb.ic95_haut)]
                carte_regions(mb, "carte_mobile_banking", "valeur", [20, 30, 40, 50],
                              [bi("moins de 20 %", "under 20%"), bi("20 à 30 %", "20 to 30%"), bi("30 à 40 %", "30 to 40%"),
                               bi("40 à 50 %", "40 to 50%"), bi("50 % et plus", "50% and over")], selection=f["regions"], hauteur=500)
            with tableau_d:
                # Phrase de lecture avec les noms de région en couleur : HTML, donc écrite directement (note() échappe son texte)
                st.markdown('<div class="note-graphique forte">'
                            + bi(f"À offre voisine, l’usage diffère du simple au triple : le {rg('Grand Lomé')} a {nombre(g_od.mm_pour_10k_adultes, 1)} "
                                 f"points mobile money pour 10 000 adultes et {pc(g_od.usage_mobile_banking_2021_pct)} d’usage ; la {rg('Centrale')}, "
                                 f"{nombre(c_od.mm_pour_10k_adultes, 1)} points et {pc(c_od.usage_mobile_banking_2021_pct)}.",
                                 f"With similar supply, use varies threefold: {rg('Grand Lomé')} has {nombre(g_od.mm_pour_10k_adultes, 1)} mobile money "
                                 f"points per 10,000 adults and {pc(g_od.usage_mobile_banking_2021_pct)} use; {rg('Centrale')}, "
                                 f"{nombre(c_od.mm_pour_10k_adultes, 1)} points and {pc(c_od.usage_mobile_banking_2021_pct)}.")
                            + "</div>", unsafe_allow_html=True)
                c_reg, c_off, c_use = bi("région", "region"), bi("points pour 10 000 adultes", "points per 10,000 adults"), \
                    bi("usage (%)", "use (%)")
                tab_od = pd.DataFrame({c_reg: od.unite.map(region), c_off: od.mm_pour_10k_adultes, c_use: od.usage_mobile_banking_2021_pct.round(1)})
                if f["regions"]:
                    tab_od = tab_od[od.unite.isin(f["regions"]).values]
                st.dataframe(colorer_regions(tab_od.sort_values(c_use), c_reg), hide_index=True, use_container_width=True,
                             column_config={c_reg: st.column_config.TextColumn(c_reg, width="medium"),
                                            c_use: st.column_config.ProgressColumn(c_use, min_value=0, max_value=100, format="%.1f")})
                st.caption(bi("Six régions : c’est un constat, pas une corrélation. Offre : recensement de 2021/2022 ; usage : enquête de 2021/22.",
                              "Six regions: an observation, not a correlation. Supply: 2021/2022 survey of points; use: 2021/22 household survey."))
                export_csv(od.reset_index(), "offre_usage_mobile_money_regions.csv", "export_offre_usage")

        # ------------------------------------------------------------- Frais d’un retrait
        st.write("")
        with st.container(border=True):
            titre_bloc(bi("Ce que coûte un retrait chez un agent", "What a withdrawal at an agent costs"),
                       bi(f"Frais en % du montant retiré, grille publiée par Moov Africa (Flooz) ; repère de {REPERE_FRAIS} %.",
                          f"Fees as a % of the amount withdrawn, grid published by Moov Africa (Flooz); {REPERE_FRAIS}% reference."))
            g_f, d_f = st.columns([1.2, 1], gap="large")
            with g_f:
                fig = go.Figure()
                x = [f"{nombre(m)} FCFA" for m in retraits.montant_fcfa]
                fig.add_bar(x=x, y=list(retraits.frais_pct_montant), width=0.55,
                            marker_color=[ROUGE if v > REPERE_FRAIS else BLEUS[2] for v in retraits.frais_pct_montant],
                            text=[bi(f"{nombre(fr_)} FCFA ({pct(p)})", f"{nombre(fr_)} FCFA ({pct(p)})") for fr_, p in zip(retraits.frais_fcfa, retraits.frais_pct_montant)],
                            textposition=["inside" if v >= 2 else "outside" for v in retraits.frais_pct_montant], insidetextanchor="end",
                            textangle=0, textfont=dict(size=12, color=["#ffffff" if v >= 2 else BLEU_FONCE for v in retraits.frais_pct_montant]),
                            hovertemplate=bi("retrait de %{x} : %{y:.1f} % du montant", "withdrawal of %{x}: %{y:.1f}% of the amount") + "<extra></extra>")
                fig.add_hline(y=REPERE_FRAIS, line_dash="dot", line_color=ROUGE, line_width=1)
                fig.add_annotation(x=1, xref="paper", xanchor="right", y=REPERE_FRAIS, yanchor="bottom", showarrow=False,
                                   font=dict(size=11, color=TEXTE_CATEGORIELLE[ROUGE]), text=bi(f"repère : {REPERE_FRAIS} %", f"reference: {REPERE_FRAIS}%"))
                tracer(habiller(fig, 320, " %", showlegend=False, yaxis=dict(range=[0, retraits.frais_pct_montant.max() * 1.3], ticksuffix=" %",
                                                                             gridcolor="#efece4")), "frais_retrait")
            with d_f:
                st.write("")
                note(bi(f"Plus le retrait est petit, plus il coûte cher : {pct(petit.frais_pct_montant)} du montant pour {nombre(petit.montant_fcfa)} FCFA, "
                        f"{pct(gros.frais_pct_montant)} pour {nombre(gros.montant_fcfa)} FCFA.",
                        f"The smaller the withdrawal, the more it costs: {pct(petit.frais_pct_montant)} of the amount for {nombre(petit.montant_fcfa)} FCFA, "
                        f"{pct(gros.frais_pct_montant)} for {nombre(gros.montant_fcfa)} FCFA."), forte=True)
                note(bi(f"Seul le petit retrait dépasse le repère de {REPERE_FRAIS} %. Transferts : gratuits jusqu’au 3e chez Moov Africa ; 6 par jour, "
                        "puis 1 % du montant, chez YAS (Mixx), dont la grille de retrait n’est pas publiée.",
                        f"Only the small withdrawal exceeds the {REPERE_FRAIS}% reference. Transfers: free up to the 3rd at Moov Africa; 6 a day, "
                        "then 1% of the amount, at YAS (Mixx), whose withdrawal grid is not published."))
                note(bi(f"Recommandation liée : ramener les frais du petit retrait sous {REPERE_FRAIS} % (page {og}{t('page.recommandations')}{fg}).",
                        f"Related recommendation: bring small-withdrawal fees below {REPERE_FRAIS}% ({og}{t('page.recommandations')}{fg} page)."))
                export_csv(frais, "frais_mobile_money.csv", "export_frais")
        limite(bi("Trois mesures du compte, qui ne se comparent pas : comptes actifs (relevé de la banque centrale), comptes déclarés par les "
                  "opérateurs, adultes titulaires (enquête). Les opérateurs ont révisé leurs comptes début 2021 : pas d’évolution calculée à "
                  "travers cette rupture. Frais relevés le 26/09/2026, sans historique ; le repère de 3 % est indicatif. Usage par région : six "
                  "régions ; la question a changé entre les deux vagues de l’enquête.",
                  "Three account measures that do not compare: active accounts (central bank records), accounts reported by operators, adult "
                  "holders (survey). Operators revised their account counts in early 2021: no change is computed across this break. Fees "
                  "recorded on 26/09/2026, no history; the 3% reference is indicative. Use by region: six regions; the question changed "
                  "between the two survey waves."))
pied()
