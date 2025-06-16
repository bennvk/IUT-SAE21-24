FROM python:3.10

WORKDIR /app

# Installer les dépendances
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Exposer le port Flask
EXPOSE 5000

# Commande pour démarrer l'application
CMD ["python", "app.py"]
