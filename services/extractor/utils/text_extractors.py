import fitz
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import requests
from bs4 import BeautifulSoup
import trafilatura

def smart_pdf_parser(file_path: str) -> str:
    """
    Extract text from a PDF file using multiple strategies:
    PyMuPDF > pdfplumber > OCR fallback.
    """
    try:
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()

        if len(text.strip()) < 100:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""

        if len(text.strip()) < 100:
            images = convert_from_path(file_path)
            for img in images:
                text += pytesseract.image_to_string(img)

        return text.strip()

    except Exception as e:
        return f"PDF extraction failed: {str(e)}"


def smart_url_parser(url: str) -> str:
    """
    Extract text from a URL using trafilatura with a fallback to BeautifulSoup.
    """
    try:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            extracted = trafilatura.extract(downloaded)
            if extracted:
                return extracted.strip()

        # Fallback: BeautifulSoup extraction
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise if not 200 OK

        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()

        return soup.get_text(separator="\n", strip=True)

    except Exception as e:
        return f"URL extraction failed: {str(e)}"