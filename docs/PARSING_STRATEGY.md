## Parsing Strategy

### Goals
- Maximize extraction quality
- Support real-world document types (scans, tables, web)
- Minimize cost where possible

---

### Approach & Rationale

| Type | Tool | Why |
|------|------|-----|
| Standard PDFs | PyMuPDF | Fast, accurate layout |
| Table PDFs | pdfplumber | Preserves structure |
| Scanned PDFs | Tesseract OCR | Open-source OCR |
| Complex Layouts | unstructured | Handles noisy/mixed content |
| JS-heavy Web Pages | Playwright | Real DOM execution |

---

### Alternatives Considered

- **AWS Textract**: Excellent quality but costly for bulk OCR.
- **Grobid**: Great for academic PDFs but limited layout support.
- **pdfminer.six**: Slow and outdated vs PyMuPDF.

---

### Cost Trade-offs

| Option | Monthly Cost (est.) | Notes |
|--------|----------------------|-------|
| PyMuPDF + Tesseract | $0 | Free tools, lower accuracy on bad scans |
| AWS Textract | $1.50 per 1000 pages | High accuracy, good fallback |
| Playwright | ~$0.30 per 1000 URLs (with serverless) | Good for JS pages |

---

### Future Improvements

- Auto-detect layout type using ML
- Batch OCR via serverless for scale
- Add language detection + translation
