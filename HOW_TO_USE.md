# 🏥 How to Use the Hospital AI Chatbot

## 🚀 Step-by-Step Guide

### 1️⃣ Start the Application

**Option A: Using Python directly**
```bash
python app.py
```

**Option B: Using batch file (Windows)**
```bash
run.bat
```

**Option C: Using shell script (Linux/Mac)**
```bash
chmod +x run.sh
./run.sh
```

### What You'll See:
```
📊 Initializing database...
✅ Database initialized
🤖 Loading AI models...
✅ Embedding model loaded for intent classification
✅ DistilBERT model loaded (for future fine-tuning)
✅ RAG engine loaded: 1 documents
✅ AI components loaded
============================================================
🏥 Hospital AI Chatbot - Starting Server
============================================================
Server running on: http://localhost:8000
Chat interface: http://localhost:8000/
API health: http://localhost:8000/api/health
============================================================
```

### 2️⃣ Open Your Browser

Go to: **http://localhost:8000**

You'll see a ChatGPT-like interface with:
- Sidebar with quick action buttons (desktop)
- Chat area in the middle
- Input box at the bottom

---

## 💬 How to Chat

### Basic Usage

1. **Type your message** in the input box at the bottom
2. **Press Enter** or click the **Send button** (arrow icon)
3. **Wait for response** - The bot will process and reply
4. **Continue the conversation** - The bot remembers context!

---

## 🎯 Example Conversations

### Example 1: Simple Greeting
```
You: Hi
Bot: Hello! I'm your Hospital AI Assistant...
```

### Example 2: Book Appointment (Step by Step)
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

You: tomorrow at 10 AM
Bot: ✅ Appointment booked successfully!
     Appointment Details:
     • Doctor: Dr. John Smith
     • Date: 2026-02-15
     • Time: 10:00
     • Appointment ID: 1
```

### Example 3: All Details at Once
```
You: Book appointment with Dr. Sarah Johnson tomorrow at 2 PM
Bot: ✅ Appointment booked successfully!
```

### Example 4: Symptom-Based Help
```
You: I have diabetes
Bot: Based on your symptoms (diabetes), I recommend the **Endocrinology** department.
     Would you like to see available doctors in Endocrinology?

You: Yes
Bot: Doctors in Endocrinology:
     • Dr. Mark Thompson - Endocrinologist
     • Dr. Susan White - Diabetes Specialist
```

### Example 5: Quick Questions
```
You: What are the OPD timings?
Bot: OPD Timings:
     • Monday to Friday: 9:00 AM - 5:00 PM
     • Saturday: 9:00 AM - 1:00 PM
     • Sunday: Closed

You: What is your address?
Bot: Hospital Location:
     123 Medical Center Drive
     Healthcare City, HC 12345
```

---

## 🎨 Using Quick Action Buttons

On the left sidebar (desktop view), you'll see buttons:

- **⏰ OPD Timings** - Click to ask about timings
- **📅 Book Appointment** - Click to start booking
- **👨‍⚕️ Departments** - Click to see departments
- **🏥 Services** - Click to see services

**Just click any button** and it will send that query automatically!

---

## 📝 What You Can Ask

### ✅ Appointment Booking
- "Book appointment"
- "I want an appointment tomorrow at 10"
- "Schedule with Dr. John Smith"
- "Book me for next Monday morning"

### ✅ Doctor Information
- "What doctors are available?"
- "Show me cardiology doctors"
- "Dr. John Smith"
- "Who are the doctors?"

### ✅ Symptoms & Health
- "I have diabetes"
- "I'm feeling chest pain"
- "I have joint pain"
- "Skin allergy"

### ✅ General Information
- "What are the OPD timings?"
- "What is your address?"
- "What services do you offer?"
- "How do I book an appointment?"

### ✅ Cancellation
- "Cancel my appointment"
- "Cancel appointment ID 123"

---

## 💡 Pro Tips

### Tip 1: Use Natural Language
✅ **Good**: "I want an appointment tomorrow at 10"
❌ **Avoid**: "appt tom 10"

### Tip 2: Provide Complete Information
✅ **Good**: "Book appointment with Dr. John Smith tomorrow at 10 AM"
❌ **Partial**: "Book appointment" (bot will ask for details)

### Tip 3: The Bot Remembers Context
✅ You can provide information step by step:
```
You: I want an appointment
Bot: Please provide doctor, date, time
You: Dr. John Smith
Bot: Please provide date and time
You: tomorrow at 10
Bot: ✅ Booked!
```

### Tip 4: Use Quick Actions
Click the sidebar buttons for instant queries!

---

## 🎬 Complete Demo Walkthrough

Try this complete conversation:

```
1. You: "Hi"
   Bot: Greets you and lists capabilities

