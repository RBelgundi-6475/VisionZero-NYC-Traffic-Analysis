from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
# Import our Python scripts for STAGE A: Fetch data from API and upload to GCS. 
# STAGE B: Load data from GCS bucket to BigQuery table
from nyc_fetch_to_gcs import main as fetch_data
from load_to_bigquery import main as load_bq

with DAG(
    dag_id='nyc_traffic_pipeline',
    start_date=days_ago(1),
    schedule_interval='@daily',
    catchup=False,
    tags=["nyc", "traffic", "pipeline"]
) as dag:
    fetch_task = PythonOperator(
        task_id='fetch_nyc_data',
        python_callable=fetch_data
    )

    load_task = PythonOperator(
        task_id='load_to_bigquery',
        python_callable=load_bq
    )

    dbt_run = BashOperator(
        task_id='run_dbt_models',
        bash_command='cd /opt/airflow/dbt/nyc_crash_analysis_project && dbt run --profiles-dir .'
    )

    dbt_test = BashOperator(
        task_id='test_dbt_models',
        bash_command='cd /opt/airflow/dbt/nyc_crash_analysis_project && dbt test --profiles-dir .'
    )

    # Define the lineage for tasks
    fetch_task >> load_task >> dbt_run >> dbt_test