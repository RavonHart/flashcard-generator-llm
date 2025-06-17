from transformers import pipeline

#Load the model FLAN-T5
flan_pipe=pipeline("text2text-generation", model="google/flan-t5-base")

def generate_flashcards(text,subject="General", n_cards=15):
    chunks=text.strip().split(". ")[:n_cards]  #split text into sentence and limit to n_cards

    flashcards=[]
    for i, chunk in enumerate(chunks):
        prompt=f"""You are an expert in {subject}. Generate 15 concise flashcards from the provided text. Each flashcard must include:
        Question: Clear, standalone, and phrased to test knowledge.
        Answer: Factually correct, accurate self-contained(no external references), and concise(2-5 sentences max)
        
        Format strictly as follows:
        Q: [Question]
        A: [Answer]
        
        Text to process:{chunk.strip()}"""

    #results
    result= flan_pipe(prompt.strip(), max_new_tokens=1024)[0]['generated_text']

    #post processing to create Q&A pairs
    flashcards=[]
    lines=result.split("\n")
    current_que ,current_ans= None, None

    for line in lines:
        if line.strip().startswith("Q:"):
            current_que=line.replace("Q:", "").strip()
        elif line.strip().startswith("A:"):
            current_ans=line.replace("A:").strip()
            if current_que and current_ans:
                flashcards.append({"question": current_que, "answer": current_ans})
                current_que, current_ans = None, None

    return flashcards