import sys
import pyupbit
"""
calc_vol_upbit.py
* Date: 2021. 10. 9.
* Author: Jeon Won
* Func: 업비트 거래량이 평소보다 높아졌다고 판단하기 위한 기준 계산 (판단기준: 평균거래량 + 승수*표준편차)
* Usage: 비트코인에 승수를 2로 하는 조사 명령어는 `python calc_vol_upbit.py KRW-BTC 2`
"""


TICKER = sys.argv[1]    # ticker
N = float(sys.argv[2])  # 승수

timeframes = ["minute1", "minute3", "minute5", "minute15", "minute30", "minute60", "minute240", "day"]

print(f"# {TICKER}")

for tf in timeframes:
    # ticker
    ohlcvs = pyupbit.get_ohlcv(TICKER, interval=tf)

    mean = ohlcvs["volume"].mean() # 평균
    std = ohlcvs["volume"].std()   # 표준편차
    n_std = mean + N * std         # 현재 거래량이 이 값보다 높으면 거래량이 급증한 것으로 판단
    current_vol = ohlcvs["volume"][len(ohlcvs)-1] # 현재 거래량
    is_increased = "평소보다 증가" if current_vol >= n_std else "보통"

    print(f" - [{tf}] 거래량 평균: {round(mean)} / 거래량 증가 판단 기준: {round(n_std)} / 현재 거래량: {round(current_vol)} / {is_increased}")