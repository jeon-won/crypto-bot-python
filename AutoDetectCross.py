import time
import datetime
import requests
import cryptofunc

"""
AutoDetectCross.py
* Date: 2021.05.10.
* Author: Jeon Won
* Func: 가상화폐 이동평균선이 골든크로스로 변할 것으로 예상될 때 슬랙 메시지 전송
* Notice: 봉 마감 전에 조사하므로 정확하지 않을 수 있음...
"""

#############  상수  ##########################################################################
SLACK_OAUTH_TOKEN = "sLaCkOaUtHtOkEn"
INTERVAL = "minute60"  # 1시간 차트 조사
###############################################################################################


#############  변수  ######################################################################
coin_tickers = []       # 업비트에서 거래 가능한 코인 목록
tickers_to_cross = []   # 골든크로스로 변할 것으로 예상되는 코인 목록
message = ""            # Slack 메시지 내용
###############################################################################################


#############  함수  ##########################################################################
def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer " + token},
        data={"channel": channel,"text": text}
    )

def get_message(tickers):
    """슬랙 메시지 생성"""
    msg = ""
    if(len(tickers) != 0):
        msg += "골든크로스 할 것으로 예상되는 코인: "
        for ticker in tickers:
            msg += ticker.replace("KRW-", "") + " "
    return msg

def find_coin(tickers):
    """골든크로스로 변할 것 같은 코인 찾기"""
    buy_list = []

    for ticker in tickers:
        ma7 = cryptofunc.get_ma(ticker, INTERVAL, 7)  
        ma15 = cryptofunc.get_ma(ticker, INTERVAL, 15)
        ma50 = cryptofunc.get_ma(ticker, INTERVAL, 50)
        prev_ma7 = cryptofunc.get_prev_ma(ticker, INTERVAL, 7)
        prev_ma15 = cryptofunc.get_prev_ma(ticker, INTERVAL, 15)
        prev_ma50 = cryptofunc.get_prev_ma(ticker, INTERVAL, 50)

        # 7 - 15일 이평선이 골든크로스로 변하고
        if((prev_ma7 < prev_ma15) and (ma7 > ma15)):
            # 7 - 15 - 50일 이평선이 정배열인 경우 알림
            if(ma15 > ma50):
                buy_list.append(ticker)
        
        # (테스트) 7 - 50일 이평선이 골든크로스로 변했을 때도 알림
        if((prev_ma7 < prev_ma50) and (ma7 > ma50)):
            buy_list.append(ticker)

    return buy_list
###############################################################################################


while True:
    try:
        # 시간 간격은 설정 안 해도 되지만 알아서 설정... 여기선 매 시간 0~5분 사이에 수행
        now = datetime.datetime.now() # - datetime.timedelta(minutes=15)
        start_time_1 = datetime.datetime(now.year, now.month, now.day, now.hour)
        end_time_1 = datetime.datetime(now.year, now.month, now.day, now.hour, minute=5)
        start_time_2 = datetime.datetime(now.year, now.month, now.day, now.hour, minute=55)
        end_time_2 = datetime.datetime(now.year, now.month, now.day, now.hour, minute=59, second=50)

        if((start_time_1 <= now < end_time_1) or (start_time_2 <= now < end_time_2)):
            coin_tickers = cryptofunc.get_coin_tickers()
            tickers_to_cross = find_coin(coin_tickers)
            if(len(tickers_to_cross) != 0):
                message = get_message(tickers_to_cross)
                post_message(SLACK_OAUTH_TOKEN, "#crypto", message) # 토큰, 채널명, 메시지
            time.sleep(300)
        else:
            time.sleep(60)
    
    except Exception as e:
        print(e)
        time.sleep(1)