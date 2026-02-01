"""
Database schema for hospital chatbot
"""

from database.db import get_db_connection

def create_tables():
    """Create all database tables."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Departments
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
    ''')
    
    # Doctors
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department_id INTEGER,
            specialization TEXT,
            availability TEXT,
            FOREIGN KEY(department_id) REFERENCES departments(id)
        )
    ''')
    
    # Services
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
    ''')
    
    # Appointments
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            doctor_id INTEGER,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            status TEXT DEFAULT 'scheduled',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(doctor_id) REFERENCES doctors(id)
        )
    ''')
    
    # FAQs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    
    # Insert sample data if tables are empty
    _insert_sample_data(cursor, conn)
    
    conn.close()
    # Suppress print to reduce noise (already printed in app.py)

def _insert_sample_data(cursor, conn):
    """Insert sample data if tables are empty."""
    
    # Check if data exists
    cursor.execute('SELECT COUNT(*) FROM departments')
    if cursor.fetchone()[0] > 0:
        return  # Data already exists
    
    # Departments
    departments = [
        ('Cardiology', 'Heart and cardiovascular care'),
        ('Orthopedics', 'Bone and joint care'),
        ('Pediatrics', 'Child healthcare'),
        ('General Medicine', 'General healthcare services'),
        ('Emergency', '24/7 emergency services'),
        ('Endocrinology', 'Diabetes and hormone disorders'),
        ('Dermatology', 'Skin and dermatological care'),
        ('Gastroenterology', 'Digestive system and stomach care'),
        ('Ophthalmology', 'Eye and vision care'),
        ('Neurology', 'Brain and nervous system care'),
        ('Urology', 'Urinary tract and kidney care'),
        ('ENT', 'Ear, nose, and throat care')
    ]
    cursor.executemany('INSERT INTO departments (name, description) VALUES (?, ?)', departments)
    
    # Doctors - At least 2 doctors per department for demo
    doctors = [
        # Cardiology (Department ID: 1)
        ('Dr. John Smith', 1, 'Cardiologist', 'Mon-Fri 9AM-5PM'),
        ('Dr. Sarah Johnson', 1, 'Cardiologist', 'Mon-Fri 10AM-6PM'),
        ('Dr. James Wilson', 1, 'Cardiac Surgeon', 'Mon-Fri 8AM-4PM'),
        
        # Orthopedics (Department ID: 2)
        ('Dr. Michael Brown', 2, 'Orthopedic Surgeon', 'Mon-Fri 9AM-5PM'),
        ('Dr. Emily Davis', 2, 'Orthopedic Specialist', 'Mon-Fri 8AM-4PM'),
        ('Dr. Christopher Taylor', 2, 'Sports Medicine Specialist', 'Mon-Fri 10AM-6PM'),
        
        # Pediatrics (Department ID: 3)
        ('Dr. Robert Wilson', 3, 'Pediatrician', 'Mon-Fri 9AM-5PM'),
        ('Dr. Lisa Anderson', 3, 'Pediatrician', 'Mon-Fri 10AM-6PM'),
        ('Dr. Maria Garcia', 3, 'Pediatric Neurologist', 'Mon-Fri 8AM-4PM'),
        
        # General Medicine (Department ID: 4)
        ('Dr. David Martinez', 4, 'General Physician', 'Mon-Sat 9AM-5PM'),
        ('Dr. Jennifer Lee', 4, 'General Physician', 'Mon-Fri 8AM-4PM'),
        ('Dr. William Chen', 4, 'Family Medicine', 'Mon-Fri 9AM-5PM'),
        
        # Emergency (Department ID: 5)
        ('Dr. Amanda White', 5, 'Emergency Medicine', '24/7 Rotating Shifts'),
        ('Dr. Thomas Anderson', 5, 'Emergency Physician', '24/7 Rotating Shifts'),
        ('Dr. Patricia Moore', 5, 'Trauma Specialist', '24/7 Rotating Shifts'),
        
        # Endocrinology (Department ID: 6)
        ('Dr. Mark Thompson', 6, 'Endocrinologist', 'Mon-Fri 9AM-5PM'),
        ('Dr. Susan White', 6, 'Diabetes Specialist', 'Mon-Fri 10AM-6PM'),
        ('Dr. Richard Harris', 6, 'Thyroid Specialist', 'Mon-Fri 8AM-4PM'),
        
        # Dermatology (Department ID: 7)
        ('Dr. Rachel Green', 7, 'Dermatologist', 'Mon-Fri 9AM-5PM'),
        ('Dr. Kevin Johnson', 7, 'Cosmetic Dermatologist', 'Mon-Fri 10AM-6PM'),
        ('Dr. Nicole Brown', 7, 'Skin Cancer Specialist', 'Mon-Fri 8AM-4PM'),
        
        # Gastroenterology (Department ID: 8)
        ('Dr. Steven Clark', 8, 'Gastroenterologist', 'Mon-Fri 9AM-5PM'),
        ('Dr. Michelle Lewis', 8, 'Hepatologist', 'Mon-Fri 10AM-6PM'),
        ('Dr. Daniel Walker', 8, 'GI Surgeon', 'Mon-Fri 8AM-4PM'),
        
        # Ophthalmology (Department ID: 9)
        ('Dr. Laura Hall', 9, 'Ophthalmologist', 'Mon-Fri 9AM-5PM'),
        ('Dr. Robert Allen', 9, 'Retina Specialist', 'Mon-Fri 10AM-6PM'),
        ('Dr. Catherine Young', 9, 'Cataract Surgeon', 'Mon-Fri 8AM-4PM'),
        
        # Neurology (Department ID: 10)
        ('Dr. Matthew King', 10, 'Neurologist', 'Mon-Fri 9AM-5PM'),
        ('Dr. Jessica Wright', 10, 'Epilepsy Specialist', 'Mon-Fri 10AM-6PM'),
        ('Dr. Andrew Scott', 10, 'Stroke Specialist', 'Mon-Fri 8AM-4PM'),
        
        # Urology (Department ID: 11)
        ('Dr. Benjamin Adams', 11, 'Urologist', 'Mon-Fri 9AM-5PM'),
        ('Dr. Samantha Baker', 11, 'Urological Surgeon', 'Mon-Fri 10AM-6PM'),
        ('Dr. Ryan Hill', 11, 'Kidney Specialist', 'Mon-Fri 8AM-4PM'),
        
        # ENT (Department ID: 12)
        ('Dr. Olivia Nelson', 12, 'ENT Specialist', 'Mon-Fri 9AM-5PM'),
        ('Dr. Jason Carter', 12, 'Otolaryngologist', 'Mon-Fri 10AM-6PM'),
        ('Dr. Stephanie Mitchell', 12, 'Head & Neck Surgeon', 'Mon-Fri 8AM-4PM')
    ]
    cursor.executemany(
        'INSERT INTO doctors (name, department_id, specialization, availability) VALUES (?, ?, ?, ?)',
        doctors
    )
    
    # Services
    services = [
        ('Emergency Services', '24/7 emergency care'),
        ('Outpatient Services', 'General outpatient care'),
        ('Laboratory Services', 'Medical testing and analysis'),
        ('Radiology', 'X-ray and imaging services'),
        ('Pharmacy', 'Prescription medications'),
        ('Ambulance Services', 'Emergency transport')
    ]
    cursor.executemany('INSERT INTO services (name, description) VALUES (?, ?)', services)
    
    # FAQs
    faqs = [
        ('What are the OPD timings?', 'OPD timings are Monday to Friday: 9:00 AM - 5:00 PM, Saturday: 9:00 AM - 1:00 PM. Sunday is closed except for emergency services.'),
        ('How do I book an appointment?', 'You can book an appointment online through our website, call our appointment desk at +1-234-567-8900, or visit in person.'),
        ('What documents do I need?', 'Please bring a valid ID, insurance card (if applicable), and any previous medical records.'),
        ('Is parking available?', 'Yes, free parking is available for patients and visitors.'),
        ('Do you accept insurance?', 'Yes, we accept most major insurance plans. Please contact our billing department for details.')
    ]
    cursor.executemany('INSERT INTO faqs (question, answer) VALUES (?, ?)', faqs)
    
    conn.commit()
    print("Sample data inserted")

