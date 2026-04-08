FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV HF_TOKEN=""
ENV PYTHONUNBUFFERED=1

# Validate environment
RUN python -c "from environment import EmailTriageEnv; env = EmailTriageEnv('easy_email_triage'); env.reset(); print('Environment validated')"

CMD ["python", "inference.py"]