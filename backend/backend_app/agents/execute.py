# backend_app/agents/execute.py

import json
from backend_app.core.database import update_full_name

function_registry = {
    "update_user_name": lambda args: update_full_name(
        args["phone_number"], args["full_name"]
    ),
    # Add more functions here in the future
}

def execute_function(function_name: str, arguments: str):
    try:
        parsed_args = json.loads(arguments)
    except Exception as e:
        print(f"[⚠️] Failed to parse arguments for {function_name}: {e}")
        return {"error": str(e)}

    func = function_registry.get(function_name)
    if not func:
        print(f"[⚠️] Unknown function: {function_name}")
        return {"error": "Function not registered"}

    try:
        return func(parsed_args)
    except Exception as e:
        print(f"[❌] Function {function_name} execution error: {e}")
        return {"error": str(e)}