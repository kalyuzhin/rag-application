import os
import random
from dotenv import load_dotenv
from azure.ai.inference import EmbeddingsClient
from azure.core.credentials import AzureKeyCredential

ENDPOINT = "https://models.inference.ai.azure.com"
MODEL_NAME = "text-embedding-3-large"
load_dotenv()
TOKEN = os.environ["GITHUB_TOKEN"]


def get_embeddings(chunks: list[str]) -> list:
    embeddings = []
    client = EmbeddingsClient(
        endpoint=ENDPOINT,
        credential=AzureKeyCredential(TOKEN)
    )
    if len(chunks) > 60:
        chunks_halves_number = len(chunks) // 60
        chunks_halves = []
        j = 60
        for i in range(chunks_halves_number):
            chunks_halves.append(chunks[j * i:j * (i + 1)])
        if len(chunks) % 60 != 0:
            chunks_halves.append(chunks[chunks_halves_number * 60:])
        for chunk in chunks_halves:
            response = client.embed(
                input=chunk,
                model=MODEL_NAME)
            embeddings.extend([embedding['embedding'] for embedding in response.data])
        return embeddings
    else:
        response = client.embed(
            input=chunks,
            model=MODEL_NAME)
        return [embedding['embedding'] for embedding in response.data]
