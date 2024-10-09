from django.db import models

# Create your models here.
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    age = models.IntegerField()
    genderf = models.IntegerField()
    genderm = models.IntegerField()
    size = models.IntegerField()
    pp = models.IntegerField()
    pm = models.IntegerField()
    fp = models.IntegerField()