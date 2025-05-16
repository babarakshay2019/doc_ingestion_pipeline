#
import textract
import requests
from bs4 import BeautifulSoup

def extract_text_from_file(filepath: str) -> str:
    return textract.process(filepath).decode("utf-8")

def extract_text_from_url(url: str) -> str:
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text(separator="\n")
