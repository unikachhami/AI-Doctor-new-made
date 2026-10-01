import logging
import os
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def record_audio_simple(
    filepath,
    timeout=20,
    phrase_time_limit=None
):
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:

            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            logging.info("Start speaking now...")

            record_data = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit
            )

            logging.info("Recording complete.")

            wav_data = record_data.get_wav_data()

            audio_segment = AudioSegment.from_wav(
                BytesIO(wav_data)
            )

            audio_segment.export(
                filepath,
                format="mp3",
                bitrate="128k"
            )

            logging.info(
                f"Audio saved to {filepath}"
            )

            return filepath

    except Exception as e:
        logging.error(f"Audio recording error: {e}")
        return None


def transcribe_using_groq(
    stt_model,
    audio_file_path,
    GROQ_API_KEY
):

    if not audio_file_path:
        raise ValueError("No audio file received.")

    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(
            f"Audio file not found: {audio_file_path}"
        )

    client = Groq(api_key=GROQ_API_KEY)

    with open(audio_file_path, "rb") as audio_file:

        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model=stt_model,
            language="en",
            response_format="json",
            temperature=0
        )

    return transcription.text.strip()
