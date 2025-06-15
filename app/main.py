import streamlit as st
from utils import extract_text
#PAGE SETUP:
st.set_page_config(page_title="Flashcard Generator",layout="wide")
#Custom CSS for Light Mode and Dark Mode
st.markdown("""
    <style>
        body {
            background-color: #f4f7fa;
            color: #333333;  /* <-- Ensures text is always visible */
        }

        .stApp {
            background-image: linear-gradient(to right top, #e0f7fa, #f9fbe7);
            background-attachment: fixed;
        }

        h1, h2, h3, h4, h5, h6, p, div {
            color: #333333 !important;  /* <-- Fix for dark mode text */
        }

        .block-container {
            padding-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)
st.markdown("""
    <style>
        .stButton > button {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

#TITLE AND DESCRIPTION:
st.title("LLM powered Flashcard Generator")
st.markdown("Easily convert study material into smart flashcards for effective learning")

#INPUT SECTON:
st.subheader("Input Academic Material:")
#File Upload and Text Input
with st.expander("📂 Upload or Paste Content", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("Upload a `.txt` or `.pdf` file", type=['txt', 'pdf'])
    with col2:
        text_input = st.text_area("Paste your content here 👇", height=240)

#Subjet Selection
with st.sidebar:
    st.title("🧠 Settings")
    subject = st.selectbox(
        "🎓 Subject (optional)",
        ["General", "Biology", "History", "Computer Science", "Physics", "Chemistry"]
    )


#Process Input
st.subheader("Preview Input and Extract")

content=""
with st.expander("🔍 Input Preview", expanded=False):
    if st.button("📤 Show Input"):
        if uploaded_file:
            st.write(f"📄 Your File: `{uploaded_file.name}`")
        elif text_input.strip():
            st.write("📝 You Pasted:")
            st.write(text_input[:500] + "..." if len(text_input) > 500 else text_input)
        else:
            st.warning("⚠️ Please upload a file or paste some text to preview.")

#Extract text from uploaded file
with st.expander("📄 Extract Text", expanded=True):
    if st.button("Extract Text"):
        if uploaded_file:
            content = extract_text(uploaded_file)
            st.session_state["extracted_text"] = content
            st.success("✅ Text extracted successfully!")
            st.text_area("📝 Extracted Text", content[:2000] + "..." if len(content) > 2000 else content, height=300)
        elif text_input.strip():
            content = text_input
            st.session_state["extracted_text"] = content
            st.success("✅ Using pasted text!")
            st.text_area("📝 Pasted Text Preview", content[:2000] + "..." if len(content) > 2000 else content, height=300)
        else:
            st.warning("⚠️ Please upload a file or paste some text to extract.")
#Save the extracted text for LLM content
st.session_state["extracted_text"] = content
st.session_state["subject"] = subject