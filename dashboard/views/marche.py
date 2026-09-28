"""Page 2 bis — Marché des télécoms : « Qui tient le marché, et investit-il encore ? » (objectif 2 ; plan visuel, section 7).

Page créée le 28/09/2026 (relevé de l’objectif 2, `workspace/conding-progress.md`, décisions V6 à V9) : le marché quitte
le dernier onglet de la page Internet, et l’onglet des technologies le suit. Cinq sous-onglets, comme la page Internet :
une « Vue synthèse », puis les trois vues que le 07 prévoyait pour l’objectif 2 (marché, investissement, accès), la vue
« accès » étant partagée entre les technologies et la fibre d’une part, le prix et la couverture d’autre part.

Tout est lu dans les tables du 05, du 06 et du 07, sans recalcul d’indicateur. Chiffres nationaux, sauf la carte de la
fibre (communes) et la couverture (régions).
"""
import html

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from composants import (BLEU_FONCE, ariane, carte_kpi, carte_valeur, colorer_regions, constat, couleur_region, entete, export_csv,
                        habiller, limite, note, onglets, pct, pied, rangee_kpi, synthese, titre_bloc, tracer)
from donnees import communes, contours, lire, nombre
from i18n import bi, langue, region, t
from theme import BLEUS, CATEGORIELLE, OCRE, TEXTE_CATEGORIELLE

SEUIL_SOUS_INVESTISSEMENT, SEUIL_EXTENSION = 15, 25   # taux d’investissement (O2-04)
SEUIL_PRIX = 2                                        # coût de 1 Go en % du revenu mensuel (O2-05b)
REPERE_SITES = 50                                     # ajouts nets de sites radio par an (seuil de veille déclaré, P26 du 10)
ROUGE = "#e34948"
GRIS = "#b9b6ad"

# ----------------------------------------------------------------- Tables (lectures en cache, aucun recalcul d’indicateur)
parts = lire("05_eda", "s4_parts_togocom").set_index("annee")            # part de Togocom selon trois mesures
hhi = lire("07_indicateurs", "o2_01_parts_hhi")
ecart = lire("07_indicateurs", "o2_02_ca_contre_abonnes").set_index("annee")
ca = lire("07_indicateurs", "o2_03_ca")
inv = lire("07_indicateurs", "o2_04_investissement").set_index("annee")
arpu = lire("07_indicateurs", "o2_05a_arpu").set_index("annee")
c1go = lire("07_indicateurs", "o2_05b_cout_1go").set_index("annee")
paniers = lire("05_eda", "s4_paniers_uit").set_index("annee")
couv = lire("06_spatial", "s6_couverture_unites").set_index("unite_regionale")
recep = lire("07_indicateurs", "o2_06_reception_declaree")
techno = lire("07_indicateurs", "o1_04_technologies").set_index("annee")
fixe = lire("05_eda", "s4_fibre")
ftth = lire("07_indicateurs", "o2_07_ftth").set_index("annee")
fibre_p = lire("07_indicateurs", "o2_07_fibre_prefectures")
fibre_c = lire("06_spatial", "s6_fibre_communes")
sites = lire("07_indicateurs", "o2_08_sites_radio").set_index("annee")
r6 = lire("10_recommandations", "r6_cout_data").iloc[0]

# ----------------------------------------------------------------- Chiffres partagés entre onglets
og, fg = bi("« ", "“"), bi(" »", "”")  # guillemets selon la langue
a_m = int(parts.data_mobile_ARCEP.dropna().index.max())
a_m0 = int(parts.data_mobile_ARCEP.dropna().index.min())
data_0, data_n = parts.loc[a_m0, "data_mobile_ARCEP"], parts.loc[a_m, "data_mobile_ARCEP"]
camob_0, camob_n = parts.loc[a_m0, "ca_mobile_ARCEP"], parts.loc[a_m, "ca_mobile_ARCEP"]
segments = {"data": hhi[hhi.segment.str.startswith("abonnés data")].set_index("annee"),
            "ca": hhi[hhi.segment.str.startswith("chiffre")].set_index("annee"),
            "tel": hhi[hhi.segment.str.startswith("abonnés téléphonie")].set_index("annee")}
hhi_toujours_haut = bool((hhi.hhi > 5000).all())

arcep = ca[ca.source == "ARCEP"].set_index("annee")
inseed = ca[ca.source != "ARCEP"].set_index("annee")
a_ca, a_ca0 = int(arcep.index.max()), int(arcep.index.min())
ca_n, ca_0 = arcep.loc[a_ca, "ca_md_fcfa"], arcep.loc[a_ca0, "ca_md_fcfa"]
hausse_ca = 100 * (ca_n / ca_0 - 1)
croiss_ca_n = arcep.loc[a_ca, "croissance_pct"]

a_i, a_i0 = int(inv.index.max()), int(inv.index.min())
inv_n = inv.loc[a_i]

a_t = int(techno.index.max())
a_t0 = int(techno[techno.serie_retenue_pour_la_bascule].index.min())
fixe["date"] = pd.PeriodIndex(fixe.periode.str.replace("T", "Q"), freq="Q").to_timestamp()
fx_n = fixe.iloc[-1]
part_gva = 100 * fx_n.ftth_gva / fx_n.ftth_total
a_f = int(ftth.index.max())


def signe(x, d=1) -> str:
    """Variation avec son signe : « +1,0 », « -3,8 »."""
    return ("+" if x > 0 else "") + nombre(x, d)


def trimestre(periode: str) -> str:
    """« 2026T2 » → « 2e trimestre 2026 » en français, « Q2 2026 » en anglais."""
    a, q = periode.split("T")
    return f"{q}{'er' if q == '1' else 'e'} trimestre {a}" if langue() == "fr" else f"Q{q} {a}"


c1go_n, a_p = c1go.iloc[-1].cout_pct_revenu_mensuel, int(c1go.index.max())
c1go_0, a_p0 = c1go.iloc[0].cout_pct_revenu_mensuel, int(c1go.index.min())

# Réception déclarée (EHCVM 2021/22) : l’enquête nomme « Maritime » la région hors du Grand Lomé
rec = recep[(recep.vague == recep.vague.max())].copy()
rec["unite"] = rec.domaine.replace({"Maritime": "Maritime hors Grand Lomé"})
rec1 = rec[rec.indicateur == "reseau_1_bien_capte"].set_index("unite").estimation_pct
rec2 = rec[rec.indicateur == "reseau_2_bien_capte"].set_index("unite").estimation_pct
r_couv_min = couv.couverture_ponderee_pop_pct.idxmin()
r_rec_max, r_rec_min = rec1.idxmax(), rec1.idxmin()

CLASSE_CA = {"croissance réelle positive": (bi("croissance réelle", "real growth"), BLEUS[3]),
             "croissance nominale sans gain réel": (bi("croissance sans gain réel", "nominal growth, no real gain"), BLEUS[1]),
             "stagnation (moins de 2 %)": (bi("stagnation (moins de 2 %)", "stagnation (under 2%)"), OCRE),
             "recul nominal": (bi("recul", "decline"), ROUGE),
             "non classée": (bi("non classée", "not classified"), GRIS)}
CLASSE_INV = {"cycle d’extension": (bi("cycle d’extension (plus de 25 %)", "extension cycle (above 25%)"), BLEUS[4]),
              "régime normal": (bi("régime normal (15 à 25 %)", "normal regime (15 to 25%)"), BLEUS[1]),
              "sous-investissement": (bi("sous-investissement (moins de 15 %)", "under-investment (below 15%)"), ROUGE)}


def classe_ca(x) -> str:
    """Classe du chiffre d’affaires telle qu’écrite dans la table ; « non classée » pour la première année d’une source ou
    une inflation inconnue."""
    return x if isinstance(x, str) and x in CLASSE_CA else "non classée"


def classe_inv(x: str) -> str:
    return str(x).replace("'", "’")


