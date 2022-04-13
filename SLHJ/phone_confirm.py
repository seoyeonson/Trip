import sys, random, math, requests, json, sdk
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException
from bs4 import BeautifulSoup as bs

r = requests.get("")

##  @brief This sample code demonstrate how to send sms through CoolSMS Rest API PHP
if __name__ == "__main__":
    # set api key, api secret
    api_key = "NCSBBQKQMGO7AFBL"
    api_secret = "AUB8IHWTNNKQEYV7DTAETK8BFTTOJVMS"

    ## 4 params(to, from, type, text) are mandatory. must be filled
    params = dict()
    params['type'] = 'sms' # Message type ( sms, lms, mms, ata )
    params['to'] = '01034544451' # Recipients Number '01000000000,01000000001'
    params['from'] = '01034544451' # Sender number
    confirm_num = round(random.random()*(1000000))
    params['text'] = f'Trip에서 전송한 메시지입니다.\n 인증번호 : [ {confirm_num} ]' # Message

    cool = Message(api_key, api_secret)
    try:
        response = cool.send(params)
        print("Success Count : %s" % response['success_count'])
        print("Error Count : %s" % response['error_count'])
        print("Group ID : %s" % response['group_id'])

        if "error_list" in response:
            print("Error List : %s" % response['error_list'])

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)

    sys.exit()