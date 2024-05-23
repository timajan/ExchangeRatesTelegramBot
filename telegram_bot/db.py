import requests

host_ip = 'api'
host_port = '5000'


def get_rates(date):
    r = requests.get(f'http://{host_ip}:{host_port}/api/rates?date={date}')
    return r.json(), r.status_code