lib_classe_ca_n = CLASSE_CA[classe_ca(arcep.loc[a_ca, "classe_02"])][0].split(" (")[0]  # « stagnation », sans son seuil
lib_classe_inv_n = CLASSE_INV[classe_inv(inv_n.classe_02)][0].split(" (")[0]

# ----------------------------------------------------------------- En-tête (commun aux onglets)
ariane(t("page.marche"))
entete(t("page.marche"), bi("Qui tient le marché, et investit-il encore ?", "Who holds the market, and is it still investing?"),
       bi(f"Togocom (YAS) détient <strong>{pct(data_n)}</strong> des abonnés data en {a_m}. L’investissement tombe à "
          f"<strong>{pct(inv_n.taux_investissement_pct)}</strong> du chiffre d’affaires, près du seuil de {SEUIL_SOUS_INVESTISSEMENT} %.",
          f"Togocom (YAS) holds <strong>{pct(data_n)}</strong> of data subscribers in {a_m}. Investment falls to "
          f"<strong>{pct(inv_n.taux_investissement_pct)}</strong> of revenue, close to the {SEUIL_SOUS_INVESTISSEMENT}% threshold."))
st.markdown(f'<div class="filtres-actifs">{html.escape(bi("Chiffres nationaux (et régionaux pour la couverture) : ils ne changent pas avec les filtres de la barre latérale.", "National figures (and regional ones for coverage): they do not change with the sidebar filters."))}</div>',
            unsafe_allow_html=True)

LIBELLES = [bi("Vue synthèse", "Overview"), bi("Parts de marché", "Market shares"),
            bi("Chiffre d’affaires et investissement", "Revenue and investment"), bi("Technologies et fibre", "Technologies and fibre"),
            bi("Prix et couverture", "Price and coverage")]
o_synth, o_parts, o_ca, o_techno, o_prix = onglets("marche_onglets", LIBELLES)


def renvoi(i: int) -> str:
    return f" <i>({bi('détail : onglet', 'details: tab')} {og}{LIBELLES[i]}{fg})</i>"


# =================================================================== 1. Vue synthèse
if o_synth.open is not False:
    with o_synth:
        seg = segments["data"]
        rangee_kpi(bi("Le marché des télécoms en quatre chiffres", "The telecom market in four figures"), [
            carte_kpi(bi(f"Parts de marché ({a_m})", f"Market shares ({a_m})"), pct(data_n),
                      bi("des abonnés data chez Togocom (YAS)", "of data subscribers with Togocom (YAS)"),
                      bi(f"{pct(camob_n)} du chiffre d’affaires mobile ; indice de concentration : {nombre(seg.loc[a_m, 'hhi'], 0)} sur 10 000",
                         f"{pct(camob_n)} of mobile revenue; concentration index: {nombre(seg.loc[a_m, 'hhi'], 0)} out of 10,000"),
                      bi("Deux opérateurs : l’indice dépasse 5 000 chaque année, sur chaque segment." if hhi_toujours_haut
                         else "Deux opérateurs : un indice au-dessus de 5 000 signale un duopole très concentré.",
                         "Two operators: the index is above 5,000 every year, on every segment." if hhi_toujours_haut
                         else "Two operators: an index above 5,000 signals a highly concentrated duopoly."),
                      bi("Très concentré", "Highly concentrated"), "alerte"),
            carte_kpi(bi(f"Chiffre d’affaires ({a_ca})", f"Revenue ({a_ca})"), nombre(ca_n, 1),
                      bi("milliards de FCFA de chiffre d’affaires pour le secteur", "billion FCFA of revenue for the sector"),
                      bi(f"{signe(croiss_ca_n)} % en {a_ca} ; +{nombre(hausse_ca, 0)} % depuis {a_ca0}",
                         f"{signe(croiss_ca_n)}% in {a_ca}; +{nombre(hausse_ca, 0)}% since {a_ca0}"),
                      bi("Inflation inconnue après 2023 ; un opérateur de fibre (GVA) manque au chiffre du fixe de 2021 à début 2023.",
                         "Inflation unknown after 2023; a fibre operator (GVA) is missing from fixed revenue from 2021 to early 2023."),
                      lib_classe_ca_n.capitalize(), "alerte" if classe_ca(arcep.loc[a_ca, "classe_02"]).startswith(("stagnation", "recul")) else "ok"),
            carte_kpi(bi(f"Investissement ({a_i})", f"Investment ({a_i})"), pct(inv_n.taux_investissement_pct),
                      bi("du chiffre d’affaires investi par les opérateurs", "of revenue invested by operators"),
                      bi(f"seuil de sous-investissement : {SEUIL_SOUS_INVESTISSEMENT} % ; {pct(inv.loc[a_i0, 'taux_investissement_pct'])} en {a_i0}",
                         f"under-investment threshold: {SEUIL_SOUS_INVESTISSEMENT}%; {pct(inv.loc[a_i0, 'taux_investissement_pct'])} in {a_i0}"),
                      bi("Mesure en valeur, cyclique d’une année à l’autre.", "Measured in value, cyclical from year to year."),
                      lib_classe_inv_n.capitalize(), "ok" if inv_n.taux_investissement_pct >= SEUIL_SOUS_INVESTISSEMENT else "alerte"),
            carte_kpi(bi(f"Fibre jusqu’au domicile ({a_f})", f"Fibre to the home ({a_f})"), nombre(ftth.loc[a_f, "ftth_pour_100_habitants"], 2),
                      bi("abonnements pour 100 habitants", "subscriptions per 100 people"),
                      bi(f"+{nombre(ftth.loc[a_f, 'croissance_pct'], 0)} % en un an ; {pct(fx_n.part_ftth_internet_fixe_pct)} de l’Internet fixe "
                         f"({trimestre(fx_n.periode)})",
                         f"+{nombre(ftth.loc[a_f, 'croissance_pct'], 0)}% in one year; {pct(fx_n.part_ftth_internet_fixe_pct)} of fixed Internet "
                         f"({trimestre(fx_n.periode)})"),
                      bi(f"Des abonnés à domicile, pas des km de câble ; {pct(fx_n.part_ftth_data_mobile_pct)} des abonnements data mobile.",
                         f"Home subscribers, not km of cable; {pct(fx_n.part_ftth_data_mobile_pct)} of mobile data subscriptions."),
                      bi("En hausse", "Rising"), "ok"),
        ])
        st.write("")
        constat(bi(f"Deux opérateurs se partagent le marché, et Togocom renforce sa position. Le chiffre d’affaires "
                   f"{'stagne' if classe_ca(arcep.loc[a_ca, 'classe_02']).startswith('stagnation') else 'évolue'} en {a_ca} "
                   f"({signe(croiss_ca_n)} %) et l’investissement revient à {pct(inv_n.taux_investissement_pct)} du chiffre "
                   f"d’affaires, près du seuil de sous-investissement. La 4G est devenue majoritaire ; la fibre remplace l’Internet fixe, "
                   f"mais reste marginale face au mobile.",
                   f"Two operators share the market, and Togocom is strengthening its position. Revenue "
                   f"{'stagnates' if classe_ca(arcep.loc[a_ca, 'classe_02']).startswith('stagnation') else 'moves'} in {a_ca} "
                   f"({signe(croiss_ca_n)}%) and investment falls back to {pct(inv_n.taux_investissement_pct)} of revenue, close to "
                   f"the under-investment threshold. 4G has become the majority; fibre is replacing fixed Internet, but remains "
                   f"marginal next to mobile."))
        synthese(pct(inv_n.taux_investissement_pct),
                 bi(f"du chiffre d’affaires investi en {a_i}, contre {pct(inv.loc[a_i0, 'taux_investissement_pct'])} en {a_i0} : à "
                    f"{nombre(inv_n.taux_investissement_pct - SEUIL_SOUS_INVESTISSEMENT, 1)} point du seuil de sous-investissement",
                    f"of revenue invested in {a_i}, against {pct(inv.loc[a_i0, 'taux_investissement_pct'])} in {a_i0}: "
                    f"{nombre(inv_n.taux_investissement_pct - SEUIL_SOUS_INVESTISSEMENT, 1)} points above the under-investment threshold"), [
            bi(f"Togocom passe de {pct(data_0)} à {pct(data_n)} des abonnés data et de {pct(camob_0)} à {pct(camob_n)} du chiffre "
               f"d’affaires mobile ({a_m0}-{a_m}).",
               f"Togocom rises from {pct(data_0)} to {pct(data_n)} of data subscribers and from {pct(camob_0)} to {pct(camob_n)} of "
               f"mobile revenue ({a_m0}-{a_m}).") + renvoi(1),
            bi(f"Le chiffre d’affaires du secteur atteint {nombre(ca_n, 1)} milliards de FCFA en {a_ca} (+{nombre(hausse_ca, 0)} % depuis {a_ca0}), "
               f"mais il stagne en {a_ca} ({signe(croiss_ca_n)} %).",
               f"Sector revenue reaches {nombre(ca_n, 1)} billion FCFA in {a_ca} (+{nombre(hausse_ca, 0)}% since {a_ca0}), but it "
               f"stagnates in {a_ca} ({signe(croiss_ca_n)}%).") + renvoi(2),
            bi(f"La 4G fait {pct(techno.loc[a_t, '4G'])} des abonnements data mobile en {a_t} ; la fibre, "
               f"{pct(fx_n.part_ftth_internet_fixe_pct)} de l’Internet fixe mais {pct(fx_n.part_ftth_data_mobile_pct)} des abonnements "
               f"data mobile.",
               f"4G accounts for {pct(techno.loc[a_t, '4G'])} of mobile data subscriptions in {a_t}; fibre, "
               f"{pct(fx_n.part_ftth_internet_fixe_pct)} of fixed Internet but {pct(fx_n.part_ftth_data_mobile_pct)} of mobile data "
               f"subscriptions.") + renvoi(3),
            bi(f"1 Go coûte {pct(c1go_n, 2)} du revenu mensuel (seuil : {SEUIL_PRIX} %). {region(r_couv_min)}, la moins couverte en "
               f"théorie, déclare {'la meilleure' if r_couv_min == r_rec_max else 'une bonne'} réception.",
               f"1 GB costs {pct(c1go_n, 2)} of monthly income (threshold: {SEUIL_PRIX}%). {region(r_couv_min)}, the least covered in "
               f"theory, reports {'the best' if r_couv_min == r_rec_max else 'good'} reception.") + renvoi(4),
        ])
        limite(bi("Le marché n’est mesuré qu’au niveau national : parts, chiffre d’affaires, investissement et prix ne se déclinent "
                  "pas par territoire. Les segments du marché ne se mélangent pas, et les deux séries du chiffre d’affaires (annuelle "
                  "jusqu’en 2022, trimestrielle depuis 2018) ne sont jamais raccordées. La couverture affichée est théorique : la qualité de service n’est pas mesurée par "
                  "territoire.",
                  "The market is only measured nationally: shares, revenue, investment and prices are not broken down by territory. "
                  "Market segments are never mixed, and the two revenue series (annual up to 2022, quarterly since 2018) are never joined. The coverage shown "
                  "is theoretical: quality of service is not measured by territory."))

