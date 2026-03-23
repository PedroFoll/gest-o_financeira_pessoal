import calendar
from datetime import date, timedelta
from decimal import Decimal
from pages.lancamentos.repositories import LancamentoRepository, LancamentoRecorrenteRepository
from pages.lancamentos.models import Lancamento, LancamentoRecorrente


def _dia_seguro_no_mes(ano, mes, dia):
    """Retorna o dia no mês, limitado ao último dia válido."""
    ultimo = calendar.monthrange(ano, mes)[1]
    return date(ano, mes, min(dia, ultimo))


def _meses_entre(inicio, fim):
    """Yields (ano, mes) de inicio até fim inclusive."""
    ano, mes = inicio.year, inicio.month
    while (ano, mes) <= (fim.year, fim.month):
        yield ano, mes
        mes += 1
        if mes > 12:
            mes = 1
            ano += 1


class LancamentoService:
    """Regras de negócio de Lançamento."""

    def __init__(self):
        self.repository = LancamentoRepository()

    def listar(self, tipo=None, categoria_id=None, data_inicio=None, data_fim=None):
        return LancamentoRepository.listar_todos(
            tipo=tipo,
            categoria_id=categoria_id,
            data_inicio=data_inicio,
            data_fim=data_fim,
        )

    def obter(self, pk):
        return LancamentoRepository.buscar_por_id(pk)

    def criar(self, form):
        if not form.is_valid():
            raise ValueError('Dados inválidos.')
        return form.save()

    def atualizar(self, pk, form):
        if not form.is_valid():
            raise ValueError('Dados inválidos.')
        instancia = LancamentoRepository.buscar_por_id(pk)
        dados = form.cleaned_data
        return LancamentoRepository.atualizar(instancia, dados)

    def deletar(self, pk):
        LancamentoRepository.deletar(pk)

    def calcular_saldo(self, data_inicio=None, data_fim=None):
        receitas = LancamentoRepository.total_por_tipo(
            Lancamento.TIPO_RECEITA, data_inicio, data_fim
        )
        despesas = LancamentoRepository.total_por_tipo(
            Lancamento.TIPO_DESPESA, data_inicio, data_fim
        )
        return receitas - despesas


class LancamentoRecorrenteService:
    """Regras de negócio de lançamentos recorrentes."""

    def listar(self):
        return LancamentoRecorrenteRepository.listar_todos()

    def obter(self, pk):
        return LancamentoRecorrenteRepository.buscar_por_id(pk)

    def criar(self, form):
        if not form.is_valid():
            raise ValueError('Dados inválidos.')
        return form.save()

    def atualizar(self, pk, form):
        if not form.is_valid():
            raise ValueError('Dados inválidos.')
        return form.save()

    def deletar(self, pk):
        LancamentoRecorrenteRepository.deletar(pk)

    def gerar_pendentes(self):
        """
        Gera lançamentos ainda não criados para todos os recorrentes ativos.
        Retorna a quantidade de lançamentos criados.
        """
        hoje = date.today()
        total_gerados = 0

        for rec in LancamentoRecorrenteRepository.listar_ativos():
            limite = min(rec.data_fim, hoje) if rec.data_fim else hoje
            if rec.data_inicio > limite:
                continue
            total_gerados += self._gerar_para(rec, limite)

        return total_gerados

    def _gerar_para(self, rec, limite):
        total = 0
        f = rec.frequencia

        if f == LancamentoRecorrente.FREQ_MENSAL:
            for ano, mes in _meses_entre(rec.data_inicio, limite):
                if not LancamentoRecorrenteRepository.ja_gerado_no_mes(rec.pk, ano, mes):
                    data = _dia_seguro_no_mes(ano, mes, rec.dia_vencimento)
                    if rec.data_inicio <= data <= limite:
                        Lancamento.objects.create(
                            descricao=rec.descricao, valor=rec.valor, tipo=rec.tipo,
                            data=data, categoria=rec.categoria,
                            observacao=rec.observacao, recorrente=rec,
                        )
                        total += 1

        elif f == LancamentoRecorrente.FREQ_ANUAL:
            ano = rec.data_inicio.year
            while True:
                data = _dia_seguro_no_mes(ano, rec.data_inicio.month, rec.dia_vencimento)
                if data > limite:
                    break
                if data >= rec.data_inicio and not LancamentoRecorrenteRepository.ja_gerado_no_mes(
                    rec.pk, ano, rec.data_inicio.month
                ):
                    Lancamento.objects.create(
                        descricao=rec.descricao, valor=rec.valor, tipo=rec.tipo,
                        data=data, categoria=rec.categoria,
                        observacao=rec.observacao, recorrente=rec,
                    )
                    total += 1
                ano += 1

        elif f in (LancamentoRecorrente.FREQ_SEMANAL, LancamentoRecorrente.FREQ_QUINZENAL):
            intervalo = 7 if f == LancamentoRecorrente.FREQ_SEMANAL else 15
            data = rec.data_inicio
            while data <= limite:
                if not LancamentoRecorrenteRepository.ja_gerado_na_data(rec.pk, data):
                    Lancamento.objects.create(
                        descricao=rec.descricao, valor=rec.valor, tipo=rec.tipo,
                        data=data, categoria=rec.categoria,
                        observacao=rec.observacao, recorrente=rec,
                    )
                    total += 1
                data += timedelta(days=intervalo)

        return total
