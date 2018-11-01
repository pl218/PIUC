from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from feed.models import Post


# Create your models here.
class UserProfile(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    bio=models.CharField(max_length=500, default='')
    city=models.CharField(max_length=30, default='')
    website=models.URLField(default='')
    ORCID=models.CharField(max_length=30, default='')
    researchInterests=models.CharField(max_length=200, default='')
    confirmed_email=models.BooleanField(default=False)
    favorites = models.ManyToManyField(Post)
    profilePic=models.ImageField(default='profile_pics/profile_pic_placeholder.jpg',upload_to='profile_pics/')

@receiver(post_save, sender=User) #Tratamento de Sinais
def update_UserProfile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()


class BookmarksModel(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    urlName=models.CharField(max_length=50)
    url=models.URLField(max_length=150)
    keyword=models.CharField(max_length=100, default='')
