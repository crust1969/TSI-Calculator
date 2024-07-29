import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# Funktion zur Berechnung des exponentiell gleitenden Durchschnitts (EMA)
def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

# Funktion zur Berechnung des TSI-Werts und Zwischenergebnisse
def calculate_tsi(close_prices, r=25, s=13):
    delta = close_prices.diff()
    abs_delta = delta.abs()

    ema1 = ema(delta, r)
    ema2 = ema(ema1, s)
    
    abs_ema1 = ema(abs_delta, r)
    abs_ema2 = ema(abs_ema1, s)

    tsi = 100 * (ema2 / abs_ema2)
    
    return tsi.iloc[-1], ema1.iloc[-1], ema2.iloc[-1], abs_ema1.iloc[-1], abs_ema2.iloc[-1]

st.sidebar.title("TSI Berechnung")

# Hochladen der Excel-Datei
uploaded_file = st.sidebar.file_uploader("Laden Sie eine Excel-Datei mit Ticker- und Bezeichnungsinformationen hoch", type=["xlsx"])

if uploaded_file is not None:
    # Lesen der Excel-Datei
    stock_df = pd.read_excel(uploaded_file)
    st.write("Hochgeladene Aktienliste:")
    st.write(stock_df)

    # Verfügbare Spalten überprüfen
    st.write("Verfügbare Spalten:")
    st.write(stock_df.columns)

    # Überprüfen, ob die erforderlichen Spalten vorhanden sind
    if 'Ticker' in stock_df.columns and 'Bezeichnung' in stock_df.columns:
        # Platzhalter für Börsenkursdaten
        stock_df['Close Prices'] = None

        # Börsenkurse der letzten 14 Tage abrufen
        end_date = datetime.today()
        start_date = end_date - timedelta(days=21)  # 14 Handelstage innerhalb von 21 Kalendertagen

        close_prices_dict = {}

        for index, row in stock_df.iterrows():
            ticker = row['Ticker']
            bezeichnung = row['Bezeichnung']
            data = yf.download(ticker, start=start_date, end=end_date)
            close_prices = data['Close'].iloc[-14:]
            if len(close_prices) < 14:
                st.write(f"Nicht genügend Daten für {bezeichnung} ({ticker})")
                continue
            stock_df.at[index, 'Close Prices'] = close_prices.values
            close_prices_dict[bezeichnung] = close_prices

        st.write("Börsenkursdaten der letzten 14 Tage:")
        close_prices_df = pd.DataFrame(close_prices_dict)
        st.write(close_prices_df)

        if st.sidebar.button("TSI Werte berechnen"):
            # Berechnung der TSI-Werte und Zwischenergebnisse
            results = stock_df.apply(lambda row: calculate_tsi(pd.Series(row['Close Prices'])), axis=1)
            stock_df['TSI Wert'], stock_df['EMA1'], stock_df['EMA2'], stock_df['Abs_EMA1'], stock_df['Abs_EMA2'] = zip(*results)

            st.write("TSI Werte und Zwischenergebnisse der Aktien:")
            st.write(stock_df[['Ticker', 'Bezeichnung', 'TSI Wert', 'EMA1', 'EMA2', 'Abs_EMA1', 'Abs_EMA2']])
            
            # Anzeige der Formel
            st.markdown("""
            **Formel zur Berechnung des TSI:**

            \[
            \text{TSI} = 100 \times \left( \frac{\text{EMA}(\text{EMA}(\Delta \text{Close}, 25), 13)}{\text{EMA}(\text{EMA}(|\Delta \text{Close}|, 25), 13)} \right)
            \]

            **Zwischenergebnisse:**
            - \(\text{EMA1} = \text{EMA}(\Delta \text{Close}, 25)\)
            - \(\text{EMA2} = \text{EMA}(\text{EMA1}, 13)\)
            - \(\text{Abs\_EMA1} = \text{EMA}(|\Delta \text{Close}|, 25)\)
            - \(\text{Abs\_EMA2} = \text{EMA}(\text{Abs\_EMA1}, 13)\)
            """)
    else:
        st.write("Die erforderlichen Spalten 'Ticker' und 'Bezeichnung' sind nicht in der hochgeladenen Datei vorhanden.")

st.sidebar.write("Die Börsenkurse werden automatisch von Yahoo Finance abgerufen.")
