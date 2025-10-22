from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def alunos_view(request: HttpRequest) -> HttpResponse:
    """
    Renderiza a página de alunos com uma lista de dados de exemplo.
    """
    
    # Dados de exemplo que seriam do seu banco de dados
    alunos = [
        {'id': 1, 'nome': 'Ana Silva', 'turma': '3ºEM', 'desempenho':76.5 , 'questoes_respondidas': 90, 'corretas': 85},
        {'id': 2, 'nome': 'Bruno Costa', 'turma': '3ºEM', 'desempenho': 92, 'questoes_respondidas': 100, 'corretas': 92},
        {'id': 3, 'nome': 'Carla Dias', 'turma': '3ºEM', 'desempenho': 70.2, 'questoes_respondidas': 90, 'corretas': 78},
        {'id': 4, 'nome': 'Daniel Martins', 'turma': '3ºEM', 'desempenho': 60, 'questoes_respondidas': 40, 'corretas': 24},
        {'id': 5, 'nome': 'Eduarda Faria', 'turma': '2ºEM', 'desempenho': 95, 'questoes_respondidas': 45, 'corretas': 40},
        {'id': 6, 'nome': 'Felipe Souza', 'turma': '2ºEM', 'desempenho': 88, 'questoes_respondidas': 10, 'corretas': 5},
        {'id': 7, 'nome': 'Gabriela Lima', 'turma': '1ºEM', 'desempenho': 71, 'questoes_respondidas': 30, 'corretas': 3},
    ]
    
    context = {
        'alunos': alunos,
        'turmas': ['3º A', '3º B', '3º C'], # Para o filtro de turmas
    }
    
    # CORREÇÃO: Alteramos o caminho para 'alunos.html'.
    # O Django irá procurar este arquivo dentro de 'alunos_app/templates/'.
    # O caminho completo esperado no seu projeto é: alunos_app/templates/alunos.html
    return render(request, 'alunos.html', context)

