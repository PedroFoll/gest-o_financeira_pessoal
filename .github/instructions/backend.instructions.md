---
description: "Use quando: desenvolver backend com Django, Python ou SQLite. Aplica padrões de arquitetura em camadas (Page Object Pattern adaptado para backend), convenções Django, segurança e boas práticas."
applyTo: "**/*.py"
---

# Padrões de Backend — Django + Python + SQLite

## Arquitetura em Camadas (Page Object Pattern para Backend)

O **Page Object Pattern** adaptado para backend organiza o código em camadas com responsabilidades únicas, da mesma forma que o padrão original abstrai interações de tela. Cada camada é uma "página" do sistema com uma responsabilidade clara:

```
views.py        ← Camada de Apresentação  (recebe request, devolve response)
services.py     ← Camada de Negócio       (regras e lógica da aplicação)
repositories.py ← Camada de Dados         (acesso ao banco — queries isoladas)
models.py       ← Camada de Domínio       (entidades e suas validações)
serializers.py  ← Camada de Contrato      (validação e transformação de dados)
```

### Regra de Dependência
- `views` → chamam `services`
- `services` → chamam `repositories` e `models`
- `repositories` → chamam `models` (ORM)
- **Views nunca acessam o banco diretamente**
- **Services nunca conhecem `request` ou `response`**

---

## Estrutura de Projeto Django

### Organização por Página/Funcionalidade (Page Object Structure)

**Cada tela ou funcionalidade do sistema é uma pasta própria**, contendo todos os seus arquivos relacionados. Isso garante que qualquer alteração — HTML, lógica, rota ou modelo — seja feita em um único lugar previsível.

```
projeto/
├── manage.py
├── config/                        ← configurações globais do projeto
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py                    ← inclui as URLs de cada página
│   └── wsgi.py
│
├── pages/                         ← cada pasta = uma página/funcionalidade
│   │
│   ├── home/                      ← Página inicial
│   │   ├── templates/
│   │   │   └── home.html
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py
│   │   ├── repositories.py
│   │   └── tests.py
│   │
│   ├── produtos/                  ← Funcionalidade: Produtos
│   │   ├── templates/
│   │   │   ├── lista.html
│   │   │   ├── detalhe.html
│   │   │   └── form.html
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py
│   │   ├── repositories.py
│   │   └── tests.py
│   │
│   ├── usuarios/                  ← Funcionalidade: Usuários / Autenticação
│   │   ├── templates/
│   │   │   ├── login.html
│   │   │   ├── cadastro.html
│   │   │   └── perfil.html
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py
│   │   ├── repositories.py
│   │   └── tests.py
│   │
│   └── dashboard/                 ← Funcionalidade: Dashboard
│       ├── templates/
│       │   └── dashboard.html
│       ├── __init__.py
│       ├── views.py
│       ├── urls.py
│       ├── services.py
│       └── tests.py
│
├── static/                        ← arquivos estáticos globais
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/                     ← templates globais (base, partials)
│   ├── base.html
│   └── partials/
│       ├── navbar.html
│       └── footer.html
│
├── requirements.txt
└── .env
```

### Regra de Nomenclatura de Arquivos por Página

Ao criar uma nova tela ou funcionalidade `<nome>`, a estrutura obrigatória é:

```
pages/<nome>/
├── templates/
│   └── <nome>.html        ← template da página
├── __init__.py
├── models.py              ← entidades específicas desta página
├── views.py               ← view que renderiza o template
├── urls.py                ← rotas desta página
├── services.py            ← regras de negócio
├── repositories.py        ← queries ao banco
└── tests.py               ← testes desta página
```

### Registro no config/urls.py

Cada página deve ser incluída no roteador principal:

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',            include('pages.home.urls')),
    path('produtos/',   include('pages.produtos.urls')),
    path('usuarios/',   include('pages.usuarios.urls')),
    path('dashboard/',  include('pages.dashboard.urls')),
]
```

### Registro no settings.py

Cada pasta de página é um app Django e deve ser declarada em `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # apps do Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # páginas do projeto
    'pages.home',
    'pages.produtos',
    'pages.usuarios',
    'pages.dashboard',
]

