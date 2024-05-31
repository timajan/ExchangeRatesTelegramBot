FROM python:3.9

WORKDIR /telegram_bot

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENV API_TOKEN='6491433399:AAEvvaXsDVDGsdTAOCNmVu9POKuXyZcGvMM'

EXPOSE 3000

CMD ["python", "main.py"]