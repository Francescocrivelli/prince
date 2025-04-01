import uvicorn
from twilio.twiml.voice_response import VoiceResponse, Connect, Say, Stream
from fastapi.websockets import WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, WebSocket, Request
import websockets
import base64
import json
import asyncio
from openai.helpers import LocalAudioPlayer
from agents import Agent, Runner, function_tool, VoicePipeline
from dotenv import load_dotenv
from backend.backend_app.config import Config
from backend.backend_app.voice_agent.text_to_speech import TextToSpeech
import simpleaudio as sa
import numpy as np
from agents.voice import SingleAgentVoiceWorkflow, AudioInput


# tool to process worker registration details
load_dotenv()

# get from the config file
openai_api_key = Config.OPENAI_API_KEY
elevenlabs_api_key = Config.ELEVENLABS_API_KEY
elevenlabs_voice_id = Config.ELEVENLABS_VOICE_ID


SYSTEM_MESSAGE = (
    "You are a helpful and bubbly AI assistant who loves to chat about "
    "anything the user is interested in and is prepared to offer them facts. "
    "You have a penchant for dad jokes, owl jokes, and rickrolling – subtly. "
    "Always stay positive, but work in a joke when appropriate.")
VOICE = 'alloy'
LOG_EVENT_TYPES = [
    'response.content.done', 'rate_limits.updated', 'response.done',
    'input_audio_buffer.committed', 'input_audio_buffer.speech_stopped',
    'input_audio_buffer.speech_started', 'session.created'
]
app = FastAPI()
if not openai_api_key:
    raise ValueError(
        'Missing the OpenAI API key. Please set it in the .env file.')


@app.api_route("/", methods=["GET", "POST"])
async def index_page():
    return "Hello World"


@app.api_route("/incoming-call", methods=["GET", "POST"])
async def handle_incoming_call(request: Request):
    """Handle incoming call and return TwiML response."""
    response = VoiceResponse()
    response.say(
        "Hey buddy, do you want to join this exclusive community? Let's connect with Bill Gates."
    )
    response.pause(length=1)
    host = request.url.hostname
    connect = Connect()
    connect.stream(url=f'wss://{host}/media-stream')
    response.append(connect)
    return HTMLResponse(content=str(response), media_type="application/xml")


@app.websocket("/media-stream")
async def handle_media_stream(websocket: WebSocket):
    """Handle WebSocket connections using Voice Pipeline."""
    print("Client connected")
    await websocket.accept()
    # Buffer to accumulate audio data
    audio_buffer = []
    stream_sid = None

    try:
        async for message in websocket.iter_text():
            data = json.loads(message)

            if data['event'] == 'start':
                stream_sid = data['start']['streamSid']
                print(f"Incoming stream has started {stream_sid}")

            elif data['event'] == 'media':
                # Decode audio data
                audio_data = base64.b64decode(data['media']['payload'])
                # Convert to numpy array for Voice Pipeline
                audio_np = np.frombuffer(audio_data, dtype=np.int16)

                # Create AudioInput for the pipeline
                audio_input = AudioInput(
                    buffer=audio_np,
                    sample_rate=8000,  # g711_ulaw rate
                    channels=1
                )

                # Run the pipeline
                result = await pipeline.run(audio_input)

                # Stream the response back to Twilio
                async for event in result.stream():
                    if event.type == "voice_stream_event_audio":
                        # Convert numpy array back to base64 for Twilio
                        audio_payload = base64.b64encode(
                            event.data.tobytes()
                        ).decode('utf-8')

                        audio_delta = {
                            "event": "media",
                            "streamSid": stream_sid,
                            "media": {
                                "payload": audio_payload
                            }
                        }
                        await websocket.send_json(audio_delta)

    except Exception as e:
        print(f"Error in websocket handler: {e}")


async def send_session_update(openai_ws):
    """Send session update to OpenAI WebSocket."""
    session_update = {
        "type": "session.update",
        "session": {
            "turn_detection": {
                "type": "server_vad"
            },
            "input_audio_format": "g711_ulaw",
            "output_audio_format": "g711_ulaw",
            "voice": VOICE,
            "instructions": SYSTEM_MESSAGE,
            "modalities": ["text", "audio"],
            "temperature": 0.8,
        }
    }
    print('Sending session update:', json.dumps(session_update))
    await openai_ws.send(json.dumps(session_update))


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

# Create the voice pipeline
pipeline = VoicePipeline(
    workflow=SingleAgentVoiceWorkflow(worker_registration_agent))

# # make tts object
# tts = TextToSpeech()


def play_audio_from_pcm(audio_bytes: bytes, sample_rate: int = 22050):
    # Convert byte stream to numpy int16 array
    audio_np = np.frombuffer(audio_bytes, dtype=np.int16)

    # Play raw PCM buffer
    play_obj = sa.play_buffer(
        audio_np, 1, 2, sample_rate)  # mono, 2 bytes/sample
    play_obj.wait_done()


async def main():
    pass
    # result = await Runner.run(worker_registration_agent,
    #                           "My name is Kaleb Cole and I live in San Francisco, CA. I speak English and Spanish. My phone number is 123-456-7890.")
    # print(result.final_output)
    # output_audio = await tts.synthesize(result.final_output)
    # play_audio_from_pcm(output_audio)

if __name__ == "__main__":
    # asyncio.run(main())
    uvicorn.run(app, host="0.0.0.0", port=5000)
