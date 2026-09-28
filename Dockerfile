# Image de production du tableau de bord — déployée sur Heroku via le Container Registry,
# comme au défi 1.
#
# Pourquoi Docker plutôt qu'un buildpack : le dépôt pèse plusieurs centaines de mégaoctets
# (dont 491 Mo de données brutes dans `data/raw/`) quand l'image n'a besoin que des tables
# publiées et des contours. La préparation (`prep/`), les analyses (`analyse/`), leurs
# figures et les documents de méthode n'ont rien à faire en production. Le découpage
# requirements.txt / requirements-runtime.txt n'a de sens que si le build l'applique.
#
# Architecture : les dynos Heroku sont en amd64. La CI construit sur des runners amd64, donc
# nativement. Pour un push manuel depuis un poste ARM, ajoutez `--platform linux/amd64` à la
# commande de build, sans quoi Heroku refusera l'image.

FROM python:3.11-slim-bookworm

# PYTHONUNBUFFERED : sans lui, la sortie de Streamlit est bufferisée et `heroku logs`
# n'affiche rien tant que le tampon n'est pas plein.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Les dépendances d'abord, le code ensuite : tant que requirements-runtime.txt ne change
# pas, cette couche est réutilisée et une page modifiée ne réinstalle pas pandas.
#
# Aucun paquet système n'est nécessaire : geopandas lit les GeoJSON par pyogrio, dont la
# roue embarque GDAL ; pyproj embarque PROJ.
COPY requirements-runtime.txt ./
RUN pip install --no-cache-dir -r requirements-runtime.txt

# Thème, service des fichiers statiques (armoiries, logos) et mode sans navigateur.
# Streamlit lit ce fichier relativement au répertoire courant : d'où le WORKDIR /app et le
# lancement depuis la racine, comme en local.
COPY .streamlit/ ./.streamlit/

# L'arborescence doit rester celle du dépôt : `dashboard/donnees.py` résout ses chemins par
# `Path(__file__).resolve().parents[1]`, et la page Sources et méthode lit
# `07_indicators.md` à la racine. `dashboard/` et `data/` doivent rester frères sous /app.
COPY dashboard/ ./dashboard/

# Les seules données que le tableau de bord lit : les tables publiées par les analyses
# (sans leurs figures, exclues par .dockerignore) et les contours administratifs.
COPY data/analysis/ ./data/analysis/
COPY data/processed/geo/ ./data/processed/geo/

# Le tableau des 27 indicateurs est lu tel quel dans ce document (page Sources et méthode).
COPY 07_indicators.md ./

# Exécution sans privilèges. Streamlit veut écrire dans $HOME (cache, configuration) : on
# lui donne /app, déjà possédé par l'utilisateur.
RUN useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /app
USER appuser
ENV HOME=/app

EXPOSE 8501

# Endpoint de santé natif de Streamlit. Heroku ne s'en sert pas, mais le test de fumée de la
# CI et un `docker run` local s'appuient dessus.
HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request,os,sys; \
sys.exit(0 if urllib.request.urlopen(f'http://127.0.0.1:{os.environ.get(\"PORT\",8501)}/_stcore/health').status==200 else 1)"

# Heroku assigne $PORT au lancement du conteneur : il doit être lu à l'exécution, pas figé
# au build. D'où le passage par un shell ; `exec` rend ensuite son PID 1 à Streamlit, pour
# qu'il reçoive le SIGTERM qu'Heroku envoie à l'arrêt d'un dyno.
CMD ["sh", "-c", "exec streamlit run dashboard/app.py --server.port=${PORT:-8501} --server.address=0.0.0.0"]
