"""
Data ingestion script for hospital documents.
Builds RAG index from hospital knowledge base.
"""

import os
import sys
from pathlib import Path
from typing import List
import PyPDF2

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from ai.rag_engine import RAGEngine

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF file."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
    return text

def extract_text_from_file(file_path: str) -> str:
    """Extract text from a text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ""

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Split text into chunks with overlap."""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    
    return chunks

def load_hospital_data(data_path: str) -> List[str]:
    """Load all documents from the hospital data directory."""
    documents = []
    
    data_dir = Path(data_path)
    if not data_dir.exists():
        print(f"Data directory {data_path} does not exist. Creating it...")
        data_dir.mkdir(parents=True, exist_ok=True)
        return documents
    
    # Supported file extensions
    pdf_extensions = ['.pdf']
    text_extensions = ['.txt', '.md']
    
    for file_path in data_dir.rglob('*'):
        if file_path.is_file():
            file_ext = file_path.suffix.lower()
            
            if file_ext in pdf_extensions:
                text = extract_text_from_pdf(str(file_path))
                if text.strip():
                    chunks = chunk_text(text)
                    documents.extend(chunks)
            
            elif file_ext in text_extensions:
                text = extract_text_from_file(str(file_path))
                if text.strip():
                    chunks = chunk_text(text)
                    documents.extend(chunks)
    
    return documents

def main():
    """Main ingestion function."""
    data_path = os.getenv("HOSPITAL_DATA_PATH", "./data/hospital_knowledge")
    vector_db_path = os.getenv("VECTOR_DB_PATH", "./data/vector_db")
    
    print("🏥 Hospital AI Chatbot - Data Ingestion")
    print("=" * 50)
    
    # Load documents
    print(f"\nLoading documents from {data_path}...")
    documents = load_hospital_data(data_path)
    
    if not documents:
        print("No documents found. Please add PDFs or text files to the data directory.")
        return
    
    print(f"Loaded {len(documents)} document chunks")
    
    # Build RAG index
    print(f"\nBuilding RAG index...")
    rag_engine = RAGEngine(vector_db_path=vector_db_path)
    rag_engine.build_index(documents)
    
    print("\n✅ Data ingestion completed successfully!")
    print(f"RAG index saved to: {vector_db_path}")

if __name__ == "__main__":
    main()
