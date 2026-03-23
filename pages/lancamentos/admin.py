from django.contrib import admin
from pages.lancamentos.models import Lancamento, LancamentoRecorrente


@admin.register(Lancamento)
class LancamentoAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'tipo', 'valor', 'data', 'categoria', 'recorrente', 'created_at']
    list_filter = ['tipo', 'categoria', 'data']
    search_fields = ['descricao', 'observacao']
    date_hierarchy = 'data'


@admin.register(LancamentoRecorrente)
class LancamentoRecorrenteAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'tipo', 'valor', 'frequencia', 'dia_vencimento', 'data_inicio', 'data_fim', 'ativo']
    list_filter = ['tipo', 'frequencia', 'ativo']
    search_fields = ['descricao']
    list_editable = ['ativo']
