from statistics import mode
from tabnanny import verbose
from tkinter import CASCADE
from django.db import models

class User(models.Model):
    user_id = models.CharField(max_length=20, verbose_name='유저ID') 
    user_password = models.CharField(max_length=20, verbose_name='유저비밀번호')
    user_type = models.IntegerField(verbose_name='유저타입') # 1:관리자 2:일반
    user_email = models.EmailField(max_length=100, verbose_name='유저이메일')
    user_phonenum = models.CharField(max_length=15, verbose_name='유저전화번호')

    class Meta:
        db_table = 'SLHJ_user'
        verbose_name = '사용자'
        verbose_name_plural = '사용자(들)'  

    def __str__(self):
        return self.user_id

class Vacation(models.Model):
    vacation_id = models.AutoField(primary_key=True)
    SIGUN_NM = models.CharField(max_length=20, verbose_name='시군명')
    TURSM_INFO_NM = models.CharField(max_length=20, verbose_name='관광지명')
    SM_RE_ADDR = models.CharField(max_length=50, verbose_name='소재주소')
    TELNO = models.CharField(max_length=15, verbose_name='전화번호')
    REFINE_WGS84_LAT = models.FloatField(verbose_name='정제WGS84위도')
    REFINE_WGS84_LOGT = models.FloatField(verbose_name='정제WGS84경도')
    vacation_comment = models.CharField(max_length=200, verbose_name='요약설명')
    vacation_price = models.IntegerField(verbose_name='여행지가격')
    vacation_rate = models.FloatField(verbose_name='여행지평점')

    vacation_admin_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'SLHJ_vacation'
        verbose_name = '여행지'
        verbose_name_plural = '여행지(들)'

    def __str__(self):
        return self.TURSM_INFO_NM

class Vacation_review(models.Model):
    vacation_review_id = models.AutoField(primary_key=True)
    vacation_review_content = models.CharField(max_length=100, verbose_name='리뷰내용')
    vacation_review_rate = models.IntegerField(verbose_name='리뷰평점')
    vacation_review_date = models.DateTimeField(auto_now_add=True, verbose_name='리뷰등록시간')

    id = models.ForeignKey(User, on_delete=models.CASCADE)
    vacation_id = models.ForeignKey(Vacation, on_delete=models.CASCADE)

    class Meta:
        db_table = 'SLHJ_vacation_review'
        verbose_name = '여행지리뷰'
        verbose_name_plural = '여행지리뷰(들)'

    def __str__(self):
        return self.vacation_review_id

class Vacation_reserve(models.Model):
    vacation_reserve_id = models.AutoField(primary_key=True)
    vacation_reserve_people = models.IntegerField(verbose_name='예약인원')
    vacation_reserve_date = models.DateField(verbose_name='예약날짜')
    vacation_reserve_username = models.CharField(max_length=20, verbose_name='예약자명')
    vacation_reserve_phonenum = models.CharField(max_length=15, verbose_name='핸드폰번호')
    vacation_reserve_price = models.IntegerField(verbose_name='결제금액')

    id = models.ForeignKey(User, on_delete=models.CASCADE)
    vacation_id = models.ForeignKey(Vacation, on_delete=models.CASCADE)

    class Meta:
        db_table = 'SLHJ_vacation_reserve'
        verbose_name = '여행지예약'
        verbose_name_plural = '여행지예약(들)'

    def __str__(self):
        return self.vacation_reserve_id

class Vacation_image(models.Model):
    vacation_id = models.OneToOneField(Vacation, primary_key=True, on_delete=models.CASCADE)
    vacation_image_title = models.CharField(max_length=100, verbose_name='파일이름')

    # upload_to=업로드될 경로 (media/ 이하 경로)
    vacation_image_file_path = models.FileField(upload_to="UploadedFiles/", verbose_name='파일경로')
    vacation_image_originname = models.CharField(max_length=100, verbose_name='원본이름')

    class Meta:
        db_table = 'SLHJ_vacation_image'
        verbose_name = '여행지사진'
    
    def __str__(self):
        return self.vacation_id

class Hotel(models.Model):
    hotel_id = models.AutoField(primary_key=True)
    BIZPLC_NM = models.CharField(max_length=30, verbose_name='사업장명')
    SIGUN_NM = models.CharField(max_length=20, verbose_name='시군명')
    BSN_STATE_NM = models.BooleanField(verbose_name='영업상태명')
    REFINE_ROADNM_ADDR = models.CharField(max_length=50, verbose_name='소재지도로명주소')
    REFINE_WGS84_LAT = models.FloatField(verbose_name='WGS84위도')
    REFINE_WGS84_LOGT = models.FloatField(verbose_name='WGS84경도')
    hotel_rate = models.FloatField(verbose_name='평점')
    hotel_comment = models.CharField(max_length=200, verbose_name='요약설명')

    hotel_admin_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'SLHJ_hotel'
        verbose_name = '호텔'
        verbose_name_plural = '호텔(들)'

    def __str__(self):
        return self.BIZPLC_NM

class Hotel_room(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_type = models.CharField(max_length=20, verbose_name='방타입')
    room_price = models.IntegerField(verbose_name='방가격')
    room_people = models.IntegerField(verbose_name='사용인원')

    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'SLHJ_hotel_room'
        verbose_name = '호텔방'
        verbose_name_plural = '호텔방(들)'

    def __str__(self):
        return self.room_id

class Hotel_reserve(models.Model):
    hotel_reserve_id = models.AutoField(primary_key=True)
    hotel_reserve_people = models.IntegerField(verbose_name='예약인원')
    hotel_reserve_username = models.CharField(max_length=20, verbose_name='예약자명')
    hotel_reserve_phonenum = models.CharField(max_length=15, verbose_name='핸드폰번호')
    hotel_reserve_startdate = models.DateField(verbose_name='체크인날짜')
    hotel_reserve_enddate = models.DateField(verbose_name='체크아웃날짜')
    hotel_reserve_price = models.IntegerField(verbose_name='결제금액')

    id = models.ForeignKey(User, on_delete=models.CASCADE)
    room_id = models.ForeignKey(Hotel_room, on_delete=models.CASCADE)

    class Meta:
        db_table = 'SLHJ_hotel_reserve'
        verbose_name = '호텔예약'
        verbose_name_plural = '호텔예약(들)'

    def __str__(self):
        return self.hotel_reserve_id

class Hotel_review(models.Model):
    hotel_review_id = models.AutoField(primary_key=True)
    hotel_review_content = models.CharField(max_length=100, verbose_name='리뷰내용')
    hotel_review_rate = models.IntegerField(verbose_name='리뷰평점')
    hotel_review_date = models.DateField(verbose_name='리뷰등록시간')

    id = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'SLHJ_hotel_review'
        verbose_name = '호텔리뷰'
        verbose_name_plural = '호텔예약(들)'

    def __str__(self):
        return self.hotel_review_id


class Hotel_image(models.Model):
    hotel_id = models.OneToOneField(Hotel, primary_key=True, on_delete=models.CASCADE)
    hotel_image_title = models.CharField(max_length=100, verbose_name='파일이름')

    # upload_to=업로드될 경로 (media/ 이하 경로)
    hotel_image_file_path = models.FileField(upload_to="UploadedFiles/", verbose_name='파일경로')
    hotel_image_originname = models.CharField(max_length=100, verbose_name='원본이름')

    class Meta:
        db_table = 'SLHJ_hotel_image'
        verbose_name = '호텔사진'

    def __str__(self):
        return self.hotel_id
