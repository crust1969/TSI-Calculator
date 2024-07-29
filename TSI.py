import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# Funktion zur Berechnung des RSI
def calculate_rsi(changes, period=14):
    gains = changes[changes > 0].sum() / period
    losses = -changes[changes < 0].sum() / period
    if losses == 0:
        return 100
    rs = gains / losses
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Funktion zur Berechnung des TSI-Werts
def calculate_tsi(close_prices):
    changes = close_prices.diff().dropna()
    rsi = calculate_rsi(changes)
    short_ma = close_prices.rolling(window=10).mean().iloc[-1]
    long_ma = close_prices.rolling(window=50).mean().iloc[-1]
    tsi = (rsi + short_ma + long_ma) / 3
    return tsi

st.sidebar.title("TSI Berechnung")

# Hochladen der Excel-Datei
uploaded_file = st.sidebar.file_uploader("Laden Sie eine Excel-Datei mit Ticker- und Bezeichnungsinformationen hoch", type=["xlsx"])

if uploaded_file is not None:
    # Lesen der Excel-Datei
    stock_df = pd.read_excel(uploaded_file)
    st.write("Hochgeladene Aktienliste:")
    st.write(stock_df)

    # Platzhalter für Börsenkursdaten
    stock_df['Close Prices'] = None

    # Börsenkurse der letzten 14 Tage abrufen
    end_date = datetime.today()
    start_date = end_date - timedelta(days=21)  # 14 Handelstage innerhalb von 21 Kalendertagen

    for index, row in stock_df.iterrows():
        ticker = row['Ticker']
        bezeichnung = row['Bezeichnung']
        data = yf.download(ticker, start=start_date, end=end_date)
        close_prices = data['Close'].iloc[-14:]
        stock_df.at[index, 'Close Prices'] = close_prices.values

    st.write("Börsenkursdaten der letzten 14 Tage:")
    for index, row in stock_df.iterrows():
        st.write(f"{row['Bezeichnung']} ({row['Ticker']}): {row['Close Prices']}")

    if st.sidebar.button("TSI Werte berechnen"):
        # Berechnung der TSI-Werte
        stock_df['TSI Wert'] = stock_df.apply(lambda row: calculate_tsi(pd.Series(row['Close Prices'])), axis=1)
        st.write("TSI Werte der Aktien:")
        st.write(stock_df[['Ticker', 'Bezeichnung', 'TSI Wert']])

st.sidebar.write("Die Börsenkurse werden automatisch von Yahoo Finance abgerufen.")
