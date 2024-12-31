import streamlit as st
import yfinance as yf
import pandas as pd

# Funktion zur Berechnung der 90-Tage-Rendite
def calculate_90_day_returns(df):
    df['90_day_return'] = df['Close'].pct_change(periods=90) * 100
    return df

# Funktion zur Berechnung der besten 90-Tage-Perioden pro Jahr
def best_90_day_periods(df):
    df['Year'] = df.index.year
    best_periods = []

    for year in df['Year'].unique():
        yearly_data = df[df['Year'] == year]
        max_return = yearly_data['90_day_return'].max()
        best_period = yearly_data[yearly_data['90_day_return'] == max_return]
        best_periods.append(best_period)

    return pd.concat(best_periods)

# Streamlit App
def main():
    st.title("Aktien mit der höchsten 90-Tage-Rendite im Jahr")

    # Eingabe der Aktie
    ticker = st.text_input("Geben Sie das Aktiensymbol ein:", "MSFT")

    if ticker:
        # Daten von Yahoo Finance abrufen
        df = yf.download(ticker, start="2010-01-01", end="2024-12-31")

        # Berechnung der 90-Tage-Rendite
        df_with_returns = calculate_90_day_returns(df)

        # Berechnung der besten 90-Tage-Perioden pro Jahr
        best_periods = best_90_day_periods(df_with_returns)

        # Ergebnisse anzeigen
        st.subheader(f"Die besten 90-Tage-Perioden für {ticker}")
        st.dataframe(best_periods[['Close', '90_day_return', 'Year']])

# Hauptfunktion starten
if __name__ == "__main__":
    main()


  