# Templates: Django encontra templates dentro de cada página
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],   # templates globais (base.html, partials)
    'APP_DIRS': True,                   # encontra templates/ dentro de cada app/página
    ...
}]
```

### Criação de nova página — checklist

Ao criar uma nova tela/funcionalidade, **sempre** seguir esta ordem:

1. Criar a pasta `pages/<nome>/` com todos os arquivos listados acima
2. Criar `pages/<nome>/templates/<nome>.html`
3. Implementar `models.py` → rodar `makemigrations` e `migrate`
4. Implementar `repositories.py`
5. Implementar `services.py`
6. Implementar `views.py`
7. Declarar as URLs em `pages/<nome>/urls.py`
8. Incluir em `config/urls.py`
9. Registrar em `INSTALLED_APPS` no `settings.py`
10. Escrever testes em `tests.py`

---

## Models — Camada de Domínio

- Todo Model deve herdar de `django.db.models.Model`
- Use `verbose_name` e `verbose_name_plural` em todos os Models
- Sempre defina `__str__` retornando uma representação legível
- Use `auto_now_add=True` para `created_at` e `auto_now=True` para `updated_at`
- Prefira `CharField` com `choices` a campos livres para valores enumerados
- Use `on_delete=models.PROTECT` para FKs críticas; `CASCADE` apenas quando fizer sentido semântico
- Nunca coloque lógica de negócio em `save()` — use services

```python
# ✅ Correto
class Produto(models.Model):
    nome = models.CharField(max_length=255, verbose_name='Nome')
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['-created_at']

    def __str__(self):
        return self.nome
```

---

## Repositories — Camada de Dados

- Toda query ao banco deve estar em `repositories.py`, nunca em views ou services
- Métodos devem ser descritivos: `buscar_por_id`, `listar_ativos`, `criar`
- Retorne QuerySets ou instâncias — nunca dicionários crus
- Use `select_related` e `prefetch_related` para evitar N+1

```python
# repositories.py
from .models import Produto

class ProdutoRepository:
    @staticmethod
    def listar_ativos():
        return Produto.objects.filter(ativo=True).order_by('-created_at')

    @staticmethod
    def buscar_por_id(produto_id: int):
        return Produto.objects.filter(pk=produto_id).first()

    @staticmethod
    def criar(dados: dict) -> Produto:
        return Produto.objects.create(**dados)

    @staticmethod
    def atualizar(produto: Produto, dados: dict) -> Produto:
        for campo, valor in dados.items():
            setattr(produto, campo, valor)
        produto.save()
        return produto
```

---

## Services — Camada de Negócio

- Toda regra de negócio fica aqui — nunca em views ou models
- Métodos recebem dados primitivos ou instâncias de Model — nunca `request`
- Levante exceções customizadas para erros de negócio
- Use type hints em todos os métodos públicos

```python
# services.py
from decimal import Decimal
from .repositories import ProdutoRepository

class ProdutoNaoEncontrado(Exception):
    pass

class PrecoInvalido(Exception):
    pass

class ProdutoService:
    @staticmethod
    def listar_produtos():
        return ProdutoRepository.listar_ativos()

    @staticmethod
    def criar_produto(nome: str, preco: Decimal) -> dict:
        if preco <= 0:
            raise PrecoInvalido('O preço deve ser maior que zero.')
        dados = {'nome': nome, 'preco': preco}
        produto = ProdutoRepository.criar(dados)
        return produto

    @staticmethod
    def desativar_produto(produto_id: int):
        produto = ProdutoRepository.buscar_por_id(produto_id)
        if not produto:
            raise ProdutoNaoEncontrado(f'Produto {produto_id} não encontrado.')
        ProdutoRepository.atualizar(produto, {'ativo': False})
```

---

## Views — Camada de Apresentação (Thin Views)

- Views devem ser finas: recebem `request`, delegam ao service, devolvem `response`
- Use `JsonResponse` para APIs simples ou Django REST Framework para APIs complexas
- Trate exceções de negócio e converta em respostas HTTP adequadas
- Use `require_http_methods` ou `@login_required` para proteção de endpoints

```python
# views.py
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .services import ProdutoService, ProdutoNaoEncontrado, PrecoInvalido

