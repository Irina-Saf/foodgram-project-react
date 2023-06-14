FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

CMD ["gunicorn", "Foodgram.wsgi:application", "--bind", "0:8000" ]
