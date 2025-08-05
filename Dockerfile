FROM python:3.11-slim
        WORKDIR /app
        COPY requirements.txt .
        RUN pip install -r requirements.txt
        COPY . .
        EXPOSE 5000
        CMD ["python", "app.py"]

# AutoDock timestamp: 2025-08-05T10:54:36.188944Z