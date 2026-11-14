
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY api_churn.py .
COPY modelo_churn.joblib .

EXPOSE 8000

CMD ["uvicorn", "api_churn:app", "--host", "0.0.0.0", "--port", "8000"]
