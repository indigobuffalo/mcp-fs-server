import random
import string


def generate_random_string(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


# LLM_MODEL = "gpt-4.1-2025-04-14"
LLM_MODEL = "gpt-3.5-turbo-0125"


AGENT_NAME = "File System Agent"


AGENT_INSTRUCTIONS = """
You are a helpful, non-interactive assistant.
You are not allowed to ask questions. Make your best guess based on the provided context.
Answer the user questions using the tools provided.
"""


DEFAULT_PROMPT = f"""
Write me a haiku about file systems under /tmp/{generate_random_string()}/{generate_random_string()}.
If that directory does not exist, create it.
After writing the file, append to the file with a signature of your name.
Finally, read me the poem and provide the full path to the file you created.
If you encounter any issues, provide a detailed error message.
"""
