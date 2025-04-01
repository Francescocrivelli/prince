
"""
MAIN ISSUES:

1. The audio buffer that is sent is too small.

We are sending audio data in chunks. There seems to be timing issues when sending the audio data. Idk what the root cause is.

Try to go from the OpenAI API docs and build a new implementation from there instead of vibe code from chatgpt.

"""


import json

import logging
import threading
import time
import websockets
import asyncio
from typing import Optional, Callable, List
from backend.backend_app.config import Config
import urllib.parse
import base64
import traceback
import sys

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)
logger = logging.getLogger(__name__)

# URL for the OpenAI Realtime API
WS_URL = "wss://api.openai.com/v1/realtime?intent=transcription"

# Audio format constants
SAMPLE_RATE = 16000
CHANNELS = 1
FORMAT = "pcm16"  # 16-bit PCM audio


class RealTimeSpeechToText:
    def __init__(self, api_key: str):
        """
        Initialize the RealTimeSpeechToText class.
        Args:
            api_key (str): The API key for the OpenAI Realtime API.
        """
        self.api_key = api_key
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.session_id = None
        self.connected = False
        self.transcript_callbacks: List[Callable[[str, bool], None]] = []
        self.full_transcript = ""
        self.audio_queue = asyncio.Queue()
        self.is_recording = False
        self.stop_recording = threading.Event()
        self._queue_processor_task = None
        self._listen_task = None

        # Audio format configuration
        self.SAMPLE_RATE = SAMPLE_RATE
        self.CHANNELS = CHANNELS
        self.FORMAT = FORMAT

        logger.info(
            f"Initialized RealTimeSpeechToText with sample_rate={SAMPLE_RATE}, channels={CHANNELS}, format={FORMAT}")

    async def connect(self):
        """Establish WebSocket connection with OpenAI API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "OpenAI-Beta": "realtime=v1"
        }

        # Configure WebSocket parameters - keep it minimal
        ws_params = {
            "intent": "transcription"
        }

        # Format URL with parameters
        url = f"wss://api.openai.com/v1/realtime?{urllib.parse.urlencode(ws_params)}"

        try:
            logger.info(f"Attempting to connect to WebSocket at {url}")
            self.websocket = await websockets.connect(url, additional_headers=headers)
            self.connected = True
            logger.info("WebSocket connection established successfully")

            # Start listening for messages
            self._listen_task = asyncio.create_task(self._listen())
            logger.debug("Started WebSocket listener task")

            # Start the audio queue processor
            self._queue_processor_task = asyncio.create_task(
                self._process_audio_queue())
            logger.debug("Started audio queue processor task")

            # Wait for session creation
            timeout = 10
            start_time = time.time()
            while not self.session_id and time.time() - start_time < timeout:
                await asyncio.sleep(0.1)
                logger.debug(
                    f"Waiting for session ID... ({time.time() - start_time:.1f}s elapsed)")

            if not self.session_id:
                raise TimeoutError(
                    "Session ID was not received within timeout period")

            logger.info(f"Session established with ID: {self.session_id}")

        except websockets.exceptions.InvalidStatusCode as e:
            logger.error(
                f"Failed to connect: Invalid status code {e.status_code}")
            self.connected = False
            raise
        except websockets.ConnectionClosedOK:
            logger.info("WebSocket closed cleanly (1000 OK)")
            self.connected = False
            self.session_id = None
        except websockets.ConnectionClosedError as e:
            logger.error(f"WebSocket closed unexpectedly: {e}")
            self.connected = False
            self.session_id = None
        except Exception as e:
            logger.error(
                f"Failed to connect: {str(e)}\n{traceback.format_exc()}")
            self.connected = False
            raise

    async def _process_audio_queue(self):
        """Process audio chunks from the queue."""
        logger.info("Starting audio queue processor")
        chunks_processed = 0
        try:
            while self.connected:
                try:
                    # Get the next audio chunk from the queue (with timeout)
                    audio_data = await asyncio.wait_for(self.audio_queue.get(), timeout=1.0)
                    chunks_processed += 1
                    logger.debug(
                        f"Processing audio chunk #{chunks_processed} ({len(audio_data)} bytes)")

                    # Process the audio chunk
                    await self._send_audio_chunk(audio_data)
                    self.audio_queue.task_done()

                except asyncio.TimeoutError:
                    # No audio data in the queue, continue waiting
                    continue
                except Exception as e:
                    logger.error(
                        f"Error processing audio chunk: {str(e)}\n{traceback.format_exc()}")
                    self.audio_queue.task_done()  # Ensure we mark the task as done even if it fails

        except Exception as e:
            logger.error(
                f"Fatal error in audio queue processor: {str(e)}\n{traceback.format_exc()}")
        finally:
            logger.info(
                f"Audio queue processor stopped. Processed {chunks_processed} chunks total.")

    async def _send_audio_chunk(self, audio_data: bytes):
        """Send a single chunk of audio data to the API."""
        if not self.connected or not self.session_id:
            logger.error(
                f"Cannot send audio: connected={self.connected}, session_id={self.session_id}")
            return

        try:
            # Ensure we have at least 100ms of audio
            min_size = int(self.SAMPLE_RATE * 0.1 * 2)
            if len(audio_data) < min_size:
                logger.warning(
                    f"Audio data too small: {len(audio_data)} bytes. Minimum required: {min_size} bytes")
                # Pad with silence if too small
                padding_needed = min_size - len(audio_data)
                audio_data += b'\x00\x00' * (padding_needed // 2)
                logger.info(f"Padded audio data to {len(audio_data)} bytes")

            # Step 1: Clear any existing audio buffer
            clear_message = {"type": "input_audio_buffer.clear"}
            await self.websocket.send(json.dumps(clear_message))
            logger.debug("Sent clear buffer request")

            # Convert audio to base64 while waiting for clear confirmation
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')

            # Wait a very short time for clear to take effect
            await asyncio.sleep(0.05)

            # Append the audio data
            payload_append = {
                "type": "input_audio_buffer.append",
                "audio": audio_base64
            }
            await self.websocket.send(json.dumps(payload_append))
            logger.debug(f"Sent audio data ({len(audio_data)} bytes)")

            # Immediately commit - don't wait between append and commit
            payload_commit = {"type": "input_audio_buffer.commit"}
            await self.websocket.send(json.dumps(payload_commit))
            logger.debug("Committed audio buffer")

            logger.info(
                f"Successfully processed {len(audio_data)} bytes of audio")

        except websockets.exceptions.ConnectionClosed as e:
            logger.error(
                f"WebSocket connection closed while sending audio: {str(e)}")
            self.connected = False
            raise
        except Exception as e:
            logger.error(
                f"Error sending audio chunk: {str(e)}\n{traceback.format_exc()}")
            raise

    async def send_audio(self, audio_data: bytes):
        """Add audio data to the processing queue."""
        try:
            await self.audio_queue.put(audio_data)
            logger.debug(
                f"Added {len(audio_data)} bytes to audio queue (queue size: {self.audio_queue.qsize()})")
        except Exception as e:
            logger.error(
                f"Failed to add audio to queue: {str(e)}\n{traceback.format_exc()}")
            raise

    async def _listen(self):
        """Listen for messages from the WebSocket connection."""
        messages_processed = 0
        try:
            while self.connected:
                try:
                    message = await self.websocket.recv()
                    messages_processed += 1
                    # Log first 100 chars
                    logger.debug(
                        f"Received message #{messages_processed}: {message[:100]}...")

                    data = json.loads(message)
                    msg_type = data.get("type", "")

                    if msg_type == "transcription_session.created":
                        session = data.get("session", {})
                        self.session_id = session.get("id", "")
                        logger.info(
                            f"Session created with ID: {self.session_id}")

                    elif msg_type == "transcript":
                        transcript = data.get("transcript", {})
                        text = transcript.get("text", "")
                        is_final = transcript.get("is_final", False)
                        logger.info(
                            f"Transcript received: {text} (final: {is_final})")

                        if text:
                            if is_final:
                                self.full_transcript += text + " "
                            for callback in self.transcript_callbacks:
                                try:
                                    callback(text, is_final)
                                except Exception as e:
                                    logger.error(
                                        f"Error in transcript callback: {str(e)}\n{traceback.format_exc()}")

                    elif msg_type == "error":
                        error = data.get("error", {})
                        error_message = error.get("message", "")
                        logger.error(f"API Error: {error_message}")

                        # Handle specific buffer too small error by logging a more helpful message
                        if "buffer too small" in error_message:
                            logger.warning(
                                "Buffer size error detected. This usually indicates a timing issue between " +
                                "audio buffer operations. If this persists, check the _send_audio_chunk method timing."
                            )

                except json.JSONDecodeError as e:
                    logger.error(
                        f"Failed to parse message as JSON: {e}\nMessage: {message[:100]}...")
                except Exception as e:
                    logger.error(
                        f"Error processing message: {str(e)}\n{traceback.format_exc()}")

        except websockets.ConnectionClosed:
            logger.error(
                "WebSocket connection closed during listening")
            self.connected = False
            self.session_id = None
        except Exception as e:
            logger.error(
                f"Fatal error in _listen: {str(e)}\n{traceback.format_exc()}")
            self.connected = False
            self.session_id = None
        finally:
            logger.info(
                f"Message listener stopped. Processed {messages_processed} messages.")

    async def stop(self):
        """Stop the WebSocket connection and cleanup."""
        logger.info("Starting cleanup process...")

        # First wait for the audio queue to be fully processed
        if self.audio_queue.qsize() > 0:
            logger.info(
                f"Waiting for {self.audio_queue.qsize()} audio chunks to be processed...")
            try:
                await asyncio.wait_for(self.audio_queue.join(), timeout=10.0)
                logger.info("I LOVE FRANCESCOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO \n\n\n\n\\n\n\n\n\n\n\n\n\n\n\n Audio queue processing complete")
            except asyncio.TimeoutError:
                logger.error("Timeout waiting for audio queue to process")

        if self.websocket:
            try:
                if self.session_id:
                    # Send final messages
                    clear_message = {"type": "input_audio_buffer.clear"}
                    cancel_message = {"type": "response.cancel"}
                    await self.websocket.send(json.dumps(clear_message))
                    await self.websocket.send(json.dumps(cancel_message))
                    logger.debug("Sent final cleanup messages")

                await self.websocket.close()
                logger.info("WebSocket connection closed successfully")

            except Exception as e:
                logger.error(
                    f"Error during cleanup: {str(e)}\n{traceback.format_exc()}")
            finally:
                self.connected = False
                self.session_id = None
                return self.full_transcript

    def add_transcript_callback(self, callback: Callable[[str, bool], None]) -> None:
        """Add a callback to be called when new transcript is available."""
        self.transcript_callbacks.append(callback)
        logger.debug(
            f"Added transcript callback. Total callbacks: {len(self.transcript_callbacks)}")

    def get_transcript(self) -> str:
        """Get the current full transcript."""
        return self.full_transcript


# Simple test of the connection and sending dummy audio data
if __name__ == "__main__":
    async def main():
        config = Config()
        API_KEY = config.OPENAI_API_KEY
        stt = RealTimeSpeechToText(api_key=API_KEY)
        try:
            await stt.connect()
            # For testing, send 1 second of silence (16000 samples of 16-bit PCM)
            dummy_audio = b'\x00\x00' * 16000  # 2 bytes per sample
            await stt.send_audio(dummy_audio)
            # Wait to receive any transcript messages
            await asyncio.sleep(5)
        finally:
            await stt.stop()

    asyncio.run(main())
