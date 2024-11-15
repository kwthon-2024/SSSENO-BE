from django.db import models

# Create your models here.

class Professor(models.Model):
    Professor_name = models.CharField(max_length=45,default='')
    College = models.CharField(max_length=45,default='')
    Department = models.CharField(max_length=45,default='')
    Description = models.CharField(max_length=45,default='')
    Professor_photo = models.CharField(max_length=45,default='')
    Number = models.CharField(max_length=45,default='')
    Lab = models.CharField(max_length=45,default='')
    Email = models.CharField(max_length=45,default='')
    subject_name1 = models.CharField(max_length=45,default='')
    subject_name2 = models.CharField(max_length=45,default='')
    subject_name3 = models.CharField(max_length=45,default='')

class Reputation(models.Model):
    Professor = models.ForeignKey(Professor, related_name="Reputations", on_delete=models.CASCADE)
    title = models.CharField(max_length=45,default='')
    Description = models.CharField(max_length=45,default='')
    User_ID = models.CharField(max_length=45,default='')
    Reputation1 = models.CharField(max_length=45,default='')
    Reputation2 = models.CharField(max_length=45,default='')
    Reputation3 = models.CharField(max_length=45,default='')
    Reputation4 = models.CharField(max_length=45,default='')
    Reputation5 = models.CharField(max_length=45,default='')

class Repu_static(models.Model):
    professor = models.ForeignKey(Professor, related_name="Repu_statics", on_delete=models.CASCADE)
    static1 = models. IntegerField(default=0)
    static2 = models. IntegerField(default=0)
    static3 = models. IntegerField(default=0)
    static4 = models. IntegerField(default=0)
    static5 = models. IntegerField(default=0)