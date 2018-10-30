from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from accounts.models import UserProfile

class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
           
    def create_user_profile(self):
        user = User.objects.create_user(username='john', email='test@test.com', password='testpassword123', first_name="Test", last_name="Testrino")
        user.save()
        user.ORCID="1234-1234-1234-1234"
        user.favorites="Ai"
        user.description="Tests&Tests"
        user.city="Testlandia"
        user.website="http://www.google.com"
        user.save()
        return user

    #Profile view tests
    #if anyone can access the user's profiles even if not logged in
    def test_view_url_accessible_by_name(self):
        user = self.create_user_profile()
        response = self.client.get('/accounts/profile/john')
        self.assertEquals(response.status_code, 200)
        pass

    def test_profile_page_contains_correct_template(self):
        user = self.create_user_profile()
        response = self.client.get('/accounts/profile/john')
        self.assertTemplateUsed(response, 'accounts/profile.html')


    def test_profile_page_contains_html_for_research_interests(self):
        user = self.create_user_profile()
        response = self.client.get('/accounts/profile/john')
        self.assertContains(response, f'<li class="user_desc"> Research Interests</li>')

    def test_profile_page_contains_htlm_for_ORCID(self):
        user = self.create_user_profile()
        response = self.client.get('/accounts/profile/john')
        self.assertContains(response, f'<li class="user_desc"> ORCID</li>')

    def test_profile_page_contains_htlm_for_username(self):
        user = self.create_user_profile()
        response = self.client.get('/accounts/profile/john')
        self.assertContains(response, f'<div id="user_info">')


    #Register view tests if not logged in
    def test_register_has_correct_status_code_if_not_logged_in(self):
        response = self.client.get('/accounts/register')
        self.assertEquals(response.status_code, 200)
    

    def test_register_contains_correct_template_if_not_logged_in(self):
        response = self.client.get('/accounts/register')
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_register_contains_correct_html_if_not_logged_in(self):
        response = self.client.get('/accounts/register')
        self.assertContains(response, f'<div id="register_form">')
    

    #Register view tests if logged in
    def test_register_has_correct_status_code_if_logged_in(self):
        user = User.objects.create_user('test', 'test@test.com', 'testpassowrd123')
        user.save()
        logged = self.client.login(username='test', password='testpassowrd123')
        response = self.client.get('/accounts/register')
        self.assertEquals(response.status_code, 302)

    #the redirection of the register page if logged in should be to feed page
    def test_register_contains_correct_template_if_logged_in(self):
        user = User.objects.create_user('test', 'test@test.com', 'testpassowrd123')
        user.save()
        logged = self.client.login(username='test', password='testpassowrd123')
        response = self.client.get('/accounts/register', follow=True)
        self.assertTemplateUsed(response, 'feed/feed_page.html')


    #Logout views tests
    #if not logged in the logout should redirect to login
    def test_logout_has_correct_status_code_if_not_logged_in(self):
        response = self.client.get('/accounts/logout')
        self.assertEquals(response.status_code, 302)

    def test_logout_contains_correct_template_if_not_logged_in(self):
        response = self.client.get('/accounts/logout', follow=True)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_register_contains_correct_html_if_not_logged_in(self):
        response = self.client.get('/accounts/register')
        self.assertContains(response, f'<div id="login_para">')
    
    #Logout view tests if logged in
    def test_register_has_correct_status_code_if_logged_in(self):
        user = User.objects.create_user('test', 'test@test.com', 'testpassowrd123')
        user.save()
        logged = self.client.login(username='test', password='testpassowrd123')
        response = self.client.get('/accounts/logout')
        self.assertEquals(response.status_code, 200)

    def test_register_contains_correct_template_if_logged_in(self):
        user = User.objects.create_user('test', 'test@test.com', 'testpassowrd123')
        user.save()
        logged = self.client.login(username='test', password='testpassowrd123')
        response = self.client.get('/accounts/logout')
        self.assertTemplateUsed(response, 'feed/logout.html')
    
    def test_logout_contains_correct_html_if_logged_in(self):
        user = User.objects.create_user('test', 'test@test.com', 'testpassowrd123')
        user.save()
        logged = self.client.login(username='test', password='testpassowrd123')
        response = self.client.get('/accounts/logout')
        self.assertContains(response, f'<h1>Logged out</h1>')
    

