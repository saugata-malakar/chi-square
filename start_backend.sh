#!/bin/bash
echo "🚀 Starting TradeGuard AI Backend..."
cd "$(dirname "$0")/backend"
pip install -r requirements.txt -q
echo "✅ Dependencies installed"
echo "📡 API starting at http://localhost:8000"
echo "📖 Docs at http://localhost:8000/docs"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
