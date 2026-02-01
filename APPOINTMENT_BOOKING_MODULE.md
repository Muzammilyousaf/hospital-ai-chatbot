# 📅 Appointment Booking Module - Complete Guide

## 🎯 Overview

The appointment booking module is a **multi-step, intelligent system** that handles appointment scheduling through natural language conversations. It supports:

- ✅ Natural language date/time parsing
- ✅ Multi-turn conversations
- ✅ Doctor name matching (flexible)
- ✅ Availability validation
- ✅ Duplicate prevention
- ✅ Error handling

---

## 🔄 Complete Booking Flow

### Step 1: User Initiates Booking

**User Input Examples:**
```
"I want to book an appointment"
"Book appointment"
"Schedule with Dr. John Smith"
"Book appointment with Dr. Sarah Johnson tomorrow at 10 AM"
```

### Step 2: Intent Classification

The system detects `appointment_booking` intent using:
- Keyword matching ("book", "appointment", "schedule")
- ML-based intent classification (DistilBERT + embeddings)
- Context from conversation history

**Location:** `ai/intent_model.py`

### Step 3: Entity Extraction

Extracts three key entities:
1. **Doctor Name** - From user message
2. **Date** - Natural language or formatted
3. **Time** - Natural language or formatted

**Location:** `ai/entity_extractor.py`

**Examples:**
```
Input: "Book with Dr. John Smith tomorrow at 10 AM"
Extracted:
  - doctor: "Dr. John Smith"
  - date: "tomorrow"
  - time: "10 AM"
```

### Step 4: Multi-Turn Conversation Support

If information is missing, the bot asks for it step by step:

**Example Flow:**
```
User: "I want to book an appointment"
Bot: "I can help you book an appointment. Please provide:
     • Doctor name (e.g., Dr. Sarah Johnson)
     • Date (e.g., tomorrow, next Monday, or 2026-02-01)
     • Time (e.g., 10 AM, morning, evening, or 12:30)"

User: "Dr. John Smith"
Bot: "I have some of your appointment details:
     • Doctor: Dr. John Smith
     Please also provide: Date and Time"

User: "tomorrow at 10 AM"
Bot: "✅ Appointment booked successfully!"
```

**Key Features:**
- Remembers previous conversation context
- Merges entities from multiple turns
- Handles follow-up questions ("yes", "ok", "that works")

**Location:** `app.py` - `generate_response()` function (lines 498-549)

### Step 5: Date/Time Normalization

Converts natural language to standardized formats:

**Date Parsing:**
- "tomorrow" → `2026-02-15` (actual date)
- "next Monday" → `2026-02-17` (actual date)
- "today" → `2026-02-14` (actual date)
- "2026-02-01" → `2026-02-01` (already formatted)

**Time Parsing:**
- "10 AM" → `10:00`
- "morning" → `09:00`
- "evening" → `18:00`
- "afternoon" → `14:00`
- "12:30" → `12:30` (already formatted)

**Location:** `ai/date_time_parser.py`

### Step 6: Doctor Matching

Searches for doctor in database using multiple strategies:

1. **Exact Match** - Full name match
2. **Partial Match** - First name or last name
3. **Flexible Matching** - Handles "Dr." prefix variations

**Example:**
```
User Input: "John Smith"
Search Patterns:
  1. "John Smith" (full name)
  2. "John" (first name)
  3. "Smith" (last name)
```

**Location:** `app.py` - `process_appointment_booking()` (lines 781-907)

### Step 7: Availability Validation

Checks if the slot is available:

**Validations:**
1. ✅ **Date Validation** - Not in the past
2. ✅ **Time Validation** - Valid time format (HH:MM)
3. ✅ **Slot Availability** - No existing appointment at same time
4. ✅ **Doctor Exists** - Doctor is in database

**If Slot Not Available:**
- Shows error message
- Suggests alternative times
- Provides contact information

**Location:** `database/availability.py` - `AvailabilityChecker` class

### Step 8: Duplicate Prevention

Prevents booking the same appointment twice:

**Check:**
- Same doctor
- Same date
- Same time
- Recent booking attempt

**Response:**
```
"You already have an appointment booked with these details. 
If you need to make changes, please contact us at +1-234-567-8900."
```

### Step 9: Database Insertion

Creates appointment record:

**SQL Insert:**
```sql
INSERT INTO appointments (patient_name, doctor_id, date, time, status)
VALUES ('Patient', doctor_id, '2026-02-15', '10:00', 'scheduled')
```

**Database Schema:**
- `id` - Auto-increment appointment ID
- `patient_name` - Patient name (default: "Patient")
- `doctor_id` - Foreign key to doctors table
- `date` - Date in YYYY-MM-DD format
- `time` - Time in HH:MM format
- `status` - Status (default: 'scheduled')
- `created_at` - Timestamp

