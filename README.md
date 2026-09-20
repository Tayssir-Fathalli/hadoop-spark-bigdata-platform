# Big Data Analytics with Hadoop, Spark & Flask

## Overview

This project implements a distributed Big Data analytics environment using **Apache Hadoop, Apache Spark, Docker, and Flask**.

The objective is to process and analyze datasets in a distributed environment using **HDFS, Hadoop MapReduce, and Apache Spark**, then present selected analytical results through an interactive web dashboard.

The project includes two main data-processing workflows:

* **Hadoop MapReduce** jobs for distributed processing
* **Apache Spark** DataFrame-based analysis for computing analytical KPIs

A Flask web application with Chart.js is also provided to visualize the resulting heart disease analysis through an interactive dashboard.

---

## Architecture

The complete environment is containerized using Docker Compose.

```text
                         Docker Compose
                               |
          +--------------------+--------------------+
          |                    |                    |
       Hadoop                 YARN                Spark
          |                    |                    |
     +----+----+          +----+----+        +------+------+
     |         |          |         |        |             |
 NameNode   DataNode  ResourceManager NodeManager  Spark Master
                                                       |
                                                +------+------+
                                                |             |
                                           Worker 1       Worker 2
```

The data is stored in **HDFS** and processed using Hadoop MapReduce and Apache Spark.

The Spark analysis reads the heart disease dataset from HDFS and generates eight analytical KPIs. The results are stored in Parquet format in HDFS.

A Flask-based dashboard is used to visualize the heart disease KPIs.

---

## Technologies

| Technology         | Purpose                                     |
| ------------------ | ------------------------------------------- |
| Python             | Data processing and application development |
| Apache Hadoop 3    | Distributed storage and MapReduce           |
| HDFS               | Distributed file storage                    |
| YARN               | Cluster resource management                 |
| Apache Spark 3.5.0 | Distributed data processing                 |
| PySpark            | Spark analysis using Python                 |
| Docker             | Containerization                            |
| Docker Compose     | Cluster orchestration                       |
| Flask              | Web application                             |
| Chart.js           | Data visualization                          |
| Parquet            | Storage of processed Spark results          |

---

## Project Structure

```text
hadoop-spark-big-data/
│
├── README.md
├── docker-compose.yml
├── start.sh
├── .gitignore
│
├── config/
│   └── Hadoop configuration
│
├── data/
│   └── Dataset documentation
│
├── scripts/
│   ├── mapper.py
│   ├── mapper_b.py
│   ├── mapper_c.py
│   ├── mapper_d.py
│   ├── reducer.py
│   ├── reducer_b.py
│   ├── reducer_c.py
│   ├── reducer_d.py
│   └── spark_analysis.py
│
└── web/
    ├── app.py
    └── templates/
        └── index.html
```

---

## Datasets

### Heart Disease Dataset

The heart disease dataset contains **1,025 patient records and 14 variables**.

It is used for the Spark analytical workflow and dashboard.

The analysis includes variables such as:

* Age
* Sex
* Chest pain type
* Resting blood pressure
* Cholesterol
* Maximum heart rate
* Heart disease target
* and other clinical attributes

The dataset is intentionally not included directly in the repository if its redistribution or repository size is a concern.

The expected HDFS location is:

```text
/user/hadoop/heart/heart.csv
```

### Purchases Dataset

A large purchases dataset is used for the Hadoop MapReduce workflow.

The dataset contains approximately **4.1 million records**.

Due to its size, the original dataset is not included in the GitHub repository.

The expected HDFS location is:

```text
/user/hadoop/input/purchases.txt
```

---

# Hadoop MapReduce

Several Mapper and Reducer implementations are included in the `scripts/` directory.

```text
mapper.py
reducer.py

mapper_b.py
reducer_b.py

mapper_c.py
reducer_c.py

mapper_d.py
reducer_d.py
```

These scripts demonstrate distributed processing using the Hadoop MapReduce programming model.

The workflow consists of:

```text
Input Dataset
      |
      v
    Mapper
      |
      v
Intermediate Key/Value Pairs
      |
      v
    Shuffle
      |
      v
    Reducer
      |
      v
Processed Results
```

The scripts are designed to be executed within the Hadoop environment using data stored in HDFS.

---

# Apache Spark Analysis

The Spark workflow is implemented in:

```text
scripts/spark_analysis.py
```

The application creates a Spark session connected to the Spark cluster:

```python
SparkSession.builder \
    .appName("HeartDiseaseAnalysis") \
    .master("spark://spark-master:7077") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
    .getOrCreate()
```

The heart disease dataset is read directly from HDFS.

```text
HDFS
 |
 | heart.csv
 v
Spark
 |
 v
PySpark DataFrame
 |
 v
KPI calculations
 |
 v
Parquet results
```

The Spark workflow generates eight KPIs.

---

# Analytical KPIs

## KPI 1 — Heart Disease Distribution

Calculates the number of patients classified as:

* Patients with heart disease
* Patients without heart disease

---

## KPI 2 — Average Age by Health Status

Calculates the average patient age according to the target classification.

---

## KPI 3 — Distribution by Sex

Analyzes the distribution of patients according to:

* Sex
* Heart disease status

---

## KPI 4 — Average Cholesterol by Age Group

Patients are divided into age groups:

