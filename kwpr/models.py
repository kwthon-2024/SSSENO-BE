from django.db import models

class Info(models.Model):
    professor = models.CharField(max_length=45)
    college = models.CharField(max_length=45)
    department = models.CharField(max_length=45)
    description = models.CharField(max_length=45, blank=True, null=True)
    photo = models.CharField(max_length=45, blank=True, null=True)
    number = models.CharField(max_length=45, blank=True, null=True)
    lab = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)
    subject1 = models.CharField(max_length=45, blank=True, null=True)
    subject2 = models.CharField(max_length=45, blank=True, null=True)
    subject3 = models.CharField(max_length=45, blank=True, null=True)
    repu1 = models.IntegerField(default=0)
    repu2 = models.IntegerField(default=0)
    repu3 = models.IntegerField(default=0)
    repu4 = models.IntegerField(default=0)
    repu5 = models.IntegerField(default=0)
    count = models.IntegerField(default=0)

    class Meta:
        db_table = 'info'