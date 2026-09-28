"""Alerte Telegram à l'ouverture du tableau de bord (repris du défi 1).

Une notification par visite, envoyée à un bot Telegram privé. L'usage visé est de savoir qu'un jury ou un partenaire a
ouvert le tableau de bord, pas de faire de la mesure d'audience : à la première dizaine de visiteurs simultanés, ce
mécanisme devient du bruit et il faudra lui substituer un récapitulatif quotidien.

Ce module s'exécute dans le processus Streamlit du dyno, **pas dans la CI**. Aucun workflow GitHub ne peut le remplacer :
un runner ne voit pas les connexions au site, il ne pourrait qu'interroger l'URL de l'extérieur, ce qui répond à « le
site est-il debout ? », pas à « quelqu'un l'a-t-il ouvert ? ».

Activation par variables d'environnement, jamais par le code :

    TELEGRAM_BOT_TOKEN   jeton donné par @BotFather
    TELEGRAM_CHAT_ID     identifiant de la conversation destinataire

Les deux absentes (poste de développement, CI), le module ne fait strictement rien : aucun réseau sollicité pendant
`pytest`.

Quatre points ont dicté cette implémentation :

  * Streamlit réexécute le script en entier à chaque interaction. Sans le drapeau posé dans `st.session_state`, chaque
    changement de filtre de la barre latérale enverrait une notification. Le dédoublonnage est par session, pas par
    exécution.

  * L'envoi part dans un thread démon. Un `api.telegram.org` lent ou injoignable retarderait sinon le premier rendu de
    la page d'autant : le visiteur paierait la notification. Démon pour ne pas retenir le dyno au moment d'un arrêt.

  * Plafond quotidien. Un robot qui ouvre des sessions en rafale ne doit pouvoir saturer ni la conversation Telegram,
    ni le quota d'API du bot.

  * `urllib` de la bibliothèque standard, pas `requests`. Le déploiement installe `requirements-runtime.txt`, tenu
    synchronisé avec `requirements.txt` par la CI : n'ajouter aucune dépendance évite de toucher à ce couple pour une
    fonction annexe.
"""
from __future__ import annotations

import os
import sys
import threading
import urllib.parse
import urllib.request
from datetime import datetime, timezone

import streamlit as st

from i18n import t

_ENDPOINT = "https://api.telegram.org/bot{token}/sendMessage"

# Au-delà, l'appel est abandonné. Le thread est démon, mais un socket sans délai d'expiration resterait ouvert
# indéfiniment.
_DELAI = 5

# Compté par journée UTC, remis à zéro au premier envoi du jour suivant.
_PLAFOND_QUOTIDIEN = 50

# Les en-têtes d'un navigateur dépassent facilement le raisonnable ; tronqués pour garder le message lisible sur un
# téléphone.
_LONGUEUR_MAX_ENTETE = 180

_CLE_SESSION = "_visite_signalee"

# Compteur partagé par toutes les sessions du processus. Les globales d'un module importé survivent aux réexécutions du
# script (`sys.modules` le garde en cache), là où celles d'`app.py` sont reconstruites à chaque fois. Verrou car les
# sessions Streamlit sont servies par des threads distincts.
_verrou = threading.Lock()
_compteur = {"jour": None, "envoyes": 0}


def _configuration():
    """(jeton, destinataire) si les deux variables sont définies, sinon None.

    Lues à l'appel et non à l'import : un `heroku config:set` suivi du redémarrage automatique du dyno suffit à activer
    les alertes, et les tests peuvent les poser ou les retirer sans jouer sur l'ordre des imports.
    """
    jeton = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    destinataire = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not jeton or not destinataire:
        return None
    return jeton, destinataire


def _quota_disponible():
    """Consomme une unité du plafond du jour. False si le plafond est atteint."""
    aujourdhui = datetime.now(timezone.utc).date()
    with _verrou:
        if _compteur["jour"] != aujourdhui:
            _compteur["jour"] = aujourdhui
            _compteur["envoyes"] = 0
        if _compteur["envoyes"] >= _PLAFOND_QUOTIDIEN:
            return False
        _compteur["envoyes"] += 1
        return True


