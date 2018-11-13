from django.urls import path, include
from feed import views

app_name = 'feed'
urlpatterns = [
    path('mainpage', views.FeedView.as_view(), name='mainpage'),
    path('favorites/<slug:username>', views.FeedView.favorites, name='favorites'),
    path('loginReddit',views.LoginReddit,name='loginReddit'),
    path('checkReddit',views.checkReddit,name='checkReddit'),
]
