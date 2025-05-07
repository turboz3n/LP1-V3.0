import os
from typing import Dict

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import chromadb
from chromadb.utils import embedding_functions

# Load NLP model
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

# Set up Chroma DB
client = chromadb.Client()
collection = client.get_or_create_collection("lp1_memory")
embedder = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

def predict(inputs: Dict) -> Dict:
    user_input = inputs.get("input", "").strip()
    feedback = inputs.get("feedback", None)

    if not user_input:
        return {"error": "Empty input"}

    # Check memory
    similar = collection.query(query_texts=[user_input], n_results=3)
    context = " ".join([item for item in similar["documents"][0]]) if similar["documents"] else ""
    prompt = f"{context}\nUser: {user_input}\nCommand:"

    # NLP interpretation
    tokens = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    output = model.generate(**tokens, max_new_tokens=50)
    interpreted = tokenizer.decode(output[0], skip_special_tokens=True).strip()

    # Store to memory
    collection.add(
        documents=[interpreted],
        metadatas=[{"input": user_input}],
        ids=[f"id_{hash(user_input) % (10 ** 8)}"]
    )

    # Optionally process feedback
    feedback_note = f"Feedback received: {feedback}" if feedback else "No feedback"
    return {
        "interpreted": interpreted,
        "context_used": context,
        "feedback_status": feedback_note
    }
 
