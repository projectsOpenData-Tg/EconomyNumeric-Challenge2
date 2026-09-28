"""Page 8 — Recommandations : « Quelle action engager ? » (plan visuel, section 8).

12 recommandations, en cartes ; filtres par thème, priorité, nature, horizon ; vue d’ensemble sans addition de
populations qui se recoupent ; carte par thème."""
import html

import pandas as pd
import streamlit as st

from composants import ariane, entete, export_csv, limite, pied
from donnees import ANALYSE, communes, contours, lire, nombre, prefectures
from i18n import bi, langue, t

FR = langue() == "fr"
s = lire("10_recommandations", "synthese_recommandations").set_index("id")
C, P = communes(), prefectures()

THEME = {"R1": "formels", "R2": "formels", "R3": "mm", "R4a": "couverture", "R4b": "couverture", "R5": "prix",
        "R6": "prix", "R7": "competences", "R7b": "competences", "R8": "investissement", "R9": "fibre", "R10": "investissement"}
LIB_THEME = {"formels": bi("Points formels", "Formal points"), "mm": bi("Mobile money", "Mobile money"),
            "couverture": bi("Couverture réseau", "Network coverage"), "fibre": bi("Fibre", "Fibre"),
            "prix": bi("Prix et frais", "Price and fees"), "competences": bi("Compétences et équipement", "Skills and equipment"),
            "investissement": bi("Investissement (veille)", "Investment (watch)")}
TITRE = {
    "R1": bi("Un premier guichet formel dans chacune des 22 communes où le mobile money est seul",
            "A first formal service point in each of the 22 communes where mobile money is the only option"),
    "R2": bi("Des guichets formels dans les 10 préfectures prioritaires", "Formal service points in the 10 priority prefectures"),
    "R3": bi("Des points de service mobile money là où le réseau est mince", "Mobile money service points where the network is thin"),
    "R4a": bi("Mesurer la couverture réelle dans 14 communes", "Measure actual coverage in 14 communes"),
    "R4b": bi("Étendre le réseau dans 6 préfectures prioritaires", "Extend the network in 6 priority prefectures"),
    "R5": bi("Ramener les frais du petit retrait sous 3 %", "Bring small-withdrawal fees below 3%"),
    "R6": bi("Ramener le coût de 1 Go sous 2 % du revenu", "Bring the cost of 1 GB below 2% of income"),
    "R7": bi("Relever les compétences numériques dans les Savanes et les Plateaux", "Raise digital skills in Savanes and Plateaux"),
    "R7b": bi("Réduire le frein de coût sur le smartphone", "Reduce the smartphone cost barrier"),
    "R8": bi("Garder l’investissement au-dessus de 15 % du chiffre d’affaires", "Keep investment above 15% of revenue"),
    "R9": bi("Étendre la fibre aux 8 préfectures non raccordées", "Extend fibre to the 8 unconnected prefectures"),
    "R10": bi("Relancer les ajouts nets de sites radio", "Revive net radio-site additions"),
}
PRIO_BADGE = {"R1": t("priorite.absolue"), "R2": t("priorite.haute"), "R3": t("priorite.haute"), "R4a": bi("Préalable", "Prerequisite"),
             "R4b": t("priorite.haute"), "R5": bi("National", "National"), "R6": bi("National", "National"),
             "R7": t("priorite.haute"), "R7b": bi("National", "National"), "R8": bi("National", "National"),
             "R9": t("priorite.haute"), "R10": bi("National", "National")}

ariane(t("page.recommandations"))
entete(t("page.recommandations"), bi("Quelle action engager ?", "What action to take?"),
       bi(f"<strong>{len(s)} recommandations</strong>, réparties en 7 thèmes, du guichet manquant au prix de la data.",
          f"<strong>{len(s)} recommendations</strong>, across 7 themes, from the missing service point to the price of data."))

