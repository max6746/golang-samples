# Utility Module for GenAI Agent

from abc import ABC, abstractmethod
from vertexai.generative_models import (
    FunctionDeclaration,
    GenerativeModel,
    Part,
    Tool,
)

from logger.logging import Logger

# Create logger object
logger = Logger(__name__)


class BaseAgent(ABC):
    """
    Base agent class

    Args:
        functions: list of functions/tools can be used by agent
    """

    def __init__(self, functions, config=None):
        """Intitializer

        Args:
            functions (list): list of tools
            config: Configuration instance class
        """
        self.function_declarations = []
        for function in functions:
            self.function_declarations.append(
                self.add_function_declaration(
                    function["name"], function["description"], function["parameters"]
                )
            )
        self.tools = Tool(function_declarations=self.function_declarations)

    def add_function_declaration(self, name, description, parameters):
        """Method to add Function Declaration

        Args:
            name (str): name of function
            description (str): precise description of function
            parameters (dict): defination of paramters passed to functions

        Returns:
            _type_: FunctionDeclaration object
        """
        function_declaration = FunctionDeclaration(
            name=name,
            description=description,
            parameters=parameters,
        )
        return function_declaration

    def predict(self, prompt, model_name="gemini-1.5-pro"):
        """Predict Method

        Args:
            prompt (str): user prompt

        Returns:
            dict: model response
        """
        self.model = GenerativeModel(model_name)
        response = self.model.generate_content(
            prompt,
            generation_config={"temperature": 0},
            tools=[self.tools],
        )
        return response

    def get_chat_session(self, model_name="gemini-1.5-pro"):
        """Create chat sessions

        Returns:
            chat_session: chat session object
        """
        model = GenerativeModel(
            model_name, generation_config={"temperature": 0}, tools=[self.tools]
        )
        self.chat_session = model.start_chat()
        return self.chat_session

    def run(self, prompt):
        """Orchestrates the multi-agent workflow.

        Args:
            prompt: A description of the overall task.
        """
        self.prompt = prompt
        # Step 2: Prompt Gemini to get function call

        response = self.chat_session.send_message(prompt)
        response = response.candidates[0].content.parts[0]

        # Step 3: Call Agent

        function_calling_in_process = True
        while function_calling_in_process:
            try:
                params = {}
                for key, value in response.function_call.args.items():
                    params[key] = value

                logger.debug(
                    f"[Agent] Predicted Funtion Call: {response.function_call.name}"
                )

                func_response = self._call_function(response.function_call.name, params)

                logger.debug(f"[Agent] Function Response: {func_response}")

                response = self.chat_session.send_message(
                    Part.from_function_response(
                        name=response.function_call.name,
                        response={
                            "content": func_response,
                        },
                    ),
                )
                response = response.candidates[0].content.parts[0]

            except AttributeError:
                function_calling_in_process = False

        return str(response)

    @abstractmethod
    def _call_function(self, function_name, params) -> str:
        """Abstract Method to be overriden by agent based
          on use case.

        Args:
            function_name (str): predicted function name
            params (dict): parameters for function

        Returns:
            str: response from the function call
        """
        pass
