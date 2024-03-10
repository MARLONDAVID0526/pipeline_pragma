# %%
# pylint: disable=R0801
import os

# import duckdb
from dotenv import dotenv_values

# Loading local packages
# pylint: disable=E0401
from modules.apis.google_drive import googledrive

env_variables = dotenv_values(".env")


googleDriveUrl = os.getenv("folderUrl")
googleDriveFolderId = os.getenv(
    "folderGoogleDrive",
)
googleDriveFolderIdProccessed = os.getenv("folderGoogleDriveProcessed")

serviceAccountPath = os.getenv("serviceAccountJsonKeyPath")
gDFolderUrl = os.getenv("gDFolderUrl")

googledriveObject = googledrive.GoogleDriveAPI(
    service_account_path=serviceAccountPath, folder_id=googleDriveFolderId
)

path_list = [
    "../tests/dataset_testing/2012-1.csv",
    "../tests/dataset_testing/2012-2.csv",
    "../tests/dataset_testing/2012-3.csv",
    "../tests/dataset_testing/2012-4.csv",
    "../tests/dataset_testing/2012-5.csv",
    "../tests/dataset_testing/validation.csv",
]

for path_ in path_list:
    upload = googledriveObject.upload_file(
        file_path=path_, folder_id="1Igp_dLYVV29bJRMIJyQoRdcnI82PH1eK"
    )

resultCsvList = googledriveObject.list_files()

"""
file_id = "1tSZetLOULX3BVt8a6acPvBDrVJ0vChZa"
move_file = googledriveObject.copy_and_delete_file(file_id=file_id,
destination_folder_id=googleDriveFolderIdProccessed)
#create_folder = googledriveObject.create_folder(folder_name = "pragma_pipeline_raw")

shared_folder = googledriveObject.share_folder_with_user(
    folder_id="1Igp_dLYVV29bJRMIJyQoRdcnI82PH1eK",
    email="marlondavid0526.gcp.2024.02.08@gmail.com",
    role="writer")"""
