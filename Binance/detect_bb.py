from dotenv import load_dotenv
import os
from module_binance import get_bb
import telegram
import sys

"""
detect_bb_binance.py
* Date: 2021. 10. 5.
* Author: Jeon Won
* Func: 바이낸스 차트의 현재가가 볼린저 밴드 상단 또는 하단을 터치하는 캔들 발생 시 텔레그램 메시지 전송
* Usage: 15분봉 차트 조사 명령어는 `python3 detect_bb_binance.py 15m` (1m, 3m, 5m, 15m, 30m, 1h, 4h, 6h, 12h, 1d 사용)
"""

load_dotenv()

INTERVAL = sys.argv[1]  # 차트 종류
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")      # 텔레그렘 봇 토큰
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")  # 텔레그램 봇 아이디
BB_COUNT = 20      # 볼린저 밴드 길이
BB_MULTIPLIER = 2  # 볼린저 밴드에서 상하한선을 정하기 위해 사용하는 곱(승수)

bot = telegram.Bot(TELEGRAM_TOKEN)
tickers = ["BTC/USDT", "XRP/USDT", "ETH/USDT"]
alert_0_list = []  # 텔레그램 메시지 보낼 과매도 tickers 리스트
alert_1_list = []  # 텔레그램 메시지 보낼 과매수 tickers 리스트

# 각 ticker 조사
for ticker in tickers:                 
    bb = get_bb(ticker, INTERVAL, BB_COUNT, BB_MULTIPLIER)

    # %B 값 0 미만 시(과매도, 현재가가 볼린저 밴드 하단 아래에 위치하면) 텔레그램 메시지 보낼 tickers 리스트에 추가
    if(bb["per_b"] < 0):
        alert_0_list.append(ticker)
    
    # %B 값 1 초과 시(과매수, 현재가가 볼린저 밴드 상단 위에 위치하면) 텔레그램 메시지 보낼 tickers 리스트에 추가
    if(bb["per_b"] > 1):
        alert_1_list.append(ticker)

# 과매도 Tickers 리스트 텔레그램 메시지 전송
if alert_0_list:
    message = f"Binance {INTERVAL} 차트 볼린저밴드 과매도 Tickers: {alert_0_list}"
    bot.sendMessage(TELEGRAM_CHAT_ID, text=message)

# 과매수 Tickers 리스트 텔레그램 메시지 전송
if alert_1_list:
    message = f"Binance {INTERVAL} 차트 볼린저밴드 과매수 Tickers: {alert_1_list}"
    bot.sendMessage(TELEGRAM_CHAT_ID, text=message)