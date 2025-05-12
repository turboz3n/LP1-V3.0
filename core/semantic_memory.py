import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class SemanticMemory:
    def __init__(self, config):
        self.index_path = config["vector_store"]
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.data_path = self.index_path.replace(".faiss", ".json")

        self.texts = []
        self.index = faiss.IndexFlatL2(384)

        if os.path.exists(self.index_path) and os.path.exists(self.data_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.data_path, "r") as f:
                self.texts = json.load(f)

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.data_path, "w") as f:
            json.dump(self.texts, f, indent=2)

    def store(self, text: str):
        vector = self.model.encode([text])
        self.index.add(np.array(vector, dtype=np.float32))
        self.texts.append(text)
        self.save()

    def query(self, prompt: str, top_k: int = 5):
        vector = self.model.encode([prompt])
        distances, indices = self.index.search(np.array(vector, dtype=np.float32), top_k)
        return [self.texts[i] for i in indices[0] if i < len(self.texts)]