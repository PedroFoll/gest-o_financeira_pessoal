from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from pages.usuarios.forms import CadastroForm, LoginForm
from pages.usuarios.services import UsuarioService


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home:index')

    # Preserva o `next` para redirecionar após login bem-sucedido
    next_url = request.POST.get('next') or request.GET.get('next', '')

    form = LoginForm(request, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        service = UsuarioService()
        service.fazer_login(request, form.get_user())
        messages.success(request, f'Bem-vindo, {form.get_user().username}!')

        # Valida o next para evitar open redirect
        if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            next_url = reverse('home:index')

        return redirect(next_url or reverse('home:index'))

    return render(request, 'usuarios/login.html', {'form': form, 'next': next_url})


def cadastro_view(request):
    if request.user.is_authenticated:
        return redirect('home:index')

    form = CadastroForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        service = UsuarioService()
        service.cadastrar(form)
        messages.success(request, 'Conta criada com sucesso! Faça login para continuar.')
        return redirect('usuarios:login')

    return render(request, 'usuarios/cadastro.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        service = UsuarioService()
        service.fazer_logout(request)
        messages.info(request, 'Você saiu do sistema.')
    return redirect('usuarios:login')
