from django import forms
from pages.lancamentos.models import Lancamento, LancamentoRecorrente
from pages.categorias.models import Categoria


class LancamentoForm(forms.ModelForm):
    class Meta:
        model = Lancamento
        fields = ['descricao', 'valor', 'tipo', 'data', 'categoria', 'observacao']
        widgets = {
            'descricao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descrição do lançamento',
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0,00',
                'step': '0.01',
                'min': '0.01',
            }),
            'tipo': forms.RadioSelect(),
            'data': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'observacao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações opcionais...',
            }),
        }
        labels = {
            'descricao': 'Descrição',
            'valor': 'Valor (R$)',
            'tipo': 'Tipo',
            'data': 'Data',
            'categoria': 'Categoria',
            'observacao': 'Observação',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove a opção vazia que o RadioSelect adiciona automaticamente
        self.fields['tipo'].choices = Lancamento.TIPO_CHOICES
        self.fields['categoria'].queryset = Categoria.objects.filter(ativo=True).order_by('nome')
        self.fields['categoria'].empty_label = 'Sem categoria'
        self.fields['categoria'].required = False


class LancamentoRecorrenteForm(forms.ModelForm):
    class Meta:
        model = LancamentoRecorrente
        fields = ['descricao', 'valor', 'tipo', 'frequencia', 'dia_vencimento',
                  'data_inicio', 'data_fim', 'categoria', 'observacao', 'ativo']
        widgets = {
            'descricao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Aluguel, Salário, Netflix...',
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0,00',
                'step': '0.01',
                'min': '0.01',
            }),
            'tipo': forms.RadioSelect(),
            'frequencia': forms.Select(attrs={'class': 'form-select'}),
            'dia_vencimento': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '28',
            }),
            'data_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'observacao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observações opcionais...',
            }),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'descricao': 'Descrição',
            'valor': 'Valor (R$)',
            'tipo': 'Tipo',
            'frequencia': 'Frequência',
            'dia_vencimento': 'Dia de vencimento',
            'data_inicio': 'Início',
            'data_fim': 'Encerramento',
            'categoria': 'Categoria',
            'observacao': 'Observação',
            'ativo': 'Ativo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo'].choices = LancamentoRecorrente.TIPO_CHOICES
        self.fields['categoria'].queryset = Categoria.objects.filter(ativo=True).order_by('nome')
        self.fields['categoria'].empty_label = 'Sem categoria'
        self.fields['categoria'].required = False
        self.fields['data_fim'].required = False
