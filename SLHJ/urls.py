from django.urls import path
from SLHJ import views

urlpatterns = [
    path('main/', views.main),
    path('hotel_reserve/', views.hotel_reserve),
    path('vacation_reserve/', views.vacation_reserve),
    path('login/', views.login),
]
