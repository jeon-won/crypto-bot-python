import cryptofunc
import pyupbit
import telegram
import time
import datetime

"""
AutoDetectFall.py
* Date: 2021. 6. 9.
* Author: Jeon Won
* Func: 다음 두 가지 조건 중 한 가지를 만족하면 텔레그램 메시지 전송
  - 현재가가 볼린저밴드 하한선 밑에 있고 스토캐스틱 %K 값이 낮을 때
  - 5분봉 3틱룰 적용 가능성이 있는 경우
* Notice: 산식이 맞는건지 모르게씀. 업비트에서 보는 값과 조금 오차가 있는 듯...
"""

##### 상수 ##################################################################################
INTERVAL = "minute5"                 # 차트 종류
SLEEP_TIME = 0.1                     # API 호출 후 잠시 쉴 시간(초 단위)
TICK_ESTI_RATE = 1                   # 캔들 크기가 이 비율보다 낮으면 1틱으로 산정(1은 0%)

TELEGRAM_TOKEN = "mYtElEgRaMtOkEn"  # 텔레그렘 봇 토큰
TELEGRAM_CHAT_ID = 123456789        # 텔레그램 봇 아이디

COUNT = 20                          # 분석할 차트의 최근 봉 개수
BB_COUNT = 20                       # 볼린저 밴드(BB)의 길이
BB_MULTIPLIER = 2                   # 볼린저 밴드(BB)에서 상하한선을 정하기 위해 사용하는 곱(승수)

STOCH_COUNT = 20                    # 스토캐스틱(Stochastic)의 길이
STOCH_UPPER_LIMIT = 0.8             # 스토캐스틱(Stochastic) 상한선(Upper Limit)
STOCH_LOWER_LIMIT = 0.2             # 스토캐스틱(stochastic) 하한선(Lower Limit)
############################################################################################

##### 변수 ##################################################################################
bot = telegram.Bot(TELEGRAM_TOKEN)
notified_tickers = []
tickers = ["KRW-BTC", "KRW-ETH", "KRW-ETC", "KRW-XRP", "KRW-XLM", "KRW-DOGE", "KRW-EOS", "KRW-ADA", "KRW-BCH", "KRW-LTC", "KRW-QTUM"]
# 또는 tickers = cryptofunc.get_coin_tickers()
############################################################################################

while True:
    try: 
        # 코인들 중에서
        for ticker in tickers:
            bb = cryptofunc.get_bb(ticker, INTERVAL, BB_COUNT, BB_MULTIPLIER)
            stoch_k = cryptofunc.get_stoch_k(ticker, INTERVAL, STOCH_COUNT)
            current_price = cryptofunc.get_current_price(ticker)

            # 스토캐스틱 %K 값이 낮고 현재가가 볼린저 밴드 하한선 밑에 있으면 급락 알림
            if((stoch_k < STOCH_LOWER_LIMIT) and (current_price < bb["lbb"])):
                if(notified_tickers.count(ticker) == 0):
                    notified_tickers.append(ticker)
                    message = f"{ticker} BB 하단 터치했습니다. (현재가: {current_price})"
                    bot.sendMessage(TELEGRAM_CHAT_ID, text=message)

            # 최근 차트에서 음봉 캔들을 3개 발견하면 3틱룰 가능성 알림
            tick = 0
            df = pyupbit.get_ohlcv(ticker, INTERVAL, COUNT)
            time.sleep(SLEEP_TIME)
            for i in range(COUNT-2, COUNT-7, -1):  # 최근 차트를 조사하여
                open_price = df["open"][i]
                close_price = df["close"][i]
                rate = close_price / open_price
                if(rate < TICK_ESTI_RATE):         # 음봉을 발견하면
                    tick = tick + 1                # tick 값을 1 증가
                else:                              # 양봉을 발견하면
                    break                          # 더 이상 조사하지 않음
            
            if(tick >= 3 and notified_tickers.count(ticker) == 0):
                notified_tickers.append(ticker)
                message = f"{ticker} 3틱룰 적용 가능성이 있습니다. (현재가: {current_price})"
                bot.sendMessage(TELEGRAM_CHAT_ID, text=message)

        # 5분마다 notified_tickers 초기화
        now = datetime.datetime.now()
        mod = divmod(now.minute, 5)[1]
        is_multiple_5 = True if mod == 0 else False
        if(is_multiple_5 and now.second < 10):
            notified_tickers.clear()

    except Exception as e:
        print(e)
        time.sleep(1)
