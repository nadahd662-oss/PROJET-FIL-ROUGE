from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import os


# Import our scripts
from bronze_ingest import ingest_bronze
from silver_clean import clean_silver
from gold_build import build_gold

# DAG definition
with DAG(
    dag_id='school_performance_pipeline',
    description='Pipeline ETL for school performance analysis',
    start_date=datetime(2026, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Task 1 : Extract bronze
    task_bronze = PythonOperator(
        task_id='bronze_ingestion',
        python_callable=ingest_bronze
    )

    # Task 2 : Clean silver
    task_silver = PythonOperator(
        task_id='silver_cleaning',
        python_callable=clean_silver
    )

    # Task 3 : Build gold
    task_gold = PythonOperator(
        task_id='gold_build',
        python_callable=build_gold
    )

    # Pipeline order
    task_bronze >> task_silver >> task_gold