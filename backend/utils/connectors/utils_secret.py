from google.cloud import secretmanager


class SecretManagerConnector:
    """
    Modular class to interact with Google Secret Manager.
    """

    def __init__(self, project_id):
        """
        Initializes the connector.

        Args:
            project_id (str): The ID of the Google Cloud project.
        """
        self.project_id = project_id
        self._client = secretmanager.SecretManagerServiceClient()

    def create_secret(self, secret_id, secret_value):
        """
        Creates a new secret in Secret Manager.

        Args:
            secret_id (str): The name of the secret to create.
            secret_value (str): The value of the secret.
        """
        parent = f"projects/{self.project_id}"

        response = self._client.create_secret(
            request={
                "parent": parent,
                "secret_id": secret_id,
                "secret": {"replication": {"automatic": {}}},
            }
        )
        print(f"Created secret: {response.name}")

    def add_secret_version(self, secret_id, secret_value):
        """
        Adds a new version to an existing secret.

        Args:
            secret_id (str): The name of the secret.
            secret_value (str): The new version of the secret.
        """
        parent = f"projects/{self.project_id}/secrets/{secret_id}"

        payload = secretmanager.SecretPayload(data=secret_value.encode("utf-8"))
        response = self._client.add_secret_version(
            request={"parent": parent, "payload": payload}
        )
        print(f"Added secret version: {response.name}")

    def access_secret_version(self, secret_id, version_id="latest"):
        """
        Retrieves the value of a secret version.

        Args:
            secret_id (str): The name of the secret.
            version_id (str, optional): The version ID of the secret to access.
                                        Defaults to "latest".

        Returns:
            str: The secret value.
        """
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self._client.access_secret_version(request={"name": name})
        return response.payload.data.decode("utf-8")
