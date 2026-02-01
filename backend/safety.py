"""
Safety prompts and validation for the Hospital AI Chatbot.
Ensures the bot does not provide medical diagnosis or prescriptions.
"""

SYSTEM_PROMPT = """You are a helpful hospital assistant chatbot. Your role is to provide general information and workflow assistance only.

CRITICAL RULES:
1. You provide general information about:
   - Appointment booking procedures
   - Doctor and department information
   - OPD timings and schedules
   - Hospital services and facilities
   - Patient FAQs
   - Location and contact information
   - General emergency guidance (non-diagnostic)

2. You MUST NOT:
   - Provide medical diagnosis
   - Prescribe medications or treatments
   - Replace or substitute for medical professionals
   - Give specific medical advice based on symptoms
   - Make health-related recommendations beyond general information

3. For medical concerns:
   - Always advise users to consult with qualified medical professionals
   - For emergencies, direct users to contact emergency services immediately
   - Provide contact information for relevant departments

4. If asked about symptoms or medical conditions:
   - Acknowledge the concern
   - Provide general information if available
   - Strongly recommend consulting a doctor
   - Offer to help book an appointment

5. Always be helpful, empathetic, and professional.
6. Base your answers ONLY on the provided hospital knowledge base.
7. If information is not available, say so clearly.

Remember: You are an informational assistant, not a medical professional."""

EMERGENCY_KEYWORDS = [
    "chest pain", "heart attack", "stroke", "severe bleeding",
    "difficulty breathing", "unconscious", "severe injury",
    "overdose", "seizure", "severe allergic reaction"
]

def contains_emergency_keywords(message: str) -> bool:
    """Check if message contains emergency-related keywords."""
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in EMERGENCY_KEYWORDS)

def get_emergency_response() -> str:
    """Get standardized emergency response."""
    return """🚨 EMERGENCY ALERT 🚨

If this is a medical emergency, please:
1. Call emergency services immediately: 108 or your local emergency number
2. Go to the nearest emergency department
3. Do not delay seeking medical attention

For non-emergency medical concerns, please consult with our doctors. I can help you book an appointment."""

def validate_response(response: str) -> str:
    """Add safety disclaimer if response might be interpreted as medical advice."""
    medical_advice_indicators = [
        "you should take", "you need to", "prescribe", "diagnosis",
        "you have", "treatment for", "medication for"
    ]
    
    response_lower = response.lower()
    if any(indicator in response_lower for indicator in medical_advice_indicators):
        return response + "\n\n⚠️ Note: This is general information only. Please consult with a qualified medical professional for personalized advice."
    
    return response

