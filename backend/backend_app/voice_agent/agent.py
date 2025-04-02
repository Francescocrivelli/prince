from twilio.twiml.voice_response import VoiceResponse, Connect
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
import base64
import json
import logging
import uvicorn
from agents import Agent, function_tool
from dotenv import load_dotenv
import numpy as np
from agents.voice import SingleAgentVoiceWorkflow, AudioInput, VoicePipeline
from backend.backend_app.config import Config
# from backend.backend_app.voice_agent.text_to_speech import TextToSpeech

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# tool to process worker registration details
load_dotenv()

# =============================== CONSTANTS ===============================
# get from the config file
openai_api_key = Config.OPENAI_API_KEY
elevenlabs_api_key = Config.ELEVENLABS_API_KEY
elevenlabs_voice_id = Config.ELEVENLABS_VOICE_ID
VOICE = 'alloy'
LOG_EVENT_TYPES = [
    'response.content.done', 'rate_limits.updated', 'response.done',
    'input_audio_buffer.committed', 'input_audio_buffer.speech_stopped',
    'input_audio_buffer.speech_started', 'session.created'
]

# =============================== FASTAPI APP ===============================
app = FastAPI()
if not openai_api_key:
    logger.error("Missing OpenAI API key in environment variables")
    raise ValueError(
        'Missing the OpenAI API key. Please set it in the .env file.')

# =============================== UTILITY FUNCTIONS ===============================


async def send_mark(websocket: WebSocket, stream_sid: str):
    """Send a mark event to the websocket."""
    logger.debug(f"Sending mark event for stream {stream_sid}")
    await websocket.send_json({
        "event": "mark",
        "streamSid": stream_sid
    })
    logger.debug("Mark event sent successfully")


async def stream_pipeline_results(websocket: WebSocket, result, stream_sid: str, mark_queue: list, latest_media_timestamp=None, response_start_timestamp=None):
    """Stream the results of the pipeline to the websocket."""
    logger.debug(
        f"Starting to stream pipeline results for stream {stream_sid}")
    try:
        async for event in result.stream():
            logger.debug(f"Received event type: {event.type}")
            if event.type == "voice_stream_event_audio":
                logger.debug("Processing audio event")
                audio_payload = base64.b64encode(
                    event.data.tobytes()
                ).decode('utf-8')
                logger.debug(f"Audio payload size: {len(audio_payload)} bytes")

                await websocket.send_json({
                    "event": "media",
                    "streamSid": stream_sid,
                    "media": {"payload": audio_payload}
                })
                logger.debug("Audio event sent to Twilio")

                if response_start_timestamp is None:
                    response_start_timestamp = latest_media_timestamp
                    logger.debug(
                        f"Set response start timestamp to: {latest_media_timestamp}")

                await send_mark(websocket, stream_sid)
                mark_queue.append('responsePart')
                logger.debug(f"Mark queue length: {len(mark_queue)}")
            elif event.type == "voice_stream_event_lifecycle":
                logger.info(f"Lifecycle event: {event.event}")
            elif event.type == "voice_stream_event_error":
                logger.error(f"Error event: {event.error}")
    except Exception as e:
        logger.error(
            f"Error in stream_pipeline_results: {str(e)}", exc_info=True)
        raise

# =============================== ROUTES ===============================


@app.api_route("/", methods=["GET", "POST"])
async def index_page():
    logger.debug("Root endpoint accessed")
    return "Hello World"


@app.api_route("/incoming-call", methods=["GET", "POST"])
async def handle_incoming_call(request: Request):
    """Handle incoming call and return TwiML response."""
    logger.info("Received incoming call request")
    response = VoiceResponse()
    # TODO: Replace this with the elevenlabs tts
    response.say(
        "Hey buddy, do you want to join this exclusive community? Let's connect with Bill Gates."
    )
    response.pause(length=1)
    host = request.url.hostname
    # host = "dory-actual-hedgehog.ngrok-free.app"
    logger.debug(f"Using host: {host}")
    connect = Connect()
    connect.stream(url=f'wss://{host}/media-stream')
    response.append(connect)
    logger.info(
        "TwiML response prepared and sending back to Twilio for verification")
    return HTMLResponse(content=str(response), media_type="application/xml")


