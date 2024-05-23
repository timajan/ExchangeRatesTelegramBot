FROM python:3.9

WORKDIR /api

COPY ./requirements.txt /api/requirements.txt

RUN pip install --no-cache-dir -r /api/requirements.txt

COPY . /api

ENV FLASK_APP=manage.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

EXPOSE 5000

CMD ["flask", "run"]
