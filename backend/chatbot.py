import os
from groq import Groq
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, util
from data import FAQ_DATA, SYSTEM_PROMPT

load_dotenv()

# Initialize Groq Client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Initialize Semantic Search Model (Intent Classification)
# This model runs locally and is very fast
embedder = SentenceTransformer('all-MiniLM-L6-v2')
faq_questions = [item["question"] for item in FAQ_DATA]
faq_embeddings = embedder.encode(faq_questions, convert_to_tensor=True)

def classify_intent(query: str):
    query_embedding = embedder.encode(query, convert_to_tensor=True)
    cos_scores = util.cos_sim(query_embedding, faq_embeddings)[0]
    top_results = util.semantic_search(query_embedding, faq_embeddings, top_k=1)
    
    score = top_results[0][0]['score']
    idx = top_results[0][0]['corpus_id']
    
    if score > 0.6: # Threshold for intent matching
        return FAQ_DATA[idx]["intent"], FAQ_DATA[idx]["answer"]
    return "unknown", None

def generate_response(query: str):
    intent, faq_answer = classify_intent(query)
    
    # Prepare context for Groq
    faq_context = "\n".join([f"Q: {item['question']} A: {item['answer']}" for item in FAQ_DATA])
    
    prompt = SYSTEM_PROMPT.format(faq_context=faq_context)
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": query}
            ],
            model="llama-3.1-8b-instant", # Newer, faster model
            temperature=0.2, # Low temperature for factual consistency
            max_tokens=150
        )
        response_text = chat_completion.choices[0].message.content
        return response_text, intent
    except Exception as e:
        return f"I'm sorry, I'm having trouble connecting. {str(e)}", "error"
