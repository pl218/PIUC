from django.test import TestCase, Client

# Create

class TestView(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("Esta merda vai correr uma vez caralho")

    def setUp(self):
        print("Isto vai correr varias vezes no incio de cada teste, consoante o n de testes.")

    def tearDown(self):
        print("Isto vai correr varias vezes no fim de cada teste, consoante o n de testes.")

    def test_true_is_true(self):
        self.assertEqual(True,True)

    def test_false_is_false(self):
        self.assertEqual(False,False)

    def test_login_view(self):
        client = Client()
        response = client.get('', follow_redirect = True)
        print(response)
        self.assertEqual(response.status_code, 302)
        print(response.content)
        self.assertEqual(response.content, True)
