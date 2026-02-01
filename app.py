"""
Flask application for Hospital AI Chatbot
PyTorch + Flask + RAG (100% Free, No Paid APIs)
"""

import warnings
import os

# Suppress warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*Pydantic.*')
warnings.filterwarnings('ignore', message='.*HF Hub.*')
warnings.filterwarnings('ignore', message='.*UNEXPECTED.*')
warnings.filterwarnings('ignore', message='.*MISSING.*')

# Suppress HuggingFace warnings
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import uuid
import traceback
import re
from ai.intent_model import IntentClassifier
from ai.rag_engine import RAGEngine
from ai.entity_extractor import EntityExtractor
from ai.conversation_memory import ConversationMemory
from ai.symptom_mapper import SymptomMapper
from database.db import init_db, get_db_connection
from database.schema import create_tables
from database.availability import AvailabilityChecker

app = Flask(__name__)
CORS(app)

# Initialize database
print("📊 Initializing database...")
init_db()
create_tables()
print("✅ Database initialized")

# Initialize AI components (with suppressed warnings)
print("🤖 Loading AI models...")
intent_classifier = IntentClassifier()
rag_engine = RAGEngine()
entity_extractor = EntityExtractor()
conversation_memory = ConversationMemory(session_timeout_minutes=30)
symptom_mapper = SymptomMapper()
availability_checker = AvailabilityChecker()
print("✅ AI components loaded")