```text
< 40
40–49
50–59
60+
```

The average cholesterol level is calculated for each group.

---

## KPI 5 — Heart Rate and Blood Pressure

Calculates average:

* Maximum heart rate
* Resting blood pressure

for the different heart disease status groups.

---

## KPI 6 — Chest Pain Type vs Heart Disease

Analyzes the relationship between chest pain categories and heart disease status.

---

## KPI 7 — Patient Risk Profile

Patients are grouped by:

* Age group
* Sex

The analysis calculates:

* Total patients
* Number of patients with heart disease
* Average cholesterol
* Average maximum heart rate
* Disease rate

The resulting groups are ordered according to the calculated disease rate.

---

## KPI 8 — Heart Rate and Disease Rate

Maximum heart rate is divided into several ranges:

```text
< 120
120–139
140–159
160–179
180+
```

For each range, the analysis calculates:

* Number of patients
* Number of patients with heart disease
* Average heart rate
* Disease rate

---

# Storing Results in HDFS

The Spark workflow stores the KPI outputs as **Parquet files**.

```text
/user/hadoop/results/
├── kpi1/
├── kpi2/
├── kpi3/
├── kpi4/
├── kpi5/
├── kpi6/
├── kpi7/
└── kpi8/
```

Parquet provides a columnar storage format suitable for analytical workloads.

---

# Flask Dashboard

The project includes a Flask web application located in:

```text
web/app.py
```

The dashboard uses **Chart.js** to display the heart disease analysis.

The interface contains eight visualizations organized into two sections:

### Descriptive Analysis

* KPI 1 — Disease distribution
* KPI 2 — Average age
* KPI 3 — Distribution by sex
* KPI 4 — Cholesterol by age group
* KPI 5 — Heart rate and blood pressure
* KPI 6 — Chest pain type

### Advanced Analysis

* KPI 7 — Risk profile by age and sex
* KPI 8 — Disease rate by heart rate range

The dashboard is accessible on:

```text
http://localhost:5000
```

> **Implementation note:** the current Flask dashboard receives predefined KPI values from `app.py` for visualization. The Spark pipeline independently computes and stores the analytical results in HDFS as Parquet files.

---

# Running the Project

## Requirements

The project requires:

* Docker Desktop
* Docker Compose
* Git
* A Linux/WSL environment is recommended for running `start.sh`

Make sure Docker is running before starting the cluster.

---

## 1. Start the Hadoop and Spark cluster

From the project root:

```bash
docker compose up -d
```

The Docker Compose configuration launches:

* NameNode
* DataNode
* ResourceManager
* NodeManager
* Spark Master
* Spark Worker 1
* Spark Worker 2

---

## 2. Load the datasets into HDFS

The provided startup script automates cluster startup and data loading:

```bash
./start.sh
```

The script:

1. Starts the Docker Compose cluster
2. Waits for the services to initialize
3. Copies datasets into the NameNode container
4. Copies processing scripts into the appropriate containers
5. Creates the required HDFS directories
6. Uploads the datasets to HDFS

---

## 3. Run the Spark analysis

The Spark script is copied to the Spark master container by the startup script.

It can then be submitted to the Spark cluster using:

```bash
docker exec spark-master spark-submit \
    --master spark://spark-master:7077 \
    /tmp/spark_analysis.py
```

The generated KPI results are written to HDFS in Parquet format.

---

# Flask Web Application

The Flask dashboard is currently launched separately from the Hadoop/Spark Compose cluster.

Example:

```bash
docker run -it --rm \
    -p 5000:5000 \
    -v "$(pwd)/web:/app" \
    python:3.12 \
    bash -c "pip install flask && python /app/app.py"
```

Then open:

```text
http://localhost:5000
```

---

# Cluster Monitoring

Once the cluster is running, the following interfaces are available:

| Service              | URL                     | Purpose                  |
| -------------------- | ----------------------- | ------------------------ |
| HDFS NameNode        | `http://localhost:9870` | HDFS monitoring          |
| YARN ResourceManager | `http://localhost:8088` | YARN cluster monitoring  |
| Spark Master         | `http://localhost:8080` | Spark cluster monitoring |
| Flask Dashboard      | `http://localhost:5000` | KPI visualization        |

---

# Results

The project demonstrates a complete Big Data processing workflow:

```text
Raw Data
   |
   v
HDFS
   |
   +--------------------+
   |                    |
   v                    v
MapReduce             Spark
   |                    |
   v                    v
Processed Data       KPI Analysis
                        |
                        v
                     Parquet
                        |
                        v
                  Visualization
                        |
                        v
                  Flask Dashboard
```

---

# Learning Objectives

This project provided practical experience with:

* Distributed storage using HDFS
* Hadoop cluster architecture
* Hadoop MapReduce
* Mapper and Reducer development
* YARN resource management
* Apache Spark cluster configuration
* PySpark DataFrame operations
* Aggregations and analytical KPIs
* Parquet data storage
* Docker containerization
* Docker Compose orchestration
* Flask web application development
* Chart.js data visualization

---

# Author

**Tayssir Fathalli**

Big Data & Data Analysis Student

Technologies of interest:

`Python` · `SQL` · `Big Data` · `Apache Spark` · `Hadoop` · `Machine Learning` · `Data Analysis`