**Location:** `app.py` - `process_appointment_booking()` (lines 889-896)

### Step 10: Confirmation Response

Returns success message with appointment details:

**Response Format:**
```
✅ Appointment booked successfully!

Appointment Details:
• Doctor: Dr. John Smith
• Date: 2026-02-15
• Time: 10:00
• Appointment ID: 1

Please arrive 15 minutes before your scheduled time. 
If you need to cancel or reschedule, please contact us at +1-234-567-8900.
```

---

## 🧩 Module Components

### 1. **Intent Classification** (`ai/intent_model.py`)
- Detects `appointment_booking` intent
- Uses keyword matching + ML models
- Returns intent probability scores

### 2. **Entity Extraction** (`ai/entity_extractor.py`)
- Extracts doctor, date, time from user message
- Uses regex patterns + spaCy (optional)
- Handles natural language variations

### 3. **Date/Time Parser** (`ai/date_time_parser.py`)
- Converts natural language to standardized formats
- Supports: "tomorrow", "next week", "10 AM", "morning", etc.
- Returns YYYY-MM-DD and HH:MM formats

### 4. **Availability Checker** (`database/availability.py`)
- Validates appointment slots
- Checks for conflicts
- Suggests alternative times
- Prevents past date bookings

### 5. **Conversation Memory** (`ai/conversation_memory.py`)
- Tracks conversation history
- Remembers last intent and entities
- Enables multi-turn conversations
- Session-based (30-minute timeout)

### 6. **Main Booking Logic** (`app.py`)
- `generate_response()` - Routes booking requests
- `process_appointment_booking()` - Core booking function
- Handles all validation and database operations

---

## 📊 Database Schema

### Appointments Table
```sql
CREATE TABLE appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT NOT NULL,
    doctor_id INTEGER,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    status TEXT DEFAULT 'scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(doctor_id) REFERENCES doctors(id)
)
```

### Related Tables
- **doctors** - Doctor information
- **departments** - Department information

---

## 🔍 Key Functions

### 1. `process_appointment_booking(doctor, date, time, entities)`

**Purpose:** Main booking function

**Steps:**
1. Find doctor in database
2. Normalize date format
3. Normalize time format
4. Validate availability
5. Insert appointment
6. Return confirmation

**Location:** `app.py` lines 781-907

### 2. `validate_appointment_slot(doctor_id, date, time)`

**Purpose:** Check if slot is available

**Returns:** `(is_valid, message)`

**Validations:**
- Date not in past
- Time format valid
- No existing appointment
- Doctor exists

**Location:** `database/availability.py` lines 201-232

### 3. `parse_date(text)` and `parse_time(text)`

**Purpose:** Convert natural language to standardized formats

**Examples:**
- "tomorrow" → `2026-02-15`
- "10 AM" → `10:00`
- "morning" → `09:00`

**Location:** `ai/date_time_parser.py`

---

## 💬 Example Conversations

### Example 1: Complete Booking in One Message
```
User: "Book appointment with Dr. John Smith tomorrow at 10 AM"
Bot: "✅ Appointment booked successfully!
     Appointment Details:
     • Doctor: Dr. John Smith
     • Date: 2026-02-15
     • Time: 10:00
     • Appointment ID: 1"
```

### Example 2: Multi-Turn Booking
```
User: "I want to book an appointment"
Bot: "I can help you book an appointment. Please provide:
     • Doctor name (e.g., Dr. Sarah Johnson)
     • Date (e.g., tomorrow, next Monday, or 2026-02-01)
     • Time (e.g., 10 AM, morning, evening, or 12:30)"

User: "Dr. John Smith"
Bot: "I have some of your appointment details:
     • Doctor: Dr. John Smith
     Please also provide: Date and Time"

User: "tomorrow"
Bot: "I have some of your appointment details:
     • Doctor: Dr. John Smith
     • Date: 2026-02-15
     Please also provide: Time"

User: "10 AM"
Bot: "✅ Appointment booked successfully!"
```

### Example 3: Slot Not Available
```
User: "Book appointment with Dr. John Smith tomorrow at 10 AM"
Bot: "⚠️ Slot already booked for Dr. John Smith on 2026-02-15 at 10:00.
     Available alternative times: 10:30, 11:00, 11:30
     If you need to make changes, please contact us at +1-234-567-8900."
```

### Example 4: Invalid Date
```
User: "Book appointment with Dr. John Smith yesterday at 10 AM"
Bot: "⚠️ Cannot book appointments in the past for Dr. John Smith on 2026-02-13 at 10:00.
     Available alternative times: 10:00, 10:30, 11:00
     If you need to make changes, please contact us at +1-234-567-8900."
```

---

## 🛡️ Error Handling

