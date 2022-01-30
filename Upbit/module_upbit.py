import pyupbit
import ccxt
import requests
import numpy as np
import pandas

def get_krw_tickers():
    """업비트에서 한화로 거래 가능한 코인을 조회합니다.

    Args: 없음

    Returns: list (예: ["KRW-BTC","KRW-ETC","KRW-XRP", ... ])
    """
    tickers = []
    for ticker in pyupbit.get_tickers():
        if(ticker[0:3] == "KRW"):
            tickers.append(ticker)
    return tickers


def get_current_price(ticker):
    """ticker의 현재가를 조회합니다.

    Args: ticker (예: "KRW-BTC")

    Returns: float
    """
    current_price = pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]
    return current_price


def get_ma(ticker, interval, count):
    """ticker의 현재 이동 평균을 조회합니다.

    Args: 
        ticker: ticker (예: "BTC/USDT")
        interval: 몇분 봉? (예: "5m", "15m" 등)
        count: 이동평균선 기간  (예: 5, 20, 60, 120 등)
    
    Returns: numpy.float64
    """
    binance = ccxt.upbit()
    ohlcvs = binance.fetch_ohlcv(ticker, interval, limit=count)
    ohlcvs_np = np.array([])

    for ohlcv in ohlcvs:
        ohlcvs_np = np.append(ohlcvs_np, ohlcv[4])
    
    return ohlcvs_np.mean()


def get_prev_ma(ticker, interval, count, before):
    """ticker의 과거 이동 평균을 조회합니다.

    Args: 
        ticker: ticker (예: "BTC/USDT")
        interval: 몇분 봉? (예: "5m", "15m" 등)
        count: 이동평균선 기간  (예: 5, 20, 60, 120 등)
        before: 며칠 전 이동평균을 구할 것인지? (예: 1, 2, ... )
    
    Returns: numpy.float64
    """

    binance = ccxt.upbit()
    ohlcvs = binance.fetch_ohlcv(ticker, interval, limit=count+before)
    _ohlcvs = ohlcvs[:len(ohlcvs)-before]
    ohlcvs_np = np.array([])

    for ohlcv in _ohlcvs:
        ohlcvs_np = np.append(ohlcvs_np, ohlcv[4])
    
    return ohlcvs_np.mean()


def get_bb(ticker, interval, count: int=20, multiplier: int=2):
    """ticker의 볼린저 밴드에 사용되는 값(중심선, 상한선, 하한선)을 계산합니다.

    Args: 
        ticker: ticker (예: "KRW-BTC") 
        interval: 몇분 봉? (예: "minute5", "minute15" 등)
        count: 이동평균선 기간  (기본값: 20)
        multipler: 승수 (기본값: 2)
    
    Returns: dict
    """
    df = pyupbit.get_ohlcv(ticker, interval, count)
    
    current_price = df['close'][count-1]
    std = df['close'].std()                # 종가 기준 표준편차
    mbb = df['close'].mean()               # 볼린저 밴드 중심선(이동평균)
    ubb = mbb + std * multiplier           # 상한선 = 중심선 + 기간 내 표준편차 * 승수
    lbb = mbb - std * multiplier           # 하한선 = 중신선 + 기간 내 표준편차 * 승수
    per_b = (current_price - lbb) / (ubb - lbb)  # %b = (가격 - 볼린저밴드_하단선) / (볼린저밴드 상단선 - 볼린저 밴드 하단선)
    
    dict_bb = {}
    dict_bb["ticker"] = ticker
    dict_bb["mbb"] = mbb
    dict_bb["ubb"] = ubb
    dict_bb["lbb"] = lbb
    dict_bb["current_price"] = current_price
    dict_bb["per_b"] = per_b
    
    return dict_bb


def get_pyupbit_bb(ticker, df, multiplier: int=2):
    """pandas.DataFrame 객체를 받아 볼린저 밴드에 사용되는 값(중심선, 상한선, 하한선)을 계산합니다. pandas.DataFrame 객체는 pyupbit의 get_ohlcv() 함수가 반환하는 값입니다.

    Args: 
        ticker: ticker (예: "KRW-BTC") 
        df: pandas.DataFrame (pyupbit get_ohlcv() 함수의 반환값)
        multipler: 승수 (기본값: 2)
    
    Returns: dict
    """
    current_price = df.iloc[len(df)-1]["close"]  # 현재 가격
    std = df["close"].std()                      # 종가 기준 표준편차
    mbb = df["close"].mean()                     # 볼린저 밴드 중심선(이동평균)
    ubb = mbb + std * multiplier                 # 상한선 = 중심선 + 기간 내 표준편차 * 승수
    lbb = mbb - std * multiplier                 # 하한선 = 중신선 + 기간 내 표준편차 * 승수
    per_b = (current_price - lbb) / (ubb - lbb)  # %b = (가격 - 볼린저밴드_하단선) / (볼린저밴드 상단선 - 볼린저 밴드 하단선)
    
    dict_bb = {}
    dict_bb["ticker"] = ticker
    dict_bb["mbb"] = mbb
    dict_bb["ubb"] = ubb
    dict_bb["lbb"] = lbb
    dict_bb["current_price"] = current_price
    dict_bb["per_b"] = per_b
    
    return dict_bb


