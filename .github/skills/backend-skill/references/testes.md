# Referência Testes — Django TestCase

## Estrutura base — Arrange / Act / Assert

```python
# apps/produtos/tests/test_services.py
from django.test import TestCase
from decimal import Decimal
from ..models import Categoria
from ..services import (
    ProdutoService,
    CategoriaService,
    ProdutoNaoEncontrado,
    PrecoInvalido,
    EstoqueInsuficiente,
)


class ProdutoServiceTest(TestCase):
    def setUp(self):
        """Criado antes de cada teste."""
        self.categoria = Categoria.objects.create(nome='Eletrônicos')

    # --- Testes de criação ---

    def test_criar_produto_com_dados_validos(self):
        # Arrange
        nome, preco, categoria_id = 'Notebook', Decimal('3999.90'), self.categoria.id

        # Act
        produto = ProdutoService.criar(nome=nome, preco=preco, categoria_id=categoria_id)

        # Assert
        self.assertEqual(produto.nome, nome)
        self.assertEqual(produto.preco, preco)
        self.assertEqual(produto.categoria, self.categoria)

    def test_criar_produto_com_preco_zero_levanta_preco_invalido(self):
        with self.assertRaises(PrecoInvalido):
            ProdutoService.criar(nome='Produto', preco=0, categoria_id=self.categoria.id)

    def test_criar_produto_com_preco_negativo_levanta_preco_invalido(self):
        with self.assertRaises(PrecoInvalido):
            ProdutoService.criar(nome='Produto', preco=-10, categoria_id=self.categoria.id)

    def test_criar_produto_com_categoria_inexistente_levanta_excecao(self):
        from ..services import CategoriaNaoEncontrada
        with self.assertRaises(CategoriaNaoEncontrada):
            ProdutoService.criar(nome='Produto', preco=100, categoria_id=9999)

    # --- Testes de busca ---

    def test_buscar_produto_existente_retorna_produto(self):
        # Arrange
        produto = ProdutoService.criar('Mouse', Decimal('99.90'), self.categoria.id)

        # Act
        resultado = ProdutoService.buscar(produto.id)

        # Assert
        self.assertEqual(resultado.id, produto.id)

    def test_buscar_produto_inexistente_levanta_nao_encontrado(self):
        with self.assertRaises(ProdutoNaoEncontrado):
            ProdutoService.buscar(9999)

    # --- Testes de estoque ---

    def test_baixar_estoque_com_quantidade_valida(self):
        # Arrange
        produto = ProdutoService.criar('Teclado', Decimal('199.90'), self.categoria.id, estoque=10)

        # Act
        produto_atualizado = ProdutoService.baixar_estoque(produto.id, 3)

        # Assert
        self.assertEqual(produto_atualizado.estoque, 7)

    def test_baixar_estoque_acima_do_disponivel_levanta_excecao(self):
        produto = ProdutoService.criar('Monitor', Decimal('1299.90'), self.categoria.id, estoque=2)
        with self.assertRaises(EstoqueInsuficiente):
            ProdutoService.baixar_estoque(produto.id, 5)
```

## Testes de Views

```python
# apps/produtos/tests/test_views.py
import json
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Categoria


class ProdutoViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.categoria = Categoria.objects.create(nome='Eletrônicos')

    def test_listar_produtos_retorna_200(self):
        response = self.client.get(reverse('produtos:listar'))
        self.assertEqual(response.status_code, 200)
        dados = json.loads(response.content)
        self.assertIn('produtos', dados)

    def test_criar_produto_com_dados_validos_retorna_201(self):
        payload = {
            'nome': 'Notebook',
            'preco': '3999.90',
            'categoria_id': self.categoria.id,
        }
        response = self.client.post(
            reverse('produtos:criar'),
            data=json.dumps(payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 201)
        dados = json.loads(response.content)
        self.assertIn('id', dados)

    def test_criar_produto_sem_nome_retorna_400(self):
        payload = {'preco': '99.90', 'categoria_id': self.categoria.id}
        response = self.client.post(
            reverse('produtos:criar'),
            data=json.dumps(payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)

    def test_detalhar_produto_inexistente_retorna_404(self):
        response = self.client.get(reverse('produtos:detalhar', args=[9999]))
        self.assertEqual(response.status_code, 404)
```

## Testes de Models

```python
# apps/produtos/tests/test_models.py
from django.test import TestCase
from decimal import Decimal
from ..models import Produto, Categoria


class ProdutoModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome='Teste')

    def test_produto_str_retorna_nome_e_preco(self):
        produto = Produto.objects.create(
            nome='Item Teste',
            preco=Decimal('49.90'),
            categoria=self.categoria,
        )
        self.assertIn('Item Teste', str(produto))

    def test_produto_disponivel_quando_ativo_e_com_estoque(self):
        produto = Produto.objects.create(
            nome='Item',
            preco=Decimal('10.00'),
            categoria=self.categoria,
            estoque=5,
            status=Produto.Status.ATIVO,
        )
        self.assertTrue(produto.disponivel)

    def test_produto_indisponivel_quando_sem_estoque(self):
        produto = Produto.objects.create(
            nome='Item',
            preco=Decimal('10.00'),
            categoria=self.categoria,
            estoque=0,
        )
        self.assertFalse(produto.disponivel)
```

## Fixtures e dados de teste

```python
# Usando fixtures (JSON)
# Crie o arquivo apps/produtos/fixtures/produtos.json e use:
class MeuTestCase(TestCase):
    fixtures = ['produtos.json']

# Usando factory diretamente no setUp (preferível para testes unitários):
class MeuTestCase(TestCase):
    def setUp(self):
        from ..models import Categoria, Produto
        self.categoria = Categoria.objects.create(nome='Cat Teste')
        self.produto = Produto.objects.create(
            nome='Prod Teste',
            preco='99.90',
            categoria=self.categoria,
        )
```

## Mock — simular dependências externas

```python
from unittest.mock import patch, MagicMock
from django.test import TestCase

class ProdutoServiceComMockTest(TestCase):
    @patch('apps.produtos.services.ProdutoRepository.criar')
    def test_criar_produto_chama_repository(self, mock_criar):
        # Arrange
        mock_criar.return_value = MagicMock(id=1, nome='Produto Mock')

        # Act
        from ..services import ProdutoService
        from decimal import Decimal
        from ..models import Categoria
        cat = Categoria.objects.create(nome='Cat')
        ProdutoService.criar('Produto', Decimal('10.00'), cat.id)

        # Assert
        mock_criar.assert_called_once()
```

## Executar testes

```bash
# Todos os testes
python manage.py test

# Testes de um app específico
python manage.py test apps.produtos

# Teste específico
python manage.py test apps.produtos.tests.test_services.ProdutoServiceTest

# Com cobertura (requer coverage)
coverage run manage.py test
coverage report
coverage html
```
