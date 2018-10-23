from django.test import TestCase, Client
from django.contrib.auth.models import User

class HomePageTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        #print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        #print("setUp: Run once for every test method to setup clean data.")
        pass

    def tearDown(self):
        #print("tearDown: Run once for every test method to restore to initial state, in this case TestCase already cleans the db.")        
        pass

    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 302)

    def test_view_uses_correct_template(self):
        response = self.client.get('/', follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_home_page_contains_correct_html(self):
        response = self.client.get('/', follow=True)
        self.assertContains(response, f'id="login_form"')

    def test_home_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/', follow=True)
        self.assertNotContains(
            response, 'Hi there! I should not be on the page.')

    def test_view_uses_correct_template_after_login(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.save()
        logged = self.client.login(username='john', password='johnpassword')
        response = self.client.get('/', follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed/feed_page.html')

    def test_home_page_contains_correct_html_after_login(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.save()
        logged = self.client.login(username='john', password='johnpassword')
        response = self.client.get('/', follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, f'div id="feed_cont"')

    def test_home_page_does_not_contain_incorrect_html_after_login(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.save()
        logged = self.client.login(username='john', password='johnpassword')
        response = self.client.get('/', follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertNotContains(
            response, f'id="login_form"')