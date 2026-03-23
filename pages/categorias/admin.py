from django.contrib import admin
from pages.categorias.models import Categoria


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cor', 'icone', 'ativo', 'created_at']
    list_filter = ['ativo']
    search_fields = ['nome']
    list_editable = ['ativo']
