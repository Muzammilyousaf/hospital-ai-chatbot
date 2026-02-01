"""
Conversation Memory and Context Tracking
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json

class ConversationMemory:
    """Manages conversation context and memory."""
    
    def __init__(self, session_timeout_minutes: int = 30):
        """Initialize conversation memory."""
        self.sessions: Dict[str, Dict] = {}
        self.session_timeout = timedelta(minutes=session_timeout_minutes)
    
    def get_session(self, session_id: str) -> Dict:
        """Get or create a session."""
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'messages': [],
                'context': {},
                'last_activity': datetime.now(),
                'intent_history': [],
                'entities_history': []
            }
        else:
            # Update last activity
            self.sessions[session_id]['last_activity'] = datetime.now()
        
        return self.sessions[session_id]
    
    def add_message(self, session_id: str, role: str, message: str, intent: Optional[str] = None, entities: Optional[Dict] = None):
        """Add a message to conversation history."""
        session = self.get_session(session_id)
        
        session['messages'].append({
            'role': role,  # 'user' or 'assistant'
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'intent': intent,
            'entities': entities
        })
        
        if intent:
            session['intent_history'].append(intent)
        if entities:
            session['entities_history'].append(entities)
        
        # Keep only last 10 messages to prevent memory bloat
        if len(session['messages']) > 10:
            session['messages'] = session['messages'][-10:]
            session['intent_history'] = session['intent_history'][-5:]
            session['entities_history'] = session['entities_history'][-5:]
    
    def get_context(self, session_id: str) -> Dict:
        """Get conversation context."""
        session = self.get_session(session_id)
        return session.get('context', {})
    
    def update_context(self, session_id: str, key: str, value):
        """Update conversation context."""
        session = self.get_session(session_id)
        session['context'][key] = value
    
    def get_recent_messages(self, session_id: str, n: int = 3) -> List[Dict]:
        """Get recent messages from conversation."""
        session = self.get_session(session_id)
        return session['messages'][-n:] if len(session['messages']) >= n else session['messages']
    
    def get_last_intent(self, session_id: str) -> Optional[str]:
        """Get the last intent from conversation."""
        session = self.get_session(session_id)
        if session['intent_history']:
            return session['intent_history'][-1]
        return None
    
    def get_last_entities(self, session_id: str) -> Optional[Dict]:
        """Get the last entities from conversation."""
        session = self.get_session(session_id)
        if session['entities_history']:
            return session['entities_history'][-1]
        return None
    
    def is_follow_up(self, session_id: str, current_intent: str) -> bool:
        """Check if current message is a follow-up to previous conversation."""
        session = self.get_session(session_id)
        if not session['messages']:
            return False
        
        last_intent = self.get_last_intent(session_id)
        if not last_intent:
            return False
        
        # Check if it's a follow-up question
        follow_up_keywords = ['yes', 'no', 'ok', 'sure', 'that', 'this', 'it', 'also', 'and', 'more', 'another']
        last_message = session['messages'][-1]['message'].lower()
        current_message = session['messages'][-1]['message'].lower() if session['messages'] else ''
        
        # If last intent was appointment_booking and current is also appointment_booking, likely follow-up
        if last_intent == 'appointment_booking' and current_intent == 'appointment_booking':
            return True
        
        # If message starts with follow-up keywords
        if any(keyword in current_message.split()[:3] for keyword in follow_up_keywords):
            return True
        
        return False
    
    def clear_session(self, session_id: str):
        """Clear a session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions."""
        now = datetime.now()
        expired = [
            sid for sid, session in self.sessions.items()
            if now - session['last_activity'] > self.session_timeout
        ]
        for sid in expired:
            del self.sessions[sid]
    
    def get_conversation_summary(self, session_id: str) -> str:
        """Get a summary of the conversation for context."""
        session = self.get_session(session_id)
        if not session['messages']:
            return ""
        
        summary_parts = []
        recent = self.get_recent_messages(session_id, 3)
        
        for msg in recent:
            role = msg['role']
            text = msg['message'][:100]  # Truncate long messages
            summary_parts.append(f"{role}: {text}")
        
        return "\n".join(summary_parts)

