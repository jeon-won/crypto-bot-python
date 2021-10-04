import sys
import numpy as np
import ccxt
import telegram
import time
from datetime import datetime
"""
detect_vol_binance.py
* Date: 2021. 10. 5.
* Author: Jeon Won
* Func: 바이낸스 차트 거래량이 급증했을 때 텔레그램 메시지 전송(판단기준: 현재 거래량이 (평균거래량 + N * 표준편차) 이상일 때)
* Usage: 5분봉 차트 조사 명령어는 `python detect_vol_binance.py 5` (3, 5, 15, 30, 60분 봉에만 사용)
"""

##### 상수 #############################################
MIN = int(sys.argv[1])  # 몇분 봉인가?
INTERVAL = f"{MIN}m"    # 차트 종류
N = 1                   # 승수
SLEEP_TIME = 0.5

TELEGRAM_TOKEN = "tElEgRaMtOkEn"  # 텔레그렘 봇 토큰
TELEGRAM_CHAT_ID = 1234567890     # 텔레그램 봇 아이디
#######################################################

##### 변수 #############################################
bot = telegram.Bot(TELEGRAM_TOKEN)
notified_tickers = []
tickers = ["BTC/USDT"]
binance = ccxt.binance()
#######################################################

while True:
    try:
        # 알림을 보내지 않은 ticker에 대해 조사
        for ticker in tickers:
            if(notified_tickers.count(ticker) == 0):
                ohlcvs = binance.fetch_ohlcv(ticker, INTERVAL)

                # numpy 배열에 거래량 데이터만 담기
                ohlcvs_np = np.array([])
                for ohlcv in ohlcvs:
                    ohlcvs_np = np.append(ohlcvs_np, ohlcv[5])

                mean = ohlcvs_np.mean()  # 평균
                std = ohlcvs_np.std()    # 표준편차
                n_std = mean + N * std   # 현재 거래량이 이 값보다 높으면 거래량이 급증한 것으로 판단
                current_vol = ohlcvs[len(ohlcvs) - 1][5]  # 현재 거래량

                # 현재 거래량이 급증한 경우 텔레그램 메시지 전송
                if(current_vol >= n_std):
                    message = f"Binance {ticker} {MIN}분봉 차트 거래량 ★폭발★"
                    bot.sendMessage(TELEGRAM_CHAT_ID, text=message)
                    notified_tickers.append(ticker)
                    print(message)

                
                # API 호출 제한에 걸리지 않도록 적절히 쉼
                time.sleep(SLEEP_TIME)

        # 알림이 중복되어 오지 않도록 notified_tickers 관리
        now = datetime.now()
        mod = divmod(now.minute, MIN)[1]
        is_multiple = True if mod == 0 else False
        if(is_multiple and now.second < 10):
            notified_tickers.clear()
            
    except Exception as e:
        print(e)
        time.sleep(1)