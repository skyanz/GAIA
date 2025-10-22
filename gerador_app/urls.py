# gerador_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Supondo que você tenha uma view para o gerador
    # path('', views.gerador_questoes, name='gerador_questoes'), 
    
    # URLs do Quiz
    path('quiz/', views.exibir_quiz, name='exibir_quiz'),
    path('quiz/submeter/', views.submeter_quiz, name='submeter_quiz'),
]