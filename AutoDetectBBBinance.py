import ccxt
import time
import numpy
import telegram
import sys
from datetime import datetime

"""
AutoDetectBBBinance.py
* Date: 2021. 8. 29.
* Author: Jeon Won
* Func: 바이낸스 차트에서 볼린저 밴드 상단 또는 하단 터치하는 캔들 발생 시 텔레그램 메시지 전송
* Usage: 5분봉 차트 조사 명령어는 `nohup python3 AutoDetectBBBinance.py 5 &` 
"""

##### 상수 ###################################
MIN = int(sys.argv[1])  # 몇분 봉인가?
INTERVAL = f"{MIN}m"    # 차트 종류

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


##### 함수 ##################################
def get_bb(ticker, interval, count, multipler):
    list_close = []

    binance = ccxt.binance()
    ohlcvs = binance.fetch_ohlcv(ticker, interval)
    ohlcvs_len = len(ohlcvs)
    ohlcvs_edited = ohlcvs[ohlcvs_len-count:ohlcvs_len-1]

    for ohlcv in ohlcvs_edited: # BB에 사용할 정보
        list_close.append(ohlcv[4])
    ticker = binance.fetch_ticker(ticker)
    current = ticker['close'] # 현재가
    list_close.append(current)

    std = numpy.std(list_close)      # 표준편차(종가 기준)
    mbb = numpy.average(list_close)  # 볼린저 밴드의 중심선(이동평균)
    ubb = mbb + std * multipler      # 상한선 = 중심선 + 기간 내 표준편차 * 승수
    lbb = mbb - std * multipler      # 하한선 = 중신선 + 기간 내 표준편차 * 승수

    dict_bb = {}
    dict_bb["ubb"] = ubb
    dict_bb["mbb"] = mbb
    dict_bb["lbb"] = lbb
    dict_bb["current"] = current
    return dict_bb
#############################################

while(True):
    try:
        for ticker in tickers:                        # 티커들을 조사함
            if(notified_tickers.count(ticker) == 0):  # 최근에 알림을 보낸 티커가 아니면 조사 시작
                bb = get_bb(ticker, INTERVAL, BB_COUNT, BB_MULTIPLIER)
                if(bb["current"] > bb["ubb"]):                                                    # 현재가가 볼린저 밴드 상단 위에 위치하면
                    message = f"Binance {ticker} {MIN}분봉 BB 상단 터치했습니다. (현재가: {bb['current']})" # 알림 메시지 발송
                    bot.sendMessage(TELEGRAM_CHAT_ID, text=message)
                    notified_tickers.append(ticker)
                    time.sleep(5)

                if(bb["current"] < bb["lbb"]):                                                    # 현재가가 볼린저 밴드 하단 아래에 위치하면
                    message = f"Binance {ticker} {MIN}분봉 BB 하단 터치했습니다. (현재가: {bb['current']})" # 알림 메시지 발송
                    bot.sendMessage(TELEGRAM_CHAT_ID, text=message)
                    notified_tickers.append(ticker)
                    time.sleep(5)
        
        # 특정 시간 간격마다 알림이 오도록 notified_tickers 초기화
        now = datetime.now()
        mod = divmod(now.minute, MIN)[1]
        is_multiple = True if mod == 0 else False
        if(is_multiple and now.second < 5):
            notified_tickers.clear()

        time.sleep(1)
        
    except Exception as e:
        print(e)
        time.sleep(1)