from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import psycopg2
import logging


def reset_market_table():
    conn = psycopg2.connect(
        host="postgres",
        database="airflow",
        user="airflow",
        password="airflow"
    )
    cursor = conn.cursor()

    try:
        logging.info("Dropping table if exists...")

        cursor.execute("""
        DROP TABLE IF EXISTS market_data;
        """)

        logging.info("Creating fresh table...")

        cursor.execute("""
        CREATE TABLE market_data (
            id SERIAL PRIMARY KEY,
            instrument_id TEXT NOT NULL,
            price DOUBLE PRECISION NOT NULL,
            volume DOUBLE PRECISION NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            vwap DOUBLE PRECISION,
            is_outlier BOOLEAN DEFAULT FALSE,
            UNIQUE (instrument_id, timestamp)
        );
        """)

        conn.commit()
        logging.info("Table recreated successfully ✅")

    except Exception as e:
        logging.error(f"Error resetting table: {e}")
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()


with DAG(
    dag_id="reset_market_table_dag",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,   
    catchup=False
) as dag:

    reset_table_task = PythonOperator(
        task_id="drop_and_recreate_table",
        python_callable=reset_market_table
    )