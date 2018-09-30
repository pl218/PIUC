from django import forms
from accounts.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password')
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

class RegistrationForm(forms.ModelForm):
    # email= forms.EmailField(required=True)
    # ORCID= forms.CharField(max_length=30, required=True)
    # scientific_area=forms.CharField(max_length=30,required=True)
    # image = forms.ImageField(required = True)

    class Meta:
        model = UserProfile
        fields = (
            'first_name',
            'last_name',
            'email',
            'ORCID',
            'scientific_area',
            'image'
        )
