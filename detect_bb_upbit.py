from dotenv import load_dotenv
import os
import module_upbit
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
tickers = module_upbit.get_vol_top_tickers(10)
# tickers = ["KRW-BTC", "KRW-ETH", "KRW-XRP"]

# 각 ticker 조사
for ticker in tickers:
    bb = module_upbit.get_bb(ticker, INTERVAL, BB_COUNT, BB_MULTIPLIER)
    
    # # 현재가가 볼린저 밴드 하단 아래에 위치하면 텔레그램 메시지 전송
    # if(bb["current"] < bb["lbb"]):
    #     message = f"Upbit {ticker} {INTERVAL} 차트 볼린저밴드 하단 터치 (현재가: {bb['current']}"
    #     bot.sendMessage(TELEGRAM_CHAT_ID, text=message)

    # %B 값 0 미만 시 텔레그램 메시지 전송
    if(bb["per_b"] < 0):
        message = f"Upbit {ticker} {INTERVAL} 차트 볼린저밴드 %B 값 0 미만 (%B: {round(bb['per_b'], 3)} / 현재가: {bb['current']})"
        bot.sendMessage(TELEGRAM_CHAT_ID, text=message)