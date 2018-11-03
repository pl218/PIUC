from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from feed.forms import FeedForm
from feed.models import Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class FeedView(TemplateView):
    
    @method_decorator(login_required)
    def get(self, request):
        
        form=FeedForm()
        posts= Post.objects.all().order_by('-date')
        return render(request, 'feed/feed_page.html', {'form': form,'posts': posts})

    @method_decorator(login_required)
    def post(self, request):
        form= FeedForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.user= request.user
            post.save()
            return redirect('/feed/mainpage')

        return render(request, 'feed/feed_page.html',{'form':form})

    @method_decorator(login_required)
    def favorites(request, username):
        user = User.objects.get(username=username)
        
        if user.userprofile.favorites.count()>0:
            posts = user.userprofile.favorites.all().order_by('-date')
            return render(request,'feed/fav_page.html',{'user':user ,'posts': posts})
        else:
            return redirect('/feed/mainpage')