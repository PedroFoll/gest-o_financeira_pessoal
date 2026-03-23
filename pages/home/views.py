from django.shortcuts import render
from pages.home.services import HomeService


def home(request):
    service = HomeService()
    contexto = service.obter_contexto()
    return render(request, 'home/home.html', contexto)
