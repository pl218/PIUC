from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from feed.forms import FeedForm
from feed.models import Post, Seartweet
from django.contrib.auth.models import User
from searchtweets import ResultStream, gen_rule_payload, load_credentials, collect_results

enterprise_search_args = load_credentials('twitter_keys.yaml', yaml_key='search_tweets_api', env_overwrite=False)

class FeedView(TemplateView):
    template_name= 'feed/feed_page.html'

    def get(self, request):

        form=FeedForm()
        user = request.user
        posts= Seartweet.objects.filter(user_id=user.id)

        auxRule = ''
        auxCount = 1
        for post in posts:
            if 'True' in str(post.check):
                if auxCount == 1:
                    auxRule = post.name
                    auxCount = 2
                else:
                    auxRule = auxRule + ' OR ' + post.name

        tweets = None
        if(auxRule != ''):
            rule = gen_rule_payload(auxRule, results_per_call=100)
            tweets = collect_results(rule, max_results=100, result_stream_args=enterprise_search_args)
        return render(request,self.template_name,{'form': form,'posts': posts,'tweets': tweets})

    def post(self, request):
        form= FeedForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.user= request.user
            post.save();
            return redirect('/feed/mainpage')

        return render(request,self.template_name,{'form':form})

    def favorites(request, username):
        user = User.objects.get(username=username)

        if user.userprofile.favorites.count()>0:
            posts = user.userprofile.favorites.all().order_by('-date')
            return render(request,'feed/fav_page.html',{'user':user ,'posts': posts})
        else:
            return redirect('/feed/mainpage')
