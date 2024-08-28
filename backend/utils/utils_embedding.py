from google.cloud import aiplatform
from google.protobuf import struct_pb2


class GenerateEmbeddings:
    """
    Utility module for Vertex AI embeddings generations
    """

    def __init__(self, project_id: str, location: str) -> None:
        self.api_endpoint = "us-central1-aiplatform.googleapis.com"
        self.PROJECT_ID = project_id
        self.LOCATION = location

    def get_embedding(self, text: str = None, image_file: str = None):
        client = aiplatform.gapic.PredictionServiceClient(
            client_options={"api_endpoint": self.api_endpoint}
        )
        image_bytes = image_file

        instance = struct_pb2.Struct()

        if text:
            instance.fields["text"].string_value = text

        if image_bytes:
            encoded_content = image_file
            image_struct = instance.fields["image"].struct_value
            image_struct.fields["bytesBase64Encoded"].string_value = encoded_content

        instances = [instance]
        endpoint = (
            f"projects/{self.PROJECT_ID}/locations/{self.LOCATION}"
            "/publishers/google/models/multimodalembedding"
        )
        response = client.predict(endpoint=endpoint, instances=instances)

        embedding = None

        if text:
            text_emb_value = response.predictions[0]["textEmbedding"]
            embedding = [v for v in text_emb_value]

        elif image_bytes:
            image_emb_value = response.predictions[0]["imageEmbedding"]
            embedding = [v for v in image_emb_value]

        return embedding
