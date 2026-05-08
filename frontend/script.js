const API_URL = 'http://localhost:5000';  //aqui q pega a API


let tarefas = []; // Estado da aplicação
let usuarios = [];
let categorias = [];
let filtroAtual = 'todos';
let tarefaEmEdicao = null;
let abaAtiva = 'tarefas';

// Inicializar quando a página carregar
document.addEventListener('DOMContentLoaded', () => {
    verificarConexaoAPI();
    carregarDados();
    setInterval(carregarDados, 5000); // Atualizar a cada 5 segundos
});

// Verificar conexão com API
async function verificarConexaoAPI() {
    try {
        const response = await fetch(`${API_URL}/tasks`);
        if (response.ok) {
            document.getElementById('apiStatus').textContent = 'Conectado à API V1.0';
            document.getElementById('apiStatus').style.color = '#4caf50';
        }
    } catch (erro) {
        document.getElementById('apiStatus').textContent = 'API desconectada';
        document.getElementById('apiStatus').style.color = '#f44336';
        console.error('Erro ao conectar com API:', erro);
    }
}

// Carregar dados da API
async function carregarDados() {
    try {
        await Promise.all([
            carregarTarefas(),
            carregarUsuarios(),
            carregarCategorias()
        ]);
        renderizarTarefas();
    } catch (erro) {
        console.error('Erro ao carregar dados:', erro);
    }
}

async function carregarTarefas() {
    const response = await fetch(`${API_URL}/tasks`);
    if (!response.ok) throw new Error('Erro ao carregar tarefas');
    tarefas = await response.json();
}

async function carregarUsuarios() {
    const response = await fetch(`${API_URL}/users`);
    if (!response.ok) throw new Error('Erro ao carregar usuários');
    usuarios = await response.json();
    atualizarSelectUsuarios();
}

async function carregarCategorias() {
    const response = await fetch(`${API_URL}/categories`);
    if (!response.ok) throw new Error('Erro ao carregar categorias');
    categorias = await response.json();
    atualizarSelectCategorias();
}

function atualizarSelectUsuarios() {
    const select = document.getElementById('tarefaUser');
    const opcoesSalvas = select.value;
    select.innerHTML = '<option value="">Selecione um usuário</option>';
    usuarios.forEach(usuario => {
        const option = document.createElement('option');
        option.value = usuario.id;
        option.textContent = usuario.name;
        select.appendChild(option);
    });
    select.value = opcoesSalvas;
}

function atualizarSelectCategorias() {
    const select = document.getElementById('tarefaCategory');
    const opcoesSalvas = select.value;
    select.innerHTML = '<option value="">Selecione uma categoria</option>';
    categorias.forEach(categoria => {
        const option = document.createElement('option');
        option.value = categoria.id;
        option.textContent = categoria.name;
        select.appendChild(option);
    });
    select.value = opcoesSalvas;
}

// Renderizar tarefas
function renderizarTarefas() {
    if (filtroAtual === 'todos') {
        renderizarTarefasTodos();
    } else {
        renderizarTarefasPorStatus();
    }
}

function renderizarTarefasPorStatus() {
    document.getElementById('tarefasTodos').style.display = 'none';
    document.getElementById('tarefasContainer').style.display = 'grid';

    const statusMap = {
        pending: 'tarefasPending',
        doing: 'tarefasDoing',
        done: 'tarefasDone'
    };

    // Limpar todas as listas
    Object.values(statusMap).forEach(id => {
        document.getElementById(id).innerHTML = '';
    });

    // Agrupar tarefas por status
    const tarefasPorStatus = {
        pending: [],
        doing: [],
        done: []
    };

    tarefas.forEach(tarefa => {
        if (filtroAtual === tarefa.status || filtroAtual === 'todos') {
            tarefasPorStatus[tarefa.status].push(tarefa);
        }
    });

    // Renderizar cada grupo
    Object.entries(tarefasPorStatus).forEach(([status, tarefasStatus]) => {
        const container = document.getElementById(statusMap[status]);
        tarefasStatus.forEach(tarefa => {
            container.appendChild(criarCardTarefa(tarefa));
        });
    });
}

