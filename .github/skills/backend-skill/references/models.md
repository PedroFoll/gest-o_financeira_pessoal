# Referência Models — Django ORM

## Model completo com boas práticas

```python
# apps/produtos/models.py
from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome', unique=True)
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Produto(models.Model):
    class Status(models.TextChoices):
        ATIVO = 'ativo', 'Ativo'
        INATIVO = 'inativo', 'Inativo'
        ESGOTADO = 'esgotado', 'Esgotado'

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='produtos',
        verbose_name='Categoria',
    )
    nome = models.CharField(max_length=255, verbose_name='Nome')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')
    estoque = models.PositiveIntegerField(default=0, verbose_name='Estoque')
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ATIVO,
        verbose_name='Status',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['categoria', 'status']),
        ]

    def __str__(self):
        return f'{self.nome} (R$ {self.preco})'

    @property
    def disponivel(self) -> bool:
        return self.status == self.Status.ATIVO and self.estoque > 0
```

## Tipos de campos mais usados

```python
# Texto
models.CharField(max_length=255)           # texto curto
models.TextField()                          # texto longo
models.SlugField()                          # slug para URLs

# Números
models.IntegerField()
models.PositiveIntegerField()
models.DecimalField(max_digits=10, decimal_places=2)
models.FloatField()

# Datas
models.DateField()
models.DateTimeField()
models.DateTimeField(auto_now_add=True)    # criação
models.DateTimeField(auto_now=True)        # atualização

# Booleano
models.BooleanField(default=True)

# Relações
models.ForeignKey(Modelo, on_delete=models.PROTECT)    # N:1
models.ManyToManyField(Modelo)                          # N:N
models.OneToOneField(Modelo, on_delete=models.CASCADE) # 1:1

# Arquivo
models.FileField(upload_to='uploads/')
models.ImageField(upload_to='imagens/')

# Email / URL
models.EmailField()
models.URLField()
```

## on_delete — quando usar cada opção

| Opção | Quando usar |
|-------|-------------|
| `PROTECT` | FK para dados críticos — impede exclusão acidental |
| `CASCADE` | FK onde o filho sem pai não faz sentido (ex: itens de pedido) |
| `SET_NULL` | FK opcional — o registro filho pode existir sem o pai |
| `SET_DEFAULT` | FK com valor padrão quando o pai é excluído |
| `DO_NOTHING` | Raro — quando a integridade é gerenciada externamente |

## Signals (use com moderação)

```python
# Use signals apenas para efeitos colaterais desacoplados
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Produto

@receiver(post_save, sender=Produto)
def notificar_estoque_zerado(sender, instance, **kwargs):
    if instance.estoque == 0 and instance.status != Produto.Status.ESGOTADO:
        # lógica de notificação
        pass
```

## Admin

```python
# apps/produtos/admin.py
from django.contrib import admin
from .models import Produto, Categoria

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'preco', 'status', 'estoque', 'created_at']
    list_filter = ['status', 'categoria']
    search_fields = ['nome', 'descricao']
    list_editable = ['status', 'estoque']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'created_at']
    search_fields = ['nome']
```
