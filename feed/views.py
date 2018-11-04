from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from feed.forms import FeedForm
from feed.models import Post
from django.contrib.auth.models import User
from twitter import *

consumer_key= "gXZaakLcHCXoZ9zrtmZGz9gw5"
consumer_secret= "vIlaHSCNQGlvYbfmxri2EzZEHTcQu0PaVqv1wkXaRpSIIEVYTQ"
t = object

class FeedView(TemplateView):
    template_name= 'feed/feed_page.html'

    def get(self, request):
        
        form=FeedForm()
        posts= Post.objects.all().order_by('-date')
        return render(request,self.template_name,{'form': form,'posts': posts})

    def post(self, request):
        form= FeedForm(request.POST)
        try:
            t.t.statuses.home_timeline()
        except:
            return redirect('/feed/TwitterLogIn')

        if form.is_valid():
            post=form.save(commit=False)
            post.user= request.user
            post.save();
            t.statuses.update(status=post.title + " - " + post.post)
            return redirect('/feed/mainpage')

        return render(request,self.template_name,{'form':form})

    def TwitterLogIn(request):
        form= TwitterLoginForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.user= request.user
            post.save();
            t = Twitter(auth=OAuth(token, token_secret, consumer_key, consumer_secret))
            return redirect('/feed/mainpage')
        return render(request,self.template_name,{'form':form})



    def favorites(request, username):
        user = User.objects.get(username=username)
        
        if user.userprofile.favorites.count()>0:
            posts = user.userprofile.favorites.all().order_by('-date')
            return render(request,'feed/fav_page.html',{'user':user ,'posts': posts})
        else:
            return redirect('/feed/mainpage')