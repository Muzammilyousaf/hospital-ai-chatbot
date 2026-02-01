"""
Setup script for Hospital AI Chatbot
Installs dependencies and sets up the environment
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a shell command."""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main setup function."""
    print("🏥 Hospital AI Chatbot - Setup")
    print("=" * 60)
    
    # Step 1: Install Python dependencies
    print("\n📦 Step 1: Installing Python dependencies...")
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing requirements"):
        print("❌ Failed to install dependencies")
        return
    
    # Step 2: Install spaCy model
    print("\n📦 Step 2: Installing spaCy English model...")
    if not run_command(f"{sys.executable} -m spacy download en_core_web_sm", "Installing spaCy model"):
        print("⚠️  Warning: Could not install spaCy model. Entity extraction may not work.")
        print("   You can install it manually later with: python -m spacy download en_core_web_sm")
    
    # Step 3: Create directories
    print("\n📁 Step 3: Creating directories...")
    directories = [
        "data/hospital_knowledge",
        "data/vector_db",
        "database",
        "templates",
        "static"
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   ✓ Created {directory}")
    
    # Step 4: Ingest data
    print("\n📚 Step 4: Building RAG index...")
    if os.path.exists("data/hospital_knowledge/hospital_info.txt"):
        if run_command(f"{sys.executable} scripts/ingest_data.py", "Building RAG index"):
            print("✅ RAG index built successfully")
        else:
            print("⚠️  Warning: Could not build RAG index. You can run it later with: python scripts/ingest_data.py")
    else:
        print("⚠️  No hospital data found. Add documents to data/hospital_knowledge/ and run: python scripts/ingest_data.py")
    
    print("\n" + "=" * 60)
    print("✅ Setup completed!")
    print("=" * 60)
    print("\nTo start the application:")
    print("   python app.py")
    print("\nThe server will run on http://localhost:5000")

if __name__ == "__main__":
    main()