def get_prev_bb(ticker, interval, count, multiplier):
    """ticker의 직전 봉에 대한 볼린저 밴드에 사용되는 값(중심선, 상한선, 하한선)을 계산합니다.

    Args: 
        ticker: ticker (예: "KRW-BTC") 
        interval: 몇분 봉? (예: "minute5", "minute15" 등)
        count: 이동평균선 기간  (예: 20)
        multipler: 승수 (예: 2)
    
    Returns: dict
    """
    df = pyupbit.get_ohlcv(ticker, interval, count+1)[0:count]
    
    current_price = df['close'][count-1]
    std = df['close'].std()                # 종가 기준 표준편차
    mbb = df['close'].mean()               # 볼린저 밴드 중심선(이동평균)
    ubb = mbb + std * multiplier           # 상한선 = 중심선 + 기간 내 표준편차 * 승수
    lbb = mbb - std * multiplier           # 하한선 = 중신선 + 기간 내 표준편차 * 승수
    per_b = (current_price - lbb) / (ubb - lbb)  # %b = (가격 - 볼린저밴드_하단선) / (볼린저밴드 상단선 - 볼린저 밴드 하단선)
    
    dict_bb = {}
    dict_bb["ticker"] = ticker
    dict_bb["mbb"] = mbb
    dict_bb["ubb"] = ubb
    dict_bb["lbb"] = lbb
    dict_bb["current_price"] = current_price
    dict_bb["per_b"] = per_b
    
    return dict_bb


def get_rsi(ticker, interval, period: int=14):
    """ticker의 RSI 값을 계산합니다. (소스코드 출처: https://rebro.kr/139)

    Args: 
        ticker: ticker (예: "KRW-BTC") 
        interval: 몇분 봉? (예: "minute5", "minute15" 등)
        period: 기간(기본값: 14)
    
    Returns: numpy.float64
    """
    ohlcv = pyupbit.get_ohlcv(ticker, interval)
    delta = ohlcv["close"].diff()
    ups, downs = delta.copy(), delta.copy() 
    ups[ups < 0] = 0 
    downs[downs > 0] = 0 
    
    AU = ups.ewm(com = period-1, min_periods = period).mean() 
    AD = downs.abs().ewm(com = period-1, min_periods = period).mean() 
    RS = AU/AD 
    
    return pandas.Series(100 - (100/(1 + RS)), name = "RSI").iloc[-1]


def get_pyupbit_rsi(df: pandas.DataFrame, period: int = 14): 
    """panda.DataFrame 객체를 받아 RSI 값을 게산합니다. pandas.DataFrame 객체는 pyupbit의 get_ohlcv() 함수가 반환하는 값입니다. (소스코드 출처: https://rebro.kr/139)
    Args: 
        ohlc: pandas.DataFrame (pyupbit.get_ohlcv() 함수의 반환값)
        period: 기간(기본값: 14)

    Returns: numpy.float64
    """
    delta = df["close"].diff() 
    ups, downs = delta.copy(), delta.copy() 
    ups[ups < 0] = 0 
    downs[downs > 0] = 0 
    
    AU = ups.ewm(com = period-1, min_periods = period).mean() 
    AD = downs.abs().ewm(com = period-1, min_periods = period).mean() 
    RS = AU/AD 
    
    return pandas.Series(100 - (100/(1 + RS)), name = "RSI").iloc[-1]


def get_vol_top_tickers(top_num=0, remove_tickers=[]):
    """업비트의 최근 24시간 기준 거래량 높은 코인들을 얻어옵니다.

    Args: 
        top_num (거래량 상위 몇 개의 코인들을 얻어올 것인가?)
        remove_tickers (제외할 ticker list)

    Returns: list (잘못된 매개변수를 입력한 경우 None)
    """

    # 업비트에서 KRW로 거래 가능한 tickers 얻어오기
    tickers = ""
    for item in get_krw_tickers():
        tickers += f"{item},"
    tickers = tickers[:-1] # 마지막 문자열(쉼표) 자르기

    # tickers의 데이터를 얻어온 후 최근 24시간 내 거래량이 높은 순으로 정렬
    url = "https://api.upbit.com/v1/ticker"
    headers = {"Accept": "application/json"}
    query = { 'markets': tickers }
    response = requests.request("GET", url, headers=headers, params=query)
    sorted_data = sorted(response.json(), key=(lambda x: x['acc_trade_price_24h']), reverse=True)

    # tickers의 데이터 중 거래량 상위 tickers의 list 반환
    sorted_tickers = []
    for item in sorted_data:
        sorted_tickers.append(item['market'])
    
    # 원치않는 ticker 제거
    for item in remove_tickers:
        if item in sorted_tickers:
            sorted_tickers.remove(item)

    if(top_num == 0): # 매개변수 값이 0이면 모든 tickers List 반환
        return sorted_tickers
    elif(top_num > 0): # 매개변수 값이 0 초과 시 상위 ticker List 반환
        return sorted_tickers[:top_num]
    else: # 매개변수 값이 적절치 않으면 None 반환
        return