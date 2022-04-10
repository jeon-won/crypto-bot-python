from dotenv import load_dotenv
from playsound import playsound
import numpy as np
import os
import time
import datetime
import telegram
import ccxt
"""
Binance/detect_candle_15m.py
* Date: 2022. 3. 1.
* Author: Jeon Won
* Func: 바이낸스 15분봉 차트 캔들 크기(시가와 종가의 차이)가 평균 크기 이상일 때 텔레그램 메시지 전송
* Usage: `python3 Binance/detect_candle_15m.py`
"""

load_dotenv()

INTERVAL = "15m"   # 15분봉 조사
COUNT = 96         # 캔들 몇개를 조사할 것인가?
MULTIPLIER = 3     # 평균 캔들 크기의 몇 배일 때 알림을 보낼 것인가?
SLEEP_TIME = 0.1   # 다음 ticker 조사하기 전 쉬는 시간(초)
ALARM_TELEGRAM = False  # 텔레그램 메시지 전송 여부
ALARM_SOUND = True      # 알림 사운드 재생 여부
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")      # 텔레그렘 봇 토큰
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")  # 텔레그램 봇 아이디

bot = telegram.Bot(TELEGRAM_TOKEN)
binance = ccxt.binance()
tickers = ["BTC/USDT", "ETH/USDT", "XRP/USDT", "SOL/USDT", "SAND/USDT", "BNB/USDT", "AXS/USDT", "ATOM/USDT", "DOGE/USDT", "EOS/USDT", 
    "BCH/USDT",  "LTC/USDT", "ADA/USDT", "ETC/USDT", "LINK/USDT", "TRX/USDT", "DOT/USDT", "MATIC/USDT", "UNI/USDT", "ICP/USDT", 
    "AAVE/USDT", "FIL/USDT", "XLM/USDT", "XTZ/USDT", "SUSHI/USDT", "THETA/USDT", "AVAX/USDT", "LUNA/USDT", "DASH/USDT", "SHIB/USDT", 
    "XEM/USDT", "MANA/USDT", "GALA/USDT", "DYDX/USDT", "CRV/USDT", "NEAR/USDT", "EGLD/USDT", "KSM/USDT", "AR/USDT", "REN/USDT", 
    "FTM/USDT"]
notified_tickers = []  # 텔레그램 메시지 보낸 ticker 리스트(15분마다 초기화됨)

while True:
    try:
        for ticker in tickers:
            ohlcvs = binance.fetch_ohlcv(ticker, INTERVAL, limit=COUNT)

            # 평균 캔들 크기(시가와 종가의 차이) 계산
            list_oc = []
            for ohlcv in ohlcvs:
                abs_oc = abs(ohlcv[1] - ohlcv[4])
                list_oc.append(abs_oc)
            avg_oc = np.average(list_oc)  # 평균 캔들 크기
            
            # 현재 캔들 크기(시가와 종가의 차이) 계산
            current_open = ohlcvs[len(ohlcvs)-1][1]
            current_close = ohlcvs[len(ohlcvs)-1][4]
            current_abs_oc = abs(current_open - current_close)  # 현재 캔들 크기

            # 현재 캔들 크기가 평균 캔들 크기의 MULTIPLIER배 이상이면 
            # 사운드 재생
            if(current_abs_oc >= avg_oc * MULTIPLIER and notified_tickers.count(ticker) == 0 and ALARM_SOUND):
                notified_tickers.append(ticker)
                print(f"Binance {INTERVAL} 차트 캔들 크기 평균 {MULTIPLIER}배 이상 Ticker: {ticker}")
                playsound('/Users/jeonwon/Code/crypto-bot-python/alarm.mp3')

            # 텔레그램 메시지 전송
            if(current_abs_oc >= avg_oc * MULTIPLIER and notified_tickers.count(ticker) == 0 and ALARM_TELEGRAM):
                notified_tickers.append(ticker)
                message = f"Binance {INTERVAL} 차트 캔들 크기 평균 {MULTIPLIER}배 이상 Ticker: {ticker}"
                bot.sendMessage(TELEGRAM_CHAT_ID, text=message)

            # 봉 마다 한 번 알림이 오도록 0, 15, 30, 45분마다 notified_tickers 초기화
            now = datetime.datetime.now()
            mod = divmod(now.minute, 15)[1]
            is_multiple_15 = True if mod == 0 else False
            if(is_multiple_15 and now.second > 5 and now.second < 10):
                notified_tickers.clear()

            time.sleep(SLEEP_TIME)

    except Exception as e:
        print(e)
        time.sleep(1)