"""Page 1 — Synthèse nationale : « Le numérique et l’inclusion financière au Togo : où en est-on ? » (plan visuel,
section 7, page 1).

Chiffres de tête nationaux (Internet, marché, prix, comptes) ; chiffres territoriaux filtrés (communes sans guichet,
suppléance, situations critiques), chacun lu comme une phrase avec sa réserve ; carte des priorités ; constat, lecture
des écarts, premières actions ; synthèse chiffrée ; ce que la page ne montre pas. Aucun chiffre n’est écrit en dur :
tout vient des tables du projet. Bilingue (section 3.3) : chaque texte est écrit deux fois, choisi avec `FR`.
"""
import html

import streamlit as st

from composants import (ariane, carte_kpi, carte_priorites, constat, entete, export_csv, limite, pied, rangee_kpi,
                        synthese)
from donnees import chiffres_nationaux, communes, contours, filtrer_communes, filtrer_prefectures, fr, lire, nombre, prefectures
from i18n import bi, langue, region, t

FR = langue() == "fr"

f = {"regions": st.session_state.f_regions, "priorites": st.session_state.f_priorites, "milieux": st.session_state.f_milieux}
actif = any(f.values())
N = chiffres_nationaux()
(n_comptes_actifs, n_cout_1go, n_cout_2pct_annee, n_cout_annee, n_dist_autres, n_dist_p1, n_haut_debit, n_haut_debit_annee,
 n_haut_debit_statut, n_hhi_min, n_marche_annee, n_togocom_data, n_usage, n_usage_2016, n_usage_annee, n_usage_ass,
 n_usage_var_recentes) = (N["comptes_actifs"], N["cout_1go"], N["cout_2pct_annee"], N["cout_annee"], N["dist_autres"],
                          N["dist_p1"], N["haut_debit"], N["haut_debit_annee"], N["haut_debit_statut"], N["hhi_min"],
                          N["marche_annee"], N["togocom_data"], N["usage"], N["usage_2016"], N["usage_annee"],
                          N["usage_ass"], N["usage_var_recentes"])
P, C = prefectures(), communes()
Pf, Cf = filtrer_prefectures(P, f), filtrer_communes(C, f)

p1 = Pf[Pf.priorite == "haute"]
sans_guichet = Cf[Cf.n_formels == 0]
maritime = {"Grand Lomé", "Maritime hors Grand Lomé"}
hors_maritime = len(p1) > 0 and not (set(p1.unite_regionale) & maritime)


def habitants(n) -> str:
    return nombre(n) + bi(" habitants", " inhabitants")


def rurales(df) -> str:
    if not len(df):
        return ""
    if (df.milieu == "Rural").all():
        return bi(", toutes rurales", ", all rural")
    return bi(f", dont {int((df.milieu == 'Rural').sum())} rurales", f", {int((df.milieu == 'Rural').sum())} of them rural")


def accord(n: int, singulier: str, pluriel: str) -> str:
    return pluriel if n > 1 else singulier


def s(n: int) -> str:  # marque du pluriel français ; l’anglais utilise accord() séparément
    return "s" if n > 1 else ""


# ----------------------------------------------------------------- En-tête
ariane(t("page.synthese"))
if hors_maritime and not actif:
    lieu = bi("Le déficit est rural et se situe hors du Maritime : ", "The gap is rural and outside the Maritime region: ")
elif actif:
    lieu = bi("Dans la sélection : ", "In the current selection: ")
else:
    lieu = ""
entete(t("page.synthese"),
       bi("Le numérique et l’inclusion financière au Togo : où en est-on ?",
          "Digital access and financial inclusion in Togo: where do things stand?"),
       f"{lieu}<strong>{len(p1)} {bi('préfecture', 'prefecture')}{s(len(p1))} {bi('en priorité haute', 'in high priority')}</strong> "
       f"({habitants(p1.pop_totale.sum())}), "
       f"{bi('et', 'and')} <strong>{len(sans_guichet)} {bi('commune', 'commune')}{s(len(sans_guichet))} "
       f"{bi('sans aucun guichet', 'with no formal service point at all')}</strong>, "
       f"{bi('où le mobile money est seul.', 'where mobile money is the only option.')}")
