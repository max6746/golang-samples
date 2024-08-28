from google.cloud import dialogflowcx_v3 as dialogflow
import uuid
from logger.logging import Logger

# Create logger object
logger = Logger(__name__)


class DecoupledDialogflow:
    """
    Dialogflow Python Client Based Integration Class
    """

    def __init__(
        self, project_id: str, location: str, agent_id: str, language_code: str
    ) -> None:
        """Intialize

        Args:
            project_id (str): Agent Project Id
            location (str): Location of Dialogflow Agent
            agent_id (str): Dialogflow Agent Id
            language_code (str): Language Code for the conversation
        """

        self.session_id = str(uuid.uuid4())
        self.client = dialogflow.SessionsClient()
        self.session = self.client.session_path(
            project_id, location, agent_id, self.session_id
        )
        self.language_code = language_code

    def send_message(self, user_input: str, context: list) -> str:
        """Send Message Method

        Args:
            user_input (str): User Utterance
            context (list): Context

        Returns:
            str: Agent Response
        """

        # Create a text input object
        text_input = dialogflow.types.TextInput(text=user_input)

        # Create a query input object
        query_input = dialogflow.types.QueryInput(
            text=text_input, language_code=self.language_code
        )

        # Create a detect intent request
        detect_intent_request = dialogflow.types.DetectIntentRequest(
            session=self.session, query_input=query_input
        )

        # Send the request and get the response
        response = self.client.detect_intent(detect_intent_request)

        # Process the response
        agent_response = ""
        for message in response.query_result.response_messages:
            if message.text.text:
                agent_response += ", ".join(
                    str(message) for message in message.text.text
                )

        # Check if the conversation should end
        if response.query_result.intent.is_fallback:
            logger.debug("Fallback:Agent could not understand your request.")

        return agent_response
