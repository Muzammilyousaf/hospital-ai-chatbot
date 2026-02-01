#!/bin/bash

echo "🏥 Hospital AI Chatbot - Quick Start"
echo "===================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "Creating .env from env.example..."
    cp env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your OPENAI_API_KEY"
    read -p "Press Enter to continue after adding your API key..."
fi

# Check if vector DB exists
if [ ! -f "data/vector_db/index.faiss" ]; then
    echo "📚 Vector database not found. Building it now..."
    echo ""
    python scripts/ingest_data_simple.py
    if [ $? -ne 0 ]; then
        echo "❌ Error building vector database. Please check the error above."
        exit 1
    fi
    echo ""
    echo "✅ Vector database created successfully!"
    echo ""
fi

echo "🚀 Starting Hospital AI Chatbot server..."
echo ""
echo "Server will be available at:"
echo "  - API: http://localhost:8000/docs"
echo "  - Frontend: Open frontend/index.html in your browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python main.py

