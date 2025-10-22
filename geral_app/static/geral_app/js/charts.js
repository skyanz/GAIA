// geral_app/static/geral_app/js/charts.js
document.addEventListener('DOMContentLoaded', function() {
    // Gráfico de Desempenho por Matéria (Barras)
    const ctxMateria = document.getElementById('desempenhoMateriaChart').getContext('2d');
    new Chart(ctxMateria, {
        type: 'bar',
        data: {
            labels: ['Matéria A', 'Matéria B', 'Matéria C', 'Matéria D'], // Nomes das matérias
            datasets: [{
                label: 'Taxa de Acerto (%)',
                data: [85, 62, 90, 78], // Valores de acerto para cada matéria
                backgroundColor: [
                    '#28B4C8', // Ciano
                    '#A050A0', // Roxo
                    '#E83E8C', // Magenta
                    '#20C997'  // Verde
                ],
                borderColor: [
                    '#28B4C8',
                    '#A050A0',
                    '#E83E8C',
                    '#20C997'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            },
            plugins: {
                legend: {
                    display: false // Esconde a legenda como na imagem
                }
            }
        }
    });

    // Gráfico de Evolução de Desempenho (Linha)
    const ctxEvolucao = document.getElementById('evolucaoDesempenhoChart').getContext('2d');
    new Chart(ctxEvolucao, {
        type: 'line',
        data: {
            labels: ['Semana 1', 'Semana 2', 'Semana 3', 'Semana 4', 'Semana 5'], // Período de tempo
            datasets: [{
                label: 'Desempenho Geral',
                data: [65, 70, 70, 80, 85], // Dados de evolução
                fill: false,
                borderColor: '#007BFF', // Azul
                tension: 0.1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
});