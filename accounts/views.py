from django.shortcuts import render, redirect
from accounts.forms import RegistrationForm
from django.contrib.auth.models import User
from feed.models import Post
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import authenticate, login

# Create your views here.
#def loginPage(request):
#    return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST': #POST -> cliente envia info para o server
        form=RegistrationForm(request.POST)
        if form.is_valid(): #caso todos os dados recebidos sejam válidos
            user=form.save() #guarda os dados basicos do utilizador (username pass...)
            user.refresh_from_db()
            user.userprofile.ORCID= form.cleaned_data.get('ORCID') # cleaned_data para prevenir caso o utilizador introduza dados que possam prejudicar o website
            user.userprofile.scientific_area=form.cleaned_data.get('scientific_area')
            user.save() #guarda os dados adicionais do perfil na bd

            #Entrar na conta após os registo
            username = user.username
            password = form.cleaned_data.get('password1')
            user = authenticate(username= username, password=password)
            login(request,user)
            return redirect('/accounts/profile/'+username)
    else:
        form=RegistrationForm()
    return render(request,'accounts/register.html',{'form':form})

def profile(request, username):
    user = User.objects.get(username=username)
    #return render(request, '<app_name>/user_profile.html', {"user":user})
    return render(request,'accounts/profile.html',{'user': user})

def logout(request):
    return render(request,'accounts/logout.html')

def search(request, input):
    posts = Post.objects.filter(post__contains = input );
    users = User.objects.filter(username__contains = input);
    return render(request,'accounts/search.html', {'posts': posts, 'users': users})    
