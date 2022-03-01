from dotenv import load_dotenv
import os
import sys
from module_binance import get_ccxt_bb
import telegram
import ccxt
import pandas as pd

"""
Binance/detect_bb_exceed.py
* Date: 2022. 1. 30.
* Author: Jeon Won
* Func: 바이낸스 차트의 %B 0 값을 상향돌파 또는 1 값을 하향돌파 시 텔레그램 메시지 전송
* Usage: 15분봉 기준 조사 명령어는 `python3 Binance/detect_bb_exceed.py 15m` (1m, 3m, 5m, 15m, 30m, 1h, 4h, 6h, 12h, 1d 사용)
"""

load_dotenv()

INTERVAL = sys.argv[1]  # 차트 종류
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")      # 텔레그램 봇 토큰
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")  # 텔레그램 봇 아이디
BB_COUNT = 20      # 볼린저 밴드(BB)의 길이
BB_MULTIPLIER = 2  # 볼린저 밴드(BB)에서 상하한선을 정하기 위해 사용하는 곱(승수)

bot = telegram.Bot(TELEGRAM_TOKEN)
binance = ccxt.binance()
tickers = ["BTC/USDT", "ETH/USDT", "XRP/USDT", "SOL/USDT", "SAND/USDT", "BNB/USDT", "AXS/USDT", "ATOM/USDT", "DOGE/USDT", "EOS/USDT", 
    "BCH/USDT",  "LTC/USDT", "ADA/USDT", "ETC/USDT", "LINK/USDT", "TRX/USDT", "DOT/USDT", "MATIC/USDT", "UNI/USDT", "ICP/USDT", 
    "AAVE/USDT", "FIL/USDT", "XLM/USDT", "XTZ/USDT", "SUSHI/USDT", "THETA/USDT", "AVAX/USDT", "LUNA/USDT", "DASH/USDT", "SHIB/USDT", 
    "XEM/USDT", "MANA/USDT", "GALA/USDT", "DYDX/USDT", "CRV/USDT", "NEAR/USDT", "EGLD/USDT", "KSM/USDT", "AR/USDT", "REN/USDT", 
    "FTM/USDT"]
alert_0_list = []  # %B 0 값 상향돌파 시 텔레그램 메시지 보낼 ticker 리스트
alert_1_list = []  # %B 1 값 하향돌파 시 텔레그램 메시지 보낼 ticker 리스트

# 각 ticker 조사
for ticker in tickers:
    # ccxt로 ticker의 BB_COUNT+1개 만큼의 list를 얻어옴
    # 0 ~ BB_COUNT 범위의 list는 직전 볼린저밴드 계산용
    # 1 ~ BB_COUNT+1 범위의 list는 현재 볼린저밴드 계산용
    ohlcvs = binance.fetch_ohlcv(ticker, INTERVAL, limit=BB_COUNT+1)

    prev_ohlcvs = ohlcvs[0:len(ohlcvs)-1]   # 직전 기준 BB_COUNT개의 list
    current_ohlcvs = ohlcvs[1:len(ohlcvs)]  # 현재 기준 BB_COUNT개의 list

    prev_bb = get_ccxt_bb(ticker, prev_ohlcvs, BB_MULTIPLIER)        # 직전 기준 볼린저밴드 값
    current_bb = get_ccxt_bb(ticker, current_ohlcvs, BB_MULTIPLIER)  # 현재 기준 볼리저밴드 값

    prev_per_b = prev_bb["per_b"]        # 직전 기준 %B 값
    current_per_b = current_bb["per_b"]  # 현재 기준 %B 값

    # 직전 -> 현재 %B값이 0을 상향돌파한 ticker를 텔레그램 메시지 보낼 ticker 리스트에 추가
    if(prev_per_b < 0 and current_per_b > 0):
        alert_0_list.append(ticker)
        
    # 직전 -> 현재 %B값이 1을 하향돌파한 ticker를 텔레그램 메시지 보낼 ticker 리스트에 추가
    if(prev_per_b > 1 and current_per_b < 1):
        alert_1_list.append(ticker)
    
# 텔레그램 메시지 전송
if alert_0_list:
    message = f"Binance {INTERVAL} 차트 볼린저밴드 %B 0 상향돌파 Tickers: {alert_0_list}"
    bot.sendMessage(TELEGRAM_CHAT_ID, text=message)
if alert_1_list:
    message = f"Binance {INTERVAL} 차트 볼린저밴드 %B 1 하향돌파 Tickers: {alert_1_list}"
    bot.sendMessage(TELEGRAM_CHAT_ID, text=message)