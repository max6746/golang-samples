from google.cloud import texttospeech, speech
from logger.logging import Logger

# Create logger object
logger = Logger(__name__)


class TexttoSpeech:
    def __init__(self, project_id: str, location: str = "us-central1") -> None:
        """Text to Speech Client Intialization

        Args:
            project_id (str): Project Id
            location (str): Location
        """
        self.project_id = project_id
        self.location = location
        self.client = texttospeech.TextToSpeechLongAudioSynthesizeClient()

    def synthesize_long_audio(
        self, text: str, output_gcs_uri: str, language_code: str, voice_name: str
    ):
        """
        Synthesizes long input, writing the resulting audio to `output_gcs_uri`.

        Example usage: synthesize_long_audio(''text', 'gs://{BUCKET_NAME}/{OUTPUT_FILE_NAME}.wav')

        """

        input = texttospeech.SynthesisInput(text=text)

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )

        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code, name=voice_name
        )

        parent = f"projects/{self.project_id}/locations/{self.location}"

        request = texttospeech.SynthesizeLongAudioRequest(
            parent=parent,
            input=input,
            audio_config=audio_config,
            voice=voice,
            output_gcs_uri=output_gcs_uri,
        )

        operation = self.client.synthesize_long_audio(request=request)
        # Set a deadline for your LRO to finish. 300 seconds is reasonable, but can be adjusted depending on the length of the input.
        # If the operation times out, that likely means there was an error. In that case, inspect the error, and try again.
        result = operation.result(timeout=300)
        logger.info(
            "\nFinished processing, check your GCS bucket to find your audio file!"
            + output_gcs_uri
        )
        return result


class SpeechtoText:
    def __init__(self, staging_bucket) -> None:
        self.staging_bucket = staging_bucket
        # Initialize Speech API client
        self.speech_client = speech.SpeechClient()

    def transcribe(
        self,
        audio_gcs_uri: str,
        language_code: str,
        model: str = None,
        audio_channel_count: int = 2,
    ) -> str:
        """Recogni

        Args:
            audio_gcs_uri (str): GCS URL of Audio file
            language_code (str): Language Code format eg: en-US
            model (str): model best suited to your domain to get best results eg: video (if audio is from video)
            audio_channel_count (int, optional): input files might not have 2 channels. Defaults to 2.

        Returns:
            str: Transcript URL
        """
        transcript_file = self.__update_file_suffix(audio_gcs_uri, "json")

        # Configure API request
        audio = speech.RecognitionAudio(uri=audio_gcs_uri)

        config = speech.RecognitionConfig(
            language_code=language_code,
            audio_channel_count=audio_channel_count,
            enable_separate_recognition_per_channel=True,
            enable_automatic_punctuation=True,
            model=model,
        )
        output_config = speech.TranscriptOutputConfig(
            gcs_uri=f"gs://{self.staging_bucket}/{transcript_file}"
        )

        if self.__file_exists(transcript_file):
            logger.info("Transcription already exists, skipping")
            return transcript_file

        request = speech.LongRunningRecognizeRequest(
            audio=audio,
            config=config,
            output_config=output_config,
        )

        # TODO: Make this a long poll on the returned Operation object
        logger.info("Starting transcription...")
        operation = self.speech_client.long_running_recognize(request=request)
        logger.info("Waiting for operation to complete...")
        response = operation.result(timeout=3600 * 3)
        logger.info("Transcription complete.")

        return transcript_file

        # Helper function to change file extensions (suffix)

    def __update_file_suffix(self, file, suffix):
        return file.split(".", 1)[0] + "." + suffix
