import io
import os

from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.discovery import build


class GoogleDriveAPI:
    """
    Clase para interactuar con la API de Google Drive.

    Attributes:
        service_account_path (str): La ruta al archivo de credenciales de servicio.
        folder_id (str): El ID de la carpeta de Google Drive con la que se interactuará.
    """

    def __init__(self, service_account_path: str, folder_id: str):
        """
        Inicializa una instancia de GoogleDriveAPI.

        Args:
            service_account_path (str): La ruta al archivo de credenciales de servicio.
            folder_id (str): El ID de la carpeta de Google Drive con la que se interactuará.
        """
        self.scope = ['https://www.googleapis.com/auth/drive']
        self.credentials = service_account.Credentials.from_service_account_file(
            filename=service_account_path, scopes=self.scope
        )
        self.service = build('drive', 'v3', credentials=self.credentials)
        self.folder_id = folder_id

    def list_files(self, mime_type: str = 'text/csv'):
        """
        This function lists files in a specified folder within your Google Drive.

        Args:
            mime_type (str, optional): The type of files to list (e.g., 'text/csv').
              Defaults to 'text/csv'.

        Returns:
            list: A list of dictionaries containing information about the files found
                (e.g., ID and name). If no files are found, an empty list is returned.
        """
        # pylint: disable=E1101
        query = f"mimeType='{mime_type}' and '{self.folder_id}' in parents"
        results = self.service.files().list(q=query, fields="files(id, name)").execute()
        # Check if 'files' key exists before accessing it
        return results.get('files', [])  # Return empty list if 'files' is missing

    def download_file(self, file_id: str):
        """
        Descarga un archivo de Google Drive.

        Args:
            file_id (str): El ID del archivo que se va a descargar.

        Yields:
            bytes: Los datos del archivo descargado.
        """
        # pylint: disable=E1101
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            yield fh.getvalue()
            fh.seek(0)
            print(status)

    def copy_and_delete_file(self, file_id: str, destination_folder_id: str):
        """
        Copies a file to another folder based on its file ID, and then deletes the original file.

        Args:
            file_id (str): The ID of the file to copy and delete.
            destination_folder_id (str): The ID of the destination
            folder where the copied file will be placed.
        """
        # Copy the file to the destination folder
        # pylint: disable=E1101
        copied_file = (
            self.service.files()
            .copy(fileId=file_id, body={"parents": [destination_folder_id]})
            .execute()
        )
        copied_file_id = copied_file.get('id')
        # body_value = {'trashed': True}
        # Delete the original file
        # pylint: disable=E1101
        self.service.files().delete(fileId=file_id).execute()
        return copied_file_id

    def create_folder(self, folder_name: str, parent_folder_id: str = None):
        """
        Crea una carpeta en Google Drive.

        Args:
            folder_name (str): El nombre de la carpeta que se va a crear.
            parent_folder_id (str, optional): El ID de la carpeta padre
            en la que se creará la carpeta.Si no se proporciona,
            la carpeta se creará en el directorio raíz de Google Drive.

        Returns:
            dict: Un diccionario que contiene información sobre la carpeta creada (incluido su ID).
        """
        folder_metadata = {'name': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
        if parent_folder_id:
            folder_metadata['parents'] = [parent_folder_id]
        # pylint: disable=E1101
        folder = self.service.files().create(body=folder_metadata, fields='id').execute()
        return folder

    def share_folder_with_user(self, folder_id: str, email: str, role: str = 'reader'):
        """
        Comparte una carpeta en Google Drive con una cuenta de usuario.

        Args:
            folder_id (str): El ID de la carpeta que se compartirá.
            email (str): La dirección de correo electrónico de la cuenta
            de usuario con la que se compartirá la carpeta.
            role (str, optional): El rol que se otorgará a la
            cuenta de usuario en la carpeta.
                Puede ser 'owner', 'organizer', 'fileOrganizer', 'writer' o 'reader'.
                Por defecto, se establece en 'reader', que proporciona permisos de solo lectura.

        Returns:
            dict: Un diccionario que contiene información sobre el nuevo permiso creado.
        """
        permission_metadata = {'type': 'user', 'role': role, 'emailAddress': email}
        # pylint: disable=E1101
        permission = (
            self.service.permissions().create(fileId=folder_id, body=permission_metadata).execute()
        )
        return permission

    def upload_file(self, file_path: str, folder_id: str):
        """
        Uploads a file to a folder in Google Drive.

        Args:
            file_path (str): The local path to the file to be uploaded.
            folder_id (str): The ID of the folder in Google Drive where the file will be uploaded.
        """
        file_metadata = {'name': os.path.basename(file_path), 'parents': [folder_id]}
        # pylint: disable=E1101
        media = MediaFileUpload(file_path, resumable=True)
        file = (
            self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        )
        return file
