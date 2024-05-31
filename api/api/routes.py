import requests
from flask import request, jsonify
from datetime import datetime
from . import app, db
from api.api.config import Config
from api.api.models import User, Wallet, Currency


@app.route('/api/rates')
def get_rates():
    today = datetime.today()
    date_format = '%d.%m.%Y'
    date_string = request.args.get('date')
    if not date_string:
        return jsonify({'Error': 'Bad request. Please check your request data.'}), 400

    try:
        datetime_object = datetime.strptime(date_string, date_format)
    except ValueError:
        return jsonify({'Error': 'Bad request. Please check your date format. It should be dd.mm.YYYY .'}), 400

    if datetime_object > today:
        return jsonify({'Error': 'Bad request. The date cannot be later than today.'}), 400

    r = requests.get(f'{Config.URL}?date={date_string}')

    if r.status_code == 200:
        return r.json(), 200
    else:
        return jsonify({'Error': 'Some error'}), r.status_code


@app.route('/api/user/register', methods=['POST'])
def create_user():
    # Get form data from the request body
    data = request.get_json()
    username = data.get('username')
    telegram_id = data.get('telegram_id')
    name = data.get('name')
    phone = data.get('phone')

    if not username or not telegram_id or not name or not phone:
        return jsonify({'Error': 'Bad request. Missing required fields'}), 400

    try:
        new_user = User(username=username, telegram_id=telegram_id, name=name, phone=phone)
        db.session.add(new_user)
        db.session.commit()
    except Exception:
        return jsonify({'Error': 'The error occurred while adding to the database'}), 500
    else:
        return jsonify(
            {'Message': 'User created successfully', 'user': {
                'id': new_user.id,
                'username': new_user.username,
                'telegram_id': new_user.telegram_id,
                'name': new_user.name,
                'phone': new_user.phone
            }}
        ), 201


@app.route('/api/user/<int:telegram_id>')
def get_user_by_telegram_id(telegram_id):
    try:
        user = User.query.filter_by(telegram_id=telegram_id).first()

        if not user:
            return jsonify({'Error': 'User not found'}), 404

        return jsonify({'User': {
            'id': user.id,
            'username': user.username,
            'telegram_id': user.telegram_id,
            'name': user.name,
            'created_at': user.created_at
        }}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': str(e)}), 500


@app.route('/api/wallets', methods=['GET'])
def get_wallets():
    # Parse the incoming JSON data
    data = request.get_json()
    # Example of processing the data and interacting with the database
    if not data:
        return jsonify({'Error': 'Bad request. Missing required fields'}), 400
    try:
        telegram_id = data.get('telegram_id')
        user = User.query.filter_by(telegram_id=telegram_id).first()
        wallets = Wallet.query.filter_by(user_id=user.id).all()
        wallet_list = [wallet.to_dict() for wallet in wallets]

        if not user:
            return jsonify({'Error': 'User not found'}), 404

        return jsonify({'Wallets': wallet_list}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': str(e)}), 500


@app.route('/api/wallet', methods=['POST'])
def create_wallet():
    # Parse the incoming JSON data
    data = request.get_json()

    # Example of processing the data and interacting with the database
    if not data:
        return jsonify({'Error': 'Bad request. Missing required fields'}), 400

    try:
        currency = Currency.query.filter_by(code=data['basic_currency_code']).first()
        user = User.query.filter_by(telegram_id=data['telegram_id']).first()

        if not user:
            return jsonify({'Error': 'User not found'}), 404

        new_wallet = Wallet(
            title=data['title'],
            description=data['description'],
            user_id=user.id,
            basic_currency_id=currency.id,
            amount=0
        )
        db.session.add(new_wallet)
        db.session.commit()
        return jsonify({'Message': 'Wallet created successfully', 'Wallet': data}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': str(e)}), 500


@app.route('/api/wallet/<int:wallet_id>', methods=['PUT'])
def update_wallet(wallet_id):
    # Parse the incoming JSON data
    data = request.get_json()

    # Example of processing the data and interacting with the database
    if not data:
        return jsonify({'Error': 'Bad request. Missing required fields'}), 400

    try:
        wallet = Wallet.query.get(wallet_id)
        if not wallet:
            return jsonify({'Error': 'Wallet not found'}), 404

        wallet.title = data.get('title')
        wallet.description = data.get('description')

        db.session.commit()
        return jsonify({'Message': 'Wallet was updated successfully', 'Wallet': data}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': str(e)}), 500


@app.route('/api/wallet/<int:wallet_id>', methods=['DELETE'])
def delete_wallet(wallet_id):
    try:
        wallet = Wallet.query.get(wallet_id)

        if not wallet:
            return jsonify({'Error': 'Wallet not found'}), 404

        db.session.delete(wallet)

        db.session.commit()
        return jsonify({'Message': 'Wallet was deleted successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': str(e)}), 500
