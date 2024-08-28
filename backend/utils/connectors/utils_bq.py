from google.cloud import bigquery
from logger.logging import Logger

# Create logger object
logger = Logger(__name__)


class BigQueryConnector:
    """
    BigQuery Connector Class
    """

    def __init__(self, project_id: str) -> None:
        logger.debug("initializing properties of BigQueryConnector")
        self.__gcp_project_id: str = project_id

    @property
    def gcp_project_id(self) -> str:
        return self.__gcp_project_id

    @property
    def bq_client(self) -> bigquery.Client():
        return bigquery.Client(project=self.gcp_project_id)

    def execute_query(self, sql):
        job = self.bq_client.query(sql)
        result = job.to_dataframe().to_json(orient="records")
        return result

    def write_to_bq(self, data: dict, dataset_id: str, table_id: str):
        """
        Writes a dictionary of data into a BigQuery table.

        Args:
            data (dict): The data to be written to BigQuery. Assumes that dictionary
                keys correspond to BigQuery column names.
            dataset_id (str): The ID of the BigQuery dataset.
            table_id (str): The ID of the BigQuery table.
        """

        # Construct a fully qualified table reference
        table_ref = self.bq_client.dataset(dataset_id).table(table_id)

        # BigQuery expects data as a list of rows
        rows_to_insert = [data]

        # Specify how data should be inserted ("INSERT_ROWS" here)
        job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")

        # Error handling with try-except block
        try:
            errors = self.bq_client.insert_rows_json(
                table_ref, rows_to_insert, job_config=job_config
            )
            if errors == []:
                print(f"Successfully loaded data into {dataset_id}.{table_id}")
            else:
                print("Errors encountered during write:", errors)
        except Exception as e:
            print(f"Failed to write to BigQuery: {e}")
