# from agents import Agent, Runner
# from dotenv import load_dotenv
# import os



# agent = Agent(name="Assistant", instructions="You are a helpful assistant")

# result = Runner.run_sync(agent, "say hi to kaleb")
# print(result.final_output)


from agents import Agent, Runner, function_tool
import os
from dotenv import load_dotenv




# tool to process worker registration details
load_dotenv()

# Get OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

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

    return f"Worker registration successful for {name}."


worker_registration_agent = Agent(
    name="Worker Registration Agent",
    instructions=(
        "You are an agent that handles blue-collar worker registrations. "
        "Capture and validate worker information (name, location, skills, language) from voice or SMS inputs. "
        "Use the process_registration tool to register workers in the system."
    ),
    tools=[process_worker_registration]
)