@require_http_methods(['GET'])
def listar_produtos(request):
    produtos = ProdutoService.listar_produtos()
    dados = list(produtos.values('id', 'nome', 'preco'))
    return JsonResponse({'produtos': dados})

@require_http_methods(['POST'])
def criar_produto(request):
    try:
        corpo = json.loads(request.body)
        produto = ProdutoService.criar_produto(
            nome=corpo['nome'],
            preco=corpo['preco'],
        )
        return JsonResponse({'id': produto.id, 'nome': produto.nome}, status=201)
    except (KeyError, json.JSONDecodeError):
        return JsonResponse({'erro': 'Dados inválidos.'}, status=400)
    except PrecoInvalido as e:
        return JsonResponse({'erro': str(e)}, status=422)
```

---

## Serializers — Camada de Contrato

- Use serializers para validar entrada e formatar saída de dados
- Nunca confie nos dados do `request.body` sem passar pelo serializer
- Separe serializers de leitura e escrita quando os campos diferem

```python
# serializers.py (com Django REST Framework)
from rest_framework import serializers
from .models import Produto

class ProdutoInputSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=255)
    preco = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)

class ProdutoOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'preco', 'ativo', 'created_at']
```

---

## Segurança

- **Nunca** exponha chaves, senhas ou tokens no código — use variáveis de ambiente (`.env` + `python-decouple`)
- Use `SECRET_KEY` via variável de ambiente em produção
- Sempre use o ORM do Django — **nunca** construa SQL com concatenação de strings (SQL Injection)
- Proteja endpoints com `@login_required` ou permissões DRF
- Desative `DEBUG = True` em produção
- Use `ALLOWED_HOSTS` corretamente
- Habilite `CSRF_COOKIE_SECURE` e `SESSION_COOKIE_SECURE` em produção
- Não versione `.env`, `db.sqlite3`, `*.pyc` ou `__pycache__/` no git

---

## SQLite — Boas Práticas

- Use SQLite apenas para desenvolvimento e projetos pequenos
- Configure no `settings.py`:
  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': BASE_DIR / 'db.sqlite3',
      }
  }
  ```
- Habilite WAL mode para melhor performance concorrente
- Nunca versione `db.sqlite3` — adicione ao `.gitignore`
- Para produção, migre para PostgreSQL

---

## Migrações

- Sempre execute `makemigrations` após alterar models
- Nunca edite arquivos de migração gerados automaticamente
- Use `--name` para nomear migrações descritivamente: `python manage.py makemigrations --name adiciona_campo_ativo`
- Revise migrações antes de aplicar em produção

---

## Testes

- Cada camada deve ter seus próprios testes
- Use `TestCase` do Django para testes com banco de dados
- Use `SimpleTestCase` quando não precisar do banco
- Nomeie testes descritivamente: `test_criar_produto_com_preco_zero_levanta_excecao`
- Siga o padrão **Arrange / Act / Assert**

```python
# tests/test_services.py
from django.test import TestCase
from ..services import ProdutoService, PrecoInvalido

class ProdutoServiceTest(TestCase):
    def test_criar_produto_com_preco_valido(self):
        # Arrange
        nome, preco = 'Produto Teste', 49.90

        # Act
        produto = ProdutoService.criar_produto(nome=nome, preco=preco)

        # Assert
        self.assertEqual(produto.nome, nome)
        self.assertEqual(float(produto.preco), preco)

    def test_criar_produto_com_preco_zero_levanta_excecao(self):
        with self.assertRaises(PrecoInvalido):
            ProdutoService.criar_produto(nome='Produto', preco=0)
```

---

## Python — Convenções

- Siga o PEP 8 para formatação e estilo
- Use type hints em todas as funções e métodos públicos
- Prefira `f-strings` para interpolação de strings
- Use `dataclasses` ou `TypedDict` para transportar dados entre camadas
- Evite `except Exception` genérico — capture exceções específicas
- Prefira `pathlib.Path` a `os.path`
