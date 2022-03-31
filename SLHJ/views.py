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
