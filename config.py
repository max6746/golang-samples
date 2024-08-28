# config.py


class Config:
    """
    Application Configurations
    """

    # Google Cloud Project Global Configurations
    PROJECT_ID = "ezyai-demos"
    LOCATION = "us-central1"

    # Generative AI model and parameters

    # Prompts
    DEFAULT_SYSTEM_INSTRUCTION = """
        You are an expert researcher. You always stick to the facts in the sources provided, and never make up new facts.
        Now look at these documents papers, and answer the following questions.
    """

    # Secrets Name
