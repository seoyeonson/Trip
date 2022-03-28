from django.shortcuts import render

def main(request):
    return render(request, 'main.html')

def hotel_reserve(request):
    return render(request, 'hotel_reserve.html')

def vacation_reserve(request):
    return render(request, 'vacation_reserve.html')
