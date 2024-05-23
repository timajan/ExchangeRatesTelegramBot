import requests
from flask import request, jsonify
from datetime import datetime
from . import app
from api.api.models import User


@app.route("/api/rates")
def get_rates():
    today = datetime.today()
    date_format = "%d.%m.%Y"
    date_string = request.args.get('date')
    if not date_string:
        return jsonify({'Error': 'Bad request. Please check your request data.'}), 400

    try:
        datetime_object = datetime.strptime(date_string, date_format)
    except ValueError:
        return jsonify({'Error': 'Bad request. Please check your date format. It should be dd.mm.YYYY .'}), 400

    if datetime_object > today:
        return jsonify({'Error': 'Bad request. The date cannot be later than today.'}), 400

    r = requests.get(f"{URL}?date={date_string}")

    if r.status_code == 200:
        return r.json(), 200
    else:
        return jsonify({"Error": "Some error"}), r.status_code


@app.route("/api/register")
def create_user():
    # Get form data from the request body
    username = request.form.get('username')
    telegram_id = request.form.get('telegram_id')
    name = request.form.get('name')
    phone = request.form.get('phone')

    if not username or not telegram_id or not name or not phone:
        return jsonify({'Error': 'Bad request. Missing required fields'}), 400

    try:
        new_user = User(username=username, telegram_id=telegram_id, name=name, phone=phone)
        db.session.add(new_user)
        db.session.commit()
    except Exception:
        return jsonify({'Error': 'The error occurred while adding to the database'})
    else:
        return jsonify(
            {'message': 'User created successfully', 'user': {'id': new_user.id, 'username': new_user.username}}
        ), 201
