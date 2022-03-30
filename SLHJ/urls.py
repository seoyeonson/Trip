from django.urls import path
from SLHJ import views

urlpatterns = [
    path('main/', views.main),
    path('list/', views.list),
    path('user/', views.user),
    path('user_create/', views.user_create),
    path('hotel_reserve/', views.hotel_reserve),
    path('vacation_reserve/', views.vacation_reserve),
    # path('hotel_detail/<int:id>/', views.hotel_detail),
    path('hotel_detail/', views.hotel_detail),
    path('hotel_confirm/', views.hotel_confirm),
    path('vacation_confirm/', views.vacation_confirm),
]
