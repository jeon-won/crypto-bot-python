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
* Usage: 15분봉 차트 조사 명령어는 `python detect_vol_binance.py 15m` (1m, 3m, 5m, 15m, 30m, 1h, 4h, 6h, 12h, 1d 사용)
"""

##### 상수 #############################################
INTERVAL = sys.argv[1]  # 차트 종류
N = 1                   # 승수
TELEGRAM_TOKEN = "tElEgRaMtOkEn"  # 텔레그렘 봇 토큰
TELEGRAM_CHAT_ID = 1234567890     # 텔레그램 봇 아이디
#######################################################

##### 변수 #############################################
bot = telegram.Bot(TELEGRAM_TOKEN)
tickers = ["BTC/USDT"]
binance = ccxt.binance()
#######################################################

# 알림을 보내지 않은 ticker에 대해 조사
for ticker in tickers:
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
        message = f"Binance {ticker} {INTERVAL} 차트 차트 거래량 ★폭발★"
        bot.sendMessage(TELEGRAM_CHAT_ID, text=message)