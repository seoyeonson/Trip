from distutils.log import error
from pickle import TRUE
from ssl import AlertDescription
from django.http import Http404
# from jinja2 import Undefined
import requests, bs4
import pandas as pd
from lxml import html
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote
from django.shortcuts import render, redirect
from django.http import HttpResponse
from SLHJ.models import User, Vacation, Vacation_reserve, Vacation_review, Vacation_image
from SLHJ.models import Hotel, Hotel_room, Hotel_review, Hotel_reserve, Hotel_image
from datetime import datetime
import datetime
from django.core.paginator import Paginator
import os
import mimetypes
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
import time
import json

def main(request):
    vacation_imgs = []
    hotel_imgs = []

    if request.method == 'GET':
        hotel_places = Hotel.objects.all().values('SIGUN_NM').distinct()
        recommand_vacations = Vacation.objects.all().order_by('-vacation_rate')[:4]
        recommand_hotels = Hotel.objects.all().order_by('-hotel_rate')[:4]

        # 추천 호텔 이미지
        for hotel in recommand_hotels:
            # 추천 호텔 이미지가 있을 경우
            if Hotel_image.objects.filter(hotel_id=hotel.hotel_id):
                hotel_imgs.append(Hotel_image.objects.get(hotel_id=hotel.hotel_id))
            # 추천 호텔 이미지가 없을 경우
            else:
                hotel_imgs.append("")

        # 추천 여행지 이미지
        for vacation in recommand_vacations:
            # 추천 여행지 이미지가 있을 경우
            if Vacation_image.objects.filter(vacation_id=vacation.vacation_id):
                vacation_imgs.append(Vacation_image.objects.get(vacation_id=vacation.vacation_id))
            # 추천 여행지 이미지가 없을 경우
            else:
                vacation_imgs.append("")


        context = {
            'hotel_places' : hotel_places,
            'hotel_imgs': hotel_imgs,
            'vacation_imgs': vacation_imgs,
        }
        return render(request, 'main.html', context)

    if request.method == 'POST':
        if request.POST.get('hotel_type') == 'hotel_type' :
            SIGUN_NM = request.POST.get('SIGUN_NM')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            hotel_reserve_people = request.POST.get('hotel_reserve_people')

            request.session['SIGUN_NM'] = SIGUN_NM
            request.session['start_date'] = start_date
            request.session['end_date'] = end_date
            request.session['hotel_reserve_people'] = hotel_reserve_people

            return redirect('/hotel_search/')

        if request.POST.get('vacation_type') == 'vacation_type':
            SIGUN_NM = request.POST.get('SIGUN_NM')
            vacation_reserve_people = request.POST.get('vacation_reserve_people')

            request.session['SIGUN_NM'] = SIGUN_NM
            request.session['vacation_reserve_people'] = vacation_reserve_people

            return redirect('/vacation_search/')


def hotel_search(request):
    if request.method == "POST":
        SIGUN_NM = request.POST.get('SIGUN_NM')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        hotel_reserve_people = request.POST.get('hotel_reserve_people')
        print(start_date, end_date)

        request.session['SIGUN_NM'] = SIGUN_NM
        request.session['start_date'] = start_date
        request.session['end_date'] = end_date
        request.session['hotel_reserve_people'] = hotel_reserve_people

        return redirect('/hotel_search/')

    if request.method == "GET":
        count={}
        # [TODO] hotel list => seach 조건 고려해서 가져오기 (날짜, 인원수, 지역) 
        hotel_places = Hotel.objects.all().values('SIGUN_NM').distinct()
        SIGUN_NM = request.session.get('SIGUN_NM')
        start_date = request.session.get('start_date')
        end_date = request.session.get('end_date')
        hotel_reserve_people = request.session.get('hotel_reserve_people')

        # SIGUN_NM= OO시인 hotel 테이블 가져옴
        # 그 호텔의 예약정보가 겹치지 않는 호텔
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

        last_page=0

        for last_page in paginator.page_range:
            last_page = last_page + 1

        last_page= last_page -1
        zero = 0
        context = {
            # 'hotel': hotel,
            'hotel_places' : hotel_places,
            'lists': page_obj,  # Hotel table
            'SIGUN_NM': SIGUN_NM,
            'start_date': start_date,
            'end_date' : end_date,
            'hotel_reserve_people': hotel_reserve_people,
            'start_page': start_page,
            'end_page': end_page,
            'last_page' : last_page,
            'page_range': range(start_page, end_page + 1),
            'count' : count,
            'zero' : zero,
            'hotel_rooms' : hotel_room, # Hotel_room table
                }
        return render(request, 'hotel_search.html', context)

