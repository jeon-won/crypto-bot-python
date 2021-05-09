import time
import pyupbit
import datetime
import logging
from logging import handlers

#############  상수  ##########################################################################
ACCESS = "mYuPbItAcCeSsKeY"            # 업비트 Access Key
SECRET = "mYuPbItSeCrEtKeY"            # 업비트 Secret Key
COIN_TICKER = "KRW-BTC"                # 코인 티커
COIN_NAME = "BTC"                      # 코인 이름
INTERVAL = "minute240"                 # 차트 종류
HOUR_TO_SELL = [0, 4, 8, 12, 18, 20]   # 변동성 돌파 전략 시 코인 매도 시간
NOT_BUY_KRW = 1000000                  # 변동성 돌파 전략을 사용하지 않을 원화
NOT_BUY_COIN = 0.123456                # 변동성 돌파 전략을 사용하지 않을 코인 수
K = 0.5                                # 변동폭 계산에 사용되는 값
################################################################################################


#############  함수  ###########################################################################
def get_target_price(ticker, interval, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval=interval, count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_ma(ticker, interval, count):
    """이동 평균선 조회 (count: 일 수)"""
    df = pyupbit.get_ohlcv(ticker, interval=interval, count=count)
    ma = df['close'].rolling(count).mean().iloc[-1]
    return ma

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]
###############################################################################################


############# 로그 설정  ######################################################################
# log settings
coinLogFormatter = logging.Formatter('%(asctime)s, %(message)s')

# handler settings
coinLogHandler = handlers.TimedRotatingFileHandler(filename=f"{COIN_NAME}.log", when="midnight", interval=1, encoding="utf-8")
coinLogHandler.setFormatter(coinLogFormatter)
coinLogHandler.suffix = "%Y%m%d"

# logger set
coinLogger = logging.getLogger()
coinLogger.setLevel(logging.INFO)
coinLogger.addHandler(coinLogHandler)

# use logger
print(f"{COIN_NAME} Auto trade start!")
coinLogger.info(f"{COIN_NAME} Auto trade start!")
###############################################################################################

upbit = pyupbit.Upbit(ACCESS, SECRET)
ma5 = 0
ma3 = 0

while True:
    try:
        now = datetime.datetime.now() # + datetime.timedelta(hours=1, minutes=12, seconds=30)
        start_time = datetime.datetime(now.year, now.month, now.day, now.hour, minute=59, second=50)
        end_time = datetime.datetime(now.year, now.month, now.day, now.hour, minute=59, second=59)

        # 차트 마감 10초 전에 코인을 현재가로 매도
        if((now.hour in HOUR_TO_SELL) and (start_time <= now <= end_time)):
            ma5 = get_ma(COIN_TICKER, INTERVAL, 5)
            ma3 = get_ma(COIN_TICKER, INTERVAL, 3)
            coin = get_balance(COIN_NAME) - NOT_BUY_COIN
            current_price = get_current_price(COIN_TICKER)
            # 최소 거래가능 코인을 보유해야 거래 가능
            if (coin > (1 / current_price * 5000)):
                coinLogger.info(f"========== {COIN_NAME} 코인 {coin}개를 현재가로 매도합니다. ===========")
                coinLogger.info(upbit.sell_market_order(COIN_TICKER, coin))
                coinLogger.info("========== 코인 매도 완료 ==========")

        # 코인 매수 각 잡기
        else: 
            # 직전 차트의 이평선이 (3일 > 7일)인 경우
            if(ma3 > ma5): 
                # 변동성 돌파 전략 수행
                current_price = get_current_price(COIN_TICKER)
                target_price = get_target_price(COIN_TICKER, INTERVAL, K)
                if(target_price < current_price): 
                    # 최소 5,000원 이상 거래
                    krw = get_balance("KRW") - NOT_BUY_KRW
                    if(krw > 5000):
                        coinLogger.info(f"========== KRW {krw}원에 코인을 매수합니다. ==========")
                        coinLogger.info(upbit.buy_market_order(COIN_TICKER, krw))
                        coinLogger.info("========== 코인 매수 완료 ==========")
        
        time.sleep(5)

    except Exception as e:
        print(e)
        time.sleep(5)