=== INSTRUCTIONS POUR LANCER LE PROJET ===

PRÉREQUIS : Docker installé et démarré

ÉTAPE 1 — Charger les images (une seule fois) :
    docker load -i images.tar

ÉTAPE 2 — Lancer tout automatiquement :

exp : si     /home/user/projet-bigdata/
cd ~/projet-bigdata


bash start.sh


ÉTAPE 3 — Lancer l'interface web (nouveau terminal) :
    docker run -it --rm -p 5000:5000 \
      -v ./web:/app python:3.12 \
      bash -c "pip install flask && python /app/app.py"

ÉTAPE 4 — Ouvrir dans le navigateur :
    Interface Web    → http://localhost:5000
    HDFS             → http://localhost:9870
    YARN             → http://localhost:8088
    Spark            → http://localhost:8080


docker ps
docker compose up -d
