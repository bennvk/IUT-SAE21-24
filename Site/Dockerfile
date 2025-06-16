# Utilise une image Python légère comme base
FROM python:3.10-slim

# Déclare les arguments de build pour le proxy (utiles en environnement universitaire)
ARG HTTP_PROXY
ARG HTTPS_PROXY

# Définit les variables d'environnement pour le proxy dans le conteneur
ENV HTTP_PROXY=$HTTP_PROXY
ENV HTTPS_PROXY=$HTTPS_PROXY

# Définit le dossier de travail dans le conteneur
WORKDIR /app

# Copie le fichier des dépendances Python dans le conteneur
COPY requirements.txt requirements.txt

# Installe les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie tout le code de l'application dans le conteneur
COPY . .

# Commande de lancement de l'application Flask
CMD ["flask", "run", "--host=0.0.0.0"]