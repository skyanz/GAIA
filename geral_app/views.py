# geral_app/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # Futuramente, você buscará os dados do banco de dados aqui.
    # Exemplo: context = {'total_alunos': 57, 'total_questoes': 120}
    context = {} # Por enquanto, deixaremos o contexto vazio
    return render(request, 'geral_app/dashboard.html', context)

@login_required
def dashboard_aluno(request):
    return render(request, 'geral_app/dashboard_aluno.html')
