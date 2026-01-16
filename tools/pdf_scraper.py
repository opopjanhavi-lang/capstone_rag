import pdfplumber
import re
from pathlib import Path
from PyPDF2 import PdfReader


# -------------------- NOISE PATTERNS --------------------

NOISE_PATTERNS = [
    r"references\s*.*$",
    r"bibliography\s*.*$",
    r"figure\s*\d+.*",
    r"table\s*\d+.*",
    r"©.*",
    r"arxiv:\d+\.\d+",
    r"equal contribution.*",
    r"listing order.*",
    r"corresponding author.*",
]


# -------------------- GARBLED TEXT DETECTION --------------------

def is_garbled(text: str) -> bool:
    if not text or len(text) < 50:
        return True

    non_alpha = sum(1 for c in text if not c.isalnum() and not c.isspace())
    ratio = non_alpha / max(len(text), 1)

    return ratio > 0.4


# -------------------- EXTRACTION METHODS --------------------

def extract_with_pdfplumber_text(pdf_path: str) -> str:
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
    return "\n".join(pages)


def extract_with_pdfplumber_words(pdf_path: str) -> str:
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            words = page.extract_words(use_text_flow=True)
            page_text = " ".join(word["text"] for word in words)
            if page_text:
                pages.append(page_text)
    return "\n".join(pages)


def extract_with_pypdf2(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    return "\n".join(pages)


# -------------------- CLEANING & REPAIR --------------------

def remove_noise(text: str) -> str:
    cleaned = text.lower()

    for pattern in NOISE_PATTERNS:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE | re.MULTILINE)

    cleaned = re.sub(r"\$.*?\$", "", cleaned)   # equations
    cleaned = re.sub(r"\[.*?\]", "", cleaned)   # citations

    return cleaned


def fix_spacing(text: str) -> str:
    # lowercase → Uppercase
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)

    # letter → number / number → letter
    text = re.sub(r"([a-zA-Z])(\d)", r"\1 \2", text)
    text = re.sub(r"(\d)([a-zA-Z])", r"\1 \2", text)

    # punctuation spacing
    text = re.sub(r"([.,;:!?])([A-Za-z])", r"\1 \2", text)

    # normalize whitespace
    return re.sub(r"\s+", " ", text).strip()


# -------------------- SECTION EXTRACTION --------------------

def extract_sections(text: str) -> str:
    sections = []

    patterns = [
        r"abstract\s*(.*?)(introduction|1\. introduction)",
        r"(introduction|1\. introduction)\s*(.*?)(related work|methodology|methods|conclusion)",
        r"(conclusion|discussion)\s*(.*)$",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            sections.append(match.group(0))

    return "\n".join(sections)


# -------------------- MAIN SCRAPER --------------------

def scrape_pdf(pdf_path: str) -> dict:
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(pdf_path)

    # 1️⃣ Primary extraction
    text = extract_with_pdfplumber_text(str(pdf_path))

    # 2️⃣ Fallback: extract_words
    if is_garbled(text):
        print("⚠️ Garbled text detected → using pdfplumber.extract_words()")
        text = extract_with_pdfplumber_words(str(pdf_path))

    # 3️⃣ Final fallback: PyPDF2
    if is_garbled(text):
        print("⚠️ Still garbled → using PyPDF2 fallback")
        text = extract_with_pypdf2(str(pdf_path))

    # 4️⃣ Cleaning & repair
    cleaned = remove_noise(text)
    cleaned = fix_spacing(cleaned)

    # 5️⃣ Section prioritization
    sections = extract_sections(cleaned)
    final_text = sections if sections.strip() else cleaned

    return {
        "source": pdf_path.name,
        "text": final_text
    }
