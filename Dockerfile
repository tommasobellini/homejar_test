FROM python:3.11-alpine
WORKDIR /homejar_test
ENV PYTHONPATH ${PYTHONPATH}:/homejar_test
COPY /app/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]