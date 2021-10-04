import pyupbit
import time
import requests

SLEEP_TIME = 0 # 업비트 API 호출 제한시간이 있어서 잠깐 쉬는 시간(초)
URL = "https://api.upbit.com/v1/ticker"
HEADERS = {"Accept": "application/json"}


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
    time.sleep(SLEEP_TIME)
    return current_price

def get_ma(ticker, interval, count):
    """이동 평균을 조회합니다.

    Args: 
        ticker: ticker (예: "KRW-BTC")
        interval: 몇분 봉? (예: "minute5", "minute15" 등)
        count: 이동평균선 기간  (예: 5, 20, 60, 120 등)
    
    Returns: numpy.float64
    """
    df = pyupbit.get_ohlcv(ticker, interval, count)
    ma = df['close'].rolling(count).mean().iloc[-1]
    time.sleep(SLEEP_TIME)
    return ma

def get_prev_ma(ticker, interval, count):
    """직전 이동 평균을 조회합니다.

    Args: 
        ticker: ticker (예: "KRW-BTC")
        interval: 몇분 봉? (예: "minute5", "minute15" 등)
        count: 이동평균선 기간  (예: 5, 20, 60, 120 등)
    
    Returns: numpy.float64
    """
    df = pyupbit.get_ohlcv(ticker, interval=interval, count=count+1)
    prev_df = df.drop(df.index[len(df)-1])
    prev_ma = prev_df['close'].rolling(count).mean().iloc[-1]
    time.sleep(SLEEP_TIME)
    return prev_ma

def get_ema(ticker, interval, count):
    """지수 이동 평균을 조회합니다.

    Args: 
        ticker: ticker (예: "KRW-BTC")
        interval: 몇분 봉? (예: "minute5", "minute15" 등)
        count: 이동평균선 기간  (예: 5, 20, 60, 120 등)
    
    Returns: numpy.float64
    """
    df = pyupbit.get_ohlcv(ticker, interval, count)
    ma = df['close'].ewm(span=count).mean().iloc[-1]
    time.sleep(SLEEP_TIME)
    return ma

def get_prev_ema(ticker, interval, count):
    """직전 지수 이동 평균을 조회합니다.

    Args: 
        ticker: ticker (예: "KRW-BTC")
        interval: 몇분 봉? (예: "minute5", "minute15" 등)
        count: 이동평균선 기간  (예: 5, 20, 60, 120 등)
    
    Returns: numpy.float64
    """
    df = pyupbit.get_ohlcv(ticker, interval=interval, count=count+1)
    prev_df = df.drop(df.index[len(df)-1])
    prev_ma = prev_df['close'].ewm(span=count).mean().iloc[-1]
    time.sleep(SLEEP_TIME)
    return prev_ma

def get_stoch_k(ticker, interval, count):
    """스토캐스틱(Stochastic)에서 사용되는 %K 값을 계산합니다.

    Args: 
        ticker: ticker (예: "KRW-BTC")
        interval: 몇분 봉? (예: "minute5", "minute15" 등)
        count: 이동평균선 기간  (예: 5, 20, 60, 120 등)
    
    Returns: numpy.float64
    """
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

    wave_min = min(prices)                     # 파동의 최저가격
    wave_max = max(prices) - min(prices)       # 파동의 전체 폭
    current_price = get_current_price(ticker)  # 현재 가격
    time.sleep(SLEEP_TIME)
    
    stoch_k = (current_price - wave_min) / wave_max
    return stoch_k

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
    time.sleep(SLEEP_TIME)
    
    std = df.std()['close']                # 종가 기준 표준편차
    mbb = get_ma(ticker, interval, count)  # 중심선 = 기간 내 이동평균선(저항자리)
    ubb = mbb + std * multiplier           # 상한선 = 중심선 + 기간 내 표준편차 * 승수
    lbb = mbb - std * multiplier           # 하한선 = 중신선 + 기간 내 표준편차 * 승수
    time.sleep(SLEEP_TIME)
    
    dict_bb = {}
    dict_bb["mbb"] = mbb
    dict_bb["ubb"] = ubb
    dict_bb["lbb"] = lbb
    return dict_bb

# def get_fall_rate(ticker, interval, count):
#     """최근 차트 감소율 계산"""
#     df = pyupbit.get_ohlcv(ticker, interval, count)
#     time.sleep(SLEEP_TIME)
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

def get_vol_top_tickers(top_num=0):
    """업비트의 최근 24시간 기준 거래량 높은 코인들을 얻어옵니다.

    Args: top_num (거래량 상위 몇 개의 코인들을 얻어올 것인가?)

    Returns: list (잘못된 매개변수를 입력한 경우 None)
    """

    tickers = ""
    for item in get_krw_tickers():
        tickers += f"{item},"
    tickers = tickers[:-1] # 마지막 문자열(쉼표) 자르기

    query = { 'markets': tickers }
    response = requests.request("GET", URL, headers=HEADERS, params=query)
    sorted_data = sorted(response.json(), key=(lambda x: x['acc_trade_price_24h']), reverse=True)

    sorted_tickers = []
    for item in sorted_data:
        sorted_tickers.append(item['market'])

    if(top_num == 0):
        return sorted_tickers
    elif(top_num > 0):
        return sorted_tickers[:top_num]
    else:
        return