# %%
# %%
import io
import os

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
# File ID from Google Drive
dfs = []
for index, result in enumerate(resultCsvList):
    file_id = result["id"]
    csv_file = googledriveObject.download_file(file_id=file_id)

    print(file_id)
    progress = 0
    for chunk in csv_file:
        chunk_str = chunk.decode('utf-8')
        df_chunk = pd.read_csv(io.StringIO(chunk_str))
        print(df_chunk)
        print("------")
        dfs.append(df_chunk)
    # Concatenate all DataFrame chunks into a single DataFrame
    df = pd.concat(dfs, ignore_index=True)
