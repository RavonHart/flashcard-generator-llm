# 🧠 Flashcard Generator with LLM

This tool lets you upload or paste educational content and automatically generates flashcards using a Large Language Model (LLM).

## 🚀 Features

- Upload `.txt` or `.pdf` content
- Paste text directly
- Extract and preview content
- Subject selection for context
- Ready for flashcard generation (LLM integration coming next)

## 📦 Tech Stack

- Python
- Streamlit
- PyMuPDF (for PDF extraction)

## 📁 How to Run

```bash
pip install -r requirements.txt
streamlit run app/main.py

## 📂 Folder Structure
flashcard-generator-llm/
├── app/
│   ├── main.py         ← Streamlit app
│   └── utils.py        ← Text extraction helpers
├── sample_inputs/      ← Put your .pdf/.txt files here for testing
├── README.md
└── requirements.txt

## 📄 Requirements
streamlit
PyMuPDF
