FROM python:3.10

WORKDIR /app

# Ajoute les variables proxy pour le build
ENV HTTP_PROXY=http://cache-etu.univ-artois.fr:3128
ENV HTTPS_PROXY=http://cache-etu.univ-artois.fr:3128

# Installer les dépendances
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Variables d'environnement pour PostgreSQL (à adapter si besoin)
ENV POSTGRES_HOST=db
ENV POSTGRES_DB=ramba
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

# Exposer le port Flask
EXPOSE 5050

# Commande pour démarrer l'application
CMD ["python", "app.py"]
