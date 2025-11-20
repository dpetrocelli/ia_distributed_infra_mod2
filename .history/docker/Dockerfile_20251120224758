FROM python:3.11-slim
WORKDIR /app

# requirements
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# app
COPY app/app.py .

# CMD inicio
CMD ["python", "app.py"]