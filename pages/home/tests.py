from django.test import TestCase, Client
from django.urls import reverse


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_retorna_200(self):
        resposta = self.client.get(reverse('home:index'))
        self.assertEqual(resposta.status_code, 200)

    def test_home_usa_template_correto(self):
        resposta = self.client.get(reverse('home:index'))
        self.assertTemplateUsed(resposta, 'home/home.html')
