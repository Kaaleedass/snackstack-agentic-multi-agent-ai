
"""OpenAI text-to-speech and audio playback."""

import io

import sounddevice as sd
import soundfile as sf

from SnackStack.config import get_logger, openai_client

logger = get_logger("voice_speaker")


class VoiceSpeaker:
    """Convert text into speech and play the generated WAV audio."""

    def __init__(self, voice: str = "nova", speed: float = 1.0):
        self.voice = voice
        self.speed = speed

    def speak(self, text: str) -> None:
        """Generate WAV speech and play it."""

        if not text or not text.strip():
            return

        try:
            response = openai_client.audio.speech.create(
                model="tts-1",
                voice=self.voice,
                input=text,
                speed=self.speed,
                response_format="wav",
            )

            audio_data, sample_rate = sf.read(
                io.BytesIO(response.content),
                dtype="float32",
            )

            sd.play(audio_data, sample_rate)
            sd.wait()

            logger.info("Speech playback completed.")

        except Exception:
            logger.exception("Text-to-speech or audio playback failed.")
