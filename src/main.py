import io
import os
import time

import dlt

# import duckdb
import pandas as pd
from dotenv import dotenv_values

# Loading local packages
from modules.apis.google_drive import googledrive

env_variables = dotenv_values(".env")


googleDriveUrl = os.getenv("folderUrl")
googleDriveFolderId = os.getenv(
    "folderGoogleDrive",
)
serviceAccountPath = os.getenv("serviceAccountJsonKeyPath")
gDFolderUrl = os.getenv("gDFolderUrl")

print("gDFolderUrl", gDFolderUrl)

# %%
googledriveObject = googledrive.GoogleDriveAPI(
    service_account_path=serviceAccountPath, folder_id=googleDriveFolderId
)


# %%

resultCsvList = googledriveObject.list_files()
# Function to authenticate with Google Drive


# %%
def df_pipeline(
    df: pd.DataFrame,
) -> iter:
    """
    Generate dictionaries from DataFrame rows.

    Parameters:
        df (pd.DataFrame): Input DataFrame to iterate over.

    Yields:
        dict: A dictionary representing each row of the DataFrame.
    """
    # Iterate over rows in the DataFrame
    for index_df, row in df.iterrows():
        time.sleep(0.5)
        print(f"Insert row{index_df}", row.to_dict())
        yield row.to_dict()


# %%
# File ID from Google Drive
dfs = []

pipeline = dlt.pipeline(destination="duckdb", dataset_name="people")

for index, result in enumerate(resultCsvList[0:6]):
    file_id = result["id"]
    csv_file = googledriveObject.download_file(file_id=file_id)

    print(file_id)
    for chunk in csv_file:
        chunk_str = chunk.decode('utf-8')
        df_chunk = pd.read_csv(io.StringIO(chunk_str))
        print(df_chunk)
        print("------")
        dfs.append(len(df_chunk))
        info = pipeline.run(
            df_pipeline(
                df_chunk,
            ),
            table_name="fact_tablex",
            write_disposition="merge",
            primary_key=("user_id", "timestamp"),
        )
