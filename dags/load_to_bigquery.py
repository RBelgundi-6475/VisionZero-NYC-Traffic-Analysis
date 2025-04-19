from google.cloud import bigquery
from datetime import datetime

def main():
    # ===== CONFIG =====
    PROJECT_ID = 'nyc-traffic-analysis-456021'
    DATASET_ID = 'nyc_traffic_data'    # The dataset ID when we created dataset in BigQuery
    TABLE_ID = 'raw_crashes'           # The table to create in BigQuery
    BUCKET_NAME = 'nyc-traffic-data-bucket'
    GCS_FOLDER = 'nyc_data'

    # ===== Build today's file name =====
    today = datetime.today().strftime('%Y%m%d')
    file_name = f"accidents_{today}.csv"
    gcs_uri = f"gs://{BUCKET_NAME}/{GCS_FOLDER}/{file_name}"

    # ===== Full table reference =====
    full_table_id = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    client = bigquery.Client()    # Initialize BigQuery client

    # ===== Job Config =====
    job_config = bigquery.LoadJobConfig(
        source_format = bigquery.SourceFormat.CSV,
        skip_leading_rows = 1,
        autodetect = True,
        write_disposition = "WRITE_APPEND"
    )

    # Run the load Job
    load_job = client.load_table_from_uri(
        gcs_uri,
        destination = full_table_id,
        job_config= job_config
    )
    load_job.result()

    # Confirm the load job's successful execution
    table = client.get_table(full_table_id)
    print(f"✅ Loaded {table.num_rows} rows into {full_table_id}.")

# This allows Airflow to call main()
if __name__ == "__main__":
    main()