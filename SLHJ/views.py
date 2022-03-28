from django.shortcuts import render

def main(request):
    return render(request, 'main.html')

def list(request):
    return render(request, 'hotel_list.html')