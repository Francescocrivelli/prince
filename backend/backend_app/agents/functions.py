# backend_app/agents/functions.py
from typing import List, Dict

function_definitions: List[Dict] = [
    {
        "name": "update_user_name",
        "description": "Update the full name of the user based on what they said.",
        "parameters": {
            "type": "object",
            "properties": {
                "full_name": {
                    "type": "string",
                    "description": "The user's full name, e.g., 'Jane Smith'"
                },
                "phone_number": {
                    "type": "string",
                    "description": "The user's phone number, used as unique ID"
                }
            },
            "required": ["full_name", "phone_number"]
        }
    }
]