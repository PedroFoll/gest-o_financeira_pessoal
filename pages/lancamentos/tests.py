from django.test import TestCase
from decimal import Decimal
from django.utils import timezone
from pages.lancamentos.models import Lancamento


class LancamentoModelTest(TestCase):
    def test_criar_receita(self):
        lanc = Lancamento.objects.create(
            descricao='Salário',
            valor=Decimal('5000.00'),
            tipo=Lancamento.TIPO_RECEITA,
            data=timezone.now().date(),
        )
        self.assertEqual(lanc.tipo, 'RECEITA')
        self.assertEqual(str(lanc), 'Receita — Salário (5000.00)')
