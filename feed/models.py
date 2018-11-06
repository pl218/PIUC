from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    idpost = models.CharField(max_length=100, default='')
    user = models.ForeignKey(User,on_delete=models.CASCADE) #Many to one (User pode ter vários posts)
    title = models.CharField(max_length=100)
    post = models.CharField(max_length=1000)
    created_at = models.CharField(max_length=100, default='')
    date= models.DateTimeField(auto_now_add=True) #Creation date

class Seartweet(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='')
    check = models.BooleanField(default=True)
