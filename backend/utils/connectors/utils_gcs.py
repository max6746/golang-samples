from google.cloud import storage
from logger.logging import Logger

# Create logger object
logger = Logger(__name__)


class GCSConnector:
    """
    GCS Connector Class
    """

    def __init__(self, project_id: str, bucket_name: str) -> None:
        logger.debug("initializing properties of GCSConnector")
        self.__gcp_project_id: str = project_id
        self.__bucket_name: str = bucket_name

    @property
    def gcp_project_id(self) -> str:
        return self.__gcp_project_id

    @property
    def bucket_name(self) -> str:
        return self.__bucket_name

    @property
    def get_gcs_client(self):
        return storage.Client(project=self.gcp_project_id)

    def read_text(self, file_path: str) -> str:
        gcp_resp = self.get_gcs_client().get_bucket(self.bucket_name).blob(file_path)
        text_data: str = gcp_resp.download_as_string().decode("utf-8")
        return text_data

    def write_text(self, data: str, file_path: str) -> None:
        self.get_gcs_client().get_bucket(self.bucket_name).blob(
            file_path,
        ).upload_from_string(data)
