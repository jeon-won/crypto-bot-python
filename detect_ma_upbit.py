from module_upbit import get_prev_ma, get_vol_top_tickers
import telegram
import sys

"""
detect_ma_upbit.py
* Date: 2021. 10. 29.
* Author: Jeon Won
* Func: 5, 10, 15, 25 이동평균선이 골든크로스로 변하는 순간 텔레그램 메시지 전송
* Usage: 15분봉 차트 조사 명령어는 `python3 detect_ma_upbit.py minute15` (minute1~240, day 등 사용)
* Strategy: https://youtu.be/og4BhKT6-4U
  - 골든(데드)크로스로 변하는 순간 매수 포지션 각 잡기
  - 포지션 잡은 후 이평선 간격이 좀 벌어지면 10, 15일 이평선 가격으로 물을 타거나 25일 이평선 가격으로 손절 치기
  - 익절은 알아서...
"""

##### 상수 ###################################
INTERVAL = sys.argv[1]    # 차트 종류
TELEGRAM_TOKEN = "tElEgRaMtOkEn"  # 텔레그렘 봇 토큰
TELEGRAM_CHAT_ID = 123456789      # 텔레그램 봇 아이디
#############################################

##### 변수 ##################################
bot = telegram.Bot(TELEGRAM_TOKEN)
#############################################

tickers = get_vol_top_tickers(10)

for ticker in tickers: 
    print(f"{ticker} 조사 중...")
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
            message = f"Upbit {ticker} {INTERVAL}분봉 골든크로스 전환"
            bot.sendMessage(TELEGRAM_CHAT_ID, text=message)