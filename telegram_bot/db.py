import requests

host_ip = 'api'
host_port = '5000'


def get_rates(date):
    r = requests.get(f'http://{host_ip}:{host_port}/api/rates?date={date}')
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
    return r.json(), r.status_code
