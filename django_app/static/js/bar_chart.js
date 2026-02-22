function renderBarChart(canvasId, configuracao) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    // Configurações com valor padrão (cor azul) onde não especificado pelo dicionário
    const backgroundColor = configuracao.backgroundColor || 'rgba(54, 162, 235, 0.7)';
    const borderColor = configuracao.borderColor || 'rgba(54, 162, 235, 1)';
    const datasetLabel = configuracao.datasetLabel || 'Quantidade';
    const titleText = configuracao.titleText || 'Gráfico';
    const yTitleText = configuracao.yTitleText || 'Quantidade';

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: configuracao.labels,
            datasets: [{
                label: datasetLabel,
                data: configuracao.data,
                backgroundColor: backgroundColor,
                borderColor: borderColor,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: titleText,
                    font: { size: 16 }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: yTitleText
                    },
                    ticks: {
                        stepSize: 1
                    }
                },
                x: {
                    ticks: {
                        autoSkip: false
                    }
                }
            }
        }
    });
}
