
"""Microphone recording and OpenAI Whisper speech-to-text."""

import io

import sounddevice as sd
import soundfile as sf

from SnackStack.config import get_logger, openai_client

logger = get_logger("voice_recorder")


class VoiceRecorder:
    """Record microphone audio and convert speech into text."""

    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate

    def record(self, duration: int = 5) -> bytes:
        """Record audio and return it as WAV bytes."""

        print(f"\nRecording for {duration} seconds. Speak now!")

        audio = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32",
        )
        sd.wait()

        buffer = io.BytesIO()
        sf.write(
            buffer,
            audio,
            self.sample_rate,
            format="WAV",
        )

        logger.info("Recording completed.")
        return buffer.getvalue()

    def transcribe(self, wav_data: bytes, language: str = "en") -> str:
        """Send WAV audio to Whisper and return the transcript."""

        audio_file = io.BytesIO(wav_data)
        audio_file.name = "recording.wav"

        try:
            result = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=language,
            )

            text = result.text.strip()
            logger.info("Transcription: %s", text)

            if text:
                print(f"You said: {text}")

            return text

        except Exception:
            logger.exception("Whisper transcription failed.")
            return ""

    def listen(self, duration: int = 5) -> str:
        """Record microphone audio and return the recognized text."""

        wav_data = self.record(duration)
        return self.transcribe(wav_data)
