// Contadores globais para gerar IDs únicos no formulário
let rowCounter = 0;
let quadrosCounter = {}; // Armazena a quantidade de quadros por linha ex: { 'row_1': 2 }

// Inicializa modal do Bootstrap
let modalLayout;
document.addEventListener("DOMContentLoaded", function() {
    const modalEl = document.getElementById('modalLayoutLinha');
    if (modalEl) {
        modalLayout = new bootstrap.Modal(modalEl);
    }
});

/**
 * Adiciona uma nova linha ao canvas de construção.
 * @param {string} tipoLayout - 'tabela_1', 'grafico_1', 'grafico_2', 'quadros'
 * @param {object} dadosIniciais - JSON com dados do banco (usado na edição)
 * @returns {number} rowId gerado
 */
function adicionarLinha(tipoLayout, dadosIniciais = null) {
    rowCounter++;
    const rowId = rowCounter;
    
    // 1. Clonar a Linha Base
    const tplLinha = document.getElementById('tpl-linha-base').innerHTML;
    let tituloLinha = "";
    
    if (tipoLayout === 'tabela_1') tituloLinha = "Layout: 1 Tabela de Dados (100%)";
    if (tipoLayout === 'grafico_1') tituloLinha = "Layout: 1 Gráfico Grande (100%)";
    if (tipoLayout === 'grafico_2') tituloLinha = "Layout: 2 Gráficos Lado a Lado (50%/50%)";
    if (tipoLayout === 'quadros') tituloLinha = "Layout: Quadros Numéricos de Destaque";

    let htmlLinha = tplLinha
        .replaceAll('{ROW_ID}', rowId)
        .replaceAll('{TIPO_LINHA}', tipoLayout)
        .replaceAll('{TITULO_LINHA}', tituloLinha);
    
    // Cria um elemento temporário para inserir os filhos
    const divTemp = document.createElement('div');
    divTemp.innerHTML = htmlLinha;
    const linhaElement = divTemp.firstElementChild;
    const conteudoContainer = linhaElement.querySelector('.builder-row-content');

    // 2. Injetar o conteúdo específico de acordo com o layout
    if (tipoLayout === 'tabela_1') {
        const tplTabela = document.getElementById('tpl-bloco-tabela').innerHTML;
        conteudoContainer.innerHTML = tplTabela.replaceAll('{ROW_ID}', rowId);
    } 
    else if (tipoLayout === 'grafico_1') {
        const tplGrafico = document.getElementById('tpl-bloco-grafico').innerHTML;
        conteudoContainer.innerHTML = tplGrafico
            .replaceAll('{ROW_ID}', rowId)
            .replaceAll('{COL_CLASS}', 'col-12')
            .replaceAll('{COL_IDX}', '0');
    }
    else if (tipoLayout === 'grafico_2') {
        const tplGrafico = document.getElementById('tpl-bloco-grafico').innerHTML;
        const col1 = tplGrafico.replaceAll('{ROW_ID}', rowId).replaceAll('{COL_CLASS}', 'col-md-6').replaceAll('{COL_IDX}', '0');
        const col2 = tplGrafico.replaceAll('{ROW_ID}', rowId).replaceAll('{COL_CLASS}', 'col-md-6').replaceAll('{COL_IDX}', '1');
        conteudoContainer.innerHTML = col1 + col2;
    }
    else if (tipoLayout === 'quadros') {
        quadrosCounter[rowId] = 0; // Inicia o contador para esta linha
        const tplQuadrosArea = document.getElementById('tpl-bloco-quadros').innerHTML;
        conteudoContainer.innerHTML = tplQuadrosArea.replaceAll('{ROW_ID}', rowId);
        
        // Se estiver CRIANDO (não tem dados iniciais), adiciona 3 default.
        if (!dadosIniciais) {
            setTimeout(() => {
                adicionarQuadro(rowId);
                adicionarQuadro(rowId);
                adicionarQuadro(rowId);
            }, 50);
        }
    }

    // 3. Preencher dados caso seja EDIÇÃO (dadosIniciais presente)
    if (dadosIniciais && dadosIniciais.cols) {
        dadosIniciais.cols.forEach((colData, index) => {
            
            // Popula ID antigo (para não perder os dados JSON já salvos)
            if (colData.old_id) {
                let oldIdInput = linhaElement.querySelector(`[name="linhas[${rowId}][col][${index}][old_id]"]`);
                if (oldIdInput) oldIdInput.value = colData.old_id;
            }
            
            // Popula Título
            if (colData.titulo) {
                let tituloInput = linhaElement.querySelector(`[name="linhas[${rowId}][col][${index}][titulo]"]`);
                if (tituloInput) tituloInput.value = colData.titulo;
            }
            
            // Popula Tipo de Gráfico (Se aplicável)
            if (colData.tipo) {
                let tipoInput = linhaElement.querySelector(`[name="linhas[${rowId}][col][${index}][tipo]"]`);
                if (tipoInput) tipoInput.value = colData.tipo;
            }

            // Remove a obrigatoriedade do arquivo CSV já que o banco já possui os dados
            let fileInput = linhaElement.querySelector(`[name="linhas[${rowId}][col][${index}][csv]"]`);
            if (fileInput) {
                fileInput.removeAttribute('required');
                fileInput.insertAdjacentHTML('afterend', `
                    <div class="alert alert-warning py-1 px-2 mt-2 mb-0 small border-warning text-dark d-flex align-items-center">
                        <i class="bi bi-info-circle me-2"></i> Dados em nuvem detectados. Envie um novo .csv apenas se quiser substituir.
                    </div>
                `);
            }
        });
    }

    // 4. Adiciona a linha ao Canvas final e fecha modal
    document.getElementById('builder-canvas').appendChild(linhaElement);
    if (modalLayout) modalLayout.hide();
    
    // Rola a página suavemente para a nova linha
    if (!dadosIniciais) {
        linhaElement.scrollIntoView({ behavior: 'smooth', block: 'end' });
    }

    return rowId; // Retornado para uso subsequente caso necessário (ex: quadros)
}

