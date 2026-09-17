from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("HeartDiseaseAnalysis") \
    .master("spark://spark-master:7077") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

df = spark.read.csv("hdfs://namenode:9000/user/hadoop/heart/heart.csv",
                     header=True, inferSchema=True)

print("=== STRUCTURE DU DATASET ===")
df.printSchema()
print("=== NOMBRE DE LIGNES ===")
print(df.count())
print("=== APERCU DES DONNEES ===")
df.show(5)

print("=== KPI 1 : REPARTITION MALADIES CARDIAQUES ===")
kpi1 = df.groupBy("target").count().withColumnRenamed("count", "nombre_patients")
kpi1.show()

print("=== KPI 2 : MOYENNE D'AGE PAR STATUT ===")
kpi2 = df.groupBy("target").agg(F.round(F.avg("age"), 2).alias("age_moyen"))
kpi2.show()

print("=== KPI 3 : REPARTITION PAR SEXE ===")
kpi3 = df.groupBy("sex", "target").count().orderBy("sex", "target")
kpi3.show()

print("=== KPI 4 : CHOLESTEROL MOYEN PAR TRANCHE D'AGE ===")
kpi4 = df.withColumn("tranche_age",
          F.when(F.col("age") < 40, "moins de 40") \
           .when(F.col("age") < 50, "40-49") \
           .when(F.col("age") < 60, "50-59") \
           .otherwise("60 et plus")) \
         .groupBy("tranche_age") \
         .agg(F.round(F.avg("chol"), 2).alias("cholesterol_moyen")) \
         .orderBy("tranche_age")
kpi4.show()

print("=== KPI 5 : FREQUENCE CARDIAQUE MOYENNE PAR STATUT ===")
kpi5 = df.groupBy("target").agg(
    F.round(F.avg("thalach"), 2).alias("freq_cardiaque_moyenne"),
    F.round(F.avg("trestbps"), 2).alias("tension_moyenne"))
kpi5.show()

print("=== KPI 6 : TYPE DE DOULEUR THORACIQUE VS MALADIE ===")
kpi6 = df.groupBy("cp", "target").count().orderBy("cp", "target")
kpi6.show()

kpi1.write.mode("overwrite").parquet("hdfs://namenode:9000/user/hadoop/results/kpi1")
kpi2.write.mode("overwrite").parquet("hdfs://namenode:9000/user/hadoop/results/kpi2")
kpi3.write.mode("overwrite").parquet("hdfs://namenode:9000/user/hadoop/results/kpi3")
kpi4.write.mode("overwrite").parquet("hdfs://namenode:9000/user/hadoop/results/kpi4")
kpi5.write.mode("overwrite").parquet("hdfs://namenode:9000/user/hadoop/results/kpi5")
kpi6.write.mode("overwrite").parquet("hdfs://namenode:9000/user/hadoop/results/kpi6")
kpi7.write.mode("overwrite").parquet("hdfs://namenode:9000/user/hadoop/results/kpi7")
kpi8.write.mode("overwrite").parquet("hdfs://namenode:9000/user/hadoop/results/kpi8") 
 


print("=== TOUS LES KPIs SAUVEGARDES DANS HDFS ===")
# KPI 7 - Profil patient le plus à risque
# On combine age + cholesterol + tension + frequence cardiaque
# pour créer un score de risque
print("=== KPI 7 : PROFIL PATIENT LE PLUS A RISQUE ===")
kpi7 = df.withColumn("tranche_age",
          F.when(F.col("age") < 40, "moins de 40") \
           .when(F.col("age") < 50, "40-49") \
           .when(F.col("age") < 60, "50-59") \
           .otherwise("60 et plus")) \
         .withColumn("sexe",
          F.when(F.col("sex") == 0, "Femme") \
           .otherwise("Homme")) \
         .groupBy("tranche_age", "sexe") \
         .agg(
             F.count("*").alias("total_patients"),
             F.sum(F.when(F.col("target") == 1, 1).otherwise(0)).alias("nb_malades"),
             F.round(F.avg("chol"), 2).alias("chol_moyen"),
             F.round(F.avg("thalach"), 2).alias("freq_moy")
         ) \
         .withColumn("taux_risque",
             F.round((F.col("nb_malades") / F.col("total_patients")) * 100, 2)) \
         .orderBy(F.col("taux_risque").desc())
kpi7.show()

# KPI 8 - Impact de la frequence cardiaque sur la maladie
# On divise la frequence cardiaque en tranches
# et on calcule le taux de maladie pour chaque tranche
print("=== KPI 8 : IMPACT FREQUENCE CARDIAQUE SUR MALADIE ===")
kpi8 = df.withColumn("tranche_freq",
          F.when(F.col("thalach") < 120, "Très basse (<120)") \
           .when(F.col("thalach") < 140, "Basse (120-139)") \
           .when(F.col("thalach") < 160, "Normale (140-159)") \
           .when(F.col("thalach") < 180, "Élevée (160-179)") \
           .otherwise("Très élevée (180+)")) \
         .groupBy("tranche_freq") \
         .agg(
             F.count("*").alias("total_patients"),
             F.sum(F.when(F.col("target") == 1, 1).otherwise(0)).alias("nb_malades"),
             F.round(F.avg("thalach"), 2).alias("freq_moyenne")
         ) \
         .withColumn("taux_maladie",
             F.round((F.col("nb_malades") / F.col("total_patients")) * 100, 2)) \
         .orderBy("freq_moyenne")
kpi8.show()

# Sauvegarder en Parquet dans HDFS
kpi7.write.mode("overwrite").parquet("hdfs://namenode:9000/user/hadoop/results/kpi7")
kpi8.write.mode("overwrite").parquet("hdfs://namenode:9000/user/hadoop/results/kpi8")

print("=== KPI 7 et KPI 8 SAUVEGARDES ===")
spark.stop()
