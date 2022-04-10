from dotenv import load_dotenv
from playsound import playsound
from module_upbit import get_vol_top_tickers
import os
import time
import datetime
import telegram
import pyupbit
"""
Upbit/detect_candle_15m.py
* Date: 2022. 3. 1.
* Author: Jeon Won
* Func: 업비트 15분봉 차트 캔들 크기(시가와 종가의 차이)가 평균 크기 이상일 때 텔레그램 메시지 전송
* Usage: `python3 Upbit/detect_candle_15m.py`
"""

load_dotenv()

INTERVAL = "minute15"  # 15분봉 조사
COUNT = 96             # 캔들 몇개를 조사할 것인가?
MULTIPLIER = 3         # 평균 캔들 크기의 몇 배일 때 알림을 보낼 것인가?
SLEEP_TIME = 0.15      # 다음 ticker 조사하기 전 쉬는 시간(초)
ALARM_TELEGRAM = False  # 텔레그램 메시지 전송 여부
ALARM_SOUND = True     # 알림 사운드 재생 여부
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")      # 텔레그렘 봇 토큰
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")  # 텔레그램 봇 아이디

bot = telegram.Bot(TELEGRAM_TOKEN)
notified_tickers = []  # 텔레그램 메시지 보낸 ticker 리스트(15분마다 초기화됨)

while True:
    try: 
        tickers = get_vol_top_tickers(10, remove_tickers=["KRW-BTC", "KRW-ETH"])
        
        for ticker in tickers:
            df = pyupbit.get_ohlcv(ticker, INTERVAL, COUNT)
            
            # 평균 캔들 크기(시가와 종가의 차이) 계산
            df_oc = abs(df["open"] - df["close"])
            avg_oc = df_oc.mean()

            # 현재 캔들 크기(시가와 종가의 차이) 계산
            current_open = df["open"][len(df)-1]
            current_close = df["close"][len(df)-1]
            current_abs_oc = abs(current_open - current_close)

            # 현재 음봉캔들 크기가 평균 캔들 크기의 MULTIPLIER배 이상이면 
            is_blackbody = True if current_open > current_close else False

            # 사운드 재생
            if(current_abs_oc >= avg_oc * MULTIPLIER and is_blackbody == True and notified_tickers.count(ticker) == 0 and ALARM_SOUND):
                notified_tickers.append(ticker)
                playsound("/Users/jeonwon/Code/crypto-bot-python/alarm.mp3")
                print(f"Upbit {INTERVAL} 차트 캔들 크기 평균 {MULTIPLIER}배 이상 Ticker: {ticker}")

            # 텔레그램 메시지 전송
            if(current_abs_oc >= avg_oc * MULTIPLIER and is_blackbody == True and notified_tickers.count(ticker) == 0 and ALARM_TELEGRAM):
                notified_tickers.append(ticker)
                message = f"Upbit {INTERVAL} 차트 캔들 크기 평균 {MULTIPLIER}배 이상 Ticker: {ticker}"
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