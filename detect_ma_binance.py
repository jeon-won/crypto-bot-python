from module_binance import get_prev_ma
import telegram
import sys
import time
from datetime import datetime

"""
detect_ma_binance.py
* Date: 2021. 10. 28.
* Author: Jeon Won
* Func: 5, 10, 15, 25 이동평균선이 골든(데드)크로스로 변한 순간 텔레그램 메시지 전송
* Usage: 15분봉 차트 조사 명령어는 `python3 detect_ma_binance.py 15` (3, 5, 15, 30, 60분 봉에만 사용)
* Strategy: https://youtu.be/og4BhKT6-4U
  - 골든(데드)크로스로 변하는 순간 롱(숏) 포지션 각 잡기
  - 포지션 잡은 후 이평선 간격이 좀 벌어지면 10, 15일 이평선 가격으로 물을 타거나 25일 이평선 가격으로 손절 치기
  - 익절은 알아서...
"""

##### 상수 ###################################
MIN = int(sys.argv[1])  # 몇분 봉인가?
INTERVAL = f"{MIN}m"    # 차트 종류
TELEGRAM_TOKEN = "tElEgRaMtOkEn"  # 텔레그렘 봇 토큰
TELEGRAM_CHAT_ID = 123456789      # 텔레그램 봇 아이디
#############################################

##### 변수 ##################################
bot = telegram.Bot(TELEGRAM_TOKEN)
tickers = ["BTC/USDT", "ETH/USDT", "XRP/USDT"]
#############################################

while(True):
    try: 
        now = datetime.now()
        mod = divmod(now.minute, MIN)[1]

        # 봉 갱신 직후 골든(데드)크로스 전환 여부 확인(5, 15, 30, 60분봉 사용)
        if(mod == 0):
            for ticker in tickers: 
                is_cross_1 = False # 2일 전 이평선 골든(데드)크로스 여부 체크
                is_cross_2 = False # 1일 전 이평선 골든(데드)크로스 여부 체크

                # 2일 전 골든(데드)크로스 여부 판별
                ma5_2 = get_prev_ma(ticker, INTERVAL, 5, 2)
                ma10_2 = get_prev_ma(ticker, INTERVAL, 10, 2)
                ma15_2 = get_prev_ma(ticker, INTERVAL, 15, 2)
                ma25_2 = get_prev_ma(ticker, INTERVAL, 25, 2)
                if(ma5_2 > ma10_2 > ma15_2 > ma25_2 or ma5_2 < ma10_2 < ma15_2 < ma25_2):
                    is_cross_2 = True

                # 1일 전 골든(데드)크로스 여부 판별
                ma5_1 = get_prev_ma(ticker, INTERVAL, 5, 1)
                ma10_1 = get_prev_ma(ticker, INTERVAL, 10, 1)
                ma15_1 = get_prev_ma(ticker, INTERVAL, 15, 1)
                ma25_1 = get_prev_ma(ticker, INTERVAL, 25, 1)
                if(ma5_1 > ma10_1 > ma15_1 > ma25_1 or ma5_1 < ma10_1 < ma15_1 < ma25_1):
                    is_cross_1 = True

                # 2일 전 -> 1일 전 골든(데드)크로스 전환되면 텔레그램 메시지 전송
                if(is_cross_2 == False and is_cross_1 == True):
                    if(ma5_1 > ma25_1):
                        message = f"Binance {ticker} {MIN}분봉 골든크로스 전환"
                        bot.sendMessage(TELEGRAM_CHAT_ID, text=message)
                    if(ma5_1 < ma25_1):
                        message = f"Binance {ticker} {MIN}분봉 데드크로스 전환"
                        bot.sendMessage(TELEGRAM_CHAT_ID, text=message)
            
            time.sleep(60)
        
        else:
            time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)