def _adresse_client(entetes):
    """Adresse IP du visiteur, extraite de `X-Forwarded-For`.

    Le routeur Heroku *ajoute* l'adresse qu'il observe à la fin de l'en-tête, en conservant ce que le client aurait pu
    y mettre lui-même. La dernière valeur est donc la seule que Heroku garantit ; les précédentes sont déclaratives et
    falsifiables.
    """
    transmis = entetes.get("X-Forwarded-For", "")
    if not transmis:
        return "inconnue"
    return transmis.split(",")[-1].strip() or "inconnue"


def _contexte():
    """En-têtes de la requête du visiteur, ou None hors contexte HTTP.

    `st.context` n'est pas disponible dans toutes les situations d'exécution : l'`AppTest` des tests n'ouvre aucune
    connexion réelle. Son absence n'est pas une erreur, elle produit simplement une notification sans détail.
    """
    try:
        entetes = st.context.headers or {}
    except Exception:
        return None
    return {
        "ip": _adresse_client(entetes),
        "navigateur": (entetes.get("User-Agent") or "inconnu")[:_LONGUEUR_MAX_ENTETE],
        "provenance": (entetes.get("Referer") or "accès direct")[:_LONGUEUR_MAX_ENTETE],
    }


def _titre_application():
    """Le nom de l'application, lu dans `i18n.py` comme le titre de l'onglet du navigateur (`app.py`).

    Écrit en dur, il finirait par désigner autre chose que ce que porte l'interface. Le nom est le même dans les deux
    langues : la notification part vers une conversation privée, elle ne suit pas la langue du visiteur.
    """
    return t("topbar.brand").replace("&amp;", "&")


def _message():
    horodatage = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lignes = [f"📊 Nouvelle visite — {_titre_application()}", horodatage]
    contexte = _contexte()
    if contexte:
        lignes += [
            "",
            f"IP          : {contexte['ip']}",
            f"Navigateur  : {contexte['navigateur']}",
            f"Provenance  : {contexte['provenance']}",
        ]
    return "\n".join(lignes)


def _envoyer(jeton, destinataire, texte):
    """Appelle l'API Telegram. Toute erreur est journalisée, jamais propagée.

    Ce thread s'exécute hors de tout contexte Streamlit : une exception qui en sortirait ne remonterait nulle part
    d'utile. On écrit sur stderr, que `heroku logs` capture : de quoi diagnostiquer un jeton révoqué sans que le
    visiteur voie quoi que ce soit.

    Texte brut, sans `parse_mode` : un en-tête de navigateur contenant `_` ou `*` ferait échouer l'analyse Markdown
    côté Telegram et perdre la notification.
    """
    charge = urllib.parse.urlencode({
        "chat_id": destinataire,
        "text": texte,
        "disable_web_page_preview": "true",
    }).encode("utf-8")
    requete = urllib.request.Request(_ENDPOINT.format(token=jeton), data=charge)
    try:
        with urllib.request.urlopen(requete, timeout=_DELAI):
            pass
    except Exception as erreur:
        print(f"[notify] envoi Telegram impossible : {erreur}", file=sys.stderr)


def signaler_visite():
    """Signale l'ouverture d'une session, au plus une fois par visiteur.

    Sans effet si les variables d'environnement sont absentes ou si le plafond quotidien est atteint. Ne lève jamais :
    une alerte défaillante ne doit pas empêcher le tableau de bord de s'afficher.
    """
    try:
        if st.session_state.get(_CLE_SESSION):
            return
        # Posé avant toute autre chose : même désactivée ou plafonnée, la session ne retentera pas à la réexécution
        # suivante.
        st.session_state[_CLE_SESSION] = True

        configuration = _configuration()
        if configuration is None or not _quota_disponible():
            return

        jeton, destinataire = configuration
        threading.Thread(
            target=_envoyer,
            args=(jeton, destinataire, _message()),
            daemon=True,
        ).start()
    except Exception as erreur:
        print(f"[notify] alerte de visite ignorée : {erreur}", file=sys.stderr)
