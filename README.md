# crypto-bot-python

**이 리포지토리는 더 이상 업데이트되지 않습니다. 이후 업데이트는 [crypto-bot-python-v2](https://github.com/jeon-won/crypto-bot-python-v2) 리포지토리에서 진행됩니다.**

## 개요
가상화폐 포지션을 잡기 위한 타이밍을 파악하기 위해 만든 파이썬 코드입니다. 거래량, 볼린저밴드 또는 RSI 보조지표를 사용하여 과매도 또는 과매수 시점이라고 판단할 때 텔레그램 메시지를 전송합니다. 거래소는 업비트와 바이낸스를 사용합니다.

**테스트 중인 코드이므로 정상적인 실행을 보장하지 않으며, 이 프로그램을 사용하여 발생하는 손해에 대한 책임은 사용자 본인에게 있습니다.**


## 사용한 주요 라이브러리
* pyupbit: 업비트 API를 편하게 사용하기 위한 라이브러리
* ccxt: 바이낸스 API를 편하게 사용하기 위한 라이브러리
* python-telegram-bot: 텔레그램 메시지 전송을 위한 라이브러리
* numpy 및 pandas: 배열 처리를 쉽게 하기 위한 라이브러리
* python-dotenv: 환경변수(.env)를 사용하기 위한 라이브러리
* playsound: 사운드 재생을 위한 라이브러리


## 사용법

우선 루트 경로에 `.env` 파일을 만듭니다. 이 파일에 API 키 값을 명시합니다.

```python
TELEGRAM_TOKEN = "tElEgRaMtOkEn"  # 텔레그렘 봇 토큰
TELEGRAM_CHAT_ID = 12345678990    # 텔레그램 봇 아이디
UPBIT_ACCESS_KEY = "uPbItAcCeSsKeY"  # 업비트 엑세스 키 (Upbit.stoploss_upbit.py에서만 사용)
UPBIT_SECRET_KEY = "uPbItSeCrEtKeY"  # 업비트 시크릿 키 (Upbit.stoploss_upbit.py에서만 사용)
```

아래 코드 설명을 참고하여 사용하면 됩니다. 반복적인 실행이 필요하다면 아래 명령어를 cron에 등록하여 사용합니다.


## 코드 설명(Binance)

### module_binance.py
바이낸스 API(ccxt)를 활용한 함수 모음

### calc_vol.py
* 바이낸스 거래량이 평소보다 높아졌다고 판단하기 위한 기준값을 계산합니다. 현재 거래량이 `평균거래량 + 승수 * 표준편차`보다 높다면 평소보다 거래량이 높아졌다고 판단합니다.
* 비트코인에 승수를 2로 하는 조사 명령어는 `python Binance/calc_vol.py BTC/USDT 2` 입니다.

### detect_bb_exceed.py
* 바이낸스 차트의 %B 0 값을 상향돌파 또는 1 값을 하향돌파 시 텔레그램 메시지를 전송합니다.
* 바이낸스 15분봉 기준 조사 명령어는 `python3 Binance/detect_bb_exceed.py 15m` 입니다.

### detect_bb.py
* 바이낸스 차트의 현재가가 볼린저 밴드 상단 또는 하단을 터치하는 캔들 발생 시 텔레그램 메시지를 전송합니다.
* 바이낸스 15분봉 기준 조사 명령어는 `python3 Binance/detect_bb.py 15m` 입니다. 15m 대신 1m, 3m, 5m, 30m, 1h, 4h, 6h, 12h, 1d 등을 사용할 수 있습니다.

### detect_candle_15m.py
* 바이낸스 15분봉 차트 캔들 크기(시가와 종가의 차이)가 평균 크기 이상일 때 텔레그램 메시지를 전송하거나 사운드를 재생합니다.
* 실행 명령어는 `python3 Binance/detect_candle_15m.py` 입니다. 
* 무한루프로 작동하기 떄문에 cron에 등록하여 사용하면 안 됩니다.

### detect_vol.py
* 바이낸스 차트 거래량이 평소보다 늘어났다고 판단했을 때 텔레그램 메시지를 전송합니다.
* 바이낸스 15분봉 차트에 승수를 2로 하는 조사 명령어는 `python3 Binance/detect_vol.py 15m 2` 입니다. 15m 대신 1m, 3m, 5m, 30m, 1h, 4h, 6h, 12h, 1d 등을 사용할 수 있습니다. 승수를 0으로 잡으면 거래량이 평균 이상일 때 텔레그램 메시지를 전송합니다.


## 코드 설명(Upbit)

### module_upbit.py
업비트 API(pyupbit)를 활용한 함수 모음

### calc_vol.py
* 업비트 거래량이 평소보다 높아졌다고 판단하기 위한 기준값을 계산합니다. 현재 거래량이 `평균거래량 + 승수 * 표준편차`보다 높다면 평소보다 거래량이 높아졌다고 판단합니다.
* 비트코인에 승수를 2로 하는 조사 명령어는 `python Upbit/calc_vol.py KRW-BTC 2` 입니다

### detect_bb_exceed.py
* 업비트 차트의 %B 0 값을 상향돌파 시 텔레그램 메시지를 전송합니다.
* 업비트 15분봉 기준 조사 명령어는 `python3 Upbit/detect_bb_exceed.py minute15` 입니다.
* minute15 대신 minute1, minute3, minute5, minute30, minute60, minute240 day 등을 사용할 수 있습니다.

### detect_bb.py
* 업비트 차트의 현재가가 볼린저 밴드 하단을 터치하는 캔들 발생 시 텔레그램 메시지를 전송합니다.
* 업비트 15분봉 기준 조사 명령어는 `python3 Upbit/detect_bb.py minute15` 입니다. minute15 대신 minute1, minute3, minute5, minute30, minute60, minute240 day 등을 사용할 수 있습니다.

### detect_candle_15m.py
* 업비트 15분봉 차트 캔들 크기(시가와 종가의 차이)가 평균 크기 이상일 때 텔레그램 메시지를 전송하거나 사운드를 재생합니다.
* 실행 명령어는 `python3 Upbit/detect_candle_15m.py` 입니다. 
* 무한루프로 작동하기 때문에 cron에 등록하여 사용하면 안 됩니다.

### detect_rsi_exceed.py
* 업비트 차트의 RSI 과매도 기준 값을 상향돌파 시 텔레그램 메시지를 전송합니다.
* 업비트 15분봉 및 과매도 기준 30 조사 명령어는 `python3 Upbit/detect_rsi_exceed.py minute15 30` 입니다. minute15 대신 minute1, minute3, minute5, minute30, minute60, minute240 day 등을 사용할 수 있습니다.

### detect_vol.py
* 업비트 차트 거래량이 평소보다 늘어났다고 판단했을 때 텔레그램 메시지를 전송합니다.
* 업비트 15분봉 차트에 승수를 2로 하는 명령어는 `python3 Upbit/detect_vol.py minute15 2` 입니다. minute15 대신 minute1, minute3, minute5, minute30, minute60, minute240 day 등을 사용할 수 있습니다. 
* 승수를 0으로 잡으면 거래량이 평균 이상일 때 텔레그램 메시지를 전송합니다.

### stoploss.py
* 업비트 보유 중인 특정 코인의 현재가를 감시하여 스탑로스 설정 가격에 도달하면 수익실현 또는 손절합니다.
* 실행 명령어는 `python3 Upbit/stoploss.py COIN 수익실현가 손절가` 입니다. 예를 들어, 리플 현재가가 1000원 도달 시 수익실현, 800원 도달 시 손절하는 명령어는 `python3 Upbit/stoploss.py XRP 1000 800` 입니다.


## MultiChartView
바이낸스 차트 여러 개를 한 화면에 보기 위한 html. 이것보단 아래 링크를 사용하는 것이 더 좋음.
* 바이낸스 현물 2분할 차트: https://www.binance.com/en/trade/multipleChart?layout=pro&type=two
* 바이낸스 현물 4분할 차트: https://www.binance.com/en/trade/multipleChart?layout=pro&type=four
* 바이낸스 현물 6분할 차트: https://www.binance.com/en/trade/multipleChart?layout=pro&type=six
* 바이낸스 선물 2분할 차트: https://www.binance.com/en/futures/multipleChart?layout=pro&type=two
* 바이낸스 선물 4분할 차트: https://www.binance.com/en/futures/multipleChart?layout=pro&type=four
* 바이낸스 선물 6분할 차트: https://www.binance.com/en/futures/multipleChart?layout=pro&type=six


## (압도적 감사!) 가상화폐 관련 유튜브 채널
* [나씨TV - 비트코인 단타의 모든것](https://www.youtube.com/c/ocllos)
* [머프TV - 비트코인 실전단타](https://www.youtube.com/c/MoneyPrinter)
* [경제적 자유 TV](https://www.youtube.com/channel/UCFx00f8tKyiuB7ANAajoKeA)
* [초강력 보조지표 호두형](https://www.youtube.com/channel/UC9KQaCA_EMobJUxZszQ4wlg)
