from django.urls import path
from pages.home import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='index'),
]
