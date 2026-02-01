@echo off
echo ============================================================
echo   Hospital AI Chatbot - PyTorch + Flask + RAG
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if dependencies are installed
python -c "import flask" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
)

REM Check if database exists
if not exist "database\hospital.db" (
    echo Initializing database...
    python -c "from database.schema import create_tables; create_tables()"
)

REM Check if RAG index exists
if not exist "data\vector_db\index.faiss" (
    echo Building RAG index...
    python scripts/ingest_data.py
)

echo.
echo Starting Flask server...
echo Server will be available at: http://localhost:5000
echo Press Ctrl+C to stop
echo.

python app.py
