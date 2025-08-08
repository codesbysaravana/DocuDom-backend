```dockerfile
FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["zappa", "serve"]
```

# AutoDock timestamp: 2025-08-08T08:56:22.788747Z