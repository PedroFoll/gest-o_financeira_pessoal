from django.test import TestCase
from pages.categorias.models import Categoria


class CategoriaModelTest(TestCase):
    def test_criar_categoria(self):
        cat = Categoria.objects.create(nome='Alimentação')
        self.assertEqual(str(cat), 'Alimentação')
        self.assertTrue(cat.ativo)
