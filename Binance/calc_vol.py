import sys
import numpy as np
import ccxt
"""
Binance/calc_vol.py
* Date: 2021. 10. 9.
* Author: Jeon Won
* Func: 바이낸스 거래량이 평소보다 높아졌다고 판단하기 위한 기준 계산 (판단기준: 평균거래량 + 승수 * 표준편차)
* Usage: 비트코인에 승수를 2로 하는 조사 명령어는 `python Binance/calc_vol.py BTC/USDT 2`
"""

TICKER = sys.argv[1]    # ticker
N = float(sys.argv[2])  # 승수
COUNT = 120             # 거래량 평균

timeframes = ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d"]
binance = ccxt.binance()

print(f"# {TICKER}")

for tf in timeframes:
    ohlcvs = binance.fetch_ohlcv(TICKER, tf, limit=COUNT)

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