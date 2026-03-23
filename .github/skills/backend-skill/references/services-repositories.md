# Referência Services & Repositories — Arquitetura em Camadas

## Repository — Camada de Dados

Toda query ao banco fica aqui. Views e services nunca acessam o ORM diretamente.

```python
# apps/produtos/repositories.py
from typing import Optional
from django.db.models import QuerySet
from .models import Produto, Categoria


class CategoriaRepository:
    @staticmethod
    def listar_todas() -> QuerySet:
        return Categoria.objects.all().order_by('nome')

    @staticmethod
    def buscar_por_id(categoria_id: int) -> Optional[Categoria]:
        return Categoria.objects.filter(pk=categoria_id).first()

    @staticmethod
    def buscar_por_nome(nome: str) -> Optional[Categoria]:
        return Categoria.objects.filter(nome__iexact=nome).first()

    @staticmethod
    def criar(nome: str, descricao: str = '') -> Categoria:
        return Categoria.objects.create(nome=nome, descricao=descricao)


class ProdutoRepository:
    @staticmethod
    def listar_ativos() -> QuerySet:
        return (
            Produto.objects
            .filter(status=Produto.Status.ATIVO)
            .select_related('categoria')  # evita N+1
            .order_by('-created_at')
        )

    @staticmethod
    def listar_por_categoria(categoria_id: int) -> QuerySet:
        return (
            Produto.objects
            .filter(categoria_id=categoria_id, status=Produto.Status.ATIVO)
            .select_related('categoria')
        )

    @staticmethod
    def buscar_por_id(produto_id: int) -> Optional[Produto]:
        return (
            Produto.objects
            .filter(pk=produto_id)
            .select_related('categoria')
            .first()
        )

    @staticmethod
    def criar(dados: dict) -> Produto:
        return Produto.objects.create(**dados)

    @staticmethod
    def atualizar(produto: Produto, dados: dict) -> Produto:
        for campo, valor in dados.items():
            setattr(produto, campo, valor)
        produto.save(update_fields=list(dados.keys()) + ['updated_at'])
        return produto

    @staticmethod
    def deletar(produto: Produto) -> None:
        produto.delete()
```

## Service — Camada de Negócio

Toda regra de negócio fica aqui. Services nunca conhecem `request` ou `response`.

```python
# apps/produtos/services.py
from decimal import Decimal
from typing import Optional
from .models import Produto, Categoria
from .repositories import ProdutoRepository, CategoriaRepository


# === Exceções de negócio ===

class ProdutoNaoEncontrado(Exception):
    pass

class CategoriaNaoEncontrada(Exception):
    pass

class PrecoInvalido(ValueError):
    pass

class EstoqueInsuficiente(Exception):
    pass

class NomeDuplicado(Exception):
    pass


# === Services ===

class CategoriaService:
    @staticmethod
    def listar() -> list:
        return CategoriaRepository.listar_todas()

    @staticmethod
    def criar(nome: str, descricao: str = '') -> Categoria:
        if CategoriaRepository.buscar_por_nome(nome):
            raise NomeDuplicado(f'Categoria "{nome}" já existe.')
        return CategoriaRepository.criar(nome=nome, descricao=descricao)


class ProdutoService:
    @staticmethod
    def listar() -> list:
        return ProdutoRepository.listar_ativos()

    @staticmethod
    def buscar(produto_id: int) -> Produto:
        produto = ProdutoRepository.buscar_por_id(produto_id)
        if not produto:
            raise ProdutoNaoEncontrado(f'Produto {produto_id} não encontrado.')
        return produto

    @staticmethod
    def criar(nome: str, preco: Decimal, categoria_id: int, estoque: int = 0) -> Produto:
        if preco <= 0:
            raise PrecoInvalido('O preço deve ser maior que zero.')
        if estoque < 0:
            raise ValueError('O estoque não pode ser negativo.')

        categoria = CategoriaRepository.buscar_por_id(categoria_id)
        if not categoria:
            raise CategoriaNaoEncontrada(f'Categoria {categoria_id} não encontrada.')

        dados = {
            'nome': nome,
            'preco': preco,
            'categoria': categoria,
            'estoque': estoque,
        }
        return ProdutoRepository.criar(dados)

    @staticmethod
    def atualizar(produto_id: int, **kwargs) -> Produto:
        produto = ProdutoService.buscar(produto_id)

        if 'preco' in kwargs and kwargs['preco'] <= 0:
            raise PrecoInvalido('O preço deve ser maior que zero.')

        return ProdutoRepository.atualizar(produto, kwargs)

    @staticmethod
    def desativar(produto_id: int) -> Produto:
        produto = ProdutoService.buscar(produto_id)
        return ProdutoRepository.atualizar(produto, {'status': Produto.Status.INATIVO})

    @staticmethod
    def baixar_estoque(produto_id: int, quantidade: int) -> Produto:
        produto = ProdutoService.buscar(produto_id)
        if produto.estoque < quantidade:
            raise EstoqueInsuficiente(
                f'Estoque insuficiente. Disponível: {produto.estoque}, solicitado: {quantidade}.'
            )
        novo_estoque = produto.estoque - quantidade
        dados = {'estoque': novo_estoque}
        if novo_estoque == 0:
            dados['status'] = Produto.Status.ESGOTADO
        return ProdutoRepository.atualizar(produto, dados)
```

## Exceções — convenções

```python
# Hierarquia recomendada de exceções customizadas
class BackendError(Exception):
    """Base para todas as exceções da aplicação."""

class RecursoNaoEncontrado(BackendError):
    """Recurso não existe no banco."""

class RegraDeNegocioViolada(BackendError):
    """Operação viola uma regra de negócio."""

class DadosDuplicados(BackendError):
    """Recurso já existe."""

# Mapeamento para HTTP status codes nas views:
# RecursoNaoEncontrado  → 404
# RegraDeNegocioViolada → 422
# DadosDuplicados       → 409
# ValueError            → 400
```
