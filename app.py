import streamlit as st
import requests
import json


GLOBAL_MARKET_END_POINT = 'https://api.polygon.io/v2/aggs/grouped/locale/global/market/crypto/2023-01-09?adjusted=true&apiKey=TBxDsx1YUlUNmatc_OQhkvuyOxYXYydR'
TICKERS_END_POINT = 'https://api.polygon.io/v3/reference/tickers?market=crypto&active=true&apiKey=TBxDsx1YUlUNmatc_OQhkvuyOxYXYydR'

cryptos = {}


def get_crypto_data():
    response = requests.get(GLOBAL_MARKET_END_POINT)
    data = response.json()
    return data


def get_crypto_names():
    data = get_crypto_data()
    for crypto in data['results']:
        cryptos[crypto['T']] = {'closing_value': crypto['c'], 'name': ''}

    return cryptos


def get_crypto_tickers():
    response = requests.get(TICKERS_END_POINT)
    data = response.json()

    for crypto in data['results']:
        if crypto['ticker'] in cryptos:
            cryptos[crypto['ticker']]['name'] = crypto['name']


with open("cryptos.json", "r") as cryptos_file:
    currencies = json.load(cryptos_file)

for currencie, values in currencies.items():
    if values['name']:
        st.text(currencie)
        st.subheader(values['closing_value'])
        st.write(values['name'])
    