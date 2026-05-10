#!/bin/bash

# Start FastAPI backend on port 8000 (internal only)
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Wait for backend to be ready
sleep 3

# Start Streamlit frontend on $PORT (Cloud Run routes traffic here)
streamlit run streamlit_app/app.py \
    --server.port=${PORT:-8080} \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.gatherUsageStats=false \
    --server.fileWatcherType=none
