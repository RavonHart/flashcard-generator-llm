# ❌ DEPRECATED MODULE: FLAN-T5 Flashcard Generator
# This file contains code for generating flashcards using FLAN-T5.
# Currently not in use — replaced by Gemini model (see gemini_flashcards_test.py).
# Kept for future reference or potential benchmarking.

# Do not import or use this in the current Streamlit app.




from transformers import pipeline, AutoTokenizer
import re
from typing import List, Dict, Optional
import torch
# Constants
PROMPT_OVERHEAD_TOKENS = 150
MAX_INPUT_TOKENS = 512 - PROMPT_OVERHEAD_TOKENS


def remove_duplicate_sentences(text: str) -> str:
    """Remove duplicate sentences while preserving order and punctuation."""
    seen = set()
    result = []
    for sentence in (s.strip() for s in text.split(". ") if s.strip()):
        if sentence not in seen:
            seen.add(sentence)
            result.append(sentence)
    return ". ".join(result) + ("." if text.endswith(".") else "")


def chunk_text(text: str, tokenizer: AutoTokenizer, max_chunks: int = 15) -> List[str]:
    """Split text into token-limited chunks while preserving sentence boundaries."""
    sentences = [s.strip() + ". " for s in text.split(". ") if s.strip()]
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        new_chunk = current_chunk + sentence
        if len(tokenizer(new_chunk)["input_ids"]) <= MAX_INPUT_TOKENS:
            current_chunk = new_chunk
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            if len(chunks) >= max_chunks:
                break

    if current_chunk and len(chunks) < max_chunks:
        chunks.append(current_chunk.strip())

    return chunks


def generate_flashcards(
        text: str,
        subject: str = "General",
        n_cards: int = 15,
        model: Optional[pipeline] = None,
        tokenizer: Optional[AutoTokenizer] = None
) -> List[Dict[str, str]]:
    """Generate flashcards from input text with improved robustness."""
    # Initialize model and tokenizer if not provided
    if model is None or tokenizer is None:
        local_tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")
        local_model = pipeline(
            "text2text-generation",
            model="google/flan-t5-large",
            device=0 if torch.cuda.is_available() else -1,
            truncation=True
        )
    else:
        local_tokenizer = tokenizer
        local_model = model

    text = remove_duplicate_sentences(text)
    chunks = chunk_text(text, local_tokenizer, max_chunks=n_cards)
    flashcards = []

    for chunk in chunks:
        prompt = f"""
        Act as a top-tier educator in {subject}. Create exactly one high-quality flashcard from this content:

        Content: \"\"\"{chunk.strip()}\"\"\"

        Requirements:
        1. Question (Q:): Clear, self-contained, tests key knowledge (max 15 words)
        2. Answer (A:): Precise 2-3 sentence explanation using only content facts

        Format strictly as:
        Q: [question] 
        A: [answer]"""

        result = local_model(
            prompt.strip(),
            max_new_tokens=150,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )[0]['generated_text']

        # Enhanced parsing with multiple fallback strategies
        card = None

        # Strategy 1: Strict Q:/A: format
        match = re.search(r"Q:\s*(.*?)\s*A:\s*(.*)", result, re.IGNORECASE | re.DOTALL)
        if match:
            question = match.group(1).strip()
            if not question.endswith("?"):
                question += "?"
            card = {
                "question": question,
                "answer": match.group(2).strip()
            }

        # Strategy 2: Question mark detection
        if not card and "?" in result:
            parts = result.split("?", 1)
            card = {
                "question": parts[0].strip() + "?",
                "answer": parts[1].strip()
            }

        if card:
            flashcards.append(card)
            if len(flashcards) >= n_cards:
                break

    return flashcards


if __name__ == "__main__":
    sample_text = """
    Compared to past generations, we face a whole new level of pressure to be perfect. 
    Social media isn't just a place to connect anymore—it's a place to perform. 
    People only post the best parts of their lives. 
    This leads to a culture of comparison, causing anxiety and stress among teens.
    """

    cards = generate_flashcards(sample_text, subject="Teen Mental Health", n_cards=3)
    for i, card in enumerate(cards, 1):
        print(f"Card {i}:")
        print(f"Q: {card['question']}")
        print(f"A: {card['answer']}\n")