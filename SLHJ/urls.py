from django.urls import path
from SLHJ import views

urlpatterns = [
    path('main/', views.main),
    path('list/', views.list),
    path('login/', views.login),
    path('user_create/', views.user_create),
    path('hotel_reserve/', views.hotel_reserve),
    path('vacation_reserve/', views.vacation_reserve),
    # path('hotel_detail/<int:id>/', views.hotel_detail),
    path('hotel_detail/', views.hotel_detail),
    path('hotel_confirm/', views.hotel_confirm),
    path('vacation_confirm/', views.vacation_confirm),
    path('user_divide/', views.user_divide),
    path('user_create/', views.user_create, name='user_create'),

    # 마이페이지
    path('user_info/', views.user_info, name='user_info'),
    path('pw_change/', views.pw_change, name='pw_change'),
    path('history_hotel/', views.history_hotel, name='history_hotel'),
    path('history_vacation/', views.history_vacation, name='history_vacation'),
]