# ----------------------------------------------------------------- Niveau 1 : filtres
themes_dispo = sorted(set(LIB_THEME[v] for v in THEME.values()))
c1, c2, c3 = st.columns(3)
choisir = bi("Tous", "All")
f_theme = c1.multiselect(bi("Thème", "Theme"), themes_dispo, key="reco_theme", placeholder=choisir)
f_nature = c2.multiselect(bi("Nature", "Nature"), sorted(s.nature.unique()), key="reco_nature", placeholder=choisir)
f_horizon = c3.multiselect(bi("Horizon", "Horizon"), sorted(s.horizon.unique()), key="reco_horizon", placeholder=choisir)

sf = s.copy()
sf["theme_lib"] = [LIB_THEME[THEME[i]] for i in sf.index]
if f_theme:
    sf = sf[sf.theme_lib.isin(f_theme)]
if f_nature:
    sf = sf[sf.nature.isin(f_nature)]
if f_horizon:
    sf = sf[sf.horizon.isin(f_horizon)]

# ----------------------------------------------------------------- Niveau 2 : vue d’ensemble (jamais d’addition d’habitants qui se recoupent)
n22 = int(C.priorite_absolue.sum())
pop22 = int(C[C.priorite_absolue].pop_totale.sum())
p1 = P[P.priorite == "haute"]
st.markdown(f'<div class="filtres-actifs">'
            f'{len(sf)} {bi("recommandations", "recommendations")} · '
            f'{n22} {bi("communes en priorité absolue", "absolute-priority communes")} ({nombre(pop22)} {bi("habitants", "people")}) · '
            f'{len(p1)} {bi("préfectures prioritaires", "priority prefectures")} ({nombre(int(p1.pop_totale.sum()))} {bi("habitants", "people")}) · '
            f'{int((s.nature=="conditionnelle").sum())} {bi("action conditionnelle", "conditional action")} · '
            f'{int((s.nature=="veille").sum())} {bi("veilles", "watch items")}'
            f'</div>', unsafe_allow_html=True)
st.caption(bi("Les habitants ne sont jamais additionnés d’une recommandation à l’autre : les territoires se recoupent.",
             "People are never added up from one recommendation to another: territories overlap."))

# ----------------------------------------------------------------- Niveau 3 : cartes de recommandation
st.write("")
cols = st.columns(3)
for i, (idx, row) in enumerate(sf.iterrows()):
    with cols[i % 3]:
        with st.container(border=True, key=f"carte_reco_{idx}"):
            st.markdown(f'<div class="action-titre" style="font-size:0.7rem;color:#0d366b;text-transform:uppercase;letter-spacing:0.05em">{html.escape(row.theme_lib)}</div>'
                        f'<div class="action-titre" style="min-height:3.4rem">{html.escape(TITRE[idx])}</div>'
                        f'<div class="kpi-phrase" style="margin:6px 0">{html.escape(str(row.cible))}</div>'
                        f'<div class="kpi-contexte">{html.escape(str(row.territoires))} · {nombre(int(row.population))} {bi("habitants concernés", "people concerned")}</div>'
                        f'<div class="action-meta" style="margin-top:8px">'
                        f'<span class="etiquette {"critique" if idx=="R1" else "reco-priorite"}">{html.escape(PRIO_BADGE[idx])}</span>'
                        f'<span class="etiquette reco-nature">{html.escape(row.nature)}</span>'
                        f'<span class="etiquette reco-horizon">{html.escape(row.horizon)}</span></div>', unsafe_allow_html=True)

export_csv(sf.reset_index()[["id", "territoires", "population", "nature", "horizon", "cible"]], "recommandations.csv", "export_recos")

# ----------------------------------------------------------------- Niveau 4 : carte par thème
st.write("")
with st.container(border=True):
    st.markdown(f'<div class="bloc-titre">{html.escape(bi("Priorité des territoires visés par les recommandations", "Priority of the territories targeted by the recommendations"))}</div>'
                f'<div class="bloc-sous-titre">{html.escape(bi("Classe de priorité de chaque préfecture ; en ocre, les 22 communes en priorité absolue.", "Priority class of each prefecture; in ochre, the 22 absolute-priority communes."))}</div>',
                unsafe_allow_html=True)
    from composants import carte_priorites
    carte_priorites(contours("prefectures"), P, "carte_recos", set(P.code), C[C.priorite_absolue], contours("communes"))

