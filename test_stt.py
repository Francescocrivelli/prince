import asyncio
import numpy as np
import os
import wave
from backend.backend_app.config import Config
from backend.backend_app.voice_agent.speech_to_text import RealTimeSpeechToText

# Configure logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def generate_test_audio(duration_seconds=5, sample_rate=16000, frequency=440):
    """Generate a test audio sine wave of specified duration and frequency.

    Args:
        duration_seconds: Length of audio in seconds
        sample_rate: Audio sample rate in Hz
        frequency: Frequency of tone in Hz

    Returns:
        Bytes containing the audio data in PCM format
    """
    # Generate time array
    t = np.linspace(0, duration_seconds, int(
        sample_rate * duration_seconds), False)

    # Generate sine wave
    tone = np.sin(frequency * 2 * np.pi * t)

    # Normalize and convert to int16
    tone = (tone * 32767).astype(np.int16)

    # Convert to bytes
    audio_bytes = tone.tobytes()

    # Save the test audio to a WAV file for reference
    with wave.open('test_audio.wav', 'wb') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 2 bytes per sample (16-bit)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_bytes)

    logger.info(
        f"Generated {duration_seconds}s test audio ({len(audio_bytes)} bytes) saved to test_audio.wav")
    return audio_bytes


def transcript_callback(text, is_final):
    """Callback to process incoming transcripts"""
    if is_final:
        logger.info(f"FINAL TRANSCRIPT: {text}")
    else:
        logger.info(f"Interim transcript: {text}")


async def test_with_large_audio():
    """Test the RealTimeSpeechToText with a large audio sample"""
    # Get API key
    config = Config()
    api_key = config.OPENAI_API_KEY

    if not api_key:
        logger.error(
            "No API key found. Please set OPENAI_API_KEY in your environment.")
        return

    # Generate test audio (5 seconds)
    audio_data = generate_test_audio(duration_seconds=5)

    # Create STT instance
    stt = RealTimeSpeechToText(api_key=api_key)

    # Add transcript callback
    stt.add_transcript_callback(transcript_callback)

    try:
        # Connect to the API
        logger.info("Connecting to OpenAI API...")
        await stt.connect()

        # Send audio in chunks to simulate streaming
        # Use 1-second chunks instead of 0.5-second chunks
        chunk_size = 32000  # 1s at 16kHz, 2 bytes per sample

        logger.info(f"Sending audio in chunks of {chunk_size} bytes...")
        for i in range(0, len(audio_data), chunk_size):
            chunk = audio_data[i:i+chunk_size]
            logger.info(
                f"Sending chunk {i//chunk_size + 1}/{len(audio_data)//chunk_size + 1} ({len(chunk)} bytes)")
            await stt.send_audio(chunk)
            # Longer delay between chunks to give API time to process
            await asyncio.sleep(0.5)

        # Wait a bit for processing to complete
        logger.info("Waiting for final transcripts...")
        await asyncio.sleep(5)

    except Exception as e:
        logger.error(f"Error during test: {str(e)}")
    finally:
        # Close the connection and get the final transcript
        logger.info("Closing connection...")
        final_transcript = await stt.stop()
        logger.info(f"Test complete. Final transcript: {final_transcript}")


if __name__ == "__main__":
    logger.info("Starting STT test with large audio sample...")
    asyncio.run(test_with_large_audio())
