import torch
import streamlit as st

from utils import extract_text
from llm_utils import generate_flashcards

#PAGE SETUP:
st.set_page_config(page_title="Flashcard Generator", layout="wide")

#STYLE
st.markdown("""
    <style>
        body {
            background-color: #f4f7fa;
            color: #333333;
        }
        .stApp {
            background-image: linear-gradient(to right top, #e0f7fa, #f9fbe7);
            background-attachment: fixed;
        }
        h1, h2, h3, h4, h5, h6, p, div {
            color: #333333 !important;
        }
        .block-container {
            padding-top: 2rem;
        }
        .stButton > button {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

#TITLE
st.title("LLM powered Flashcard Generator")
st.markdown("Easily convert study material into smart flashcards for effective learning")

#INPUT SECTION
st.subheader("Input Academic Material:")

with st.expander("📂 Upload or Paste Content", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("Upload a `.txt` or `.pdf` file", type=['txt', 'pdf'])
    with col2:
        text_input = st.text_area("Paste your content here 👇", height=240)

#SIDEBAR SETTINGS
with st.sidebar:
    st.title("🧠 Settings")
    subject = st.selectbox("🎓 Subject (optional)", ["General", "Biology", "History", "Computer Science", "Physics", "Chemistry"])

#EXTRACT TEXT INTO SESSION STATE
if "extracted_text" not in st.session_state:
    if uploaded_file:
        st.session_state["extracted_text"] = extract_text(uploaded_file)
    elif text_input.strip():
        st.session_state["extracted_text"] = text_input

#PREVIEW SECTION
st.subheader("Preview Input and Extract")

with st.expander("🔍 Input Preview", expanded=False):
    if st.button("📤 Show Input"):
        if uploaded_file:
            st.write(f"📄 Your File: `{uploaded_file.name}`")
        elif text_input.strip():
            st.write("📝 You Pasted:")
            st.write(text_input[:500] + "..." if len(text_input) > 500 else text_input)
        else:
            st.warning("⚠️ Please upload a file or paste some text to preview.")

#EXTRACT BUTTON
with st.expander("📄 Extract Text", expanded=True):
    if st.button("Extract Text"):
        if uploaded_file:
            st.session_state["extracted_text"] = extract_text(uploaded_file)
            st.success("✅ Text extracted successfully!")
        elif text_input.strip():
            st.session_state["extracted_text"] = text_input
            st.success("✅ Using pasted text!")
        else:
            st.warning("⚠️ Please upload a file or paste some text to extract.")

    if "extracted_text" in st.session_state and st.session_state["extracted_text"]:
        preview_text = st.session_state["extracted_text"]
        st.text_area("📝 Text Preview", preview_text[:2000] + "..." if len(preview_text) > 2000 else preview_text, height=300)

#GENERATE FLASHCARDS
if st.button("Generate Flashcards"):
    content = st.session_state.get("extracted_text", "").strip()
    if content:
        with st.spinner("Generating flashcards..."):
            flashcards = generate_flashcards(content, subject)

        if flashcards:
            st.subheader("Generated Flashcards:")
            for i, card in enumerate(flashcards):
                st.markdown(f"**Q{i+1}: {card['question']}**")
                st.markdown(f"A{i+1}: {card['answer']}")
                st.markdown("----")
        else:
            st.warning("No flashcards generated. Try with different content.")
    else:
        st.warning("Please upload or paste text before generating flashcards.")

#RESET SESSION (Optional for Debugging)
with st.sidebar:
    if st.button("🧹 Reset"):
        st.session_state.clear()
        st.experimental_rerun()