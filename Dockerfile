FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make startup script executable
RUN chmod +x start.sh

# Cloud Run sets PORT env var (default 8080)
ENV PORT=8080

# Expose Streamlit port (Cloud Run routes to $PORT)
EXPOSE 8080

# Launch both backend + frontend
CMD ["./start.sh"]
