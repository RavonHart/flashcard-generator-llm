import streamlit as st
from utils import extract_text
#PAGE SETUP:
st.set_page_config(page_title="Flashcard Generator",layout="wide")
st.title("LLM powered Flashcard Generator")
st.markdown("Easily convert study material into smart flashcards for effective learning")

#INPUT SECTON:
st.subheader("Input Academic Material:")
col1, col2=st.columns(2)

#file uploader
with col1:
    st.markdown("Upload a File")
    uploaded_file=st.file_uploader("Upload a txt or pdf file", type=["txt", "pdf"])

#creating a test area
with col2:
    st.markdown("Or Paste Text")
    text_input=st.text_area("Paste your topic/content here to generate flashcards", height=200)

#Subjet Selection
subject = st.selectbox(
    "Select a subject(optional)",
    ["Math", "Physics", "History", "Computer Science", "Chemistry", "Biology", "Literature"])

#Process Input
st.subheader("Preview Input and Extract")

content=""
if st.button(" Show Input"):
    if uploaded_file:
        st.write(f" Your File: `{uploaded_file.name}`")
    elif text_input.strip():
        st.write("You Pasted:")
        st.write(text_input[:500] + "..." if len(text_input) > 500 else text_input)
    else:
        st.warning("Please upload a file or paste some text to preview.")

#Extract text from uploaded file
if st.button("Extract Text"):
    if uploaded_file:
        content = extract_text(uploaded_file)
        st.success("Text extracted successfully!")
        st.text_area(
            "Extracted Text",
            content[:2000] + "..." if len(content) > 2000 else content,
            height=300
        )
    elif text_input.strip():
        content = text_input
        st.success("Using pasted text!")
        st.text_area(
            "Pasted Text Preview",
            content[:2000] + "..." if len(content) > 2000 else content,
            height=300
        )
    else:
        st.warning("Please upload a file or paste some text to extract.")
#Save the extracted text for LLM content
st.session_state["extracted_text"] = content
st.session_state["subject"] = subject