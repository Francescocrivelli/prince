# TODO: LOGGING FOR HOW MUCH A USER IS SPENDING
# TODO: Logging for how many tokens are used
# TODO: Logging for how many requests are made
import os
from typing import Optional
from backend.app.config import Config


from elevenlabs import ElevenLabs, Voice, VoiceSettings


class TextToSpeech:
    """A class to handle text-to-speech conversion using ElevenLabs."""

    # Required environment variables
    REQUIRED_ENV_VARS = ["ELEVENLABS_API_KEY", "ELEVENLABS_VOICE_ID"]

    def __init__(self):
        """Initialize the TextToSpeech class and validate environment variables."""
        self._validate_env_vars()
        self._client: Optional[ElevenLabs] = None

    def _validate_env_vars(self) -> None:
        """Validate that all required environment variables are set."""
        missing_vars = [
            var for var in self.REQUIRED_ENV_VARS if not os.getenv(var)]
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}")

    @property
    def client(self) -> ElevenLabs:
        """Get or create ElevenLabs client instance using singleton pattern."""
        if self._client is None:
            self._client = ElevenLabs(api_key=Config.ELEVENLABS_API_KEY)
        return self._client

    async def synthesize(self, text: str) -> bytes:
        """Convert text to speech using ElevenLabs.

        Args:
            text: Text to convert to speech

        Returns:
            bytes: Audio data

        Raises:
            ValueError: If text is empty or exceeds maximum length
            Exception: If text-to-speech conversion fails
        """
        if not text.strip():
            raise ValueError("Input text cannot be empty")

        if len(text) > 5000:  # ElevenLabs typical limit
            raise ValueError(
                "Input text exceeds maximum length of 5000 characters")

        try:
            audio_generator = self.client.generate(
                text=text,
                voice=Voice(
                    voice_id=Config.ELEVENLABS_VOICE_ID,
                    settings=VoiceSettings(
                        stability=0.5, similarity_boost=0.5),
                ),
                model=Config.TTS_MODEL_NAME,
                output_format="pcm_22050"  # TODO: see how much latency this introduces
            )

            # Convert generator to bytes
            audio_bytes = b"".join(audio_generator)
            if not audio_bytes:
                raise ValueError("Generated audio is empty")

            return audio_bytes

        except Exception as e:
            raise ValueError(f"Text-to-speech conversion failed: {e}")
