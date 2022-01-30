from dotenv import load_dotenv
import os
import sys
import numpy as np
import ccxt
import telegram
"""
detect_vol_binance.py
* Date: 2021. 10. 5.
* Author: Jeon Won
* Func: 바이낸스 차트 거래량이 급증했을 때 텔레그램 메시지 전송(판단기준: 현재 거래량이 (평균거래량 + 승수 * 표준편차) 이상일 때)
* Usage: 15분봉 차트에 승수를 2로 하는 조사 명령어는 `python3 detect_vol_binance.py 15m 2` (1m, 3m, 5m, 15m, 30m, 1h, 4h, 6h, 12h, 1d 사용)
"""

load_dotenv()

INTERVAL = sys.argv[1]  # 차트 종류
N = float(sys.argv[2])  # 승수
COUNT = 120             # 거래량 이동평균
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")      # 텔레그렘 봇 토큰
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")  # 텔레그램 봇 아이디

bot = telegram.Bot(TELEGRAM_TOKEN)
binance = ccxt.binance()
tickers = ["BTC/USDT"]
alert_list = []  # 텔레그램 메시지 보낼 tickers 리스트

# 각 ticker 조사
for ticker in tickers:
    # ticker의 시가, 고가, 저가, 종가, 거래량을 얻어온 후 numpy 배열에 거래량 데이터만 담기
    ohlcvs = binance.fetch_ohlcv(ticker, INTERVAL, limit=COUNT)
    ohlcvs_np = np.array([])
    for ohlcv in ohlcvs:
        ohlcvs_np = np.append(ohlcvs_np, ohlcv[5])

    current_vol = ohlcvs[len(ohlcvs) - 1][5]  # 현재 거래량
    mean = ohlcvs_np.mean()  # 평균
    std = ohlcvs_np.std()    # 표준편차
    n_std = mean + N * std   # 현재 거래량이 이 값보다 높으면 거래량이 급증한 것으로 판단

    # 현재 거래량이 n_std 값을 넘어선 경우 텔레그램 메시지 보낼 tickers 리스트에 추가
    if(current_vol >= n_std):
        alert_list.append(ticker)

# 텔레그램 메시지 전송
if alert_list:
    message = f"Binance {INTERVAL} 차트 거래량 폭발 Tickers: {alert_list}"
    bot.sendMessage(TELEGRAM_CHAT_ID, text=message)