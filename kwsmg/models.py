from django.db import models

class Complaint_form(models.Model):
    complaint_id = models.IntegerField(primary_key=True)
    complaint_title = models.CharField(max_length=255)
    description = models.TextField()
    accepted = models.BooleanField(default=False)
    gachucount = models.IntegerField()
    category = models.CharField(max_length=255)
    answer = models.TextField(blank=True, null=True)
    created = models.DateTimeField()
    

    class Meta:
        db_table = 'complain_dv'  