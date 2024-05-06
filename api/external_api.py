import requests
import json
from config import *


def get_rates(date):
    r = requests.get(f"{URL}?date={date}")
    return r.json()
