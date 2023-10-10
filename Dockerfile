FROM python:3.11-alpine
WORKDIR /app
ENV PYTHONPATH ${PYTHONPATH}:/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
# Expose the port on which the application will run
EXPOSE 8000

# Run the FastAPI application using uvicorn server
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]