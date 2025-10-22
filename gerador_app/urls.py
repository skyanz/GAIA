# gerador_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.gerador_questoes, name='gerador_questoes'),
    path('quiz/', views.quiz, name='quiz'),
]