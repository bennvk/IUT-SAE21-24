# Commandes de base.

## Démarré le Docker (-d --build pour lancement avec le build)
sudo docker-compose up -d --build
## Arrêter le Docker
sudo docker-compose down
## Stop Docker (tout les services): 
sudo systemctl stop docker
## Flush Docker (Pour lancer Docker de façon clean(après un stop Docker)):
sudo docker-compose down --rmi all -v
sudo docker system prune -a             (Clear all (MAIS VRAIMENT))

## Redémarrer le fichier Docker:
sudo systemctl restart docker
## Vérifié les dockers en cours:s
sudo docker ps

# Lancer script cam (être dans le bon dossier)
bash cam1-start.sh

# Préliminaires 

## Avoir le proxy et pouvoir build
sudo mkdir -p /etc/systemd/system/docker.service.d
sudo nano /etc/systemd/system/docker.service.d/http-proxy.conf

## Contenu du fichier
[Service]
Environment="HTTP_PROXY=http://cache-etu.univ-artois.fr:3128"
Environment="HTTPS_PROXY=http://cache-etu.univ-artois.fr:3128"

# Relancer le service après
sudo systemctl daemon-reload
sudo systemctl restart docker

# Autre

# Ouvre un terminal SQL dans le conteneur db :
sudo docker exec -it site_interne_db psql -U postgres -d sae24

## Si problème avec cam 
chmod +x Site\ interne/start.sh
chmod +x Site\ interne/cam1/start.sh
chmod +x Site\ interne/cam2/start.sh
