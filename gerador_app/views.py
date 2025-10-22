# gerador_app/views.py
import google.generativeai as genai
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.http import require_POST

# Importe seus NOVOS models
from .models import Questao, Avaliacao, RespostaAluno
from geral_app.models import Categoria, Turma

# --- VIEW 1: A PÁGINA DO GERADOR (O HTML) ---
@login_required
def gerador_questoes(request):
    """
    Renderiza seu 'gerador.html' e passa as Turmas do professor para o template.
    """
    try:
        # Busca as turmas associadas ao perfil do professor logado
        turmas_professor = request.user.profile.turmas.all()
    except Exception:
        # Se for admin ou não tiver perfil, mostra todas as turmas
        turmas_professor = Turma.objects.all() 
        
    context = {
        'turmas': turmas_professor
    }
    return render(request, 'gerador_app/gerador.html', context)

# --- VIEW 2: A API QUE FALA COM O GEMINI (A SUA VIEW) ---
@login_required
@require_POST # Esta view só aceita POST
def api_gerar_questoes(request):
    """
    Esta é a sua view original. Ela é chamada pelo seu 'gerador.js' (via FormData).
    Ela NÃO renderiza HTML, apenas retorna JSON para o JavaScript.
    """
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Seu 'gerador.js' envia FormData, então usamos request.POST
        num_questoes = request.POST.get('num_questoes', '5')
        dificuldade = request.POST.get('dificuldade', 'Média')
        materias = [m for m in [
            request.POST.get('materia1'),
            request.POST.get('materia2'),
            request.POST.get('materia3')
        ] if m]
        detalhes = request.POST.get('detalhes', '')
        
        prompt = f"""
        Aja como um especialista em criar provas de matemática.
        Sua única saída deve ser um objeto JSON. Não inclua a palavra "json" ou ``` no início ou no fim.
        Crie um array JSON contendo {num_questoes} objetos. Cada objeto deve representar uma questão de múltipla escolha
        com dificuldade {dificuldade} sobre os seguintes tópicos: {', '.join(materias)}.
        {f"Leve em consideração os seguintes detalhes: {detalhes}" if detalhes else ""}

        Para CADA questão, atribua um "topico" baseado na lista de tópicos fornecida (ex: "Geometria", "Estatística").

        O formato de cada objeto no array JSON deve ser exatamente o seguinte:
        {{
          "topico": "Geometria", 
          "questao": "Texto da pergunta aqui.",
          "opcoes": {{ "A": "...", "B": "...", "C": "...", "D": "..." }},
          "resposta_correta": "B"
        }}
        """
        generation_config = genai.types.GenerationConfig(response_mime_type="application/json")
        response = model.generate_content(prompt, generation_config=generation_config)
        
        questoes_json = json.loads(response.text)
        # Retorna o JSON exato que o seu 'gerador.js' espera
        return JsonResponse({'questoes': questoes_json})

    except Exception as e:
        return JsonResponse({'error': f'Ocorreu um erro ao gerar as questões: {str(e)}'}, status=500)

# --- VIEW 3: A NOVA VIEW QUE SALVA NO BANCO ---
@login_required
@require_POST
def salvar_e_abrir_quiz(request):
    """
    Chamada pelo 'gerador.js' DEPOIS que a IA gerou as questões.
    Recebe o JSON e salva tudo no banco de dados.
    """
    try:
        # Esta view espera JSON, não FormData
        data = json.loads(request.body)
        questoes_json = data.get('questoes')
        turma_id = data.get('turma_id')
        titulo_avaliacao = data.get('titulo_avaliacao', 'Avaliação Gerada')
        dificuldade_str = data.get('dificuldade', 'Média') # Pega a dificuldade
        
        if not questoes_json or not turma_id:
            return JsonResponse({'error': 'Dados incompletos (questões ou turma).'}, status=400)

        turma = get_object_or_404(Turma, id=turma_id)
        
        nova_avaliacao = Avaliacao.objects.create(
            titulo=titulo_avaliacao,
            turma=turma,
            professor=request.user
        )

        questoes_para_adicionar = []
        dificuldade_map = {'Fácil': 'F', 'Média': 'M', 'Difícil': 'D'}
        dificuldade_char = dificuldade_map.get(dificuldade_str, 'M')

        for q_json in questoes_json:
            categoria_nome = q_json.get('topico', 'Geral')
            categoria, _ = Categoria.objects.get_or_create(nome=categoria_nome.strip())
            
            nova_questao = Questao.objects.create(
                categoria=categoria,
                dificuldade=dificuldade_char,
                enunciado=q_json['questao'],
                alternativas=q_json['opcoes'], # Salva o JSON direto
                resposta_correta=q_json['resposta_correta'],
                criado_por=request.user
            )
            questoes_para_adicionar.append(nova_questao)

        nova_avaliacao.questoes.set(questoes_para_adicionar)
        
        quiz_url = f'/gerador/quiz/{nova_avaliacao.id}/' # URL do quiz
        return JsonResponse({'quiz_url': quiz_url, 'message': 'Avaliação salva com sucesso!'})

    except Exception as e:
        return JsonResponse({'error': f'Erro ao salvar no banco: {str(e)}'}, status=500)

# --- VIEW 4: A PÁGINA DO QUIZ (QUE O ALUNO VÊ) ---
def exibir_quiz(request, avaliacao_id):
    """
    Mostra o quiz para o aluno responder (Não precisa de login).
    """
    avaliacao = get_object_or_404(Avaliacao, id=avaliacao_id)
    questoes = avaliacao.questoes.all() # Pega as questões do M2M
    context = {
        'questoes': questoes,
        'avaliacao': avaliacao
    }
    return render(request, 'gerador_app/quiz.html', context)

# --- VIEW 5: A VIEW QUE RECEBE AS RESPOSTAS DO ALUNO ---
@require_POST
def submeter_quiz(request, avaliacao_id):
    """
    Salva as respostas do aluno no banco de dados.
    """
    avaliacao = get_object_or_404(Avaliacao, id=avaliacao_id)
    data = request.POST
    aluno_nome = data.get('aluno_nome', 'Aluno Anônimo') 

    for key, resposta_marcada in data.items():
        if key.startswith('questao-'):
            questao_id = key.split('-')[1]
            try:
                questao = Questao.objects.get(id=questao_id)
                RespostaAluno.objects.update_or_create(
                    avaliacao=avaliacao,
                    questao=questao,
                    aluno_id_externo=aluno_nome,
                    defaults={'resposta_aluno': resposta_marcada}
                )
            except Exception as e:
                print(f"Erro ao salvar resposta: {e}")
                continue 
                
    return redirect('exibir_quiz', avaliacao_id=avaliacao.id)