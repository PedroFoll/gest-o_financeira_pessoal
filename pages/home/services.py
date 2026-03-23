import json
from datetime import date
from pages.home.repositories import HomeRepository
from pages.lancamentos.repositories import LancamentoRepository
from pages.lancamentos.models import Lancamento

_MESES_PT = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
              'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']


class HomeService:
    """Regras de negócio da home."""

    def __init__(self):
        self.repository = HomeRepository()

    def obter_contexto(self) -> dict:
        hoje = date.today()
        ano = hoje.year
        mes_atual = hoje.month

        # Totais do mês corrente
        total_receitas = LancamentoRepository.total_por_tipo(
            Lancamento.TIPO_RECEITA,
            data_inicio=date(ano, mes_atual, 1),
            data_fim=hoje,
        )
        total_despesas = LancamentoRepository.total_por_tipo(
            Lancamento.TIPO_DESPESA,
            data_inicio=date(ano, mes_atual, 1),
            data_fim=hoje,
        )
        total_saldo = total_receitas - total_despesas

        # Últimos 5 lançamentos
        ultimos_lancamentos = list(LancamentoRepository.ultimos(5))

        # últimos 6 meses (inclusive o atual)
        meses_seq = []
        for i in range(5, -1, -1):
            m = mes_atual - i
            a = ano
            if m <= 0:
                m += 12
                a -= 1
            meses_seq.append((a, m))

        dados_mensais = []
        for a, m in meses_seq:
            dados_mensais += LancamentoRepository.totais_mensais_por_tipo(a, [m])

        total_mov = dados_mensais[-1]['movimentacoes'] if dados_mensais else 0

        # Objeto JSON para o dashboard.js
        dados_dashboard = {
            'receitas': float(total_receitas),
            'despesas': float(total_despesas),
            'saldo': float(total_saldo),
            'movimentacoes': total_mov,
            'metaMensal': 6000.0,
            'meses': [_MESES_PT[d['mes'] - 1] for d in dados_mensais],
            'receitasMensais': [d['receitas'] for d in dados_mensais],
            'despesasMensais': [d['despesas'] for d in dados_mensais],
            'movMensais': [d['movimentacoes'] for d in dados_mensais],
            'lancamentos': [
                {
                    'descricao': l.descricao,
                    'tipo': l.tipo.lower(),
                    'valor': float(l.valor),
                    'data': l.data.strftime('%d/%m'),
                    'categoria': l.categoria.nome if l.categoria else '',
                }
                for l in ultimos_lancamentos
            ],
        }

        return {
            'total_receitas': total_receitas,
            'total_despesas': total_despesas,
            'total_saldo': total_saldo,
            'total_mov': total_mov,
            'ultimos_lancamentos': ultimos_lancamentos,
            'dados_dashboard_json': json.dumps(dados_dashboard),
        }


