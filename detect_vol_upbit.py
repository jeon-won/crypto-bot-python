import sys
import telegram
import time
from datetime import datetime
import pyupbit
import module_upbit
"""
detect_vol_upbit.py
* Date: 2021. 10. 5.
* Author: Jeon Won
* Func: 업비트 차트 거래량이 급증했을 때 텔레그램 메시지 전송(판단기준: 현재 거래량이 (평균거래량 + N * 표준편차) 이상일 때)
* Usage: 5분봉 차트 조사 명령어는 `python3 detect_vol_upbit.py 5` (3, 5, 15, 30, 60분 봉에만 사용)
"""

##### 상수 #############################################
MIN = int(sys.argv[1])     # 몇분 봉인가?
INTERVAL = f"minute{MIN}"  # 차트 종류
N = 2                      # 승수
SLEEP_TIME = 0.2

TELEGRAM_TOKEN = "tElEgRaMtOkEn"  # 텔레그렘 봇 토큰
TELEGRAM_CHAT_ID = 1234567890     # 텔레그램 봇 아이디
#######################################################

##### 변수 #############################################
bot = telegram.Bot(TELEGRAM_TOKEN)
notified_tickers = []
# tickers = ["KRW-BTC", "KRW-ETH", "KRW-XRP"]
#######################################################

while True:
    try: 
        tickers = module_upbit.get_vol_top_tickers(10)

        for ticker in tickers:
            if(notified_tickers.count(ticker) == 0):
                ohlcvs = pyupbit.get_ohlcv(ticker, interval=INTERVAL)
                mean = ohlcvs["volume"].mean()
                std = ohlcvs["volume"].std()
                N_range = mean + N * std
                current_vol = ohlcvs["volume"][len(ohlcvs)-1]
                prev_vol = ohlcvs["volume"][len(ohlcvs)-2]

                # 현재 거래량과 직전 거래량이 n-시그마 범위를 넘어선 경우 텔레그램 메시지 전송
                if(current_vol >= N_range and notified_tickers.count(ticker) == 0):
                    message = f"Upbit {ticker} {MIN}분봉 차트 거래량 ★폭발★"
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