from dotenv import load_dotenv
import os
from module_upbit import get_vol_top_tickers, get_pyupbit_bb
import telegram
import pyupbit
import sys

"""
Upbit/detect_bb_exceed_upbit.py
* Date: 2022. 1. 23.
* Author: Jeon Won
* Func: 업비트 차트의 %B 0 값을 상향돌파 시 텔레그램 메시지 전송
* Usage: 15분봉 기준 조사 명령어는 `python3 Upbit/detect_bb_exceed.py minute15` (minute1~240, day 등 사용)
"""

load_dotenv()

INTERVAL = sys.argv[1]  # 차트 종류
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")      # 텔레그램 봇 토큰
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")  # 텔레그램 봇 아이디
BB_COUNT = 20      # 볼린저 밴드(BB)의 길이
BB_MULTIPLIER = 2  # 볼린저 밴드(BB)에서 상하한선을 정하기 위해 사용하는 곱(승수)

bot = telegram.Bot(TELEGRAM_TOKEN)
tickers = get_vol_top_tickers(10)  # 최근 24시간 거래량 Top 10 tickers 리스트
# tickers = ["KRW-BTC", "KRW-ETH", "KRW-XRP"]  # 또는 수동으로 Tickers 지정
alert_list = []  # 텔레그램 메시지 보낼 ticker 리스트

# 각 ticker 조사
for ticker in tickers:
    # pyupbit로 ticker의 BB_COUNT+1개 만큼의 DataFrame을 얻어옴
    # 0 ~ BB_COUNT 범위의 DataFrame은 직전 볼린저밴드 계산용
    # 1 ~ BB_COUNT+1 범위의 DataFrame은 현재 볼린저밴드 계산용
    df = pyupbit.get_ohlcv(ticker, INTERVAL, BB_COUNT+1)

    prev_df = df[0:len(df)-1]   # 직전 기준 BB_COUNT개의 데이터프레임
    current_df = df[1:len(df)]  # 현재 기준 BB_COUNT개의 데이터프레임
    
    prev_bb = get_pyupbit_bb(ticker, prev_df, BB_MULTIPLIER)        # 직전 기준 볼린저밴드 값
    current_bb = get_pyupbit_bb(ticker, current_df, BB_MULTIPLIER)  # 현재 기준 볼린저밴드 값
    
    prev_per_b = prev_bb["per_b"]        # 직전 기준 %B 값 
    current_per_b = current_bb["per_b"]  # 현재 기준 %B 값

    # 직전 -> 현재 %B값이 0을 상향돌파한 ticker를 텔레그램 메시지 보낼 ticker 리스트에 추가
    if(prev_per_b < 0 and current_per_b > 0):
        alert_list.append(ticker)
    
    # time.sleep(0.1)  # 조사할 ticker 수가 많은 경우 API 호출 제한에 걸리지 않도록 해야 함
    
# 텔레그램 메시지 전송
if alert_list:
    message = f"Upbit {INTERVAL} 차트 볼린저밴드 %B 0 상향돌파 Tickers: {alert_list}"
    bot.sendMessage(TELEGRAM_CHAT_ID, text=message)