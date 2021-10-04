import ccxt
import numpy

def get_bb(ticker, interval, count, multipler):
    """볼린저 밴드에 사용되는 값(중심선, 상한선, 하한선)을 계산합니다.

    Args: 
        ticker: ticker (예: "BTC/USDT") 
        interval: 몇분 봉? (예: "minute5", "minute15" 등)
        count: 이동평균선 기간  (예: 20)
        multipler: 승수 (예: 2)
    
    Returns: dict
    """
    list_close = []

    binance = ccxt.binance()
    ohlcvs = binance.fetch_ohlcv(ticker, interval)
    ohlcvs_len = len(ohlcvs)
    ohlcvs_edited = ohlcvs[ohlcvs_len-count:ohlcvs_len-1]

    for ohlcv in ohlcvs_edited: # BB에 사용할 정보
        list_close.append(ohlcv[4])
    ticker = binance.fetch_ticker(ticker)
    current = ticker['close'] # 현재가
    list_close.append(current)

    std = numpy.std(list_close)      # 표준편차(종가 기준)
    mbb = numpy.average(list_close)  # 볼린저 밴드의 중심선(이동평균)
    ubb = mbb + std * multipler      # 상한선 = 중심선 + 기간 내 표준편차 * 승수
    lbb = mbb - std * multipler      # 하한선 = 중신선 + 기간 내 표준편차 * 승수

    dict_bb = {}
    dict_bb["ubb"] = ubb
    dict_bb["mbb"] = mbb
    dict_bb["lbb"] = lbb
    dict_bb["current"] = current
    
    return dict_bb