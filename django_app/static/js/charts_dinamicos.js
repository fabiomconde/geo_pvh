document.addEventListener('DOMContentLoaded', function () {
    
    // Paleta de cores para os gráficos
    const colorPalette =[
        'rgba(54, 162, 235, 0.7)', // Azul
        'rgba(255, 99, 132, 0.7)', // Vermelho
        'rgba(255, 206, 86, 0.7)', // Amarelo
        'rgba(75, 192, 192, 0.7)', // Verde
        'rgba(153, 102, 255, 0.7)',// Roxo
        'rgba(255, 159, 64, 0.7)'  // Laranja
    ];

    const borderPalette = colorPalette.map(color => color.replace('0.7', '1'));

    // Pega todos os canvas na tela
    const canvases = document.querySelectorAll('canvas.dynamic-chart');

    canvases.forEach((canvas) => {
        const ctx = canvas.getContext('2d');
        
        const tipoGrafico = canvas.getAttribute('data-tipo');
        const colId = canvas.getAttribute('data-id');

        // Lê o JSON seguro gerado pelo Django
        let labels =[];
        let datasetsRaw =[];
        
        try {
            labels = JSON.parse(document.getElementById('labels_' + colId).textContent);
            datasetsRaw = JSON.parse(document.getElementById('datasets_' + colId).textContent);
        } catch (e) {
            console.error("Erro ao ler dados do gráfico ID: " + colId, e);
            return; // Interrompe se não tiver dados
        }

        // Formata os datasets injetando cores
        let datasetsFormatados = datasetsRaw.map((ds, i) => {
            if (tipoGrafico === 'pie' || tipoGrafico === 'doughnut') {
                ds.backgroundColor = colorPalette.slice(0, ds.data.length);
                ds.borderColor = borderPalette.slice(0, ds.data.length);
            } else {
                let colorIndex = i % colorPalette.length;
                ds.backgroundColor = colorPalette[colorIndex];
                ds.borderColor = borderPalette[colorIndex];
                ds.borderWidth = 1;
                
                if (tipoGrafico === 'line') {
                    ds.fill = true;
                    ds.backgroundColor = colorPalette[colorIndex].replace('0.7', '0.1'); 
                    ds.tension = 0.3; 
                }
            }
            return ds;
        });

        // Opções do Chart.js
        let options = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: (tipoGrafico === 'pie' || tipoGrafico === 'doughnut' || datasetsFormatados.length > 1),
                    position: 'bottom'
                }
            }
        };

        if (tipoGrafico === 'bar' || tipoGrafico === 'line') {
            options.scales = {
                y: { beginAtZero: true }
            };
        }

        // Desenha o Gráfico!
        new Chart(ctx, {
            type: tipoGrafico,
            data: {
                labels: labels,
                datasets: datasetsFormatados
            },
            options: options
        });
    });
});