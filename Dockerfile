FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Expone el puerto para Cloud Run
EXPOSE 8080

CMD ["gunicorn", "-b", ":8080", "back:app"]