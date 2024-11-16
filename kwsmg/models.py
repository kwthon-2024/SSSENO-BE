from django.db import models

class Complaint_form(models.Model):
    complaint_id = models.AutoField(primary_key=True)  # primary key를 AutoField로 변경 (일반적으로 이렇게 설정)
    complaint_title = models.CharField(max_length=255)
    description = models.TextField()
    accepted = models.BooleanField(default=False)
    gachucount = models.IntegerField()
    category = models.CharField(max_length=255)
    answer = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)  # 자동으로 현재 시간으로 설정
    

    class Meta:
        db_table = 'complain_dev'