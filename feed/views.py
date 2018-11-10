from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.conf import settings
from feed.forms import FeedForm
from feed.models import Post
from django.contrib.auth.models import User as UserModel
from twython import Twython
class FeedView(TemplateView):
    template_name= 'feed/feed_page.html'

    def get(self, request):
        
        form=FeedForm()
        posts= Post.objects.all().order_by('-date')
        return render(request,self.template_name,{'form': form,'posts': posts})

    def post(self, request):
        form= FeedForm(request.POST)
        user= request.user
        if not user.userprofile.token:
            print("log in first")
            return redirect('/feed/mainpage')

        twitter = Twython(settings.TOKEN, settings.SECRET, user.userprofile.token, user.userprofile.token_secret)
           
        if form.is_valid():
            post=form.save(commit=False)
            post.user= request.user
            post.save();
            twitter.update_status(status=post.title + " - " + post.post)
            return redirect('/feed/mainpage')

        return render(request,self.template_name,{'form':form})

    def favorites(request, username):
        user = UserModel.objects.get(username=username)
        
        if user.userprofile.favorites.count()>0:
            posts = user.userprofile.favorites.all().order_by('-date')
            return render(request,'feed/fav_page.html',{'user':user ,'posts': posts})
        else:
            return redirect('/feed/mainpage')

