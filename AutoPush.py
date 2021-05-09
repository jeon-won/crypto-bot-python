import time
import pyupbit
import datetime
import requests


#############  상수  ##########################################################################
SLACK_OAUTH_TOKEN = "mYsLaCkOaUtHtOkEn"
INTERVAL = "minute60"   # 1시간 차트 조사
###############################################################################################


#############  변수  ######################################################################
coin_tickers = []       # 업비트에서 거래 가능한 코인 목록
tickers_to_buy = []     # 매수 각인 코인 목록
message = ""            # Slack 메시지 내용
###############################################################################################


#############  함수  ##########################################################################
def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer " + token},
        data={"channel": channel,"text": text}
    )

def get_ma(ticker, interval, count):
    """이동 평균선 조회 (count: 일 수)"""
    df = pyupbit.get_ohlcv(ticker, interval=interval, count=count)
    ma = df['close'].rolling(count).mean().iloc[-1]
    time.sleep(0.1) # 초당 API 호출 허용 수가 정해져 있어서 쉬엄쉬엄 해줘야 함...
    return ma

def get_prev_ma(ticker, interval, count):
    """직전 이동 평균선 조회 (count: 일 수)"""
    df = pyupbit.get_ohlcv(ticker, interval=interval, count=count+1)
    prev_df = df.drop(df.index[len(df)-1])
    prev_ma = prev_df['close'].rolling(count).mean().iloc[-1]
    time.sleep(0.1)
    return prev_ma

def get_coin_tickers():
    """업비트에서 한화로 거래 가능한 코인 조회"""
    tickers = []
    for ticker in pyupbit.get_tickers():
        if(ticker[0:3] == "KRW"):
            tickers.append(ticker)
            time.sleep(0.1)
    return tickers

def find_coin(tickers):
    """매수 각인 코인 찾기"""
    buy_list = []

    for ticker in tickers:
        ma7 = get_ma(ticker, INTERVAL, 7)  
        ma15 = get_ma(ticker, INTERVAL, 15)
        prev_ma7 = get_prev_ma(ticker, INTERVAL, 7)
        prev_ma15 = get_prev_ma(ticker, INTERVAL, 15)

        # (대부분 애매하긴 하지만...) 7 - 15일 이평선이 골든크로스로 변하고
        if((prev_ma7 < prev_ma15) and (ma7 > ma15)):
            ma50 = get_ma(ticker, INTERVAL, 50)
            # 7 - 5 - 50일 이평선이 정배열인 경우 심상치 않은(?) 코인으로 간주
            if(ma15 > ma50):
                buy_list.append(ticker)
        
    return buy_list

def get_message(tickers):
    """슬랙 메시지 생성"""
    msg = ""
    if(len(tickers) != 0):
        msg += "이 코인 심상치 않다?! "
        for ticker in tickers:
            msg += ticker.replace("KRW-", "") + " "
    return msg
###############################################################################################

while True:
    try:
        # 시간 간격은 설정 안 해도 되지만 알아서 설정... 여기선 매 시간 0~5분 사이에 수행
        now = datetime.datetime.now() # - datetime.timedelta(minutes=15)
        start_time = datetime.datetime(now.year, now.month, now.day, now.hour)
        end_time = datetime.datetime(now.year, now.month, now.day, now.hour, minute=5)

        if((start_time <= now < end_time)):
            coin_tickers = get_coin_tickers()
            tickers_to_buy = find_coin(coin_tickers)
            if(len(tickers_to_buy) != 0):
                message = get_message(tickers_to_buy)
                post_message(SLACK_OAUTH_TOKEN, "#crypto", message)
            time.sleep(400)
        else:
            time.sleep(60)
    
    except Exception as e:
        print(e)
        time.sleep(1)