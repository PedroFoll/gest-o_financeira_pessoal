from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from pages.usuarios.forms import CadastroForm
from pages.usuarios.repositories import UsuarioRepository


class UsuarioService:
    """Regras de negócio para autenticação e cadastro."""

    def __init__(self):
        self.repository = UsuarioRepository()

    def fazer_login(self, request, usuario: User) -> None:
        """Registra a sessão do usuário já autenticado pelo LoginForm."""
        login(request, usuario)

    def cadastrar(self, form: CadastroForm) -> User:
        """Persiste o novo usuário via form válido."""
        return form.save()

    def fazer_logout(self, request) -> None:
        logout(request)
