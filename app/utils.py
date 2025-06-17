import fitz

def extract_text(file):

    #Extract plain text from a PDF or txt File.

    if file.name.endswith('.pdf'):
        text=""
        doc=fitz.open(stream=file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()
        return text

    elif file.name.endswith('.txt'):
        text = file.read().decode("utf-8")
        return text

    else:
        raise ValueError("Unsupported file type. Please upload a PDF or TXT file.")
