# syntax=docker/dockerfile:1
FROM python:3.12

ENV PYTHONUNBUFFERED=1
WORKDIR /prog
COPY requirements.txt /prog/
RUN pip install -r requirements.txt
COPY . /prog/

CMD ["python", "Interface/app.py"]
