import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    return {
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "device": "cuda" if os.environ.get("LP1_DEVICE") == "cuda" else "cpu",
        "data_path": os.getenv("LP1_DATA_PATH", "./data"),
        "vector_store": os.getenv("LP1_VECTOR_STORE", "./data/knowledge_vectors.faiss"),
        "memory_file": os.getenv("LP1_MEMORY_FILE", "./data/lp1_memory.json"),
        "log_feedback": os.getenv("LP1_FEEDBACK_LOG", "./data/feedback.json"),
        "patch_path": os.getenv("LP1_PATCH_FILE", "./data/patch.diff")
    }