from django.http import Http404
import requests, bs4
import pandas as pd
from lxml import html
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote
from django.shortcuts import render, redirect
from SLHJ.models import User, Vacation, Vacation_reserve, Vacation_review, Vacation_image
from SLHJ.models import Hotel, Hotel_room, Hotel_review, Hotel_reserve, Hotel_image
import datetime
from django.core.paginator import Paginator
import os
import mimetypes
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse


def main(request):
    return render(request, 'main.html')

def list(request):
    return render(request, 'hotel_list.html')

def list2(request,SIGUN_NM):
    count={}
    #SIGUN_NM= OO시인 hotel 테이블 가져옴 
    all_hotel_lists = Hotel.objects.filter(SIGUN_NM = SIGUN_NM)

    hotel_room = Hotel_room.objects.all()

    # 리뷰별 평점점수 (1~5점) count
    for i in range(5):
        # (크거나 작은 값) orm 사용
        # 참고 https://dev-yakuza.posstree.com/ko/django/orm/
        count.update({i+1 : all_hotel_lists.filter(hotel_rate__gt=i).filter(hotel_rate__lte=i+1).count()})
    # 보여질 페이지 번호 < << 1 2 3 4 5 >> >
    write_pages = int(request.session.get('write_pages', 5))
    # 한 페이지에 보일 리뷰 개수
    per_page = int(request.session.get('per_page', 5))
    # 현재 페이지
    page = int(request.GET.get('page', 1))

    # 한 페이지당 5개씩 보여주는 Paginator 생성
    paginator = Paginator(all_hotel_lists, per_page)
    # 페이지에 대한 정보
    page_obj = paginator.get_page(page)

    start_page = ((int)((page_obj.number - 1) / write_pages) * write_pages) + 1
    end_page = start_page + write_pages - 1

    if end_page >= paginator.num_pages:
        end_page = paginator.num_pages
    context = {
        # 'hotel': hotel,
        'lists': page_obj,  # Hotel table
        'start_page': start_page,
        'end_page': end_page,
        'page_range': range(start_page, end_page + 1),
        'count' : count,
        'hotel_rooms' : hotel_room, # Hotel_room table
    }
    return render(request, 'hotel_list2.html', context)

def user_create(request):
    return render(request, 'user_create.html')