def vacation_search(request):
    count={}
    vacation_places = Vacation.objects.all().values('SIGUN_NM').distinct()
    #SIGUN_NM= OO시인 vacation 테이블 가져옴 
    SIGUN_NM = request.session.get('SIGUN_NM', '평택시')
    vacation_reserve_people = request.session.get('vacation_reserve_people')
    all_vacation_lists = Vacation.objects.filter(SIGUN_NM = SIGUN_NM)


    # 리뷰별 평점점수 (1~5점) count
    for i in range(5):
        # (크거나 작은 값) orm 사용
        # 참고 https://dev-yakuza.posstree.com/ko/django/orm/
        count.update({i+1 : all_vacation_lists.filter(vacation_rate__gt=i).filter(vacation_rate__lte=i+1).count()})
    
    # 보여질 페이지 번호 < << 1 2 3 4 5 >> >
    write_pages = int(request.session.get('write_pages', 5))
   
    # 한 페이지에 보일 리뷰 개수
    per_page = int(request.session.get('per_page', 5))
    
    # 현재 페이지
    page = int(request.GET.get('page', 1))

    # 한 페이지당 5개씩 보여주는 Paginator 생성
    paginator = Paginator(all_vacation_lists, per_page)
    
    # 페이지에 대한 정보
    page_obj = paginator.get_page(page)

    start_page = ((int)((page_obj.number - 1) / write_pages) * write_pages) + 1
    end_page = start_page + write_pages - 1

    if end_page >= paginator.num_pages:
        end_page = paginator.num_pages

    last_page=0

    for last_page in paginator.page_range:
        last_page = last_page + 1

    last_page= last_page -1
    
    context = {
        'vacation_places' : vacation_places,
        'lists': page_obj,  # vacation table
        'start_page': start_page,
        'end_page': end_page,
        'SIGUN_NM': SIGUN_NM,
        'vacation_reserve_people': vacation_reserve_people,
        'last_page' : last_page,
        'page_range': range(start_page, end_page + 1),
        'count' : count,
    }
    return render(request, 'vacation_search.html', context)

def user_create(request):
    return render(request, 'user_create.html')

