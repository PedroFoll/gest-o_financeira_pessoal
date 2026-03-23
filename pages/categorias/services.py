from pages.categorias.repositories import CategoriaRepository


class CategoriaService:
    """Regras de negócio de Categoria."""

    def __init__(self):
        self.repository = CategoriaRepository()

    def listar(self, incluir_inativas=False):
        if incluir_inativas:
            return CategoriaRepository.listar_todas_incluindo_inativas()
        return CategoriaRepository.listar_todas()

    def obter(self, pk):
        return CategoriaRepository.buscar_por_id(pk)

    def criar(self, form):
        if not form.is_valid():
            raise ValueError('Dados inválidos.')
        return form.save()

    def atualizar(self, pk, form):
        if not form.is_valid():
            raise ValueError('Dados inválidos.')
        instancia = CategoriaRepository.buscar_por_id(pk)
        return CategoriaRepository.atualizar(instancia, form.cleaned_data)

    def deletar(self, pk):
        CategoriaRepository.deletar(pk)
