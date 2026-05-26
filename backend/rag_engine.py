import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List

class RAGEngine:
    def __init__(self, api_key: str, knowledge_base_path: str):
        # api_key is not needed for local embeddings, but keeping signature compatible
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.documents = self._load_documents(knowledge_base_path)
        self.index = self._build_index()

    def _load_documents(self, path: str) -> List[str]:
        if not os.path.exists(path):
            return []
        with open(path, 'r') as f:
            text = f.read()
        # Simple splitting by newline for this demo
        return [line.strip() for line in text.split('\n') if line.strip()]

    def _get_embedding(self, text: str) -> np.ndarray:
        # SentenceTransformer returns numpy array by default
        return self.model.encode(text)

    def _build_index(self):
        if not self.documents:
            return None
        
        embeddings = self.model.encode(self.documents)
        
        # Faiss expects float32
        embeddings_np = np.array(embeddings, dtype='float32')
        dimension = embeddings_np.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings_np)
        return index

    def retrieve(self, query: str, k: int = 3) -> str:
        if not self.index:
            return ""
            
        query_embedding = self.model.encode([query])
        query_np = np.array(query_embedding, dtype='float32')
        
        distances, indices = self.index.search(query_np, k)
        
        results = [self.documents[i] for i in indices[0] if i < len(self.documents)]
        return "\n".join(results)
