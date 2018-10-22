from django import forms
from accounts.models import UserProfile, BookmarksModel
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
import re

class RegistrationForm(UserCreationForm):
    first_name=forms.CharField(max_length=30, required=True)
    last_name=forms.CharField(max_length=30, required=True)
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

    def clean_email(self): #Verifica se o email já existe
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email

    def clean_first_name(self): #Verifica se o nome possui numeros
        first_name=self.cleaned_data['first_name']
        regex=re.compile('\d')
        if regex.search(first_name):
            raise forms.ValidationError('First name cannot have numbers')
        return first_name

    def clean_last_name(self): #Verifica se o nome possui numeros
        last_name=self.cleaned_data['last_name']
        regex=re.compile('\d')
        if regex.search(last_name):
            raise forms.ValidationError('Last name cannot have numbers')
        return last_name

    def clean_ORCID(self): #Verifica se o ORCID é válido
        ORCID=self.cleaned_data['ORCID']
        regex=re.compile('(\d{4})-(\d{4})-(\d{4})-(\d{3}[0-9X])$')
        if regex.search(ORCID) is None:
            raise forms.ValidationError('Please use a valid ORCID! Ex: 0001-0003-0002-0009')
        if UserProfile.objects.filter(ORCID=ORCID).exists():
            raise forms.ValidationError('ORCID already used!')
        return ORCID

class EditUserForm(ModelForm):
    class Meta:
        model=User
        fields=(
            'email',
        )
    def clean_email(self): #Verifica se o email já existe
        email = self.cleaned_data['email']
        print(self.instance.email)
        if User.objects.filter(email=email).exists() and email != self.instance.email:
            raise forms.ValidationError('Email already exists')
        return email

class EditProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields =(
            'description',
            'city',
            'website',
            'scientific_area',
        )

class BookmarksForm(ModelForm):
    url=forms.URLField(required=True);

    class Meta:
        model = BookmarksModel
        fields = (
            'urlName',
            'url',
            'keyword',
        )
