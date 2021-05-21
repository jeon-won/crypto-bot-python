import cryptofunc
import pyupbit
import telegram
import time

"""
AutoDetectFall.py
* Date: 2021.05.20.
* Author: Jeon Won
* Func: 가상화폐 급락했을 때(현재가가 볼린저밴드 하한선 밑에 있고 스토캐스틱 %K 값이 낮을 때 급락으로 판단) 텔레그램 알림 메시지 발송
* Notice: 산식이 맞는건지 모르게씀. 업비트에서 보는 값과 조금 오차가 있는 듯...
"""

##### 상수 ##################################################################################
UPBIT_ACCESS = "uPbItAcCeSsToKeN"                                  # 업비트 Access Key
UPBIT_SECRET = "uPbItSeCrEtToKeN"                                  # 업비트 Secret Key
INTERVAL = "minute5"                                               # 업비트 차트 종류

TELEGRAM_TOKEN = "1234567890:tElEgRaMbOtToKeN"                     # 텔레그렘 봇 토큰
TELEGRAM_CHAT_ID = 123456789                                       # 텔레그램 봇 아이디

BB_COUNT = 20                                                      # 볼린저 밴드(BB)의 길이(일수?)
BB_MULTIPLIER = 2                                                  # 볼린저 밴드(BB)에서 상하한선을 정하기 위해 사용하는 곱(승수)

STOCH_COUNT = 20                                                   # 스토캐스틱(Stochastic)의 길이(일수?)
STOCH_UPPER_LIMIT = 0.8                                            # 스토캐스틱(Stochastic) 상한선(Upper Limit)
STOCH_LOWER_LIMIT = 0.1                                            # 스토캐스틱(stochastic) 하한선(Lower Limit): 현재가가 이 밑으로 떨어지면 급락으로 간주
############################################################################################

##### 변수 ##################################################################################
upbit = pyupbit.Upbit(UPBIT_ACCESS, UPBIT_SECRET)
bot = telegram.Bot(TELEGRAM_TOKEN)
tickers = ["KRW-BTC", "KRW-ETH", "KRW-ETC", "KRW-XRP", "KRW-XLM", "KRW-DOGE", "KRW-EOS", "KRW-ADA", "KRW-BCH", "KRW-LTC", "KRW-QTUM", "KRW-NEO", "KRW-BTG"]
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
                # balance = upbit.get_balance(ticker)
                # time.sleep(0.1)
                # order = upbit.get_order(ticker)
                # time.sleep(0.1)
                # if(not balance and not order):
                message = f"{ticker} {current_price}원으로 급락"
                bot.sendMessage(TELEGRAM_CHAT_ID, text=message)

            # 3% 이상 하락했을 때도 알림
            fall_rate = cryptofunc.get_fall_rate(ticker, INTERVAL, 12)
            if(fall_rate >= 0.03):
                message = f"{ticker} {round(fall_rate, 3) * 100}% 하락"
                bot.sendMessage(TELEGRAM_CHAT_ID, text=message)

    except Exception as e:
        print(e)
        time.sleep(1)
