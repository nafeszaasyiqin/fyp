FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 80

COPY . .

CMD ["uvicorn", "auth:app", "--host", "0.0.0.0", "--port", "80"]
uvicorn auth:app --host 0.0.0.0 --port 80