from django.urls import path, include
from . import views
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetCompleteView
)
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(template_name= "accounts/login.html"), name='login'),
    path('register/', views.register, name='register'),
    path('profile/<slug:username>',views.profile,name='profile'),
    path('profile/edit/<slug:username>',views.edit_profile,name='edit_profile'),
    path('logout/',views.logout, name='logout'),
    path('feed/', include('feed.urls')),
    path('search/<slug:input>',views.search, name='search'),
    path('help/',views.help, name='help'),
    path('favorite/<slug:username><slug:id>', views.favorite, name='favorite'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('reset-password/', views.PasswordResetView.as_view(template_name='accounts/reset_password.html', email_template_name='accounts/reset_password_email.html'),  name='reset_password'),
    path('password_reset_form/', views.PasswordResetForm, name = 'password_reset_form'),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name='accounts/reset_password_done.html'), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password/complete/', views.password_reset_complete, name='password_reset_complete')
]
