from dotenv import load_dotenv
import os
import pyupbit
import telegram
import sys
import time

"""
stoploss_upbit.py
* Date: 2022. 1. 21.
* Author: Jeon Won
* Func: 업비트 보유 중인 특정 코인의 현재가를 감시하여 스탑로스 설정 가격에 도달하면 수익실현 또는 손절
* Usage: python3 stoploss_upbit.py 수익실현가 손절가
  - 예: 리플 현재가가 1000원 도달 시 수익실현, 800원 도달 시 손절하는 명령어는 `python3 stoploss_upbit.py XRP 1000 800`
  - 백그라운드로 돌리려면 `nohup python3 stoploss_upbit.py XRP 1000 800`
"""

load_dotenv()
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")      # 텔레그램 봇 토큰
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")  # 텔레그램 봇 아이디
UPBIT_ACCESS_KEY = os.environ.get("UPBIT_ACCESS_KEY")  # 업비트 엑세스 키
UPBIT_SECRET_KEY = os.environ.get("UPBIT_SECRET_KEY")  # 업비트 시크릿 키

KRW_TICKER = "KRW-" + sys.argv[1]  # KRW-TICKER(예: KRW-BTC)
TICKER = sys.argv[1]       # TICKER(예: BTC)
STOP = float(sys.argv[2])  # 수익실현 가격
LOSS = float(sys.argv[3])  # 손절 가격

bot = telegram.Bot(TELEGRAM_TOKEN)
upbit = pyupbit.Upbit(UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY)

# 업비트에 보유 중인 모든 암호화폐 잔고 가져오기
balances = upbit.get_balances()
for balance in balances:
    # 보유 중인 특정 코인 발견 시 1초 간격으로 현재가 감시
    if balance['currency'] == TICKER:
        while True: 
            try:
                current_price = pyupbit.get_current_price(KRW_TICKER)
                print(f"{TICKER} 현재가: {current_price} / 수익실현가: {STOP} / 손절가: {LOSS}")
                
                # 현재가가 STOP 돌파 시 수익실현
                if(current_price >= STOP):
                    upbit.sell_market_order(KRW_TICKER, float(balance['balance']))
                    message = f"{KRW_TICKER} {float(balance['balance'])}개를 수익실현합니다."
                    bot.sendMessage(TELEGRAM_CHAT_ID, text=message)
                    print(message)
                    break

                # 현재가가 LOSS 돌파 시 손절
                if(current_price <= LOSS):
                    upbit.sell_market_order(KRW_TICKER, float(balance['balance']))
                    message = f"{KRW_TICKER} {float(balance['balance'])}개를 손절합니다."
                    bot.sendMessage(TELEGRAM_CHAT_ID, text=message)
                    print(message)
                    break
                
                time.sleep(1)
            
            except Exception as e:
                print(e)