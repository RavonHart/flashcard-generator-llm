<<<<<<< HEAD
# 🧠 Flashcard Generator with LLM

This tool lets you upload or paste educational content and automatically generates flashcards using a Large Language Model (LLM).

## 🚀 Features

- ✅ Upload PDFs or paste raw text
- ✅ Generate 10–15 question-answer flashcards via Gemini Pro
- ✅ Clean UI with Streamlit
- ✅ Flashcards are well-structured, contextual, and exam-ready
- ✅ Export as `.csv` or `.json`
- ✅ Optional: Difficulty levels, multilingual support, structure-aware generation (coming soon)

## 📦 Tech Stack

- Python 3.9+
- [Streamlit](https://streamlit.io)
- [Google Generative AI SDK (Gemini Pro)](https://ai.google.dev/)
- PyMuPDF (`fitz`) for PDF extraction
## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/RavonHart/flashcard-generator-llm.git
cd flashcard-generator-llm

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

🔐 Environment Variables
Create a .env file in the root directory:

-GOOGLE_API_KEY=your_gemini_api_key_here

🧠 Usage

streamlit run app.py
Then go to http://localhost:8501 in your browser.

📤 Export Options
After generating flashcards, you can:

✅ Download as .csv or .json

✅ Review and edit (coming soon)

❌ Anki / Quizlet export (not yet implemented)

🧪 Development Notes
Gemini Pro is now the default LLM.

The previous FLAN-T5 logic has been retained in models/flan_t5_model.py but is not used anymore.

Heavy files and venv/ are excluded from Git. See .gitignore.

## 📂 Folder Structure
├── app.py
├── models/
│   ├── gemini_model.py
│   └── flan_t5_model.py   # Deprecated
├── utils/
│   ├── pdf_reader.py
│   └── text_processing.py
├── sample_inputs/
│   └── test.pdf
├── .env
├── requirements.txt
└── README.md

🤝 Contributing
Pull requests are welcome! For major changes, open an issue first to discuss.

🙋 Author
Made with ❤️ by @RavonHart
