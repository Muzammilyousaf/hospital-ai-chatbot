"""
Enhanced Intent Classification using PyTorch (DistilBERT) + Embeddings Similarity
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

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import Optional
import re

class IntentClassifier:
    """Enhanced intent classifier using DistilBERT + embeddings similarity."""
    
    INTENTS = [
        'greeting',
        'appointment_booking',
        'doctor_info',
        'services',
        'faq',
        'emergency',
        'location',
        'timings',
        'contact',
        'symptom_query',  # New intent for symptom-based queries
        'cancel_appointment'  # New intent for appointment cancellation
    ]
    
    # Intent examples for similarity matching
    INTENT_EXAMPLES = {
        'greeting': [
            'hello', 'hi', 'hey', 'good morning', 'good afternoon', 'greetings',
            'hi there', 'hello there', 'how are you', 'what\'s up'
        ],
        'appointment_booking': [
            'book appointment', 'schedule appointment', 'make appointment',
            'book with doctor', 'appointment booking', 'reserve appointment',
            'i want appointment', 'need appointment', 'set appointment'
        ],
        'doctor_info': [
            'doctor names', 'list doctors', 'available doctors', 'who are doctors',
            'doctor information', 'which doctors', 'show doctors', 'doctor list',
            'tell me doctors', 'what doctors available'
        ],
        'services': [
            'what services', 'hospital services', 'what do you offer',
            'facilities', 'departments', 'services available', 'what facilities'
        ],
        'emergency': [
            'emergency', 'urgent', 'critical', 'immediate help', 'emergency services',
            'need emergency', 'urgent care', 'critical situation'
        ],
        'location': [
            'address', 'location', 'where are you', 'where located', 'find hospital',
            'hospital address', 'your address', 'where is hospital'
        ],
        'timings': [
            'opd timings', 'opening hours', 'timings', 'when open', 'opening time',
            'closing time', 'hours', 'schedule', 'opd hours'
        ],
        'contact': [
            'contact', 'phone number', 'call', 'phone', 'email', 'contact details',
            'how to contact', 'reach us', 'contact information'
        ],
        'symptom_query': [
            'i have', 'i am suffering', 'i feel', 'symptom', 'pain', 'problem',
            'issue', 'disease', 'condition', 'diagnosis', 'what department',
            'which department', 'where should i go'
        ]
    }
    
    def __init__(self):
        """Initialize the intent classifier."""
        self.model = None
        self.tokenizer = None
        self.embedding_model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.loaded = False
        self.embeddings_loaded = False
        self.intent_embeddings = {}
        self._load_models()
    
    def _load_models(self):
        """Load intent classification and embedding models."""
        # Load embedding model for similarity matching
        try:
            # Suppress warnings during model loading
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
                self.embeddings_loaded = True
                
                # Pre-compute embeddings for intent examples
                for intent, examples in self.INTENT_EXAMPLES.items():
                    self.intent_embeddings[intent] = self.embedding_model.encode(examples)
                
                print("✅ Embedding model loaded for intent classification")
        except Exception as e:
            print(f"⚠️ Warning: Could not load embedding model: {e}")
            self.embeddings_loaded = False
        
        # Try to load DistilBERT (optional, for future fine-tuning)
        try:
            model_name = "distilbert-base-uncased"
            # Suppress warnings during model loading
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.model = AutoModelForSequenceClassification.from_pretrained(
                    model_name,
                    num_labels=len(self.INTENTS)
                )
                self.model.eval()
                self.model.to(self.device)
                self.loaded = True
                print("✅ DistilBERT model loaded (for future fine-tuning)")
        except Exception as e:
            print(f"ℹ️ Note: DistilBERT not loaded: {e}")
            print("Using enhanced keyword + embedding-based classification")
            self.loaded = False
    
    def _calculate_similarity(self, text: str, intent: str) -> float:
        """Calculate similarity score between text and intent examples."""
        if not self.embeddings_loaded or intent not in self.intent_embeddings:
            return 0.0
        
        try:
            text_embedding = self.embedding_model.encode([text])
            intent_embeddings = self.intent_embeddings[intent]
            
            # Calculate cosine similarity
            similarities = np.dot(intent_embeddings, text_embedding.T).flatten()
            max_similarity = float(np.max(similarities))
            
            return max_similarity
        except Exception:
            return 0.0
    
    def classify(self, text: str, conversation_context: Optional[str] = None) -> str:
        """Classify user intent with enhanced ML-based approach."""
        text_lower = text.lower().strip()
        
        # Combine with conversation context if available
        if conversation_context:
            full_text = f"{conversation_context} {text_lower}"
        else:
            full_text = text_lower
        
        # Pattern-based detection (fast, high confidence)
        has_doctor = bool(re.search(r'dr\.?\s+[A-Z][a-z]+', text, re.IGNORECASE))
        has_date = bool(re.search(r'\d{4}-\d{2}-\d{2}', text))
        has_time = bool(re.search(r'\d{1,2}:\d{2}', text))
        
        if has_doctor and has_date and has_time:
            return 'appointment_booking'
        
        # Greeting detection (check first, high priority)
        greeting_words = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening', 
                         'greetings', 'hi there', 'hello there', 'hey there', 'howdy', 'sup', 'hii',
                         'how are you', 'what\'s up', 'hey there']
        if any(word in text_lower for word in greeting_words) or text_lower in greeting_words:
            return 'greeting'
        
        # Emergency detection (high priority)
        if any(word in text_lower for word in ['emergency', 'urgent', 'critical', 'immediate', 'help now']):
            return 'emergency'
        
        # Use embedding similarity for better classification
        if self.embeddings_loaded:
            intent_scores = {}
            for intent in self.INTENTS:
                # Combine pattern matching and similarity
                pattern_score = 0.0
                similarity_score = self._calculate_similarity(text, intent)
                
                # Pattern matching boost
                if intent == 'appointment_booking':
                    pattern_score = 1.0 if any(word in text_lower for word in ['book', 'appointment', 'schedule', 'reserve', 'appoint']) else 0.0
                elif intent == 'doctor_info':
                    pattern_score = 1.0 if any(word in text_lower for word in ['doctor', 'physician', 'specialist']) else 0.0
                elif intent == 'services':
                    pattern_score = 1.0 if any(word in text_lower for word in ['service', 'facility', 'department', 'offer']) else 0.0
                elif intent == 'location':
                    pattern_score = 1.0 if any(word in text_lower for word in ['address', 'location', 'where', 'located']) else 0.0
                elif intent == 'timings':
                    pattern_score = 1.0 if any(word in text_lower for word in ['timing', 'time', 'opd', 'open', 'close', 'hour']) else 0.0
                elif intent == 'contact':
                    pattern_score = 1.0 if any(word in text_lower for word in ['contact', 'phone', 'call', 'email', 'number']) else 0.0
                
                # Combined score (pattern has higher weight)
                intent_scores[intent] = (pattern_score * 0.7) + (similarity_score * 0.3)
            
            # Get intent with highest score
            best_intent = max(intent_scores, key=intent_scores.get)
            best_score = intent_scores[best_intent]
            
            # Only use ML result if confidence is high enough
            if best_score > 0.3:
                return best_intent
        
        # Fallback to keyword-based classification
        if any(word in text_lower for word in ['book', 'appointment', 'schedule', 'reserve', 'appoint']):
            return 'appointment_booking'
        
        if any(word in text_lower for word in ['doctor', 'physician', 'specialist']):
            return 'doctor_info'
        
        if any(word in text_lower for word in ['service', 'facility', 'department', 'offer']):
            return 'services'
        
        if any(word in text_lower for word in ['address', 'location', 'where', 'located']):
            return 'location'
        
        if any(word in text_lower for word in ['timing', 'time', 'opd', 'open', 'close', 'hour']):
            return 'timings'
        
        if any(word in text_lower for word in ['contact', 'phone', 'call', 'email']):
            return 'contact'
        
        # Symptom query detection
        symptom_keywords = ['have', 'suffering', 'feeling', 'pain', 'problem', 'issue', 'symptom', 'disease']
        if any(keyword in text_lower for keyword in symptom_keywords):
            # Check if it's a symptom query (not just appointment booking)
            if not any(word in text_lower for word in ['appointment', 'book', 'schedule']):
                return 'symptom_query'
        
        # Default to FAQ
        return 'faq'
    
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self.loaded or self.embeddings_loaded

