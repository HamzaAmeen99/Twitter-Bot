import os
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from Helpers.UrlManager import URLManager
from openai.types.chat import ChatCompletionUserMessageParam

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def summerize_api(text: str) -> str:
    if not OPENROUTER_API_KEY:
        raise ValueError("Missing OPENROUTER_API_KEY. Please set it in your .env file.")

    try:
        # messages = poml(
        #     PROMPT_FILE,             # path to your POML file
        #     context={"text": text},       # inject tweet/text here
        #     format="openai_chat"          # returns list of messages
        # )

        # return messages
        url = URLManager.get_url(category='api_urls', key='openrouter')

        client = OpenAI(
            base_url=url,
            api_key=OPENROUTER_API_KEY,
        )

        completion = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=[
                ChatCompletionUserMessageParam(role="user", content=f"Summarize this: {text}")
            ],
            max_tokens=50,
        )

        # Defensive access in case structure changes
        if not completion.choices:
            raise RuntimeError("No choices returned by API.")

        return completion.choices[0].message.content

    except OpenAIError as e:
        # Handles API-related errors (auth, rate limits, invalid request, etc.)
        print(f"[OpenAI API Error] {e}")
        return "Error: API request failed."

    except Exception as e:
        # Handles all other unexpected errors
        print(f"[Unexpected Error] {e}")
        return "Error: Something went wrong."