@app.route('/')
def index():
    """Main chat interface."""
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat endpoint with AI processing - Enhanced with conversation memory and error handling."""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        if not user_message:
            return jsonify({
                'error': 'Message cannot be empty',
                'success': False
            }), 400
        
        # Get conversation context
        conversation_summary = conversation_memory.get_conversation_summary(session_id)
        last_intent = conversation_memory.get_last_intent(session_id)
        last_entities = conversation_memory.get_last_entities(session_id)
        
        # 1. Enhanced Intent Classification (with conversation context)
        try:
            intent = intent_classifier.classify(user_message, conversation_context=conversation_summary)
        except Exception as e:
            print(f"Intent classification error: {e}")
            # Fallback to simple classification
            intent = 'faq'
        
        # Check if this is a follow-up question
        is_follow_up = conversation_memory.is_follow_up(session_id, intent)
        
        # 2. Enhanced Entity Extraction (with conversation context)
        try:
            context_dict = {
                'last_entities': last_entities or {},
                'last_intent': last_intent
            }
            entities = entity_extractor.extract(user_message, conversation_context=context_dict)
        except Exception as e:
            print(f"Entity extraction error: {e}")
            entities = {'doctor': None, 'date': None, 'time': None, 'department': None}
        
        # 3. Enhanced RAG Search with relevance filtering
        context = ""
        try:
            # Skip RAG for:
            # 1. Appointment booking requests (even without all details)
            # 2. User mentions a specific doctor name
            # 3. Simple follow-up responses like "yes", "ok"
            # 4. Doctor info queries with specific names
            user_lower_msg = user_message.lower().strip()
            has_doctor_name = entities.get('doctor') or re.search(r'\bdr\.?\s+[A-Z][a-z]+', user_message, re.IGNORECASE)
            is_simple_response = user_lower_msg in ['yes', 'ok', 'okay', 'sure', 'no', 'nope', 'yeah']
            is_booking = intent == 'appointment_booking' or 'book' in user_lower_msg or ('appointment' in user_lower_msg and len(user_message.split()) < 5)
            is_hospital_info = any(phrase in user_lower_msg for phrase in ['hospital information', 'hospital info', 'about hospital', 'about the hospital', 'overview', 'details', 'all information', 'everything about'])
            
            skip_rag = (
                is_booking or
                is_simple_response or
                is_hospital_info or
                (has_doctor_name and intent == 'doctor_info') or
                (has_doctor_name and 'book' in user_lower_msg)
            )
            
            if not skip_rag:
                # Use enhanced RAG with relevance scoring
                context = rag_engine.search(user_message, top_k=2, min_relevance=0.3)
        except Exception as e:
            print(f"RAG search error: {e}")
            context = ""
        
        # 4. Business Logic & Response Generation (with multi-turn support)
        try:
            response = generate_response(
                intent, entities, context, user_message,
                conversation_context={
                    'session_id': session_id,
                    'is_follow_up': is_follow_up,
                    'last_intent': last_intent,
                    'last_entities': last_entities,
                    'conversation_summary': conversation_summary
                }
            )
        except Exception as e:
            print(f"Response generation error: {e}")
            traceback.print_exc()
            response = "I apologize, but I'm having trouble processing your request. Could you please rephrase it?"
        
        # Store conversation in memory
        try:
            conversation_memory.add_message(session_id, 'user', user_message, intent, entities)
            conversation_memory.add_message(session_id, 'assistant', response, intent, None)
        except Exception as e:
            print(f"Memory storage error: {e}")
        
        # Cleanup expired sessions periodically
        try:
            conversation_memory.cleanup_expired_sessions()
        except Exception:
            pass
        
        return jsonify({
            'reply': response,
            'intent': intent,
            'entities': entities,
            'session_id': session_id,
            'is_follow_up': is_follow_up,
            'success': True
        })
    
    except Exception as e:
        print(f"Chat endpoint error: {e}")
        traceback.print_exc()
        return jsonify({
            'reply': 'I apologize, but I encountered an unexpected error. Please try again or contact support.',
            'success': False,
            'error': str(e) if app.debug else None
        }), 500

@app.route('/api/book', methods=['POST'])
def book_appointment():
    """Book an appointment."""
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO appointments (patient_name, doctor_id, date, time, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data.get('patient_name'),
            data.get('doctor_id'),
            data.get('date'),
            data.get('time'),
            'scheduled'
        ))
        
        conn.commit()
        appointment_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'status': 'success',
            'appointment_id': appointment_id,
            'message': f'Appointment booked successfully! ID: {appointment_id}'
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    """Get list of doctors - Enhanced with error handling."""
    try:
        department_id = request.args.get('department_id')
        conn = get_db_connection()
        
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            cursor = conn.cursor()
            
            if department_id:
                cursor.execute('''
                    SELECT id, name, specialization, availability 
                    FROM doctors 
                    WHERE department_id = ?
                ''', (department_id,))
            else:
                cursor.execute('''
                    SELECT id, name, specialization, availability 
                    FROM doctors
                ''')
            
            doctors = [{
                'id': row[0],
                'name': row[1],
                'specialization': row[2],
                'availability': row[3]
            } for row in cursor.fetchall()]
            
            conn.close()
            return jsonify({'doctors': doctors})
        
        except Exception as db_error:
            if conn:
                conn.close()
            print(f"Database error in get_doctors: {db_error}")
            traceback.print_exc()
            return jsonify({'error': 'Failed to retrieve doctors'}), 500
    
    except Exception as e:
        print(f"Error in get_doctors: {e}")
        traceback.print_exc()
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/api/departments', methods=['GET'])
def get_departments():
    """Get list of departments - Enhanced with error handling."""
    try:
        conn = get_db_connection()
        
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, description FROM departments')
            
            departments = [{
                'id': row[0],
                'name': row[1],
                'description': row[2]
            } for row in cursor.fetchall()]
            
            conn.close()
            return jsonify({'departments': departments})
        
        except Exception as db_error:
            if conn:
                conn.close()
            print(f"Database error in get_departments: {db_error}")
            traceback.print_exc()
            return jsonify({'error': 'Failed to retrieve departments'}), 500
    
    except Exception as e:
        print(f"Error in get_departments: {e}")
        traceback.print_exc()
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'rag_loaded': rag_engine.is_loaded(),
        'intent_model_loaded': intent_classifier.is_loaded()
    })

@app.route('/api/cancel', methods=['POST'])
def cancel_appointment():
    """Cancel an appointment - Enhanced with error handling."""
    try:
        data = request.json
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No data provided'
            }), 400
        
        appointment_id = data.get('appointment_id')
        patient_name = data.get('patient_name')
        phone = data.get('phone')
        
        if not appointment_id and not patient_name:
            return jsonify({
                'status': 'error',
                'message': 'Please provide either appointment_id or patient_name'
            }), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'status': 'error',
                'message': 'Database connection failed'
            }), 500
        
        try:
            cursor = conn.cursor()
            
            # Find appointment
            if appointment_id:
                cursor.execute('''
                    SELECT id, patient_name, doctor_id, date, time, status
                    FROM appointments
                    WHERE id = ? AND status IN ('scheduled', 'confirmed')
                ''', (appointment_id,))
            elif patient_name:
                # Find most recent appointment for patient
                cursor.execute('''
                    SELECT id, patient_name, doctor_id, date, time, status
                    FROM appointments
                    WHERE patient_name = ? AND status IN ('scheduled', 'confirmed')
                    ORDER BY date DESC, time DESC
                    LIMIT 1
                ''', (patient_name,))
            else:
                conn.close()
                return jsonify({
                    'status': 'error',
                    'message': 'Please provide appointment_id or patient_name'
                }), 400
            
            appointment = cursor.fetchone()
            
            if not appointment:
                conn.close()
                return jsonify({
                    'status': 'error',
                    'message': 'No active appointment found. The appointment may have already been cancelled or does not exist.'
                }), 404
            
            appt_id, appt_patient, appt_doctor_id, appt_date, appt_time, appt_status = appointment
            
            # Get doctor name
            cursor.execute('SELECT name FROM doctors WHERE id = ?', (appt_doctor_id,))
            doctor = cursor.fetchone()
            doctor_name = doctor[0] if doctor else 'Unknown Doctor'
            
            # Cancel appointment
            cursor.execute('''
                UPDATE appointments
                SET status = 'cancelled'
                WHERE id = ?
            ''', (appt_id,))
            
            conn.commit()
            conn.close()
            
            return jsonify({
                'status': 'success',
                'message': f'Appointment cancelled successfully',
                'appointment_details': {
                    'id': appt_id,
                    'doctor': doctor_name,
                    'date': appt_date,
                    'time': appt_time
                }
            })
        
        except Exception as db_error:
            if conn:
                conn.rollback()
                conn.close()
            print(f"Database error in cancel_appointment: {db_error}")
            traceback.print_exc()
            return jsonify({
                'status': 'error',
                'message': 'Failed to cancel appointment. Please try again.'
            }), 500
    
    except Exception as e:
        print(f"Cancel appointment error: {e}")
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': 'An unexpected error occurred. Please try again.'
        }), 500

def generate_response(intent, entities, context, user_message, conversation_context=None):
    """Generate response based on intent, entities, and context - Enhanced with multi-turn support."""
    
    # Handle conversation context for multi-turn conversations
    if conversation_context:
        is_follow_up = conversation_context.get('is_follow_up', False)
        last_intent = conversation_context.get('last_intent')
        last_entities = conversation_context.get('last_entities', {})
        
        # If this is a follow-up to appointment booking, merge entities
        if is_follow_up and last_intent == 'appointment_booking':
            # Fill in missing entities from previous conversation
            for key in ['doctor', 'date', 'time', 'department']:
                if not entities.get(key) and last_entities.get(key):
                    entities[key] = last_entities[key]
        
        # Handle follow-up questions (e.g., "yes", "ok", "that works")
        if is_follow_up and (intent == 'faq' or user_message.lower().strip() in ['yes', 'ok', 'okay', 'sure', 'that works', 'yes please']):
            # If previous intent was appointment_booking, continue that flow
            if last_intent == 'appointment_booking':
                intent = 'appointment_booking'
                # Try to extract any new entities from current message
                if not entities.get('doctor') and last_entities.get('doctor'):
                    entities['doctor'] = last_entities['doctor']
                if not entities.get('date') and last_entities.get('date'):
                    entities['date'] = last_entities['date']
                if not entities.get('time') and last_entities.get('time'):
                    entities['time'] = last_entities['time']
            # If previous response was a doctor search result, treat "yes" as booking request
            elif last_intent == 'doctor_info' and last_entities.get('doctor'):
                # User selected a doctor from search results
                intent = 'appointment_booking'
                entities['doctor'] = last_entities['doctor']
    
    # Greeting handling
    if intent == 'greeting':
        return get_greeting_response()
    
    # Emergency handling (highest priority)
    if intent == 'emergency':
        return "🚨 EMERGENCY ALERT 🚨\n\nPlease contact the hospital emergency department immediately or call local emergency services. Do not delay seeking medical attention."

    # Appointment cancellation - detect before booking keywords
    if intent == 'cancel_appointment' or any(word in user_message.lower() for word in ['cancel', 'reschedule', 'change appointment']):
        return handle_appointment_cancellation(user_message, entities, conversation_context)

    # Direct booking instructions
    user_lower = user_message.lower()
    if any(phrase in user_lower for phrase in ['how do i book', 'how to book', 'how can i book', 'book an appointment?']):
        return get_booking_instructions()

    # Appointment booking - handle early to avoid misrouting to departments
    booking_keywords = any(word in user_lower for word in ['book', 'appointment', 'schedule', 'reserve'])
    if intent == 'appointment_booking' or booking_keywords:
        return handle_appointment_booking_flow(user_message, entities, conversation_context)
    
    # Symptom-based department recommendation (check early)
    symptom_recommendation = symptom_mapper.get_recommended_department(user_message)
    if symptom_recommendation and symptom_recommendation['confidence'] > 0.3:
        department = symptom_recommendation['department']
        symptoms = symptom_recommendation['symptoms']
        
        # If user is asking about symptoms, provide department recommendation
        if any(word in user_message.lower() for word in ['have', 'suffering', 'feeling', 'pain', 'problem', 'issue', 'symptom']):
            response = f"Based on your symptoms ({', '.join(symptoms[:3])}), I recommend the **{department}** department.\n\n"
            response += "⚠️ **Important:** I provide general information only. Please consult with a qualified doctor for proper diagnosis and treatment.\n\n"
            response += "Would you like to see available doctors in " + department + "?"
            return response
    
    # Department query handling (check before doctor_info)
    if entities.get('department') and not booking_keywords and not entities.get('doctor'):
        department = entities['department']
        return get_doctors_by_department(department)
    
    # Check if user is asking about a department by name
    user_lower = user_message.lower().strip()
    departments = ['cardiology', 'orthopedics', 'pediatrics', 'general medicine', 'emergency', 
                   'endocrinology', 'dermatology', 'gastroenterology', 'ophthalmology', 'neurology', 'urology', 'ent']
    for dept in departments:
        pattern = r'\b' + re.escape(dept) + r'\b'
        if re.search(pattern, user_lower) and len(user_lower) < 50 and not booking_keywords and not entities.get('doctor'):
            return get_doctors_by_department(dept.title())
    
    # Check if it's a simple name search (like "john" or "smith")
    # If it's a single word that looks like a name, try searching for doctors
    simple_name = user_message.strip()
    if len(simple_name.split()) == 1 and simple_name.isalpha() and len(simple_name) >= 2:
        # Check if it matches any doctor name (case-insensitive)
        search_result = search_doctors_by_name(simple_name)
        if "Found" in search_result and ("doctors matching" in search_result or "doctor matching" in search_result):
            return search_result
    
    # Doctor information - extract only doctor names
    # BUT: Skip if this is clearly an appointment booking request
    user_lower_msg = user_message.lower()
    is_booking_msg = 'book' in user_lower_msg or ('appointment' in user_lower_msg and len(user_message.split()) < 6)
    
    if not is_booking_msg and (intent == 'doctor_info' or ('doctor' in user_lower_msg and intent != 'appointment_booking')):
        # Check if asking for doctor names/suggestions
        if any(word in user_lower_msg for word in ['name', 'suggest', 'list', 'available', 'who', 'which']):
            return get_doctor_names_formatted()
        
        # Check if user provided a name (could be first name, last name, or full name)
        if entities.get('doctor'):
            doctor_name = entities['doctor']
            # Check if it's a search query (partial name) or specific doctor query
            if any(word in user_lower_msg for word in ['search', 'find', 'look for', 'show me']):
                return search_doctors_by_name(doctor_name)
            # ALWAYS use database query for specific doctor info
            return get_doctor_info(doctor_name)
        
        # Check if the message itself is a doctor name (like "Dr. Sarah Johnson" or "Sarah Johnson")
        # This handles cases where user selects a doctor from search results
        name_pattern = re.match(r'^(?:dr\.?\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)$', user_message.strip(), re.IGNORECASE)
        if name_pattern:
            doctor_name = user_message.strip()
            # If it doesn't start with Dr., add it
            if not doctor_name.lower().startswith('dr'):
                doctor_name = f"Dr. {doctor_name}"
            # Use database query, not RAG
            return get_doctor_info(doctor_name)
        
        # Check if the message itself is a simple name (like "John" or "Smith")
        # Simple names (1-2 words, capitalized or lowercase)
        name_pattern2 = re.match(r'^[A-Za-z]+(?:\s+[A-Z][a-z]+)?$', user_message.strip())
        if name_pattern2 and len(user_message.strip().split()) <= 2:
            # Check if it's a search query
            if any(word in user_lower_msg for word in ['search', 'find', 'look for', 'show me']):
                return search_doctors_by_name(user_message.strip())
            # Try search first (returns all matches), fallback to specific doctor
            search_result = search_doctors_by_name(user_message.strip())
            if "found" in search_result.lower() and "doctors" in search_result.lower():
                return search_result
            return get_doctor_info(user_message.strip())
        
        return get_doctor_names_formatted()
    
    # Appointment cancellation handled earlier

    # Location/Address - specific handling (check early)
    if any(word in user_message.lower() for word in ['address', 'location', 'where', 'located', 'find you']):
        return get_location_response()
    
    # Location/Address - specific handling (MUST check early, before other handlers)
    user_lower = user_message.lower()
    if any(word in user_lower for word in ['address', 'location', 'where', 'located', 'find you', 'your address']):
        return get_location_response()
    
    # OPD Timings - specific handling (check before FAQ)
    if any(word in user_lower for word in ['timing', 'time', 'opd', 'open', 'close', 'hour', 'when']):
        return get_opd_timings_response(context)
    
    # Services
    if intent == 'services':
        return get_services_response()

    # Hospital overview / information
    if any(phrase in user_message.lower() for phrase in ['hospital information', 'hospital info', 'about hospital', 'about the hospital', 'overview', 'details', 'all information', 'everything about']):
        return get_hospital_overview()
    
    # FAQ - use RAG context but extract only relevant parts
    if intent == 'faq':
        if context:
            # Extract only the relevant answer, not entire context
            relevant_answer = extract_relevant_answer(context, user_message)
            if relevant_answer and len(relevant_answer) > 50:
                return format_faq_response(relevant_answer, user_message)
        return generate_natural_response(user_message)
    
    # Default - use RAG context ONLY if it's safe and relevant
    # Double-check for common queries (in case they weren't caught earlier)
    user_lower = user_message.lower()
    
    # Check for location/address FIRST
    if any(word in user_lower for word in ['address', 'location', 'where', 'located', 'find you', 'your address']):
        return get_location_response()
    
    # Check for OPD timing
    if any(word in user_lower for word in ['timing', 'time', 'opd', 'open', 'close', 'hour', 'when']):
        return get_opd_timings_response(None)
    
    # NEVER use RAG context if it contains malformed doctor info
    # Check if context has incomplete doctor lines like "Name - Department: Dr."
    if context:
        # Check for malformed patterns in context
        has_malformed = re.search(r'[A-Z][a-z]+\s+[A-Z][a-z]+\s*-\s*[A-Za-z]+\s*:\s*Dr\.\s*$', context, re.MULTILINE)
        if has_malformed:
            # Don't use this context, it's corrupted
            context = ""
    
    if context and len(context.strip()) > 20:
        relevant_info = extract_relevant_answer(context, user_message)
        # If extract_relevant_answer returns None for specific queries, use direct answer
        if relevant_info is None:
            # Check what type of query it was
            if any(word in user_lower for word in ['timing', 'time', 'opd']):
                return get_opd_timings_response(None)
            if any(word in user_lower for word in ['address', 'location', 'where']):
                return get_location_response()
        # Only use relevant_info if it's substantial and doesn't contain malformed data
        if relevant_info and len(relevant_info) > 30:
            # Double-check for malformed patterns
            if not re.search(r'[A-Z][a-z]+\s+[A-Z][a-z]+\s*-\s*[A-Za-z]+\s*:\s*Dr\.\s*$', relevant_info, re.MULTILINE):
                return format_faq_response(relevant_info, user_message)
    
    # If no valid context, try to understand the question naturally
    return generate_natural_response(user_message)

def get_doctors_by_department(department_name):
    """Get doctors in a specific department."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT d.name, d.specialization, dept.name as department
            FROM doctors d
            LEFT JOIN departments dept ON d.department_id = dept.id
            WHERE dept.name LIKE ? OR dept.name = ?
            ORDER BY d.name
        ''', (f'%{department_name}%', department_name))
        
        doctors = cursor.fetchall()
        conn.close()
        
        if not doctors:
            return f"I couldn't find any doctors in the {department_name} department. Please check the department name or contact our reception desk."
        
        response = f"Doctors in {department_name}:\n\n"
        for doctor in doctors:
            response += f"• {doctor[0]} - {doctor[1] or 'Specialist'}\n"
        
        response += f"\nWould you like to book an appointment with any of these doctors?"
        return response
    except Exception as e:
        print(f"Error in get_doctors_by_department: {e}")
        return f"I apologize, but I encountered an error retrieving department information."

def get_doctor_names_formatted():
    """Get formatted list of doctor names from database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT d.name, d.specialization, dept.name as department
            FROM doctors d
            LEFT JOIN departments dept ON d.department_id = dept.id
            ORDER BY dept.name, d.name
        ''')
        
        doctors = cursor.fetchall()
        conn.close()
        
        if not doctors:
            return "I apologize, but I don't have doctor information available at the moment."
        
        # Group by department
        by_department = {}
        for doctor in doctors:
            dept = doctor[2] or 'General'
            if dept not in by_department:
                by_department[dept] = []
            by_department[dept].append(f"  • {doctor[0]} - {doctor[1] or 'Specialist'}")
        
        response = "Our available doctors:\n\n"
        for dept, doc_list in by_department.items():
            response += f"{dept}:\n"
            response += "\n".join(doc_list) + "\n\n"
        
        return response.strip()
    except Exception as e:
        return "I apologize, but I couldn't retrieve the doctor information. Please contact our reception desk."

