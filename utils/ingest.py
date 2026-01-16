from utils.vector_store import get_vector_store
from langchain_core.documents import Document
import re


# -----------------------------
# SOURCE NORMALIZATION
# -----------------------------

def normalize_source(source: str) -> str:
    """
    Normalize source identifiers so the same document
    (PDF / HTML) is ingested only once.
    """

    # arXiv PDF or abs → canonical arxiv ID
    arxiv_match = re.search(r"arxiv\.org/(pdf|abs)/([\d\.]+)", source)
    if arxiv_match:
        return f"arxiv:{arxiv_match.group(2)}"

    return source


# -----------------------------
# INGESTION
# -----------------------------

def ingest_chunks(chunks, source_url):
    vectordb = get_vector_store()

    normalized_source = normalize_source(source_url)

    documents = [
        Document(
            page_content=chunk,
            metadata={
                "source": normalized_source,   # used for deduplication
                "raw_source": source_url       # original URL/path
            }
        )
        for chunk in chunks
    ]

    vectordb.add_documents(documents)
    vectordb.persist()

    print(f"Ingested {len(documents)} chunks into ChromaDB.")


# -----------------------------
# DUPLICATE CHECK
# -----------------------------

def is_source_ingested(source_url):
    vectordb = get_vector_store()

    normalized_source = normalize_source(source_url)

    results = vectordb.get(
        where={"source": normalized_source},
        limit=1
    )

    return len(results["ids"]) > 0
