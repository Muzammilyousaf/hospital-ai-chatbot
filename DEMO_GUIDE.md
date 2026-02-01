# 🎯 Hospital AI Chatbot - Demo Guide

## 🚀 Quick Start

### Step 1: Start the Server

**Windows:**
```bash
python app.py
```

**Or use the batch file:**
```bash
run.bat
```

**Linux/Mac:**
```bash
python app.py
```

**Or use the shell script:**
```bash
chmod +x run.sh
./run.sh
```

### Step 2: Open the Chat Interface

Once the server starts, open your web browser and go to:
```
http://localhost:8000
```

You'll see the ChatGPT-like interface ready to chat!

---

## 💬 How to Talk with the Chatbot

### Basic Conversation Flow

The chatbot understands natural English. Just type your message and press **Enter** or click **Send**.

---

## 📝 Example Conversations

### 1. **Greeting**
```
You: Hi
Bot: Hello! I'm your Hospital AI Assistant. I can help you with:
     • 📅 Book appointments
     • 👨‍⚕️ Doctor information
     • ⏰ OPD timings
     • 🏥 Services & facilities
     • 🧾 Patient FAQs
     
     How can I help you today?
```

### 2. **Book an Appointment (Natural Language)**
```
You: I want an appointment tomorrow at 10
Bot: I can help you book an appointment. Please provide:
     • Doctor name (e.g., Dr. Sarah Johnson)
     • Date (e.g., tomorrow, next Monday, or 2026-02-01)
     • Time (e.g., 10 AM, morning, evening, or 12:30)

You: Dr. John Smith
Bot: I have some of your appointment details:
     • Doctor: Dr. John Smith
     
     Please also provide:
     • Date (e.g., tomorrow, next Monday, or 2026-02-01)
     • Time (e.g., 10 AM, morning, evening, or 12:30)

You: tomorrow at 10 AM
Bot: ✅ Appointment booked successfully!
     
     Appointment Details:
     • Doctor: Dr. John Smith
     • Date: 2026-02-15
     • Time: 10:00
     • Appointment ID: 1
     
     Please arrive 15 minutes before your scheduled time...
```

### 3. **Symptom-Based Department Recommendation**
```
You: I have diabetes
Bot: Based on your symptoms (diabetes), I recommend the **Endocrinology** department.
     
     ⚠️ **Important:** I provide general information only. Please consult with a qualified doctor for proper diagnosis and treatment.
     
     Would you like to see available doctors in Endocrinology?

You: Yes
Bot: Doctors in Endocrinology:
     • Dr. Mark Thompson - Endocrinologist
     • Dr. Susan White - Diabetes Specialist
     
     Would you like to book an appointment with any of these doctors?
```

### 4. **Ask About Doctors**
```
You: What doctors are available?
Bot: Our available doctors:
     
     Cardiology:
       • Dr. John Smith - Cardiologist
       • Dr. Sarah Johnson - Cardiologist
     
     Orthopedics:
       • Dr. Michael Brown - Orthopedic Surgeon
       • Dr. Emily Davis - Orthopedic Specialist
     
     ...
```

### 5. **Ask About OPD Timings**
```
You: What are the OPD timings?
Bot: OPD Timings:
     • Monday to Friday: 9:00 AM - 5:00 PM
     • Saturday: 9:00 AM - 1:00 PM
     • Sunday: Closed
     
     Emergency services are available 24/7.
```

### 6. **Ask About Location**
```
You: What is your address?
Bot: Hospital Location:
     
     123 Medical Center Drive
     Healthcare City, HC 12345
     
     Phone: +1-234-567-8900
     Email: info@hospital.com
```

### 7. **Cancel Appointment**
```
You: Cancel my appointment
Bot: To cancel your appointment, please provide:
     • Your appointment ID (e.g., 'Cancel appointment ID 123'), or
     • Your name (e.g., 'Cancel my appointment, I'm John Smith')
     
     You can also contact us directly at +1-234-567-8900.

You: Cancel appointment ID 1
Bot: I can help you cancel appointment #1.
     
     Please confirm by providing your name, or contact us directly at +1-234-567-8900 with:
     • Appointment ID: 1
     • Your name
```

### 8. **Department Query**
```
You: Cardiology
Bot: Doctors in Cardiology:
     • Dr. John Smith - Cardiologist
     • Dr. Sarah Johnson - Cardiologist
     
     Would you like to book an appointment with any of these doctors?
```