def search_doctors_by_name(search_term):
    """Search for doctors by name (partial match) - Returns ALL matching doctors."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Clean the search term (remove Dr. prefix, case-insensitive)
        search_clean = search_term.replace("Dr.", "").replace("dr.", "").strip()
        search_lower = search_clean.lower()
        
        # Search for doctors matching the name (case-insensitive, partial match)
        # Remove "Dr." from database names for comparison
        cursor.execute('''
            SELECT d.name, d.specialization, d.availability, dept.name as department
            FROM doctors d
            LEFT JOIN departments dept ON d.department_id = dept.id
            WHERE LOWER(REPLACE(REPLACE(d.name, 'Dr. ', ''), 'Dr ', '')) LIKE ?
               OR LOWER(d.name) LIKE ?
            ORDER BY 
                CASE 
                    WHEN LOWER(REPLACE(REPLACE(d.name, 'Dr. ', ''), 'Dr ', '')) = ? THEN 1
                    WHEN LOWER(REPLACE(REPLACE(d.name, 'Dr. ', ''), 'Dr ', '')) LIKE ? THEN 2
                    WHEN LOWER(d.name) LIKE ? THEN 3
                    ELSE 4
                END,
                d.name
        ''', (f'%{search_lower}%', f'%{search_lower}%', search_lower, f'{search_lower}%', f'%{search_lower}%'))
        
        doctors = cursor.fetchall()
        conn.close()
        
        if doctors:
            if len(doctors) == 1:
                doctor = doctors[0]
                return f"Found 1 doctor matching '{search_term}':\n\n• **{doctor[0]}**\n  - Specialization: {doctor[1] or 'Not specified'}\n  - Department: {doctor[3] or 'Not specified'}\n  - Availability: {doctor[2] or 'Please contact for availability'}\n\nWould you like to book an appointment with {doctor[0]}?"
            else:
                response = f"Found {len(doctors)} doctors matching '{search_term}':\n\n"
                for doctor in doctors:
                    response += f"• **{doctor[0]}**\n  - Specialization: {doctor[1] or 'Not specified'}\n  - Department: {doctor[3] or 'Not specified'}\n  - Availability: {doctor[2] or 'Please contact for availability'}\n\n"
                response += "Which doctor would you like to book an appointment with?"
                return response
        else:
            return f"I couldn't find any doctors matching '{search_term}' in our system.\n\nYou can ask me for a list of available doctors, or specify a department (e.g., Cardiology, Orthopedics)."
    except Exception as e:
        print(f"Error in search_doctors_by_name: {e}")
        traceback.print_exc()
        return f"I apologize, but I encountered an error searching for doctors."

def get_doctor_info(doctor_name):
    """Get specific information about a doctor - Enhanced with better name matching."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Clean the name
        doctor_clean = doctor_name.replace("Dr.", "").replace("dr.", "").strip()
        name_parts = doctor_clean.split()
        
        # Try exact match first
        cursor.execute('''
            SELECT d.name, d.specialization, d.availability, dept.name as department
            FROM doctors d
            LEFT JOIN departments dept ON d.department_id = dept.id
            WHERE LOWER(REPLACE(REPLACE(d.name, 'Dr. ', ''), 'Dr ', '')) = ?
               OR LOWER(REPLACE(REPLACE(d.name, 'Dr. ', ''), 'Dr ', '')) LIKE ?
        ''', (doctor_clean.lower(), f'%{doctor_clean.lower()}%'))
        
        doctors = cursor.fetchall()
        
        # If multiple matches, prefer exact match
        if len(doctors) > 1:
            exact_match = [d for d in doctors if d[0].lower().replace("dr. ", "").replace("dr ", "") == doctor_clean.lower()]
            if exact_match:
                doctors = exact_match
        
        # If no match, try first name or last name
        if not doctors and name_parts:
            first_name = name_parts[0].lower()
            cursor.execute('''
                SELECT d.name, d.specialization, d.availability, dept.name as department
                FROM doctors d
                LEFT JOIN departments dept ON d.department_id = dept.id
                WHERE LOWER(REPLACE(REPLACE(d.name, 'Dr. ', ''), 'Dr ', '')) LIKE ?
                   OR LOWER(REPLACE(REPLACE(d.name, 'Dr. ', ''), 'Dr ', '')) LIKE ?
                ORDER BY CASE 
                    WHEN LOWER(REPLACE(REPLACE(d.name, 'Dr. ', ''), 'Dr ', '')) LIKE ? THEN 1
                    WHEN LOWER(REPLACE(REPLACE(d.name, 'Dr. ', ''), 'Dr ', '')) LIKE ? THEN 2
                    ELSE 3
                END
                LIMIT 1
            ''', (f'{first_name}%', f'%{first_name}%', f'{first_name}%', f'%{first_name}%'))
            doctors = cursor.fetchall()
        
        conn.close()
        
        if doctors:
            doctor = doctors[0]
            return f"Doctor Information:\n\n• Name: {doctor[0]}\n• Specialization: {doctor[1] or 'Not specified'}\n• Department: {doctor[3] or 'Not specified'}\n• Availability: {doctor[2] or 'Please contact for availability'}\n\nWould you like to book an appointment with {doctor[0]}?"
        else:
            # If no exact match, try search to show similar names
            search_result = search_doctors_by_name(doctor_name)
            if "Found" in search_result and "doctors matching" in search_result:
                return search_result
            return f"I couldn't find a doctor named '{doctor_name}' in our system.\n\nYou can ask me for a list of available doctors, or specify a department (e.g., Cardiology, Orthopedics)."
    except Exception as e:
        print(f"Error in get_doctor_info: {e}")
        traceback.print_exc()
        return f"I apologize, but I encountered an error retrieving doctor information."

