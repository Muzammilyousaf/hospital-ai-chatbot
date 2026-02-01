# 🗄️ Database Setup Guide

## 📊 Database Overview

The database contains **complete demo data** with:
- **12 Departments** - All major hospital departments
- **36 Doctors** - 3 doctors per department
- **6 Services** - Hospital services
- **5 FAQs** - Common questions

---

## 🚀 Quick Setup

### Option 1: Automatic Setup (First Run)
The database is **automatically created** when you run:
```bash
python app.py
```

The first time you run the app, it will:
- Create all tables
- Insert all departments
- Insert all 36 doctors (3 per department)
- Insert services and FAQs

### Option 2: Reset Database (Refresh Data)
If you want to reset the database with fresh data:
```bash
python scripts/reset_database.py
```

This will:
- Drop all existing tables
- Recreate everything with fresh demo data
- Show you a summary of what was created

---

## 📋 Departments & Doctors

### 1. **Cardiology** (3 doctors)
- Dr. John Smith - Cardiologist
- Dr. Sarah Johnson - Cardiologist
- Dr. James Wilson - Cardiac Surgeon

### 2. **Orthopedics** (3 doctors)
- Dr. Michael Brown - Orthopedic Surgeon
- Dr. Emily Davis - Orthopedic Specialist
- Dr. Christopher Taylor - Sports Medicine Specialist

### 3. **Pediatrics** (3 doctors)
- Dr. Robert Wilson - Pediatrician
- Dr. Lisa Anderson - Pediatrician
- Dr. Maria Garcia - Pediatric Neurologist

### 4. **General Medicine** (3 doctors)
- Dr. David Martinez - General Physician
- Dr. Jennifer Lee - General Physician
- Dr. William Chen - Family Medicine

### 5. **Emergency** (3 doctors)
- Dr. Amanda White - Emergency Medicine
- Dr. Thomas Anderson - Emergency Physician
- Dr. Patricia Moore - Trauma Specialist

### 6. **Endocrinology** (3 doctors)
- Dr. Mark Thompson - Endocrinologist
- Dr. Susan White - Diabetes Specialist
- Dr. Richard Harris - Thyroid Specialist

### 7. **Dermatology** (3 doctors)
- Dr. Rachel Green - Dermatologist
- Dr. Kevin Johnson - Cosmetic Dermatologist
- Dr. Nicole Brown - Skin Cancer Specialist

### 8. **Gastroenterology** (3 doctors)
- Dr. Steven Clark - Gastroenterologist
- Dr. Michelle Lewis - Hepatologist
- Dr. Daniel Walker - GI Surgeon

### 9. **Ophthalmology** (3 doctors)
- Dr. Laura Hall - Ophthalmologist
- Dr. Robert Allen - Retina Specialist
- Dr. Catherine Young - Cataract Surgeon

### 10. **Neurology** (3 doctors)
- Dr. Matthew King - Neurologist
- Dr. Jessica Wright - Epilepsy Specialist
- Dr. Andrew Scott - Stroke Specialist

### 11. **Urology** (3 doctors)
- Dr. Benjamin Adams - Urologist
- Dr. Samantha Baker - Urological Surgeon
- Dr. Ryan Hill - Kidney Specialist

### 12. **ENT** (3 doctors)
- Dr. Olivia Nelson - ENT Specialist
- Dr. Jason Carter - Otolaryngologist
- Dr. Stephanie Mitchell - Head & Neck Surgeon

---

## 🧪 Testing the Database

### Test Query 1: List All Departments
```bash
# In chatbot:
"What departments are available?"
```

### Test Query 2: List Doctors in Department
```bash
# In chatbot:
"Cardiology"
# or
"Show me cardiology doctors"
```

### Test Query 3: Book Appointment
```bash
# In chatbot:
"Book appointment with Dr. John Smith tomorrow at 10 AM"
```

### Test Query 4: Symptom Mapping
```bash
# In chatbot:
"I have diabetes"
# Should recommend Endocrinology department
```

---

## 🔍 Database Schema

### Tables

1. **departments**
   - id (INTEGER PRIMARY KEY)
   - name (TEXT)
   - description (TEXT)

2. **doctors**
   - id (INTEGER PRIMARY KEY)
   - name (TEXT)
   - department_id (INTEGER, FOREIGN KEY)
   - specialization (TEXT)
   - availability (TEXT)

3. **appointments**
   - id (INTEGER PRIMARY KEY)
   - patient_name (TEXT)
   - doctor_id (INTEGER, FOREIGN KEY)
   - date (TEXT)
   - time (TEXT)
   - status (TEXT)
   - created_at (TIMESTAMP)

4. **services**
   - id (INTEGER PRIMARY KEY)
   - name (TEXT)
   - description (TEXT)

5. **faqs**
   - id (INTEGER PRIMARY KEY)
   - question (TEXT)
   - answer (TEXT)

---

## 📁 Database Location

The database file is stored at:
```
database/hospital.db
```

This is a SQLite database file that can be:
- Viewed with any SQLite browser
- Backed up by copying the file
- Reset by deleting the file (will recreate on next run)

---

## 🔄 Resetting the Database

### Method 1: Using Reset Script
```bash
python scripts/reset_database.py
```

### Method 2: Manual Reset
```bash
# Delete the database file
rm database/hospital.db  # Linux/Mac
del database\hospital.db  # Windows

# Then run the app
python app.py
```

---

## ✅ Verification

After setup, verify the database:

```bash
python scripts/reset_database.py
```

You should see:
```
✅ Database reset complete!
📊 Departments: 12
👨‍⚕️ Total Doctors: 36

📋 Doctors by Department:
  • Cardiology: 3 doctors
  • Orthopedics: 3 doctors
  • Pediatrics: 3 doctors
  ...
```

---

## 🎯 Demo Ready!

The database is now ready with:
- ✅ All 12 departments
- ✅ 36 doctors (3 per department)
- ✅ Complete specialization info
- ✅ Availability schedules
- ✅ Services and FAQs

**You can now run the chatbot and test all features!**

```bash
python app.py
```

Then visit: **http://localhost:8000**

---

## 💡 Tips

1. **First Run**: Database is created automatically
2. **Reset**: Use `reset_database.py` to refresh data
3. **Backup**: Copy `database/hospital.db` to backup
4. **View Data**: Use SQLite browser to inspect database
5. **Customize**: Edit `database/schema.py` to add more doctors

---

## 🐛 Troubleshooting

### Issue: "Database not found"
**Solution**: Run `python app.py` - it creates the database automatically

### Issue: "No doctors in department"
**Solution**: Run `python scripts/reset_database.py` to refresh data

### Issue: "Old data showing"
**Solution**: Delete `database/hospital.db` and restart the app

---

## 📞 Need Help?

- Check `README.md` for general setup
- Check `HOW_TO_USE.md` for chatbot usage
- Review `database/schema.py` for data structure

---

**Database is ready for demo! 🎉**

