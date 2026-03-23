from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome')
    cor = models.CharField(max_length=7, default='#D1A7E2', verbose_name='Cor')
    icone = models.CharField(max_length=50, default='bi-tag', verbose_name='Ícone')
    ativo = models.BooleanField(default=True, verbose_name='Ativa')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

    def __str__(self):
        return self.nome
