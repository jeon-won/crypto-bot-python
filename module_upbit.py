import pyupbit
import ccxt
import requests
import numpy as np

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
    """현재 이동 평균을 조회합니다.

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
    """과거 이동 평균을 조회합니다.

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



def get_bb(ticker, interval, count, multiplier):
    """볼린저 밴드에 사용되는 값(중심선, 상한선, 하한선)을 계산합니다.

    Args: 
        ticker: ticker (예: "KRW-BTC") 
        interval: 몇분 봉? (예: "minute5", "minute15" 등)
        count: 이동평균선 기간  (예: 20)
        multipler: 승수 (예: 2)
    
    Returns: dict
    """
    df = pyupbit.get_ohlcv(ticker, interval, count)
    
    current = df['close'][count-1]
    std = df['close'].std()                # 종가 기준 표준편차
    mbb = df['close'].mean()               # 볼린저 밴드 중심선(이동평균)
    ubb = mbb + std * multiplier           # 상한선 = 중심선 + 기간 내 표준편차 * 승수
    lbb = mbb - std * multiplier           # 하한선 = 중신선 + 기간 내 표준편차 * 승수
    per_b = (current - lbb) / (ubb - lbb)  # %b = (가격 - 볼린저밴드_하단선) / (볼린저밴드 상단선 - 볼린저 밴드 하단선)
    
    dict_bb = {}
    dict_bb["ticker"] = ticker
    dict_bb["mbb"] = mbb
    dict_bb["ubb"] = ubb
    dict_bb["lbb"] = lbb
    dict_bb["current"] = current
    dict_bb["per_b"] = per_b
    
    return dict_bb


def get_vol_top_tickers(top_num=0):
    """업비트의 최근 24시간 기준 거래량 높은 코인들을 얻어옵니다.

    Args: top_num (거래량 상위 몇 개의 코인들을 얻어올 것인가?)

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
    if(top_num == 0): # 매개변수 값이 0이면 모든 tickers List 반환
        return sorted_tickers
    elif(top_num > 0): # 매개변수 값이 0 초과 시 상위 ticker List 반환
        return sorted_tickers[:top_num]
    else: # 매개변수 값이 적절치 않으면 None 반환
        return


##### 아래 함수들은 제대로 작동하지 않음

# def get_ema(ticker, interval, count):
#     """지수 이동 평균을 조회합니다.

#     Args: 
#         ticker: ticker (예: "KRW-BTC")
#         interval: 몇분 봉? (예: "minute5", "minute15" 등)
#         count: 이동평균선 기간  (예: 5, 20, 60, 120 등)
    
#     Returns: numpy.float64
#     """
#     df = pyupbit.get_ohlcv(ticker, interval, count)
#     ma = df['close'].ewm(span=count).mean().iloc[-1]
#     return ma

# def get_prev_ema(ticker, interval, count):
#     """직전 지수 이동 평균을 조회합니다.

#     Args: 
#         ticker: ticker (예: "KRW-BTC")
#         interval: 몇분 봉? (예: "minute5", "minute15" 등)
#         count: 이동평균선 기간  (예: 5, 20, 60, 120 등)
    
#     Returns: numpy.float64
#     """
#     df = pyupbit.get_ohlcv(ticker, interval=interval, count=count+1)
#     prev_df = df.drop(df.index[len(df)-1])
#     prev_ma = prev_df['close'].ewm(span=count).mean().iloc[-1]
#     return prev_ma

# def get_stoch_k(ticker, interval, count):
#     """스토캐스틱(Stochastic)에서 사용되는 %K 값을 계산합니다.

#     Args: 
#         ticker: ticker (예: "KRW-BTC")
#         interval: 몇분 봉? (예: "minute5", "minute15" 등)
#         count: 이동평균선 기간  (예: 5, 20, 60, 120 등)
    
#     Returns: numpy.float64
#     """
#     df = pyupbit.get_ohlcv(ticker, interval, count)

#     prices = []
#     prices.append(df.min()['open'])
#     prices.append(df.min()['high'])
#     prices.append(df.min()['low'])
#     prices.append(df.min()['close'])
#     prices.append(df.max()['open'])
#     prices.append(df.max()['high'])
#     prices.append(df.max()['low'])
#     prices.append(df.max()['close'])

#     wave_min = min(prices)                     # 파동의 최저가격
#     wave_max = max(prices) - min(prices)       # 파동의 전체 폭
#     current_price = get_current_price(ticker)  # 현재 가격
    
#     stoch_k = (current_price - wave_min) / wave_max
#     return stoch_k

# def get_fall_rate(ticker, interval, count):
#     """최근 차트 감소율 계산"""
#     df = pyupbit.get_ohlcv(ticker, interval, count)
#
#     df_open = df["open"].to_list()
#     df_close = df["close"].to_list()
#     wave_max = max(df_open[count-1], df_close[count-1])
#     wave_min = min(df_open[count-1], df_close[count-1])

#     for i in reversed(range(count-1)):                                       # 최근 캔들 -> 과거 캔들 순으로 조사해서
#         if(df_open[i] >= df_close[i]):                                       # 하락 캔들을 발견하면
#             wave_max = df_open[i] if df_open[i] >= wave_max else wave_max    # 최대, 최소값 찾기
#             wave_min = df_close[i] if df_close[i] <= wave_min else wave_min
#         else:                                                                # 상승 캔들 발견 시
#             break                                                            # 더 이상 조사하지 않음
    
#     return 1 - (wave_min / wave_max)                                         # 감소율 반환