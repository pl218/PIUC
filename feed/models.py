from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    idpost = models.CharField(max_length=100, default='')
    title = models.CharField(max_length=100)
    post = models.CharField(max_length=1000)
    created_at = models.CharField(max_length=100, default='')
    date= models.DateTimeField(auto_now_add=True) #Creation date

class Seartweet(models.Model):
    name = models.CharField(max_length=100, default='')
    check = models.BooleanField(default=True)
    user_id = models.IntegerField(default=0)
