# Parsing Strategy

## Goals
- Maximize extraction quality  
- Support real-world document types (scans, tables, web, structured articles)  
- Minimize cost and processing latency where possible

---

## Approach & Rationale

| Type                   | Tool                          | Why                                                      |
|------------------------|-------------------------------|-----------------------------------------------------------|
| Standard PDFs          | PyMuPDF                       | Fast, layout-aware text extraction                        |
| Table-heavy PDFs       | pdfplumber                    | Accurate tabular data extraction                          |
| Scanned PDFs           | Tesseract OCR                 | Fallback OCR for image-based PDFs                         |
| Complex Layouts        | unstructured                  | Semantically tags content blocks                          |
| News/Article Web Pages | trafilatura + BeautifulSoup   | XML/text parsing for fast content-focused extraction      |
| JS-heavy Web Pages     | Playwright (planned)          | Dynamic content rendering when static parsing fails       |

---

## Parsing Flow

### PDFs
- Try `unstructured.partition.pdf` for structured blocks (titles, text, tables)  
- Fallback to PyMuPDF for page text  
- Fallback again to pdfplumber or Tesseract if needed  

### URLs
- Try `trafilatura` for XML content with structural tags  
- Fallback to `requests` + `BeautifulSoup` for raw HTML parsing  
- (Planned) Use Playwright for JS-heavy content like paywalled news  

---

## Alternatives Considered

- **AWS Textract**: Great for OCR & forms, but costly at scale  
- **Grobid**: Academic paper parsing only; not suitable for general documents  
- **pdfminer.six**: Accurate but slow and poorly maintained compared to PyMuPDF  
- **Newspaper3k**: Good for articles but abandoned and brittle  

---

## Cost Trade-offs

| Option                    | Monthly Cost (est.)     | Notes                                               |
|---------------------------|--------------------------|------------------------------------------------------|
| PyMuPDF + Tesseract       | $0                       | All open-source, good for general use               |
| AWS Textract              | $1.50 per 1,000 pages    | High OCR/structure accuracy                         |
| Playwright (headless)     | ~$0.30 per 1,000 URLs    | For JS pages; use only as fallback                  |
| Trafilatura               | $0                       | Fast, precision-focused article extraction          |

---

## Future Improvements

- Auto-detect layout type (table vs narrative vs scanned)  
- Structured error output for retry/workflow inspection  
- Multilingual content detection + translation pipeline  
- Vector-based content classification for custom domains (e.g. legal, news)  
- Optional Playwright microservice for advanced web content rendering  