# =================================================================== 2. Parts de marché
if o_parts.open is not False:
    with o_parts:
        constat(bi(f"Togocom renforce sa position : de {pct(data_0)} des abonnés data en {a_m0} à <strong>{pct(data_n)}</strong> en "
                   f"{a_m}, de {pct(camob_0)} à {pct(camob_n)} du chiffre d’affaires mobile. Le marché reste un duopole très concentré, "
                   "chaque année et sur chaque segment.",
                   f"Togocom is strengthening its position: from {pct(data_0)} of data subscribers in {a_m0} to "
                   f"<strong>{pct(data_n)}</strong> in {a_m}, from {pct(camob_0)} to {pct(camob_n)} of mobile revenue. The market "
                   "remains a highly concentrated duopoly, every year and on every segment."))
        gauche, droite = st.columns([1.5, 1], gap="large")
        with gauche:
            with st.container(border=True):
                titre_bloc(bi("Part de Togocom (YAS), selon trois mesures", "Togocom (YAS) share, by three measures"),
                           bi("Une courbe par mesure, jamais additionnées ; le reste revient à Moov Africa. En 2020, la part des abonnés "
                              "data est une rupture de série (reclassement de la 3G de Togocel), pas un mouvement du marché.",
                              "One line per measure, never added together; the rest goes to Moov Africa. In 2020, the data-subscriber "
                              "share is a series break (Togocel 3G reclassification), not a market move."))
                mesures = [("data_mobile_ARCEP", bi("abonnés data mobile", "mobile data subscribers"), CATEGORIELLE[0]),
                           ("ca_mobile_ARCEP", bi("chiffre d’affaires mobile", "mobile revenue"), CATEGORIELLE[1]),
                           ("telephonie_D3", bi("abonnés à la téléphonie mobile", "mobile telephony subscribers"), CATEGORIELLE[2])]
                sep = bi(" : ", ": ")
                fig = go.Figure()
                for col, nom, coul in mesures:
                    s = parts[col].dropna()
                    a_der = int(s.index.max())
                    y = [None if (col == "data_mobile_ARCEP" and a == 2020) else v for a, v in s.items()]
                    fig.add_scatter(x=s.index, y=y, mode="lines+markers", name=f"{nom}{sep}{pct(s.loc[a_der])} ({a_der})",
                                    line=dict(color=coul, width=2.5), marker=dict(size=7, color=coul, line=dict(color="#ffffff", width=1.5)),
                                    connectgaps=False, hovertemplate=f"{nom} " + "%{x} : %{y:.1f} %<extra></extra>")
                # 2020 : cercle vide, relié à rien (rupture de série)
                fig.add_scatter(x=[2020], y=[parts.loc[2020, "data_mobile_ARCEP"]], mode="markers", showlegend=False,
                                marker=dict(size=10, color="#ffffff", line=dict(color=CATEGORIELLE[0], width=2.5)),
                                hovertemplate=bi("2020 : %{y:.1f} % (rupture de série)", "2020: %{y:.1f}% (series break)") + "<extra></extra>")
                fig.add_annotation(x=2020, y=parts.loc[2020, "data_mobile_ARCEP"], text=bi("rupture de série", "series break"),
                                   showarrow=False, yshift=-16, font=dict(size=11, color=BLEU_FONCE))
                fig.add_hline(y=50, line=dict(color="#8a8780", width=1, dash="dash"),
                              annotation_text=bi("parts égales", "equal shares"), annotation_position="bottom right",
                              annotation_font=dict(size=11, color="#55534e"))
                habiller(fig, 400, " %", legende_y=-0.14, yaxis=dict(ticksuffix=" %", gridcolor="#efece4", range=[30, 75]),
                         xaxis=dict(gridcolor="#efece4", dtick=2))
                tracer(fig, "parts_togocom")
                ec = ecart[ecart.classe_togocom_data.isin(["alignement", "haut de marché"])].ecart_points_data
                tel = ecart.ecart_points_telephonie.dropna()
                note(bi(f"Sa part du chiffre d’affaires dépasse sa part des abonnés data de {nombre(ec.min(), 1)} à {nombre(ec.max(), 1)} points "
                        f"selon l’année : entre « alignement » et « haut de marché ». Face aux abonnés à la téléphonie ({int(tel.index.min())}-"
                        f"{int(tel.index.max())}) : +{nombre(tel.iloc[0], 1)} et +{nombre(tel.iloc[-1], 1)} points, haut de marché.",
                        f"Its revenue share exceeds its data-subscriber share by {nombre(ec.min(), 1)} to {nombre(ec.max(), 1)} points "
                        f"depending on the year: between “aligned” and “upmarket”. Against telephony subscribers ({int(tel.index.min())}-"
                        f"{int(tel.index.max())}): +{nombre(tel.iloc[0], 1)} and +{nombre(tel.iloc[-1], 1)} points, upmarket."))
                export_csv(parts.reset_index(), "parts_togocom.csv", "export_parts")
        with droite:
            with st.container(border=True):
                titre_bloc(bi("Indice de concentration, par segment", "Concentration index, by segment"),
                           bi("Somme des carrés des parts de marché ; au-dessus de 5 000 : duopole très concentré.",
                              "Sum of squared market shares; above 5,000: highly concentrated duopoly."))
                lib_seg = {"data": bi("abonnés data mobile", "mobile data subscribers"), "ca": bi("chiffre d’affaires mobile", "mobile revenue"),
                           "tel": bi("abonnés à la téléphonie", "telephony subscribers")}
                fl = " → "
                lignes = []
                for k, sg in segments.items():
                    a0, a1 = int(sg.index.min()), int(sg.index.max())
                    # les parts de Togocom sont sur le graphique voisin : le tableau ne garde que l’indice
                    lignes.append({bi("segment (période)", "segment (period)"): f"{lib_seg[k]} ({a0}-{a1})",
                                   bi("indice, début → fin", "index, start → end"): f"{nombre(sg.loc[a0, 'hhi'], 0)}{fl}{nombre(sg.loc[a1, 'hhi'], 0)}"})
                st.dataframe(pd.DataFrame(lignes), hide_index=True, use_container_width=True)
                sd, sc = segments["data"], segments["ca"]
                note(bi(f"L’indice monte sur les abonnés data ({nombre(sd.hhi.iloc[0], 0)} → {nombre(sd.hhi.iloc[-1], 0)}) et sur le chiffre "
                        f"d’affaires ({nombre(sc.hhi.iloc[0], 0)} → {nombre(sc.hhi.iloc[-1], 0)}) : la concentration augmente, portée par Togocom.",
                        f"The index rises on data subscribers ({nombre(sd.hhi.iloc[0], 0)} → {nombre(sd.hhi.iloc[-1], 0)}) and on revenue "
                        f"({nombre(sc.hhi.iloc[0], 0)} → {nombre(sc.hhi.iloc[-1], 0)}): concentration is increasing, driven by Togocom."))
                export_csv(hhi, "concentration_marche.csv", "export_hhi")
        limite(bi("Les segments ne se mélangent jamais : abonnés data et chiffre d’affaires mobile (depuis 2018), abonnés à la "
                  "téléphonie (série arrêtée en 2019). 2020 est une rupture de série sur les abonnés data. Le chiffre d’affaires "
                  "mobile couvre tous les services, les abonnés data une partie seulement : l’écart entre les deux parts situe "
                  "l’opérateur, il ne mesure pas ses prix.",
                  "Segments are never mixed: data subscribers and mobile revenue (since 2018), telephony subscribers ("
                  "series stopped in 2019). 2020 is a series break for data subscribers. Mobile revenue covers all services, data "
                  "subscribers only part of them: the gap between the two shares positions the operator, it does not measure its prices."))

