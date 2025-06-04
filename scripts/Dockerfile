# scripts/Dockerfile
FROM python:3.10

WORKDIR /app

COPY load_data.py .
COPY records.json .

RUN pip install neo4j
CMD ["python", "load_data.py"]
