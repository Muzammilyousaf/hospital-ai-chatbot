"""
Entity Extraction using regex patterns (spaCy optional)
"""

from typing import Dict, Optional
import re
from ai.date_time_parser import NaturalDateTimeParser

# Try to import spaCy, but make it optional
try:
    import spacy
    SPACY_AVAILABLE = True
except (ImportError, Exception):
    SPACY_AVAILABLE = False
    spacy = None

class EntityExtractor:
    """Extract entities from user messages."""
    
    def __init__(self):
        """Initialize entity extractor."""
        self.nlp = None
        self.loaded = False
        self.date_time_parser = NaturalDateTimeParser()
        self._load_model()
    
    def _load_model(self):
        """Load spaCy model (optional)."""
        if not SPACY_AVAILABLE:
            print("spaCy not available - using regex-based entity extraction")
            self.loaded = False
            return
        
        try:
            # Try to load English model
            self.nlp = spacy.load("en_core_web_sm")
            self.loaded = True
            print("spaCy model loaded successfully")
        except (OSError, Exception) as e:
            print(f"Warning: Could not load spaCy model: {e}")
            print("Using regex-based entity extraction (works without spaCy)")
            self.loaded = False
    
    def extract(self, text: str, conversation_context: Optional[Dict] = None) -> Dict[str, Optional[str]]:
        """Extract entities from text using enhanced NER (spaCy + regex patterns)."""
        entities = {
            'doctor': None,
            'date': None,
            'time': None,
            'department': None,
            'patient_name': None,
            'phone': None
        }
        
        text_lower = text.lower()
        
        # Use spaCy if available (enhanced NER)
        if self.loaded and self.nlp and SPACY_AVAILABLE:
            try:
                doc = self.nlp(text)
                
                # Enhanced entity extraction with spaCy
                for ent in doc.ents:
                    # Person names (doctors or patients)
                    if ent.label_ == "PERSON":
                        # Check if it's a doctor (has "Dr." prefix or in doctor context)
                        if 'dr.' in text[:ent.start_char].lower() or 'doctor' in text[:ent.start_char].lower():
                            if not entities['doctor']:
                                entities['doctor'] = ent.text
                        elif not entities['patient_name']:
                            entities['patient_name'] = ent.text
                    
                    # Dates
                    elif ent.label_ == "DATE" and not entities['date']:
                        entities['date'] = ent.text
                    
                    # Times
                    elif ent.label_ == "TIME" and not entities['time']:
                        entities['time'] = ent.text
                    
                    # Organizations (departments)
                    elif ent.label_ == "ORG" and not entities['department']:
                        # Check if it's a medical department
                        dept_keywords = ['cardiology', 'orthopedics', 'pediatrics', 'emergency', 'medicine']
                        if any(keyword in ent.text.lower() for keyword in dept_keywords):
                            entities['department'] = ent.text
                    
                    # Phone numbers (if spaCy recognizes them)
                    elif ent.label_ == "PHONE" and not entities['phone']:
                        entities['phone'] = ent.text
                
            except Exception as e:
                print(f"spaCy extraction error: {e}")
                pass  # Fall back to regex if spaCy fails
        
        # Primary extraction method: Regex patterns (always works)
        
        # Extract doctor name - Enhanced patterns (prioritize "Dr. Name" format)
        if not entities['doctor']:
            # Pattern 1: "Dr. John Smith" or "Dr John Smith" (PRIORITY - most common format)
            doctor_match = re.search(r'\bdr\.?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', text, re.IGNORECASE)
            if doctor_match:
                potential_name = doctor_match.group(0)
                # Don't extract if it's part of a question about address/location
                if not any(word in text_lower for word in ['address', 'location', 'where', 'located']):
                    entities['doctor'] = potential_name
            
            # Pattern 2: "go to doctor Sarah Johnson" or "see doctor John Smith" or "book with Dr. Sarah"
            if not entities['doctor']:
                pattern2 = re.search(r'(?:go to|see|visit|with|book.*with)\s+(?:doctor|dr\.?)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', text, re.IGNORECASE)
                if pattern2:
                    potential_name = pattern2.group(1)
                    if not potential_name.lower().startswith('dr'):
                        entities['doctor'] = f"Dr. {potential_name}"
                    else:
                        entities['doctor'] = potential_name
            
            # Pattern 3: Name after explicit "with/for" (e.g., "book appointment with Sarah Johnson")
            if not entities['doctor']:
                pattern3 = re.search(r'(?:book|appointment|schedule).*?(?:with|for)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', text, re.IGNORECASE)
                if pattern3:
                    potential_name = pattern3.group(1)
                    # Make sure it's not a common word or booking phrase
                    stop_words = {'appointment', 'book', 'schedule', 'an', 'the', 'a', 'for', 'with'}
                    tokens = [t.lower() for t in potential_name.split()]
                    if not any(token in stop_words for token in tokens) and 'appointment' not in potential_name.lower():
                        entities['doctor'] = f"Dr. {potential_name}"
            
            # Pattern 4: "Sarah Johnson - Orthopedics: Dr." (LAST - only if no other pattern matched)
            # This is usually from bot responses, not user input
            if not entities['doctor']:
                pattern4 = re.search(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*-\s*[A-Za-z]+(?:\s*:\s*Dr\.?)?', text)
                if pattern4:
                    potential_name = pattern4.group(1)
                    # Only use this if it looks like user is selecting from a list
                    if any(word in text_lower for word in ['this', 'that', 'one', 'select', 'choose']):
                        if not potential_name.lower().startswith('dr'):
                            entities['doctor'] = f"Dr. {potential_name}"
                        else:
                            entities['doctor'] = potential_name
        
        # Extract date using natural language parser (prioritize this)
        if not entities['date']:
            parsed_date = self.date_time_parser.parse_date(text)
            if parsed_date:
                entities['date'] = parsed_date
        
        # Fallback to regex patterns if natural parser didn't find anything
        if not entities['date']:
            date_patterns = [
                r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD (preferred format)
                r'\d{2}/\d{2}/\d{4}',   # MM/DD/YYYY
                r'\d{2}-\d{2}-\d{4}',   # DD-MM-YYYY
                r'\d{4}/\d{2}/\d{2}',   # YYYY/MM/DD
            ]
            for pattern in date_patterns:
                date_match = re.search(pattern, text, re.IGNORECASE)
                if date_match:
                    # Normalize the date format
                    normalized = self.date_time_parser.normalize_date(date_match.group(0))
                    if normalized:
                        entities['date'] = normalized
                    else:
                        entities['date'] = date_match.group(0)
                    break
        
        # Extract time using natural language parser (prioritize this)
        if not entities['time']:
            parsed_time = self.date_time_parser.parse_time(text)
            if parsed_time:
                entities['time'] = parsed_time
        
        # Fallback to regex patterns if natural parser didn't find anything
        if not entities['time']:
            time_patterns = [
                r'\d{1,2}:\d{2}(?:\s*(?:AM|PM|am|pm))?',  # 12:30 or 12:30 PM (preferred)
                r'\d{1,2}:\d{2}',  # 12:30 (just time)
                r'\d{1,2}\s*(?:AM|PM|am|pm)',  # 12 PM
            ]
            for pattern in time_patterns:
                time_match = re.search(pattern, text, re.IGNORECASE)
                if time_match:
                    time_str = time_match.group(0)
                    # Normalize to HH:MM format
                    normalized = self.date_time_parser.normalize_time(time_str)
                    if normalized:
                        entities['time'] = normalized
                    elif ':' in time_str:
                        entities['time'] = time_str
                    break
        
        # Extract department keywords (enhanced) with word boundaries
        if not entities['department']:
            departments = {
                'cardiology': 'Cardiology',
                'orthopedics': 'Orthopedics',
                'orthopedic': 'Orthopedics',
                'pediatrics': 'Pediatrics',
                'pediatric': 'Pediatrics',
                'general medicine': 'General Medicine',
                'emergency': 'Emergency',
                'emergency department': 'Emergency',
                'cardiac': 'Cardiology',
                'heart': 'Cardiology',
                'bone': 'Orthopedics',
                'child': 'Pediatrics',
                'ent': 'ENT'
            }
            for dept_key, dept_name in departments.items():
                pattern = r'\b' + re.escape(dept_key) + r'\b'
                if re.search(pattern, text_lower):
                    entities['department'] = dept_name
                    break
        
        # Extract phone numbers (enhanced regex)
        if not entities['phone']:
            phone_patterns = [
                r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # US format
                r'\d{10}',  # 10 digits
                r'\+?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}',  # International
            ]
            for pattern in phone_patterns:
                phone_match = re.search(pattern, text)
                if phone_match:
                    entities['phone'] = phone_match.group(0)
                    break
        
        # Use conversation context to fill missing entities
        if conversation_context:
            last_entities = conversation_context.get('last_entities', {})
            # Avoid carrying department into booking/doctor-specific turns
            has_booking_words = any(word in text_lower for word in ['book', 'appointment', 'schedule', 'reserve'])
            has_doctor_mention = bool(re.search(r'\bdr\.?\s+[A-Z][a-z]+', text, re.IGNORECASE))
            for key in ['doctor', 'date', 'time', 'department']:
                if not entities[key] and last_entities.get(key):
                    if key == 'department' and (has_booking_words or has_doctor_mention):
                        continue
                    entities[key] = last_entities[key]
        
        return entities
    
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self.loaded
