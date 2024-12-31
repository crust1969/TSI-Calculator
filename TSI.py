import streamlit as st
import yfinance as yf
import pandas as pd

# Funktion zur Berechnung der 90-Tage-Rendite
def calculate_90_day_returns(df):
    df['90_day_return'] = df['Close'].pct_change(periods=90) * 100
    return df

# Funktion zur Berechnung der durchschnittlichen 90-Tage-Rendite
def average_90_day_return(df):
    return df['90_day_return'].mean()

# Streamlit App
def main():
    st.title("Aktien 90-Tage-Rendite Berechnung")

    # Eingabe der Aktie
    ticker = st.text_input("Geben Sie das Aktiensymbol ein:", "MSFT")

    if ticker:
        # Daten von Yahoo Finance abrufen
        df = yf.download(ticker, start="2010-01-01", end="2024-12-31")

        # Daten anzeigen
        st.subheader(f"Historische Kursdaten von {ticker}")
        st.dataframe(df)

        # Berechnung der 90-Tage-Rendite
        df_with_returns = calculate_90_day_returns(df)

        # Berechnung der durchschnittlichen 90-Tage-Rendite
        avg_return = average_90_day_return(df_with_returns)
        
        # Durchschnittliche Rendite anzeigen
        st.subheader(f"Durchschnittliche 90-Tage-Rendite für {ticker}:")
        st.write(f"Durchschnittliche 90-Tage-Rendite: {avg_return:.2f}%")

        # Berechnete Renditen anzeigen
        st.subheader(f"90-Tage-Renditen für {ticker}")
        st.dataframe(df_with_returns[['Close', '90_day_return']])

# Hauptfunktion starten
if __name__ == "__main__":
    main()
  
