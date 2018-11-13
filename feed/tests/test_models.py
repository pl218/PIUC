from django.test import TestCase, Client

from django.contrib.auth.models import User
from accounts.models import UserProfile
from feed.models import Post
from django.utils import timezone


class FeedModelsTest(TestCase):

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

    def create_user_for_tests(self):
        user = User.objects.create_user(username='test', email='test@test.com', password='testpassword123', first_name="Test", last_name="Testerino")
        user.ORCID = "1234-1234-1234-1234"
        user.favorites = "Ai"
        user.city = "TestCity"
        user.website = "http://www.google.com"
        user.save()
        return user;

    def create_post_for_tests(self, user, title, post, date, edit_date):
        p = Post.objects.create(user=user, title=title, post=post,date=timezone.now())
        p.full_clean();
        p.save()
        return p


    def test_post_creation(self):
        u = self.create_user_for_tests()
        p = self.create_post_for_tests(u,"adasdasd","teste post", "2000-01-01T00:00:00", "2000-01-02T00:00:00")

    #Passed
    #def test_post_title_empty(self):
        #u = self.create_user_for_tests()
        #p = self.create_post_for_tests(u,"","teste post", "2000-01-01T00:00:00", "2000-01-02T00:00:00")

    #def test_post_post_empty(self):
        #u = self.create_user_for_tests()
        #p = self.create_post_for_tests(u,"asdad","", "2000-01-01T00:00:00", "2000-01-02T00:00:00")

    def test_post_title_empty_space(self):
        u = self.create_user_for_tests()
        p = self.create_post_for_tests(u,"  ","teste post", "2000-01-01T00:00:00", "2000-01-02T00:00:00")
        self.assertTrue(p.title,startswith=" ")
