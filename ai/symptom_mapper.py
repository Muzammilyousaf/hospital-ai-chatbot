"""
Symptom and Disease to Department Mapping
Maps user symptoms/diseases to appropriate hospital departments
"""

from typing import Optional, List, Dict

# Comprehensive symptom and disease to department mapping
SYMPTOM_TO_DEPARTMENT: Dict[str, str] = {
    # Cardiovascular / Heart
    'chest pain': 'Cardiology',
    'heart': 'Cardiology',
    'heart attack': 'Cardiology',
    'hypertension': 'Cardiology',
    'high blood pressure': 'Cardiology',
    'palpitations': 'Cardiology',
    'shortness of breath': 'Cardiology',
    'breathing difficulty': 'Cardiology',
    'cardiac': 'Cardiology',
    'cardiovascular': 'Cardiology',
    'arrhythmia': 'Cardiology',
    'angina': 'Cardiology',
    'heartburn': 'Cardiology',  # Could also be GI, but often cardiac concern
    
    # Endocrine / Diabetes
    'diabetes': 'Endocrinology',
    'diabetic': 'Endocrinology',
    'thyroid': 'Endocrinology',
    'hormone': 'Endocrinology',
    'blood sugar': 'Endocrinology',
    'hypoglycemia': 'Endocrinology',
    'hyperglycemia': 'Endocrinology',
    'insulin': 'Endocrinology',
    'metabolic': 'Endocrinology',
    
    # Orthopedic / Bones & Joints
    'joint pain': 'Orthopedics',
    'bone': 'Orthopedics',
    'fracture': 'Orthopedics',
    'knee pain': 'Orthopedics',
    'back pain': 'Orthopedics',
    'arthritis': 'Orthopedics',
    'sprain': 'Orthopedics',
    'dislocation': 'Orthopedics',
    'shoulder pain': 'Orthopedics',
    'hip pain': 'Orthopedics',
    'ankle pain': 'Orthopedics',
    'wrist pain': 'Orthopedics',
    'sports injury': 'Orthopedics',
    'orthopedic': 'Orthopedics',
    
    # Gastrointestinal / Stomach
    'stomach pain': 'Gastroenterology',
    'stomach': 'Gastroenterology',
    'digestion': 'Gastroenterology',
    'nausea': 'Gastroenterology',
    'vomiting': 'Gastroenterology',
    'diarrhea': 'Gastroenterology',
    'constipation': 'Gastroenterology',
    'abdominal pain': 'Gastroenterology',
    'gastro': 'Gastroenterology',
    'ulcer': 'Gastroenterology',
    'acid reflux': 'Gastroenterology',
    'gerd': 'Gastroenterology',
    'ibs': 'Gastroenterology',
    'liver': 'Gastroenterology',
    'gallbladder': 'Gastroenterology',
    
    # Dermatology / Skin
    'skin': 'Dermatology',
    'rash': 'Dermatology',
    'allergy': 'Dermatology',
    'acne': 'Dermatology',
    'eczema': 'Dermatology',
    'psoriasis': 'Dermatology',
    'dermatitis': 'Dermatology',
    'hives': 'Dermatology',
    'mole': 'Dermatology',
    'wart': 'Dermatology',
    'dermatology': 'Dermatology',
    
    # Ophthalmology / Eyes
    'eye': 'Ophthalmology',
    'vision': 'Ophthalmology',
    'glaucoma': 'Ophthalmology',
    'cataract': 'Ophthalmology',
    'ophthalmology': 'Ophthalmology',
    'retina': 'Ophthalmology',
    'conjunctivitis': 'Ophthalmology',
    'pink eye': 'Ophthalmology',
    'dry eyes': 'Ophthalmology',
    'blurred vision': 'Ophthalmology',
    
    # Pediatrics / Children
    'child': 'Pediatrics',
    'baby': 'Pediatrics',
    'infant': 'Pediatrics',
    'pediatric': 'Pediatrics',
    'pediatrician': 'Pediatrics',
    'newborn': 'Pediatrics',
    'toddler': 'Pediatrics',
    
    # Neurology / Brain
    'headache': 'Neurology',
    'migraine': 'Neurology',
    'seizure': 'Neurology',
    'epilepsy': 'Neurology',
    'neurology': 'Neurology',
    'dizziness': 'Neurology',
    'vertigo': 'Neurology',
    'stroke': 'Neurology',
    'parkinson': 'Neurology',
    'tremor': 'Neurology',
    
    # Urology / Urinary
    'urinary': 'Urology',
    'kidney': 'Urology',
    'bladder': 'Urology',
    'urology': 'Urology',
    'uti': 'Urology',
    'urinary tract infection': 'Urology',
    'kidney stone': 'Urology',
    
    # ENT / Ear, Nose, Throat
    'ear': 'ENT',
    'nose': 'ENT',
    'throat': 'ENT',
    'sinus': 'ENT',
    'hearing': 'ENT',
    'tonsil': 'ENT',
    'laryngitis': 'ENT',
    'otolaryngology': 'ENT',
    
    # General Medicine / Common
    'fever': 'General Medicine',
    'cold': 'General Medicine',
    'flu': 'General Medicine',
    'cough': 'General Medicine',
    'sore throat': 'General Medicine',
    'fatigue': 'General Medicine',
    'weakness': 'General Medicine',
    'general': 'General Medicine',
    
    # Emergency / Critical
    'emergency': 'Emergency',
    'severe bleeding': 'Emergency',
    'unconscious': 'Emergency',
    'severe injury': 'Emergency',
    'overdose': 'Emergency',
    'severe allergic reaction': 'Emergency',
    'anaphylaxis': 'Emergency',
}

