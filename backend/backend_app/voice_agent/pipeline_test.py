from agents.voice.pipeline import VoicePipeline, VoicePipelineConfig
from agents.voice.pipeline import VoiceWorkflowBase
from agents.voice.pipeline import AudioInput
from backend.backend_app.voice_agent.text_to_speech import TextToSpeech
import asyncio
import numpy as np
import soundfile as sf
from scipy import signal
import os
from dotenv import load_dotenv
import sounddevice as sd
import simpleaudio as sa

# Load environment variables
load_dotenv()

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OpenAI API key not found in environment variables")


class EchoWorkflow(VoiceWorkflowBase):
    async def run(self, input_text: str):
        # A simple workflow that echoes back the input with a prefix.
        yield f"You said: {input_text}"


def load_audio_file(file_path: str, target_sample_rate: int = 8000) -> np.ndarray:
    """Load an audio file and convert it to Twilio's format (8kHz, mono, 16-bit)."""
    audio_data, sample_rate = sf.read(file_path)
    # Resample if needed
    if sample_rate != target_sample_rate:
        num_samples = int(len(audio_data) * target_sample_rate / sample_rate)
        audio_data = signal.resample(audio_data, num_samples)
        sample_rate = target_sample_rate
    # Ensure mono
    if len(audio_data.shape) > 1:
        audio_data = audio_data.mean(axis=1)
    # Convert to int16
    audio_data = (audio_data * 32767).astype(np.int16)
    return audio_data


def twilio_audio_to_input(audio_data: np.ndarray, sample_rate: int = 8000) -> AudioInput:
    """Convert audio data to AudioInput format."""
    return AudioInput(
        buffer=audio_data,
        frame_rate=sample_rate,  # Twilio uses 8kHz
        sample_width=2,          # 16-bit audio
        channels=1               # mono
    )


def save_audio_to_file(audio_data: np.ndarray, output_path: str, sample_rate: int = 8000):
    """Save audio data to a WAV file."""
    # Convert back to float32 for soundfile
    audio_float = audio_data.astype(np.float32) / 32767.0
    sf.write(output_path, audio_float, sample_rate)
    print(f"Saved audio to: {output_path}")


pipeline = VoicePipeline(
    workflow=EchoWorkflow(),
    tts_model=TextToSpeech(),
    config=VoicePipelineConfig()  # Use defaults or customize as needed
)


def play_audio_from_pcm(audio_bytes: bytes, sample_rate: int = 22050):
    # Convert byte stream to numpy int16 array
    audio_np = np.frombuffer(audio_bytes, dtype=np.int16)

    # Play raw PCM buffer
    play_obj = sa.play_buffer(
        audio_np, 1, 2, sample_rate)  # mono, 2 bytes/sample
    play_obj.wait_done()


async def main():
    try:
        # Load your pre-recorded audio file
        file_path = os.path.join(os.path.dirname(__file__), "test_audio.wav")
        print("Loading audio file...")
        audio_data = load_audio_file(file_path)

        # Convert to AudioInput format
        audio_input = twilio_audio_to_input(audio_data)

        # Run the pipeline; this returns a StreamedAudioResult
        print("Processing audio through pipeline...")
        output = await pipeline.run(audio_input=audio_input)
        print("Pipeline started. Streaming events:")
        # Accumulate the audio chunks from the TTS output.
        audio_chunks = []
        async for event in output.stream():
            if event.type == "voice_stream_event_audio":
                audio_chunks.append(event.data)
            elif event.type == "voice_stream_event_lifecycle":
                print(f"Lifecycle event: {event.event}")
            elif event.type == "voice_stream_event_error":
                print(f"Error: {event.error}")

        if audio_chunks:
            # Concatenate and play the output audio
            combined_audio = np.concatenate(audio_chunks)
            print("Playing synthesized audio output...")
            play_audio_from_pcm(combined_audio, sample_rate=22050)
        else:
            print("No audio output received.")

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
