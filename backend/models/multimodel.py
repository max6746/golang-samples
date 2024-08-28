import base64
from typing import Dict
from vertexai.generative_models import GenerativeModel, Part
from vertexai.preview import generative_models

from logger.logging import Logger

# Create logger object
logger = Logger(__name__)


class MultiModel:
    """
    To Generate MultiModel Predictions
    """

    def __init__(
        self,
        model: str,
        generation_config: Dict[str, str] = None,
    ):
        """Generate text based on prompt.

        Args:
        model: model name
        parameters: The parameters used for the model.

        """

        self.generation_config = generation_config
        self.model_endpoint = GenerativeModel(model)
        self.safety_settings = {
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }
        logger.info("Intialized Multimodel Gemini Instance")

    def predict(self, prompt: str, image_bytes: str) -> str:
        """Predict Method

        Args:
            prompt (str): User text input
            image_bytes (str): Image Input in bytes

        Returns:
            str: Generated Text Response from the model
        """

        image1 = Part.from_data(
            mime_type="image/png", data=base64.b64decode(image_bytes)
        )

        response = self.model_endpoint.generate_content(
            [prompt, image1],
            generation_config=self.generation_config,
            safety_settings=self.safety_settings,
            stream=False,
        )
        logger.debug(f"Prediction Response: {response}")
        return response.text
