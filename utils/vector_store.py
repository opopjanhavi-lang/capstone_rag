from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

CHROMA_DIR = "vectorstore/chroma_db"

def get_vector_store():
    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embedding
    )

    return vectordb
