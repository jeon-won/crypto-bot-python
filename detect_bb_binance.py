import module_binance
import time
import telegram
import sys
from datetime import datetime

"""
detect_bb_binance.py
* Date: 2021. 10. 5.
* Author: Jeon Won
* Func: 바이낸스 차트의 현재가가 볼린저 밴드 상단 또는 하단을 터치하는 캔들 발생 시 텔레그램 메시지 전송
* Usage: 5분봉 차트 조사 명령어는 `python3 AutoDetectBBBinance.py 5` (3, 5, 15, 30, 60분 봉에만 사용)
"""

##### 상수 ###################################
MIN = int(sys.argv[1])  # 몇분 봉인가?
INTERVAL = f"{MIN}m"    # 차트 종류
SLEEP_TIME = 0.5

TELEGRAM_TOKEN = "tElEgRaMtOkEn"  # 텔레그렘 봇 토큰
TELEGRAM_CHAT_ID = 1234567890     # 텔레그램 봇 아이디
TELEGRAM_BOT = telegram.Bot(TELEGRAM_TOKEN)

BB_COUNT = 20      # 볼린저 밴드 길이
BB_MULTIPLIER = 2  # 볼린저 밴드에서 상하한선을 정하기 위해 사용하는 곱(승수)
#############################################

##### 변수 ##################################
bot = telegram.Bot(TELEGRAM_TOKEN)
notified_tickers = []
tickers = ["BTC/USDT"]
#############################################

while(True):
    try:
        # 알림을 보내지 않은 ticker 조사
        for ticker in tickers:                 
            if(notified_tickers.count(ticker) == 0):  
                bb = module_binance.get_bb(ticker, INTERVAL, BB_COUNT, BB_MULTIPLIER)
                # 현재가가 볼린저 밴드 상단 위에 위치하면 텔레그램 메시지 발송
                if(bb["current"] > bb["ubb"]):                                                            
                    message = f"Binance {ticker} {MIN}분봉 BB 상단 터치했습니다. (현재가: {bb['current']})"
                    bot.sendMessage(TELEGRAM_CHAT_ID, text=message)
                    notified_tickers.append(ticker)

                # 현재가가 볼린저 밴드 하단 아래에 위치하면 텔레그램 메시지 발송
                if(bb["current"] < bb["lbb"]):                                                            
                    message = f"Binance {ticker} {MIN}분봉 BB 하단 터치했습니다. (현재가: {bb['current']})"
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