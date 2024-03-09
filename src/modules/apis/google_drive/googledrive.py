import io

from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload
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
