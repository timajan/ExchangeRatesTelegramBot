from flask import Flask, request
import requests
from datetime import datetime
from .config import *
app = Flask(__name__)


@app.route("/api/rates")
def get_rates():
    today = datetime.today()
    date_format = "%d.%m.%Y"
    date_string = request.args.get('date')
    if not date_string:
        return {'Error': 'Bad request. Please check your request data.'}, 400

    try:
        datetime_object = datetime.strptime(date_string, date_format)
    except ValueError:
        return {'Error': 'Bad request. Please check your date format. It should be dd.mm.YYYY .'}, 400

    if datetime_object > today:
        return {'Error': 'Bad request. The date cannot be later than today.'}, 400

    r = requests.get(f"{URL}?date={date_string}")

    if r.status_code == 200:
        return r.json(), 200
    else:
        return {"Error": "Some error"}, r.status_code
