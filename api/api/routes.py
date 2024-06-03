import requests
from flask import request, jsonify
from . import app, db
from api.api.config import Config
from api.api.models import User, Wallet, Currency
from datetime import datetime


@app.route('/api/rates/<date>', methods=['GET'])
def get_rates(date):
    today = datetime.today()
    date_format = '%d.%m.%Y'
    if not date:
        return jsonify({'Error': 'Bad request. Please check your request data.'}), 400

    try:
        datetime_object = datetime.strptime(date, date_format)
    except ValueError:
        return jsonify({'Error': 'Bad request. Please check your date format. It should be dd.mm.YYYY .'}), 400

    if datetime_object > today:
        return jsonify({'Error': 'Bad request. The date cannot be later than today.'}), 400

    r = requests.get(f'https://api.privatbank.ua/p24api/exchange_rates?date={date}')

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


@app.route('/api/wallet/<int:wallet_number>', methods=['GET'])
def get_wallet(wallet_number):
    try:
        wallet = Wallet.query.filter_by(number=wallet_number).first()

        if not wallet:
            return jsonify({'Error': 'Wallet not found'}), 404

        return jsonify({'Wallet': wallet.to_dict()}), 200  # Call the to_dict method
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': str(e)}), 500


@app.route('/api/wallet/<int:wallet_number>', methods=['PUT'])
def update_wallet(wallet_number):
    # Parse the incoming JSON data
    data = request.get_json()

    # Example of processing the data and interacting with the database
    if not data:
        return jsonify({'Error': 'Bad request. Missing required fields'}), 400

    try:
        wallet = Wallet.query.filter_by(number=wallet_number).first()
        if not wallet:
            return jsonify({'Error': 'Wallet not found'}), 404

        wallet.title = data.get('title')
        wallet.description = data.get('description')

        db.session.commit()
        return jsonify({'Message': 'Wallet was updated successfully', 'Wallet': data}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': str(e)}), 500


@app.route('/api/wallet/<int:wallet_number>', methods=['DELETE'])
def delete_wallet(wallet_number):
    try:
        wallet = Wallet.query.filter_by(number=wallet_number).first()

        if not wallet:
            return jsonify({'Error': 'Wallet not found'}), 404

        db.session.delete(wallet)

        db.session.commit()
        return jsonify({'Message': 'Wallet was deleted successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': str(e)}), 500


@app.route('/api/wallet/to_up/<int:wallet_number>', methods=['PUT'])
def to_up_wallet(wallet_number):
    # Parse the incoming JSON data
    data = request.get_json()

    # Example of processing the data and interacting with the database
    if not data:
        return jsonify({'Error': 'Bad request. Missing required fields'}), 400

    try:
        wallet = Wallet.query.filter_by(number=wallet_number).first()
        if not wallet:
            return jsonify({'Error': 'Wallet not found'}), 404

        current_amount = wallet.amount

        if data.get('amount') <= 0:
            return jsonify({'Error': 'Amount should be greater than 0'}), 400

        wallet.amount = current_amount + data.get('amount')

        db.session.commit()
        return jsonify({'Message': 'Wallet was updated successfully', 'Wallet': wallet.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': str(e)}), 500


@app.route('/api/wallet/to_down/<int:wallet_number>', methods=['PUT'])
def to_down_wallet(wallet_number):
    # Parse the incoming JSON data
    data = request.get_json()

    # Example of processing the data and interacting with the database
    if not data:
        return jsonify({'Error': 'Bad request. Missing required fields'}), 400

    try:
        wallet = Wallet.query.filter_by(number=wallet_number).first()
        if not wallet:
            return jsonify({'Error': 'Wallet not found'}), 404

        current_amount = wallet.amount
        if data.get('amount') <= 0:
            return jsonify({'Error': 'Amount should be greater than 0'}), 400

        if current_amount < data.get('amount'):
            return jsonify({'Error': 'Not enough money'}), 400

        wallet.amount = current_amount - data.get('amount')

        db.session.commit()
        return jsonify({'Message': 'Wallet was updated successfully', 'Wallet': wallet.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': str(e)}), 500


def get_currency(currency_id):
    currencies = Currency.query.all()
    currency_map = {currency.id: currency.code for currency in currencies}
    return currency_map.get(currency_id, "Unknown")


def get_exchange_rate(base_currency, target_currency, exchange_rates):
    # return exchange_rates[0]['exchangeRate'][17]['currency'] == 'PLN'
    if base_currency == target_currency:
        return 1.0

    from_rate = None
    to_rate = None

    for rate in exchange_rates[0]['exchangeRate']:
        if rate['currency'] == base_currency:
            from_rate = rate['purchaseRateNB']
        if rate['currency'] == target_currency:
            to_rate = rate['purchaseRateNB']

    if from_rate is None or to_rate is None:
        raise ValueError("Exchange rate not found")

    return round(from_rate / to_rate, 2)


@app.route('/api/wallet/transfer', methods=['PUT'])
def to_transfer_wallet():
    data = request.get_json()
    from_wallet_number = data.get('from_wallet_number')
    to_wallet_number = data.get('to_wallet_number')
    amount = data.get('amount')

    if not from_wallet_number or not to_wallet_number or amount is None:
        return jsonify({'Error': 'Bad request. Missing required fields'}), 400

    try:
        from_wallet = Wallet.query.filter_by(number=from_wallet_number).first()
        to_wallet = Wallet.query.filter_by(number=to_wallet_number).first()

        if not from_wallet or not to_wallet:
            return jsonify({'Error': 'Wallet not found'}), 404

        current_from_amount = from_wallet.amount
        current_to_amount = to_wallet.amount

        if amount <= 0:
            return jsonify({'Error': 'Amount should be greater than 0'}), 400

        if current_from_amount < amount:
            return jsonify({'Error': 'Not enough money'}), 400

        currency_code_from = get_currency(from_wallet.basic_currency_id)
        currency_code_to = get_currency(to_wallet.basic_currency_id)

        date_format = "%d.%m.%Y"
        date_string = datetime.today().strftime(date_format)
        rates = get_rates(date_string)

        try:
            exchange_rate = get_exchange_rate(currency_code_from, currency_code_to, rates)
            # return jsonify({'Error': f'{exchange_rate}'}), 400
            converted_amount = amount * exchange_rate
        except Exception as e:
            return jsonify({'Error': str(e)}), 400

        from_wallet.amount = current_from_amount - amount
        to_wallet.amount = current_to_amount + converted_amount

        db.session.commit()
        return jsonify({'Message': 'Transfer was made successfully', 'Transfer': {
            'from_wallet_number': from_wallet_number,
            'from_wallet_title': from_wallet.title,
            'to_wallet_number': to_wallet.number,
            'to_wallet_title': to_wallet.title,
            'amount': amount,
            'basic_currency_id': from_wallet.basic_currency_id,
            'converted_amount': converted_amount
        }}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': str(e)}), 500


@app.route('/api/currency/<int:currency_id>', methods=['GET'])
def get_currency_route(currency_id):
    try:
        currency = Currency.query.get(currency_id)

        if not currency:
            return jsonify({'Error': 'Currency not found'}), 404

        return jsonify({'Currency': currency.to_dict()}), 200  # Call the to_dict method
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': str(e)}), 500


#
# rates = get_rates('03.06.2024')
# print(get_exchange_rate('USD', 'PLN', rates))
# print(rates[0]['exchangeRate'][0]['baseCurrency'] == 'UAH')
