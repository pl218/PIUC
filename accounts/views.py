from django.shortcuts import render, redirect
from accounts.forms import RegistrationForm, EditProfileForm, EditUserForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import (UserChangeForm)
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import (PasswordContextMixin)
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail, EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template import loader
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic.base import TemplateView
from django.shortcuts import resolve_url
from django import forms
from feed.forms import FeedForm
from feed.models import Post


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
    idd = user.id
    posts = []
    for post in Post.objects.all():
        if post.user_id == idd:
            posts.append(post)
    #return render(request, '<app_name>/user_profile.html', {"user":user})
    return render(request,'accounts/profile.html',{'user': user, 'posts': posts})

def logout(request):
    return render(request,'accounts/logout.html')

def search(request, input):
    posts = Post.objects.filter(post__contains = input );
    users = User.objects.filter(username__contains = input);
    return render(request,'accounts/search.html', {'posts': posts, 'users': users})

def help(request):
    #user = User.objects.get(username=username)
    return render(request,'accounts/help.html')

def edit_profile(request,username):
    user= User.objects.get(username=username)
    if request.method == 'POST':
        formProfile=EditProfileForm(request.POST,instance=request.user.userprofile)
        formUser=EditUserForm(request.POST,instance=request.user)

        if formProfile.is_valid() and formUser.is_valid() :
            postUser=formUser.save();
            postProfile=formProfile.save(commit=False)
            postProfile.user= request.user
            postProfile.save();

            return redirect('/accounts/profile/'+username)
    else:
        formProfile=EditProfileForm(instance=request.user.userprofile)
        formUser=EditUserForm(instance=request.user)
    return render(request,'accounts/profileEdit.html',{'formUser':formUser,'formProfile':formProfile})

def favorite(request,username,id):
    posts = Post.objects.all().order_by('-date')
    user = User.objects.get(username=username)
    post = Post.objects.get(id=id)
    if post in user.userprofile.favorites.all():
        user.userprofile.favorites.remove(post)
    else:
        user.userprofile.favorites.add(post)

    user.save()

    return render(request,'feed/feed_page.html',{'user': user,'posts': posts})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('accounts:view_profile'))
        else:
            return redirect(reverse('accounts:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=("Email"), max_length=254)

    def send_maill(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        active_users = UserModel._default_manager.filter(**{
            '%s__iexact' % UserModel.get_email_field_name(): email,
        })
        return (u for u in active_users if u.has_usable_password())

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        send_mail('ANTES DO PRIMERIO', user, 'OI', ['DSADASDASDASDSADSADSADS'])
        email = self.cleaned_data["email"]
        #user = self.get_users(email);
        #userna = User.objects.filter(email=email).values('username')
        send_mail('PRIMEIRO', user, 'OI', ['DSADASDASDASDSADSADSADS'])
        try:
            send_mail('SEGUNDO', user, 'OI', ['DSADASDASDASDSADSADSADS'])
            user = User.objects.get(email=email)
            send_mail('TERCEIRO', user, 'OI', ['DSADASDASDASDSADSADSADS'])
            context = {
                'email': email,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'user': user,
                'domain': get_current_site(request).domain,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
            }
            self.send_maill(
                subject_template_name, email_template_name, context, from_email,
                email, html_email_template_name=html_email_template_name,
            )
        except:
            return



class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = 'accounts/reset_password_email.html'
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')

    template_name = 'registration/password_reset_form.html'
    title = ('Password reset')
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        send_mail('PasswordResetView', 'user', 'OI', ['DSADASDASDASDSADSADSADS'])
        form.save(**opts)
        #form.send_mail(opts)


        return super().form_valid(form)


def PasswordResetCompleteView(request):
    return redirect('../../login')
