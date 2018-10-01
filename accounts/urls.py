from django.urls import path, re_path
from . import views
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    path('login/', LoginView.as_view(template_name= "accounts/login.html"), name='login'),
    path('register/', views.register, name='register'),
    path('profile/',views.profile,name='profile'),
    #path('reset-password/', PasswordResetView.as_view(template_name= "accounts/reset_password.html", email_template_name= 'accounts/reset_password_email.html'), name='password_reset'),
    #path('reset-password/done/', PasswordResetDoneView.as_view(template_name= "accounts/reset_password_done.html"), name="password_reset_done"),
    #path('reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/', PasswordResetConfirmView.as_view(template_name= 'accounts/reset_password_confirm.html'), name='password_reset_confirm'),
#    path('reset-password/complete/', PasswordResetCompleteView.as_view(template_name='accounts/reset_password_complete.html'), name='password_reset_complete')
    path('reset-password/', PasswordResetView.as_view(), name='password_reset'),
    path('reset-password/done/', PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset-password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete')

]
