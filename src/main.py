# %%
import io
import os
import time
from datetime import date, datetime

import dlt
import pandas as pd
from dotenv import dotenv_values
from pydantic import BaseModel

# Loading local packages
from modules.apis.google_drive import googledrive

# Loading environment variables
env_variables = dotenv_values(".env")
googleDriveUrl = os.getenv("folderUrl")
googleDriveFolderId = os.getenv("folderGoogleDrive")
googleDriveFolderIdProccessed = os.getenv("folderGoogleDriveProcessed")
serviceAccountPath = os.getenv("serviceAccountJsonKeyPath")
gDFolderUrl = os.getenv("gDFolderUrl")

# Database configuration
database = os.getenv("database")
username = os.getenv("username")
password = os.getenv("password")  # replace with your password
host = os.getenv("host")  # or the IP address location of your database
port = os.getenv("port")
connect_timeout = os.getenv("connect_timeout")

print("connect_timeout", connect_timeout)

# Initialize Google Drive API object
googledriveObject = googledrive.GoogleDriveAPI(
    service_account_path=serviceAccountPath, folder_id=googleDriveFolderId
)


resultCsvList = googledriveObject.list_files()
# Function to authenticate with Google Drive

# Pipeline configuration
# Local testing using duckdb
# pipeline = dlt.pipeline(destination="duckdb", dataset_name="chess_data")
engine_url = f"postgresql://{username}:{password}@{host}:{port}/{database}"
pipeline = dlt.pipeline(
    pipeline_name='chess',
    destination='postgres',
    dataset_name='chess_data',
    credentials=engine_url,
    progress="log",
)


class User(BaseModel):
    id: int
    name: str
    created_at: datetime = datetime.now()


@dlt.resource(name="user", columns=User)
def generate_rows(nr) -> iter:
    for i in range(1, nr + 1, 1):
        yield {'id': i, 'name': 'user' + ' ' + str(i), 'created_at': datetime.now()}


# Execute pipeline for users table
info = pipeline.run(generate_rows(35), table_name="user", write_disposition="replace")


class generic_fact_table(BaseModel):
    timestamp: date
    file_name: str
    batch_row_number: int
    price: float
    user_id: int


# pylint: disable=W0621
def df_pipeline(df: pd.DataFrame, file_name: str) -> iter:
    """
    Generate dictionaries from DataFrame rows.

    Parameters:
        df (pd.DataFrame): Input DataFrame to iterate over.

    Yields:
        dict: A dictionary representing each row of the DataFrame.
    """

    # Initialize in-memory statistics
    count = 0
    price_sum = 0
    price_min = float("inf")
    price_max = float("-inf")

    # Iterate over rows in the DataFrame
    for index_df, row in df.iterrows():
        time.sleep(0.5)
        row_dict = row.to_dict()
        row_dict["file_name"] = file_name
        row_dict["batch_row_number"] = index_df + 1
        print(f"Insert row{index_df}", row_dict)

        # Store in memmory the results every row:
        count += 1
        price = row["price"]  # Assuming "price" column exists
        price_sum = price_sum + price
        price_min = min(price_min, price)
        price_max = max(price_max, price)

        yield row_dict

    # Calculate average price after all rows (optional for better accuracy)
    average_price = price_sum / count if count > 0 else 0

    # Print final in-memory statistics (can be modified for desired output)
    print(f"\nFinal statistics for {file_name}:")
    print(f"Count: {count}")
    print(f"Average price: {average_price:.2f}")  # Format average price with 2 decimal places
    print(f"Minimum price: {price_min:.2f}")
    print(f"Maximum price: {price_max:.2f}")


# Process CSV files from Google Drive
# pylint: disable=W0105
"""
This section of the codebase orchestrates the sequential retrieval and processing
of CSV files sourced from Google Drive. Utilizing generators for efficient row-by-row
data loading, the process concludes by moving each processed file to a designated
folder within Google Drive. The overall workflow encompasses decoding CSV data,
converting timestamps, executing data pipelines for database integration,
computing basic statistics, and managing file archiving.
"""
for index, result in enumerate(resultCsvList):
    file_id = result["id"]
    csv_file = googledriveObject.download_file(file_id=file_id)

    print(file_id)
    print(result["name"])

    for chunk in csv_file:
        chunk_str = chunk.decode('utf-8')
        df_chunk = pd.read_csv(io.StringIO(chunk_str))
        df_chunk['timestamp'] = pd.to_datetime(df_chunk['timestamp'], format='%m/%d/%Y')
        # Extract the date part and create a new column
        df_chunk['timestamp'] = df_chunk['timestamp'].dt.date

        # Local test
        # pylint: disable=C0301
        # info = pipeline.run(df_pipeline(df_chunk,),table_name="fact_tablex", write_disposition="merge", primary_key=("user_id", "timestamp"),)

    # Running pipeline for generic_fact_table
    info = pipeline.run(
        df_pipeline(df=df_chunk, file_name=result["name"]),
        table_name="generic_fact_table",
        write_disposition="merge",
        primary_key=("user_id", "timestamp"),
    )

    # Calculate statistics for the CSV file
    count = df_chunk.shape[0]
    price_mean = df_chunk["price"].mean().item()
    price_min = df_chunk["price"].min().item()
    price_max = df_chunk["price"].max().item()
    file_name = result["name"]

    # Create statistics and send to a table calle statistics
    data = [
        {
            "count": count,
            "price_mean": price_mean,
            "price_min": price_min,
            "price_max": price_max,
            "file_name": file_name,
        }
    ]

    # Running pipeline for csv file
    info2 = pipeline.run(
        data,
        table_name="statistics",
        write_disposition="append",
    )

    # Move processed file to another folder
    move_file = googledriveObject.copy_and_delete_file(
        file_id=file_id, destination_folder_id=googleDriveFolderIdProccessed
    )
