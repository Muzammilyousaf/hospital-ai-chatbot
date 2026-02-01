"""
Reset and populate database with all doctors for all departments.
Run this script to refresh the database with complete demo data.
"""

import sys
import os

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import get_db_connection
from database.schema import create_tables

def reset_database():
    """Reset database and populate with all doctors."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("🔄 Resetting database...")
    
    # Drop all tables
    cursor.execute('DROP TABLE IF EXISTS appointments')
    cursor.execute('DROP TABLE IF EXISTS doctors')
    cursor.execute('DROP TABLE IF EXISTS departments')
    cursor.execute('DROP TABLE IF EXISTS services')
    cursor.execute('DROP TABLE IF EXISTS faqs')
    
    conn.commit()
    print("✅ Old tables dropped")
    
    # Recreate tables with all data
    print("📊 Creating tables and inserting data...")
    create_tables()
    
    # Get fresh connection to verify
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verify data
    cursor.execute('SELECT COUNT(*) FROM departments')
    dept_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM doctors')
    doctor_count = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT d.name, COUNT(doc.id) as doctor_count 
        FROM departments d 
        LEFT JOIN doctors doc ON d.id = doc.department_id 
        GROUP BY d.id, d.name
        ORDER BY d.id
    ''')
    dept_doctors = cursor.fetchall()
    
    print("\n" + "="*60)
    print("✅ Database reset complete!")
    print("="*60)
    print(f"📊 Departments: {dept_count}")
    print(f"👨‍⚕️ Total Doctors: {doctor_count}")
    print("\n📋 Doctors by Department:")
    print("-" * 60)
    for dept in dept_doctors:
        dept_name = dept[0] if isinstance(dept, tuple) else dept['name']
        doc_count = dept[1] if isinstance(dept, tuple) else dept['doctor_count']
        print(f"  • {dept_name}: {doc_count} doctors")
    print("="*60)
    print("\n🎉 Database is ready for demo!")
    print("\n💡 You can now run: python app.py")
    
    conn.close()

if __name__ == "__main__":
    try:
        reset_database()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

