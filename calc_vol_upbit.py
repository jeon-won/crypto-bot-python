import numpy as np
import ccxt
import module_upbit
"""
calc_vol_upbit.py
* Date: 2021. 10. 9.
* Author: Jeon Won
* Func: 업비트 거래량이 평소보다 높아졌다고 판단하기 위한 기준 계산 (판단기준: 평균거래량 + 승수*표준편차)
* Usage: `python detect_vol_binance.py`
"""

N = 1  # 승수
upbit = ccxt.upbit()
# tickers = ["KRW-BTC"]
tickers = module_upbit.get_vol_top_tickers(10)
timeframes = ["1m", "3m", "5m", "15m", "30m", "1h", "4h", "1d"]


for ticker in tickers:
    print(f"# {ticker}")

    for tf in timeframes:
        ohlcvs = upbit.fetch_ohlcv(ticker, tf)

        # numpy 배열에 거래량 데이터만 담기
        ohlcvs_np = np.array([])
        for ohlcv in ohlcvs:
            ohlcvs_np = np.append(ohlcvs_np, ohlcv[5])
        
        mean = ohlcvs_np.mean()  # 평균
        std = ohlcvs_np.std()    # 표준편차
        n_std = mean + N * std   # 거래량 급등 판단 기준(평균거래량 + 승수 * 표준편차)
        current_vol = ohlcvs[len(ohlcvs) - 1][5]  # 현재 거래량
        is_increased = "평소보다 증가" if current_vol >= n_std else "보통"

        print(f" - [{tf}] 거래량 평균: {round(mean)} / 거래량 증가 판단 기준: {round(n_std)} / 현재 거래량: {round(current_vol)} / {is_increased}")