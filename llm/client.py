from dotenv import load_dotenv
from openai import OpenAI
import os
import time

# Load environment variables from .env
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY not found. Make sure it exists in your .env file."
    )

# Create OpenAI client
client = OpenAI(api_key=api_key)


def standardize_llm_output(text: str) -> str:
    """
    Normalize LLM output for safe parsing.
    """
    return text.strip().lower()


def ask_llm(prompt: str, max_retries: int = 2) -> str:
    """
    Sends a prompt to the LLM and returns text response.
    Includes retry logic for transient API failures.
    """

    last_error = None

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0,  # deterministic output
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            last_error = e

            # small backoff before retry
            time.sleep(1)

    raise last_error