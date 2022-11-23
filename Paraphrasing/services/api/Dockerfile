FROM python:3.9

COPY . /app/app

WORKDIR /app/app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD [ "uvicorn", "server:app", "--host", "0.0.0.0"]