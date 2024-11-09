import os
import shutil
import langchain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_community.document_loaders import DirectoryLoader
from langchain_chroma.vectorstores import Chroma
from embeddings.embeddings import get_embedding_ollama_function


def create_chroma(chunks: list[Document]):
    clear_database()
    db = Chroma.from_documents(
        documents=chunks, persist_directory='chroma', embedding=get_embedding_ollama_function()
    )
    db.persist()
    print(f'Database created.\n{len(chunks)} chunks created.')


def generate_data():
    documents = load_documents()
    chunks = split_documents(documents)
    create_chroma(chunks)


def load_documents() -> list[Document]:
    loader = DirectoryLoader(path='data', glob='*.md')
    documents = loader.load()
    return documents


def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)


def clear_database():
    if os.path.exists('chroma'):
        shutil.rmtree('chroma')
