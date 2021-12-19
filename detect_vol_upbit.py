import sys
import telegram
import pyupbit
import module_upbit
"""
detect_vol_upbit.py
* Date: 2021. 10. 5.
* Author: Jeon Won
* Func: 업비트 차트 거래량이 급증했을 때 텔레그램 메시지 전송(판단기준: 현재 거래량이 (평균거래량 + N * 표준편차) 이상일 때)
* Usage: 15분봉 차트 조사 명령어는 `python3 detect_vol_upbit.py 15` (minute1~240, day 등 사용)
"""

##### 상수 #############################################
INTERVAL = sys.argv[1]  # 차트 종류
N = 2                   # 승수
TELEGRAM_TOKEN = "tElEgRaMtOkEn"  # 텔레그렘 봇 토큰
TELEGRAM_CHAT_ID = 1234567890     # 텔레그램 봇 아이디
#######################################################

##### 변수 #############################################
bot = telegram.Bot(TELEGRAM_TOKEN)
# tickers = ["KRW-BTC", "KRW-ETH", "KRW-XRP"]
#######################################################

tickers = module_upbit.get_vol_top_tickers(10)

for ticker in tickers:
    ohlcvs = pyupbit.get_ohlcv(ticker, interval=INTERVAL)
    mean = ohlcvs["volume"].mean()
    std = ohlcvs["volume"].std()
    N_range = mean + N * std
    current_vol = ohlcvs["volume"][len(ohlcvs)-1]
    prev_vol = ohlcvs["volume"][len(ohlcvs)-2]

    # 현재 거래량과 직전 거래량이 n-시그마 범위를 넘어선 경우 텔레그램 메시지 전송
    if(current_vol >= N_range):
        message = f"Upbit {ticker} {INTERVAL}분봉 차트 거래량 ★폭발★"
        bot.sendMessage(TELEGRAM_CHAT_ID, text=message)
        print(message)