import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import elevenlabs

load_dotenv()

ELEVEN_LABS_API_KEY = os.getenv(
    "ELEVEN_LABS_API_KEY"
)


def text_to_speech_elevenlabs(
    input_text,
    output_filepath
):

    if not input_text:
        raise ValueError("No text provided for speech.")

    if not ELEVEN_LABS_API_KEY:
        raise ValueError(
            "ELEVEN_LABS_API_KEY not found in .env"
        )

    client = ElevenLabs(
        api_key=ELEVEN_LABS_API_KEY
    )

    audio = client.text_to_speech.convert(
        text=input_text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_flash_v2_5",
        output_format="mp3_44100_128"
    )

    elevenlabs.save(
        audio,
        output_filepath
    )

    return output_filepath

