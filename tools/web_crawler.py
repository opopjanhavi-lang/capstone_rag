import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

def fetch_html(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.text


import re
from bs4 import BeautifulSoup

def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # Remove junk tags
    for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
        tag.decompose()

    main = soup.find("div", {"id": "mw-content-text"})
    if not main:
        main = soup

    text = main.get_text(separator=" ")

    # Remove citations like [1], [2], [12]
    text = re.sub(r"\[\d+\]", "", text)

    # Remove excessive whitespace
    text = " ".join(text.split())

    # Remove reference section explicitly
    stop_words = ["References", "External links", "See also"]
    for word in stop_words:
        if word in text:
            text = text.split(word)[0]

    return text



def crawl_url(url: str) -> dict:
    """
    Web Crawler Tool

    Input:
        url (str)

    Output:
        {
            "source": url,
            "text": extracted plain text
        }
    """
    html = fetch_html(url)
    text = html_to_text(html)

    return {
        "source": url,
        "text": text
    }
