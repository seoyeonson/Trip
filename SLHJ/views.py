from django.shortcuts import render

def main(request):
    return render(request, 'main.html')

def list(request):
    return render(request, 'hotel_list.html')
def hotel_reserve(request):
    return render(request, 'hotel_reserve.html')

def vacation_reserve(request):
    return render(request, 'vacation_reserve.html')

def login(request):
    return render(request, 'login.html')
