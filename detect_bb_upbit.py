import module_upbit
import telegram
import time
import datetime
import sys

"""
detect_bb_upbit.py
* Date: 2021. 10. 5.
* Author: Jeon Won
* Func: 업비트 차트의 현재가가 볼린저밴드 하한선 밑에 있으면 텔레그램 메시지 전송
* Usage: 5분봉 차트 조사 명령어는 `python3 detect_bb_upbit.py 5` (3, 5, 15, 30, 60분 봉에만 사용)
"""

##### 상수 #######################
MIN = int(sys.argv[1])
INTERVAL = f"minute{MIN}"         # 차트 종류
SLEEP_TIME = 0.2                  # API 호출 후 잠시 쉴 시간(초 단위)

TELEGRAM_TOKEN = "tElEgRaMtOkEn"  # 텔레그렘 봇 토큰
TELEGRAM_CHAT_ID = 1234567890     # 텔레그램 봇 아이디

COUNT = 20                        # 분석할 차트의 최근 봉 개수
BB_COUNT = 20                     # 볼린저 밴드(BB)의 길이
BB_MULTIPLIER = 2                 # 볼린저 밴드(BB)에서 상하한선을 정하기 위해 사용하는 곱(승수)
##################################

##### 변수 #######################
bot = telegram.Bot(TELEGRAM_TOKEN)
notified_tickers = []
# tickers = ["KRW-BTC", "KRW-ETH", "KRW-XRP"]
##################################

while True:
    # 최근 24시간 거래량 TOP 10 코인 조사
    tickers = module_upbit.get_vol_top_tickers(10)  

    try: 
        # 코인들 중에서
        for ticker in tickers:
            bb = module_upbit.get_bb(ticker, INTERVAL, BB_COUNT, BB_MULTIPLIER)
            current_price = module_upbit.get_current_price(ticker)

            # 현재가가 볼린저 밴드 하한선 밑에 있으면 알림
            if(current_price < bb["lbb"]):
                if(notified_tickers.count(ticker) == 0):
                    notified_tickers.append(ticker)
                    message = f"{ticker} {MIN}분봉 BB 하단 터치했습니다. (현재가: {current_price})"
                    bot.sendMessage(TELEGRAM_CHAT_ID, text=message)
                    print(message)
            
            # API 호출 제한에 걸리지 않도록 적절히 쉼
            time.sleep(SLEEP_TIME)

        # 알림이 중복되어 오지 않도록 notified_tickers 관리
        now = datetime.datetime.now()
        mod = divmod(now.minute, MIN)[1]
        is_multiple = True if mod == 0 else False
        if(is_multiple and now.second < 10):
            notified_tickers.clear()

    except Exception as e:
        print(e)
        time.sleep(1)
