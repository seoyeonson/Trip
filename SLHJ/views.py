import requests, bs4
import pandas as pd
from lxml import html
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote
from django.shortcuts import render, redirect


def main(request):
    return render(request, 'main.html')

def list(request):
    return render(request, 'hotel_list.html')

def user_create(request):
    return render(request, 'user_create.html')

def hotel_reserve(request):
    return render(request, 'hotel_reserve.html')

def vacation_reserve(request):
    return render(request, 'vacation_reserve.html')

def hotel_detail(request):
    return render(request, 'hotel_detail.html')
    
def vacation_detail(request):
    return render(request, 'vacation_detail.html')
    
def login(request):
    return render(request, 'login.html')

def hotel_confirm(request):
    return render(request, 'hotel_confirm.html')

def vacation_confirm(request):
    return render(request, 'vacation_confirm.html')

def user_divide(request):
    if request.method == "GET":
        return render(request, 'user_divide.html')
    elif request.method == "POST":
        user_type = request.POST.get('user_type')
        request.session['user_type'] = user_type
        # print(request.session['user_type']) #세션값 확인
        return redirect('/user_create')

def user_create(request):
    user_type = request.session['user_type'] # 회원구분에서 받아온 회원 타입 정보. admin 또는 basic
    return render(request, 'user_create.html')

def user_info(request):
    return render(request, 'user_info.html')

def pw_change(request):
    return render(request, 'pw_change.html')

def history_hotel(request):
    return render(request, 'history_hotel.html')

def history_vacation(request):
    return render(request, 'history_vacation.html')

def api(request):

    KEY = unquote("db11faf6254746fbb71311dedf6cdb3d")
    url = "https://openapi.gg.go.kr/CTST"
    Type = "xml"
    pSize = "100"
    pindex = "1"

    queryParmas = '?' + urlencode({ 
        quote_plus('KEY') : KEY,
        quote_plus('Type') : Type,
        quote_plus('pindex') : pindex,
        quote_plus('pSize') : pSize
    })

    res = requests.get(url + queryParmas).text.encode('utf-8')
    xmlobj = bs4.BeautifulSoup(res, 'lxml-xml')
    rows = xmlobj.findAll('row')

    rowList = []
    nameList = []
    columnList = []

    rowsLen = len(rows)
    for i in range(0, rowsLen):
        columns = rows[i].find_all()
        
        columnsLen = len(columns)
        for j in range(0, columnsLen):
            # 첫 번째 행 데이터 값 수집 시에만 컬럼 값을 저장한다. (어차피 rows[0], rows[1], ... 모두 컬럼헤더는 동일한 값을 가지기 때문에 매번 반복할 필요가 없다.)
            if i == 0:
                nameList.append(columns[j].name)
            # 컬럼값은 모든 행의 값을 저장해야한다.    
            eachColumn = columns[j].text
            columnList.append(eachColumn)
        rowList.append(columnList)
        columnList = []    # 다음 row의 값을 넣기 위해 비워준다. (매우 중요!!)

    result = pd.DataFrame(rowList, columns=nameList)
    print(result)

    columns = rows[0].find_all()
    print(columns)
    print(columns[0])

    return render(request, 'api.html')

