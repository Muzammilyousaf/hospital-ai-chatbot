"""
Doctor Availability Checking
Validates appointment slots before booking
"""

from database.db import get_db_connection
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

class AvailabilityChecker:
    """Check doctor availability and validate appointment slots."""
    
    def __init__(self):
        """Initialize availability checker."""
        pass
    
    def check_doctor_availability(self, doctor_id: int, date: str, time: str) -> Dict:
        """
        Check if doctor is available at given date/time.
        
        Args:
            doctor_id: Doctor ID
            date: Date in YYYY-MM-DD format
            time: Time in HH:MM format
            
        Returns:
            Dictionary with availability status and details
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check existing appointments (scheduled or confirmed)
            cursor.execute('''
                SELECT COUNT(*) FROM appointments
                WHERE doctor_id = ? 
                AND date = ? 
                AND time = ? 
                AND status IN ('scheduled', 'confirmed')
            ''', (doctor_id, date, time))
            
            existing_count = cursor.fetchone()[0]
            
            # Get doctor availability schedule
            cursor.execute('SELECT availability, name FROM doctors WHERE id = ?', (doctor_id,))
            doctor = cursor.fetchone()
            
            if not doctor:
                conn.close()
                return {
                    'available': False,
                    'reason': 'Doctor not found',
                    'doctor_name': None
                }
            
            availability = doctor[0]
            doctor_name = doctor[1]
            
            # Check if date is in the past
            try:
                appointment_date = datetime.strptime(date, '%Y-%m-%d').date()
                today = datetime.now().date()
                if appointment_date < today:
                    conn.close()
                    return {
                        'available': False,
                        'reason': 'Cannot book appointments in the past',
                        'doctor_name': doctor_name
                    }
            except ValueError:
                pass
            
            # Check if time is valid (basic validation)
            try:
                hour, minute = map(int, time.split(':'))
                if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                    conn.close()
                    return {
                        'available': False,
                        'reason': 'Invalid time format',
                        'doctor_name': doctor_name
                    }
            except (ValueError, AttributeError):
                conn.close()
                return {
                    'available': False,
                    'reason': 'Invalid time format',
                    'doctor_name': doctor_name
                }
            
            conn.close()
            
            is_available = existing_count == 0
            
            return {
                'available': is_available,
                'reason': 'Slot already booked' if not is_available else None,
                'doctor_name': doctor_name,
                'existing_appointments': existing_count,
                'availability_schedule': availability
            }
        
        except Exception as e:
            print(f"Error checking availability: {e}")
            return {
                'available': False,
                'reason': f'Error checking availability: {str(e)}',
                'doctor_name': None
            }
    
    def get_available_slots(self, doctor_id: int, date: str) -> List[str]:
        """
        Get available time slots for a doctor on a given date.
        
        Args:
            doctor_id: Doctor ID
            date: Date in YYYY-MM-DD format
            
        Returns:
            List of available time slots in HH:MM format
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Get doctor's availability schedule
            cursor.execute('SELECT availability FROM doctors WHERE id = ?', (doctor_id,))
            doctor = cursor.fetchone()
            
            if not doctor:
                conn.close()
                return []
            
            # Get existing appointments for this doctor on this date
            cursor.execute('''
                SELECT time FROM appointments
                WHERE doctor_id = ? 
                AND date = ? 
                AND status IN ('scheduled', 'confirmed')
                ORDER BY time
            ''', (doctor_id, date))
            
            booked_times = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            # Generate common time slots (9 AM to 5 PM, hourly)
            common_slots = []
            for hour in range(9, 18):  # 9 AM to 5 PM
                for minute in [0, 30]:  # Every 30 minutes
                    time_slot = f"{hour:02d}:{minute:02d}"
                    common_slots.append(time_slot)
            
            # Filter out booked slots
            available_slots = [slot for slot in common_slots if slot not in booked_times]
            
            return available_slots
        
        except Exception as e:
            print(f"Error getting available slots: {e}")
            return []
    
    def suggest_alternative_slots(self, doctor_id: int, date: str, preferred_time: str, 
                                  num_suggestions: int = 3) -> List[str]:
        """
        Suggest alternative time slots if preferred time is not available.
        
        Args:
            doctor_id: Doctor ID
            date: Date in YYYY-MM-DD format
            preferred_time: Preferred time in HH:MM format
            num_suggestions: Number of suggestions to return
            
        Returns:
            List of alternative time slots
        """
        try:
            # Parse preferred time
            pref_hour, pref_minute = map(int, preferred_time.split(':'))
            
            # Get available slots
            available_slots = self.get_available_slots(doctor_id, date)
            
            if not available_slots:
                return []
            
            # Find slots closest to preferred time
            def time_difference(slot):
                slot_hour, slot_minute = map(int, slot.split(':'))
                diff = abs((slot_hour * 60 + slot_minute) - (pref_hour * 60 + pref_minute))
                return diff
            
            # Sort by time difference and return closest slots
            sorted_slots = sorted(available_slots, key=time_difference)
            
            return sorted_slots[:num_suggestions]
        
        except Exception as e:
            print(f"Error suggesting alternatives: {e}")
            return []
    
    def validate_appointment_slot(self, doctor_id: int, date: str, time: str) -> Tuple[bool, str]:
        """
        Validate if an appointment slot can be booked.
        
        Args:
            doctor_id: Doctor ID
            date: Date in YYYY-MM-DD format
            time: Time in HH:MM format
            
        Returns:
            Tuple of (is_valid, message)
        """
        availability = self.check_doctor_availability(doctor_id, date, time)
        
        if not availability['available']:
            reason = availability.get('reason', 'Slot not available')
            doctor_name = availability.get('doctor_name', 'Doctor')
            
            # Get alternative suggestions
            alternatives = self.suggest_alternative_slots(doctor_id, date, time)
            
            message = f"{reason} for {doctor_name} on {date} at {time}."
            
            if alternatives:
                alt_times = ', '.join(alternatives)
                message += f"\n\nAvailable alternative times: {alt_times}"
            else:
                message += f"\n\nPlease try a different date or time."
            
            return False, message
        
        return True, "Slot is available"

