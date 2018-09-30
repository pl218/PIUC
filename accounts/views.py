from django.shortcuts import render, redirect
from accounts.forms import RegistrationForm
from accounts.forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.shortcuts import render_to_response


# Create your views here.
#def loginPage(request):
#    return render(request, 'accounts/login.html')

def register(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST': #POST -> cliente envia info para o server
        user_form = UserForm(data=request.POST)
        profile_form=RegistrationForm(data=request.POST)
        if profile_form.is_valid() and user_form.is_valid(): #caso todos os dados recebidos sejam válidos
            print("xupamos")
            user=user_form.save() #guarda os dados basicos do utilizador (username pass...)
            user.set_password(user.password)
            #user.refresh_from_db()
            user.save()
            profile = profile_form.save()
            profile.ORCID= form.cleaned_data.get('ORCID') # cleaned_data para prevenir caso o utilizador introduza dados que possam prejudicar o website
            profile.scientific_area=form.cleaned_data.get('scientific_area')
            profile.image = request.FILES['image']
            profile.save() #guarda os dados adicionar do perfil na bd
            registered = True
            #Entrar na conta após os registo
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username= username, password=password)
            login(request,user)
            return redirect('/accounts/profile')
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form=RegistrationForm()
        return render_to_response(
            'accounts/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def profile(request):
    return render(request,'accounts/profile.html',{'user': request.user})
