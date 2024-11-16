from django.db import models

class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    birthday = models.CharField(max_length=10)  # 생일을 문자열로 저장
    gubun = models.CharField(max_length=50)
    code_name1 = models.CharField(max_length=100)
    sex = models.CharField(max_length=10)
    hakbun = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class UserAuthentication(models.Model):
    name = models.CharField(max_length=100)
    birthday = models.CharField(max_length=6)
    gubun = models.CharField(max_length=50, null=True, blank=True)
    codeName1 = models.CharField(max_length=50, null=True, blank=True)
    sex = models.CharField(max_length=10, null=True, blank=True)
    hakbun = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name
