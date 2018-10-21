
from django.shortcuts import render, redirect
from accounts.forms import RegistrationForm, EditProfileForm, EditUserForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import (UserChangeForm, SetPasswordForm)
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.views import (PasswordContextMixin)
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template import loader
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic.base import TemplateView
from django.shortcuts import resolve_url
from django.http import HttpResponseRedirect
from django import forms
from feed.forms import FeedForm
from feed.models import Post
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from searchtweets import ResultStream, gen_rule_payload, load_credentials, collect_results

# Create your views here.
#def loginPage(request):
#    return render(request, 'accounts/login.html')

enterprise_search_args = load_credentials('twitter_keys.yaml', yaml_key='search_tweets_api', env_overwrite=False)

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

def password_reset_complete(request):
    return redirect('../../login')

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
        email = self.cleaned_data["email"]
        try:
            user = User.objects.get(email=email)
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
        form.save(**opts)
        #form.send_mail(opts)


        return super().form_valid(form)

INTERNAL_RESET_URL_TOKEN = 'set-password'
INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'

class PasswordResetConfirmView(PasswordContextMixin, FormView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'accounts/reset_password_confirm.html'
    title = ('Enter new password')
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if token == INTERNAL_RESET_URL_TOKEN:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, INTERNAL_RESET_URL_TOKEN)
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        #try:
            # urlsafe_base64_decode() decodes to bytestring
        UserModel = get_user_model()
        uid = urlsafe_base64_decode(uidb64).decode()
        #user = UserModel._default_manager.get(pk=uid)
        user = User.objects.get(pk=uid)
        print(user)
        #except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, ValidationError):
        #    user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
        else:
            context.update({
                'form': None,
                'title': ('Password reset unsuccessful'),
                'validlink': False,
            })
        return context

def search_tweets(request, input):
    rule = gen_rule_payload(input, results_per_call=100)
    tweets = collect_results(rule, max_results=100, result_stream_args=enterprise_search_args)
    return render(request,'accounts/search_tweets.html', {'tweets': tweets})
