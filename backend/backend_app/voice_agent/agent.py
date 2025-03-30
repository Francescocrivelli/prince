import asyncio
from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
from backend.app.config import Config
from backend.app.voice_agent.text_to_speech import TextToSpeech
import simpleaudio as sa
import numpy as np
import io


# tool to process worker registration details
load_dotenv()

# get from the config file
openai_api_key = Config.OPENAI_API_KEY
elevenlabs_api_key = Config.ELEVENLABS_API_KEY
elevenlabs_voice_id = Config.ELEVENLABS_VOICE_ID


@function_tool
def process_worker_registration(name: str, phone: str, location: str, language: str):
    """
    Process the worker registration details and save them to the database.
    """
    print(
        f"Processing worker registration for {name} with phone {phone}")

    # save to database
    # TODO: Francesco needs to save to chroma db

    # send confirmation message

    return f"details are the following: {name}, {phone}, {location}, {language}"


worker_registration_agent = Agent(
    name="Worker Registration Agent",
    instructions=(
        "You are an agent that handles blue-collar worker registrations. "
        "Capture and validate worker information (name, location, skills, language) from voice or SMS inputs. "
        "Use the process_registration tool to register workers in the system."
    ),
    tools=[process_worker_registration]
)

# make tts object
tts = TextToSpeech()


def play_audio_from_pcm(audio_bytes: bytes, sample_rate: int = 22050):
    # Convert byte stream to numpy int16 array
    audio_np = np.frombuffer(audio_bytes, dtype=np.int16)

    # Play raw PCM buffer
    play_obj = sa.play_buffer(
        audio_np, 1, 2, sample_rate)  # mono, 2 bytes/sample
    play_obj.wait_done()


async def main():
    result = await Runner.run(worker_registration_agent,
                              "My name is Kaleb Cole and I live in San Francisco, CA. I speak English and Spanish. My phone number is 123-456-7890.")
    print(result.final_output)
    output_audio = await tts.synthesize(result.final_output)
    play_audio_from_pcm(output_audio)

if __name__ == "__main__":
    asyncio.run(main())
