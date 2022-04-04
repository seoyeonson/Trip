from django.http import Http404
import requests, bs4
import pandas as pd
from lxml import html
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote
from django.shortcuts import render, redirect
from SLHJ.models import User, Vacation, Vacation_reserve, Vacation_review, Vacation_image
from SLHJ.models import Hotel, Hotel_room, Hotel_review, Hotel_reserve
import datetime


def main(request):
    return render(request, 'main.html')

def list(request):
    return render(request, 'hotel_list.html')

def list2(request):
    return render(request, 'hotel_list2.html')

def user_create(request):
    return render(request, 'user_create.html')

def hotel_reserve(request):
    return render(request, 'hotel_reserve.html')

def vacation_reserve(request):
    return render(request, 'vacation_reserve.html')

def hotel_detail(request, pk):
    try:
        hotel = Hotel.objects.get(pk=pk)
    except Hotel.DoesNotExist:
        raise Http404('게시글을 찾을수 없습니다')

    return render(request, 'hotel_detail.html', {'hotel': hotel})
    
def vacation_detail(request, pk):
    try:
        vacation = Vacation.objects.get(pk=pk)
    except Vacation.DoesNotExist:
        raise Http404('게시글을 찾을수 없습니다')
        
    return render(request, 'vacation_detail.html', {'vacation' : vacation})
    
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

def sample(request):  # vacation_review 데이터 입력포맷입니다.

    vacation_review_content = 'sample데이터입니다.'
    vacation_review_rate = 1
    
    id = User.objects.get(pk=1)
    # id = User.objects.get(pk=pk)  pk 값을 받아와서 처리
    vacation_id = Vacation.objects.get(pk=1)
    # vacation_id = Vacation.objects.get(pk=pk)
    vacation_review = Vacation_review(
        vacation_review_content = vacation_review_content,
        vacation_review_rate = vacation_review_rate,
        id = id,
        vacation_id = vacation_id
    )
    vacation_review.save()


    all_cnt = Vacation_review.objects.filter(vacation_id_id = 1).count()    # 외래키인 vacation_id 를 받아와야합니다. filter(vacation_id_id = pk)
    vacation_id.vacation_rate = round((vacation_id.vacation_rate * (all_cnt-1) + vacation_review_rate) / all_cnt, 2)    # 평점을 새로고침하는 계산식입니다.
    vacation_id.save()

    return render(request, 'sample.html')

def sample2(request):  # vacation_reserve 데이터 입력포맷입니다.

    vacation_reserve_people = 2
    vacation_reserve_date = '2022-04-01'
    vacation_reserve_username = '이광우'
    vacation_reserve_phonenum = '010-1234-5678'
    vacation_reserve_price = 100000 * vacation_reserve_people  # 기본가격 + 인원 수

    id = User.objects.get(pk=1)
    # id = User.objects.get(pk=pk)
    vacation_id = Vacation.objects.get(pk=1)

    vacation_reserve = Vacation_reserve(
        vacation_reserve_people = vacation_reserve_people,
        vacation_reserve_date = vacation_reserve_date,
        vacation_reserve_username = vacation_reserve_username,
        vacation_reserve_phonenum = vacation_reserve_phonenum,
        vacation_reserve_price = vacation_reserve_price,
        id = id,
        vacation_id = vacation_id
    )

    vacation_reserve.save()

    return render(request, 'sample2.html')

def sample3(request):   # hotel_room 포맷입니다.

    room_type = "디럭스"
    room_price = 100000
    room_people = 2

    hotel_id = Hotel.objects.get(pk=1)  # 외래키 지정으로 pk값은 외부로 부터 받아와야합니다.

    hotel_room = Hotel_room(
        room_type = room_type,
        room_price = room_price,
        room_people = room_people,

        hotel_id = hotel_id
    )

    hotel_room.save()

    return render(request, 'sample3.html')

def sample4(request):   # hotel_reserve 포맷입니다.
    
    hotel_reserve_people = 2
    hotel_reserve_username = '이광우'
    hotel_reserve_phonenum = '010-1234-5678'
    hotel_reserve_startdate = '2022-04-02'
    hotel_reserve_enddate = '2022-04-04'

    hotel_room = Hotel_room.objects.get(pk=1)       # 방의 번호 hotel_room_id 를 사용합니다.
    hotel_reserve_price = hotel_room.room_price     # 각 방의 가격을 데이터 테이블로 받아와서 사용합니다.

    id = User.objects.get(pk=1)
    room_id = hotel_room

    hotel_reserve = Hotel_reserve(
        hotel_reserve_people = hotel_reserve_people,
        hotel_reserve_username = hotel_reserve_username,
        hotel_reserve_phonenum = hotel_reserve_phonenum,
        hotel_reserve_startdate = hotel_reserve_startdate,
        hotel_reserve_enddate = hotel_reserve_enddate,
        hotel_reserve_price = hotel_reserve_price,
        
        id = id,
        room_id = room_id        
    )

    hotel_reserve.save()

    return render(request, 'sample4.html')

def sample5(request):       # hotel_review 포맷입니다.

    hotel_review_content = 'sample 데이터입니다.'
    hotel_review_rate = 5.0
    hotel_review_date = datetime.datetime.now().strftime('%Y-%m-%d')    # 현재시간을 YYYY-MM-DD형태로 가져옵니다.

    id = User.objects.get(pk=1)             # 유저의 primary key 를 외부로 받아옵니다. 
    hotel_id = Hotel.objects.get(pk = 1)    # 호텔의 primary key 를 외부로 받아와야 됩니다. pk=pk

    hotel_review = Hotel_review(
        hotel_review_content = hotel_review_content,
        hotel_review_rate = hotel_review_rate,
        hotel_review_date = hotel_review_date,
        id = id,
        hotel_id = hotel_id
    )

    hotel_review.save()

    all_cnt = Hotel_review.objects.filter(hotel_id_id = 1).count()    # 외래키인 vacation_id 를 받아와야합니다. filter(vacation_id_id = pk)
    hotel_id.hotel_rate = round((hotel_id.hotel_rate * (all_cnt-1) + hotel_review_rate) / all_cnt, 2)    # 평점을 새로고침하는 계산식입니다.
    hotel_id.save()

    return render(request, 'sample5.html')