@app.websocket("/media-stream")
async def handle_media_stream(websocket: WebSocket):
    """Handle WebSocket connections using Voice Pipeline."""
    logger.info("New WebSocket connection request")
    await websocket.accept()
    logger.info("WebSocket connection accepted")
    # Initialize variables
    stream_sid = None
    latest_media_timestamp = 0
    last_ai_item = None
    mark_queue = []
    response_start_timestamp = None
    try:
        async for message in websocket.iter_text():
            # Log first 100 chars
            logger.debug(f"Received WebSocket message: {message[:100]}...")
            data = json.loads(message)

            if data['event'] == 'start':
                logger.info("Received start event")
                stream_sid = data['start']['streamSid']
                logger.info(f"Call started with stream SID: {stream_sid}")

                empty_audio = AudioInput(
                    buffer=np.array([], dtype=np.int16),
                    frame_rate=8000,
                    sample_width=2,
                    channels=1
                )
                logger.debug("Created empty audio input for initial greeting")

                try:
                    # how to handle the empty audio input? how to send the metadata for this?
                    result = await pipeline.run(audio_input=empty_audio)
                    logger.info("Pipeline run completed for initial greeting")
                    await stream_pipeline_results(websocket, result, stream_sid, mark_queue, response_start_timestamp)
                except Exception as e:
                    logger.error(
                        f"Error in initial pipeline run: {str(e)}", exc_info=True)

            elif data['event'] == 'media':
                logger.debug("Received media event")
                latest_media_timestamp = data['media']['timestamp']
                logger.debug(f"Media timestamp: {latest_media_timestamp}")

                audio_data = base64.b64decode(data['media']['payload'])
                audio_np = np.frombuffer(audio_data, dtype=np.int16)
                logger.debug(f"Decoded audio data shape: {audio_np.shape}")

                if mark_queue and response_start_timestamp is not None:
                    logger.info("User interruption detected")
                    if stream_sid:
                        await websocket.send_json({
                            "event": "clear",
                            "streamSid": stream_sid
                        })
                        logger.debug("Sent clear event to Twilio")

                    mark_queue = []
                    last_ai_item = None
                    response_start_timestamp = None
                    logger.debug("Reset state after interruption")

                audio_input = AudioInput(
                    buffer=audio_np,
                    frame_rate=8000,
                    sample_width=2,
                    channels=1
                )
                logger.debug("Created AudioInput for pipeline")

                if not response_start_timestamp:
                    response_start_timestamp = latest_media_timestamp
                    logger.debug(
                        f"Set response start timestamp to: {latest_media_timestamp}")

                try:
                    result = await pipeline.run(audio_input=audio_input)
                    logger.info("Pipeline run completed for media event")
                    await stream_pipeline_results(websocket, result, stream_sid, mark_queue, latest_media_timestamp, response_start_timestamp)
                except Exception as e:
                    logger.error(
                        f"Error in pipeline run: {str(e)}", exc_info=True)

            elif data['event'] == 'mark':
                logger.debug("Received mark event")
                if mark_queue:
                    mark_queue.pop(0)
                    logger.debug(
                        f"Mark queue length after pop: {len(mark_queue)}")

            elif data['event'] == 'conversation.item.done':
                logger.debug("Received conversation item done event")
                last_ai_item = data['conversation']['item']
                logger.debug(f"Updated last AI item: {last_ai_item}")

    except Exception as e:
        logger.error(f"Error in WebSocket handler: {str(e)}", exc_info=True)
    finally:
        logger.info("WebSocket connection closed")

# =============================== FUNCTION TOOLS ===============================


@function_tool
def process_worker_registration(name: str, phone: str, location: str, language: str):
    """Process the worker registration details and save them to the database."""
    logger.info(f"Processing worker registration for {name}")
    logger.debug(
        f"Registration details - Phone: {phone}, Location: {location}, Language: {language}")

    # save to database
    # TODO: Francesco needs to save to chroma db
    logger.debug("Database save pending implementation")

    return f"details are the following: {name}, {phone}, {location}, {language}"


# =============================== AGENTS and VOICE PIPELINE ===============================
logger.info("Initializing worker registration agent")
worker_registration_agent = Agent(
    name="Worker Registration Agent",
    instructions=(
        "You are an agent that handles blue-collar worker registrations. "
        "Capture and validate worker information (name, location, skills, language) from voice or SMS inputs. "
        "Use the process_registration tool to register workers in the system."
    ),
    tools=[process_worker_registration]
)

logger.info("Creating voice pipeline")
pipeline = VoicePipeline(
    workflow=SingleAgentVoiceWorkflow(worker_registration_agent))
logger.info("Voice pipeline created successfully")

# =============================== MAIN ===============================


async def main():
    pass
    # result = await Runner.run(worker_registration_agent,
    #                           "My name is Kaleb Cole and I live in San Francisco, CA. I speak English and Spanish. My phone number is 123-456-7890.")
    # print(result.final_output)
    # output_audio = await tts.synthesize(result.final_output)
    # play_audio_from_pcm(output_audio)

if __name__ == "__main__":
    # asyncio.run(main())
    logger.info("Starting FastAPI server")
    uvicorn.run(app, host="0.0.0.0", port=5000)
