# 🚀 Quick Start Guide - Hospital AI Chatbot

## Step-by-Step Instructions

### Step 1: Install Dependencies
```bash
python -m pip install -r requirements.txt
```

**Note:** If you get PyTorch DLL errors on Windows, install Visual C++ Redistributable:
- Download: https://aka.ms/vs/17/release/vc_redist.x64.exe
- Install it, then retry

### Step 2: Set Up Environment Variables
```bash
# Windows PowerShell:
copy env.example .env

# Then edit .env and add your OpenAI API key:
# OPENAI_API_KEY=your_actual_api_key_here
```

### Step 3: Build Vector Database (One-time setup)
```bash
python scripts/ingest_data_simple.py
```

This will:
- Use the sample data in `data/hospital_knowledge/hospital_info.txt`
- Create embeddings and build the vector database
- Save to `data/vector_db/`

### Step 4: Start the Server
```bash
python main.py
```

You should see:
```
🏥 Hospital AI Chatbot Starting...
Server will run on http://0.0.0.0:8000
API docs available at http://0.0.0.0:8000/docs
```

### Step 5: Open the Chatbot
Open `frontend/index.html` in your web browser, or visit:
- **API Docs:** http://localhost:8000/docs
- **API Endpoint:** http://localhost:8000/api/chat

## Testing the API

Once the server is running, test it with cURL:

```bash
curl -X POST "http://localhost:8000/api/chat" -H "Content-Type: application/json" -d "{\"message\": \"What are the OPD timings?\"}"
```

## Troubleshooting

### Issue: PyTorch DLL Error
**Solution:** Install Visual C++ Redistributable (link above)

### Issue: "OPENAI_API_KEY not found"
**Solution:** Make sure you created `.env` file and added your API key

### Issue: "Vector database not found"
**Solution:** Run `python scripts/ingest_data_simple.py` first

### Issue: Port 8000 already in use
**Solution:** Change PORT in `.env` file or stop the other service

## What's Next?

- Add more hospital documents to `data/hospital_knowledge/`
- Run ingestion again to update the vector database
- Customize the frontend in `frontend/` directory
- Modify safety prompts in `backend/safety.py`

