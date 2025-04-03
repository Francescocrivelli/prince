# backend_app/routes/voice.py
from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from backend_app.core.database import (
    get_student_by_phone,
    create_student_with_phone,
    update_conversation_history,
    update_full_name,
)
from backend_app.agents.functions import function_definitions
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

    # STEP 1: Get/create user
    profile = get_student_by_phone(phone_number)
    if not profile or not profile.get("documents"):
        create_student_with_phone(phone_number)
    profile = get_student_by_phone(phone_number)  # Refresh profile from DB

    # STEP 2: Get memory
    updated_profile = get_student_by_phone(phone_number)
    history_text = (updated_profile.get("documents", [""])[0])[:12000]  # Truncate long history
    metadata = updated_profile.get("metadatas", [{}])[0]
    full_name = metadata.get("full_name")

    # STEP 3: Generate first message if no input
    if not user_input:
        if full_name:
            gpt_reply = f"Hey {full_name}, how’s everything going?"
        else:
            gpt_reply = "Hi! Before we get started, may I know your name?"
    else:
        # STEP 4: Call GPT to extract info + maybe run function
        extraction_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Extract only important user information (e.g. Full name, goals, facts, preferences, identity) "
                        "from this input. Format as a bullet point list. Omit filler or small talk. "
                        "If the user mentions their name, use the update_user_name function to update the user's name."
                    )
                },
                {"role": "user", "content": user_input}
            ],
            functions=function_definitions,
            function_call="auto"
        )

        choice = extraction_response.choices[0]

        # STEP 4.5: Handle function call
        if choice.finish_reason == "function_call":
            func_name = choice.message["function_call"]["name"]
            raw_args = choice.message["function_call"]["arguments"]
            try:
                args = json.loads(raw_args)
            except Exception as e:
                print(f"[❌] Failed to parse tool args: {e}")
                args = {}

            if func_name == "update_user_name":
                full_name = args.get("full_name", "")
                if full_name:
                    update_full_name(phone_number, full_name)
                else:
                    print("[❌] Full name missing in function call args.")

        # STEP 5: Save only user's input info
        extracted_info = choice.message.get("content", "")
        if extracted_info:
            update_conversation_history(phone_number, extracted_info)

        # STEP 6: Generate reply to user
        chat_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You're a friendly buddy learning about the user's life, uniqueness, past work experience, goals, and preferences, what he is building, and what he is looking for. You remember the user's past responses and use them "
                        "to carry a meaningful, helpful conversation. Ask thoughtful follow-up questions"
                    )
                },
                {"role": "system", "content": f"User memory:\n{history_text}"},
                {"role": "user", "content": user_input}
            ]
        )
        gpt_reply = chat_response['choices'][0]['message']['content']

    # STEP 7: Twilio XML response
    twiml = f"""
    <Response>
        <Say>{gpt_reply}</Say>
        <Gather input="speech" action="/twilio/voice" method="POST" timeout="3" />
    </Response>
    """
    return Response(content=twiml.strip(), media_type="application/xml")