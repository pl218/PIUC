from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView


app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(template_name= "accounts/login.html"), name='login'),
    path('register/', views.register, name='register'),
    path('profile/<slug:username>',views.profile,name='profile'),
    path('logout/',views.logout,name='logout'),
    path('feed/', include('feed.urls')),
    path('search/<slug:input>',views.search, name='search')
]
