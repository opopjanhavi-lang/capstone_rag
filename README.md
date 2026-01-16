
# 📄 RAG System for Web & PDF (Research Papers)

This project implements a **Retrieval-Augmented Generation (RAG)** pipeline that can ingest:
- 🌐 Web pages
- 📑 PDF research papers (including arXiv and non-arXiv PDFs)

It allows you to **ask questions** over the ingested content using an LLM + vector database.

---

## 🚀 Features

- Web scraping support
- PDF URL ingestion (auto-download)
- Robust PDF text extraction with fallbacks
- Text cleaning & chunking
- Vector storage using **ChromaDB**
- LLM-powered question answering (RAG)
- Debug-friendly chunk inspection

---

## 🧱 Project Structure

```
.
├── main.py
├── tools/
│   ├── web_crawler.py
│   └── pdf_scraper.py
├── utils/
│   ├── pdf_url_handler.py
│   ├── text_chunker.py
│   ├── ingest.py
│   ├── vector_store.py
│   └── rag_chain.py
├── chroma_db/
└── README.md
```

---

## 🔁 RAG Pipeline Flow (End-to-End)

Below is the **complete flow of the RAG pipeline** implemented in this project:

### 1️⃣ Source Input
User provides a source:
- Web URL  
- PDF URL (e.g. research paper)
- Local PDF file

```text
User → SOURCE (URL / PDF)
```

---

### 2️⃣ Source Detection
The system detects the source type:

- `http + .pdf` → PDF URL
- `http` → Web page
- `.pdf` → Local PDF

Handled inside:
```
main.py → ingest_source()
```

---

### 3️⃣ PDF URL Handling (if applicable)

For PDF URLs:
- PDF is downloaded locally
- Temporary file path is created

```
utils/pdf_url_handler.py
```

---

### 4️⃣ Text Extraction

Depending on the source:

#### 🌐 Web
- HTML scraped
- Boilerplate removed

#### 📑 PDF
- pdfplumber (text mode)
- pdfplumber (word-flow mode) → fallback
- PyPDF2 → final fallback

Handled in:
```
tools/pdf_scraper.py
```

---

### 5️⃣ Cleaning & Section Filtering

The extracted text is:
- Lowercased
- References, tables, figures removed
- Equations stripped
- Abstract / Introduction / Conclusion preferred

This ensures **LLM-friendly text**.

---

### 6️⃣ Chunking

Cleaned text is split using:
- RecursiveCharacterTextSplitter
- Overlapping chunks for context preservation

```
utils/text_chunker.py
```

Example:
```text
Chunk size: 500
Overlap: 100
```

---

### 7️⃣ Vector Ingestion

Each chunk is:
- Embedded
- Stored in ChromaDB
- Tagged with source metadata

```
utils/ingest.py
```

---

### 8️⃣ Query Time (RAG)

When a user asks a question:

1. Question → embedding
2. Top-k relevant chunks retrieved
3. Context + question sent to LLM
4. Final grounded answer returned

```
utils/rag_chain.py
```

```text
User Question
   ↓
Vector Search
   ↓
Relevant Chunks
   ↓
LLM Prompt
   ↓
Answer
```

---

## 🧪 Example Usage

```python
SOURCE = "https://arxiv.org/pdf/1706.03762.pdf"
ingest_source(SOURCE)
chat_loop()
```

Ask:
```
What problem does this paper aim to solve?
```

---

## ⚠️ Note on arXiv PDFs

arXiv PDFs often:
- Lack proper spacing
- Use ligatures
- Embed text as glyphs

This project mitigates that using:
- `extract_words(use_text_flow=True)`
- Multiple fallback extractors

Non-arXiv PDFs usually parse perfectly.

---

## 🧹 Resetting the Database

To start fresh:
```bash
rm -rf chroma_db/
```

---

## 📌 Future Improvements

- Layout-aware PDF parsing (GROBID)
- Table-aware chunking
- Section-level metadata
- Hybrid search (BM25 + embeddings)

---

## 👨‍💻 Author

Built as a **learning-first, production-style RAG system**.

---

⭐ If this helped you, consider starring the repo!
