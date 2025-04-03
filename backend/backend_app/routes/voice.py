# backend_app/routes/voice.py

from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from backend_app.core.database import (
    get_student_by_phone,
    create_student_with_phone,
    update_conversation_history,
)
from backend_app.agents.functions import function_definitions
from backend_app.agents.execute import execute_function
import openai
import os
import json

router = APIRouter()

@router.post("/twilio/voice")
async def twilio_voice_handler(request: Request):
    return await voice_webhook(request)


@router.get("/debug/memory/{phone_number}")
def view_conversation_history(phone_number: str):
    record = get_student_by_phone(phone_number)
    if not record:
        return JSONResponse(content={"error": "User not found"}, status_code=404)

    return {
        "id": record.get("ids", ["unknown"])[0],
        "document": record.get("documents", [""])[0],
        "metadata": record.get("metadatas", [{}])[0],
    }


@router.post("/voice/incoming-call")
async def voice_webhook(request: Request):
    form = await request.form()
    phone_number = form.get("From")
    user_input = form.get("SpeechResult") or ""

    openai.api_key = os.getenv("OPENAI_API_KEY")

    # STEP 1: Get or create user in Chroma
    profile = get_student_by_phone(phone_number)
    if not profile or not profile.get("documents"):
        create_student_with_phone(phone_number)

    # STEP 2: Call GPT to extract info + maybe run function
    extraction_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract important user information (e.g. full name, preferences, goals, identity). "
                    "Format it as a bullet point list. If the user mentions their name, call the `update_user_name` function. "
                    "Do not return small talk or filler content."
                )
            },
            {"role": "user", "content": user_input}
        ],
        functions=function_definitions,
        function_call="auto"
    )

    choice = extraction_response.choices[0]

    # STEP 2.5: Execute GPT-suggested tool (if any)
    if choice.finish_reason == "function_call":
        func_name = choice.message["function_call"]["name"]
        args = choice.message["function_call"]["arguments"]
        execute_function(func_name, args)

    # STEP 3: Save extracted info as memory
    extracted_info = choice.message.get("content", "")
    update_conversation_history(phone_number, extracted_info)

    # STEP 4: Retrieve full memory
    updated_profile = get_student_by_phone(phone_number)
    history_text = updated_profile.get("documents", [""])[0]

    # STEP 5: Generate assistant reply
    chat_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You're a helpful, friendly AI assistant that remembers what the user said before. "
                    "Use memory to personalize your response and ask follow-ups."
                    "If the user mentions their name, use the update_user_name function to update the user's name."
                )
            },
            {"role": "system", "content": f"User memory:\n{history_text}"},
            {"role": "user", "content": user_input}
        ]
    )
    gpt_reply = chat_response.choices[0].message["content"]

    # STEP 6: Twilio voice response
    twiml = f"""
    <Response>
        <Say>{gpt_reply}</Say>
        <Gather input="speech" action="/twilio/voice" method="POST" timeout="3"/>
    </Response>
    """
    return Response(content=twiml.strip(), media_type="application/xml")