# def api(request):

#     KEY = unquote("db11faf6254746fbb71311dedf6cdb3d")
#     url = "https://openapi.gg.go.kr/StayingTourismHotel"
#     Type = "xml"
#     pSize = "500"
#     pindex = "1"  # 일단 수동으로 넣어줬습니다.

#     queryParmas = '?' + urlencode({ 
#         quote_plus('KEY') : KEY,
#         quote_plus('Type') : Type,
#         quote_plus('pindex') : pindex,
#         quote_plus('pSize') : pSize
#     })

#     res = requests.get(url + queryParmas).text.encode('utf-8')
#     xmlobj = bs4.BeautifulSoup(res, 'lxml-xml')
#     rows = xmlobj.findAll('row')

#     rowList = []
#     nameList = []
#     columnList = []

#     rowsLen = len(rows)
#     for i in range(0, rowsLen):
#         columns = rows[i].find_all()
        
#         columnsLen = len(columns)
#         for j in range(0, columnsLen):

#             if i == 0:
#                 nameList.append(columns[j].name)
  
#             eachColumn = columns[j].text
#             columnList.append(eachColumn)
#         rowList.append(columnList)
#         columnList = []    

#     result = pd.DataFrame(rowList, columns=nameList)
#     print(result)

#     for i in range(int(pSize)):
#         columns = rows[i].find_all()
#         BIZPLC_NM = columns[2].text             # 사업장명
#         SIGUN_NM = columns[1].text              # 시군명
#         BSN_STATE_NM = True                     # 영업상태명
#         REFINE_ROADNM_ADDR = columns[15].text   # 소재지도로명주소
#         REFINE_WGS84_LAT = columns[18].text     # WGS위도
#         if columns[18].text == "":
#             REFINE_WGS84_LAT = 0.0
#         REFINE_WGS84_LOGT = columns[17].text    # WGS경도
#         if columns[17].text == "":
#             REFINE_WGS84_LOGT = 0.0
#         hotel_rate = 0.0
#         hotel_comment = "설명이 없습니다."

#         hotel_admin_id = User.objects.get(pk=1)

#         hotel = Hotel(
#             BIZPLC_NM = BIZPLC_NM, 
#             SIGUN_NM = SIGUN_NM, 
#             BSN_STATE_NM = BSN_STATE_NM, 
#             REFINE_ROADNM_ADDR = REFINE_ROADNM_ADDR, 
#             REFINE_WGS84_LAT = REFINE_WGS84_LAT, 
#             REFINE_WGS84_LOGT = REFINE_WGS84_LOGT,
#             hotel_comment = hotel_comment,
#             hotel_rate = hotel_rate,
#             hotel_admin_id = hotel_admin_id,
#             )
        
#         hotel.save()

    # user_id = 'user1'
    # user_password = '1234'
    # user_type = '1'
    # user_email = 'test@email.com'
    # user_phonenum = '010-1234-5678'

    # user = User(user_id = user_id, user_password = user_password, user_type = user_type, user_email = user_email, user_phonenum = user_phonenum)
    # user.save()   #테스트 유저 확보 

    # return render(request, 'api.html')

# def api2(request):

#     KEY = unquote("db11faf6254746fbb71311dedf6cdb3d")
#     url = "https://openapi.gg.go.kr/CTST"
#     Type = "xml"
#     pSize = "481"
#     pindex = "1"  # 일단 수동으로 넣어줬습니다.

#     queryParmas = '?' + urlencode({ 
#         quote_plus('KEY') : KEY,
#         quote_plus('Type') : Type,
#         quote_plus('pindex') : pindex,
#         quote_plus('pSize') : pSize
#     })
    
#     res = requests.get(url + queryParmas).text.encode('utf-8')
#     xmlobj = bs4.BeautifulSoup(res, 'lxml-xml')
#     rows = xmlobj.findAll('row')

#     for i in range(int(pSize)):
#         columns = rows[i].find_all()
#         SIGUN_NM = columns[0].text
#         TURSM_INFO_NM = columns[1].text
#         SM_RE_ADDR = columns[2].text
#         TELNO = columns[3].text
#         REFINE_WGS84_LAT = columns[5].text
#         if columns[5].text == "":
#             REFINE_WGS84_LAT = 0.0
#         REFINE_WGS84_LOGT = columns[6].text
#         if columns[6].text == "":
#             REFINE_WGS84_LOGT = 0.0
#         vacation_comment = "설명이 없습니다."
#         vacation_price = 100000
#         vacation_rate = 0.0

#         vacation_admin_id = User.objects.get(pk=1)

#         vacation = Vacation(
#             SIGUN_NM = SIGUN_NM,
#             TURSM_INFO_NM = TURSM_INFO_NM,
#             SM_RE_ADDR = SM_RE_ADDR,
#             TELNO = TELNO,
#             REFINE_WGS84_LAT = REFINE_WGS84_LAT,
#             REFINE_WGS84_LOGT = REFINE_WGS84_LOGT,
#             vacation_comment = vacation_comment,
#             vacation_price = vacation_price,
#             vacation_rate = vacation_rate,
#             vacation_admin_id = vacation_admin_id
#         )

#         vacation.save()

#     return render(request, 'api2.html')
