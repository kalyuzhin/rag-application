import os
import time
import random
from dotenv import load_dotenv
from azure.ai.inference import EmbeddingsClient
from azure.core.credentials import AzureKeyCredential
from langchain_community.embeddings.ollama import OllamaEmbeddings

ENDPOINT = "https://models.inference.ai.azure.com"
MODEL_NAME = "text-embedding-3-large"
load_dotenv()
TOKEN = os.environ["GITHUB_TOKEN"]
MAX_AMOUNT = 40


def get_embeddings(chunks: list[str]) -> list:
    embeddings = []
    client = EmbeddingsClient(
        endpoint=ENDPOINT,
        credential=AzureKeyCredential(TOKEN)
    )
    if len(chunks) > MAX_AMOUNT:
        chunks_halves_number = len(chunks) // MAX_AMOUNT
        chunks_halves = []
        j = MAX_AMOUNT
        for i in range(chunks_halves_number):
            chunks_halves.append(chunks[j * i:j * (i + 1)])
        if len(chunks) % MAX_AMOUNT != 0:
            chunks_halves.append(chunks[chunks_halves_number * MAX_AMOUNT:])
        i = 1
        for chunk in chunks_halves:
            time.sleep(random.random() * random.randint(1, 10))
            response = client.embed(
                input=chunk,
                model=MODEL_NAME)
            embeddings.extend([embedding['embedding'] for embedding in response.data])
            print(i)
            i += 1
        return embeddings
    else:
        response = client.embed(
            input=chunks,
            model=MODEL_NAME)
        return [embedding['embedding'] for embedding in response.data]


def get_embedding_ollama_function():
    embedding_ollama = OllamaEmbeddings(model='llama3.2:1b')
    return embedding_ollama