# Department synonyms for better matching
DEPARTMENT_SYNONYMS: Dict[str, str] = {
    'cardiology': 'Cardiology',
    'cardiac': 'Cardiology',
    'heart': 'Cardiology',
    'endocrinology': 'Endocrinology',
    'endocrine': 'Endocrinology',
    'orthopedics': 'Orthopedics',
    'orthopedic': 'Orthopedics',
    'bone': 'Orthopedics',
    'gastroenterology': 'Gastroenterology',
    'gastro': 'Gastroenterology',
    'stomach': 'Gastroenterology',
    'dermatology': 'Dermatology',
    'skin': 'Dermatology',
    'ophthalmology': 'Ophthalmology',
    'eye': 'Ophthalmology',
    'pediatrics': 'Pediatrics',
    'pediatric': 'Pediatrics',
    'neurology': 'Neurology',
    'urology': 'Urology',
    'ent': 'ENT',
    'ear nose throat': 'ENT',
    'general medicine': 'General Medicine',
    'general': 'General Medicine',
    'emergency': 'Emergency',
}

class SymptomMapper:
    """Maps symptoms and diseases to hospital departments."""
    
    def __init__(self):
        """Initialize symptom mapper."""
        self.symptom_map = SYMPTOM_TO_DEPARTMENT
        self.department_synonyms = DEPARTMENT_SYNONYMS
    
    def map_symptom_to_department(self, symptom_text: str) -> Optional[str]:
        """
        Map symptom/disease text to appropriate department.
        
        Args:
            symptom_text: User's symptom or disease description
            
        Returns:
            Department name or None if no match found
        """
        if not symptom_text:
            return None
        
        symptom_lower = symptom_text.lower().strip()
        
        # Check for exact symptom matches (prioritize longer phrases first)
        # Sort by length descending to match longer phrases first
        sorted_symptoms = sorted(self.symptom_map.items(), key=lambda x: len(x[0]), reverse=True)
        
        for symptom, department in sorted_symptoms:
            if symptom in symptom_lower:
                return department
        
        # Check for department synonyms (user might directly mention department)
        for synonym, department in self.department_synonyms.items():
            if synonym in symptom_lower:
                return department
        
        return None
    
    def extract_symptoms(self, text: str) -> List[str]:
        """
        Extract all symptoms mentioned in text.
        
        Args:
            text: User message text
            
        Returns:
            List of detected symptoms
        """
        text_lower = text.lower()
        detected_symptoms = []
        
        for symptom in self.symptom_map.keys():
            if symptom in text_lower:
                detected_symptoms.append(symptom)
        
        return detected_symptoms
    
    def get_recommended_department(self, text: str) -> Optional[Dict[str, any]]:
        """
        Get recommended department with confidence score.
        
        Args:
            text: User message text
            
        Returns:
            Dictionary with department, symptoms, and confidence, or None
        """
        symptoms = self.extract_symptoms(text)
        
        if not symptoms:
            return None
        
        # Count department matches
        department_counts = {}
        for symptom in symptoms:
            dept = self.symptom_map.get(symptom)
            if dept:
                department_counts[dept] = department_counts.get(dept, 0) + 1
        
        if not department_counts:
            return None
        
        # Get most common department
        recommended_dept = max(department_counts, key=department_counts.get)
        confidence = department_counts[recommended_dept] / len(symptoms)
        
        return {
            'department': recommended_dept,
            'symptoms': symptoms,
            'confidence': confidence,
            'match_count': department_counts[recommended_dept]
        }
    
    def suggest_doctors_for_symptom(self, text: str) -> Optional[str]:
        """
        Suggest department and doctors for a symptom.
        Used for generating user-friendly responses.
        
        Args:
            text: User message with symptoms
            
        Returns:
            Formatted suggestion string or None
        """
        recommendation = self.get_recommended_department(text)
        
        if not recommendation:
            return None
        
        dept = recommendation['department']
        symptoms = recommendation['symptoms']
        
        return f"Based on your symptoms ({', '.join(symptoms[:3])}), I recommend the **{dept}** department. Would you like to see available doctors in {dept}?"

