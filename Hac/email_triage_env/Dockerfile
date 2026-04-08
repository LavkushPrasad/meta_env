FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV HF_TOKEN=""
ENV PORT=7860
ENV PYTHONUNBUFFERED=1

# Expose the port for the API server
EXPOSE 7860

# Run the FastAPI server instead of inference.py
CMD ["python", "server.py"]