def hotel_reserve(request):
    # 세션에 저장된 예약 정보들 (hotel_detail 에서 선택한 옵션들) 받아옵니다. *추후 기본값 수정 필요*
    hotel_name = request.session.get('hotel_name', Hotel.objects.get(hotel_id=1).BIZPLC_NM)
    hotel_reserve_people = request.session.get('hotel_reserve_people', 2)
    hotel_reserve_startdate = request.session.get('start_date', '2022-04-01')
    hotel_reserve_enddate = request.session.get('end_date', '2022-04-02')
    start_date = datetime.datetime.strptime(hotel_reserve_startdate, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(hotel_reserve_enddate, '%Y-%m-%d').date()
    reserve_room = request.session.get('reserve_room')


    hotel_room_pk = request.session.get('hotel_room_pk', 1) #detail에서, 선택한 객실의 pk. 
    hotel_room = Hotel_room.objects.get(pk=hotel_room_pk)       # 방의 번호 hotel_room_id 를 사용합니다.
    night = (end_date - start_date).days
    hotel_reserve_price = hotel_room.room_price * night  # 각 방의 가격을 데이터 테이블로 받아와서 사용합니다.
    if request.method=="GET":
        context = {
            'hotel_name': hotel_name,
            'reserve_people': hotel_reserve_people,
            'reserve_startdate':  hotel_reserve_startdate,
            'reserve_enddate': hotel_reserve_enddate,
            'reserve_room' : reserve_room,
            'night': night,
            'room_type': hotel_room.room_type,
            'hotel_price': '{0:,}'.format(hotel_reserve_price),
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
            room_id = room_id,       
        )

        hotel_reserve.save()

        return redirect(f'/hotel_confirm/?reserve={hotel_reserve.hotel_reserve_id}')

def vacation_reserve(request):
    
    vacation_id = request.session.get('vacation_pk')
    vacation_reserve_people = request.session.get('vacation_reserve_people')
    vacation_reserve_date = request.session.get('vacation_reserve_date')
    if (vacation_id=="") or (vacation_reserve_people=="") or (vacation_reserve_date==""):
        return redirect('/main/') # session에 예약정보가 담겨있지 않은 경우 main으로 redirect됩니다.
    try:    
        vacation= Vacation.objects.get(vacation_id=vacation_id)
        vacation_reserve_price = vacation.vacation_price 
        vacation_reserve_people = int(vacation_reserve_people)
        place_name = vacation.TURSM_INFO_NM
        id = User.objects.get(id=request.session.get('user','')) # session에 저장된 user의 정보를 불러옵니다.
        if id == "":
            return redirect('/login/')

        if request.method=="GET":
            
            context = {
                'place_name': place_name,
                'reserve_people': vacation_reserve_people,
                'vacation_price': vacation_reserve_price,
                'show_price': vacation_reserve_price * vacation_reserve_people,
                'vacation_reserve_date': vacation_reserve_date,
            }
            return render(request, 'vacation_reserve.html', context)

        elif request.method=="POST":
            vacation_reserve = Vacation_reserve(
                vacation_reserve_people = request.POST['peopleNum'],
                vacation_reserve_date = request.POST['end_date'],
                vacation_reserve_username = request.POST['reserve_name'],
                vacation_reserve_phonenum = request.POST['phone_num'],
                vacation_reserve_price = vacation_reserve_price * int(request.POST['peopleNum']),
                id = id,
                vacation_id_id = vacation_id
            )
            vacation_reserve.save()
            del request.session['vacation_pk'] # vacation 예약 후 세션삭제
            del request.session['vacation_reserve_people']
            return redirect(f'/vacation_confirm/?reserve={vacation_reserve.vacation_reserve_id}')
    
    except Vacation.DoesNotExist:
        raise Http404('잘못된 접근입니다.')


def hotel_detail(request, pk):
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    if request.method == "GET":
        # list 에서 session으로 넘어온 값
        # check_in = request.session.get('check_in', now)
        # check_out = request.session.get('check_out', now)
        # hotel_reserve_people = request.session.get('hotel_reserve_people', 2)

        # 평점별 인원수
        count = {}
        # 추천 여행지 이미지
        vacation_imgs = []

        # ##### hotel_detail
        try:
            hotel = Hotel.objects.get(pk=pk)

            # ##### hotel_room
            # hotel_room = Hotel_room.objects.filter(hotel_id=pk).values('room_type','room_people', 'room_price').distinct()
            hotel_room = Hotel_room.objects.filter(hotel_id=pk)

            # ##### hotel_review
            # hotel_id 가 pk인 hotel_review 를 가져옴
            all_hotel_reviews = Hotel_review.objects.filter(hotel_id=pk).order_by('-hotel_review_id')

            # ##### recommand_vacation
            # 같은 지역,vacation_rate 가 높은 순으로 4개 가져오기
            recommand_vacations = Vacation.objects.filter(SIGUN_NM = hotel.SIGUN_NM).order_by('-vacation_rate')[:4]

            print(type(recommand_vacations))

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

            # 추천 여행지 이미지
            for vacation in recommand_vacations:
                # 추천 여행지 이미지가 있을 경우
                if Vacation_image.objects.filter(vacation_id=vacation.vacation_id):
                    vacation_imgs.append(Vacation_image.objects.get(vacation_id=vacation.vacation_id))
                # 추천 여행지 이미지가 없을 경우
                else:
                    vacation_imgs.append("")

        except Hotel.DoesNotExist:
            raise Http404('게시글을 찾을수 없습니다')
            

        context = {
            # 'check_in' : check_in,
            # 'check_out' : check_out,
            # 'hotel_reserve_people' : hotel_reserve_people,
            'vacation_imgs': vacation_imgs,
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

    if request.method == "POST":
        hotel_pk = pk
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        hotel_reserve_people = request.POST.get('hotel_reserve_people')
        reserve_room = request.POST.get('reserve_room')
        hotel_room_pk = request.POST.get('hotel_room_pk')

        request.session['start_date'] = start_date
        request.session['end_date'] = end_date
        request.session['hotel_pk'] = hotel_pk
        request.session['hotel_reserve_people'] = hotel_reserve_people
        request.session['reserve_room'] = reserve_room
        request.session['hotel_room_pk'] = hotel_room_pk

        return redirect('/hotel_reserve/')

def vacation_detail(request, pk):
    now = datetime.datetime.now()
    hotel_imgs = []
    if request.method == "GET":
        check_in = request.session.get('check_in', now)
        check_out = request.session.get('check_out', now)
        vacation_reserve_people = request.session.get('vacation_reserve_people', 2)

        count = {}
        try:
            vacation = Vacation.objects.get(pk=pk)
            all_vacation_reviews = Vacation_review.objects.filter(vacation_id=pk).order_by('-vacation_review_id')
            recommand_hotels = Hotel.objects.filter(SIGUN_NM = vacation.SIGUN_NM).order_by('-hotel_rate')[:4]
            
            try:
                vacation_img = Vacation_image.objects.get(vacation_id=pk)
            except Vacation_image.DoesNotExist:
                vacation_img = '';

            # 추천 호텔 이미지
            for hotel in recommand_hotels:
                # 추천 호텔 이미지가 있을 경우
                if Hotel_image.objects.filter(hotel_id=hotel.hotel_id):
                    hotel_imgs.append(Hotel_image.objects.get(hotel_id=hotel.hotel_id))
                # 추천 호텔 이미지가 없을 경우
                else:
                    hotel_imgs.append("")

            # Pagination
            # 리뷰별 평점점수 (1~5점) count
            for i in range(5):
                # (크거나 작은 값) orm 사용
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

        except Hotel.DoesNotExist:
            raise Http404('게시글을 찾을수 없습니다')
            

        context = {
            'check_in' : check_in,
            'check_out' : check_out,
            'vacation_reserve_people' : vacation_reserve_people,
            'hotel_imgs': hotel_imgs,
            'vacation': vacation,
            'reviews': page_obj,
            'start_page': start_page,
            'end_page': end_page,
            'page_range': range(start_page, end_page + 1),
            'recommand_hotels' : recommand_hotels,
            'count' : count,
            'vacation_img' : vacation_img,
        }

        return render(request, 'vacation_detail.html', context)

    if request.method == "POST":
        vacation_pk = pk
        vacation_reserve_people = request.POST.get('vacation_reserve_people')
        vacation_reserve_date = request.POST.get('end_date') # 우선 end_date를 이용날짜로 받아오도록 하였습니다. (추후 하루만 선택가능하도록 datepicker 수정 필요)

        request.session['vacation_reserve_date'] = vacation_reserve_date
        request.session['vacation_reserve_people'] = vacation_reserve_people
        request.session['vacation_pk'] = vacation_pk

        return redirect('/vacation_reserve/')

def login(request):
    context = {
    }

    if request.method == 'POST':
        user_id = request.POST.get('id')
        user_pw = request.POST.get('pw')
        try:
            user = User.objects.get(user_id = user_id)
        except User.DoesNotExist:
            return redirect('/loginFail/')
        context = {
            'user' : user,
        }
        if user.user_password == user_pw:
            request.session['user'] = user.id
            request.session['user_type'] = user.user_type
            # request.session['user_email'] = user.user_email

            # context['logged'] = True
            # context['id'] = user.id
            # context['user_id'] = user_id
            # context['user_type'] = user.user_type
            # context['user'] = user
            # print(context['user_type'],  context['user_id'], context['logged'], context['id'], context['user'].user_password)
            return render(request, 'loginOk.html', context)
        elif user.user_password != user_pw:
            return redirect('/loginFail/')

    return render(request, 'login.html', context)

def logout(request):
    request.session.flush()
    return render(request, 'logout.html')

def loginFail(request):
    return render(request, 'loginFail.html')

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
        join_type = request.POST.get('join_type') # 혹시 삭제되지 않을 경우 다른 기능에 영향을 주지 않도록 'user_type' 대신 다른 이름으로 변경했습니다.
        request.session['join_type'] = join_type
        return redirect('/user_create')

def user_create(request):
    user_type = request.session['join_type'] # 회원구분에서 받아온 회원 타입 정보. admin 또는 basic

    if request.method == 'POST':
        user_id = request.POST.get('id')
        user_password = request.POST.get('pw')
        if user_type == 'admin':    # 관리자 회원은 user_type 이 1 입니다.
            user_type = 1
        elif user_type == 'basic':  # 일반회원은 user_type이 2 입니다.
            user_type = 2

        user_email = request.POST.get('email')
        user_phonenum = request.POST.get('phonenum')

        user = User(
            user_id = user_id,
            user_password = user_password,
            user_type = user_type,
            user_email = user_email,
            user_phonenum = user_phonenum
        )

        user.save()
        del request.session['join_type'] # 회원등록 완료. 세션 삭제
        return redirect('/login/')

    return render(request, 'user_create.html')

def user_info(request):
    pk = request.session['user']
    
    if request.method=="POST":
        # 이메일, 전화번호를 입력한 값으로 변경
        user = User.objects.get(pk=pk)
        user_phonenum = request.POST.get('user_phonNum')
        user_email = request.POST.get('user_email')

        user.user_phonenum = user_phonenum
        user.user_email = user_email
        user.save()

        context = {
            'user': user,
        }

        return render(request, 'user_info.html', context)
    if request.method=="GET":
        user = User.objects.get(pk=pk)
        context = {
            'user': user
        }
        return render(request, 'user_info.html', context)

def pw_change(request):
    pk = request.session['user']

    user = User.objects.get(pk=pk)
    context = {
        'user':user
    }
    if request.method == 'POST':
        now_password = request.POST.get('current_pw')
        if now_password != user.user_password:
            return redirect('/pw_changeFail2/')
        user_password = request.POST.get('confirm_pw')

        user.user_password = user_password
        user.save()
        request.session.flush()
        return redirect('/pw_changeOk/')

    return render(request, 'pw_change.html', context)

def pw_changeOk(request):
    return render(request, 'pw_changeOk.html')

def history_hotel(request):
    pk = request.session['user']

    user = User.objects.get(pk=pk)
    hotel_reserve = Hotel_reserve.objects.filter(id=pk).order_by('-hotel_reserve_enddate')
    # hotel_reserves = []

    try:
        hotel_image = Hotel_image.objects.get(pk=hotel_reserve[0].room_id.hotel_id)

    except Hotel_image.DoesNotExist:
        hotel_image = ''

    # for i in range(hotel_reserve.count()):
    #     hotel_reserves.append(hotel_reserve[i])

    # 한 페이지에 보일 예약 개수
    per_page = 5
    # 현재 페이지
    page = int(request.GET.get('page',1))
    # 페이지네이터 생성
    paginator = Paginator(hotel_reserve, per_page)
    # 페이지 개수 
    page_obj = paginator.get_page(page)
    # 보여질 페이징 개수. 
    write_pages = int(request.session.get('write_pages', 5))
    # 시작페이지
    start_page =((int)((page_obj.number -1 ) / write_pages) * write_pages) + 1
    end_page = start_page + write_pages -1
    if end_page >= paginator.num_pages:
        end_page = paginator.num_pages

    # hotel_reserves = []
    # hotel_image = Hotel_image.objects.get(pk=hotel_reserve[0].room_id.hotel_id)

    # for i in range(hotel_reserve.count()):
    #     hotel_reserves.append(hotel_reserve[i])
    
    context = {
        'user': user,
        'hotel_reserves' : page_obj,
        'start_page' : start_page,
        'end_page' : end_page,
        'page_range' : range(start_page, end_page + 1),
        'hotel_image' : hotel_image,
        'today': datetime.datetime.now().date(),        
    }

    if request.method == 'POST':
        review = request.POST.get('review')
        rate = request.POST.get('rate')
        hotel_id = request.POST.get('hotel_id')
        hotel = Hotel.objects.get(pk=hotel_id)
        now = datetime.datetime.now().strftime('%Y-%m-%d')

        hotel_review = Hotel_review(
            hotel_review_content = review,
            hotel_review_rate = rate,
            hotel_review_date = now,

            id = user,
            hotel_id = hotel
        )

        hotel_review.save()

        all_cnt = Hotel_review.objects.filter(hotel_id_id = hotel_id).count()
        hotel.hotel_rate = round((hotel.hotel_rate * (all_cnt-1) + int(rate)) / all_cnt, 2)    # 평점을 새로고침하는 계산식입니다.
        hotel.save()
        return redirect(f'/hotel_detail/{hotel_id}')

    return render(request, 'history_hotel.html', context)

def history_vacation(request):
    pk = request.session['user']

    user = User.objects.get(pk=pk)
    vacation_reserve = Vacation_reserve.objects.filter(id=pk).order_by('-vacation_reserve_date')

    # 한 페이지에 보일 예약 개수
    per_page = 5
    # 현재 페이지
    page = int(request.GET.get('page',1))
    # 페이지네이터 생성
    paginator = Paginator(vacation_reserve, per_page)
    # 페이지 개수 
    page_obj = paginator.get_page(page)
    # 보여질 페이징 개수. 
    write_pages = int(request.session.get('write_pages', 5))
    # 시작페이지
    start_page =((int)((page_obj.number - 1) / write_pages) * write_pages) + 1
    end_page = start_page + write_pages -1
    if end_page >= paginator.num_pages:
        end_page = paginator.num_pages
    
    context = {
        'user': user,
        'vacation_reserves': page_obj,
        'start_page': start_page,
        'end_page': end_page,
        'page_range': range(start_page, end_page+1),
        'today': datetime.datetime.now().date()
    }
    return render(request, 'history_vacation.html', context)

def admin_info(request):
    pk = request.session['user']
    
    if request.method=="POST":
        # 이메일, 전화번호를 입력한 값으로 변경
        user = User.objects.get(pk=pk)
        user_phonenum = request.POST.get('user_phonNum')
        user_email = request.POST.get('user_email')

        user.user_phonenum = user_phonenum
        user.user_email = user_email
        user.save()

        context = {
            'user': user,
        }

        return render(request, 'admin_info.html', context)
    if request.method=="GET":
        user = User.objects.get(pk=pk)
        context = {
            'user': user
        }
        return render(request, 'admin_info.html', context)

def admin_pw_change(request):
    pk = request.session['user']
    
    user = User.objects.get(pk=pk)
    context = {
        'user':user
    }
    if request.method == "POST":
        now_password = request.POST.get('current_pw')
        if now_password != user.user_password:
            return redirect('/pw_changeFail/')
        user_password = request.POST.get('confirm_pw')

        user.user_password = user_password
        user.save()
        request.session.flush()
        return redirect('/pw_changeOk/')

    return render(request, 'admin_pw_change.html', context)

def pw_changeFail(request):
    return render(request, 'pw_changeFail.html')

def pw_changeFail2(request):
    return render(request, 'pw_changeFail2.html')

def admin_hotel(request):
    pk = request.session['user']

    user = User.objects.get(pk=pk)
    hotel = Hotel.objects.filter(hotel_admin_id = user.id)
    # hotels = []
    # for i in range(hotel.count()):
    #     hotels.append(hotel[i])
    # per_page = 5
    page = int(request.GET.get('page',1))
    paginator = Paginator(hotel, 5)
    page_obj = paginator.get_page(page)
    write_pages = int(request.session.get('write_pages', 5))
    # 시작페이지
    start_page = ((int)((page_obj.number-1) / write_pages) * write_pages) + 1
    end_page = start_page + write_pages -1
    if end_page >= paginator.num_pages:
        end_page = paginator.num_pages

    context = {
        'user' : user,
        'hotels' : page_obj,
        'start_page': start_page,
        'end_page': end_page,
        'page_range': range(start_page, end_page+1),
    }

    return render(request, 'admin_hotel.html', context)
    '''
    pk=request.session['user']
    if request.method=="POST":
        hotels=Hotel.objects.get(pk=pk) 
        

   
    
    # 리뷰별 평점점수 (1~5점) count
    # count={}
    # for i in range(5):
    # #     # (크거나 작은 값) orm 사용
    # #     # 참고 https://dev-yakuza.posstree.com/ko/django/orm/
    #     count.update({i+1 : hotels.filter(hotel_rate__gt=i).filter(hotel_rate__lte=i+1).count()})
    # # 보여질 페이지 번호 < << 1 2 3 4 5 >> >
    # write_pages = int(request.session.get('write_pages', 5))

    # # 한 페이지에 보일 리뷰 개수
    # per_page = int(request.session.get('per_page', 5))

    # # 현재 페이지
    # page = int(request.GET.get('page', 1))

    # # 한 페이지당 5개씩 보여주는 Paginator 생성
    # paginator = Paginator(hotels, per_page)
    
    # # 페이지에 대한 정보
    # page_obj = paginator.get_page(page)

    # start_page = ((int)((page_obj.number - 1) / write_pages) * write_pages) + 1
    # end_page = start_page + write_pages - 1

    # if end_page >= paginator.num_pages:
    #     end_page = paginator.num_pages

    # last_page=0

    # for last_page in paginator.page_range:
    #     last_page = last_page + 1

    # last_page= last_page -1
    

    
   
    '''
    # five=5
    # i =1

    # context={
    #      'five' : five,
    #      'i' : i 
    #     # 'hotels' : hotels
    #     # 'lists' : page_obj,
    #     # 'start_page': start_page,
    #     # 'end_page': end_page,
    #     # 'last_page' : last_page,
    #     # 'page_range': range(start_page, end_page + 1),
    #     # 'count' : count,

    # }
    

    # return render(request, 'admin_hotel.html', context)

def admin_vacation(request):
    pk = request.session['user']

    user = User.objects.get(pk=pk)
    vacation = Vacation.objects.filter(vacation_admin_id = user.id)

    per_page = 5
    page = int(request.GET.get('page',1))
    paginator = Paginator(vacation, per_page)
    page_obj = paginator.get_page(page)
    write_pages = 5
    # 시작페이지
    start_page =((int)((page_obj.number-1) / write_pages) * write_pages) + 1
    end_page = start_page + write_pages -1
    if end_page >= paginator.num_pages:
        end_page = paginator.num_pages

    context = {
        'user' : user,
        'vacations' : page_obj,
        'start_page': start_page,
        'end_page': end_page,
        'page_range': range(start_page, end_page+1),
    }
    return render(request, 'admin_vacation.html', context)

def admin_manage(request):
    pk = request.session['user']
    user = User.objects.get(pk=pk)

    context = {
        'user' : user,
    }
    return render(request, 'admin_manage.html', context)

def hotel_register(request):
    pk = request.session['user']
    user = User.objects.get(pk=pk)

    if request.method == 'POST':
        BIZPLC_NM = request.POST.get('hotel_name')
        SIGUN_NM = request.POST.get('hotel_area')
        BSN_STATE_NM = 1
        REFINE_ROADNM_ADDR = request.POST.get('hotel_adress')
        REFINE_WGS84_LAT = 0.0
        REFINE_WGS84_LOGT = 0.0
        hotel_rate = 0.0
        hotel_comment = request.POST.get('context')
        hotel_admin_id = user
        if hotel_comment == '':
            hotel_comment = '설명이 없습니다.'

        hotel = Hotel(
            BIZPLC_NM = BIZPLC_NM,
            SIGUN_NM = SIGUN_NM,
            BSN_STATE_NM = BSN_STATE_NM,
            REFINE_ROADNM_ADDR = REFINE_ROADNM_ADDR,
            REFINE_WGS84_LAT = REFINE_WGS84_LAT,
            REFINE_WGS84_LOGT = REFINE_WGS84_LOGT,
            hotel_rate = hotel_rate,
            hotel_comment = hotel_comment,
            hotel_admin_id = hotel_admin_id,
        )

        hotel.save()
        return redirect('/admin_hotel/')

    context = {
        'user' : user,
    }
    return render(request, 'hotel_register.html', context)

def vacation_register(request):
    pk = request.session['user']
    user = User.objects.get(pk=pk)

    context = {
        'user' : user,
    }
    return render(request, 'vacation_register.html', context)

def admin_hotel_detail(request, hk):
    pk = request.session['user']
    hotel = Hotel.objects.get(pk = hk)
    hotel_room = Hotel_room.objects.filter(hotel_id = hk)
    user = User.objects.get(pk=pk)
    hotel_review = Hotel_review.objects.filter(hotel_id = hk).order_by("-pk")
    all_review = hotel_review.count()

    context = {
        'user' : user,
        'hotel' : hotel,
        'hotel_rooms' : hotel_room,
        'hotel_reviews' : hotel_review,
        'all_review' : all_review,
    }
    return render(request, 'admin_hotel_detail.html', context)

def admin_vacation_detail(request):
    pk = request.session['user']
    user = User.objects.get(pk=pk)

    context = {
        'user' : user,
    }

    return render(request, 'admin_vacation_detail.html',context )

def hotel_update(request):
    pk = request.session['user']
    user = User.objects.get(pk=pk)

    context = {
        'user' : user,
    }
    return render(request, 'hotel_update.html', context)

def vacation_update(request):
    pk = request.session['user']
    user = User.objects.get(pk=pk)

    context = {
        'user' : user,
    }
    return render(request, 'vacation_update.html', context)

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
    vacation_reserve_date = '2022-12-31'
    vacation_reserve_username = '이광우'
    vacation_reserve_phonenum = '010-1234-5678'

    id = User.objects.get(pk=3)
    # id = User.objects.get(pk=pk)
    vacation_id = Vacation.objects.get(pk=14)

    vacation_reserve_price = vacation_id.vacation_price * vacation_reserve_people  # 기본가격 + 인원 수

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

    room_type = "더블베드룸"
    room_price = 200000
    room_people = 3

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
    
    hotel_reserve_people = 3
    hotel_reserve_username = '김사과'
    hotel_reserve_phonenum = '010-1234-5678'
    hotel_reserve_startdate = '2022-08-09'
    hotel_reserve_enddate = '2022-08-10'

    hotel_room = Hotel_room.objects.get(pk=10)       # 방의 번호 hotel_room_id 를 사용합니다.
    hotel_reserve_price = hotel_room.room_price     # 각 방의 가격을 데이터 테이블로 받아와서 사용합니다.

    id = User.objects.get(pk=2)
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

    id = User.objects.get(pk=3)             # 유저의 primary key 를 외부로 받아옵니다. 
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
    # if request.method == "GET":
    #     request.session()
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

def sample7(request):   # vacation_image 포맷입니다.  vacation_image 는 vacation => vacation 으로 바꾸기만 하면됩니다.
    # if request.method == "GET":
    #     request.session()
    if request.method == "POST":
        vacation_id = Vacation.objects.get(pk=1)      # 어떤 호텔의 사진인지 가져와야 합니다. ex) pk = pk
        vacation_image_title = request.POST['fileTitle']
        vacation_image_file_path = request.FILES["uploadedFile"]

        document = Vacation_image(
            vacation_id = vacation_id,
            vacation_image_title = vacation_image_title,
            vacation_image_file_path = vacation_image_file_path,
            vacation_image_originname = vacation_image_file_path.name,
        )
        document.save()
    
    documents = Vacation_image.objects.all().order_by("-pk")

    return render(request, 'sample7.html', {"sample7s" : documents})

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

def option_change(request, pk):
    if request.method == "POST":
        check_in = request.POST.get('check_in', '')
        check_out = request.POST.get('check_out', '')
        hotel_reserve_people = request.POST.get('hotel_reserve_people', 0)

        reserve = Hotel_reserve.objects.get(pk=pk)
        hotel_room = Hotel_room.objects.filter(hotel_id=pk)

        
        context = {
            'check_in' : check_in,
            'check_out' : check_out,
            'hotel_reserve_people' : hotel_reserve_people,
            'hotel_room' : hotel_room,
        }
        return HttpResponse(json.dumps(context), content_type="application/json")
        # context를 json 타입으로