### 9. **Natural Date/Time Parsing**
```
You: Book appointment with Dr. Sarah Johnson next Monday morning
Bot: ✅ Appointment booked successfully!
     
     Appointment Details:
     • Doctor: Dr. Sarah Johnson
     • Date: 2026-02-17 (next Monday)
     • Time: 09:00 (morning)
     • Appointment ID: 2
```

### 10. **Emergency Query**
```
You: I'm having chest pain
Bot: 🚨 EMERGENCY ALERT 🚨
     
     Please contact the hospital emergency department immediately or call local emergency services. Do not delay seeking medical attention.
```

---

## 🎨 Quick Action Buttons

The sidebar (on desktop) or interface has quick action buttons:

- **⏰ OPD Timings** - Ask about opening hours
- **📅 Book Appointment** - Start appointment booking
- **👨‍⚕️ Departments** - List all departments
- **🏥 Services** - View hospital services

Click any button to send that query automatically!

---

## 💡 Tips for Best Results

### ✅ Do This:
- **Use natural language**: "I want an appointment tomorrow at 10"
- **Be specific**: "Book with Dr. John Smith"
- **Provide complete info**: Doctor name + Date + Time
- **Ask follow-up questions**: "Yes", "That works", "Show me doctors"

### ❌ Avoid:
- Medical diagnosis requests (bot will redirect you)
- Prescription requests (bot will redirect you)
- Very vague queries without context

---

## 🔄 Multi-Turn Conversations

The chatbot remembers context! You can have natural conversations:

```
You: I want to book an appointment
Bot: I can help you book an appointment. Please provide:
     • Doctor name (e.g., Dr. Sarah Johnson)
     • Date (e.g., tomorrow, next Monday, or 2026-02-01)
     • Time (e.g., 10 AM, morning, evening, or 12:30)

You: Dr. John Smith
Bot: I have some of your appointment details:
     • Doctor: Dr. John Smith
     Please also provide: Date and Time

You: tomorrow
Bot: I have some of your appointment details:
     • Doctor: Dr. John Smith
     • Date: 2026-02-15
     Please also provide: Time

You: 10 AM
Bot: ✅ Appointment booked successfully!
```

---

## 📱 Supported Query Types

### Appointment Booking
- "Book appointment"
- "I want an appointment"
- "Schedule with Dr. John Smith"
- "Appointment tomorrow at 10"

### Doctor Information
- "What doctors are available?"
- "Show me cardiology doctors"
- "Dr. John Smith"
- "Who are the doctors?"

### Symptoms & Departments
- "I have diabetes"
- "I'm feeling chest pain"
- "I have joint pain"
- "Skin allergy"

### General Queries
- "What are the OPD timings?"
- "What is your address?"
- "What services do you offer?"
- "How do I book an appointment?"

### Cancellation
- "Cancel my appointment"
- "Cancel appointment ID 123"
- "I want to cancel"

---

## 🎬 Demo Script

Here's a complete demo conversation you can try:

```
1. Start: "Hi"
2. Ask: "What are the OPD timings?"
3. Ask: "I have diabetes"
4. Ask: "Yes" (to see doctors)
5. Book: "Book appointment with Dr. Mark Thompson tomorrow at 2 PM"
6. Ask: "What is your address?"
7. Cancel: "Cancel my appointment"
```

---

## 🐛 Troubleshooting

### Chatbot not responding?
- Check if server is running (should see "Server running on http://localhost:8000")
- Check browser console for errors (F12)
- Make sure port 8000 is not used by another application

### Getting errors?
- Check terminal/console for error messages
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Restart the server

### Models not loading?
- First run downloads models (may take a few minutes)
- Check internet connection
- Models are cached after first download

---

## 🎯 Quick Test Queries

Try these to test all features:

1. **Greeting**: "Hello"
2. **Timings**: "What are the OPD timings?"
3. **Location**: "Where are you located?"
4. **Doctors**: "What doctors are available?"
5. **Symptom**: "I have chest pain"
6. **Booking**: "Book appointment with Dr. John Smith tomorrow at 10 AM"
7. **Department**: "Cardiology"
8. **Services**: "What services do you offer?"
9. **Emergency**: "I'm having severe chest pain"
10. **Cancellation**: "Cancel my appointment"

---

## 📞 Support

If you encounter issues:
- Check the terminal for error messages
- Review the README.md for setup instructions
- Ensure all dependencies are installed
- Check that the database is initialized

---

## 🎉 You're Ready!

The chatbot is ready to use. Just start the server and start chatting naturally. The bot understands:
- ✅ Natural language
- ✅ Multiple date/time formats
- ✅ Symptoms and diseases
- ✅ Follow-up questions
- ✅ Context from previous messages

Happy chatting! 💬

