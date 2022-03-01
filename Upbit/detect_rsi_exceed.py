from dotenv import load_dotenv
import os
from module_upbit import get_vol_top_tickers, get_pyupbit_rsi
import telegram
import pyupbit
import sys
# import time

"""
Upbit/detect_rsi_exceed.py
* Date: 2022. 1. 23.
* Author: Jeon Won
* Func: 업비트 차트의 RSI 과매도 기준 값을 상향돌파 시 텔레그램 메시지 전송
* Usage: 15분봉 및 과매도 기준 30 조사 명령어는 `python3 Upbit/detect_rsi_exceed.py minute15 30` (minute1~240, day 등 사용)
"""

load_dotenv()

INTERVAL = sys.argv[1]  # 차트 종류
OVERSOLD = sys.argv[2]  # RSI 과매도 기준 값
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")      # 텔레그램 봇 토큰
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")  # 텔레그램 봇 아이디

bot = telegram.Bot(TELEGRAM_TOKEN)
tickers = get_vol_top_tickers(10)  # 최근 24시간 거래량 Top 10 tickers 리스트
# tickers = ["KRW-BTC", "KRW-ETH", "KRW-XRP"]  # 또는 수동으로 Tickers 지정
alert_list = []  # 텔레그램 메시지 보낼 ticker 리스트

# 각 ticker 조사
for ticker in tickers:
    # pyupbit로 ticker의 DataFrame을 얻어옴
    df = pyupbit.get_ohlcv(ticker, INTERVAL)

    prev_df = df[0:len(df)-1]   # 직전 기준 RSI 계산을 위한 데이터프레임
    current_df = df[0:len(df)]  # 현재 기준 RSI 계산을 위한 데이터프레임

    prev_rsi = get_pyupbit_rsi(prev_df)        # 직전 기준 RSI
    current_rsi = get_pyupbit_rsi(current_df)  # 현재 기준 RSI
    
    # 직전 -> 현재 RSI값이 과매도 기준 값(OVERSOLD) 상향돌파 시 텔레그램 메시지 전송
    if(prev_rsi < OVERSOLD and current_rsi > OVERSOLD):
        alert_list.append(ticker)

    # time.sleep(0.1)  # 조사할 ticker 수가 많은 경우 API 호출 제한에 걸리지 않도록 해야 함

# 텔레그램 메시지 보낼 ticker 리스트가 존재하면 텔레그램 메시지 전송
if alert_list:
    message = f"Upbit {INTERVAL} 차트 RSI {OVERSOLD} 상향돌파 Tickers: {alert_list}"
    bot.sendMessage(TELEGRAM_CHAT_ID, text=message)
