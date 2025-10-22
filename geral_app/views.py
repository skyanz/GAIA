# geral_app/views.py
# geral_app/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Case, When, FloatField
from gerador_app.models import Questao, RespostaAluno, Categoria
from django.db.models.functions import Coalesce # Para evitar nulos

@login_required
def dashboard(request):
    # Lógica de dados para o dashboard
    
    # Métrica 1: Qnt. Alunos
    # Conta quantos alunos únicos responderam
    total_alunos = RespostaAluno.objects.values('aluno_id_externo').distinct().count()

    # Métrica 2: Qnt. Questões
    total_questoes = Questao.objects.count()

    # Métrica 3 e 4: Taxa de Acerto e Nota Média
    # Usamos agregação para calcular a média de respostas corretas
    # Coalesce(..., 0.0) garante que se não houver respostas, ele retorna 0 e não None
    agregado = RespostaAluno.objects.aggregate(
        media_acertos=Coalesce(
            Avg(
                Case(When(esta_correta=True, then=1.0), default=0.0, output_field=FloatField())
            ), 
            0.0
        )
    )
    taxa_acerto_geral = agregado['media_acertos'] * 100
    nota_media = agregado['media_acertos'] * 10

    # Gráfico 1: Desempenho por Matéria (Dados para o Chart.js)
    # Agrupamos por Categoria e calculamos a média de acertos de cada uma
    desempenho_materia = Categoria.objects.annotate(
        taxa_acerto=Coalesce(
            Avg(
                Case(When(questoes__respostaaluno__esta_correta=True, then=1.0), default=0.0, output_field=FloatField())
            ),
            0.0
        )
    ).values('nome', 'taxa_acerto')

    # Prepara os dados para o JavaScript
    labels_materia = [item['nome'] for item in desempenho_materia]
    data_materia = [item['taxa_acerto'] * 100 for item in desempenho_materia] # Em porcentagem

    context = {
        'total_alunos': total_alunos,
        'total_questoes': total_questoes,
        'nota_media': round(nota_media, 1), # Arredonda para 1 casa decimal
        'taxa_acerto_geral': round(taxa_acerto_geral, 1),
        
        # Envia os dados do gráfico para o template
        'labels_materia': labels_materia,
        'data_materia': data_materia,
    }
    
    return render(request, 'geral_app/dashboard.html', context)

# ... (outras views) ...

@login_required
def dashboard_aluno(request):
    return render(request, 'geral_app/dashboard_aluno.html')
