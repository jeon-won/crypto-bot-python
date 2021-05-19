import pyupbit
import time

"""
cryptofunc.py
* Date: 2021.05.20.
* Author: Jeon Won
* Func: 업비트 가상화폐 관련 정보를 얻어오기 위한 모듈
* Notice: 산식을 맞게 적은건지 모르게씀. 업비트에서 보는 값과 조금 오차가 있을 수 있음...
"""

SLEEP_TIME = 0.1 # 업비트 API 호출 제한시간이 있어서 잠깐 쉬는 시간(초)

def get_coin_tickers():
    """업비트에서 한화로 거래 가능한 코인 조회"""
    tickers = []
    for ticker in pyupbit.get_tickers():
        if(ticker[0:3] == "KRW"):
            tickers.append(ticker)
            time.sleep(SLEEP_TIME)
    return tickers

def get_current_price(ticker):
    """현재가 조회"""
    current_price = pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]
    time.sleep(SLEEP_TIME)
    return current_price

def get_ma(ticker, interval, count):
    """이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval, count)
    ma = df['close'].rolling(count).mean().iloc[-1]
    time.sleep(SLEEP_TIME)
    return ma

def get_prev_ma(ticker, interval, count):
    """직전 이동 평균선 조회 (count: 일 수)"""
    df = pyupbit.get_ohlcv(ticker, interval=interval, count=count+1)
    prev_df = df.drop(df.index[len(df)-1])
    prev_ma = prev_df['close'].rolling(count).mean().iloc[-1]
    time.sleep(SLEEP_TIME)
    return prev_ma

def get_ema(ticker, interval, count):
    """지수 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval, count)
    ma = df['close'].ewm(span=count).mean().iloc[-1]
    time.sleep(SLEEP_TIME)
    return ma

def get_prev_ema(ticker, interval, count):
    """직전 지수 이동 평균선 조회 (count: 일 수)"""
    df = pyupbit.get_ohlcv(ticker, interval=interval, count=count+1)
    prev_df = df.drop(df.index[len(df)-1])
    prev_ma = prev_df['close'].ewm(span=count).mean().iloc[-1]
    time.sleep(SLEEP_TIME)
    return prev_ma

def get_stoch_k(ticker, interval, count):
    """스토캐스틱(Stochastic) 지표에서 사용되는 %K 값 구하기"""
    df = pyupbit.get_ohlcv(ticker, interval, count)
    time.sleep(SLEEP_TIME)

    prices = []
    prices.append(df.min()['open'])
    prices.append(df.min()['high'])
    prices.append(df.min()['low'])
    prices.append(df.min()['close'])
    prices.append(df.max()['open'])
    prices.append(df.max()['high'])
    prices.append(df.max()['low'])
    prices.append(df.max()['close'])

    wave_min = min(prices)                    # 파동의 최저가격
    wave_max = max(prices) - min(prices)      # 파동의 전체 폭
    current_price = get_current_price(ticker) # 현재 가격
    time.sleep(SLEEP_TIME)
    
    stoch_k = (current_price - wave_min) / wave_max
    return stoch_k

def get_bb(ticker, interval, count, multiplier):
    """볼린저 밴드에 사용되는 값(중심선, 상한선, 하한선)이 담긴 딕셔너리 반환"""
    df = pyupbit.get_ohlcv(ticker, interval, count)
    time.sleep(SLEEP_TIME)
    
    std = df.std()['close']               # 종가 기준 표준편차
    mbb = get_ma(ticker, interval, count) # 중심선 = 기간 내 이동평균선(저항자리)
    ubb = mbb + std * multiplier          # 상한선 = 중심선 + 기간 내 표준편차 * 승수
    lbb = mbb - std * multiplier          # 하한선 = 중신선 + 기간 내 표준편차 * 승수
    time.sleep(SLEEP_TIME)
    
    dict_bb = {}
    dict_bb["mbb"] = mbb
    dict_bb["ubb"] = ubb
    dict_bb["lbb"] = lbb
    return dict_bb