FROM python:3.11-alpine
WORKDIR /app
ENV PYTHONPATH ${PYTHONPATH}:/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]