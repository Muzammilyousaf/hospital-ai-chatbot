# 🏥 AI Hospital Chatbot

![Hospital Chatbot Demo](https://github.com/Muzammilyousaf/hospital-ai-chatbot/blob/master/demo-screenshot.png)

**PyTorch + Flask + RAG (100% Free, No Paid APIs)**

This repository provides a **professional, production-style starter setup** for building an **AI-powered hospital chatbot** using **PyTorch**, **Flask**, and **Retrieval-Augmented Generation (RAG)**. The system is fast, secure, offline-capable, and suitable for real hospital environments.

---

## 🎯 Project Goals

* Provide instant, accurate hospital information
* Enable appointment booking via chat
* Avoid paid APIs and cloud dependencies
* Prevent medical diagnosis or hallucinations
* Use AI for understanding, not unsafe generation

---

## 🧠 AI Architecture (RAG-Based)

```
User (Web UI)
   ↓
Flask Backend (API)
   ↓
AI Layer (PyTorch)
   ├─ Intent Classification (DistilBERT)
   ├─ Semantic Search (RAG + FAISS)
   ├─ Entity Extraction (spaCy)
   ├─ Conversation Memory (Context Tracking)
   ├─ Symptom Mapping (Department Routing)
   ├─ Natural Date/Time Parsing
   ↓
Hospital Knowledge Base (Vector DB + SQLite)
   ├─ FAISS Vector Store
   ├─ SQLite Database
   ↓
Business Logic Layer
   ├─ Availability Checking
   ├─ Appointment Booking
   ├─ Response Generation
   ↓
Safe Response (No Medical Advice)
```

---

## 🛠️ Technology Stack

### Backend

* **Python 3.10+**
* **Flask** – API & web UI
* **PyTorch** – AI models
* **Sentence-Transformers** – embeddings
* **FAISS** – vector similarity search
* **spaCy** – entity extraction
* **SQLite** – hospital database

### Frontend

* Flask Templates (HTML/CSS/JS)
* Responsive design

---

## 📁 Project Structure

```
hospital-chatbot/
├── app.py                      # Flask application (main entry point)
├── ai/
│   ├── intent_model.py         # PyTorch intent classification (DistilBERT)
│   ├── rag_engine.py           # FAISS RAG engine (semantic search)
│   ├── entity_extractor.py     # spaCy entity extraction (doctor, date, time)
│   ├── conversation_memory.py  # Multi-turn conversation context tracking
│   ├── symptom_mapper.py       # Symptom-to-department mapping
│   └── date_time_parser.py     # Natural date/time parsing ("tomorrow", "next week")
├── database/
│   ├── db.py                   # Database connection & utilities
│   ├── schema.py              # Database schema definitions
│   ├── availability.py        # Availability checking & slot validation
│   └── hospital.db            # SQLite database (auto-created)
├── backend/
│   └── safety.py              # Safety filters (no medical advice)
├── data/
│   ├── hospital_knowledge/    # Hospital documents (FAQs, policies)
│   └── vector_db/             # FAISS vector database (embeddings)
│       ├── index.faiss        # FAISS index file
│       └── documents.pkl     # Document metadata
├── templates/
│   └── chat.html              # Chat interface (HTML)
├── static/
│   ├── style.css              # Styles (CSS)
│   └── script.js              # Frontend logic (JavaScript)
├── scripts/
│   ├── ingest_data.py         # Data ingestion (builds FAISS index)
│   └── reset_database.py      # Database reset utility
├── requirements.txt           # Python dependencies
├── run.sh / run.bat          # Startup scripts
└── README.md                 # This file
```

---

## 🧾 Database Schema

### Tables

* **departments** - Hospital departments
* **doctors** - Doctor information
* **services** - Hospital services
* **appointments** - Patient appointments
* **faqs** - Frequently asked questions

All tables are automatically created with sample data on first run.

---

## ✅ Key Features

### 1. Availability Checking
Before confirming a booking, the system validates the requested slot:

* ✅ Prevents double bookings (conflict check)
* ✅ Rejects past dates or invalid times
* ✅ Suggests alternative time slots when unavailable
* ✅ Validates time format

**Where it lives:**
* `database/availability.py` → `AvailabilityChecker` class
* Integrated in `process_appointment_booking()` (in `app.py`)

**Example:**
```
User: "Book appointment with Dr. John Smith tomorrow at 10:00"
Bot: ⚠️ "Slot already booked. Available alternatives: 10:30, 11:00, 11:30"
```

### 2. Appointment Cancellation
Cancellation is supported through chat or API:

* **Chat:** "Cancel my appointment" → prompts for appointment ID or name
* **API:** `POST /api/cancel` with `appointment_id` or `patient_name`

**Example API call:**
```bash
curl -X POST "http://localhost:8000/api/cancel" \
  -H "Content-Type: application/json" \
  -d "{\"appointment_id\": 123}"
```

### 3. Multi-Turn Conversations
The system maintains conversation context across multiple turns:

* Session-based memory (30-minute timeout)
* Entity persistence (remembers doctor name, date, time across turns)
* Follow-up detection
* Context-aware responses

**Example:**
```
Turn 1: User: "Book appointment"
Turn 2: User: "Dr. John Smith" (bot remembers booking intent)
Turn 3: User: "tomorrow at 10 AM" (bot combines all info)
```

### 4. Natural Date/Time Parsing
Supports natural language date/time expressions:

* **Dates:** "tomorrow", "next week", "next Monday", "February 15"
* **Times:** "10 AM", "morning", "evening", "12:30"

**Location:** `ai/date_time_parser.py`

### 5. Symptom Mapping
Maps symptoms to departments and suggests relevant doctors:

* Dictionary-based symptom-to-department mapping
* Automatic department routing
* Doctor suggestions based on symptoms

**Location:** `ai/symptom_mapper.py`

### 6. Flexible Doctor Search
Supports partial name matching:

* "john" → finds "Dr. John Smith", "Dr. Sarah Johnson"
* Case-insensitive matching
* Partial string matching

### 7. RAG with Relevance Filtering
Semantic search with quality control:

* Minimum relevance score: 0.3
* Top-k retrieval (default: 2)
* Skips RAG for specific intents (booking, simple responses)

---

## 📚 RAG Knowledge Sources

Used to answer patient queries:

* Hospital FAQs
* OPD timings
* Doctor schedules
* Departments & services
* Hospital policies

All documents are:

1. Cleaned
2. Chunked
3. Embedded using PyTorch models
4. Stored in FAISS

---

## 🤖 AI Models & Components (PyTorch)

### Intent Classification

* **Model:** `distilbert-base-uncased` (HuggingFace)
* **Classes:**
  * `appointment_booking` - Book appointments
  * `doctor_info` - Get doctor information
  * `services` - Hospital services inquiry
  * `faq` - General questions
  * `emergency` - Emergency situations
  * `cancel_appointment` - Cancel appointments
* **Location:** `ai/intent_model.py`
* **Features:** Context-aware classification using conversation history

### Embeddings (RAG)

* **Model:** `all-MiniLM-L6-v2` (Sentence-Transformers)
* **Purpose:** Semantic similarity search
* **Location:** `ai/rag_engine.py`
* **Features:** Relevance filtering (min score: 0.3), top-k retrieval

### Entity Extraction

* **Library:** spaCy (`en_core_web_sm`)
* **Extracts:**
  * Doctor names (with fuzzy matching)
  * Dates (natural language: "tomorrow", "next week")
  * Times (natural language: "10 AM", "morning")
  * Departments
* **Location:** `ai/entity_extractor.py`
* **Features:** Context-aware extraction, conversation memory integration

### Conversation Memory

* **Purpose:** Multi-turn conversation support
* **Features:**
  * Session-based context tracking
  * Conversation summary generation
  * Entity persistence across turns
  * Follow-up detection
* **Location:** `ai/conversation_memory.py`
* **Timeout:** 30 minutes (configurable)

### Symptom Mapping

* **Purpose:** Map symptoms to departments
* **Features:**
  * Dictionary-based symptom-to-department mapping
  * Doctor suggestions based on symptoms
* **Location:** `ai/symptom_mapper.py`

### Natural Date/Time Parsing

* **Purpose:** Parse natural language dates/times
* **Supports:**
  * Relative dates: "tomorrow", "next week", "next Monday"
  * Absolute dates: "2026-02-15", "February 15"
  * Times: "10 AM", "morning", "evening", "12:30"
* **Location:** `ai/date_time_parser.py`

---

## 🛡️ Safety & Compliance

Hard rules enforced in backend:

* ❌ No diagnosis
* ❌ No prescriptions
* ❌ No medical advice
* ✅ Emergency redirection

**Emergency Response:**

> "Please contact the hospital emergency department immediately or call local emergency services."

---

## ⚡ Performance

| Component        | Avg Time |
| ---------------- | -------- |
| Intent Detection | 20 ms    |
| RAG Search       | 30 ms    |
| Business Logic   | 10 ms    |
| Total Response   | < 100 ms |

---

## 🚀 Complete Workflow (Step-by-Step)

### Detailed Chat Flow

```
1. User Input
   └─> User sends message via web UI or API
   
2. Session Management
   └─> Generate/retrieve session_id
   └─> Load conversation history (if exists)
   
3. Intent Classification
   └─> Use DistilBERT model to classify intent:
       • appointment_booking
       • doctor_info
       • services
       • faq
       • emergency
       • cancel_appointment
   └─> Consider conversation context for better accuracy
   
4. Entity Extraction
   └─> Extract entities using spaCy + regex:
       • Doctor name (flexible matching: "john" → "Dr. John Smith")
       • Date (natural: "tomorrow", "next Monday" → parsed date)
       • Time (natural: "10 AM", "morning" → parsed time)
       • Department (from symptom mapping if applicable)
   └─> Use conversation context to fill missing entities
   
5. Symptom Mapping (if applicable)
   └─> Map symptoms to departments
   └─> Suggest relevant doctors
   
6. RAG Search (Conditional)
   └─> Skip RAG for:
       • Appointment booking requests
       • Simple responses ("yes", "ok")
       • Specific doctor queries
   └─> Otherwise: Search FAISS vector DB for relevant info
   └─> Filter by relevance score (min 0.3)
   
7. Business Logic Execution
   └─> Route based on intent:
       
       A. Appointment Booking:
          • Check if all details present (doctor, date, time)
          • If missing → Ask for missing info (multi-turn)
          • If complete → Validate availability
          • Check for conflicts (double booking)
          • Validate date (no past dates)
          • Suggest alternatives if slot unavailable
          • Create appointment in database
          
       B. Doctor Info:
          • Search by name (partial match supported)
          • Search by department
          • Return doctor details (name, department, specialization)
          
       C. Services/FAQ:
          • Use RAG results + database queries
          • Return formatted response
          
       D. Emergency:
          • Return emergency contact info
          • No medical advice
          
       E. Cancellation:
          • Extract appointment ID or patient name
          • Find appointment in database
          • Update status to 'cancelled'
          • Return confirmation
   
8. Response Generation
   └─> Format response based on intent
   └─> Include relevant information
   └─> Ensure no medical advice/diagnosis
   └─> Add helpful suggestions if needed
   
9. Conversation Memory Update
   └─> Store user message + intent + entities
   └─> Store bot response
   └─> Update conversation summary
   └─> Enable context-aware follow-ups
   
10. Response Return
    └─> Return JSON with:
        • reply (response text)
        • intent (detected intent)
        • entities (extracted entities)
        • session_id
        • is_follow_up (boolean)
        • success (boolean)
```

### Multi-Turn Conversation Example

```
Turn 1:
User: "I want to book an appointment"
Bot: "I can help you book an appointment. Please provide:
     • Doctor name (e.g., Dr. Sarah Johnson)
     • Date (e.g., tomorrow, next Monday, or 2026-02-01)
     • Time (e.g., 10 AM, morning, or 12:30)"

Turn 2:
User: "Dr. John Smith"
Bot: "I have some of your appointment details:
     • Doctor: Dr. John Smith
     Please also provide: Date and Time"

Turn 3:
User: "tomorrow at 10 AM"
Bot: "✅ Appointment booked successfully!
     Appointment ID: 123
     Doctor: Dr. John Smith
     Date: 2026-02-15
     Time: 10:00"
```

---

## 📦 Installation

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Install spaCy Model

```bash
python -m spacy download en_core_web_sm
```

**Note:** If you encounter PyTorch DLL errors on Windows:
- Install Visual C++ Redistributable: https://aka.ms/vs/17/release/vc_redist.x64.exe

### Step 3: Ingest Hospital Data

```bash
python scripts/ingest_data.py
```

This will:
- Load documents from `data/hospital_knowledge/`
- Create embeddings
- Build FAISS index

### Step 4: Run the Application

```bash
python app.py
```

The server will start on `http://localhost:8000`

---

## 🔌 API Endpoints

### 1. Chat Endpoint
**POST** `/api/chat`

Main chat interface for user interactions.

**Request:**
```json
{
  "message": "What are the OPD timings?",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "reply": "Our OPD timings are...",
  "intent": "faq",
  "entities": {},
  "session_id": "uuid-here",
  "is_follow_up": false,
  "success": true
}
```

### 2. Book Appointment
**POST** `/api/book`

Direct appointment booking endpoint.

**Request:**
```json
{
  "doctor_name": "Dr. John Smith",
  "date": "2026-02-15",
  "time": "10:00",
  "patient_name": "John Doe"
}
```

**Response:**
```json
{
  "status": "success",
  "appointment_id": 123,
  "message": "Appointment booked successfully"
}
```

### 3. Get Doctors
**GET** `/api/doctors`

Retrieve list of doctors (optionally filtered by department).

**Query Parameters:**
- `department` (optional): Filter by department name

**Example:**
```bash
curl "http://localhost:8000/api/doctors?department=Cardiology"
```

### 4. Get Departments
**GET** `/api/departments`

Retrieve list of all departments.

**Example:**
```bash
curl "http://localhost:8000/api/departments"
```

### 5. Cancel Appointment
**POST** `/api/cancel`

Cancel an existing appointment.

**Request:**
```json
{
  "appointment_id": 123
}
```
OR
```json
{
  "patient_name": "John Doe"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Appointment cancelled successfully",
  "appointment_details": {...}
}
```

### 6. Health Check
**GET** `/api/health`

Check if the server is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-14T10:00:00"
}
```

---

## 🧪 Testing

### Using cURL

**Test chat endpoint:**
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"What are the OPD timings?\"}"
```

**Test appointment booking:**
```bash
curl -X POST "http://localhost:8000/api/book" \
  -H "Content-Type: application/json" \
  -d "{\"doctor_name\": \"Dr. John Smith\", \"date\": \"2026-02-15\", \"time\": \"10:00\", \"patient_name\": \"John Doe\"}"
```

**Get doctors list:**
```bash
curl "http://localhost:8000/api/doctors"
```

**Health check:**
```bash
curl http://localhost:8000/api/health
```

---

## 📈 Future Enhancements

* Admin dashboard
* Doctor slot validation
* Multilingual support
* Voice chatbot
* WhatsApp integration

---

## 🏁 Summary

This system is:

* AI-powered but safe
* Fast and offline-capable
* Free and open-source
* Suitable for real hospitals
* Ideal for academic & production use

---

## 📌 Ideal For

* Hospital IT systems
* Final Year Projects (FYP)
* Healthcare startups
* AI research demos

---

**Built with PyTorch + Flask + RAG**
