from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from pages.categorias.models import Categoria


class LancamentoRecorrente(models.Model):
    TIPO_RECEITA = 'RECEITA'
    TIPO_DESPESA = 'DESPESA'
    TIPO_CHOICES = [
        (TIPO_RECEITA, 'Receita'),
        (TIPO_DESPESA, 'Despesa'),
    ]

    FREQ_SEMANAL = 'SEMANAL'
    FREQ_QUINZENAL = 'QUINZENAL'
    FREQ_MENSAL = 'MENSAL'
    FREQ_ANUAL = 'ANUAL'
    FREQ_CHOICES = [
        (FREQ_SEMANAL, 'Semanal'),
        (FREQ_QUINZENAL, 'Quinzenal'),
        (FREQ_MENSAL, 'Mensal'),
        (FREQ_ANUAL, 'Anual'),
    ]

    descricao = models.CharField(max_length=200, verbose_name='Descrição')
    valor = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Valor')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, verbose_name='Tipo')
    frequencia = models.CharField(max_length=10, choices=FREQ_CHOICES, default=FREQ_MENSAL, verbose_name='Frequência')
    dia_vencimento = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(28)],
        verbose_name='Dia de vencimento',
        help_text='Dia do mês (1–28). Usado para frequências Mensal e Anual.',
    )
    data_inicio = models.DateField(verbose_name='Data de início')
    data_fim = models.DateField(null=True, blank=True, verbose_name='Data de encerramento')
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recorrentes',
        verbose_name='Categoria',
    )
    observacao = models.TextField(blank=True, default='', verbose_name='Observação')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Lançamento Recorrente'
        verbose_name_plural = 'Lançamentos Recorrentes'
        ordering = ['descricao']

    def __str__(self):
        return f'{self.get_tipo_display()} — {self.descricao} ({self.get_frequencia_display()})'


class Lancamento(models.Model):
    TIPO_RECEITA = 'RECEITA'
    TIPO_DESPESA = 'DESPESA'
    TIPO_CHOICES = [
        (TIPO_RECEITA, 'Receita'),
        (TIPO_DESPESA, 'Despesa'),
    ]

    descricao = models.CharField(max_length=200, verbose_name='Descrição')
    valor = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Valor')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, verbose_name='Tipo')
    data = models.DateField(verbose_name='Data')
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lancamentos',
        verbose_name='Categoria',
    )
    observacao = models.TextField(blank=True, default='', verbose_name='Observação')
    recorrente = models.ForeignKey(
        LancamentoRecorrente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lancamentos_gerados',
        verbose_name='Recorrente',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Lançamento'
        verbose_name_plural = 'Lançamentos'
        ordering = ['-data', '-created_at']

    def __str__(self):
        return f'{self.get_tipo_display()} — {self.descricao} ({self.valor})'
