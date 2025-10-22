// gerador_app/static/gerador_app/js/gerador.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('gerador-form');
    const resultadoDiv = document.getElementById('resultado');
    const questoesContainer = document.getElementById('questoes-container');
    const gabaritoContainer = document.getElementById('gabarito-container');
    const loadingDiv = document.getElementById('loading');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        resultadoDiv.style.display = 'block';
        loadingDiv.style.display = 'block';
        questoesContainer.innerHTML = ''; 
        if (gabaritoContainer) gabaritoContainer.innerHTML = ''; 

        const formData = new FormData(form);

        fetch(form.action, { 
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
                const gabarito = []; 
                
                data.questoes.forEach((item, index) => {
                    // 1. Cria a div principal para cada questão
                    const divQuestao = document.createElement('div');
                    divQuestao.className = 'card mb-4 p-3 questao-gerar';

                    // 2. Cria e adiciona o título da questão
                    const titulo = document.createElement('h5');
                    titulo.className = 'card-title';
                    titulo.textContent = `Questão ${index + 1}`;
                    divQuestao.appendChild(titulo);

                    // 3. Cria e adiciona o enunciado da questão
                    const enunciado = document.createElement('p');
                    enunciado.className = 'card-text';
                    enunciado.textContent = item.questao;
                    divQuestao.appendChild(enunciado);

                    // 4. Cria a lista de opções
                    const opcoesList = document.createElement('div');
                    
                    // Itera sobre as opções (A, B, C, D)
                    for (const letra in item.opcoes) {
                        const opcaoTexto = item.opcoes[letra];
                        const opcaoElement = document.createElement('div');
                        opcaoElement.className = ''; 
                        opcaoElement.textContent = `${letra}) ${opcaoTexto}`;
                        opcoesList.appendChild(opcaoElement);
                    }

                    divQuestao.appendChild(opcoesList);

                    // ===== ADIÇÃO PRINCIPAL AQUI (MOVIDA PARA O LUGAR CORRETO) =====
                    // Cria um elemento para mostrar a resposta correta dentro do card.
                    const respostaDiv = document.createElement('div');
                    // Usamos classes do Bootstrap para dar um destaque visual de "sucesso"
                    respostaDiv.className = 'mt-3 resposta-gerar'; 
                    respostaDiv.setAttribute('role', 'alert'); // Boa prática de acessibilidade
                    respostaDiv.innerHTML = `<strong>Resposta Correta:</strong> ${item.resposta_correta}`;
                    
                    // Adiciona a div da resposta ao final do card da questão
                    divQuestao.appendChild(respostaDiv);
                    // ================================================================

                    // 5. Adiciona a div da questão completa ao container na página
                    questoesContainer.appendChild(divQuestao);
                });
                
                // O restante do seu código original permanece inalterado.
            }
        })
        .catch(error => {
            loadingDiv.style.display = 'none';
            questoesContainer.innerHTML = `<div class="alert alert-danger">Ocorreu um erro de conexão. Verifique o console para detalhes.</div>`;
            console.error('Error:', error);
        });
    });
});