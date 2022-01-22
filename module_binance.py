import ccxt
import numpy as np

def get_ma(ticker, interval, count):
    """현재 이동 평균을 조회합니다.

    Args: 
        ticker: ticker (예: "BTC/USDT")
        interval: 몇분 봉? (예: "5m", "15m" 등)
        count: 이동평균선 기간  (예: 5, 20, 60, 120 등)
    
    Returns: numpy.float64
    """
    binance = ccxt.binance()
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

    binance = ccxt.binance()
    ohlcvs = binance.fetch_ohlcv(ticker, interval, limit=count+before)
    _ohlcvs = ohlcvs[:len(ohlcvs)-before]
    ohlcvs_np = np.array([])

    for ohlcv in _ohlcvs:
        ohlcvs_np = np.append(ohlcvs_np, ohlcv[4])
    
    return ohlcvs_np.mean()


def get_bb(ticker, interval, count, multipler):
    """볼린저 밴드에 사용되는 값(중심선, 상한선, 하한선)을 계산합니다.

    Args: 
        ticker: ticker (예: "BTC/USDT") 
        interval: 몇분 봉? (예: "minute5", "minute15" 등)
        count: 이동평균선 기간  (예: 20)
        multipler: 승수 (예: 2)
    
    Returns: dict
    """
    list_close = [] # 종가 정보를 담을 list

    binance = ccxt.binance()
    ohlcvs = binance.fetch_ohlcv(ticker, interval)
    ohlcvs_len = len(ohlcvs)
    ohlcvs_edited = ohlcvs[ohlcvs_len-count:ohlcvs_len-1]

    for ohlcv in ohlcvs_edited: # BB에 사용할 정보
        list_close.append(ohlcv[4])
    fetch_ticker = binance.fetch_ticker(ticker)
    current = fetch_ticker['close'] # 현재가
    list_close.append(current)

    std = np.std(list_close)      # 표준편차(종가 기준)
    mbb = np.average(list_close)  # 볼린저 밴드의 중심선(이동평균)
    ubb = mbb + std * multipler   # 상한선 = 중심선 + 기간 내 표준편차 * 승수
    lbb = mbb - std * multipler   # 하한선 = 중신선 + 기간 내 표준편차 * 승수
    per_b = (current - lbb) / (ubb - lbb) # %b = (가격 - 볼린저밴드 하단선) / (볼린저밴드 상단선 - 볼린저 밴드 하단선)

    dict_bb = {}
    dict_bb["ticker"] = ticker
    dict_bb["ubb"] = ubb
    dict_bb["mbb"] = mbb
    dict_bb["lbb"] = lbb
    dict_bb["current"] = current
    dict_bb["per_b"] = per_b
    
    return dict_bb