from argparse import Namespace
from unicodedata import name
from django.urls import path
from SLHJ import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('main/', views.main, name='main'),
    path('list/', views.list),
    path('hotel_search/<str:SIGUN_NM>/', views.hotel_search),
    path('vacation_search/<str:SIGUN_NM>/', views.vacation_search),
    # path('login/', views.login),
    path('login/', views.login, name='login'),
    path('loginFail/', views.loginFail),
    path('user_create/', views.user_create),
    path('hotel_reserve/', views.hotel_reserve),
    path('vacation_reserve/', views.vacation_reserve),
    path('hotel_detail/<int:pk>/', views.hotel_detail),
    path('vacation_detail/<int:pk>/', views.vacation_detail),
    path('hotel_confirm/', views.hotel_confirm),
    path('vacation_confirm/', views.vacation_confirm),
    path('user_divide/', views.user_divide, name='user_divide'),
    path('user_create/', views.user_create, name='user_create'),

    # 마이페이지
    path('user_info/<int:pk>/', views.user_info, name='user_info'),
    path('pw_change/<int:pk>/', views.pw_change, name='pw_change'),
    path('pw_changeOk/', views.pw_changeOk, name='pw_changeOk'),
    path('history_hotel/<int:pk>', views.history_hotel, name='history_hotel'),
    path('history_vacation/<int:pk>', views.history_vacation, name='history_vacation'),

    # 마이페이지 - admin
    path('admin_info/', views.admin_info, name='admin_info'),
    path('admin_pw_change/', views.admin_pw_change, name='admin_pw_change'),
    path('admin_hotel/', views.admin_hotel, name='admin_hotel'),
    path('admin_vacation/', views.admin_vacation, name='admin_vacation'),
    path('admin_manage/', views.admin_manage, name='admin_manage'),

    path('hotel_register/', views.hotel_register, name="hotel_register"),
    path('vacation_register/', views.vacation_register, name="vacation_register"),

    #api data용
    # path('api/', views.api, name='api'),
    # path('api2/', views.api2, name='api2'),

    path('sample/', views.sample, name='sample'),       # vacation_reveiew 포맷입니다.
    path('sample2/', views.sample2, name='sample2'),    # vacation_reserve 포맷입니다.
    path('sample3/', views.sample3, name='sample3'),    # hotel_room 포맷입니다.
    path('sample4/', views.sample4, name='sample4'),    # hotel_reserve 포맷입니다.
    path('sample5/', views.sample5, name='sample5'),    # hotel_review 포맷입니다.
    path('sample6/', views.sample6, name='sample6'),    # hotel_imgage 포맷입니다.
]

# hotel_image, vacation_image 경로
urlpatterns += static(
    settings.MEDIA_URL, 
    document_root = settings.MEDIA_ROOT
)