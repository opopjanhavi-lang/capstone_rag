import requests
from pathlib import Path
import tempfile

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def download_pdf_from_url(pdf_url: str) -> Path:
    response = requests.get(pdf_url, headers=HEADERS, timeout=20)
    response.raise_for_status()

    if "application/pdf" not in response.headers.get("Content-Type", ""):
        raise ValueError("URL does not point to a PDF")

    temp_dir = Path(tempfile.gettempdir())
    filename = pdf_url.split("/")[-1]
    pdf_path = temp_dir / filename

    with open(pdf_path, "wb") as f:
        f.write(response.content)

    return pdf_path