def process_appointment_booking(doctor, date, time, entities):
    """Process appointment booking with provided details - Enhanced with better doctor matching."""
    try:
        # Find doctor in database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Clean doctor name - remove "Dr." prefix and extra spaces
        doctor_clean = doctor.replace("Dr.", "").replace("dr.", "").strip()
        
        # Extract first and last name if available
        name_parts = doctor_clean.split()
        first_name = name_parts[0] if name_parts else ""
        last_name = name_parts[-1] if len(name_parts) > 1 else ""
        
        # More precise search - try multiple patterns
        search_patterns = [
            doctor_clean,  # Full name without Dr.
            f"{first_name} {last_name}",  # First + Last
            first_name,  # Just first name
            last_name,  # Just last name
        ]
        
        # Remove empty patterns
        search_patterns = [p for p in search_patterns if p]
        
        doctor_row = None
        for pattern in search_patterns:
            # Search for exact match first, then partial
            cursor.execute('''
                SELECT id, name FROM doctors 
                WHERE name = ? OR name LIKE ?
                ORDER BY CASE WHEN name = ? THEN 1 ELSE 2 END
                LIMIT 1
            ''', (pattern, f'%{pattern}%', pattern))
            
            doctor_row = cursor.fetchone()
            if doctor_row:
                break
        
        # If still not found, try broader search
        if not doctor_row:
            cursor.execute('''
                SELECT id, name FROM doctors 
                WHERE name LIKE ? OR name LIKE ?
                LIMIT 1
            ''', (f'%{first_name}%', f'%{last_name}%'))
            doctor_row = cursor.fetchone()
        
        if not doctor_row:
            conn.close()
            return f"I couldn't find {doctor} in our system. Please check the doctor name or use the format 'Dr. [First Name] [Last Name]'.\n\nYou can ask me for a list of available doctors."
        
        doctor_id = doctor_row[0]
        doctor_name = doctor_row[1]
        
        # Validate and normalize date format
        from ai.date_time_parser import NaturalDateTimeParser
        date_parser = NaturalDateTimeParser()
        normalized_date = date_parser.normalize_date(date)
        
        if not normalized_date:
            # Try parsing as natural language
            parsed_date = date_parser.parse_date(date)
            if parsed_date:
                date = parsed_date
            else:
                conn.close()
                return f"Please provide a valid date. You can use formats like:\n• YYYY-MM-DD (e.g., 2026-02-01)\n• Tomorrow\n• Next Monday\n• Today\n\nYou provided: {date}"
        else:
            date = normalized_date
        
        # Final validation
        if not re.match(r'\d{4}-\d{2}-\d{2}', date):
            conn.close()
            return f"Please provide the date in YYYY-MM-DD format (e.g., 2026-02-01). You provided: {date}"
        
        # Validate and normalize time format
        from ai.date_time_parser import NaturalDateTimeParser
        time_parser = NaturalDateTimeParser()
        normalized_time = time_parser.normalize_time(time)
        
        if not normalized_time:
            # Try parsing as natural language
            parsed_time = time_parser.parse_time(time)
            if parsed_time:
                time = parsed_time
            else:
                conn.close()
                return f"Please provide a valid time. You can use formats like:\n• HH:MM (e.g., 12:30)\n• 10 AM\n• Morning\n• Evening\n• Afternoon\n\nYou provided: {time}"
        else:
            time = normalized_time
        
        # Final validation
        if not re.match(r'\d{1,2}:\d{2}', time):
            conn.close()
            return f"Please provide the time in HH:MM format (e.g., 12:30). You provided: {time}"
        
        # Check availability using availability checker
        is_valid, validation_message = availability_checker.validate_appointment_slot(
            doctor_id, date, time
        )
        
        if not is_valid:
            conn.close()
            return f"⚠️ {validation_message}\n\nIf you need to make changes, please contact us at +1-234-567-8900."
        
        # Create appointment
        cursor.execute('''
            INSERT INTO appointments (patient_name, doctor_id, date, time, status)
            VALUES (?, ?, ?, ?, ?)
        ''', ('Patient', doctor_id, date, time, 'scheduled'))
        
        conn.commit()
        appointment_id = cursor.lastrowid
        conn.close()
        
        return f"✅ Appointment booked successfully!\n\n" \
               f"Appointment Details:\n" \
               f"• Doctor: {doctor_name}\n" \
               f"• Date: {date}\n" \
               f"• Time: {time}\n" \
               f"• Appointment ID: {appointment_id}\n\n" \
               f"Please arrive 15 minutes before your scheduled time. If you need to cancel or reschedule, please contact us at +1-234-567-8900."
    
    except Exception as e:
        return f"I apologize, but I encountered an error while booking your appointment: {str(e)}. Please try again or contact our reception desk at +1-234-567-8900."

