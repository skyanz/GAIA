// gerador_app/static/gerador_app/js/gerador.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('gerador-form');
    const resultadoDiv = document.getElementById('resultado');
    const questoesContainer = document.getElementById('questoes-container');
    const gabaritoContainer = document.getElementById('gabarito-container');
    const loadingDiv = document.getElementById('loading');

    // --- NOVOS ELEMENTOS ---
    const salvarQuizContainer = document.getElementById('salvar-quiz-container');
    const btnSalvarQuiz = document.getElementById('btn-salvar-quiz');
    const salvarLoading = document.getElementById('salvar-loading');
    const salvarError = document.getElementById('salvar-error');

    // Variável para guardar as questões geradas e a dificuldade
    let questoesGeradas = [];
    let dificuldadeGerada = '';

    // --- ETAPA 1: GERAR PREVIEW (Seu código, adaptado) ---
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        // 1. Limpa tudo e mostra loading
        resultadoDiv.style.display = 'block';
        loadingDiv.style.display = 'block';
        questoesContainer.innerHTML = '';
        if (gabaritoContainer) gabaritoContainer.innerHTML = '';
        salvarQuizContainer.style.display = 'none'; // Esconde o botão de salvar
        salvarError.style.display = 'none';
        questoesGeradas = []; // Limpa questões anteriores

        const formData = new FormData(form);
        dificuldadeGerada = formData.get('dificuldade'); // Guarda a dificuldade

        // 2. Faz o fetch para a API de GERAR
        fetch(form.action, { // form.action é '/gerador/api/gerar/'
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            loadingDiv.style.display = 'none';
            if (data.error) {
                questoesContainer.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
            } else {
                // 3. Salva os dados na variável
                questoesGeradas = data.questoes;
                
                // 4. Desenha o preview (seu código original)
                desenharPreview(data.questoes);

                // 5. Mostra o botão "Salvar"
                salvarQuizContainer.style.display = 'block';
            }
        })
        .catch(error => {
            loadingDiv.style.display = 'none';
            questoesContainer.innerHTML = `<div class="alert alert-danger">Ocorreu um erro de conexão.</div>`;
            console.error('Error:', error);
        });
    });

    // --- ETAPA 2: SALVAR A AVALIAÇÃO (Novo) ---
    btnSalvarQuiz.addEventListener('click', function() {
        salvarLoading.style.display = 'block';
        salvarError.style.display = 'none';
        btnSalvarQuiz.disabled = true;

        // 1. Pega os dados do formulário
        const turmaId = document.getElementById('turma_id').value;
        const tituloAvaliacao = document.getElementById('titulo_avaliacao').value;
        const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;

        if (!turmaId) {
            salvarError.textContent = 'Por favor, selecione uma turma.';
            salvarError.style.display = 'block';
            salvarLoading.style.display = 'none';
            btnSalvarQuiz.disabled = false;
            return;
        }

        // 2. Prepara os dados para enviar à view 'salvar_e_abrir_quiz'
        const payload = {
            questoes: questoesGeradas,       // O JSON da IA
            turma_id: turmaId,
            titulo_avaliacao: tituloAvaliacao,
            dificuldade: dificuldadeGerada  // A dificuldade usada
        };

        // 3. Faz o fetch para a NOVA view (api_salvar_quiz)
        fetch('/gerador/api/salvar/', { // URL da Ação 4.2
            method: 'POST',
            body: JSON.stringify(payload), // Envia JSON
            headers: {
                'Content-Type': 'application/json', // Importante!
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            salvarLoading.style.display = 'none';
            btnSalvarQuiz.disabled = false;
            if (data.error) {
                salvarError.textContent = data.error;
                salvarError.style.display = 'block';
            } else {
                // 4. SUCESSO! Abre o link do quiz em uma nova aba
                salvarError.style.display = 'none';
                window.open(data.quiz_url, '_blank'); // Abre o link do aluno
            }
        })
        .catch(error => {
            salvarLoading.style.display = 'none';
            btnSalvarQuiz.disabled = false;
            salvarError.textContent = 'Erro de conexão ao salvar.';
            salvarError.style.display = 'block';
            console.error('Erro ao salvar:', error);
        });
    });

    // --- FUNÇÃO AUXILIAR PARA DESENHAR PREVIEW (Seu código original) ---
    function desenharPreview(questoes) {
        questoes.forEach((item, index) => {
            const divQuestao = document.createElement('div');
            divQuestao.className = 'card mb-4 p-3 questao-gerar';

            const titulo = document.createElement('h5');
            titulo.className = 'card-title';
            titulo.textContent = `Questão ${index + 1} (Tópico: ${item.topico || 'Geral'})`;
            divQuestao.appendChild(titulo);

            const enunciado = document.createElement('p');
            enunciado.className = 'card-text';
            enunciado.innerHTML = item.questao.replace(/\n/g, '<br>'); // Converte quebras de linha
            divQuestao.appendChild(enunciado);

            const opcoesList = document.createElement('div');
            for (const letra in item.opcoes) {
                const opcaoTexto = item.opcoes[letra];
                const opcaoElement = document.createElement('div');
                opcaoElement.textContent = `${letra}) ${opcaoTexto}`;
                opcoesList.appendChild(opcaoElement);
            }
            divQuestao.appendChild(opcoesList);

            const respostaDiv = document.createElement('div');
            respostaDiv.className = 'mt-3 resposta-gerar';
            respostaDiv.innerHTML = `<strong>Resposta Correta:</strong> ${item.resposta_correta}`;
            divQuestao.appendChild(respostaDiv);

            questoesContainer.appendChild(divQuestao);
        });
    }
});