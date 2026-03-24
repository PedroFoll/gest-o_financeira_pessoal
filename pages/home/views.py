from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from pages.home.services import HomeService


@login_required
def home(request):
    service = HomeService()
    contexto = service.obter_contexto()
    return render(request, 'home/home.html', contexto)