def get_greeting_response():
    """Generate a friendly greeting response."""
    import random
    
    greetings = [
        "Hello! 👋 Welcome to our Hospital AI Assistant. I'm here to help you with:\n\n• 📅 Booking appointments\n• 👨‍⚕️ Doctor information\n• ⏰ OPD timings\n• 🏥 Services and facilities\n• 🧾 Patient FAQs\n\nHow can I assist you today?",
        
        "Hi there! 👋 I'm your Hospital AI Assistant. I can help you with:\n\n• Appointment bookings\n• Doctor details and availability\n• Hospital services\n• General inquiries\n\nWhat would you like to know?",
        
        "Good day! 🌟 Welcome to our Hospital AI Assistant. I'm here to provide information about:\n\n• 📅 Appointments\n• 👨‍⚕️ Doctors and departments\n• ⏰ Operating hours\n• 🏥 Our services\n\nHow may I help you?",
        
        "Hello! 👋 Thank you for contacting our Hospital AI Assistant. I can assist you with:\n\n• Booking appointments\n• Finding doctor information\n• Hospital services and timings\n• Answering your questions\n\nWhat can I do for you today?"
    ]
    
    return random.choice(greetings)

def format_faq_response(context, query):
    """Format FAQ response in a natural, conversational way."""
    # Remove redundant headers
    context = context.replace("HOSPITAL INFORMATION", "").strip()
    context = context.replace("DEPARTMENTS:", "").strip()
    
    # Extract the most relevant sentence or paragraph
    sentences = context.split('.')
    query_lower = query.lower()
    
    # Find sentences that contain keywords from the query
    relevant_sentences = []
    query_words = set(query_lower.split())
    
    for sentence in sentences:
        sentence_lower = sentence.lower()
        # Count how many query words appear in this sentence
        matches = sum(1 for word in query_words if word in sentence_lower and len(word) > 2)
        if matches > 0:
            relevant_sentences.append((matches, sentence.strip()))
    
    # Sort by relevance and take top 2-3 sentences
    relevant_sentences.sort(reverse=True, key=lambda x: x[0])
    
    if relevant_sentences:
        answer = '. '.join([s[1] for s in relevant_sentences[:3] if s[1]])
        if answer:
            return answer + '.'
    
    # Fallback: return first meaningful sentence
    for sentence in sentences:
        if len(sentence.strip()) > 20:
            return sentence.strip() + '.'
    
    return context[:200] + '...' if len(context) > 200 else context

