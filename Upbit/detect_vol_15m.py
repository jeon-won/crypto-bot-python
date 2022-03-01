from dotenv import load_dotenv
import os
import time
import datetime
import telegram
import pyupbit
import module_upbit
"""
Upbit/detect_vol_15m.py
* Date: 2022. 2. 20.
* Author: Jeon Won
* Func: 업비트 15분봉 차트 거래량이 평균 이상일 때 텔레그램 메시지 전송
* Usage: `python3 Upbit/detect_vol_15m.py`
"""

load_dotenv()

INTERVAL = "minute15"
COUNT = 120       # 거래량 이동평균
SLEEP_TIME = 0.2  # 다음 ticker 조사 시 쉴 시간(초). 안 쉬면 API 호출 제한 걸림
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")      # 텔레그렘 봇 토큰
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")  # 텔레그램 봇 아이디

bot = telegram.Bot(TELEGRAM_TOKEN)
tickers = module_upbit.get_vol_top_tickers(10, remove_tickers=["KRW-BTC", "KRW-ETH"])  # 최근 24시간 거래량 Top 10 tickers 리스트
notified_tickers = []

while True:
    try:
        # 각 ticker 조사
        for ticker in tickers:
            
            ohlcvs = pyupbit.get_ohlcv(ticker, INTERVAL, COUNT)      # ticker의 시가, 고가, 저가, 종가, 거래량
            current_vol = round(ohlcvs["volume"][len(ohlcvs)-1], 0)  # ticker의 현재 거래량
            mean = round(ohlcvs["volume"].mean(), 0)                 # ticker의 거래량 평균
            open_price = ohlcvs["open"][len(ohlcvs)-1]                  # ticker의 시가
            close_price = ohlcvs["close"][len(ohlcvs)-1]                # ticker의 종가
            is_blackbody = True if open_price > close_price else False  # 음봉 여부
            print(f"{ticker} mean: {mean} / current: {current_vol} / {is_blackbody}")

            # 현재 거래량이 평균 이상이고 음봉일 때 텔레그램 메시지 전송
            if(current_vol > mean and is_blackbody == True and notified_tickers.count(ticker) == 0):
                notified_tickers.append(ticker)
                message = f"Upbit {ticker} {INTERVAL} 차트 거래량 평균 이상"
                bot.sendMessage(TELEGRAM_CHAT_ID, text=message)
                print(message)

            time.sleep(SLEEP_TIME)
        
            # 봉 마다 한 번 알림이 오도록 0, 15, 30, 45분마다 notified_tickers 초기화
            now = datetime.datetime.now()
            mod = divmod(now.minute, 15)[1]
            is_multiple_15 = True if mod == 0 else False
            if(is_multiple_15 and now.second < 5):
                notified_tickers.clear()

    except Exception as e:
        print(e)
        time.sleep(1)