# =================================================================== 3. Chiffre d’affaires et investissement
if o_ca.open is not False:
    with o_ca:
        constat(bi(f"Le chiffre d’affaires du secteur passe de {nombre(ca_0, 1)} à <strong>{nombre(ca_n, 1)} milliards de FCFA</strong> de {a_ca0} "
                   f"à {a_ca} (+{nombre(hausse_ca, 0)} %), mais il stagne en {a_ca} ({signe(croiss_ca_n)} %). L’investissement suit des "
                   f"cycles : {pct(inv.loc[a_i0, 'taux_investissement_pct'])} du chiffre d’affaires en {a_i0}, "
                   f"<strong>{pct(inv_n.taux_investissement_pct)}</strong> en {a_i}, près du seuil de {SEUIL_SOUS_INVESTISSEMENT} %.",
                   f"Sector revenue rises from {nombre(ca_0, 1)} to <strong>{nombre(ca_n, 1)} billion FCFA</strong> from {a_ca0} to {a_ca} "
                   f"(+{nombre(hausse_ca, 0)}%), but it stagnates in {a_ca} ({signe(croiss_ca_n)}%). Investment follows cycles: "
                   f"{pct(inv.loc[a_i0, 'taux_investissement_pct'])} of revenue in {a_i0}, <strong>{pct(inv_n.taux_investissement_pct)}</strong> "
                   f"in {a_i}, close to the {SEUIL_SOUS_INVESTISSEMENT}% threshold."))
        g1, g2 = st.columns(2, gap="large")
        with g1:
            with st.container(border=True):
                titre_bloc(bi(f"Chiffre d’affaires du secteur, {int(inseed.index.min())}-{a_ca}", f"Sector revenue, {int(inseed.index.min())}-{a_ca}"),
                           bi("Milliards de FCFA ; chaque année est classée face à l’inflation. Deux séries publiées, jamais "
                              "raccordées : en barres, la série trimestrielle (depuis 2018) ; en ligne, la série annuelle (2010-2022).",
                              "Billions of FCFA; each year is classified against inflation. Two published series, never joined: as bars, "
                              "the quarterly series (since 2018); as a line, the annual series (2010-2022)."))
                ar = arcep.copy()
                ar["cl"] = ar.classe_02.map(classe_ca)
                ins = inseed.copy()
                ins["cl"] = ins.classe_02.map(classe_ca)
                fig = go.Figure()
                for cl, (lib, coul) in CLASSE_CA.items():
                    sub = ar[ar.cl == cl]
                    x, y = (list(sub.index), list(sub.ca_md_fcfa)) if len(sub) else ([int(ins.index.min())], [0])  # barre nulle : entrée de légende
                    fig.add_bar(x=x, y=y, name=lib, marker_color=coul, legendrank=list(CLASSE_CA).index(cl),
                                customdata=[[f"{nombre(v, 1)}" if pd.notna(v) else "—"] for v in (sub.croissance_pct if len(sub) else [None])],
                                hovertemplate=bi("série trimestrielle", "quarterly series") + " %{x} : %{y:.1f} " + bi("milliards de FCFA", "billion FCFA") + " (%{customdata[0]} %)<extra>" + lib + "</extra>",
                                hoverinfo=None if len(sub) else "skip")
                fig.add_scatter(x=ins.index, y=ins.ca_md_fcfa, mode="lines+markers", name=bi("série annuelle (ligne)", "annual series (line)"),
                                line=dict(color="#55534e", width=1.5), legendrank=99,
                                marker=dict(size=9, color=[CLASSE_CA[c][1] for c in ins.cl], line=dict(color="#55534e", width=1)),
                                customdata=[[CLASSE_CA[c][0]] for c in ins.cl],
                                hovertemplate=bi("série annuelle", "annual series") + " %{x} : %{y:.1f} " + bi("milliards de FCFA", "billion FCFA") + "<extra>%{customdata[0]}</extra>")
                fig.add_annotation(x=a_ca, y=ca_n, text=f"<b>{nombre(ca_n, 1)}</b>", showarrow=False, yshift=12, font=dict(size=11, color=BLEU_FONCE))
                habiller(fig, 380, legende_y=-0.14, barmode="relative", bargap=0.3, xaxis=dict(gridcolor="#efece4", dtick=2),
                         yaxis=dict(gridcolor="#efece4", range=[0, ca_n * 1.15]))
                tracer(fig, "chiffre_affaires")
                export_csv(ca, "chiffre_affaires.csv", "export_ca")
        with g2:
            with st.container(border=True):
                titre_bloc(bi(f"Taux d’investissement, {a_i0}-{a_i}", f"Investment rate, {a_i0}-{a_i}"),
                           bi(f"Investissement des opérateurs en % du chiffre d’affaires ; seuils à {SEUIL_SOUS_INVESTISSEMENT} % et {SEUIL_EXTENSION} %.",
                              f"Operators’ investment as a % of revenue; thresholds at {SEUIL_SOUS_INVESTISSEMENT}% and {SEUIL_EXTENSION}%."))
                iv = inv.copy()
                iv["cl"] = iv.classe_02.map(classe_inv)
                fig = go.Figure()
                for cl, (lib, coul) in CLASSE_INV.items():
                    sub = iv[iv.cl == cl]
                    x, y = (list(sub.index), list(sub.taux_investissement_pct)) if len(sub) else ([a_i0], [0])
                    fig.add_bar(x=x, y=y, name=lib, marker_color=coul, text=[pct(v) for v in y] if len(sub) else None,
                                textposition="outside", textfont=dict(size=11, color=BLEU_FONCE),
                                customdata=list(sub.investissement_md_fcfa) if len(sub) else None,
                                hovertemplate="%{x} : %{y:.1f} % (%{customdata:.1f} " + bi("milliards de FCFA", "billion FCFA") + ")<extra>" + lib + "</extra>",
                                hoverinfo=None if len(sub) else "skip")
                fig.add_hline(y=SEUIL_SOUS_INVESTISSEMENT, line=dict(color=ROUGE, width=1, dash="dash"))
                fig.add_hline(y=SEUIL_EXTENSION, line=dict(color="#8a8780", width=1, dash="dot"))
                habiller(fig, 380, " %", legende_y=-0.14, barmode="relative", bargap=0.3, xaxis=dict(gridcolor="#efece4", dtick=1),
                         yaxis=dict(ticksuffix=" %", gridcolor="#efece4", range=[0, iv.taux_investissement_pct.max() * 1.2]))
                tracer(fig, "taux_investissement")
                ext = [int(a) for a in iv.index if iv.loc[a, "cl"] == "cycle d’extension"]
                cycles = []  # années consécutives regroupées en périodes
                for a in ext:
                    if cycles and a == cycles[-1][1] + 1:
                        cycles[-1][1] = a
                    else:
                        cycles.append([a, a])
                per = [f"{d}-{f}" if f > d else str(d) for d, f in cycles]
                per_txt = bi(", ".join(per[:-1]) + " et " + per[-1], ", ".join(per[:-1]) + " and " + per[-1]) if len(per) > 1 else per[0]
                n_cyc = {1: bi("Un cycle", "One extension cycle"), 2: bi("Deux cycles", "Two extension cycles")}.get(len(per), bi(f"{len(per)} cycles", f"{len(per)} extension cycles"))
                note(bi(f"{n_cyc} d’extension ({per_txt}), puis le régime normal : {pct(inv_n.taux_investissement_pct)} en {a_i}, "
                        f"à {nombre(inv_n.taux_investissement_pct - SEUIL_SOUS_INVESTISSEMENT, 1)} point du seuil de sous-investissement.",
                        f"{n_cyc} ({per_txt}), then the normal regime: {pct(inv_n.taux_investissement_pct)} in {a_i}, "
                        f"{nombre(inv_n.taux_investissement_pct - SEUIL_SOUS_INVESTISSEMENT, 1)} points above the under-investment threshold."))
                export_csv(inv.reset_index(), "taux_investissement.csv", "export_investissement")
        g3, g4 = st.columns([1.5, 1], gap="large")
        with g3:
            with st.container(border=True):
                s_0, s_n = int(sites.index.min()), int(sites.index.max())
                titre_bloc(bi(f"Sites radio : {nombre(sites.loc[s_0, 'total_sites'])} en {s_0}, {nombre(sites.loc[s_n, 'total_sites'])} en {s_n}",
                              f"Radio sites: {nombre(sites.loc[s_0, 'total_sites'])} in {s_0}, {nombre(sites.loc[s_n, 'total_sites'])} in {s_n}"),
                           bi(f"Ajouts nets par an, par opérateur ; repère de veille à {REPERE_SITES}. Un site compte une fois, quelle que soit "
                              "sa technologie.",
                              f"Net additions per year, by operator; watch reference at {REPERE_SITES}. A site counts once, whatever its technology."))
                s4 = sites.loc[s_0 + 1:]
                fig = go.Figure()
                fig.add_bar(x=s4.index, y=s4.ajouts_nets_moov, name="Moov Africa", marker_color=CATEGORIELLE[0])
                fig.add_bar(x=s4.index, y=s4.ajouts_nets_yas, name="YAS (Togocom)", marker_color=CATEGORIELLE[1])
                fig.add_hline(y=REPERE_SITES, line=dict(color="#8a1c1b", width=1, dash="dash"),
                              annotation_text=bi(f"Repère de veille : {REPERE_SITES}", f"Watch reference: {REPERE_SITES}"),
                              annotation_position="top right", annotation_font=dict(size=11, color="#8a1c1b"))
                habiller(fig, 280, legende_y=1.18, barmode="relative", xaxis=dict(gridcolor="#efece4", dtick=1))
                tracer(fig, "sites_radio")
                a2 = s_0 + 1
                deux_trois = int(sites.loc[s_0, "moov_2g3g_seulement"] + sites.loc[s_0, "yas_2g3g_seulement"])
                note(bi(f"Les ajouts nets tombent de {int(sites.loc[a2, 'ajouts_nets_total'])} à {int(sites.loc[s_n, 'ajouts_nets_total'])} en "
                        f"{s_n - a2} ans ; {s_n} est la première année sous le repère de veille. Depuis {a2}, tous les sites portent la 4G "
                        f"({deux_trois} sites en 2G ou 3G seulement en {s_0}).",
                        f"Net additions fall from {int(sites.loc[a2, 'ajouts_nets_total'])} to {int(sites.loc[s_n, 'ajouts_nets_total'])} in "
                        f"{s_n - a2} years; {s_n} is the first year below the watch reference. Since {a2}, every site carries 4G "
                        f"({deux_trois} sites with 2G or 3G only in {s_0})."))
                export_csv(sites.reset_index(), "sites_radio.csv", "export_sites_radio")
        with g4:
            a_r, a_r0 = int(arpu.index.max()), int(arpu.index.min())
            a_rmax = int(arpu.arpu_fcfa_mois.idxmax())
            rangee_kpi(bi("Revenu par abonnement", "Revenue per subscription"), [
                carte_kpi(bi(f"Revenu moyen mobile ({a_r})", f"Average mobile revenue ({a_r})"), nombre(arpu.loc[a_r, "arpu_fcfa_mois"]),
                          bi("FCFA par mois et par abonnement mobile, tous services", "FCFA per month per mobile subscription, all services"),
                          bi(f"{nombre(arpu.loc[a_r0, 'arpu_fcfa_mois'])} en {a_r0} ; {nombre(arpu.loc[a_rmax, 'arpu_fcfa_mois'])} en {a_rmax}, le plus haut",
                             f"{nombre(arpu.loc[a_r0, 'arpu_fcfa_mois'])} in {a_r0}; {nombre(arpu.loc[a_rmax, 'arpu_fcfa_mois'])} in {a_rmax}, the highest"),
                          bi(f"Abonnés moyens sur 4 trimestres ; {nombre(arpu.loc[a_r, 'arpu_fcfa_mois_sensibilite_T4'])} FCFA avec ceux du 4e trimestre.",
                             f"Average subscribers over 4 quarters; {nombre(arpu.loc[a_r, 'arpu_fcfa_mois_sensibilite_T4'])} FCFA with fourth-quarter ones."),
                          None, "neutre"),
            ])
        limite(bi("Chiffre d’affaires : du 1er trimestre 2021 au 1er trimestre 2023, le chiffre du fixe est publié sans l’opérateur GVA ; une "
                  "partie des hausses de 2023 et 2024 tient à son retour. L’inflation n’est connue que jusqu’en 2023 : 2024 n’est pas classé. "
                  "Net ou brut de taxes : non documenté. L’investissement est une mesure en valeur, cyclique ; les sites radio la complètent "
                  "en volume. Tout est national.",
                  "Revenue: from Q1 2021 to Q1 2023, fixed revenue is published without operator GVA; part of the 2023 and 2024 "
                  "increases comes from its return. Inflation is only known up to 2023: 2024 is not classified. Net or gross of taxes: "
                  "not documented. Investment is measured in value and is cyclical; radio sites complement it in volume. Everything is "
                  "national."))

