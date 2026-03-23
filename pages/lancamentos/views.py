from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from pages.lancamentos.forms import LancamentoForm, LancamentoRecorrenteForm
from pages.lancamentos.models import Lancamento, LancamentoRecorrente
from pages.lancamentos.services import LancamentoService, LancamentoRecorrenteService
from pages.categorias.models import Categoria


def lista(request):
    # Gera automaticamente quaisquer lançamentos recorrentes pendentes
    gerados = LancamentoRecorrenteService().gerar_pendentes()
    if gerados:
        messages.info(request, f'{gerados} lançamento(s) recorrente(s) gerado(s) automaticamente.')

    service = LancamentoService()

    tipo = request.GET.get('tipo', '')
    categoria_id = request.GET.get('categoria', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    lancamentos = service.listar(
        tipo=tipo or None,
        categoria_id=categoria_id or None,
        data_inicio=data_inicio or None,
        data_fim=data_fim or None,
    )

    categorias = Categoria.objects.filter(ativo=True).order_by('nome')

    contexto = {
        'lancamentos': lancamentos,
        'categorias': categorias,
        'filtro_tipo': tipo,
        'filtro_categoria': categoria_id,
        'filtro_data_inicio': data_inicio,
        'filtro_data_fim': data_fim,
    }
    return render(request, 'lancamentos/lista.html', contexto)


def novo(request):
    if request.method == 'POST':
        form = LancamentoForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Lançamento criado com sucesso.')
                return redirect('lancamentos:lista')
            except Exception as e:
                messages.error(request, f'Erro ao criar lançamento: {e}')
    else:
        form = LancamentoForm()
    return render(request, 'lancamentos/form.html', {'form': form, 'titulo': 'Novo Lançamento'})


def editar(request, pk):
    lancamento = get_object_or_404(Lancamento, pk=pk)
    if request.method == 'POST':
        form = LancamentoForm(request.POST, instance=lancamento)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Lançamento atualizado com sucesso.')
                return redirect('lancamentos:lista')
            except Exception as e:
                messages.error(request, f'Erro ao atualizar lançamento: {e}')
    else:
        form = LancamentoForm(instance=lancamento)
    return render(request, 'lancamentos/form.html', {
        'form': form,
        'titulo': 'Editar Lançamento',
        'lancamento': lancamento,
    })


def excluir(request, pk):
    if request.method == 'POST':
        lancamento = get_object_or_404(Lancamento, pk=pk)
        try:
            lancamento.delete()
            messages.success(request, 'Lançamento excluído com sucesso.')
        except Exception as e:
            messages.error(request, f'Erro ao excluir lançamento: {e}')
        return redirect('lancamentos:lista')
    else:
        messages.error(request, 'Método inválido para exclusão de lançamento.')
        return redirect('lancamentos:lista')


# =====================================================
# VIEWS — LANÇAMENTOS RECORRENTES
# =====================================================

def recorrentes_lista(request):
    service = LancamentoRecorrenteService()
    recorrentes = service.listar()
    return render(request, 'lancamentos/recorrentes_lista.html', {'recorrentes': recorrentes})


def recorrentes_novo(request):
    if request.method == 'POST':
        form = LancamentoRecorrenteForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Lançamento recorrente criado com sucesso.')
                return redirect('lancamentos:recorrentes_lista')
            except Exception as e:
                messages.error(request, f'Erro ao criar lançamento recorrente: {e}')
    else:
        form = LancamentoRecorrenteForm()
    return render(request, 'lancamentos/recorrentes_form.html', {
        'form': form,
        'titulo': 'Novo Lançamento Recorrente',
    })


def recorrentes_editar(request, pk):
    recorrente = get_object_or_404(LancamentoRecorrente, pk=pk)
    if request.method == 'POST':
        form = LancamentoRecorrenteForm(request.POST, instance=recorrente)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Lançamento recorrente atualizado com sucesso.')
                return redirect('lancamentos:recorrentes_lista')
            except Exception as e:
                messages.error(request, f'Erro ao atualizar lançamento recorrente: {e}')
    else:
        form = LancamentoRecorrenteForm(instance=recorrente)
    return render(request, 'lancamentos/recorrentes_form.html', {
        'form': form,
        'titulo': 'Editar Lançamento Recorrente',
        'recorrente': recorrente,
    })


def recorrentes_excluir(request, pk):
    if request.method == 'POST':
        recorrente = get_object_or_404(LancamentoRecorrente, pk=pk)
        try:
            recorrente.delete()
            messages.success(request, 'Lançamento recorrente excluído com sucesso.')
        except Exception as e:
            messages.error(request, f'Erro ao excluir lançamento recorrente: {e}')
        return redirect('lancamentos:recorrentes_lista')
    else:
        messages.error(request, 'Método inválido para exclusão de lançamento.')
        return redirect('lancamentos:recorrentes_lista')

