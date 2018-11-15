from django import forms
from feed.models import Post

class FeedForm(forms.ModelForm):
    title=forms.CharField()
    post=forms.CharField(required=True)

    class Meta:
        model = Post
        fields = (
            'title',
            'post',

        )
