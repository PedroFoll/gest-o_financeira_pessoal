from decimal import Decimal
from django.db.models import Sum, Count, Q
from pages.lancamentos.models import Lancamento, LancamentoRecorrente


class LancamentoRepository:
    """Camada de acesso a dados de Lançamento."""

    @staticmethod
    def listar_todos(tipo=None, categoria_id=None, data_inicio=None, data_fim=None):
        qs = Lancamento.objects.select_related('categoria').all()
        if tipo:
            qs = qs.filter(tipo=tipo)
        if categoria_id:
            qs = qs.filter(categoria_id=categoria_id)
        if data_inicio:
            qs = qs.filter(data__gte=data_inicio)
        if data_fim:
            qs = qs.filter(data__lte=data_fim)
        return qs

    @staticmethod
    def buscar_por_id(pk):
        return Lancamento.objects.select_related('categoria').get(pk=pk)

    @staticmethod
    def criar(dados):
        return Lancamento.objects.create(**dados)

    @staticmethod
    def atualizar(instancia, dados):
        for campo, valor in dados.items():
            setattr(instancia, campo, valor)
        instancia.save()
        return instancia

    @staticmethod
    def deletar(pk):
        Lancamento.objects.filter(pk=pk).delete()

    @staticmethod
    def total_por_tipo(tipo, data_inicio=None, data_fim=None):
        qs = Lancamento.objects.filter(tipo=tipo)
        if data_inicio:
            qs = qs.filter(data__gte=data_inicio)
        if data_fim:
            qs = qs.filter(data__lte=data_fim)
        resultado = qs.aggregate(total=Sum('valor'))
        return resultado['total'] or Decimal('0.00')

    @staticmethod
    def ultimos(quantidade=5):
        return Lancamento.objects.select_related('categoria').order_by('-data', '-created_at')[:quantidade]

    @staticmethod
    def totais_mensais_por_tipo(ano, meses):
        """Retorna totais mensais de receita e despesa para o intervalo de meses fornecido."""
        resultado = []
        for mes in meses:
            receitas = Lancamento.objects.filter(
                tipo=Lancamento.TIPO_RECEITA,
                data__year=ano,
                data__month=mes,
            ).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')

            despesas = Lancamento.objects.filter(
                tipo=Lancamento.TIPO_DESPESA,
                data__year=ano,
                data__month=mes,
            ).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')

            movimentacoes = Lancamento.objects.filter(
                data__year=ano, data__month=mes
            ).aggregate(total=Count('id'))['total'] or 0

            resultado.append({
                'mes': mes,
                'receitas': float(receitas),
                'despesas': float(despesas),
                'movimentacoes': movimentacoes,
            })
        return resultado


class LancamentoRecorrenteRepository:
    """Camada de acesso a dados de LancamentoRecorrente."""

    @staticmethod
    def listar_todos():
        return LancamentoRecorrente.objects.select_related('categoria').all()

    @staticmethod
    def listar_ativos():
        return LancamentoRecorrente.objects.select_related('categoria').filter(ativo=True)

    @staticmethod
    def buscar_por_id(pk):
        return LancamentoRecorrente.objects.select_related('categoria').get(pk=pk)

    @staticmethod
    def deletar(pk):
        LancamentoRecorrente.objects.filter(pk=pk).delete()

    @staticmethod
    def ja_gerado_no_mes(recorrente_id, ano, mes):
        return Lancamento.objects.filter(
            recorrente_id=recorrente_id,
            data__year=ano,
            data__month=mes,
        ).exists()

    @staticmethod
    def ja_gerado_na_data(recorrente_id, data):
        return Lancamento.objects.filter(
            recorrente_id=recorrente_id,
            data=data,
        ).exists()