# ----------------------------------------------------------------- Blocs complémentaires
st.write("")
with st.container(border=True):
    st.markdown(f'<div class="bloc-titre">{html.escape(bi("Ordre d’action", "Order of action"))}</div>', unsafe_allow_html=True)
    ordre = [(1, "R1", bi("D’abord : sortir les 22 communes du statut « mobile money uniquement ».", "First: get the 22 communes out of the \"mobile money only\" status.")),
            (2, "R4a", bi("Ensuite : mesurer la couverture avant toute extension.", "Then: measure coverage before any extension.")),
            (3, "R2,R3,R9", bi("Puis : guichets, points mobile money et fibre dans les préfectures prioritaires.", "Then: service points, mobile money points and fibre in priority prefectures.")),
            (4, "R4b,R5,R6,R7,R7b,R8,R10", bi("Enfin : extension conditionnelle, prix, compétences et veille.", "Finally: conditional extension, price, skills and watch items."))]
    for rang, ids, texte in ordre:
        st.markdown(f'<div class="action"><span class="etiquette ok">{rang}</span> <strong>{ids}</strong> — {html.escape(texte)}</div>', unsafe_allow_html=True)

with st.container(border=True):
    st.markdown(f'<div class="bloc-titre">{html.escape(bi("Qui agit ?", "Who acts?"))}</div>'
                f'<div class="bloc-sous-titre">{html.escape(bi("Fondement vérifié sur sources publiques (journal de recherche, section 18).", "Grounding verified from public sources (research log, section 18)."))}</div>',
                unsafe_allow_html=True)
    acteurs = pd.DataFrame([
        (bi("Banques", "Banks"), "R1, R2", bi("Commission bancaire de l’UMOA (BCEAO)", "UMOA Banking Commission (BCEAO)")),
        (bi("IMF", "MFIs"), "R1, R2", bi("Loi 2011-009 ; BCEAO ; Commission bancaire de l’UMOA", "Law 2011-009; BCEAO; UMOA Banking Commission")),
        (bi("Émetteurs de monnaie électronique", "E-money issuers"), "R3, R5", bi("Agrément BCEAO (instruction 008-05-2015)", "BCEAO licensing (instruction 008-05-2015)")),
        (bi("Assurances", "Insurers"), "R2", bi("Code CIMA ; CRCA", "CIMA code; CRCA")),
        (bi("Société d’infrastructures numériques (SIN)", "Digital Infrastructure Company (SIN)"), "R9", bi("Décret 2016-166/PR ; coentreprise CSquared Woezon", "Decree 2016-166/PR; CSquared Woezon joint venture")),
        (bi("Fonds du service universel (ARCEP)", "Universal Service Fund (ARCEP)"), "R4b, R8", bi("Décret 2018-070/PR", "Decree 2018-070/PR")),
        (bi("Ministère chargé du numérique", "Ministry in charge of digital affairs"), "R7, R7b, R8", bi("Stratégie Togo Digital 2025-2030", "Togo Digital 2025-2030 strategy")),
    ], columns=[bi("acteur", "actor"), bi("recommandations", "recommendations"), bi("fondement", "grounding")])
    st.dataframe(acteurs, hide_index=True, use_container_width=True)

with st.container(border=True):
    st.markdown(f'<div class="bloc-titre">{html.escape(bi("Ce qui n’est pas recommandé", "What is not recommended"))}</div>', unsafe_allow_html=True)
    nr = pd.read_csv(ANALYSE / "10_recommandations" / "non_retenues.csv")
    st.dataframe(nr.rename(columns={"piste": bi("piste", "option"), "statut": bi("statut", "status"), "raison": bi("raison", "reason")}),
                hide_index=True, use_container_width=True)

limite(bi("Les scénarios ne disent pas quel levier produit quel rythme : les événements passés sont des coïncidences, pas des causes. "
         "Les habitants concernés ne sont jamais additionnés d’une carte à l’autre.",
         "The scenarios do not say which lever produces which pace: past events are coincidences, not causes. People concerned "
         "are never added up from one card to another."))
pied()
