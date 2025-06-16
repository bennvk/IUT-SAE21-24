## Docker:
sudo docker-compose up -d --build

## Stop Docker (tout les services): 
sudo systemctl stop docker

## Relancer Docker (pensez à clear):
sudo docker-compose up -d --build

## Flush Docker (Pour lancer Docker de façon clean):
sudo docker-compose down --rmi all -v
sudo docker system prune -a             (Clear all (MAIS VRAIMENT))

## Redémarrer le fichier Docker:
sudo systemctl restart docker

## Vérifié les dockers en cours:
sudo docker ps

## Supprimer la DB au terminal
rm -f instance/data.db


## Préliminaires 
sudo mkdir -p /etc/systemd/system/docker.service.d
sudo nano /etc/systemd/system/docker.service.d/http-proxy.conf

[Service]
Environment="HTTP_PROXY=http://cache-etu.univ-artois.fr:3128"
Environment="HTTPS_PROXY=http://cache-etu.univ-artois.fr:3128"

sudo systemctl daemon-reload
sudo systemctl restart docker

## Test de pull la db au cas où

sudo docker pull postgres:15

