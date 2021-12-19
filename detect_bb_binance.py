import module_binance
import telegram
import sys

"""
detect_bb_binance.py
* Date: 2021. 10. 5.
* Author: Jeon Won
* Func: 바이낸스 차트의 현재가가 볼린저 밴드 상단 또는 하단을 터치하는 캔들 발생 시 텔레그램 메시지 전송
* Usage: 15분봉 차트 조사 명령어는 `python3 AutoDetectBBBinance.py 15m` (1m, 3m, 5m, 15m, 30m, 1h, 4h, 6h, 12h, 1d 사용)
"""

##### 상수 ###################################
INTERVAL = sys.argv[1]  # 몇분 봉인가?
TELEGRAM_TOKEN = "tElEgRaMtOkEn"  # 텔레그렘 봇 토큰
TELEGRAM_CHAT_ID = 1234567890     # 텔레그램 봇 아이디

BB_COUNT = 20      # 볼린저 밴드 길이
BB_MULTIPLIER = 2  # 볼린저 밴드에서 상하한선을 정하기 위해 사용하는 곱(승수)
#############################################

##### 변수 ##################################
bot = telegram.Bot(TELEGRAM_TOKEN)
tickers = ["BTC/USDT"]
#############################################

# 알림을 보내지 않은 ticker 조사
for ticker in tickers:                 
    bb = module_binance.get_bb(ticker, INTERVAL, BB_COUNT, BB_MULTIPLIER)

    # # 현재가가 볼린저 밴드 상단 위에 위치하면 텔레그램 메시지 발송
    # if(bb["current"] > bb["ubb"]):                                                            
    #     message = f"Binance {ticker} {INTERVAL} 차트 볼린저밴드 상단 터치 (현재가: {bb['current']})"
    #     bot.sendMessage(TELEGRAM_CHAT_ID, text=message)

    # # 현재가가 볼린저 밴드 하단 아래에 위치하면 텔레그램 메시지 발송
    # if(bb["current"] < bb["lbb"]):                                                            
    #     message = f"Binance {ticker} {INTERVAL} 차트 볼린저밴드 하단 터치 (현재가: {bb['current']})"
    #     bot.sendMessage(TELEGRAM_CHAT_ID, text=message)
    
    # %B 값 1 초과 시 텔레그램 메시지 전송
    if(bb["per_b"] > 1):
        message = f"binance {ticker} {INTERVAL} 차트 볼린저밴드 %B 값 1 초과 (현재가: {bb['current']}"
        bot.sendMessage(TELEGRAM_CHAT_ID, text=message)

    # %B 값 0 미만 시 텔레그램 메시지 전송
    if(bb["per_b"] < 0):
        message = f"binance {ticker} {INTERVAL} 차트 볼린저밴드 %B 값 0 미만 (현재가: {bb['current']}"
        bot.sendMessage(TELEGRAM_CHAT_ID, text=message)
