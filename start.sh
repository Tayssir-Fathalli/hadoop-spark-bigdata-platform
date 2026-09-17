#!/bin/bash
echo "=== Lancement du cluster ==="
docker compose up -d

echo "Attente 20 secondes..."
sleep 20

echo "=== Chargement des données dans HDFS ==="
docker cp data/purchases.txt namenode:/tmp/purchases.txt
docker cp data/heart.csv namenode:/tmp/heart.csv
docker cp scripts/mapper.py namenode:/tmp/mapper.py
docker cp scripts/reducer.py namenode:/tmp/reducer.py
docker cp scripts/mapper_b.py namenode:/tmp/mapper_b.py
docker cp scripts/reducer_b.py namenode:/tmp/reducer_b.py
docker cp scripts/mapper_c.py namenode:/tmp/mapper_c.py
docker cp scripts/reducer_c.py namenode:/tmp/reducer_c.py
docker cp scripts/mapper_d.py namenode:/tmp/mapper_d.py
docker cp scripts/reducer_d.py namenode:/tmp/reducer_d.py
docker cp scripts/spark_analysis.py spark-master:/tmp/spark_analysis.py

docker exec namenode hdfs dfs -mkdir -p /user/hadoop/input
docker exec namenode hdfs dfs -mkdir -p /user/hadoop/heart
docker exec namenode hdfs dfs -mkdir -p /user/hadoop/results
docker exec namenode hdfs dfs -chmod 777 /user/hadoop
docker exec namenode hdfs dfs -chmod 777 /user/hadoop/results

docker exec namenode hdfs dfs -put /tmp/purchases.txt /user/hadoop/input/
docker exec namenode hdfs dfs -put /tmp/heart.csv /user/hadoop/heart/

echo "=== TOUT EST PRET ==="
echo "HDFS    → http://localhost:9870"
echo "YARN    → http://localhost:8088"
echo "Spark   → http://localhost:8080"
echo "Web App → http://localhost:5000"
