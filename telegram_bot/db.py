import requests

host_ip = 'api'
host_port = '5000'


def get_rates(date):
    r = requests.get(f'http://{host_ip}:{host_port}/api/rates/date={date}')
    return r.json(), r.status_code


def get_user(telegram_id):
    r = requests.get(f'http://{host_ip}:{host_port}/api/user/{telegram_id}')
    return r.json(), r.status_code


def create_user(data):
    url = f'http://{host_ip}:{host_port}/api/user/register'
    r = requests.post(url, json=data)
    return r.json(), r.status_code


def create_wallet(data):
    url = f'http://{host_ip}:{host_port}/api/wallet'
    r = requests.post(url, json=data)
    return r.json(), r.status_code


def get_users_wallets(telegram_id):
    url = f'http://{host_ip}:{host_port}/api/wallets'
    data = {'telegram_id': telegram_id}
    r = requests.get(url, json=data)
    response_data = r.json()
    wallets = response_data.get('Wallets', [])  # Use .get to avoid KeyError
    return wallets, r.status_code


def get_wallet(wallet_number):
    url = f'http://{host_ip}:{host_port}/api/wallet/{wallet_number}'
    r = requests.get(url)
    if r.status_code == 200:
        response_data = r.json()
        return response_data
    else:
        return None


def to_up(wallet_number, amount):
    url = f'http://{host_ip}:{host_port}/api/wallet/to_up/{wallet_number}'
    data = {'amount': amount}
    r = requests.put(url, json=data)
    if r.status_code == 201:
        response_data = r.json()
        return response_data
    else:
        return None


def to_down(wallet_number, amount):
    url = f'http://{host_ip}:{host_port}/api/wallet/to_down/{wallet_number}'
    data = {'amount': amount}
    r = requests.put(url, json=data)
    if r.status_code == 201:
        response_data = r.json()
        return response_data
    else:
        return None


def transfer(from_wallet_number, to_wallet_number, amount):
    url = f'http://{host_ip}:{host_port}/api/wallet/transfer'
    data = {
        'from_wallet_number': from_wallet_number,
        'to_wallet_number': to_wallet_number,
        'amount': amount
    }
    r = requests.put(url, json=data)
    if r.status_code == 201:
        response_data = r.json()
        return response_data
    else:
        return None


def delete_wallet(wallet_number):
    url = f'http://{host_ip}:{host_port}/api/wallet/{wallet_number}'

    r = requests.delete(url)
    if r.status_code == 201:
        response_data = r.json()
        return response_data
    else:
        return None


def get_currency(currency_id):
    url = f'http://{host_ip}:{host_port}/api/currency/{currency_id}'
    r = requests.get(url)
    if r.status_code == 200:
        response_data = r.json()
        return response_data
    else:
        return None
