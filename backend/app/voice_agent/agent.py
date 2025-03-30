# from agents import Agent, Runner
# from dotenv import load_dotenv
# import os


# agent = Agent(name="Assistant", instructions="You are a helpful assistant")

# result = Runner.run_sync(agent, "say hi to kaleb")
# print(result.final_output)


from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
from backend.app.config import Config


# tool to process worker registration details
load_dotenv()

# get from the config file
openai_api_key = Config.OPENAI_API_KEY
elevenlabs_api_key = Config.ELEVENLABS_API_KEY
elevenlabs_voice_id = Config.ELEVENLABS_VOICE_ID


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


def main():
    result = Runner.run_sync(worker_registration_agent,
                             "My name is Kaleb Cole and I live in San Francisco, CA. I speak English and Spanish. My phone number is 123-456-7890.")
    print(result.final_output)


if __name__ == "__main__":
    main()
