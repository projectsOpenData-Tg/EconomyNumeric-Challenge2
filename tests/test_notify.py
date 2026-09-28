"""Alerte de visite Telegram — `dashboard/notify.py` (repris du défi 1).

Aucun de ces tests ne touche le réseau : `_envoyer` est systématiquement remplacé. Ce qui
est vérifié, c'est la logique de déclenchement — inertie sans configuration, une seule
alerte par session, plafond quotidien, et surtout le fait qu'une défaillance de l'alerte
n'empêche jamais le tableau de bord de s'afficher.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
import streamlit as st

import notify


@pytest.fixture
def module(monkeypatch):
    """Le module avec son compteur remis à zéro et une session vierge."""
    notify._compteur["jour"] = None
    notify._compteur["envoyes"] = 0
    st.session_state.clear()
    return notify


@pytest.fixture
def actif(module, monkeypatch):
    """Configuration présente et envoi capturé — jamais émis."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "jeton-de-test")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "12345")
    envois = []
    monkeypatch.setattr(module, "_envoyer",
                        lambda jeton, destinataire, texte: envois.append(texte))
    # Le thread démon rendrait l'assertion dépendante de l'ordonnancement : on exécute la
    # cible immédiatement, dans le thread du test.
    monkeypatch.setattr(module.threading, "Thread",
                        lambda target, args, daemon: type(
                            "ThreadImmediat", (), {"start": lambda self: target(*args)})())
    return envois


def test_inerte_sans_variables_d_environnement(module, monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)
    assert module._configuration() is None
    module.signaler_visite()          # ne doit rien lever, ni rien envoyer


def test_une_seule_variable_ne_suffit_pas(module, monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "jeton")
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)
    assert module._configuration() is None


def test_une_seule_alerte_par_session(module, actif):
    module.signaler_visite()
    module.signaler_visite()
    module.signaler_visite()
    assert len(actif) == 1, "Streamlit réexécute le script à chaque interaction"


def test_chaque_nouveau_visiteur_est_signale(module, actif):
    module.signaler_visite()
    st.session_state.clear()          # nouvelle session
    module.signaler_visite()
    assert len(actif) == 2


def test_le_plafond_quotidien_borne_les_envois(module, actif):
    for _ in range(module._PLAFOND_QUOTIDIEN + 10):
        st.session_state.clear()
        module.signaler_visite()
    assert len(actif) == module._PLAFOND_QUOTIDIEN


def test_le_plafond_se_remet_a_zero_le_lendemain(module, actif):
    for _ in range(module._PLAFOND_QUOTIDIEN):
        st.session_state.clear()
        module.signaler_visite()
    assert len(actif) == module._PLAFOND_QUOTIDIEN
    # ⚠️ Le compteur raisonne en **UTC**, pas en heure locale. `date.today()` renvoie la
    # date locale : à 00 h 53 en UTC+2, elle vaut déjà le lendemain de la date UTC, et
    # « hier en local » désigne alors *aujourd'hui en UTC* — le test passait à côté de la
    # remise à zéro qu'il prétendait vérifier.
    veille = datetime.now(timezone.utc).date() - timedelta(days=1)
    module._compteur["jour"] = veille
    st.session_state.clear()
    module.signaler_visite()
    assert len(actif) == module._PLAFOND_QUOTIDIEN + 1


def test_l_ip_retenue_est_celle_ajoutee_par_le_routeur(module):
    """Heroku ajoute l'adresse qu'il observe **à la fin** ; les précédentes sont falsifiables."""
    entetes = {"X-Forwarded-For": "1.2.3.4, 5.6.7.8, 203.0.113.9"}
    assert module._adresse_client(entetes) == "203.0.113.9"


def test_ip_inconnue_sans_en_tete(module):
    assert module._adresse_client({}) == "inconnue"
    assert module._adresse_client({"X-Forwarded-For": ""}) == "inconnue"


def test_le_message_porte_le_titre_de_l_application(module):
    """Le titre est lu dans `i18n.py` : écrit en dur il finirait par diverger de l'interface."""
    from i18n import t
    assert t("topbar.brand").replace("&amp;", "&") in module._message()


def test_le_message_reste_produit_hors_contexte_http(module, monkeypatch):
    """`st.context` n'existe pas sous AppTest : son absence n'est pas une erreur."""
    monkeypatch.setattr(module, "_contexte", lambda: None)
    message = module._message()
    assert "Nouvelle visite" in message
    assert "IP" not in message


def test_les_entetes_trop_longs_sont_tronques(module, monkeypatch):
    class FauxContexte:
        headers = {"User-Agent": "M" * 5000, "X-Forwarded-For": "203.0.113.9"}
    monkeypatch.setattr(module.st, "context", FauxContexte())
    contexte = module._contexte()
    assert len(contexte["navigateur"]) == module._LONGUEUR_MAX_ENTETE


def test_signaler_visite_ne_leve_jamais(module, monkeypatch):
    """Une alerte défaillante ne doit pas empêcher le tableau de bord de s'afficher."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "jeton")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "12345")

    def _explose(*args, **kwargs):
        raise RuntimeError("panne simulée")

    monkeypatch.setattr(module, "_message", _explose)
    module.signaler_visite()          # aucune exception ne doit sortir
