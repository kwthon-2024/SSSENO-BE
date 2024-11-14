from django.db import models

class classroom_inf(models.Model):
    db_table = 'classroom_inf'
    capacity = models.IntegerField()
    reserved_time = models.DateTimeField()
    place_name = models.CharField(max_length=100)
    image_id = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    has_mic = models.BooleanField()
    has_projector = models.CharField(max_length=50)
    building_name = models.CharField(max_length=100)
    description = models.TextField()
    reserved = models.BooleanField()
    desk_type = models.CharField(max_length=50)
    rating = models.FloatField()

class classroom_review(models.Model):
    db_table = 'classroom_review'
    mic_status = models.DecimalField(max_digits=3, decimal_places=1)  # 0~5점으로 평가
    clean_status = models.DecimalField(max_digits=3, decimal_places=1)
    air_conditioner_status = models.DecimalField(max_digits=3, decimal_places=1)
    size_satisfaction = models.DecimalField(max_digits=3, decimal_places=1)
    user_id = models.IntegerField()  # 사용자의 ID (기타 정보는 User 모델로 관리 가능)
    place_name = models.CharField(max_length=100)
    building_name = models.CharField(max_length=100)



