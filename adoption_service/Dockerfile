# Base Python
FROM python:3.11-slim

# Définir le dossier de travail dans le container
WORKDIR /app

# Copier les dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code du microservice dans le container
COPY . .

# Définir le port du microservice (ex: 8001 pour accounts)
EXPOSE 8002

# Commande pour lancer Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8002"]
