from dotenv import load_dotenv
import os
from module_upbit import get_vol_top_tickers, get_bb
import telegram
import sys

"""
detect_bb_upbit.py
* Date: 2021. 10. 5.
* Author: Jeon Won
* Func: 업비트 차트의 현재가가 볼린저밴드 하한선 밑에 있으면 텔레그램 메시지 전송
* Usage: 15분봉 차트 조사 명령어는 `python3 detect_bb_upbit.py minute15` (minute1~240, day 등 사용)
"""

load_dotenv()

INTERVAL = sys.argv[1]  # 차트 종류
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")      # 텔레그렘 봇 토큰
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")  # 텔레그램 봇 아이디
BB_COUNT = 20      # 볼린저 밴드(BB)의 길이
BB_MULTIPLIER = 2  # 볼린저 밴드(BB)에서 상하한선을 정하기 위해 사용하는 곱(승수)

bot = telegram.Bot(TELEGRAM_TOKEN)
tickers = get_vol_top_tickers(10)  # 최근 24시간 거래량 Top 10 tickers 리스트
# tickers = ["KRW-BTC", "KRW-ETH", "KRW-XRP"]  # 또는 수동으로 Tickers 지정
alert_0_list = []  # 텔레그램 메시지 보낼 ticker 리스트

# 각 ticker 조사
for ticker in tickers:
    bb = get_bb(ticker, INTERVAL, BB_COUNT, BB_MULTIPLIER)

    # %B 값 0 미만 시(과매도, 현재가가 볼린저 밴드 하단 아래에 위치하면) 텔레그램 보낼 tickers 리스트에 추가
    if(bb["per_b"] < 0):
        alert_0_list.append(ticker)

# 과매도 Tickers 리스트 텔레그램 메시지 전송
if alert_0_list:
    message = f"Upbit {INTERVAL} 차트 볼린저밴드 과매도 Tickers: {alert_0_list}"
    bot.sendMessage(TELEGRAM_CHAT_ID, text=message)
