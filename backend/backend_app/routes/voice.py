# backend_app/routes/voice.py
from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from backend_app.core.database import (
    get_student_by_phone,
    create_student_with_phone,
    update_conversation_history
)
import openai
import os

router = APIRouter()

# ✅ Twilio webhook redirector (entry point)
@router.post("/twilio/voice")
async def twilio_voice_handler(request: Request):
    return await voice_webhook(request)


# ✅ Developer debug endpoint to inspect stored memory
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


# ✅ Main voice interaction endpoint
@router.post("/voice/incoming-call")
async def voice_webhook(request: Request):
    form = await request.form()
    phone_number = form.get("From")
    user_input = form.get("SpeechResult") or ""

    # Initialize OpenAI
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # STEP 1: Get or create user in Chroma
    profile = get_student_by_phone(phone_number)
    if not profile or not profile.get("documents"):
        create_student_with_phone(phone_number)

    # STEP 2: Extract key info from user's message (summarize to store)
    extraction_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract only important user information (e.g. name, goals, facts, preferences, identity) "
                    "from this input. Format as a bullet point list. Omit filler or small talk."
                )
            },
            {"role": "user", "content": user_input}
        ]
    )
    extracted_info = extraction_response.choices[0].message["content"]

    # STEP 3: Save extracted info to long-term memory
    update_conversation_history(phone_number, extracted_info)

    # STEP 4: Retrieve memory (entire user history)
    updated_profile = get_student_by_phone(phone_number)
    history_text = updated_profile.get("documents", [""])[0]

    # STEP 5: Generate context-aware GPT reply
    chat_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You're a friendly AI assistant. You remember the user's past responses and use them "
                    "to carry a meaningful, helpful conversation. Ask thoughtful follow-up questions or offer help."
                )
            },
            {"role": "system", "content": f"User memory:\n{history_text}"},
            {"role": "user", "content": user_input}
        ]
    )
    gpt_reply = chat_response['choices'][0]['message']['content']

    # STEP 6: Send reply back to caller
    twiml = f"""
    <Response>
        <Say>{gpt_reply}</Say>
        <Gather input="speech" action="/twilio/voice" method="POST" timeout="3"/>
    </Response>
    """
    return Response(content=twiml.strip(), media_type="application/xml")