def get_location_response():
    """Get hospital location/address - return ONLY location information."""
    return "Hospital Location:\n\n123 Medical Center Drive\nHealthcare City, HC 12345\n\nPhone: +1-234-567-8900\nEmail: info@hospital.com"

def get_opd_timings_response(context):
    """Get OPD timings - return ONLY timing information, never full context."""
    # Always return direct, concise answer for OPD timings
    return "OPD Timings:\n• Monday to Friday: 9:00 AM - 5:00 PM\n• Saturday: 9:00 AM - 1:00 PM\n• Sunday: Closed\n\nEmergency services are available 24/7."

def get_booking_instructions():
    """Return clear appointment booking instructions."""
    return (
        "You can book an appointment in any of these ways:\n"
        "• Tell me the doctor, date, and time here in chat (e.g., \"Book Dr. Sarah Johnson tomorrow at 10 AM\")\n"
        "• Call our appointment desk at +1-234-567-8900\n"
        "• Visit the hospital in person (walk-ins accepted, appointments recommended)\n\n"
        "If you'd like, tell me the doctor and preferred date/time."
    )

def get_services_response():
    """Return a clean list of hospital services."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM services ORDER BY name')
        services = [row[0] for row in cursor.fetchall()]
        conn.close()

        if not services:
            return "Our hospital offers Emergency Services, Outpatient Services, Inpatient Services, Laboratory Services, Radiology, Pharmacy, and Ambulance Services."

        response = "Hospital Services:\n"
        for service in services:
            response += f"• {service}\n"
        return response.strip()
    except Exception as e:
        print(f"Error in get_services_response: {e}")
        return "Our hospital offers Emergency Services, Outpatient Services, Inpatient Services, Laboratory Services, Radiology, Pharmacy, and Ambulance Services."

def handle_appointment_booking_flow(user_message, entities, conversation_context):
    """Handle appointment booking flow consistently."""
    # Handle follow-up messages like just "appointment" or "yes"
    if conversation_context and conversation_context.get('is_follow_up'):
        last_entities = conversation_context.get('last_entities', {})
        doctor = entities.get('doctor') or last_entities.get('doctor')
        date = entities.get('date') or last_entities.get('date')
        time = entities.get('time') or last_entities.get('time')
    else:
        doctor = entities.get('doctor')
        date = entities.get('date')
        time = entities.get('time')

    # If doctor looks like a booking phrase, ignore it and re-extract
    if doctor and any(word in doctor.lower() for word in ['appointment', 'book', 'schedule']):
        doctor = None

    # If doctor name is in the message but not extracted, FORCE extraction
    if not doctor:
        # Pattern 1: "Dr. Name"
        if 'dr.' in user_message.lower() or 'doctor' in user_message.lower():
            doctor_match = re.search(r'\bdr\.?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', user_message, re.IGNORECASE)
            if doctor_match:
                doctor = doctor_match.group(0)

        # Pattern 2: "with/for Name" (e.g., "book appointment with Sarah Johnson")
        if not doctor and ('book' in user_message.lower() or 'appointment' in user_message.lower()):
            name_after_with = re.search(r'(?:with|for)\s+(?:dr\.?\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', user_message, re.IGNORECASE)
            if name_after_with:
                potential_name = name_after_with.group(1)
                stop_words = {'appointment', 'an', 'the', 'a', 'doctor', 'dr', 'my', 'book', 'schedule', 'with', 'for'}
                tokens = [t.lower() for t in potential_name.split()]
                if not any(token in stop_words for token in tokens) and 'appointment' not in potential_name.lower():
                    doctor = f"Dr. {potential_name}" if not potential_name.lower().startswith('dr') else potential_name

    if doctor and date and time:
        # Check if this is a duplicate booking attempt
        if conversation_context and conversation_context.get('last_intent') == 'appointment_booking':
            last_entities = conversation_context.get('last_entities', {})
            if (last_entities.get('doctor') == doctor and 
                last_entities.get('date') == date and 
                last_entities.get('time') == time):
                return "You already have an appointment booked with these details. If you need to make changes, please contact us at +1-234-567-8900."
        return process_appointment_booking(doctor, date, time, entities)
    elif doctor or date or time:
        missing = []
        if not doctor:
            missing.append("Doctor name (e.g., Dr. Sarah Johnson)")
        if not date:
            missing.append("Date (e.g., tomorrow, next Monday, or 2026-02-01)")
        if not time:
            missing.append("Time (e.g., 10 AM, morning, evening, or 12:30)")

        provided = []
        if doctor:
            provided.append(f"Doctor: {doctor}")
        if date:
            provided.append(f"Date: {date}")
        if time:
            provided.append(f"Time: {time}")

        response = "I have some of your appointment details:\n"
        if provided:
            response += "• " + "\n• ".join(provided) + "\n\n"
        response += "Please also provide:\n• " + "\n• ".join(missing)
        return response

    return "I can help you book an appointment. Please provide:\n• Doctor name (e.g., Dr. Sarah Johnson)\n• Date (e.g., tomorrow, next Monday, or 2026-02-01)\n• Time (e.g., 10 AM, morning, evening, or 12:30)"

def get_hospital_overview():
    """Return a detailed, friendly hospital overview."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT name FROM departments ORDER BY name')
        departments = [row[0] for row in cursor.fetchall()]

        cursor.execute('SELECT name FROM services ORDER BY name')
        services = [row[0] for row in cursor.fetchall()]

        cursor.execute('''
            SELECT d.name, dept.name as department
            FROM doctors d
            LEFT JOIN departments dept ON d.department_id = dept.id
            ORDER BY dept.name, d.name
        ''')
        doctors = cursor.fetchall()
        conn.close()

        by_department = {}
        for name, dept in doctors:
            dept_name = dept or 'General'
            if dept_name not in by_department:
                by_department[dept_name] = []
            if len(by_department[dept_name]) < 2:
                by_department[dept_name].append(name)

        dept_list = ", ".join(departments) if departments else "Cardiology, Orthopedics, Pediatrics, General Medicine"
        service_list = ", ".join(services) if services else "Emergency, OPD, Inpatient, Laboratory, Radiology, Pharmacy"

        overview = "Here is a detailed overview of our hospital:\n\n"
        overview += f"Departments: {dept_list}\n"
        overview += f"Services: {service_list}\n\n"
        overview += "Sample doctors by department:\n"
        for dept_name, doc_list in by_department.items():
            overview += f"• {dept_name}: {', '.join(doc_list)}\n"
        overview += "\nOPD Timings:\n• Monday to Friday: 9:00 AM - 5:00 PM\n• Saturday: 9:00 AM - 1:00 PM\n• Sunday: Closed (Emergency services available 24/7)\n\n"
        overview += "Location:\n123 Medical Center Drive, Healthcare City, HC 12345\nPhone: +1-234-567-8900\nEmail: info@hospital.com\n\n"
        overview += "You can ask for specific doctors, departments, services, or book an appointment. What would you like to do?"

        return overview
    except Exception as e:
        print(f"Error in get_hospital_overview: {e}")
        return "I can help with doctors, appointments, services, OPD timings, and hospital location. What would you like to know?"

