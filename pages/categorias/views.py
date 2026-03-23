from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from pages.categorias.forms import CategoriaForm
from pages.categorias.models import Categoria
from pages.categorias.services import CategoriaService


def lista(request):
    service = CategoriaService()
    categorias = service.listar(incluir_inativas=True)
    return render(request, 'categorias/lista.html', {'categorias': categorias})


def nova(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Categoria criada com sucesso.')
                return redirect('categorias:lista')
            except Exception as e:
                messages.error(request, f'Erro ao criar categoria: {e}')
    else:
        form = CategoriaForm()
    return render(request, 'categorias/form.html', {'form': form, 'titulo': 'Nova Categoria'})


def editar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Categoria atualizada com sucesso.')
                return redirect('categorias:lista')
            except Exception as e:
                messages.error(request, f'Erro ao atualizar categoria: {e}')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categorias/form.html', {'form': form, 'titulo': 'Editar Categoria', 'categoria': categoria})


def excluir(request, pk):
    if request.method == 'POST':
        categoria = get_object_or_404(Categoria, pk=pk)
        try:
            categoria.delete()
            messages.success(request, 'Categoria excluída com sucesso.')
        except Exception as e:
            messages.error(request, f'Erro ao excluir categoria: {e}')
    else:
        messages.error(request, 'Método inválido para exclusão de categoria.')
    return redirect('categorias:lista')