def hotel_reserve(request):
    # 세션에 저장된 예약 정보들 (hotel_detail 에서 선택한 옵션들) 받아옵니다. *추후 기본값 수정 필요*
    hotel_name = request.session.get('hotel_name', Hotel.objects.get(hotel_id=1).BIZPLC_NM)
    hotel_reserve_people = request.session.get('hotel_reserve_people', 2)
    hotel_reserve_startdate = request.session.get('hotel_reserve_startdate', '2022-04-01')
    hotel_reserve_enddate = request.session.get('hotel_reserve_enddate', '2022-04-02')
    start_date = datetime.datetime.strptime(hotel_reserve_startdate, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(hotel_reserve_enddate, '%Y-%m-%d').date()

    hotel_room_pk = request.session.get('hotel_room_pk',1) #detail에서, 선택한 객실의 pk. 
    hotel_room = Hotel_room.objects.get(pk=hotel_room_pk)       # 방의 번호 hotel_room_id 를 사용합니다.
    night = (end_date - start_date).days
    hotel_reserve_price = hotel_room.room_price * night  # 각 방의 가격을 데이터 테이블로 받아와서 사용합니다.
    if request.method=="GET":
        context = {
            'hotel_name': hotel_name,
            'reserve_people': hotel_reserve_people,
            'reserve_startdate':  hotel_reserve_startdate,
            'reserve_enddate': hotel_reserve_enddate,
            'room_type': hotel_room.room_type,
            'hotel_price': '{0:,}'.format(hotel_reserve_price),
            'night': night,
        }
        return render(request, 'hotel_reserve.html', context)
    elif request.method=="POST": # 예약정보 테이블에 저장

        hotel_reserve_username = request.POST["reserve_name"]
        hotel_reserve_phonenum = request.POST["phone_num"]

        id = User.objects.get(id=request.session.get('id',1)) # session에 저장된 user의 정보를 불러옵니다.(기본값 1은 추후 수정)
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

        return redirect(f'/hotel_confirm/?reserve={hotel_reserve.hotel_reserve_id}')

def vacation_reserve(request):
    vacation_id = request.session.get('vacation_id', 1)
    vacation_reserve_people = request.session.get('vacation_reserve_people', 2)
    vacation_reserve_date = request.session.get('vacation_reserve_date', '2022-04-02')
    vacation_reserve_price = (Vacation.objects.get(vacation_id=vacation_id).vacation_price) * vacation_reserve_people
    place_name =  Vacation.objects.get(vacation_id=vacation_id).TURSM_INFO_NM
    vacation_price = '{0:,}'.format(vacation_reserve_price)
    if request.method=="GET":
        context = {
            'place_name': place_name,
            'reserve_people': vacation_reserve_people,
            'reserve_date': vacation_reserve_date,
            'vacation_price': vacation_price,
        }
        return render(request, 'vacation_reserve.html', context)

    elif request.method=="POST":
        id = User.objects.get(id=request.session.get('id',1)) # session에 저장된 user의 정보를 불러옵니다.(기본값 1은 추후 수정)
        vacation_reserve = Vacation_reserve(
            vacation_reserve_people = vacation_reserve_people,
            vacation_reserve_date = vacation_reserve_date,
            vacation_reserve_username = request.POST['reserve_name'],
            vacation_reserve_phonenum = request.POST['phone_num'],
            vacation_reserve_price = vacation_reserve_price,
            id = id,
            vacation_id_id = vacation_id
        )
        vacation_reserve.save()
        return redirect(f'/vacation_confirm/?reserve={vacation_reserve.vacation_reserve_id}')

def hotel_detail(request, pk):

    if request.method == "GET":
        count = {}
        # ##### hotel_detail
        try:
            hotel = Hotel.objects.get(pk=pk)

            # ##### hotel_room
            # hotel_room = Hotel_room.objects.filter(hotel_id=pk).values_list('room_type','room_people', 'room_price').distinct()
            hotel_room = Hotel_room.objects.filter(hotel_id=pk).values('room_type','room_people', 'room_price').distinct()
            print(hotel_room.values())

            # ##### hotel_review
            # hotel_id 가 pk인 hotel_review 를 가져옴
            all_hotel_reviews = Hotel_review.objects.filter(hotel_id=pk)

            # ##### recommand_vacation
            # 같은 지역,vacation_rate 가 높은 순으로 4개 가져오기
            recommand_vacations = Vacation.objects.filter(SIGUN_NM = hotel.SIGUN_NM).order_by('-vacation_rate')[:4]

            # ##### hotel_img
            try:
                hotel_img = Hotel_image.objects.get(hotel_id=pk)
            except Hotel_image.DoesNotExist:
                hotel_img = '';

            # Pagination
            # 리뷰별 평점점수 (1~5점) count
            for i in range(5):
                # (크거나 작은 값) orm 사용
                count.update({i+1 : all_hotel_reviews.filter(hotel_review_rate__gt=i).filter(hotel_review_rate__lte=i+1).count()})

            # 보여질 페이지 번호 < << 1 2 3 4 5 >> >
            write_pages = int(request.session.get('write_pages', 5))
            # 한 페이지에 보일 리뷰 개수
            per_page = int(request.session.get('per_page', 5))
            # 현재 페이지
            page = int(request.GET.get('page', 1))

            # 한 페이지당 5개씩 보여주는 Paginator 생성
            paginator = Paginator(all_hotel_reviews, per_page)
            # 페이지에 대한 정보
            page_obj = paginator.get_page(page)

            start_page = ((int)((page_obj.number - 1) / write_pages) * write_pages) + 1
            end_page = start_page + write_pages - 1

            if end_page >= paginator.num_pages:
                end_page = paginator.num_pages

        except Hotel.DoesNotExist:
            raise Http404('게시글을 찾을수 없습니다')
            

        context = {
            'hotel': hotel,
            'hotel_room': hotel_room,
            'reviews': page_obj,
            'start_page': start_page,
            'end_page': end_page,
            'page_range': range(start_page, end_page + 1),
            'recommand_vacations' : recommand_vacations,
            'count' : count,
            'hotel_img' : hotel_img,
        }

        return render(request, 'hotel_detail.html', context)
    
def vacation_detail(request, pk):
    count = {}
    try:
        vacation = Vacation.objects.get(pk=pk)
    except Vacation.DoesNotExist:
        raise Http404('게시글을 찾을수 없습니다')

    # ##### vacation_review
    # vacation_id 가 pk인 vacation_review 를 가져옴
    all_vacation_reviews = Vacation_review.objects.filter(vacation_id=pk)

    # 리뷰별 평점점수 (1~5점) count
    for i in range(5):
        count.update({i+1 : all_vacation_reviews.filter(vacation_review_rate__gt=i).filter(vacation_review_rate__lte=i+1).count()})

    # 보여질 페이지 번호 < << 1 2 3 4 5 >> >
    write_pages = int(request.session.get('write_pages', 5))
    # 한 페이지에 보일 리뷰 개수
    per_page = int(request.session.get('per_page', 5))
    # 현재 페이지
    page = int(request.GET.get('page', 1))

    # 한 페이지당 5개씩 보여주는 Paginator 생성
    paginator = Paginator(all_vacation_reviews, per_page)
    # 페이지에 대한 정보
    page_obj = paginator.get_page(page)

    start_page = ((int)((page_obj.number - 1) / write_pages) * write_pages) + 1
    end_page = start_page + write_pages - 1

    if end_page >= paginator.num_pages:
        end_page = paginator.num_pages

    # ##### recommand_hotel
    # 같은 지역, hotel_rate 가 높은 순으로 4개 가져오기
    recommand_hotels = Hotel.objects.filter(SIGUN_NM=vacation.SIGUN_NM).order_by('-hotel_rate')[:4]

    context = {
        'vacation': vacation,
        'reviews': page_obj,
        'start_page': start_page,
        'end_page': end_page,
        'page_range': range(start_page, end_page + 1),
        'recommand_hotels' : recommand_hotels,
        'count' : count,
    }
        
    return render(request, 'vacation_detail.html', context)
    
def login(request):
    return render(request, 'login.html')

def hotel_confirm(request):
    reserve_id = request.GET['reserve']
    reserve_info = Hotel_reserve.objects.get(hotel_reserve_id=reserve_id)
    # room_type = Hotel_room.objects.get(room_id=reserve_info.room_id        

    context = {
        'reserve_info': reserve_info, 
        'hotel': Hotel.objects.get(hotel_id = reserve_info.room_id.hotel_id.hotel_id).BIZPLC_NM,
        'price': '{0:,}'.format(reserve_info.hotel_reserve_price),
        'night': (reserve_info.hotel_reserve_enddate - reserve_info.hotel_reserve_startdate).days
        }   
    return render(request, 'hotel_confirm.html', context)

def vacation_confirm(request):
    reserve_id = request.GET['reserve']
    reserve_info = Vacation_reserve.objects.get(vacation_reserve_id=reserve_id)
    place = Vacation.objects.get(vacation_id = reserve_info.vacation_id_id).TURSM_INFO_NM
    context = {
        'reserve_info': reserve_info, 
        'place': place,
        'price': '{0:,}'.format(reserve_info.vacation_reserve_price),
        }   
    return render(request, 'vacation_confirm.html', context)

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
    if request.method=="GET":
        user = User.objects.get(id=1)
        context = {
            'user': user
        }
        return render(request, 'user_info.html', context)
    if request.method=="POST":
        # 이메일, 전화번호를 입력한 값으로 변경
        user = User.objects.get(id=1)
        context = {
            'user': user
        }
        return render(request, 'user_info.html', context)

def pw_change(request):
    user = User.objects.get(id=1)
    context = {
        'user': user
    }
    return render(request, 'pw_change.html', context)

def history_hotel(request):
    user = User.objects.get(id=1)
    context = {
        'user': user
    }
    return render(request, 'history_hotel.html', context)

def history_vacation(request):
    user = User.objects.get(id=1)
    context = {
        'user': user
    }
    return render(request, 'history_vacation.html', context)

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

    room_type = "스탠다드"
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
    hotel_review_rate = 4.0
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

def sample6(request):   # hotel_image 포맷입니다.  vacation_image 는 hotel => vacation 으로 바꾸기만 하면됩니다.
    if request.method == "POST":
        hotel_id = Hotel.objects.get(pk=1)      # 어떤 호텔의 사진인지 가져와야 합니다. ex) pk = pk
        hotel_image_title = request.POST['fileTitle']
        hotel_image_file_path = request.FILES["uploadedFile"]

        document = Hotel_image(
            hotel_id = hotel_id,
            hotel_image_title = hotel_image_title,
            hotel_image_file_path = hotel_image_file_path,
            hotel_image_originname = hotel_image_file_path.name,
        )
        document.save()
    
    documents = Hotel_image.objects.all().order_by("-pk")

    return render(request, 'sample6.html', {"sample6s" : documents})


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

#     # user_id = 'user1'
#     # user_password = '1234'
#     # user_type = '1'
#     # user_email = 'test@email.com'
#     # user_phonenum = '010-1234-5678'

#     # user = User(user_id = user_id, user_password = user_password, user_type = user_type, user_email = user_email, user_phonenum = user_phonenum)
#     # user.save()   #테스트 유저 확보 

#     return render(request, 'api.html')

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