# =================================================================== 4. Technologies et fibre
if o_techno.open is not False:
    with o_techno:
        rangee_kpi(bi(f"Abonnements data mobile et fibre ({a_t})", f"Mobile data subscriptions and fibre ({a_t})"), [
            carte_kpi(bi("Haut débit", "Broadband"), pct(techno.loc[a_t, "part_haut_debit_pct"]),
                      bi("des abonnements data mobile sont en 3G ou 4G", "of mobile data subscriptions are 3G or 4G"),
                      bi("seuil du passage au haut débit : 80 %", "broadband switch threshold: 80%"),
                      bi("Un abonnement n’est pas une personne : un usager peut avoir plusieurs cartes SIM.",
                         "A subscription is not a person: a user may have several SIM cards."),
                      bi("Seuil franchi", "Threshold reached") if techno.loc[a_t, "part_haut_debit_pct"] >= 80 else bi("Sous le seuil", "Below threshold"),
                      "ok" if techno.loc[a_t, "part_haut_debit_pct"] >= 80 else "alerte"),
            carte_kpi("4G", pct(techno.loc[a_t, "4G"]), bi("des abonnements data mobile", "of mobile data subscriptions"),
                      bi(f"{pct(techno.loc[a_t0, '4G'])} en {a_t0}", f"{pct(techno.loc[a_t0, '4G'])} in {a_t0}"), "", None, "neutre"),
            carte_kpi("2G", pct(techno.loc[a_t, "2G"]), bi("des abonnements data mobile", "of mobile data subscriptions"),
                      bi(f"{pct(techno.loc[a_t0, '2G'])} en {a_t0}", f"{pct(techno.loc[a_t0, '2G'])} in {a_t0}"), "", None, "neutre"),
            carte_kpi(bi("Fibre jusqu’au domicile", "Fibre to the home"), pct(techno.loc[a_t, "part_ftth_internet_pct"]),
                      bi("des abonnements Internet", "of Internet subscriptions"),
                      bi(f"{nombre(techno.loc[a_t, 'abonnes_ftth_T4'])} abonnés en {a_t}", f"{nombre(techno.loc[a_t, 'abonnes_ftth_T4'])} subscribers in {a_t}"),
                      "", None, "neutre"),
        ])
        st.write("")
        gauche, droite = st.columns([1.6, 1], gap="large")
        with gauche:
            with st.container(border=True):
                titre_bloc(bi(f"Abonnements data mobile par technologie, {a_t0}-{a_t}", f"Mobile data subscriptions by technology, {a_t0}-{a_t}"),
                           bi("Part de chaque technologie (valeur du 4e trimestre).", "Share of each technology (fourth-quarter value)."))
                tt = techno.loc[a_t0:]
                fig = go.Figure()
                for col, nom, coul in (("2G", "2G", CATEGORIELLE[4]),
                                       ("3G+4G (Moov, non ventilé)", bi("3G et 4G de Moov, non ventilées", "Moov 3G and 4G, not broken down"), CATEGORIELLE[3]),
                                       ("3G", "3G", CATEGORIELLE[1]), ("4G", "4G", CATEGORIELLE[0])):
                    fig.add_bar(x=tt.index, y=tt[col], name=nom, marker_color=coul, marker_line_color="#ffffff", marker_line_width=1.5,
                                text=[pct(v, 0) if col == "4G" and v >= 10 else "" for v in tt[col]], textposition="inside",
                                textfont=dict(color="#ffffff", size=11), hovertemplate=f"{nom} " + "%{x} : %{y:.1f} %<extra></extra>")
                fig.add_vline(x=2019.5, line=dict(color="#55534e", width=1))
                fig.add_annotation(x=2019.5, y=100, text=bi("rupture de série (1er trimestre 2020)", "series break (Q1 2020)"), showarrow=False,
                                   xanchor="left", yanchor="bottom", xshift=4, font=dict(size=10, color="#55534e"))
                habiller(fig, 380, " %", legende_y=1.14, barmode="stack", bargap=0.3, xaxis=dict(gridcolor="#efece4", dtick=1),
                         yaxis=dict(ticksuffix=" %", gridcolor="#efece4", range=[0, 106]))
                tracer(fig, "mix_technologique")
                export_csv(tt.reset_index()[["annee", "2G", "3G", "4G", "3G+4G (Moov, non ventilé)", "part_haut_debit_pct"]],
                           "technologies_data.csv", "export_technologies")
        with droite:
            c4g = lambda x: f'<strong style="color:{TEXTE_CATEGORIELLE[CATEGORIELLE[0]]}">{x}</strong>'
            c2g = lambda x: f'<strong style="color:{TEXTE_CATEGORIELLE[CATEGORIELLE[4]]}">{x}</strong>'
            constat(bi(f"La {c4g('4G')} devient majoritaire en {a_t} ({c4g(pct(techno.loc[a_t, '4G']))} des abonnements data) ; la {c2g('2G')} "
                       f"recule de {c2g(pct(techno.loc[a_t0, '2G']))} à {c2g(pct(techno.loc[a_t, '2G']))}. L’Internet fixe se reconstruit "
                       f"sur la fibre : {pct(fx_n.part_ftth_internet_fixe_pct)} de l’Internet fixe, mais {pct(fx_n.part_ftth_data_mobile_pct)} "
                       "des abonnements data mobile.",
                       f"{c4g('4G')} becomes the majority in {a_t} ({c4g(pct(techno.loc[a_t, '4G']))} of data subscriptions); {c2g('2G')} "
                       f"falls from {c2g(pct(techno.loc[a_t0, '2G']))} to {c2g(pct(techno.loc[a_t, '2G']))}. Fixed Internet is rebuilding "
                       f"on fibre: {pct(fx_n.part_ftth_internet_fixe_pct)} of fixed Internet, but {pct(fx_n.part_ftth_data_mobile_pct)} of "
                       "mobile data subscriptions."))
        g1, g2 = st.columns([1.6, 1], gap="large")
        with g1:
            with st.container(border=True):
                titre_bloc(bi(f"Internet fixe et fibre jusqu’au domicile, {fixe.periode.iloc[0][:4]}-{fx_n.periode[:4]}",
                              f"Fixed Internet and fibre to the home, {fixe.periode.iloc[0][:4]}-{fx_n.periode[:4]}"),
                           bi("Abonnés, par trimestre. GVA : son Internet fixe avant 2024, tout en fibre depuis que sa fibre est "
                              "publiée à part ; la fibre de Togo Telecom n’est pas publiée à part de fin 2021 à fin 2023 (bande grise).",
                              "Subscribers, by quarter. GVA: its fixed Internet before 2024, all fibre since its fibre is published "
                              "separately; Togo Telecom’s fibre is not published separately from late 2021 to late 2023 (grey band)."))
                fixe["trim"] = fixe.periode.map(trimestre)
                avant = fixe[fixe.ftth_gva.isna() | (fixe.date == fixe.loc[fixe.ftth_gva.notna(), "date"].min())]
                series = [(fixe, "internet_fixe_total", bi("Internet fixe, total", "Fixed Internet, total"), "#141413", "solid", 2.5),
                          (fixe[fixe.date <= fixe.loc[fixe.evdo_togo_telecom == 0, "date"].min()], "evdo_togo_telecom",
                           bi("EvDo de Togo Telecom (ancien accès)", "Togo Telecom EvDo (former access)"), "#8a8780", "dot", 2),
                          (fixe, "ftth_togo_telecom", bi("fibre de Togo Telecom", "Togo Telecom fibre"), CATEGORIELLE[0], "solid", 2.5),
                          (avant, "internet_fixe_gva", bi("GVA : Internet fixe (avant 2024)", "GVA: fixed Internet (before 2024)"), CATEGORIELLE[1], "dash", 2),
                          (fixe, "ftth_gva", bi("GVA : fibre (depuis 2024)", "GVA: fibre (since 2024)"), CATEGORIELLE[1], "solid", 2.5)]
                fig = go.Figure()
                for df, col, nom, coul, trait, ep in series:
                    fig.add_scatter(x=df.date, y=df[col], mode="lines", name=nom, line=dict(color=coul, dash=trait, width=ep), connectgaps=False,
                                    customdata=df.trim, hovertemplate=f"{nom}, " + "%{customdata} : %{y:,.0f}<extra></extra>")
                # bande grise sur les trimestres où la fibre de Togo Telecom n’est pas publiée à part (figure 13 du 05)
                publie = fixe.ftth_togo_telecom.notna()
                trou = fixe[~publie & (fixe.date > fixe.loc[publie, "date"].min())]
                if len(trou):
                    apres = fixe.loc[publie & (fixe.date > trou.date.max()), "date"]
                    fin_trou = apres.min() if len(apres) else trou.date.max()
                    fig.add_vrect(x0=trou.date.min(), x1=fin_trou, fillcolor="#8a8780", opacity=0.14, line_width=0, layer="below")
                    fig.add_annotation(x=trou.date.min() + (fin_trou - trou.date.min()) / 2, y=0, yanchor="bottom", yshift=6,
                                       text=bi("fibre de Togo Telecom<br>non publiée à part", "Togo Telecom fibre<br>not published separately"),
                                       showarrow=False, font=dict(size=11, color="#55534e"))
                arret = fixe.loc[fixe.evdo_togo_telecom == 0].iloc[0]
                fig.add_annotation(x=arret.date, y=arret.internet_fixe_total, ax=40, ay=-50, showarrow=True, arrowcolor="#8a8780",
                                   text=bi("arrêt de l’EvDo", "EvDo shut down"), font=dict(size=11, color=BLEU_FONCE), xanchor="left")
                habiller(fig, 400, legende_y=-0.14, yaxis=dict(gridcolor="#efece4", tickformat=",.0f"), xaxis=dict(gridcolor="#efece4"))
                tracer(fig, "fibre_trimestres")
                note(bi(f"L’Internet fixe chute au {trimestre(arret.periode)}, quand l’EvDo de Togo Telecom s’arrête, puis se reconstruit sur la "
                        f"fibre : {nombre(fx_n.ftth_total)} abonnés au {trimestre(fx_n.periode)}, {pct(fx_n.part_ftth_internet_fixe_pct)} de "
                        f"l’Internet fixe, dont {nombre(part_gva, 0)} % chez GVA.",
                        f"Fixed Internet drops in {trimestre(arret.periode)}, when Togo Telecom’s EvDo shuts down, then rebuilds on fibre: "
                        f"{nombre(fx_n.ftth_total)} subscribers in {trimestre(fx_n.periode)}, {pct(fx_n.part_ftth_internet_fixe_pct)} of fixed "
                        f"Internet, {nombre(part_gva, 0)}% of them with GVA."))
                export_csv(fixe.drop(columns=["date", "trim"]), "internet_fixe_fibre.csv", "export_fibre_trimestres")
        with g2:
            with st.container(border=True):
                cm = communes().set_index("code")
                fc = fibre_c.copy()
                sans = fc[fc.aucune_fibre_recensee]
                sans_formel = int((cm.loc[sans.code, "statut_O4_05"] == "mobile money uniquement").sum())
                toutes_rurales = bool((cm.loc[sans.code, "milieu"] == "Rural").all())
                titre_bloc(bi("Communes sans fibre recensée", "Communes with no recorded fibre"),
                           bi(f"{len(sans)} communes sur {len(fc)}{', toutes rurales' if toutes_rurales else ''} "
                              f"({nombre(sans.pop_totale.sum())} habitants) ; {sans_formel} n’ont pas non plus d’agence financière.",
                              f"{len(sans)} communes out of {len(fc)}{', all rural' if toutes_rurales else ''} "
                              f"({nombre(sans.pop_totale.sum())} people); {sans_formel} have no financial branch either."))
                lib_sans, lib_avec = bi("aucune fibre recensée", "no recorded fibre"), bi("fibre recensée", "recorded fibre")
                c_ent, c_aer = bi("fibre enterrée (km)", "buried fibre (km)"), bi("fibre aérienne (km)", "aerial fibre (km)")
                fc["fibre"] = fc.aucune_fibre_recensee.map({True: lib_sans, False: lib_avec})
                fc = fc.rename(columns={"km_fibre_enterree": c_ent, "km_fibre_aerienne": c_aer})
                carte_valeur(contours("communes"), fc, "carte_fibre_communes", "fibre", bi("Fibre", "Fibre"), hauteur=460, categorique=True,
                             couleurs_categorie={lib_sans: CATEGORIELLE[1], lib_avec: BLEUS[0]}, hover_extra={c_ent: ":.1f", c_aer: ":.1f"})
                export_csv(fibre_c, "fibre_communes.csv", "export_fibre_communes")
            with st.container(border=True):
                sans_p = fibre_p[fibre_p.raccorde_02 == "non raccordé"]
                titre_bloc(bi("Préfectures sans fibre recensée", "Prefectures with no recorded fibre"),
                           bi(f"{len(sans_p)} préfectures sur {len(fibre_p)} ({nombre(sans_p.pop_totale.sum())} habitants).",
                              f"{len(sans_p)} prefectures out of {len(fibre_p)} ({nombre(sans_p.pop_totale.sum())} people)."))
                tab = sans_p[["nom", "unite_regionale", "pop_totale"]].rename(columns={
                    "nom": bi("préfecture", "prefecture"), "unite_regionale": bi("région", "region"), "pop_totale": bi("habitants", "population")})
                tab[bi("région", "region")] = tab[bi("région", "region")].map(region)
                tab[bi("habitants", "population")] = tab[bi("habitants", "population")].map(nombre)
                st.dataframe(colorer_regions(tab, bi("région", "region")), hide_index=True, use_container_width=True)
                export_csv(sans_p[["nom", "unite_regionale", "pop_totale"]], "prefectures_sans_fibre.csv", "export_fibre")
        limite(bi("Un abonnement n’est pas une personne. Rupture de série au 1er trimestre 2020 (reclassement de la 3G de Togocel) ; avant "
                  "2020, la 3G et la 4G de Moov ne sont pas ventilées. La fibre se lit de deux façons, jamais additionnées : des abonnés à "
                  "domicile, et une longueur de câble recensée (carte de 2021/2022, sans date de pose, transport et accès confondus). "
                  "Une commune traversée par un câble n’est pas pour autant raccordée à domicile.",
                  "A subscription is not a person. Series break in Q1 2020 (Togocel 3G reclassification); before 2020, Moov’s 3G and 4G "
                  "are not broken down. Fibre is read in two ways, never added together: home subscribers, and a recorded cable "
                  "length (2021/2022 map, no laying date, backbone and access combined). A commune crossed by a cable is not necessarily "
                  "connected at home."))

