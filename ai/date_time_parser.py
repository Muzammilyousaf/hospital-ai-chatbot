"""
Natural Language Date and Time Parsing
Converts natural language dates/times to standardized formats
"""

from datetime import datetime, timedelta
import re
from typing import Optional, Tuple

class NaturalDateTimeParser:
    """Parse natural language dates and times to standardized formats."""
    
    def __init__(self):
        """Initialize the parser."""
        self.now = datetime.now()
        self.today = self.now.date()
    
    def parse_date(self, text: str) -> Optional[str]:
        """
        Parse natural language dates to YYYY-MM-DD format.
        
        Args:
            text: User message containing date information
            
        Returns:
            Date in YYYY-MM-DD format or None
        """
        if not text:
            return None
        
        text_lower = text.lower().strip()
        today = datetime.now()
        
        # Relative dates (highest priority)
        if 'tomorrow' in text_lower:
            date = today + timedelta(days=1)
            return date.strftime('%Y-%m-%d')
        
        if 'today' in text_lower:
            return today.strftime('%Y-%m-%d')
        
        if 'day after tomorrow' in text_lower or 'day after' in text_lower:
            date = today + timedelta(days=2)
            return date.strftime('%Y-%m-%d')
        
        if 'next week' in text_lower:
            date = today + timedelta(weeks=1)
            return date.strftime('%Y-%m-%d')
        
        if 'next month' in text_lower:
            # Add approximately 30 days
            date = today + timedelta(days=30)
            return date.strftime('%Y-%m-%d')
        
        if 'next year' in text_lower:
            date = today + timedelta(days=365)
            return date.strftime('%Y-%m-%d')
        
        # Day names (Monday, Tuesday, etc.)
        days_of_week = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
            'friday': 4, 'saturday': 5, 'sunday': 6
        }
        
        for day_name, day_num in days_of_week.items():
            if day_name in text_lower:
                today_weekday = today.weekday()
                days_ahead = day_num - today_weekday
                
                # If the day has passed this week, get next week's occurrence
                if days_ahead <= 0:
                    days_ahead += 7
                
                # Handle "next Monday" vs "Monday"
                if 'next' in text_lower and day_name in text_lower:
                    # Find the position of "next" and day name
                    next_pos = text_lower.find('next')
                    day_pos = text_lower.find(day_name)
                    if next_pos < day_pos:  # "next" comes before day name
                        days_ahead += 7
                
                date = today + timedelta(days=days_ahead)
                return date.strftime('%Y-%m-%d')
        
        # Relative day references
        if 'in a week' in text_lower or 'week from now' in text_lower:
            date = today + timedelta(weeks=1)
            return date.strftime('%Y-%m-%d')
        
        if 'in two weeks' in text_lower or 'two weeks from now' in text_lower:
            date = today + timedelta(weeks=2)
            return date.strftime('%Y-%m-%d')
        
        if 'in a month' in text_lower or 'month from now' in text_lower:
            date = today + timedelta(days=30)
            return date.strftime('%Y-%m-%d')
        
        # Standard date formats (existing support)
        # YYYY-MM-DD
        date_match = re.search(r'\d{4}-\d{2}-\d{2}', text)
        if date_match:
            return date_match.group(0)
        
        # MM/DD/YYYY
        date_match = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', text)
        if date_match:
            month, day, year = date_match.groups()
            return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        
        # DD-MM-YYYY
        date_match = re.search(r'(\d{1,2})-(\d{1,2})-(\d{4})', text)
        if date_match:
            day, month, year = date_match.groups()
            return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        
        # DD/MM/YYYY
        date_match = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', text)
        if date_match:
            day, month, year = date_match.groups()
            return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        
        return None
    
    def parse_time(self, text: str) -> Optional[str]:
        """
        Parse natural language times to HH:MM format.
        
        Args:
            text: User message containing time information
            
        Returns:
            Time in HH:MM format (24-hour) or None
        """
        if not text:
            return None
        
        text_lower = text.lower().strip()
        now = datetime.now()
        
        # Time of day phrases
        if 'right now' in text_lower or 'now' in text_lower:
            return now.strftime('%H:%M')
        
        if 'morning' in text_lower:
            # Default morning time: 9:00 AM
            if 'early' in text_lower:
                return '08:00'
            elif 'late' in text_lower:
                return '11:00'
            else:
                return '09:00'
        
        if 'afternoon' in text_lower:
            # Default afternoon time: 2:00 PM
            if 'early' in text_lower:
                return '13:00'
            elif 'late' in text_lower:
                return '17:00'
            else:
                return '14:00'
        
        if 'evening' in text_lower or 'tonight' in text_lower:
            # Default evening time: 6:00 PM
            if 'early' in text_lower:
                return '17:00'
            elif 'late' in text_lower:
                return '20:00'
            else:
                return '18:00'
        
        if 'night' in text_lower:
            # Default night time: 8:00 PM
            return '20:00'
        
        # Extract numeric time patterns
        # Pattern 1: HH:MM (24-hour or 12-hour)
        time_match = re.search(r'(\d{1,2}):(\d{2})', text_lower)
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2))
            
            # Check for AM/PM
            if 'pm' in text_lower or 'p.m.' in text_lower:
                if hour < 12:
                    hour += 12
            elif 'am' in text_lower or 'a.m.' in text_lower:
                if hour == 12:
                    hour = 0
            
            # Validate hour (0-23)
            if hour > 23:
                hour = 23
            if minute > 59:
                minute = 59
            
            return f"{hour:02d}:{minute:02d}"
        
        # Pattern 2: Just hour with AM/PM (e.g., "10 AM", "3 PM")
        time_match = re.search(r'(\d{1,2})\s*(?:am|pm|a\.m\.|p\.m\.)', text_lower)
        if time_match:
            hour = int(time_match.group(1))
            
            if 'pm' in text_lower or 'p.m.' in text_lower:
                if hour < 12:
                    hour += 12
            elif 'am' in text_lower or 'a.m.' in text_lower:
                if hour == 12:
                    hour = 0
            
            if hour > 23:
                hour = 23
            
            return f"{hour:02d}:00"
        
        # Pattern 3: Just hour number (e.g., "10", "3")
        # Only if it's a reasonable hour (1-12) and context suggests time
        if any(word in text_lower for word in ['at', 'around', 'about', 'by', 'before', 'after']):
            time_match = re.search(r'\b(\d{1,2})\b', text_lower)
            if time_match:
                hour = int(time_match.group(1))
                # Assume reasonable hours (1-12) are in 12-hour format
                if 1 <= hour <= 12:
                    # Default to PM for afternoon/evening context, AM for morning
                    if any(word in text_lower for word in ['afternoon', 'evening', 'night', 'pm']):
                        if hour < 12:
                            hour += 12
                    elif any(word in text_lower for word in ['morning', 'am']):
                        if hour == 12:
                            hour = 0
                    else:
                        # Default: assume PM for hours 1-11, AM for 12
                        if hour < 12:
                            hour += 12
                    
                    return f"{hour:02d}:00"
        
        return None
    
    def parse_datetime(self, text: str) -> Optional[Tuple[str, str]]:
        """
        Parse both date and time from text.
        
        Args:
            text: User message containing date and time information
            
        Returns:
            Tuple of (date, time) in (YYYY-MM-DD, HH:MM) format or None
        """
        date = self.parse_date(text)
        time = self.parse_time(text)
        
        if date and time:
            return (date, time)
        elif date:
            return (date, None)
        elif time:
            return (None, time)
        
        return None
    
    def normalize_date(self, date_str: str) -> Optional[str]:
        """
        Normalize various date formats to YYYY-MM-DD.
        
        Args:
            date_str: Date string in various formats
            
        Returns:
            Normalized date in YYYY-MM-DD format or None
        """
        if not date_str:
            return None
        
        # Try parsing as natural language first
        parsed = self.parse_date(date_str)
        if parsed:
            return parsed
        
        # Already in correct format
        if re.match(r'\d{4}-\d{2}-\d{2}', date_str):
            return date_str
        
        return None
    
    def normalize_time(self, time_str: str) -> Optional[str]:
        """
        Normalize various time formats to HH:MM.
        
        Args:
            time_str: Time string in various formats
            
        Returns:
            Normalized time in HH:MM format or None
        """
        if not time_str:
            return None
        
        # Try parsing as natural language first
        parsed = self.parse_time(time_str)
        if parsed:
            return parsed
        
        # Already in correct format
        if re.match(r'\d{2}:\d{2}', time_str):
            return time_str
        
        return None

