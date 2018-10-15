from django.urls import path, re_path, reverse_lazy
from . import views
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordChangeView,
    PasswordChangeDoneView
)

urlpatterns = [
    path('login/', LoginView.as_view(template_name= "accounts/login.html"), name='login'),
    path('register/', views.register, name='register'),
    path('profile/',views.profile,name='profile'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    #path('reset-password/', PasswordResetView.as_view(template_name= "accounts/reset_password.html", email_template_name= 'accounts/reset_password_email.html'), name='password_reset'),
    #path('reset-password/done/', PasswordResetDoneView.as_view(template_name= "accounts/reset_password_done.html"), name="password_reset_done"),
    #path('reset-password/', PasswordResetView.as_view(template_name='accounts/reset_password.html', email_template_name= 'accounts/reset_password_email.html'), name='reset_password'),
    path('reset-password/', views.PasswordResetView.as_view(template_name='accounts/reset_password.html', email_template_name='accounts/reset_password_email.html'),  name='reset_password'),
    path('password_reset_form', views.PasswordResetForm, name = 'password_reset_form'),
     #url(r'^reset-password/$', password_reset, {'template_name': 'accounts/reset_password.html', 'post_reset_redirect': 'accounts:password_reset_done', 'email_template_name': 'accounts/reset_password_email.html'}, name='reset_password'),

    path('reset-password/done/', PasswordResetDoneView.as_view(template_name='accounts/reset_password_done.html'), name="password_reset_done"),
    path('reset-password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='accounts/reset_password_confirm.html'), name='password_reset_confirm'),
    #path('reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/', PasswordResetConfirmView.as_view(template_name='accounts/reset_password_confirm.html'), name='password_reset_confirm'),

    path('reset-password/complete/', views.PasswordResetCompleteView, name='password_reset_complete')

]
