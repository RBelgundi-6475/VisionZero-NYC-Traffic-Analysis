# Import packages
import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from google.cloud import storage

# ===== Config variables =====
BUCKET_NAME = 'nyc-traffic-data-bucket'
FOLDER = 'nyc_data'
# base_url = 'https://data.cityofnewyork.us/resource/h9gi-nx95.csv?$limit=10000'
BASE_URL = 'https://data.cityofnewyork.us/resource/h9gi-nx95.json'
MAX_RECORDS = 50000
BATCH_SIZE = 1000

# Generate filename for today
today = datetime.today().strftime("%Y%m%d")
FILE_NAME = f"accidents_{today}.csv"
LOCAL_PATH = f"nyc_data/{FILE_NAME}"
GCS_PATH = f"{FOLDER}/{FILE_NAME}"

# Fetch Data from NYC API
def fetch_nyc_data(limit = BATCH_SIZE, max_records = MAX_RECORDS):
    print(f"Fetching {max_records} records from NYC Open Data API")
    offset = 0
    all_data = []

    while offset < max_records:
        params = {
            "$limit":limit,
            "$offset":offset
        }
        response = requests.get(BASE_URL,params = params)
        if response.status_code != 200:
            raise Exception(f"API Error {response.status_code}: {response.text}")

        batch = response.json()
        # print(batch[0])
        if not batch:
            print("No more data coming in from the API.")
            break
        
        all_data.extend(batch)
        offset += limit
        print(f"Fetched {offset} records so far....")
    
    df = pd.DataFrame(all_data)
    print(f"Total records fetched: {len(df)}")
    return df

# Upload the local CSV to GCS
def upload_csv_to_gcs(local_file_path,bucket_name,gcs_path):
    print(f"Uploading {local_file_path} to GCS: {bucket_name}//{gcs_path}")

    client = storage.Client() # Create a client for Google Cloud Storage
    bucket = client.bucket(bucket_name)  # Create an instance of the bucket in GCS
    blob = bucket.blob(gcs_path)

    blob.upload_from_filename(local_file_path) # Actual upload function

    print('Upload complete!')

def main():
    print("Starting NYC ingestion script...")
    df = fetch_nyc_data(limit= 1000, max_records=10000)
    os.makedirs(os.path.dirname(LOCAL_PATH), exist_ok=True)
    df.to_csv(LOCAL_PATH, index=False)
    print(f"CSV saved to: {LOCAL_PATH}")

    # Upload data to GCS bucket
    upload_csv_to_gcs(local_file_path = LOCAL_PATH,
                        bucket_name = BUCKET_NAME,
                        gcs_path = GCS_PATH)

if __name__ == "__main__":
    main()
    # try:
    #     print("Starting NYC ingestion script...")
    #     df = fetch_nyc_data(limit= 1000, max_records=10000)
    #     os.makedirs(os.path.dirname(LOCAL_PATH), exist_ok=True)
    #     df.to_csv(LOCAL_PATH, index=False)
    #     print(f"CSV saved to: {LOCAL_PATH}")

    #     # Upload data to GCS bucket
    #     upload_csv_to_gcs(local_file_path = LOCAL_PATH,
    #                       bucket_name = BUCKET_NAME,
    #                       gcs_path = GCS_PATH)
    # except Exception as e:
    #     print(f"Error occurred: {e}")