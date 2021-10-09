# crypto-bot-python

## 개요
가상화폐의 가격변동, 거래량 등을 실시간으로 파악하기 위해 만든 파이썬 코드입니다. 주요 기능은 가격이 평소보다 하락 또는 상승하거나, 거래량이 평소보다 증가할 때 텔레그램 메시지 전송입니다. 거래소는 업비트와 바이낸스를 사용합니다.

**여기 있는 코드는 테스트 중이므로 정상적인 실행을 보장하지 않으며, 이 프로그램을 사용하여 발생하는 손해에 대한 책임은 사용자 본인에게 있습니다.**

## 사용한 주요 라이브러리
* pyupbit: 업비트 API를 편하게 사용하기 위한 라이브러리
* ccxt: 바이낸스 API를 편하게 사용하기 위한 라이브러리
* python-telegram-bot: 텔레그램 메시지 전송을 위한 라이브러리
* numpy: 배열 처리를 쉽게 하기 위한 라이브러리

## 코드 설명

### calc_vol_binance.py
바이낸스 거래량이 평소보다 높아졌다고 판단하기 위한 기준 계산

### detect_bb_binance.py
바이낸스 차트의 현재가가 볼린저 밴드 상단 또는 하단을 터치하는 캔들 발생 시 텔레그램 메시지 전송

### detect_bb_upbit.py
업비트 차트의 현재가가 볼린저 밴드 하단을 터치하는 캔들 발생 시 텔레그램 메시지 전송

### detect_vol_binance.py
바이낸스 차트 거래량이 평소보다 늘어났다고 판단했을 때 텔레그램 메시지 전송

### detect_vol_upbit.py
업비트 차트 거래량이 평소보다 늘어났다고 판단했을 때 텔레그램 메시지 전송

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
* 바이낸스 선물 2분할 차트: https://www.binance.com/en/futures/multipleChart?layout=pro&type=six
* 바이낸스 선물 2분할 차트: https://www.binance.com/en/futures/multipleChart?layout=pro&type=six