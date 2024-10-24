import os
import shutil
import chromadb
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import MarkdownTextSplitter
from langchain.schema.document import Document
from embeddings.embeddings import get_embeddings
from query.chat_query import make_query

DATA_PATH = 'data/rules.md'
CHROMA_PATH = 'chroma/'


def create_chroma(embeddings: list[float], chunks: list[str]) -> chromadb.Collection:
    clear_database()
    chroma_db = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = chroma_db.get_or_create_collection(name='embeddings_collection')
    ids = []
    for i in enumerate(zip(chunks, embeddings)):
        ids.append(f'chunk_{i}')
    collection.upsert(embeddings=embeddings, ids=ids, documents=chunks)
    print('Chroma database has been created.')

    return collection


def get_chroma() -> chromadb.Collection:
    chroma_db = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = chroma_db.get_or_create_collection(name='embeddings_collection')
    return collection


def clear_database():
    if os.path.exists('chroma'):
        shutil.rmtree('chroma')


def create_chunks(documents: list[Document]) -> list[str]:
    text_splitter = MarkdownTextSplitter(chunk_size=500, chunk_overlap=400, length_function=len)
    chunks = []
    for document in documents:
        chunks.extend(text_splitter.split_text(document.page_content))
    print(f'{len(chunks)} chunks created')
    return chunks


def load_documents() -> list[Document]:
    loader = DirectoryLoader(path='data', glob='*.md')
    documents = loader.load()
    return documents


def create_embeddings(chunks: list[str]) -> list[float]:
    return get_embeddings(chunks=chunks)


def generate_data() -> chromadb.Collection:
    documents = load_documents()
    chunks = create_chunks(documents)
    embeddings = create_embeddings(chunks)
    db = create_chroma(embeddings=embeddings, chunks=chunks)
    return db


def get_related_chunks(query: str, collection: chromadb.Collection):
    query_embedding = get_embeddings([query])[0]
    results = collection.query(query_embeddings=[query_embedding], n_results=5)
    return results


def generate_response(query: str, context: list[str]):
    input_text = f"Query: {query}\nContext: {' '.join(context['documents'][0])}"
    return input_text


def rag_query(query: str, collection: chromadb.Collection) -> None:
    context = get_related_chunks(query, collection)
    response = generate_response(query, context)
    make_query(response)
    # return response