### 1. Doctor Not Found
```
"I couldn't find Dr. XYZ in our system. Please check the doctor name 
or use the format 'Dr. [First Name] [Last Name]'.

You can ask me for a list of available doctors."
```

### 2. Invalid Date Format
```
"Please provide a valid date. You can use formats like:
• YYYY-MM-DD (e.g., 2026-02-01)
• Tomorrow
• Next Monday
• Today

You provided: [invalid_date]"
```

### 3. Invalid Time Format
```
"Please provide a valid time. You can use formats like:
• HH:MM (e.g., 12:30)
• 10 AM
• Morning
• Evening
• Afternoon

You provided: [invalid_time]"
```

### 4. Slot Not Available
```
"⚠️ Slot already booked for [Doctor] on [Date] at [Time].
Available alternative times: [suggestions]
If you need to make changes, please contact us at +1-234-567-8900."
```

### 5. Database Error
```
"I apologize, but I encountered an error while booking your appointment: [error]. 
Please try again or contact our reception desk at +1-234-567-8900."
```

---

## 🔄 API Endpoints

### 1. `/api/chat` (POST)
**Main chat endpoint** - Handles all booking requests through natural language

**Request:**
```json
{
  "message": "Book appointment with Dr. John Smith tomorrow at 10 AM",
  "session_id": "abc123"
}
```

**Response:**
```json
{
  "reply": "✅ Appointment booked successfully!...",
  "intent": "appointment_booking"
}
```

### 2. `/api/book` (POST)
**Direct booking endpoint** - For programmatic access

**Request:**
```json
{
  "patient_name": "John Doe",
  "doctor_id": 1,
  "date": "2026-02-15",
  "time": "10:00"
}
```

**Response:**
```json
{
  "status": "success",
  "appointment_id": 1,
  "message": "Appointment booked successfully! ID: 1"
}
```

---

## 🎯 Key Features

### ✅ Natural Language Processing
- Understands "tomorrow", "next week", "10 AM", "morning"
- Flexible date/time formats
- Handles variations in doctor names

### ✅ Multi-Turn Conversations
- Remembers context across messages
- Asks for missing information step by step
- Handles follow-up questions

### ✅ Availability Checking
- Validates slots before booking
- Prevents double bookings
- Suggests alternatives

### ✅ Error Handling
- Comprehensive validation
- User-friendly error messages
- Graceful failure handling

### ✅ Duplicate Prevention
- Checks for recent duplicate bookings
- Prevents accidental double bookings

---

## 📝 Supported Date/Time Formats

### Dates
- **Natural:** "tomorrow", "today", "next Monday", "next week"
- **Formatted:** "2026-02-15", "2026-02-01"
- **Relative:** "day after tomorrow", "next month"

### Times
- **Natural:** "10 AM", "morning", "evening", "afternoon"
- **Formatted:** "10:00", "12:30", "14:00"
- **12-hour:** "10 AM", "2 PM", "11:30 AM"
- **24-hour:** "10:00", "14:00", "23:30"

---

## 🧪 Testing

### Test Case 1: Complete Booking
```
Input: "Book appointment with Dr. John Smith tomorrow at 10 AM"
Expected: Success message with appointment ID
```

### Test Case 2: Multi-Turn
```
Input 1: "I want to book an appointment"
Input 2: "Dr. John Smith"
Input 3: "tomorrow at 10 AM"
Expected: Success message
```

### Test Case 3: Invalid Date
```
Input: "Book appointment with Dr. John Smith yesterday at 10 AM"
Expected: Error message about past dates
```

### Test Case 4: Slot Not Available
```
Input: "Book appointment with Dr. John Smith tomorrow at 10 AM"
(If slot already booked)
Expected: Error message with alternative times
```

---

## 🔧 Configuration

### Session Timeout
- Default: 30 minutes
- Location: `ai/conversation_memory.py`
- Configurable in `ConversationMemory` initialization

### Availability Hours
- Default: 9 AM - 5 PM
- Location: `database/availability.py`
- Configurable in `get_available_slots()`

### Time Slot Interval
- Default: 30 minutes
- Location: `database/availability.py`
- Configurable in `get_available_slots()`

---

## 📚 Related Documentation

- `NATURAL_DATE_TIME_FEATURE.md` - Date/time parsing details
- `AVAILABILITY_AND_CANCELLATION_FEATURES.md` - Availability checking
- `HOW_TO_USE.md` - User guide
- `DEMO_GUIDE.md` - Demo examples

---

## 🎉 Summary

The appointment booking module is a **complete, intelligent system** that:

1. ✅ Understands natural language
2. ✅ Handles multi-turn conversations
3. ✅ Validates all inputs
4. ✅ Checks availability
5. ✅ Prevents duplicates
6. ✅ Provides helpful error messages
7. ✅ Stores appointments in database

**It's ready for production use!** 🚀

