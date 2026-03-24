from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario = User.objects.create_user(username='teste', password='Senha@123')
        self.url_login = reverse('usuarios:login')

    def test_get_retorna_200(self):
        resposta = self.client.get(self.url_login)
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, 'usuarios/login.html')

    def test_login_valido_redireciona_para_home(self):
        resposta = self.client.post(self.url_login, {
            'username': 'teste',
            'password': 'Senha@123',
        })
        self.assertRedirects(resposta, reverse('home:index'))

    def test_login_invalido_retorna_200_com_erro(self):
        resposta = self.client.post(self.url_login, {
            'username': 'teste',
            'password': 'senhaerrada',
        })
        self.assertEqual(resposta.status_code, 200)
        self.assertTrue(resposta.context['form'].non_field_errors())

    def test_usuario_autenticado_redireciona_sem_mostrar_login(self):
        self.client.force_login(self.usuario)
        resposta = self.client.get(self.url_login)
        self.assertRedirects(resposta, reverse('home:index'))


class CadastroViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url_cadastro = reverse('usuarios:cadastro')

    def test_get_retorna_200(self):
        resposta = self.client.get(self.url_cadastro)
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, 'usuarios/cadastro.html')

    def test_cadastro_valido_redireciona_para_login(self):
        resposta = self.client.post(self.url_cadastro, {
            'username': 'novousuario',
            'email': 'novo@email.com',
            'password1': 'Senh@Segura123',
            'password2': 'Senh@Segura123',
        })
        self.assertRedirects(resposta, reverse('usuarios:login'))
        self.assertTrue(User.objects.filter(username='novousuario').exists())

    def test_cadastro_senhas_diferentes_retorna_erro(self):
        resposta = self.client.post(self.url_cadastro, {
            'username': 'novousuario',
            'email': 'novo@email.com',
            'password1': 'Senh@Segura123',
            'password2': 'SenhaDiferente',
        })
        self.assertEqual(resposta.status_code, 200)


class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario = User.objects.create_user(username='teste', password='Senha@123')
        self.url_logout = reverse('usuarios:logout')

    def test_logout_post_redireciona_para_login(self):
        self.client.force_login(self.usuario)
        resposta = self.client.post(self.url_logout)
        self.assertRedirects(resposta, reverse('usuarios:login'))
