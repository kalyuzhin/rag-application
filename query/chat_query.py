import os

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ENDPOINT = "https://models.inference.ai.azure.com"
MODEL_NAME_LLAMA = "meta-llama-3.1-405b-instruct"
MODEL_NAME_OPENAI = "gpt-4o"


def make_query(query: str):
    client = ChatCompletionsClient(
        endpoint=ENDPOINT,
        credential=AzureKeyCredential(GITHUB_TOKEN),
    )
    response = client.complete(
        # stream=True,
        messages=[
            SystemMessage(content=""),
            UserMessage(content=query),
        ],
        temperature=1.0,
        top_p=1.0,
        max_tokens=4096,
        model=MODEL_NAME_OPENAI,
    )
    # for update in response:
    #     if update.choices:
    #         print(update.choices[0].delta.content or "", end="")
    return response.choices[0].message.content
