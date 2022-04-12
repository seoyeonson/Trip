import sys, random, math, requests, json
# from selenium import webdriver
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException
from bs4 import BeautifulSoup as bs

page = requests.get("https://library.gabia.com/")
soup = bs(page.text, "html.parser")

elements = soup.select('div.esg-entry-content a > span')

for index, element in enumerate(elements, 1):
		print("{} 번째 게시글의 제목: {}".format(index, element.text))


def coolSMS(phoneNum):
    url = 'http://127.0.0.1:8000/vacation_reserve/'
    try:
        res = requests.get(url)
        soup = bs(res.content, 'html.parser')

        attr = soup.find(id="coolsms_pNum")
        print("HTML:/n", attr)
    except:
        print("Invalid URL or some error occured while making the GET request to the specified URL")

    if __name__ == "__main__":
        # set api key, api secret
        api_key = "NCSBBQKQMGO7AFBL"
        api_secret = "AUB8IHWTNNKQEYV7DTAETK8BFTTOJVMS"
        ## 4 params(to, from, type, text) are mandatory. must be filled
        params = dict()
        params['type'] = 'sms' # Message type ( sms, lms, mms, ata )
        params['to'] = 'phoneNum' # Recipients Number '01000000000,01000000001'
        params['from'] = '01034544451' # Sender number
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

