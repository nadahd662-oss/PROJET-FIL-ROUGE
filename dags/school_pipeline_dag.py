from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys

sys.path.insert(0, '/opt/airflow/dags')

from bronze_ingest import ingest_bronze
from silver_clean import clean_silver
from gold_build import build_gold
from snowflake_load import load_to_snowflake

with DAG(
    dag_id='school_performance_pipeline',
    description='Pipeline ETL for school performance analysis',
    start_date=datetime(2026, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    task_bronze = PythonOperator(
        task_id='bronze_ingestion',
        python_callable=ingest_bronze
    )

    task_silver = PythonOperator(
        task_id='silver_cleaning',
        python_callable=clean_silver
    )

    task_gold = PythonOperator(
        task_id='gold_build',
        python_callable=build_gold
    )

    task_snowflake = PythonOperator(
        task_id='snowflake_load',
        python_callable=load_to_snowflake
    )

    # Pipeline order
    task_bronze >> task_silver >> task_gold >> task_snowflake