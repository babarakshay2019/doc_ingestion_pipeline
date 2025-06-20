import collections
import collections.abc
from urllib.parse import urlparse

import fitz
import pdfplumber
import pytesseract
import requests
import trafilatura
from bs4 import BeautifulSoup
from pdf2image import convert_from_path
from unstructured.partition.pdf import partition_pdf

collections.Callable = collections.abc.Callable


def smart_pdf_parser(file_path: str) -> list:
    try:
        elements = partition_pdf(filename=file_path)
        structured_output = []
        for el in elements:
            structured_output.append(
                {
                    "type": el.category,
                    "text": el.text,
                    "metadata": {
                        "page_number": el.metadata.page_number,
                        "coordinates": el.metadata.coordinates,
                    },
                }
            )

        if structured_output:
            return structured_output

    except Exception:
        pass  # Try fallback methods

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

        return [{"type": "Text", "text": text.strip()}]
    except Exception as e:
        return [{"type": "error", "text": f"PDF extraction failed: {str(e)}"}]


def smart_url_parser(url: str) -> dict:
    try:
        # Normalize URL
        parsed = urlparse(url)
        if not parsed.scheme:
            url = "https://" + url

        # Try with trafilatura
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            extracted = trafilatura.extract(
                downloaded,
                output_format="xml",
                include_comments=False,
                include_tables=True,
                favor_precision=True,
            )
            if extracted:
                soup = BeautifulSoup(extracted, "xml")
                structured_sections = []

                for section in soup.find_all(
                    ["head", "p", "h1", "h2", "h3", "ul", "ol", "li", "table"]
                ):
                    text = section.get_text(strip=True)
                    if text:
                        structured_sections.append({"type": section.name, "text": text})

                return {"url": url, "sections": structured_sections}

        # Fallback: raw HTML parsing with requests
        response = requests.get(
            url, timeout=60, allow_redirects=True, headers={"User-Agent": "Mozilla/5.0"}
        )
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()

        return {
            "url": url,
            "sections": [{"type": "text", "text": soup.get_text(separator="\n", strip=True)}],
        }

    except requests.exceptions.Timeout:
        return {"error": f"Timeout while fetching URL: {url}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error while fetching URL: {str(e)}"}
    except Exception as e:
        return {"error": f"URL extraction failed: {str(e)}"}
