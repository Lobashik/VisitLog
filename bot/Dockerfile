FROM python:3.12.10-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./src/ /app/

CMD ["python", "main.py"]