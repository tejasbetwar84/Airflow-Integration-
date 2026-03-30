<<<<<<< HEAD
▶️ How to Run
1. Start services
docker compose up -d
2. Access Airflow UI
http://localhost:8080
3. Create Airflow User

Run this on your host machine:

docker exec -it <airflow-webserver-container> airflow users create \
  --username airflow \
  --password airflow \
  --firstname Airflow \
  --lastname Admin \
  --role Admin \
  --email airflow@example.com
4. Trigger DAGs
(Optional) Reset table:
reset_market_table_dag
Run pipeline:
market_etl_pipeline
🔍 Verify Data

Connect to Postgres:

docker exec -it <postgres-container> psql -U airflow -d airflow

Run:

SELECT COUNT(*) FROM market_data;
SELECT * FROM market_data ORDER BY timestamp DESC LIMIT 5;


## Conceptual / System Design

### 1. Scaling (Handling 1 Billion Events/Day)

If data volume increases significantly, the architecture would evolve from a batch-based pipeline to a distributed, scalable system:

* **Ingestion Layer**: Replace direct API calls with **Kafka** for high-throughput, real-time ingestion.
* **Processing Layer**: Use **Apache Spark (Structured Streaming)** or **Flink** for distributed processing instead of single-node Python transformations.
* **Storage Layer**:

  * Use **Data Lake (S3 / GCS / ADLS)** for raw + processed data
  * Use **Columnar warehouses (BigQuery / Snowflake / Redshift)** for analytics
* **Orchestration**:

  * Airflow remains for scheduling, but heavy compute moves to Spark jobs
* **Partitioning Strategy**:

  * Partition data by **date/hour** to improve query performance and scalability


### 2. Monitoring (Health Checks)

To ensure the pipeline runs reliably in production:

* **Airflow Monitoring**:

  * Use built-in task retries, SLA alerts, and failure notifications
* **Logging**:

  * Centralized logging using tools like **ELK Stack / Cloud Logging**
* **Data Quality Checks**:

  * Validate row counts, null values, schema consistency
  * Tools: **Great Expectations**
* **Custom Health Checks**:

  * Check API availability before extraction
  * Validate record counts (e.g., sudden drop = alert)
* **Alerting**:

  * Integrate with **Slack / Email** for failures
* **Metrics Tracking**:

  * Track pipeline metrics (latency, success rate, throughput)


### 3. Recovery & Idempotency

To handle failures (e.g., pipeline crashes midway through a 10GB batch):

* **Idempotent Loads (Already Implemented)**:

  * Use **UPSERT (`ON CONFLICT`)** in PostgreSQL
  * Prevents duplicate records

* **Checkpointing**:

  * Store last processed timestamp or offset
  * Resume from last successful state

* **Atomic Transactions**:

  * Use database transactions (`COMMIT/ROLLBACK`)
  * Ensures partial loads are not persisted

* **Batch Processing Strategy**:

  * Break large data into smaller chunks (e.g., 10k records per batch)
  * Retry only failed batches instead of full reload

* **Staging Tables (Advanced)**:

  * Load data into staging table first
  * Validate → then merge into final table

=======
# Airflow-Integration-
>>>>>>> 816b69b82344fda0b4743aaef7dbaec7fa075fc6
