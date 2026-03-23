from pages.categorias.models import Categoria


class CategoriaRepository:
    """Camada de acesso a dados de Categoria."""

    @staticmethod
    def listar_todas():
        return Categoria.objects.filter(ativo=True).order_by('nome')

    @staticmethod
    def listar_todas_incluindo_inativas():
        return Categoria.objects.all().order_by('nome')

    @staticmethod
    def buscar_por_id(pk):
        return Categoria.objects.get(pk=pk)

    @staticmethod
    def criar(dados):
        return Categoria.objects.create(**dados)

    @staticmethod
    def atualizar(instancia, dados):
        for campo, valor in dados.items():
            setattr(instancia, campo, valor)
        instancia.save()
        return instancia

    @staticmethod
    def deletar(pk):
        Categoria.objects.filter(pk=pk).delete()
