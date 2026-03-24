from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario = User.objects.create_user(username='teste', password='Senha@123')
        self.client.force_login(self.usuario)

    def test_home_retorna_200(self):
        resposta = self.client.get(reverse('home:index'))
        self.assertEqual(resposta.status_code, 200)

    def test_home_usa_template_correto(self):
        resposta = self.client.get(reverse('home:index'))
        self.assertTemplateUsed(resposta, 'home/home.html')

    def test_home_sem_login_redireciona_para_login(self):
        self.client.logout()
        resposta = self.client.get(reverse('home:index'))
        self.assertRedirects(resposta, '/usuarios/login/?next=/')
