from django.db import models

class ClassroomInfDev(models.Model):
    capacity = models.IntegerField(null=True, blank=True)
    capacity_max = models.IntegerField(null=True, blank=True) # 수정필요
    reserved_time = models.DateTimeField(null=True, blank=True)
    place_name = models.CharField(max_length=100, null=True, blank=True) 
    image_id = models.CharField(max_length=50, null=True, blank=True) 
    type = models.CharField(max_length=50, null=True, blank=True)
    has_mic = models.BooleanField(null=True, blank=True)
    has_projector = models.BooleanField(max_length=50, null=True, blank=True)
    building_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    reserved = models.BooleanField(null=True, blank=True)
    desk_type = models.CharField(max_length=50, null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = 'classroom_inf_dev'  

class ClassroomReviewDev(models.Model):
    mic_status = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)  
    clean_status = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    air_conditioner_status = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    size_satisfaction = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    user_id = models.IntegerField()  
    place_name = models.CharField(max_length=100, null=True, blank=True)
    building_name = models.CharField(max_length=100, null=True, blank=True)
    #rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    class Meta:
        db_table = 'classroom_review_dev'  
