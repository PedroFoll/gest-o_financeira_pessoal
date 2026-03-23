from django import forms
from pages.categorias.models import Categoria


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'cor', 'icone', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da categoria'}),
            'cor': forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color'}),
            'icone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: bi-tag'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nome': 'Nome',
            'cor': 'Cor',
            'icone': 'Ícone (Bootstrap Icons)',
            'ativo': 'Ativa',
        }
