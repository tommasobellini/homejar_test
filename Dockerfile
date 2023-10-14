FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt ./
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps
ENV PYTHONPATH ${PYTHONPATH}:/app
COPY . .
# Expose the port on which the application will run
EXPOSE 8000

# Run the FastAPI application using uvicorn server
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]