2. You: "What are the OPD timings?"
   Bot: Shows OPD timings

3. You: "I have diabetes"
   Bot: Recommends Endocrinology department

4. You: "Yes" (to see doctors)
   Bot: Lists Endocrinology doctors

5. You: "Book appointment with Dr. Mark Thompson tomorrow at 2 PM"
   Bot: Books appointment successfully

6. You: "What is your address?"
   Bot: Shows hospital location

7. You: "Cancel my appointment"
   Bot: Asks for appointment ID or name
```

---

## 🔄 Multi-Turn Conversations

The chatbot **remembers** your conversation! You can:

- Provide information in multiple messages
- Use follow-up questions like "Yes", "That works"
- Reference previous parts of the conversation

**Example:**
```
You: I want an appointment
Bot: Please provide doctor, date, time

You: Dr. John Smith
Bot: Please provide date and time

You: tomorrow
Bot: Please provide time

You: 10 AM
Bot: ✅ Appointment booked!
```

---

## 📱 Mobile Usage

On mobile devices:
- Sidebar is hidden (more screen space)
- Same chat interface
- Touch-friendly buttons
- Responsive text sizing

---

## ⚠️ Important Notes

### What the Bot CAN Do:
✅ Book appointments
✅ Provide doctor information
✅ Answer FAQs
✅ Recommend departments based on symptoms
✅ Show timings and location
✅ Cancel appointments

### What the Bot CANNOT Do:
❌ Provide medical diagnosis
❌ Prescribe medications
❌ Give treatment advice
❌ Replace a doctor's consultation

**For medical emergencies, the bot will direct you to emergency services immediately.**

---

## 🐛 Troubleshooting

### Problem: Chatbot not responding
**Solution:**
- Check if server is running (terminal should show "Server running")
- Refresh browser
- Check browser console for errors (F12)

### Problem: Can't access http://localhost:8000
**Solution:**
- Make sure server is running
- Try http://127.0.0.1:8000
- Check if port 8000 is available

### Problem: Models not loading
**Solution:**
- First run downloads models (wait a few minutes)
- Check internet connection
- Models are cached after first download

### Problem: Getting errors
**Solution:**
- Check terminal for error messages
- Make sure all dependencies installed: `pip install -r requirements.txt`
- Restart the server

---

## 🎯 Quick Test

Try these 5 quick queries to test everything:

1. **"Hi"** - Test greeting
2. **"What are the OPD timings?"** - Test information query
3. **"I have diabetes"** - Test symptom mapping
4. **"Book appointment with Dr. John Smith tomorrow at 10 AM"** - Test booking
5. **"What is your address?"** - Test location query

---

## 📞 Need Help?

- Check `README.md` for setup instructions
- Check `QUICKSTART.md` for quick start guide
- Check `SAMPLE_INPUTS.md` for more example queries
- Review terminal output for error messages

---

## 🎉 You're All Set!

The chatbot is ready to use. Just:
1. Start the server (`python app.py`)
2. Open browser (http://localhost:8000)
3. Start chatting!

**Happy chatting!** 💬✨