function renderizarTarefasTodos() {
    document.getElementById('tarefasContainer').style.display = 'none';
    const container = document.getElementById('tarefasTodos');
    container.innerHTML = '';
    container.style.display = 'block';

    tarefas.forEach(tarefa => {
        const card = document.createElement('div');
        card.className = `tarefa-card-todos ${tarefa.status}`;
        card.innerHTML = `
            <div style="flex: 1;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                    <h3 style="margin: 0; color: #2c2c2c;">${escapeHtml(tarefa.title)}</h3>
                    <span class="tarefa-status ${tarefa.status}">${traduzirStatus(tarefa.status)}</span>
                    <span class="tarefa-prioridade ${tarefa.priority}">${traduzirPrioridade(tarefa.priority)}</span>
                </div>
                <p style="color: #666; margin: 0; font-size: 14px;">${escapeHtml(tarefa.description)}</p>
                ${tarefa.user ? `<div style="color: #999; font-size: 12px; margin-top: 5px;">👤 ${escapeHtml(tarefa.user.name)}</div>` : ''}
                ${tarefa.category ? `<div style="color: #999; font-size: 12px;">${escapeHtml(tarefa.category.name)}</div>` : ''}
            </div>
            <div class="tarefa-acoes">
                <button class="btn-editar" onclick="editarTarefa(${tarefa.id})">Editar</button>
                <button class="btn-deletar" onclick="deletarTarefa(${tarefa.id})">Deletar</button>
            </div>
        `;
        container.appendChild(card);
    });
}

function criarCardTarefa(tarefa) {
    const card = document.createElement('div');
    card.className = `tarefa-card ${tarefa.status}`;
    
    const nomeUsuario = tarefa.user ? tarefa.user.name : 'Sem usuário';
    const inicialUsuario = nomeUsuario.charAt(0).toUpperCase();
    
    card.innerHTML = `
        <div class="tarefa-header">
            <h3 class="tarefa-titulo">${escapeHtml(tarefa.title)}</h3>
        </div>
        <div style="margin-bottom: 10px;">
            <span class="tarefa-status ${tarefa.status}">${traduzirStatus(tarefa.status)}</span>
            <span class="tarefa-prioridade ${tarefa.priority}">${traduzirPrioridade(tarefa.priority)}</span>
        </div>
        ${tarefa.description ? `<p class="tarefa-descricao">${escapeHtml(tarefa.description)}</p>` : ''}
        <div class="tarefa-meta">
            ${tarefa.deadline ? `<div class="tarefa-meta-item"><strong>${tarefa.deadline}</strong></div>` : ''}
            ${tarefa.category ? `<div class="tarefa-meta-item"><strong>${escapeHtml(tarefa.category.name)}</strong></div>` : ''}
        </div>
        <div class="tarefa-footer">
            <div class="tarefa-usuario">
                <div class="avatar">${inicialUsuario}</div>
                <span>${escapeHtml(nomeUsuario)}</span>
            </div>
            <div class="tarefa-acoes">
                <button class="btn-editar" onclick="editarTarefa(${tarefa.id})">Editar</button>
                <button class="btn-deletar" onclick="deletarTarefa(${tarefa.id})">Deletar</button>
            </div>
        </div>
    `;
    
    return card;
}

// Traduzir status e prioridade
function traduzirStatus(status) {
    const map = {
        pending: 'Pendente',
        doing: 'Em andamento',
        done: 'Concluída'
    };
    return map[status] || status;
}

function traduzirPrioridade(prioridade) {
    const map = {
        low: 'Baixa',
        medium: 'Média',
        high: 'Alta'
    };
    return map[prioridade] || prioridade;
}

// Filtrar tarefas
function filtrarTarefas(filtro) {
    filtroAtual = filtro;
    
    // Atualizar botões de filtro
    document.querySelectorAll('.filtro-btn').forEach(btn => {
        btn.classList.remove('ativo');
    });
    event.target.classList.add('ativo');
    
    renderizarTarefas();
}

// Abrir modal nova tarefa
function abrirModalNovaTarefa() {
    tarefaEmEdicao = null;
    document.getElementById('modalTitulo').textContent = 'Criar Nova Tarefa';
    document.getElementById('formTarefa').reset();
    document.getElementById('tarefaStatus').value = 'pending';
    document.getElementById('tarefaPriority').value = 'low';
    document.getElementById('modalTarefa').classList.add('ativo');
    document.getElementById('modalOverlay').style.display = 'block';
}

