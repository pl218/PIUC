from django.shortcuts import render

def MainFeed(request):
    return render(request,'feed/feed_page.html')
