from django.urls import path
from pages.lancamentos import views

app_name = 'lancamentos'

urlpatterns = [
    path('', views.lista, name='lista'),
    path('novo/', views.novo, name='novo'),
    path('<int:pk>/editar/', views.editar, name='editar'),
    path('<int:pk>/excluir/', views.excluir, name='excluir'),
    # Lançamentos recorrentes
    path('recorrentes/', views.recorrentes_lista, name='recorrentes_lista'),
    path('recorrentes/novo/', views.recorrentes_novo, name='recorrentes_novo'),
    path('recorrentes/<int:pk>/editar/', views.recorrentes_editar, name='recorrentes_editar'),
    path('recorrentes/<int:pk>/excluir/', views.recorrentes_excluir, name='recorrentes_excluir'),
]
