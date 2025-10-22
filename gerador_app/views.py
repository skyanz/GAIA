# gerador_app/views.py
import google.generativeai as genai
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json # Importe a biblioteca JSON


@login_required
def gerador_questoes(request):
    if request.method == 'POST':
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            
            # Usando um modelo mais recente e capaz de gerar JSON com mais precisão
            model = genai.GenerativeModel('gemini-2.5-flash')

            num_questoes = request.POST.get('num_questoes', '5')
            dificuldade = request.POST.get('dificuldade', 'Média')
            
            materias = [m for m in [
                request.POST.get('materia1'),
                request.POST.get('materia2'),
                request.POST.get('materia3')
            ] if m]
            
            detalhes = request.POST.get('detalhes', '')

            # --- MUDANÇA PRINCIPAL AQUI: O NOVO PROMPT ---
            prompt = f"""
            Aja como um especialista em criar provas de matemática.
            Sua única saída deve ser um objeto JSON. Não inclua a palavra "json" ou ``` no início ou no fim.
            Crie um array JSON contendo {num_questoes} objetos. Cada objeto deve representar uma questão de múltipla escolha
            com dificuldade {dificuldade} sobre os seguintes tópicos: {', '.join(materias)}.

            {f"Leve em consideração os seguintes detalhes: {detalhes}" if detalhes else ""}

            O formato de cada objeto no array JSON deve ser exatamente o seguinte:
            {{
              "questao": "Texto da pergunta aqui.",
              "opcoes": {{
                "A": "Texto da alternativa A",
                "B": "Texto da alternativa B",
                "C": "Texto da alternativa C",
                "D": "Texto da alternativa D"
              }},
              "resposta_correta": "B"
            }}

            Certifique-se de que a resposta_correta seja apenas a letra correspondente (A, B, C ou D).
            Não adicione nenhum texto ou formatação fora do array JSON.
            """

            # Configure o modelo para gerar a resposta em formato JSON
            generation_config = genai.types.GenerationConfig(
                response_mime_type="application/json"
            )
            response = model.generate_content(prompt, generation_config=generation_config)
            
            # O ideal é que a API já retorne um JSON, mas caso retorne uma string,
            # vamos convertê-la para um objeto Python.
            questoes_json = json.loads(response.text)
            
            # Retorna o JSON diretamente para o frontend
            return JsonResponse({'questoes': questoes_json})

        except Exception as e:
            return JsonResponse({'error': f'Ocorreu um erro ao gerar as questões: {str(e)}'}, status=500)

    return render(request, 'gerador_app/gerador.html')

def quiz(request):

    questoes = [
        {'id':1, 'enunciado':'Qual a área de um círculo de raio 5?, considere π = 3', 'alternativa_a':75, 'alternativa_b':46, 'alternativa_c':90, 'alternativa_d':25},
        {'id':2, 'enunciado':'Qual a área de um quadrado de lado 7?', 'alternativa_a':5, 'alternativa_b':7, 'alternativa_c':10, 'alternativa_d':49},
        {'id':3, 'enunciado':'Qual o perímetro de um retângulo de lado maior = 5 e lado menor = 4?', 'alternativa_a':20,'alternativa_b':22,'alternativa_c':18,'alternativa_d':90}
        ]
    
    
    return render(request, 'gerador_app/quiz.html', {'questoes':questoes})


