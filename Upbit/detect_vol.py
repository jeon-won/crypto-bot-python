from dotenv import load_dotenv
import os
import sys
import telegram
import pyupbit
import module_upbit
"""
detect_vol_upbit.py
* Date: 2021. 10. 5.
* Author: Jeon Won
* Func: 업비트 차트 거래량이 급증했을 때 텔레그램 메시지 전송(판단기준: 현재 거래량이 (평균거래량 + 승수 * 표준편차) 이상일 때)
* Usage: 15분봉 차트에 승수를 2로 하는 조사 명령어는 `python3 detect_vol_upbit.py minute15 2` (minute1~240, day 등 사용)
"""

load_dotenv()

INTERVAL = sys.argv[1]  # 차트 종류
N = float(sys.argv[2])  # 승수
COUNT = 120             # 거래량 이동평균
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")      # 텔레그렘 봇 토큰
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")  # 텔레그램 봇 아이디

bot = telegram.Bot(TELEGRAM_TOKEN)
tickers = module_upbit.get_vol_top_tickers(10)  # 최근 24시간 거래량 Top 10 tickers 리스트
# tickers = ["KRW-BTC", "KRW-ETH", "KRW-XRP"]  # 또는 수동으로 Tickers 지정
alert_list = []

# 각 ticker 조사
for ticker in tickers:
    # ticker의 시가, 고가, 저가, 종가, 거래량을 얻어옴
    ohlcvs = pyupbit.get_ohlcv(ticker, interval=INTERVAL, count=COUNT)
    
    mean = ohlcvs["volume"].mean() # 평균
    std = ohlcvs["volume"].std()   # 표준편차
    n_std = mean + N * std         # 현재 거래량이 이 값보다 높으면 거래량이 급증한 것으로 판단
    
    current_vol = ohlcvs["volume"][len(ohlcvs)-1] # 현재 거래량
    open_price = ohlcvs["open"][len(ohlcvs)-1]    # 현재 시가
    close_price = ohlcvs["close"][len(ohlcvs)-1]  # 현재 종가

    # 현재 거래량이 n_std 값을 넘어서고, 음봉인 경우 텔레그램 메시지 전송(업비트는 숏 포지션을 잡을 수 없으므로...)
    if(current_vol >= n_std and open_price >= close_price):
        alert_list.append(ticker)

# 텔레그램 메시지 전송
if alert_list:
    message = f"Upbit {INTERVAL} 차트 거래량 폭발 Tickers: {alert_list}"
    bot.sendMessage(TELEGRAM_CHAT_ID, text=message)