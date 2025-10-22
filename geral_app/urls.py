# geral_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard_aluno', views.dashboard_aluno, name='dashboard_aluno'),
]