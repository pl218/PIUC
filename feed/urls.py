from django.urls import path, include
from feed import views

app_name = 'feed'
urlpatterns = [
    path('mainpage', views.FeedView.as_view(), name='mainpage'),
]