function removerLinha(rowIdString) {
    if (confirm("Tem certeza que deseja remover esta linha inteira? Todos os gráficos/tabelas atrelados a ela serão perdidos ao salvar.")) {
        const row = document.getElementById(rowIdString);
        if (row) {
            row.style.opacity = '0';
            setTimeout(() => row.remove(), 200); // Efeito suave
        }
    }
}

// ---- Funções Específicas para Quadros (Stat Cards) ----

/**
 * Adiciona um Quadro Numérico (Card) em uma linha existente.
 * @param {number} rowId - O ID lógico da linha pai
 * @param {object} dadosIniciais - Dados para preencher na edição
 */
function adicionarQuadro(rowId, dadosIniciais = null) {
    const container = document.getElementById(`quadros_container_${rowId}`);
    if (!container) return;

    // Verifica limite máximo de 6 quadros para evitar quebra de layout responsivo
    const totalAtual = container.querySelectorAll('.quadro-item').length;
    if (totalAtual >= 6) {
        alert("Você atingiu o limite máximo de 6 quadros nesta linha.");
        return;
    }

    quadrosCounter[rowId]++;
    const quadroIdx = quadrosCounter[rowId];

    const tplItemQuadro = document.getElementById('tpl-item-quadro').innerHTML;
    let htmlQuadro = tplItemQuadro
        .replaceAll('{ROW_ID}', rowId)
        .replaceAll('{QUADRO_IDX}', quadroIdx);

    // Converte para Node DOM e injeta
    const divTemp = document.createElement('div');
    divTemp.innerHTML = htmlQuadro;
    const quadroElement = divTemp.firstElementChild;

    // Preenche com os dados se for modo Edição
    if (dadosIniciais) {
        quadroElement.querySelector(`[name="linhas[${rowId}][quadros][${quadroIdx}][titulo]"]`).value = dadosIniciais.titulo || '';
        quadroElement.querySelector(`[name="linhas[${rowId}][quadros][${quadroIdx}][valor]"]`).value = dadosIniciais.valor || '';
        
        if (dadosIniciais.icone) {
            quadroElement.querySelector(`[name="linhas[${rowId}][quadros][${quadroIdx}][icone]"]`).value = dadosIniciais.icone;
        }
        if (dadosIniciais.cor) {
            quadroElement.querySelector(`[name="linhas[${rowId}][quadros][${quadroIdx}][cor]"]`).value = dadosIniciais.cor;
        }
    }

    container.appendChild(quadroElement);
}

function removerQuadro(quadroIdString, rowId) {
    const quadro = document.getElementById(quadroIdString);
    if (quadro) {
        quadro.style.transform = 'scale(0.9)';
        quadro.style.opacity = '0';
        setTimeout(() => quadro.remove(), 200);
    }
}
