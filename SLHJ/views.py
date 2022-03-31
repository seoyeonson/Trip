from django.shortcuts import render

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
    
def login(request):
    return render(request, 'login.html')

def hotel_confirm(request):
    return render(request, 'hotel_confirm.html')

def vacation_confirm(request):
    return render(request, 'vacation_confirm.html')

def 