from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from etl.extract import extract_data
from etl.validate import validate_data
from etl.transform import transform_data
from etl.load import load_data


default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}


def run_etl():
    raw_data = extract_data()
    validated_data = validate_data(raw_data)
    transformed_data = transform_data(validated_data)
    load_data(transformed_data)


with DAG(
    dag_id="market_etl_pipeline",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval="*/5 * * * *",
    catchup=False,
) as dag:

    etl_task = PythonOperator(
        task_id="run_etl",
        python_callable=run_etl,
    )