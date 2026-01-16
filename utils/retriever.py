from utils.vector_store import get_vector_store

def retrieve_chunks(query: str, k: int = 4):
    vectordb = get_vector_store()

    results = vectordb.similarity_search(
        query=query,
        k=k
    )

    return results
