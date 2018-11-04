from django import forms
from feed.models import Post

class FeedForm(forms.ModelForm):
    title=forms.CharField(required=True)
    post=forms.CharField()

    class Meta:
        model = Post
        fields = (
            'title',
            'post',

        )

class TwitterLoginForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'username',
            'password',
        )