if actif:
    morceaux = [", ".join(region(r) for r in f["regions"]),
               ", ".join(t(f"priorite.{'non_classee' if p == 'non classée' else p}") for p in f["priorites"]),
               ", ".join(t(f"milieu.{m}") for m in f["milieux"])]
    st.markdown(f'<div class="filtres-actifs">{html.escape(t("filtres.actifs"))} : {html.escape(" · ".join(m for m in morceaux if m))}. '
                + html.escape(bi("Les chiffres nationaux (Internet, marché, prix, comptes) ne changent pas avec les filtres.",
                                "National figures (Internet, market, price, accounts) do not change with the filters."))
                + "</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------- Chiffres clés
sous_seuil = n_usage < 40
acquise = str(n_haut_debit_statut).startswith("acquise")
rangee_kpi(bi("Internet et marché des télécommunications (national)", "Internet and telecommunications market (national)"), [
    carte_kpi(bi(f"Internet ({n_usage_annee})", f"Internet ({n_usage_annee})"), f"{nombre(n_usage, 1)} %",
              bi("de la population utilise Internet", "of the population uses the Internet"),
              bi(f"seuil de 40 % ; Afrique subsaharienne : {nombre(n_usage_ass, 1)} %",
                 f"threshold: 40%; Sub-Saharan Africa: {nombre(n_usage_ass, 1)}%"),
              bi("Estimation internationale (UIT). Les enquêtes auprès des ménages en confirment la tendance, pas le niveau.",
                 "International estimate (ITU). Household surveys confirm the trend, not the level."),
              bi("Sous le seuil", "Below threshold") if sous_seuil else bi("Seuil franchi", "Threshold reached"),
              "alerte" if sous_seuil else "ok"),
    carte_kpi(bi(f"Haut débit mobile ({n_haut_debit_annee})", f"Mobile broadband ({n_haut_debit_annee})"),
              f"{nombre(n_haut_debit, 1)} %",
              bi("des abonnements data mobile sont en 3G ou 4G", "of mobile data subscriptions are 3G or 4G"),
              bi(f"passage au haut débit {'acquis' if acquise else 'non acquis'} en {n_haut_debit_annee} (seuil : 80 %)",
                 f"broadband transition {'reached' if acquise else 'not reached'} in {n_haut_debit_annee} (threshold: 80%)"),
              bi("Un abonnement n’est pas une personne : un usager peut avoir plusieurs cartes SIM.",
                 "A subscription is not a person: a user may hold several SIM cards."),
              bi("Seuil franchi", "Threshold reached") if acquise else bi("Sous le seuil", "Below threshold"),
              "ok" if acquise else "alerte"),
    carte_kpi(bi(f"Marché des télécoms ({n_marche_annee})", f"Telecom market ({n_marche_annee})"),
              bi("Duopole", "Duopoly"), bi("deux opérateurs se partagent le marché", "two operators share the market"),
              bi(f"Togocom (YAS) : {nombre(n_togocom_data, 1)} % des abonnés data ; indice de concentration "
                 + ("au-dessus de 5 000 chaque année" if n_hhi_min > 5000 else "élevé"),
                 f"Togocom (YAS): {nombre(n_togocom_data, 1)}% of data subscribers; concentration index "
                 + ("above 5,000 every year" if n_hhi_min > 5000 else "high")),
              "", bi("Très concentré", "Highly concentrated"), "alerte"),
    carte_kpi(bi(f"Prix de la data ({n_cout_annee})", f"Data price ({n_cout_annee})"), f"{nombre(n_cout_1go, 2)} %",
              bi("du revenu mensuel pour 1 Go de data mobile", "of monthly income for 1 GB of mobile data"),
              bi("seuil d’accessibilité international : 2 %", "international affordability threshold: 2%"),
              bi("Revenu moyen par habitant, pas revenu médian : pour un ménage modeste, la part est plus lourde.",
                 "Average income per capita, not median income: for a modest household, the share is heavier."),
              bi("Non abordable", "Not affordable") if n_cout_1go > 2 else bi("Abordable", "Affordable"),
              "alerte" if n_cout_1go > 2 else "ok"),
])

suppl = Cf[Cf.classe_O4_03 == "suppléance quasi totale"]
crit = Cf[Cf.cellule_critique]
seul = int((crit.statut_O4_05 == "mobile money uniquement").sum())
part_suppl = 100 * suppl.pop_totale.sum() / Cf.pop_totale.sum() if len(Cf) else 0
de_la_sel = bi(" de la sélection", " of the selection") if actif else ""
groupe2 = bi("Inclusion financière et territoires", "Financial inclusion and territories") + (bi(" (sélection)", " (selection)") if actif else "")
rangee_kpi(groupe2, [
    carte_kpi(bi("Mobile money (2024)", "Mobile money (2024)"), f"{nombre(n_comptes_actifs, 1)} %",
              bi("des comptes mobile money sont actifs", "of mobile money accounts are active"),
              bi("la moitié des comptes ouverts dort ; chiffre national" if n_comptes_actifs < 50 else "chiffre national",
                 "half of opened accounts are dormant; national figure" if n_comptes_actifs < 50 else "national figure"),
              bi("Compte actif : au moins une transaction en 90 jours (définition de la BCEAO).",
                 "Active account: at least one transaction in 90 days (BCEAO definition)."),
              bi("Usage faible", "Low activity") if n_comptes_actifs < 50 else None, "alerte"),
    carte_kpi(bi("Guichets (2021/2022)", "Service points (2021/2022)"), fr(len(sans_guichet)),
              accord(len(sans_guichet), bi("n’a ni banque, ni IMF, ni assurance", "has no bank, MFI or insurer"),
                     bi("n’ont ni banque, ni IMF, ni assurance", "have no bank, MFI or insurer")),
              f"{habitants(sans_guichet.pop_totale.sum())}{rurales(sans_guichet)} ; "
              + (bi("aucun DAB non plus : ", "no ATM either: ") if sans_guichet.n_dab.sum() == 0 else "")
              + bi("le mobile money y est seul", "mobile money is the only option there"),
              bi("Point formel : banque, institution de microfinance (IMF) ou assurance, recensés en 2021/2022.",
                 "Formal point: bank, microfinance institution (MFI) or insurer, surveyed in 2021/2022."),
              t("priorite.absolue") if len(sans_guichet) else None, "critique",
              accord(len(sans_guichet), bi("commune", "commune"), bi("communes", "communes"))),
    carte_kpi(bi("Mobile money et guichets", "Mobile money and service points"), fr(len(suppl)),
              bi("où le mobile money remplace presque tous les guichets", "where mobile money replaces almost all service points"),
              bi(f"{nombre(part_suppl, 1)} % de la population{de_la_sel} ; plus de 20 points de service pour un guichet ; "
                 "en plus des communes sans guichet",
                 f"{nombre(part_suppl, 1)}% of the population{de_la_sel}; over 20 service points per formal point; "
                 "in addition to communes with no service point"),
              bi("On compte des points de service, pas des agents.", "These are service points, not agents."),
              bi("Guichet rare", "Scarce service point") if len(suppl) else None, "alerte",
              accord(len(suppl), bi("commune", "commune"), bi("communes", "communes"))),
    carte_kpi(bi("Réseau et mobile money", "Network and mobile money"), fr(len(crit)),
              accord(len(crit), bi("cumule mobile money seul ou dominant et couverture réseau faible",
                                   "combines mobile money alone or dominant with weak network coverage"),
                     bi("cumulent mobile money seul ou dominant et couverture réseau faible",
                        "combine mobile money alone or dominant with weak network coverage")),
              bi(f"{habitants(crit.pop_totale.sum())} ; couverture sous 50 %", f"{habitants(crit.pop_totale.sum())}; coverage below 50%")
              + (bi(f" ; mobile money seul dans {seul}, dominant dans {len(crit) - seul}",
                    f"; mobile money alone in {seul}, dominant in {len(crit) - seul}") if len(crit) else ""),
              bi("Couverture théorique (rayon de 20 km autour des antennes), à confirmer par des mesures.",
                 "Theoretical coverage (20 km radius around antennas), to be confirmed by measurement."),
              bi("À confirmer", "To confirm") if len(crit) else None, "neutre",
              accord(len(crit), bi("commune", "commune"), bi("communes", "communes"))),
])

st.write("")

# ----------------------------------------------------------------- Où sont les problèmes ? Pourquoi ? Quelle action ?
gauche, droite = st.columns([1.12, 1], gap="large")
with gauche:
    with st.container(border=True):
        st.markdown(f'<div class="bloc-titre">{html.escape(bi("Où sont les territoires prioritaires ?", "Where are the priority territories?"))}</div>'
                    f'<div class="bloc-sous-titre">{html.escape(bi("Classe de priorité (accès aux guichets, maillage mobile money, couverture théorique) ; en ocre, les communes où le mobile money est seul.", "Priority class (access to service points, mobile money network, theoretical coverage); in ochre, communes where mobile money is the only option."))}</div>',
                    unsafe_allow_html=True)
        mmu = Cf[Cf.priorite_absolue]
        if st.session_state.f_maille == "Commune":
            tt = C.rename(columns={"priorite_prefecture": "priorite"})
            carte_priorites(contours("communes"), tt, "carte_synthese_c", set(Cf.code), mmu, contours("communes"))
        else:
            carte_priorites(contours("prefectures"), P, "carte_synthese_p", set(Pf.code), mmu, contours("communes"))
        tableau = Pf[["nom", "unite_regionale", "priorite", "pop_totale", "communes_sans_point_formel"]].rename(columns={
            "nom": bi("préfecture", "prefecture"), "unite_regionale": bi("région", "region"), "priorite": bi("priorité", "priority"),
            "pop_totale": bi("habitants", "population"), "communes_sans_point_formel": bi("communes sans guichet", "communes with no service point")})
        export_csv(tableau, "priorites_prefectures.csv", "export_synthese_carte")

with droite:
    if not actif:
        regions = ", ".join(sorted(region(r) for r in set(p1.unite_regionale)))
        tests = [c for c in P if c.startswith("classe_test_poids")]
        stables = (p1[tests] == "priorité 1").all().all() if tests else False
        texte = ((bi("Aucune préfecture du Maritime ni du Grand Lomé n’est en priorité haute. ",
                     "No prefecture in the Maritime region or Greater Lomé is in high priority. ") if hors_maritime else "")
                 + bi(f"Les {len(p1)} préfectures en priorité haute sont dans : {html.escape(regions)}",
                     f"The {len(p1)} high-priority prefectures are in: {html.escape(regions)}")
                 + (bi(", et le restent sous tous les poids testés.", ", and stay so under every weighting tested.") if stables else "."))
    elif len(p1):
        texte = bi(f"Dans la sélection, {len(p1)} préfecture{s(len(p1))} en priorité haute : {html.escape(', '.join(p1.nom))}.",
                  f"In the selection, {len(p1)} high-priority prefecture{'s' if len(p1) > 1 else ''}: {html.escape(', '.join(p1.nom))}.")
    else:
        texte = bi("Aucune préfecture de la sélection n’est en priorité haute.", "No prefecture in the selection is in high priority.")
    constat(texte)

    with st.container(border=True):
        var = n_usage_var_recentes
        rythme = bi("moins de 2 points par an", "less than 2 points a year") if var < 2 else bi(f"jusqu’à {nombre(var, 1)} points par an", f"up to {nombre(var, 1)} points a year")
        st.markdown(
            f'<div class="bloc-titre">{html.escape(bi("Pourquoi ces écarts ?", "Why these gaps?"))}</div><ol class="ecarts">'
            f'<li><span class="num">1</span><div><strong>{html.escape(bi("L’usage progresse mais ralentit.", "Use is growing but slowing down."))}</strong> '
            + bi(f"Il a été multiplié par {nombre(n_usage / n_usage_2016, 1)} depuis 2016 (de {nombre(n_usage_2016, 1)} % à {nombre(n_usage, 1)} %), "
                f"mais il a gagné {rythme} en {n_usage_annee - 1} et en {n_usage_annee}.",
                f"It has multiplied {nombre(n_usage / n_usage_2016, 1)}× since 2016 (from {nombre(n_usage_2016, 1)}% to {nombre(n_usage, 1)}%), "
                f"but gained {rythme} in {n_usage_annee - 1} and {n_usage_annee}.")
            + '</div></li>'
            f'<li><span class="num">2</span><div><strong>{html.escape(bi("Hors des villes, le guichet est loin.", "Outside towns, the service point is far away."))}</strong> '
            + bi(f"Dans les préfectures en priorité haute, {fr(n_dist_p1)} % des points mobile money sont à plus de 10 km d’un guichet (médiane), contre {fr(n_dist_autres)} % ailleurs.",
                f"In high-priority prefectures, {fr(n_dist_p1)}% of mobile money points are more than 10 km from a service point (median), against {fr(n_dist_autres)}% elsewhere.")
            + '</div></li>'
            f'<li><span class="num">3</span><div><strong>{html.escape(bi("Le prix freine l’usage.", "Price holds back use."))}</strong> '
            + bi(f"1 Go coûte {nombre(n_cout_1go, 2)} % du revenu mensuel. Au rythme récent, le seuil de 2 % ne serait atteint que vers {n_cout_2pct_annee}.",
                f"1 GB costs {nombre(n_cout_1go, 2)}% of monthly income. At the recent pace, the 2% threshold would only be reached around {n_cout_2pct_annee}.")
            + '</div></li></ol>', unsafe_allow_html=True)

    with st.container(border=True):
        sr = lire("10_recommandations", "synthese_recommandations").set_index("id")
        actions = [("R1", bi(f"Ouvrir un premier guichet formel dans chacune des {len(C[C.priorite_absolue])} communes où le mobile money est seul",
                             f"Open a first formal service point in each of the {len(C[C.priorite_absolue])} communes where mobile money is the only option"),
                    t("priorite.absolue"), "critique"),
                   ("R4a", bi(f"Mesurer la couverture réelle dans {sr.loc['R4a', 'territoires']} où elle est inconnue ou douteuse",
                             f"Measure actual coverage in {sr.loc['R4a', 'territoires']} where it is unknown or doubtful"),
                    bi("Préalable au réseau", "Network prerequisite"), "ok"),
                   ("R2", bi(f"Ajouter guichets et points mobile money dans les {sr.loc['R2', 'territoires']} prioritaires",
                            f"Add service points and mobile money points in the {sr.loc['R2', 'territoires']} priority ones"),
                    t("priorite.haute"), "ok")]
        blocs = "".join(
            f'<div class="action"><div class="action-titre">{html.escape(titre)}</div><div class="action-meta">'
            f'<span class="etiquette {ton}">{badge}</span><span class="etiquette neutre">{sr.loc[i, "horizon"]}</span>'
            f'<span>{habitants(sr.loc[i, "population"])}</span></div></div>' for i, titre, badge, ton in actions)
        st.markdown(f'<div class="bloc-titre">{html.escape(bi("Quelle action engager d’abord ?", "What action to take first?"))}</div>{blocs}',
                    unsafe_allow_html=True)
        pages = st.session_state.get("pages", {})
        if "recommandations" in pages:
            st.page_link(pages["recommandations"], label=bi(f"Voir les {len(sr)} recommandations", f"See all {len(sr)} recommendations"),
                        icon=":material/arrow_forward:")

# ----------------------------------------------------------------- Synthèse chiffrée, limite, sources
classees = Pf[Pf.priorite != "non classée"]
part = 100 * p1.pop_totale.sum() / classees.pop_totale.sum() if len(classees) else 0
par_region = ", ".join(f"{region(r)} ({n})" for r, n in p1.unite_regionale.value_counts().sort_index().items())
nc = Pf[(Pf.priorite == "non classée") & (Pf.sans_couv_classe == "priorité 1")]
puces = []
if len(p1):
    puces.append(f"<strong>{html.escape(bi('Hors du Maritime.', 'Outside the Maritime region.') if hors_maritime else bi('Où ?', 'Where?'))}</strong> "
                 + bi(f"Les préfectures en priorité haute sont dans : {html.escape(par_region)}.",
                     f"The high-priority prefectures are in: {html.escape(par_region)}."))
puces.append(f"<strong>{html.escape(bi('Le mobile money est partout, le guichet non.', 'Mobile money is everywhere, the service point is not.'))}</strong> "
             + bi(f"{len(sans_guichet)} communes n’ont que lui : {habitants(sans_guichet.pop_totale.sum())}{rurales(sans_guichet)}.",
                 f"{len(sans_guichet)} communes only have it: {habitants(sans_guichet.pop_totale.sum())}{rurales(sans_guichet)}."))
if len(nc):
    puces.append(f"<strong>{html.escape(bi('Préfectures sans couverture connue.', 'Prefectures with no known coverage.'))}</strong> "
                 + bi(f"{html.escape(', '.join(nc.nom))} ne sont pas classées ; sur les deux autres mesures, elles seraient en priorité haute.",
                     f"{html.escape(', '.join(nc.nom))} are not ranked; on the other two measures, they would be in high priority."))
synthese(nombre(p1.pop_totale.sum()),
        bi(f"habitants vivent dans une des {len(p1)} préfectures en priorité haute ({nombre(part, 1)} % de la population classée{de_la_sel})",
           f"people live in one of the {len(p1)} high-priority prefectures ({nombre(part, 1)}% of ranked population{de_la_sel})"),
        puces)

# Les réserves sont déjà sous chaque chiffre : le bandeau du bas dit seulement ce que la page ne montre pas
limite(bi("Les usages : Internet et mobile money ne sont mesurés que pour le pays et les régions, pas commune par commune. "
         "L’état actuel des points de service : ils ont été recensés en 2021/2022. Le détail est sur les pages « Internet : usage et "
         "marché », « Offre financière » et « Sources et méthode ».",
         "Usage: Internet and mobile money are only measured for the country and the regions, not commune by commune. "
         "The current state of service points: they were surveyed in 2021/2022. Details are on the \"Internet: use and market\", "
         "\"Financial services\" and \"Sources and method\" pages."),
       titre=t("bloc.ne_montre_pas"), discret=True)
pied()
