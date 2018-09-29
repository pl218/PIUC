from django.urls import path
from feed import views

urlpatterns = [
    path('', views.FeedView.as_view(), name='FeedView'),
]
