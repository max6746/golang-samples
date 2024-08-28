from google.cloud import translate_v3 as translate


class GoogleCloudVertexTranslator:
    """A class for connecting to Google Cloud Vertex Translate and performing various translation operations.

    Attributes:
        project_id (str): The Google Cloud project ID.
        client (google.cloud.translate_v2.Client): The Translation API client.
    """

    def __init__(self, project_id):
        """
        Initializes the translator object.

        Args:
            project_id (str): The Google Cloud project ID. This can also be
                set from the environment variable GOOGLE_CLOUD_PROJECT.
        """
        self.project_id = project_id
        self.client = translate.TranslationServiceClient()

    def translate_text(self, text, target_language, source_language=None):
        """
        Translates text from the source language to the target language.

        Args:
            text (str): The text to be translated.
            target_language (str): The target language code (e.g., 'en', 'es').
            source_language (str, optional): The source language code (e.g., 'fr').
                If not provided, automatic language detection will be used.

        Returns:
            str: The translated text.
        """

        if not text:
            return ""
        # Initialize request argument(s)
        request = translate.TranslateTextRequest(
            contents=[text],
            target_language_code=target_language,
            parent=f"projects/{self.project_id}/locations/global",
        )
        # Make the request
        response = self.client.translate_text(request=request)
        for translation in response.translations:
            return translation.translated_text
