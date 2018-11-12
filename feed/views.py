from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.conf import settings
from feed.forms import FeedForm
from feed.models import Post
from django.contrib.auth.models import User as UserModel
import praw
from django.utils.datastructures import MultiValueDictKeyError
from twython import Twython

class FeedView(TemplateView):
    template_name= 'feed/feed_page.html'
    def get(self, request):
        RedditPosts=[];
        loggedReddit=False
        user=UserModel.objects.get(username=request.user)
        if(user.userprofile.redditRefreshToken!=None):
            try:
                reddit = praw.Reddit(client_id='rauAoeTRAaxrCQ',
                                        client_secret='Web-2V_CRQJAKXYQY0Qqst1OIRw',
                                        refresh_token=user.userprofile.redditRefreshToken,
                                        user_agent='testing')

                subscribed = list(reddit.user.subreddits(limit=None))
                loggedReddit=True
                for subreddit in subscribed:
                    for submissions in subreddit.new(limit=1):
                        RedditPosts.append(submissions)
            except :
                print("Chave Errada!")
                user.userprofile.redditRefreshToken=None
                user.save()

        form=FeedForm()
        posts= Post.objects.all().order_by('-date')
        return render(request,self.template_name,{'form': form,'posts': posts,'loggedReddit':loggedReddit,'RedditPosts':RedditPosts})

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

def checkReddit(request):
        code = request.GET['code']
        reddit = praw.Reddit(client_id='rauAoeTRAaxrCQ',
                         client_secret='Web-2V_CRQJAKXYQY0Qqst1OIRw',
                         redirect_uri='http://127.0.0.1:8000/feed/checkReddit',
                         user_agent='testing')
        token=reddit.auth.authorize(code)
        user=UserModel.objects.get(username=request.user)
        user.userprofile.redditRefreshToken=token
        user.save()
        return redirect('/feed/mainpage')




def LoginReddit(request):
        reddit = praw.Reddit(client_id='rauAoeTRAaxrCQ',
                         client_secret='Web-2V_CRQJAKXYQY0Qqst1OIRw',
                         redirect_uri='http://127.0.0.1:8000/feed/checkReddit',
                         user_agent='testing')
        return redirect(reddit.auth.url(['identity',
                  'mysubreddits', 'read'], '...', 'permanent'))
