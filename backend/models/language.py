"""LLM text predictor."""

from typing import Dict
from vertexai.language_models import (
    CodeGenerationModel,
    TextGenerationModel,
    CodeChatModel,
)
from vertexai.language_models import ChatModel
from vertexai.generative_models import GenerativeModel, GenerationConfig

from logger.logging import Logger

# Create logger object
logger = Logger(__name__)


class TextModel:
    """Vertex Text Generation Model Class.

    Attributes:
        model: model name
        parameters: The parameters used for the model.
        llm_endpoint: The endpoint for the model.
    """

    def __init__(
        self,
        model: str,
        parameters: Dict[str, str] = {"temperature": 0.5},
        tuned_model: str = None,
    ):
        """Generate text based on prompt.

        Args:
        model: model name
        parameters: The parameters used for the model.
        tuned_model: Full Qualified Model name: projects/{PROJECT}/locations/{LOCATION}/models/{MODELID}
        """

        self.parameters = parameters
        self.model = model

        if "text-" in model:
            self.llm_endpoint = TextGenerationModel.from_pretrained(model)
        elif "code-" in model:
            self.llm_endpoint = CodeGenerationModel.from_pretrained(model)
        elif "gemini-" in model:
            self.llm_endpoint = GenerativeModel(model)
            self.parameters = GenerationConfig(**parameters)
        else:
            # Log request for debugging
            logger.error(f"{model} not supported.")
            raise ValueError(f"{model} not supported.")
        if tuned_model and "gemini" not in model:
            self.llm_endpoint = self.llm_endpoint.get_tuned_model(tuned_model)

    def predict(self, prompt: str) -> str:
        """Generate text based on prompt.

        Args:
        prompt: Prompt

        Returns:
        Generated Text.
        """
        # Log request for debugging
        logger.debug(f"Generating Text for prompt: {prompt}")
        if "text-" in self.model or "code-" in self.model:
            predict_response = self.llm_endpoint.predict(prompt, **self.parameters).text
        elif "gemini-" in self.model:
            predict_response = self.llm_endpoint.generate_content(
                prompt, generation_config=self.parameters
            ).text

        return predict_response


class MyChatModel:
    """Vertex Language Model Class.

    Attributes:
        model: model name
        parameters: The parameters used for the model.
        llm_endpoint: The endpoint for the model.
    """

    def __init__(self, model: str, parameters: Dict[str, str] = None):
        """Generate text based on prompt.

        Args:
        model: model name
        parameters: The parameters used for the model.

        """

        self.parameters = parameters
        self.model = model

        if "chat-bison" in model:
            self.chat_model = ChatModel.from_pretrained(model)
        elif "codechat-" in model:
            self.chat_model = CodeChatModel.from_pretrained(model)
        elif "gemini-" in model:
            self.chat_model = GenerativeModel(model)
        else:
            # Log request for debugging
            logger.error(f"{model} not supported.")
            raise ValueError(f"{model} not supported.")
        self.chat_session = self.chat_model.start_chat()

    def get_chat_response(self, prompt: str) -> str:
        response = self.chat_session.send_message(prompt)
        return response.text
