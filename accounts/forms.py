from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    email= forms.EmailField(required=True)
    ORCID= forms.CharField(max_length=30, required=True)
    scientific_area=forms.CharField(max_length=30,required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'ORCID',
            'scientific_area',
            'password1',
            'password2',
        )
