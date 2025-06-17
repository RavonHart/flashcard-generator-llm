import re
from typing import List, Dict
import google.generativeai as genai

import os

import streamlit as st
import google.generativeai as genai

# Load API key from Streamlit secrets
API_KEY = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in Streamlit secrets or environment variables.")

# Configure Gemini
genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-1.5-flash"  # or "gemini-1.5-pro"

#INITIALIZE GEMINI MODEL
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)
#Removes duplicate sentences while preserving order and punctuation
def remove_duplicate_sentences(text: str) -> str:
    seen = set()
    result = []
    for sentence in (s.strip() for s in text.split(". ") if s.strip()):
        if sentence not in seen:
            seen.add(sentence)
            result.append(sentence)
    return ". ".join(result) + ("." if text.endswith(".") else "")
#chunks text into sentence-based chunks for flashcard generation
def chunk_text(text: str, max_sentences: int = 2, max_chunks: int = 15) -> List[str]:
    """Split text into sentence-based chunks for flashcard generation."""
    sentences = [s.strip() + '.' for s in text.split(".") if s.strip()]
    chunks, current_chunk = [], []

    for sentence in sentences:
        current_chunk.append(sentence)
        if len(current_chunk) >= max_sentences:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            if len(chunks) >= max_chunks:
                break

    if current_chunk and len(chunks) < max_chunks:
        chunks.append(" ".join(current_chunk))

    return chunks
# Generates flashcards from the provided text using the Gemini model
def generate_flashcards(
    text: str,
    subject: str = "General",
    n_cards: int = 15,
    difficulty: str = "Medium"
) -> List[Dict[str, str]]:
    text = remove_duplicate_sentences(text)
    chunks = chunk_text(text, max_chunks=n_cards)
    flashcards = []

    for chunk in chunks:
        prompt = f"""
        Act as a master educator in {subject}. Generate one {difficulty.lower()}-level flashcard based on this content.
        Content:
        \"\"\"{chunk.strip()}\"\"\"

        Requirements:
        1. Question (Q:): Must be concise, clear, and knowledge-checking.
        2. Answer (A:): Provide a well-structured 3–4 sentence answer, giving context, reasoning, and clarity.

        Format strictly as:
        Q: [question]  
        A: [answer]
        """

        try:
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_output_tokens": 300
                }
            )
            result = response.text.strip()

            #regex parsing
            match = re.search(r"Q:\s*(.*?)\s*A:\s*(.*)", result, re.DOTALL)
            if match:
                question = match.group(1).strip()
                answer = match.group(2).strip()
                if not question.endswith("?"):
                    question += "?"
                flashcards.append({
                    "question": question,
                    "answer": answer,
                    "difficulty": difficulty
                })
            elif "?" in result:
                parts = result.split("?", 1)
                flashcards.append({
                    "question": parts[0].strip() + "?",
                    "answer": parts[1].strip(),
                    "difficulty": difficulty
                })

            if len(flashcards) >= n_cards:
                break
        except Exception as e:
            print("Error generating flashcard:", e)

    return flashcards
#testing
if __name__ == "__main__":
    sample_text = """
    Compared to past generations, we face a whole new level of pressure to be perfect. 
    Social media isn't just a place to connect anymore—it's a place to perform. 
    People only post the best parts of their lives. 
    This leads to a culture of comparison, causing anxiety and stress among teens.
    """
    cards = generate_flashcards(sample_text, subject="Teen Mental Health", n_cards=15)
    for i, card in enumerate(cards, 1):
        print(f"Card {i}:")
        print(f"Q: {card['question']}")
        print(f"A: {card['answer']}\n")