// Editar tarefa
function editarTarefa(tarefaId) {
    const tarefa = tarefas.find(t => t.id === tarefaId);
    if (!tarefa) return;
    
    tarefaEmEdicao = tarefa;
    document.getElementById('modalTitulo').textContent = 'Editar Tarefa';
    document.getElementById('tarefaTitulo').value = tarefa.title;
    document.getElementById('tarefaDescricao').value = tarefa.description;
    document.getElementById('tarefaStatus').value = tarefa.status;
    document.getElementById('tarefaPriority').value = tarefa.priority;
    document.getElementById('tarefaDeadline').value = tarefa.deadline;
    document.getElementById('tarefaUser').value = tarefa.user ? tarefa.user.id : '';
    document.getElementById('tarefaCategory').value = tarefa.category ? tarefa.category.id : '';
    
    document.getElementById('modalTarefa').classList.add('ativo');
    document.getElementById('modalOverlay').style.display = 'block';
}

// Fechar modal (compatibilidade)
function fecharModal() {
    fecharTodosModals();
}

// Salvar tarefa
async function salvarTarefa(event) {
    event.preventDefault();
    
    const titulo = document.getElementById('tarefaTitulo').value.trim();
    const descricao = document.getElementById('tarefaDescricao').value.trim();
    const status = document.getElementById('tarefaStatus').value;
    const prioridade = document.getElementById('tarefaPriority').value;
    const deadline = document.getElementById('tarefaDeadline').value;
    const userId = document.getElementById('tarefaUser').value;
    const categoryId = document.getElementById('tarefaCategory').value;
    
    if (!titulo) {
        mostrarNotificacao('Por favor, preencha o título da tarefa', 'erro');
        return;
    }
    
    const dados = {
        title: titulo,
        description: descricao,
        status: status,
        priority: prioridade,
        deadline: deadline,
        user_id: userId ? parseInt(userId) : null,
        category_id: categoryId ? parseInt(categoryId) : null
    };
    
    try {
        let response;
        if (tarefaEmEdicao) {
            // Editar tarefa existente
            response = await fetch(`${API_URL}/tasks/${tarefaEmEdicao.id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(dados)
            });
        } else {
            // Criar nova tarefa
            response = await fetch(`${API_URL}/tasks`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(dados)
            });
        }
        
        if (!response.ok) {
            const erro = await response.json();
            throw new Error(erro.error || 'Erro ao salvar tarefa');
        }
        
        fecharModal();
        await carregarTarefas();
        renderizarTarefas();
        
        const mensagem = tarefaEmEdicao ? 'Tarefa atualizada com sucesso!' : 'Tarefa criada com sucesso!';
        mostrarNotificacao(mensagem, 'sucesso');
    } catch (erro) {
        console.error('Erro ao salvar tarefa:', erro);
        mostrarNotificacao(erro.message, 'erro');
    }
}

// Deletar tarefa
async function deletarTarefa(tarefaId) {
    if (!confirm('Tem certeza que deseja deletar esta tarefa?')) return;
    
    try {
        const response = await fetch(`${API_URL}/tasks/${tarefaId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Erro ao deletar tarefa');
        }
        
        await carregarTarefas();
        renderizarTarefas();
        mostrarNotificacao('Tarefa deletada com sucesso!', 'sucesso');
    } catch (erro) {
        console.error('Erro ao deletar tarefa:', erro);
        mostrarNotificacao(erro.message, 'erro');
    }
}

// Mostrar notificação
function mostrarNotificacao(mensagem, tipo = 'sucesso') {
    const notif = document.createElement('div');
    notif.className = `notificacao ${tipo}`;
    notif.textContent = mensagem;
    document.body.appendChild(notif);
    
    setTimeout(() => {
        notif.remove();
    }, 3000);
}

function mudarAba(novaAba) {
    // Esconder todas as abas
    document.querySelectorAll('.aba-conteudo').forEach(aba => {
        aba.style.display = 'none';
    });
    
    // Mostrar aba selecionada
    document.getElementById(`abaContent-${novaAba}`).style.display = 'block';
    
    // Atualizar botões de aba
    document.querySelectorAll('.aba-btn').forEach(btn => {
        btn.classList.remove('ativa');
    });
    event.target.classList.add('ativa');
    
    // Atualizar estado
    abaAtiva = novaAba;
    
    // Renderizar conteúdo da aba
    if (novaAba === 'usuarios') {
        renderizarUsuarios();
    } else if (novaAba === 'categorias') {
        renderizarCategorias();
    }
}

function fecharTodosModals() {
    document.getElementById('modalTarefa').classList.remove('ativo');
    document.getElementById('modalUsuario').classList.remove('ativo');
    document.getElementById('modalCategoria').classList.remove('ativo');
    document.getElementById('modalOverlay').style.display = 'none';
}

function fecharModalTarefa() {
    document.getElementById('modalTarefa').classList.remove('ativo');
    document.getElementById('modalOverlay').style.display = 'none';
    tarefaEmEdicao = null;
}

function abrirModalNovoUsuario() {
    document.getElementById('formUsuario').reset();
    document.getElementById('modalUsuario').classList.add('ativo');
    document.getElementById('modalOverlay').style.display = 'block';
}

function fecharModalUsuario() {
    document.getElementById('modalUsuario').classList.remove('ativo');
    document.getElementById('modalOverlay').style.display = 'none';
}

async function salvarUsuario(event) {
    event.preventDefault();
    
    const nome = document.getElementById('usuarioNome').value.trim();
    const email = document.getElementById('usuarioEmail').value.trim();
    
    if (!nome || !email) {
        mostrarNotificacao('Por favor, preencha todos os campos', 'erro');
        return;
    }
    
    const dados = {
        name: nome,
        email: email
    };
    
    try {
        const response = await fetch(`${API_URL}/users`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        });
        
        if (!response.ok) {
            const erro = await response.json();
            throw new Error(erro.error || 'Erro ao criar usuário');
        }
        
        fecharModalUsuario();
        await carregarUsuarios();
        renderizarUsuarios();
        mostrarNotificacao('Usuário criado com sucesso!', 'sucesso');
    } catch (erro) {
        console.error('Erro ao salvar usuário:', erro);
        mostrarNotificacao(erro.message, 'erro');
    }
}

function renderizarUsuarios() {
    const container = document.getElementById('usuariosGrid');
    container.innerHTML = '';
    
    if (usuarios.length === 0) {
        container.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: #999;">Nenhum usuário cadastrado. Crie um novo!</p>';
        return;
    }
    
    usuarios.forEach(usuario => {
        const card = document.createElement('div');
        card.className = 'usuario-card';
        card.innerHTML = `
            <div class="usuario-avatar">${usuario.name.charAt(0).toUpperCase()}</div>
            <h3>${escapeHtml(usuario.name)}</h3>
            <p>${escapeHtml(usuario.email)}</p>
            <div class="usuario-info">ID: ${usuario.id}</div>
        `;
        container.appendChild(card);
    });
}

function abrirModalNovaCategoria() {
    document.getElementById('formCategoria').reset();
    document.getElementById('modalCategoria').classList.add('ativo');
    document.getElementById('modalOverlay').style.display = 'block';
}

function fecharModalCategoria() {
    document.getElementById('modalCategoria').classList.remove('ativo');
    document.getElementById('modalOverlay').style.display = 'none';
}

async function salvarCategoria(event) {
    event.preventDefault();
    
    const nome = document.getElementById('categoriaNome').value.trim();
    
    if (!nome) {
        mostrarNotificacao('Por favor, preencha o nome da categoria', 'erro');
        return;
    }
    
    const dados = {
        name: nome
    };
    
    try {
        const response = await fetch(`${API_URL}/categories`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        });
        
        if (!response.ok) {
            const erro = await response.json();
            throw new Error(erro.error || 'Erro ao criar categoria');
        }
        
        fecharModalCategoria();
        await carregarCategorias();
        renderizarCategorias();
        mostrarNotificacao('Categoria criada com sucesso!', 'sucesso');
    } catch (erro) {
        console.error('Erro ao salvar categoria:', erro);
        mostrarNotificacao(erro.message, 'erro');
    }
}

function renderizarCategorias() {
    const container = document.getElementById('categoriasGrid');
    container.innerHTML = '';
    
    if (categorias.length === 0) {
        container.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: #999;">Nenhuma categoria cadastrada. Crie uma nova!</p>';
        return;
    }
    
    categorias.forEach(categoria => {
        const card = document.createElement('div');
        card.className = 'categoria-card';
        card.innerHTML = `
            <div class="categoria-icon">📂</div>
            <h3>${escapeHtml(categoria.name)}</h3>
            <div class="categoria-info">ID: ${categoria.id}</div>
        `;
        container.appendChild(card);
    });
}

function escapeHtml(texto) {
    if (!texto) return '';
    const div = document.createElement('div');
    div.textContent = texto;
    return div.innerHTML;
}

// Tratamento de erros de CORS e conexão
window.addEventListener('error', (event) => {
    if (event.message.includes('fetch')) {
        console.error('Erro de conexão com API:', event);
    }
});
