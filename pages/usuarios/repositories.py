from django.contrib.auth.models import User


class UsuarioRepository:
    """Camada de acesso a dados para o modelo User do Django."""

    @staticmethod
    def criar(username: str, email: str, password: str) -> User:
        return User.objects.create_user(username=username, email=email, password=password)

    @staticmethod
    def buscar_por_username(username: str) -> User | None:
        return User.objects.filter(username=username).first()

    @staticmethod
    def existe_username(username: str) -> bool:
        return User.objects.filter(username=username).exists()
