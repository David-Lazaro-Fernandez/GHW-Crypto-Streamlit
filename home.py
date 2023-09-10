import streamlit as st
import requests
import pandas as pd
import json
from annotated_text import annotated_text, annotation


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


def crypto_card(currencie, values):
    if values['name']:
        currencie_string = currencie[2:]
        annotated_text(
            annotation(currencie_string, "Symbol"),
        )
        value_string = f'$ {values["closing_value"]} USD'
        st.subheader(value_string)
        st.markdown(f':rainbow[{values["name"]}]')


def pass_json_to_df():
    df = pd.read_json('cryptos.json')
    transposed_df = df.transpose()
    filt_df = transposed_df[transposed_df['name'] != '']
    return filt_df


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


with open("cryptos.json", "r") as cryptos_file:
    currencies = json.load(cryptos_file)

dataframe = pass_json_to_df()


st.set_page_config(page_icon="🦛", page_title="Crypto Dashboard")
csv = convert_df(dataframe)
with st.sidebar:
    st.header('Crypto Dashboard')
    st.selectbox(
        'Select a section',
        ('Currencies', 'See the full Dataframe')
    )
   
    st.download_button(
        label="Download currencies data as CSV",
        data=csv,
        file_name='cryptos.csv',
        mime='text/csv',
    )
    

st.image('https://em-content.zobj.net/source/microsoft/319/hippopotamus_1f99b.png', width=100)

st.markdown(
    """# **Crypto Dashboard**
A simple cryptocurrency price app pulling price data from the [Polygon API](https://polygon.io/docs/stocks/getting-started).
"""
)
col1, col2, col3 = st.columns(3)
number_of_currencies = len(currencies)
ranges = [number_of_currencies / 3,
          number_of_currencies / 3 * 2, number_of_currencies]
counter = 1


for currencie, values in currencies.items():
    if counter <= ranges[0]:
        with col1:
            crypto_card(currencie, values)
    elif counter <= ranges[1]:
        with col2:
            crypto_card(currencie, values)
    else:
        with col3:
            crypto_card(currencie, values)
    counter += 1

