"""
RAG Engine using FAISS and Sentence Transformers
"""

import warnings
import os

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*Pydantic.*')
warnings.filterwarnings('ignore', message='.*HF Hub.*')
warnings.filterwarnings('ignore', message='.*UNEXPECTED.*')
warnings.filterwarnings('ignore', message='.*MISSING.*')

# Suppress HuggingFace verbosity
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Optional

class RAGEngine:
    """Retrieval-Augmented Generation engine."""
    
    def __init__(self, vector_db_path: str = "./data/vector_db", model_name: str = "all-MiniLM-L6-v2"):
        """Initialize RAG engine."""
        self.vector_db_path = vector_db_path
        # Suppress warnings during model loading
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.model = SentenceTransformer(model_name)
        self.index = None
        self.documents = []
        self.loaded = False
        self._load_vector_db()
    
    def _load_vector_db(self):
        """Load FAISS index and documents."""
        index_path = os.path.join(self.vector_db_path, "index.faiss")
        documents_path = os.path.join(self.vector_db_path, "documents.pkl")
        
        if os.path.exists(index_path) and os.path.exists(documents_path):
            try:
                self.index = faiss.read_index(index_path)
                with open(documents_path, 'rb') as f:
                    self.documents = pickle.load(f)
                self.loaded = True
                print(f"✅ RAG engine loaded: {len(self.documents)} documents")
            except Exception as e:
                print(f"⚠️ Error loading vector DB: {e}")
                self.loaded = False
        else:
            print("ℹ️ Vector database not found. Run data ingestion first.")
            self.loaded = False
    
    def search(self, query: str, top_k: int = 3, min_relevance: float = 0.3) -> str:
        """Search for relevant documents with relevance scoring and filtering."""
        if not self.loaded or self.index is None or len(self.documents) == 0:
            return ""
        
        try:
            # Encode query
            query_embedding = self.model.encode([query])
            query_embedding = query_embedding.astype('float32')
            
            # Search with more results for filtering
            k = min(top_k * 2, len(self.documents))  # Get more results for filtering
            distances, indices = self.index.search(query_embedding, k)
            
            # Calculate relevance scores (normalize distances to similarity scores)
            # FAISS returns L2 distances, convert to similarity (lower distance = higher similarity)
            max_distance = np.max(distances[0]) if len(distances[0]) > 0 else 1.0
            relevance_scores = []
            
            results = []
            for i, idx in enumerate(indices[0]):
                if 0 <= idx < len(self.documents):
                    distance = distances[0][i]
                    # Convert distance to similarity score (0-1 range)
                    # Using exponential decay for better scoring
                    similarity = np.exp(-distance / (max_distance + 1e-6))
                    relevance_scores.append(similarity)
                    
                    # Only include results above minimum relevance threshold
                    if similarity >= min_relevance:
                        results.append({
                            'text': self.documents[idx],
                            'score': similarity,
                            'index': idx
                        })
            
            # Sort by relevance score (highest first)
            results.sort(key=lambda x: x['score'], reverse=True)
            
            # Take top_k results
            top_results = results[:top_k]
            
            # Return only the text, filtered by relevance
            return "\n".join([r['text'] for r in top_results]) if top_results else ""
        
        except Exception as e:
            print(f"RAG search error: {e}")
            return ""
    
    def search_with_scores(self, query: str, top_k: int = 3, min_relevance: float = 0.3):
        """Search and return results with relevance scores."""
        if not self.loaded or self.index is None or len(self.documents) == 0:
            return []
        
        try:
            query_embedding = self.model.encode([query])
            query_embedding = query_embedding.astype('float32')
            
            k = min(top_k * 2, len(self.documents))
            distances, indices = self.index.search(query_embedding, k)
            
            max_distance = np.max(distances[0]) if len(distances[0]) > 0 else 1.0
            results = []
            
            for i, idx in enumerate(indices[0]):
                if 0 <= idx < len(self.documents):
                    distance = distances[0][i]
                    similarity = np.exp(-distance / (max_distance + 1e-6))
                    
                    if similarity >= min_relevance:
                        results.append({
                            'text': self.documents[idx],
                            'score': float(similarity),
                            'index': idx
                        })
            
            results.sort(key=lambda x: x['score'], reverse=True)
            return results[:top_k]
        
        except Exception as e:
            print(f"RAG search error: {e}")
            return []
    
    def build_index(self, documents: List[str]):
        """Build FAISS index from documents."""
        if not documents:
            print("No documents to index")
            return
        
        print(f"Building RAG index for {len(documents)} documents...")
        
        # Generate embeddings
        embeddings = self.model.encode(documents, show_progress_bar=True)
        embeddings = embeddings.astype('float32')
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
        
        # Save
        self.documents = documents
        os.makedirs(self.vector_db_path, exist_ok=True)
        
        index_path = os.path.join(self.vector_db_path, "index.faiss")
        documents_path = os.path.join(self.vector_db_path, "documents.pkl")
        
        faiss.write_index(self.index, index_path)
        with open(documents_path, 'wb') as f:
            pickle.dump(documents, f)
        
        self.loaded = True
        print(f"RAG index built and saved: {len(documents)} documents")
    
    def is_loaded(self) -> bool:
        """Check if RAG engine is loaded."""
        return self.loaded

