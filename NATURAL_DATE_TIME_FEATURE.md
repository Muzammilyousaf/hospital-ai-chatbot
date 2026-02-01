# Natural Date/Time Parsing Feature

## ✅ Implementation Complete

Natural language date and time parsing has been successfully integrated into the Hospital AI Chatbot.

## 📅 Supported Date Formats

### Natural Language Dates
- **"tomorrow"** → Next day
- **"today"** → Current date
- **"day after tomorrow"** → Day after next
- **"next week"** → 7 days from now
- **"next month"** → ~30 days from now
- **"next year"** → ~365 days from now
- **"Monday"**, **"Tuesday"**, etc. → Next occurrence of that day
- **"next Monday"** → Monday of next week
- **"in a week"** → 7 days from now
- **"in two weeks"** → 14 days from now
- **"in a month"** → ~30 days from now

### Standard Date Formats (Still Supported)
- **YYYY-MM-DD** (e.g., 2026-02-01)
- **MM/DD/YYYY** (e.g., 02/01/2026)
- **DD-MM-YYYY** (e.g., 01-02-2026)
- **DD/MM/YYYY** (e.g., 01/02/2026)

## ⏰ Supported Time Formats

### Natural Language Times
- **"right now"** or **"now"** → Current time
- **"morning"** → 09:00
- **"early morning"** → 08:00
- **"late morning"** → 11:00
- **"afternoon"** → 14:00
- **"early afternoon"** → 13:00
- **"late afternoon"** → 17:00
- **"evening"** or **"tonight"** → 18:00
- **"early evening"** → 17:00
- **"late evening"** → 20:00
- **"night"** → 20:00

### Numeric Time Formats (Still Supported)
- **HH:MM** (e.g., 12:30)
- **HH:MM AM/PM** (e.g., 10:30 AM, 3:45 PM)
- **H AM/PM** (e.g., 10 AM, 3 PM)
- **H** (e.g., "10" → 10:00, "3" → 15:00 when context suggests time)

## 🎯 Example Queries

### Date Examples
```
User: "I want an appointment tomorrow"
Bot: Extracts date as tomorrow's date (YYYY-MM-DD format)

User: "Book me for next Monday"
Bot: Extracts date as next Monday's date

User: "Schedule for next week"
Bot: Extracts date as 7 days from today

User: "Appointment on 2026-02-01"
Bot: Extracts date as 2026-02-01 (standard format still works)
```

### Time Examples
```
User: "I want an appointment tomorrow at 10"
Bot: Extracts date as tomorrow, time as 10:00

User: "Book me right now"
Bot: Extracts time as current time

User: "Schedule with a heart doctor this evening"
Bot: Extracts time as 18:00 (evening)

User: "Appointment at 10 AM"
Bot: Extracts time as 10:00

User: "Book for 3:30 PM"
Bot: Extracts time as 15:30
```

### Combined Examples
```
User: "I want an appointment tomorrow at 10"
→ Date: tomorrow, Time: 10:00

User: "Book me right now"
→ Time: current time

User: "Schedule with a heart doctor this evening"
→ Time: 18:00

User: "Appointment next Monday morning"
→ Date: next Monday, Time: 09:00
```

## 🔧 Technical Implementation

### Files Created/Modified

1. **`ai/date_time_parser.py`** (NEW)
   - `NaturalDateTimeParser` class
   - `parse_date()` method
   - `parse_time()` method
   - `parse_datetime()` method
   - `normalize_date()` method
   - `normalize_time()` method

2. **`ai/entity_extractor.py`** (MODIFIED)
   - Integrated `NaturalDateTimeParser`
   - Uses natural parser first, falls back to regex
   - Normalizes all date/time formats

3. **`app.py`** (MODIFIED)
   - Enhanced date/time validation in appointment booking
   - Better error messages with natural language examples
   - Normalizes dates/times before validation

## 🎨 User Experience Improvements

### Before
```
User: "I want an appointment tomorrow at 10"
Bot: "Please provide the date in YYYY-MM-DD format"
```

### After
```
User: "I want an appointment tomorrow at 10"
Bot: ✅ Books appointment for tomorrow at 10:00
```

## 📝 Usage in Code

### Direct Usage
```python
from ai.date_time_parser import NaturalDateTimeParser

parser = NaturalDateTimeParser()

# Parse date
date = parser.parse_date("tomorrow")  # Returns: "2026-02-15"

# Parse time
time = parser.parse_time("10 AM")  # Returns: "10:00"

# Parse both
result = parser.parse_datetime("tomorrow at 10 AM")
# Returns: ("2026-02-15", "10:00")
```

### Automatic Integration
The parser is automatically used by:
- `EntityExtractor` - Extracts dates/times from user messages
- `process_appointment_booking()` - Validates and normalizes dates/times

## 🧪 Testing Examples

Try these queries in the chatbot:

1. **"Book appointment tomorrow at 10"**
2. **"I want to see a doctor next Monday morning"**
3. **"Schedule for this evening"**
4. **"Appointment next week at 3 PM"**
5. **"Book me right now"**
6. **"I need an appointment day after tomorrow at afternoon"**

All of these should work seamlessly!

## ⚠️ Notes

- Dates are always normalized to **YYYY-MM-DD** format
- Times are always normalized to **HH:MM** format (24-hour)
- The parser handles both natural language and standard formats
- Falls back to regex patterns if natural parsing fails
- Context-aware (e.g., "10" becomes 10:00 or 22:00 based on context)

## 🚀 Next Steps (Optional Enhancements)

1. **Time zone support** - Handle different time zones
2. **Recurring appointments** - "Every Monday at 10 AM"
3. **Date ranges** - "Sometime next week"
4. **Relative times** - "In 2 hours", "In 3 days"
5. **Holiday awareness** - Skip holidays in date calculations

