# gerador_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Página principal do gerador (HTML)
    path('', views.gerador_questoes, name='gerador_questoes'),
    
    # API que fala com o Gemini (chamada pelo JS)
    path('api/gerar/', views.api_gerar_questoes, name='api_gerar_questoes'),
    
    # API que salva no banco (chamada pelo JS)
    path('api/salvar/', views.salvar_e_abrir_quiz, name='api_salvar_quiz'),
    
    # Página do Quiz que o aluno vê (ex: /gerador/quiz/1/)
    path('quiz/<int:avaliacao_id>/', views.exibir_quiz, name='exibir_quiz'),

    # URL que recebe as respostas do aluno
    path('quiz/<int:avaliacao_id>/submeter/', views.submeter_quiz, name='submeter_quiz'),
]