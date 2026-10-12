import os
import MetaTrader5 as mt5
import pandas as pd
import requests

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

def check_market():
    if not mt5.initialize():
        return
    
    rates = mt5.copy_rates_from_pos("EURUSD", mt5.TIMEFRAME_H4, 0, 150)
    df = pd.DataFrame(rates)
    
    supply_zone = df['high'].max()
    demand_zone = df['low'].min()
    current_price = df.iloc[-1]['close']
    
    if current_price <= (demand_zone * 1.002):
        send_telegram_message("🚨 *Demand Zone Alert!*\nEURUSD reached demand area.")
    elif current_price >= (supply_zone * 0.998):
        send_telegram_message("🚨 *Supply Zone Alert!*\nEURUSD reached supply area.")
        
    mt5.shutdown()

if __name__ == "__main__":
    check_market()