def extract_specific_info(context, info_type):
    """Extract specific type of information from context."""
    lines = context.split('\n')
    result_lines = []
    in_section = False
    
    for line in lines:
        line_lower = line.lower()
        
        if info_type == 'services':
            if 'service' in line_lower or line.strip().startswith('-'):
                if 'service' in line_lower or any(word in line_lower for word in ['emergency', 'outpatient', 'inpatient', 'laboratory', 'radiology', 'pharmacy', 'ambulance']):
                    result_lines.append(line.strip())
        
        # Stop at next major section
        if line.strip() and line.strip().isupper() and len(line.strip()) > 3:
            if in_section and line.strip() not in ['OPD TIMINGS:', 'SERVICES:', 'LOCATION:']:
                break
            if info_type in line_lower:
                in_section = True
    
    return '\n'.join([line for line in result_lines if line])[:300]  # Limit length

def generate_natural_response(user_message):
    """Generate a natural response when context is not available."""
    user_lower = user_message.lower()

    # Broad hospital information requests
    if any(phrase in user_lower for phrase in ['hospital info', 'hospital information', 'about hospital', 'about the hospital',
                                               'tell me about', 'overview', 'details', 'all information', 'everything about']):
        return get_hospital_overview()
    
    # Check for common questions
    if any(word in user_lower for word in ['timing', 'time', 'opd', 'when', 'open', 'close']):
        return "Our OPD timings are:\n• Monday to Friday: 9:00 AM - 5:00 PM\n• Saturday: 9:00 AM - 1:00 PM\n• Sunday: Closed (Emergency services available 24/7)"
    
    if any(word in user_lower for word in ['location', 'address', 'where', 'find']):
        return "Our hospital is located at:\n123 Medical Center Drive\nHealthcare City, HC 12345\n\nPhone: +1-234-567-8900"
    
    if any(word in user_lower for word in ['contact', 'phone', 'call', 'number']):
        return "You can contact us at:\n• Phone: +1-234-567-8900\n• Email: info@hospital.com\n• For appointments: Call our appointment desk"
    
    if any(word in user_lower for word in ['parking', 'park']):
        return "Yes, free parking is available for patients and visitors."
    
    if any(word in user_lower for word in ['insurance', 'accept']):
        return "Yes, we accept most major insurance plans. Please contact our billing department for specific details about your insurance coverage."
    
    if any(word in user_lower for word in ['document', 'paper', 'need', 'bring']):
        return "Please bring:\n• Valid ID\n• Insurance card (if applicable)\n• Any previous medical records"
    
    # Default helpful response
    return "I can help with doctors, appointments, services, OPD timings, and hospital location. What would you like to know?"

