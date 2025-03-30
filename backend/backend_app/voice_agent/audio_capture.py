import logging
import threading
import time
import wave
from pathlib import Path
from typing import Callable, List, Optional

import pyaudio
import webrtcvad

logger = logging.getLogger(__name__)


class AudioCapture:
    """Captures audio from a microphone and sends it to a callback function."""

    # Audio format constants
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 480  # 30ms chunks at 16kHz (WebRTC VAD requirement)
    SILENCE_THRESHOLD = 0.3  # Seconds of silence to detect end of speech
    MIN_SPEECH_DURATION = 0.5  # Minimum duration of speech to send

    def __init__(self):
        """Initialize audio capture."""
        self.pyaudio = pyaudio.PyAudio()
        self.stream: Optional[pyaudio.Stream] = None
        self.callbacks: List[Callable[[bytes], None]] = []
        self.is_recording = False
        self.thread: Optional[threading.Thread] = None
        self.recorded_chunks: List[bytes] = []

        # Voice activity detection
        self.vad = webrtcvad.Vad(3)  # Aggressiveness level 3 (highest)
        self.speech_buffer = b''
        self.last_speech_time = 0
        self.silence_start_time = 0
        self.is_speaking = False

    def add_callback(self, callback: Callable[[bytes], None]) -> None:
        """Add a callback to be called with captured audio chunks.

        Args:
            callback: Function that takes audio_data (bytes) as argument
        """
        self.callbacks.append(callback)

    
    def _is_speech(self, audio_chunk: bytes) -> bool:
        """Check if the audio chunk contains speech using WebRTC VAD.

        Args:
            audio_chunk: Raw PCM audio bytes (16-bit, 16kHz, mono)

        Returns:
            bool: True if speech is detected, False otherwise
        """
        try:
            # WebRTC VAD requires 30ms chunks
            return self.vad.is_speech(audio_chunk, self.RATE)
        except Exception as e:
            logger.error(f"Error in VAD: {str(e)}")
            return False

    def _process_audio_chunk(self, audio_chunk: bytes) -> None:
        """Process an audio chunk and detect speech pauses.

        Args:
            audio_chunk: Raw PCM audio bytes (16-bit, 16kHz, mono)
        """
        current_time = time.time()

        # Check if this chunk contains speech
        if self._is_speech(audio_chunk):
            self.speech_buffer += audio_chunk
            self.last_speech_time = current_time
            self.is_speaking = True
            self.silence_start_time = 0
        else:
            if self.is_speaking:
                self.speech_buffer += audio_chunk
                if not self.silence_start_time:
                    self.silence_start_time = current_time
                elif current_time - self.silence_start_time >= self.SILENCE_THRESHOLD:
                    # We've detected a speech pause
                    # Calculate minimum bytes needed (100ms at 16kHz, 16-bit mono)
                    # 100ms * 16000Hz * 2 bytes
                    min_bytes = int(0.1 * self.RATE * 2)

                    if len(self.speech_buffer) >= min_bytes:
                        # Send the accumulated speech buffer
                        for callback in self.callbacks:
                            try:
                                callback(self.speech_buffer)
                            except Exception as e:
                                logger.error(
                                    f"Error in audio callback: {str(e)}")
                        self.speech_buffer = b''
                    self.is_speaking = False
                    self.silence_start_time = 0

    def _audio_callback(self, in_data, frame_count, time_info, status_flags):
        """Internal callback for PyAudio."""
        if status_flags:
            logger.warning(f"PyAudio status flags: {status_flags}")

        # Store the audio data
        self.recorded_chunks.append(in_data)

        # Process the audio chunk for speech detection
        self._process_audio_chunk(in_data)

        return (in_data, pyaudio.paContinue)

    def start_recording(self, device_index: Optional[int] = None) -> None:
        """Start recording audio.

        Args:
            device_index: Index of audio device to use. None for default.
        """
        if self.is_recording:
            logger.warning("Already recording")
            return

        self.recorded_chunks = []
        self.speech_buffer = b''
        self.last_speech_time = 0
        self.silence_start_time = 0
        self.is_speaking = False
        self.is_recording = True

        try:
            # Open the audio stream
            self.stream = self.pyaudio.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK,
                stream_callback=self._audio_callback,
                input_device_index=device_index
            )

            logger.info(f"Started recording with sample rate {self.RATE}Hz")
            self.stream.start_stream()

        except Exception as e:
            self.is_recording = False
            logger.error(f"Failed to start recording: {str(e)}")
            raise

    def stop_recording(self) -> bytes:
        """Stop recording and return the recorded audio.

        Returns:
            Recorded audio as bytes
        """
        if not self.is_recording or not self.stream:
            logger.warning("Not recording")
            return b''

        try:
            # Stop the stream
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

            # Send any remaining speech buffer if it meets minimum size
            min_bytes = int(0.1 * self.RATE * 2)  # 100ms * 16000Hz * 2 bytes
            if self.speech_buffer and len(self.speech_buffer) >= min_bytes:
                for callback in self.callbacks:
                    try:
                        callback(self.speech_buffer)
                    except Exception as e:
                        logger.error(f"Error in audio callback: {str(e)}")

            # Combine all chunks
            audio_data = b''.join(self.recorded_chunks)
            logger.info(f"Stopped recording. Captured {len(audio_data)} bytes")

            self.is_recording = False
            return audio_data

        except Exception as e:
            logger.error(f"Error stopping recording: {str(e)}")
            self.is_recording = False
            raise

    def save_recording(self, file_path: str) -> None:
        """Save the recorded audio to a WAV file.

        Args:
            file_path: Path to save the WAV file
        """
        if not self.recorded_chunks:
            logger.warning("No audio data to save")
            return

        # Ensure directory exists
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        # Save to WAV file
        audio_data = b''.join(self.recorded_chunks)
        try:
            # Note: The linter incorrectly thinks this is a Wave_read object,
            # but wave.open in 'wb' mode returns a Wave_write object which has
            # these methods. This is why the linter shows errors.
            wf = wave.open(file_path, 'wb')  # type: ignore
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.pyaudio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(audio_data)
            wf.close()
            logger.info(f"Saved audio to {file_path}")
        except Exception as e:
            logger.error(f"Error saving audio file: {str(e)}")
            raise

    def close(self) -> None:
        """Clean up resources."""
        if self.stream:
            if self.stream.is_active():
                self.stream.stop_stream()
            self.stream.close()
            self.stream = None

        self.pyaudio.terminate()
        logger.info("Audio capture closed")


def main():
    """Test audio capture functionality."""
    logging.basicConfig(level=logging.INFO)

    capture = AudioCapture()

    print("Recording for 5 seconds...")
    capture.start_recording()
    time.sleep(5)

    audio_data = capture.stop_recording()
    print(f"Recorded {len(audio_data)} bytes of audio")

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    capture.save_recording(str(output_dir / "test_recording.wav"))

    capture.close()
    print("Done!")


if __name__ == "__main__":
    main()
