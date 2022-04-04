import sys, random, math
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException

if __name__ == "__main__":
    # set api key, api secret
    api_key = "NCSBBQKQMGO7AFBL"
    api_secret = "AUB8IHWTNNKQEYV7DTAETK8BFTTOJVMS"
    ## 4 params(to, from, type, text) are mandatory. must be filled
    params = dict()
    params['type'] = 'sms' # Message type ( sms, lms, mms, ata )
    params['to'] = '01000000000' # Recipients Number '01000000000,01000000001'
    params['from'] = '01000000000' # Sender number
    auth_num = math.floor(random.random()*(10**6))
    params['text'] = f'''Trip에서 전송된 인증번호 입니다.
    인증번호 : {auth_num}
    '''
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

