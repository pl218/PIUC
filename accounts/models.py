from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from feed.models import Post


# Create your models here.
class UserProfile(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    description=models.CharField(max_length=500, default='')
    city=models.CharField(max_length=30, default='')
    website=models.URLField(default='')
    ORCID=models.CharField(max_length=30, default='')
    scientific_area=models.CharField(max_length=50, default='')
    confirmed_email=models.BooleanField(default=False)
    favorites = models.ManyToManyField(Post)


@receiver(post_save, sender=User) #Tratamento de Sinais
def update_UserProfile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    #instance.userprofile.save()
