from django.urls import path, include
from feed import views

app_name = 'feed'
urlpatterns = [
    #path('accounts/', include('accounts.urls')),
    path('mainpage', views.FeedView.as_view(), name='mainpage'),
    path('favorites/<slug:username>', views.FeedView.favorites, name='favorites'),
]
