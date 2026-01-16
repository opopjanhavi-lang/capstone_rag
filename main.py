from tools.web_crawler import crawl_url
from tools.pdf_scraper import scrape_pdf
from utils.pdf_url_handler import download_pdf_from_url

from utils.text_chunker import chunk_text
from utils.ingest import ingest_chunks, is_source_ingested
from utils.rag_chain import ask_rag


# -----------------------------
# PART 1: INGESTION
# -----------------------------

def ingest_source(source: str):
    """
    source can be:
    - Web URL
    - PDF URL
    - Local PDF path
    """

    if is_source_ingested(source):
        print("Source already ingested. Skipping.")
        return

    print("New source detected. Ingesting...")

    if source.startswith("http") and source.endswith(".pdf"):
        pdf_path = download_pdf_from_url(source)
        data = scrape_pdf(str(pdf_path))

    elif source.startswith("http"):
        data = crawl_url(source)

    elif source.endswith(".pdf"):
        data = scrape_pdf(source)

    else:
        raise ValueError("Unsupported source type")

    text = data["text"]
    chunks = chunk_text(text)
    ingest_chunks(chunks, source)

    print("Ingestion complete.")


# -----------------------------
# PART 2: CHAT
# -----------------------------

def chat_loop():
    print("\nRAG System with Groq (type 'exit' to quit)\n")

    while True:
        query = input("You: ")
        if query.lower() == "exit":
            break

        answer = ask_rag(query)
        print(f"\nAssistant: {answer}\n")


# -----------------------------
# ENTRY POINT
# -----------------------------

if __name__ == "__main__":

    SOURCE = "https://en.wikipedia.org/wiki/Retrieval-augmented_generation"
    ingest_source(SOURCE)
    chat_loop()



