# Referência Views & URLs — Django

## View baseada em função (FBV)

```python
# apps/produtos/views.py
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .services import (
    ProdutoService,
    ProdutoNaoEncontrado,
    PrecoInvalido,
    CategoriaNaoEncontrada,
)


def _json_body(request) -> dict:
    """Lê e valida o corpo JSON da request."""
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return None


@require_http_methods(['GET'])
def listar_produtos(request):
    produtos = ProdutoService.listar()
    dados = list(produtos.values('id', 'nome', 'preco', 'estoque', 'status'))
    return JsonResponse({'produtos': dados, 'total': len(dados)})


@require_http_methods(['GET'])
def detalhar_produto(request, produto_id: int):
    try:
        produto = ProdutoService.buscar(produto_id)
        return JsonResponse({
            'id': produto.id,
            'nome': produto.nome,
            'preco': str(produto.preco),
            'estoque': produto.estoque,
            'status': produto.status,
            'categoria': produto.categoria.nome,
        })
    except ProdutoNaoEncontrado as e:
        return JsonResponse({'erro': str(e)}, status=404)


@csrf_exempt
@require_http_methods(['POST'])
def criar_produto(request):
    corpo = _json_body(request)
    if corpo is None:
        return JsonResponse({'erro': 'JSON inválido.'}, status=400)

    campos_obrigatorios = ['nome', 'preco', 'categoria_id']
    faltando = [c for c in campos_obrigatorios if c not in corpo]
    if faltando:
        return JsonResponse({'erro': f'Campos obrigatórios: {faltando}'}, status=400)

    try:
        produto = ProdutoService.criar(
            nome=corpo['nome'],
            preco=corpo['preco'],
            categoria_id=corpo['categoria_id'],
            estoque=corpo.get('estoque', 0),
        )
        return JsonResponse({'id': produto.id, 'nome': produto.nome}, status=201)
    except PrecoInvalido as e:
        return JsonResponse({'erro': str(e)}, status=422)
    except CategoriaNaoEncontrada as e:
        return JsonResponse({'erro': str(e)}, status=404)
    except Exception as e:
        return JsonResponse({'erro': 'Erro interno.'}, status=500)


@csrf_exempt
@require_http_methods(['DELETE'])
def desativar_produto(request, produto_id: int):
    try:
        ProdutoService.desativar(produto_id)
        return JsonResponse({'mensagem': 'Produto desativado com sucesso.'})
    except ProdutoNaoEncontrado as e:
        return JsonResponse({'erro': str(e)}, status=404)
```

## URLs do app

```python
# pages/produtos/urls.py
from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    path('', views.listar_produtos, name='listar'),
    path('<int:produto_id>/', views.detalhar_produto, name='detalhar'),
    path('criar/', views.criar_produto, name='criar'),
    path('<int:produto_id>/desativar/', views.desativar_produto, name='desativar'),
]
```

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

## View com Django REST Framework (DRF)

```python
# apps/produtos/views.py (versão DRF)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProdutoInputSerializer, ProdutoOutputSerializer
from .services import ProdutoService, ProdutoNaoEncontrado, PrecoInvalido


@api_view(['GET'])
def listar_produtos(request):
    produtos = ProdutoService.listar()
    serializer = ProdutoOutputSerializer(produtos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def detalhar_produto(request, produto_id: int):
    try:
        produto = ProdutoService.buscar(produto_id)
        return Response(ProdutoOutputSerializer(produto).data)
    except ProdutoNaoEncontrado as e:
        return Response({'erro': str(e)}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def criar_produto(request):
    serializer = ProdutoInputSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        produto = ProdutoService.criar(**serializer.validated_data)
        return Response(ProdutoOutputSerializer(produto).data, status=status.HTTP_201_CREATED)
    except PrecoInvalido as e:
        return Response({'erro': str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
```

## Serializers DRF

```python
# apps/produtos/serializers.py
from rest_framework import serializers
from .models import Produto


class ProdutoInputSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=255)
    preco = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    categoria_id = serializers.IntegerField(min_value=1)
    estoque = serializers.IntegerField(min_value=0, default=0)


class ProdutoOutputSerializer(serializers.ModelSerializer):
    categoria = serializers.StringRelatedField()

    class Meta:
        model = Produto
        fields = ['id', 'nome', 'preco', 'estoque', 'status', 'categoria', 'created_at']
```

## Decoradores Django úteis

```python
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.views.decorators.cache import cache_page

@login_required                           # exige autenticação
@permission_required('produtos.add_produto')  # exige permissão específica
@require_GET                              # apenas GET
@require_POST                             # apenas POST
@cache_page(60 * 15)                     # cache de 15 minutos
```
