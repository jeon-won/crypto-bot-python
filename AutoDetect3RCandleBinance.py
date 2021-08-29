import ccxt
import time
import telegram
import sys
from datetime import datetime
"""
AutoDetect3RCandle.py
* Date: 2021. 8. 29.
* Author: Jeon Won
* Func: 바이낸스 차트에서 연속 3음봉이 뜨면 텔레그램 메시지 전송
* Usage: 5분봉 차트 조사 명령어는 `nohup python3 AutoDetect3RCandleBinance.py 5 &` 
"""

##### 상수 #############################################
MIN = int(sys.argv[1])  # 몇분 봉인가?
INTERVAL = f"{MIN}m"    # 차트 종류
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
        now = datetime.now()
        mod = divmod(now.minute, MIN)[1]

        # 봉 갱신 1분 전에 티커들을 조사함
        if(mod == MIN - 1):
            for ticker in tickers:
                # 최근 알림을 보낸 티커가 아니면 최근에 생성된 봉 3개가 모두 음봉인지 조사
                if(notified_tickers.count(ticker) == 0):
                    ohlcvs = binance.fetch_ohlcv(ticker, INTERVAL)
                    ohlcvs_len = len(ohlcvs)
                    ohlcvs_edited = ohlcvs[ohlcvs_len-3:ohlcvs_len]
                    rate_1 = ohlcvs_edited[0][4] / ohlcvs_edited[0][1] < 1
                    rate_2 = ohlcvs_edited[1][4] / ohlcvs_edited[1][1] < 1
                    rate_3 = ohlcvs_edited[2][4] / ohlcvs_edited[2][1] < 1

                    # 최근 3개 봉이 모두 음봉이면 텔레그램 메시지 전송
                    if(rate_1 and rate_2 and rate_3):
                        notified_tickers.append(ticker)
                        message = f"Binance {ticker} {MIN}분봉 3개 음봉입니다."
                        bot.sendMessage(TELEGRAM_CHAT_ID, text=message)
                    
                time.sleep(3)

        # 봉 갱신 직후 알림보낸 티커 초기화
        elif(mod == 0):
            notified_tickers.clear()
            time.sleep(60 * (MIN - 2))

        # 그 외의 시간엔 대기
        else:
            time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)
