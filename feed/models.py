from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) #Many to one (User pode ter vários posts)
    title = models.CharField(max_length=100)
    post = models.CharField(max_length=500)
    date= models.DateTimeField(auto_now_add=True) #Creation date
    Edit_date= models.DateTimeField(auto_now=True) #last edit date