# =================================================================== 5. Prix et couverture
if o_prix.open is not False:
    with o_prix:
        # régions dans leur couleur (celle des tableaux) ; chiffres dans la couleur de leur série sur les graphiques voisins
        def en(coul, txt):
            return f'<strong style="color:{coul}">{txt}</strong>'
        rg = lambda r: en(couleur_region(r), html.escape(region(r)))
        cv = lambda r: en(TEXTE_CATEGORIELLE[CATEGORIELLE[0]], pct(couv.loc[r, "couverture_ponderee_pop_pct"]))
        rc = lambda r: en(TEXTE_CATEGORIELLE[CATEGORIELLE[1]], pct(rec1[r]))
        prix = lambda x: en(BLEU_FONCE, pct(x, 2))
        seuil = en(TEXTE_CATEGORIELLE[ROUGE], pct(SEUIL_PRIX, 0))
        meilleure = r_couv_min == r_rec_max
        constat(bi(f"1 Go coûte {prix(c1go_n)} du revenu mensuel en {a_p} ({prix(c1go_0)} en {a_p0}) : il baisse, mais reste loin du "
                   f"seuil de {seuil}. Couverture théorique et réception déclarée ne vont pas ensemble : {rg(r_couv_min)}, la moins "
                   f"couverte en théorie ({cv(r_couv_min)}), déclare {'la meilleure' if meilleure else 'une bonne'} réception "
                   f"({rc(r_couv_min)}) ; à l’inverse, {rg(r_rec_min)} : {cv(r_rec_min)} de couverture théorique, {rc(r_rec_min)} de "
                   "réception déclarée.",
                   f"1 GB costs {prix(c1go_n)} of monthly income in {a_p} ({prix(c1go_0)} in {a_p0}): it is falling, but remains far "
                   f"from the {seuil} threshold. Theoretical coverage and reported reception do not go together: {rg(r_couv_min)}, the "
                   f"least covered in theory ({cv(r_couv_min)}), reports {'the best' if meilleure else 'good'} reception "
                   f"({rc(r_couv_min)}); conversely, {rg(r_rec_min)}: {cv(r_rec_min)} theoretical coverage, {rc(r_rec_min)} reported "
                   "reception."))
        g1, g2 = st.columns(2, gap="large")
        with g1:
            with st.container(border=True):
                pa = paniers.loc[2018:]
                titre_bloc(bi(f"Prix de la data mobile, en % du revenu mensuel, {int(pa.index.min())}-{int(pa.index.max())}",
                              f"Mobile data price, as a % of monthly income, {int(pa.index.min())}-{int(pa.index.max())}"),
                           bi("Un panier de prix international par courbe, chacun lu séparément : leurs définitions changent, ils ne se raccordent pas. "
                              "Le panier de 2013-2017 (1 Go postpayé sur ordinateur) n’est pas un forfait mobile : il est dans l’export, pas sur "
                              "le graphique.",
                              "One international price basket per line, each read separately: their definitions change, they are not joined. The 2013-2017 "
                              "basket (1 GB postpaid on a computer) is not a mobile plan: it is in the export, not on the chart."))
                pan = [("1,5 Go, data seule (2018-2020)", bi("1,5 Go", "1.5 GB"), "#8a8780", 2),
                       ("2 Go, data seule (2021-2024 ; publié jusqu'en 2025)", bi("2 Go", "2 GB"), CATEGORIELLE[1], 2),
                       ("5 Go, data seule (2025-)", bi("5 Go", "5 GB"), CATEGORIELLE[2], 2),
                       ("O2-05b : 1 Go de data mobile seule", bi("1 Go : indicateur retenu", "1 GB: indicator used"), BLEU_FONCE, 3.5)]
                fig = go.Figure()
                for col, nom, coul, ep in pan:
                    s = pa[col].dropna()
                    fig.add_scatter(x=s.index, y=s.values, mode="lines+markers", name=nom, line=dict(color=coul, width=ep),
                                    marker=dict(size=7, color=coul), hovertemplate=f"{nom} " + "%{x} : %{y:.2f} %<extra></extra>")
                fig.add_hline(y=SEUIL_PRIX, line=dict(color=ROUGE, width=1, dash="dash"),
                              annotation_text=bi(f"seuil d’accessibilité : {SEUIL_PRIX} %", f"affordability threshold: {SEUIL_PRIX}%"),
                              annotation_position="bottom right", annotation_font=dict(size=11, color=ROUGE))
                fig.add_annotation(x=a_p, y=c1go_n, text=f"<b>{pct(c1go_n, 2)}</b>", showarrow=False, xanchor="left", xshift=8,
                                   font=dict(size=12, color=BLEU_FONCE))
                habiller(fig, 380, " %", legende_y=-0.14, xaxis=dict(gridcolor="#efece4", dtick=1, range=[2017.6, a_p + 0.9]),
                         yaxis=dict(ticksuffix=" %", gridcolor="#efece4", rangemode="tozero"))
                tracer(fig, "prix_data")
                note(bi(f"Au rythme récent, le seuil de {SEUIL_PRIX} % serait atteint vers {int(r6.annee_cible_au_rythme_actuel)} "
                        f"(page {og}{t('page.projections')}{fg}).",
                        f"At the recent pace, the {SEUIL_PRIX}% threshold would be reached around {int(r6.annee_cible_au_rythme_actuel)} "
                        f"({og}{t('page.projections')}{fg} page)."))
                export_csv(paniers.reset_index(), "prix_data.csv", "export_prix")
        with g2:
            with st.container(border=True):
                titre_bloc(bi("Couverture théorique et réception déclarée, par région", "Theoretical coverage and reported reception, by region"),
                           bi("Couverture : part de la population à moins de 20 km d’une tour (proxy, 2021/2022). Réception : part de la "
                              "population des localités enquêtées où le premier réseau est bien capté (enquête auprès des ménages, 2021/22). Aucune des deux ne "
                              "mesure le signal.",
                              "Coverage: share of the population within 20 km of a tower (proxy, 2021/2022). Reception: share of the "
                              "population of surveyed localities where the first network is well received (household survey, 2021/22). Neither measures "
                              "the signal."))
                ordre = couv.couverture_ponderee_pop_pct.sort_values().index.tolist()
                noms = [region(r) for r in ordre]
                fig = go.Figure()
                fig.add_bar(y=noms, x=[couv.loc[r, "couverture_ponderee_pop_pct"] for r in ordre], orientation="h",
                            name=t("lib.couverture_theorique"), marker_color=CATEGORIELLE[0],
                            text=[pct(couv.loc[r, "couverture_ponderee_pop_pct"]) for r in ordre], textposition="outside",
                            textfont=dict(size=11, color=BLEU_FONCE), hovertemplate="%{y} : %{x:.1f} %<extra></extra>")
                fig.add_bar(y=noms, x=[rec1.get(r) for r in ordre], orientation="h",
                            name=bi("réception déclarée (premier réseau)", "reported reception (first network)"), marker_color=CATEGORIELLE[1],
                            text=[pct(rec1.get(r)) for r in ordre], textposition="outside", textfont=dict(size=11, color=BLEU_FONCE),
                            customdata=[[pct(rec2.get(r))] for r in ordre],
                            hovertemplate="%{y} : %{x:.1f} %" + bi(" (second réseau : %{customdata[0]})", " (second network: %{customdata[0]})")
                            + "<extra></extra>")
                habiller(fig, 380, legende_y=-0.1, barmode="group", bargap=0.25, bargroupgap=0.08,
                         xaxis=dict(ticksuffix=" %", gridcolor="#efece4", range=[0, 118]), yaxis=dict(gridcolor="#ffffff"))
                tracer(fig, "couverture_reception")
                note(bi("Qualité de service : non mesurée par territoire. Les sources institutionnelles complémentaires ne publient que des "
                        "valeurs nationales et une comparaison « Grand Lomé / reste du pays » : la couverture affichée reste théorique. "
                        f"La carte de la couverture, commune par commune, est sur la page {og}{t('page.carte')}{fg}.",
                        "Quality of service: not measured by territory. Complementary institutional sources only publish national values "
                        "and a “Greater Lomé / rest of the country” comparison: the coverage shown remains theoretical. The coverage "
                        f"map, commune by commune, is on the {og}{t('page.carte')}{fg} page."))
                export_csv(recep, "reception_declaree.csv", "export_reception")
        limite(bi("Prix : revenu national brut moyen par habitant, pas revenu médian ; pour un ménage modeste, la part est plus lourde. "
                  "Couverture : un proxy (rayon de 20 km autour des tours, toutes technologies confondues) ; "
                  f"{int(couv.non_determinables.sum())} communes ont une couverture inconnue. Réception : déclarée par la localité "
                  "enquêtée ; l’opérateur du « premier réseau » n’est pas nommé dans le fichier. Six régions seulement.",
                  "Price: average gross national income per capita, not median income; for a modest household, the share is heavier. "
                  "Coverage: a proxy (20 km radius around towers, all technologies combined); "
                  f"{int(couv.non_determinables.sum())} communes have unknown coverage. "
                  "Reception: reported by the surveyed locality; the operator of the “first network” is not named in the file. Six "
                  "regions only."))

pied()
