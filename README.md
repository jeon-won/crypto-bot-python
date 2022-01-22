# crypto-bot-python

## 개요
가상화폐 포지션을 잡기 위한 타이밍을 파악하기 위해 만든 파이썬 코드입니다. 주요 기능은 거래량이 평소보다 많아지거나, 볼린저 밴드 상하단부를 벗어났을 때 텔레그램 메시지를 전송하는 기능입니다. 거래소는 업비트와 바이낸스를 사용합니다.

**여기 있는 코드는 테스트 중이므로 정상적인 실행을 보장하지 않으며, 이 프로그램을 사용하여 발생하는 손해에 대한 책임은 사용자 본인에게 있습니다.**


## 사용한 주요 라이브러리
* pyupbit: 업비트 API를 편하게 사용하기 위한 라이브러리
* ccxt: 바이낸스 및 업비트 API를 편하게 사용하기 위한 라이브러리
* python-telegram-bot: 텔레그램 메시지 전송을 위한 라이브러리
* numpy: 배열 처리를 쉽게 하기 위한 라이브러리
* python-dotenv: 환경변수(.env)를 사용하기 위한 라이브러리


## 사용법

우선 `.env` 파일을 만듭니다. 이 파일에 텔레그램 봇 토큰과 아이디 값을 명시합니다.

```python
TELEGRAM_TOKEN = "tElEgRaMtOkEn"  # 텔레그렘 봇 토큰
TELEGRAM_CHAT_ID = 12345678990    # 텔레그램 봇 아이디
UPBIT_ACCESS_KEY = "uPbItAcCeSsKeY"  # 업비트 엑세스 키
UPBIT_SECRET_KEY = "uPbItSeCrEtKeY"  # 업비트 시크릿 키
```

아래 코드 설명을 참고하여 사용하면 됩니다. 반복적인 실행이 필요하다면 아래 명령어를 cron에 등록하여 사용합니다.


## 코드 설명

코드를 주기적으로 싫행하려면 cron에 등록해놓으면 됩니다.

### calc_vol_binance.py
* 바이낸스 거래량이 평소보다 높아졌다고 판단하기 위한 기준값을 계산합니다. 현재 거래량이 `평균거래량 + 승수 * 표준편차`보다 높다면 평소보다 거래량이 높아졌다고 판단합니다.
* 비트코인에 승수를 2로 하는 조사 명령어는 `python detect_vol_binance.py BTC/USDT 2` 입니다.

### calc_vol_upbit.py
* 업비트 거래량이 평소보다 높아졌다고 판단하기 위한 기준값을 계산합니다. 현재 거래량이 `평균거래량 + 승수 * 표준편차`보다 높다면 평소보다 거래량이 높아졌다고 판단합니다.
* 비트코인에 승수를 2로 하는 조사 명령어는 `python calc_vol_upbit.py KRW-BTC 2` 입니다

### detect_bb_binance.py
* 바이낸스 차트의 현재가가 볼린저 밴드 상단 또는 하단을 터치하는 캔들 발생 시 텔레그램 메시지를 전송합니다.
* 바이낸스 15분봉 기준 조사 명령어는 `python3 detect_vol_binance.py 15m` 입니다. 15m 대신 1m, 3m, 5m, 30m, 1h, 4h, 6h, 12h, 1d 등을 사용할 수 있습니다.
* ticker 종류는 소스코드에서 수정할 수 있습니다.

### detect_bb_exceed_upbit.py
* 업비트 차트의 %B 0 값을 상향돌파 시 텔레그램 메시지를 전송합니다.
* 업비트 15분봉 기준 조사 명령어는 `python3 detect_bb_exceed_upbit.py minute15` 입니다.
* minute15 대신 minute1, minute3, minute5, minute30, minute60, minute240 day 등을 사용할 수 있습니다.
* ticker 종류는 소스코드에서 수정할 수 있습니다.

### detect_bb_upbit.py
* 업비트 차트의 현재가가 볼린저 밴드 하단을 터치하는 캔들 발생 시 텔레그램 메시지를 전송합니다.
* 업비트 15분봉 기준 조사 명령어는 `python3 detect_bb_upbit.py minute15` 입니다. minute15 대신 minute1, minute3, minute5, minute30, minute60, minute240 day 등을 사용할 수 있습니다.
* ticker 종류는 소스코드에서 수정할 수 있습니다.

### detect_rsi_exceed_upbit.py
* 업비트 차트의 과매도 기준 값을 상향돌파 시 텔레그램 메시지를 전송합니다.
* 업비트 15분봉 및 과매도 기준 30 조사 명령어는 `python3 detect_rsi_exceed_upbit.py minute15 30` 입니다.
* ticker 종류는 소스코드에서 수정할 수 있습니다.

### detect_vol_binance.py
* 바이낸스 차트 거래량이 평소보다 늘어났다고 판단했을 때 텔레그램 메시지를 전송합니다.
* 바이낸스 15분봉 차트에 승수를 2로 하는 조사 명령어는 `python3 detect_vol_binance.py 15m 2` 입니다. 15m 대신 1m, 3m, 5m, 30m, 1h, 4h, 6h, 12h, 1d 등을 사용할 수 있습니다.
* ticker 종류는 소스코드에서 수정할 수 있습니다. 승수를 0으로 잡으면 거래량이 평균 이상일 때 텔레그램 메시지를 전송합니다.

### detect_vol_upbit.py
* 업비트 차트 거래량이 평소보다 늘어났다고 판단했을 때 텔레그램 메시지를 전송합니다.
* 업비트 15분봉 차트에 승수를 2로 하는 명령어는 `python3 detect_vol_upbit.py minute15 2` 입니다. minute15 대신 minute1, minute3, minute5, minute30, minute60, minute240 day 등을 사용할 수 있습니다.
* ticker 종류는 소스코드에서 수정할 수 있습니다. 승수를 0으로 잡으면 거래량이 평균 이상일 때 텔레그램 메시지를 전송합니다.

### stoploss_upbit.py
* 업비트 보유 중인 특정 코인의 현재가를 감시하여 스탑로스 설정 가겨에 도달하면 수익실현 또는 손절합니다.
* 실행 명령어는 `python3 stoploss_upbit.py COIN 수익실현가 손절가` 입니다. 예를 들어, 리플 현재가가 1000원 도달 시 수익실현, 800원 도달 시 손절하는 명령어는 `python3 stoploss_upbit.py XRP 1000 800` 입니다.

### module_binance.py
바이낸스 API(ccxt)를 활용한 함수 모음

### module_upbit.py
업비트 API(pyupbit)를 활용한 함수 모음

### MultiChartView
바이낸스 차트 여러 개를 한 화면에 보기 위한 html. 이것보단 아래 링크를 사용하는 것이 더 좋음.
* 바이낸스 현물 2분할 차트: https://www.binance.com/en/trade/multipleChart?layout=pro&type=two
* 바이낸스 현물 4분할 차트: https://www.binance.com/en/trade/multipleChart?layout=pro&type=four
* 바이낸스 현물 6분할 차트: https://www.binance.com/en/trade/multipleChart?layout=pro&type=six
* 바이낸스 선물 2분할 차트: https://www.binance.com/en/futures/multipleChart?layout=pro&type=two
* 바이낸스 선물 4분할 차트: https://www.binance.com/en/futures/multipleChart?layout=pro&type=four
* 바이낸스 선물 6분할 차트: https://www.binance.com/en/futures/multipleChart?layout=pro&type=six