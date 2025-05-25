# agentic-ai-office-automation

# Agentic AI Office Automation

A modular Agentic AI system that reads diverse PDF documents, extracts structured information using LLMs, and automatically routes the content into the correct office application — like Excel or Google Sheets. Built for real-world Field Force Automation (FFA), this project demonstrates how AI agents can autonomously act on unstructured inputs.

---

## Features

- Automatic PDF type classification (invoice, application form, meeting summary)
- OCR support for scanned/image-based PDFs
- Intelligent field extraction via Gemini 1.5 Flash (LLM)
- Rule-based destination routing (Excel or Google Sheets)
- Structured schema formatting
- CLI-based UX for fast prototyping
- Modular Python architecture with testable components

---

## Supported PDF Types

| PDF Type            | Format           | Output Destination | Key Fields Extracted                                 |
|---------------------|------------------|---------------------|------------------------------------------------------|
| **Invoice**         | Tabular / KV     | Excel (.xlsx)       | Invoice #, Vendor, Line Items, Subtotal, Tax, Total |
| **Application Form**| Key-Value Form   | Google Sheets       | Name, Email, Phone, Address, Education, Position     |
| **Meeting Summary** | Paragraph-based  | Google Sheets       | Title, Date, Attendees, Agenda, Action Items         |

---

## Why Agentic AI?

Unlike pure generative models, this system uses **Agentic AI** — combining LLMs with autonomous decision-making and planning.

- **LLMs** handle text interpretation
- **Agents** make structured decisions (What is this? Where should it go?)
- **Pipelines** automate the workflow end-to-end

See [`research.md`](./research.md) for details on Agentic AI vs Generative AI.

---

## Folder Structure
```
agentic-ai-office-automation/
├── app/               # Main logic
│   ├── agent/         # Planner/Router
│   ├── pipelines/     # Per-doc workflows
│   ├── extractors/    # PDF parsers + LLMs
│   ├── routers/       # Excel / GSheet writers
│   └── utils/         # OCR, doc type detection
├── config/            # YAML schemas and routes
├── data/              # Sample PDFs and outputs
├── run.py             # CLI Entry point
├── requirements.txt   # Python dependencies
└── README.md          # You’re here
```

---

## How to Run

### 1. Setup

```bash
pip install -r requirements.txt
```
For Google Sheets to work, add your Gemini API key and Google Sheets credentials to `.env` and `config/gsheet_service_account.json`.

### 2. Run from CLI

```bash
# Invoice → Excel
python run.py data/sample_pdfs/invoice_example_01.pdf --excel_path data/sample_outputs/invoice.xlsx

# Application Form → Google Sheets
python run.py data/sample_pdfs/application_example_01.pdf --sheet_name Application

# Meeting Summary → Google Sheets (exploded by line item)
python run.py data/sample_pdfs/meeting_summary_example_01.pdf --sheet_name Meeting_Summary
```

---

## Technologies Used

- **Python** 3.12
- **Gemini** 1.5 Flash Api (Google Generative AI)
- **pymupdf*, **pdfplumber**, **Tesseract OCR**
- **gspread** for Google Sheets integration
- **pandas** for data formatting
- **black** for code formatting

---

## Licence

MIT Licence. See included LICENSE.