def extract_relevant_answer(context, query):
    """Extract only the relevant part of the context based on the query."""
    query_lower = query.lower()
    
    # If asking about location/address - return None to use direct answer
    if any(word in query_lower for word in ['address', 'location', 'where', 'located']):
        return None  # Return None so get_location_response is called
    
    # If asking about OPD timings - return None to use direct answer
    if any(word in query_lower for word in ['timing', 'time', 'opd', 'open', 'close', 'hour']):
        return None  # Return None so get_opd_timings_response is called
    
    # If asking about doctors, extract only doctor-related info
    # BUT: Don't use RAG context if user is asking about a specific doctor name
    # The database query should handle that, not RAG
    if 'doctor' in query_lower or 'name' in query_lower:
        # If query contains a specific doctor name (like "Dr. Sarah Johnson"), skip RAG
        if re.search(r'\bdr\.?\s+[A-Z][a-z]+', query, re.IGNORECASE):
            return None  # Let database query handle it
        lines = context.split('\n')
        doctor_lines = [line for line in lines if 'dr.' in line.lower() or 'doctor' in line.lower()]
        if doctor_lines:
            # Format properly - remove incomplete/malformed lines
            formatted_lines = []
            for line in doctor_lines[:8]:
                line = line.strip()
                # Skip empty lines
                if not line:
                    continue
                # Skip malformed patterns like:
                # - "Sarah Johnson - Orthopedics: Dr."
                # - "- Cardiology: Dr."
                # - Any line ending with ": Dr." or ": Dr" without full name after
                if re.search(r':\s*Dr\.?\s*$', line):
                    continue
                # Skip lines with "Name - Department: Dr." format (bot response format)
                if re.search(r'^[A-Z][a-z]+\s+[A-Z][a-z]+\s*-\s*[A-Za-z]+\s*:\s*Dr\.?\s*$', line):
                    continue
                # Skip very short lines with colons (likely incomplete)
                if ':' in line and len(line) < 25:
                    continue
                # Only include lines that have complete doctor info
                formatted_lines.append(line)
            if formatted_lines:
                return '\n'.join(formatted_lines)
        # If no valid doctor lines, return None
        return None
    
    # If asking about services
    if 'service' in query_lower:
        lines = context.split('\n')
        service_lines = [line for line in lines if 'service' in line.lower() or (line.strip().startswith('-') and any(word in line.lower() for word in ['emergency', 'outpatient', 'laboratory', 'radiology', 'pharmacy']))]
        if service_lines:
            return '\n'.join(service_lines[:6])  # Limit to 6 lines
    
    # Default: return first 2 sentences only (very limited)
    sentences = context.split('.')
    relevant = []
    for sentence in sentences:
        sentence = sentence.strip()
        # Skip headers and very short sentences
        if len(sentence) > 15 and not sentence.isupper():
            relevant.append(sentence)
            if len(relevant) >= 2:
                break
    
    if relevant:
        return '. '.join(relevant) + '.'
    
    # Last resort: very limited context
    return context[:100] + '...' if len(context) > 100 else context

def handle_appointment_cancellation(user_message, entities, conversation_context):
    """Handle appointment cancellation requests from chat."""
    try:
        entities = entities or {}
        # Extract appointment ID or patient name from message
        import re
        
        # Try to extract appointment ID
        appointment_id_match = re.search(r'(?:appointment|id|#)\s*(?:is|:)?\s*(\d+)', user_message, re.IGNORECASE)
        appointment_id = None
        if appointment_id_match:
            try:
                appointment_id = int(appointment_id_match.group(1))
            except (TypeError, ValueError):
                appointment_id = None
        
        # Try to extract patient name
        patient_name = entities.get('patient_name')
        if not patient_name:
            # Look for "my appointment" or patient name patterns
            if 'my appointment' in user_message.lower():
                # Get from conversation context if available
                if conversation_context:
                    last_entities = conversation_context.get('last_entities') or {}
                    patient_name = last_entities.get('patient_name')
        
        if not appointment_id and not patient_name:
            return "To cancel your appointment, please provide:\n• Your appointment ID (e.g., 'Cancel appointment ID 123'), or\n• Your name (e.g., 'Cancel my appointment, I'm John Smith')\n\nYou can also contact us directly at +1-234-567-8900."
        
        # For chat interface, provide instructions to use the API or contact
        if appointment_id:
            return f"I can help you cancel appointment #{appointment_id}.\n\nPlease confirm by providing your name, or contact us directly at +1-234-567-8900 with:\n• Appointment ID: {appointment_id}\n• Your name"
        else:
            return f"I can help you cancel your appointment.\n\nPlease provide your appointment ID, or contact us at +1-234-567-8900 with your name: {patient_name if patient_name else 'your registered name'}."
    
    except Exception as e:
        print(f"Error in handle_appointment_cancellation: {e}")
        traceback.print_exc()
        return "I apologize, but I encountered an error processing your cancellation request. Please contact us directly at +1-234-567-8900."

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))  # Changed to 8000 to avoid conflicts
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    print("=" * 60)
    print("🏥 Hospital AI Chatbot - Starting Server")
    print("=" * 60)
    print(f"Server running on: http://localhost:{port}")
    print(f"Chat interface: http://localhost:{port}/")
    print(f"API health: http://localhost:{port}/api/health")
    print("=" * 60)
    app.run(host='0.0.0.0', port=port, debug=debug)

