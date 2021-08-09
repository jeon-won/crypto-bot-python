import cryptofunc
import pyupbit
import telegram
import time
import datetime

"""
AutoDetect3RCandle.py
* Date: 2021. 8. 10.
* Author: Jeon Won
* Func: 15분봉 차트에서 연속 3음봉이 뜨면 텔레그램 메시지 전송
* Notice: 급조해서 만듦...
"""

##### 상수 #############################################
INTERVAL = "minute15"             # 차트 종류
TELEGRAM_TOKEN = "tElEgRaMtOkEn"  # 텔레그렘 봇 토큰
TELEGRAM_CHAT_ID = 123456789      # 텔레그램 봇 아이디
#######################################################

##### 변수 #############################################
bot = telegram.Bot(TELEGRAM_TOKEN)
notified_tickers = []
tickers = ["KRW-BTC", "KRW-ETH", "KRW-ETC", "KRW-XRP"]
#######################################################

while True:
    try: 
        now = datetime.datetime.now()
        mod = divmod(now.minute, 15)[1]

        # 15분봉 갱신 1분 전에 티커들을 조사함
        if(mod == 14):
            for ticker in tickers:
                # 최근 알림을 보낸 티커가 아니면 최근에 생성된 봉 3개가 모두 음봉인지 조사
                if(notified_tickers.count(ticker) == 0):
                    ohlcv = pyupbit.get_ohlcv(ticker, interval=INTERVAL, count=3)
                    rate_1 = ohlcv["close"][0] / ohlcv["open"][0]
                    rate_2 = ohlcv["close"][1] / ohlcv["open"][1]
                    rate_3 = ohlcv["close"][2] / ohlcv["open"][2]

                    # 최근 3개 봉이 모두 음봉이면 텔레그램 메시지 전송
                    if(rate_1 < 1 and rate_2 < 1 and rate_3 < 1):
                        notified_tickers.append(ticker)
                        message = f"{ticker} 15분봉 3개 음봉입니다."
                        bot.sendMessage(TELEGRAM_CHAT_ID, text=message)
                    
                    time.sleep(1)

        # 15분봉 갱신 직후 알림보낸 티커 초기화
        elif(mod == 0):
            notified_tickers.clear()
            time.sleep(780)

        # 그 외의 시간엔 대기
        else:
            time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(SLEEP_TIME)
