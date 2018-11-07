from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from feed.forms import FeedForm
from feed.models import Post
from django.contrib.auth.models import User
from django.conf import settings
from twitter import *
import oauth2 as oauth
import cgi

consumer = oauth.Consumer(settings.TWITTER_TOKEN, settings.TWITTER_SECRET)
client = oauth.Client(consumer)

request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'
authenticate_url = 'https://api.twitter.com/oauth/authenticate'

class FeedView(TemplateView):
    template_name= 'feed/feed_page.html'

    def get(self, request):
        
        form=FeedForm()
        posts= Post.objects.all().order_by('-date')
        return render(request,self.template_name,{'form': form,'posts': posts})

    def post(self, request, username):
        form= FeedForm(request.POST)
        user= request.user
        t = Twitter(user.token, user.token_secret,consumer_key,consumer_secret)
        if not user.token:
            #print "log in first"
            return redirect('/feed/mainpage')

        if form.is_valid():
            post=form.save(commit=False)
            post.user= request.user
            post.save();
            t.statuses.update(status=post.title + " - " + post.post)
            return redirect('/feed/mainpage')

        return render(request,self.template_name,{'form':form})

    
    def TwitterSignIn(request, username):
        user = request.user   

        token = oauth.Token(request.session['request_token']['oauth_token'],request.session['request_token']['oauth_token_secret'])
        client = oauth.Client(consumer, token)
        resp, content = client.request(access_token_url, "GET")
        if resp['status'] != '200':
            raise Exception("Invalid response from Twitter.")

        access_token = dict(cgi.parse_qsl(content))

        user.token = access_token['oauth_token']
        user.token_secret = access_token['oauth_token_secret']
        profile.save()


        user = authenticate(username=access_token['screen_name'],password=access_token['oauth_token_secret'])

        auth_login(request, user)

    def favorites(request, username):
        user = User.objects.get(username=username)
        
        if user.userprofile.favorites.count()>0:
            posts = user.userprofile.favorites.all().order_by('-date')
            return render(request,'feed/fav_page.html',{'user':user ,'posts': posts})
        else:
            return redirect('/feed/mainpage')