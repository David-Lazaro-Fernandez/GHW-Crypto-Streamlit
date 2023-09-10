import streamlit as st
import pandas as pd


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


def pass_json_to_df():
    df = pd.read_json('cryptos.json')
    transposed_df = df.transpose()
    filt_df = transposed_df[transposed_df['name'] != '']
    return filt_df


dataframe = pass_json_to_df()
st.set_page_config(page_icon="🦛", page_title="Crypto Dataframe")
csv = convert_df(dataframe)

with st.sidebar:
    st.header('Crypto Dashboard')

    st.download_button(
        label="Download currencies data as CSV",
        data=csv,
        file_name='cryptos.csv',
        mime='text/csv',
    )

st.image('https://em-content.zobj.net/source/microsoft/319/chart-increasing_1f4c8.png', width=100)

st.markdown(
    """# **Dataframe**
Use this to download your own crypto dataframe.
"""
)

st.write('---')
st.dataframe(dataframe)
