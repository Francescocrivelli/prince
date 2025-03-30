FROM python:3.11-slim

WORKDIR /app
COPY . /app

#install requirements
RUN pip install -r requirements.txt

# Copy pre-downloaded model into container
COPY models /app/models

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]