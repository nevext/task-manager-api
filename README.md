# Task Manager API

Sistema de cadastro de tarefas e status desenvolvido em Python com Flask, criado como atividade acadêmica da disciplina de Python II.

---

## Tecnologias utilizadas

- Python 3.14
- Flask 3.1.3
- Postman (para testes)
- Overleaf (para documentação acadêmica)

---

## Como rodar o projeto

1. Clone o repositório:
```bash
git clone https://github.com/nevext/task-manager-api.git
```

2. Instale as dependências:
```bash
py -m pip install -r requirements.txt
```

3. Rode o servidor:
```bash
py main.py
```

4. Acesse em: `http://localhost:5000`

---

## Estrutura do projeto

```
task-manager-api/
├── models.py        → classes Category, User e Task
├── main.py          → endpoints da API
├── requirements.txt → dependências do projeto
├── README.md        → documentação
└── frontend/
    ├── index.html   → estrutura da interface
    ├── style.css    → estilização
    └── script.js    → integração com a API
```

---

## Endpoints

### Categories
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | /categories | Lista todas as categorias |
| POST | /categories | Cria uma nova categoria |

### Users
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | /users | Lista todos os usuários |
| POST | /users | Cria um novo usuário |

### Tasks
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | /tasks | Lista todas as tarefas |
| GET | /tasks/\<id\> | Busca uma tarefa pelo id |
| POST | /tasks | Cria uma nova tarefa |
| PUT | /tasks/\<id\> | Edita uma tarefa |
| DELETE | /tasks/\<id\> | Deleta uma tarefa |

---

## Versão final esperada

Ao final do projeto, o sistema deverá funcionar da seguinte forma:

- O servidor Flask estará rodando localmente em `http://localhost:5000`
- Será possível criar usuários, categorias e tarefas via requisições HTTP
- Cada tarefa terá título, descrição, status, prioridade, prazo, um usuário responsável e uma categoria
- O status de uma tarefa poderá ser atualizado entre `pending`, `doing` e `done`
- A prioridade poderá ser `low`, `medium` ou `high`
- Todos os dados serão retornados em formato JSON
- O frontend consumirá a API e exibirá as tarefas de forma visual e interativa no navegador
- Todas as entradas serão validadas antes de serem aceitas pelo sistema

---

## Integrantes e divisão de tarefas

### João Pedro Duarte — Tech Lead
**Arquivo:** nenhum  
**Função:** Testar todos os endpoints no Postman após cada entrega e reportar erros ao responsável  
**Pode começar:** a qualquer momento, conforme os endpoints forem sendo entregues

---

### David Neves
**Arquivos:** `models.py`, `README.md`, `frontend/`  
**Função:** Criação das classes base do projeto (Category, User e Task), estrutura inicial do repositório, documentação no Overleaf com Samia e desenvolvimento do frontend  
**Status:** ✅ Concluído (models.py e estrutura base)  
**Pode começar:** já concluído — frontend será feito após a API estar pronta

---

### Karlos
**Arquivo:** `main.py`  
**Função:** Implementar os endpoints de listagem de tarefas  
**Endpoints:**
- `GET /tasks` → listar todas as tarefas
- `GET /tasks/<id>` → buscar uma tarefa pelo id

**Onde mexer:** apenas dentro do `main.py`, nas seções marcadas com `# ENDPOINTS DE TASKS`  
**Não mexa em:** `models.py`, `requirements.txt` ou qualquer outro arquivo  
**Fila:** ✅ pode começar imediatamente, o `models.py` já está pronto

---

### Eduardo
**Arquivo:** `main.py`  
**Função:** Implementar os endpoints de criação de tarefas e usuários  
**Endpoints:**
- `POST /tasks` → criar uma nova tarefa
- `POST /users` → criar um novo usuário

**Onde mexer:** apenas dentro do `main.py`, nas seções marcadas com `# ENDPOINTS DE TASKS` e `# ENDPOINTS DE USERS`  
**Não mexa em:** `models.py`, `requirements.txt` ou qualquer outro arquivo  
**Fila:** ✅ pode começar imediatamente, o `models.py` já está pronto

---

### Moisés
**Arquivo:** `main.py`  
**Função:** Implementar o endpoint de edição de tarefas  
**Endpoints:**
- `PUT /tasks/<id>` → editar status, prioridade ou outras informações de uma tarefa

**Onde mexer:** apenas dentro do `main.py`, na seção marcada com `# ENDPOINTS DE TASKS`  
**Não mexa em:** `models.py`, `requirements.txt` ou qualquer outro arquivo  
**Fila:** ⚠️ aguardar o Karlos concluir o `GET /tasks` antes de começar, pois precisará entender como as tarefas estão sendo armazenadas

---

### Yara
**Arquivo:** `main.py`  
**Função:** Implementar os endpoints de deletar tarefa e criar categoria  
**Endpoints:**
- `DELETE /tasks/<id>` → deletar uma tarefa
- `POST /categories` → criar uma nova categoria

**Onde mexer:** apenas dentro do `main.py`, nas seções marcadas com `# ENDPOINTS DE TASKS` e `# ENDPOINTS DE CATEGORIES`  
**Não mexa em:** `models.py`, `requirements.txt` ou qualquer outro arquivo  
**Fila:** ⚠️ aguardar o Karlos concluir o `GET /tasks` antes de começar

---

### Samia
**Arquivo:** `main.py`, `README.md`  
**Função:** Implementar os endpoints de listagem de usuários e categorias, e documentação no Overleaf com David  
**Endpoints:**
- `GET /users` → listar todos os usuários
- `GET /categories` → listar todas as categorias

**Onde mexer:** apenas dentro do `main.py`, nas seções marcadas com `# ENDPOINTS DE USERS` e `# ENDPOINTS DE CATEGORIES`  
**Não mexa em:** `models.py`, `requirements.txt` ou qualquer outro arquivo  
**Fila:** ✅ pode começar imediatamente, o `models.py` já está pronto

---

### Zek
**Arquivo:** `main.py`  
**Função:** Implementar as validações dos endpoints  
**O que validar:**
- Status só aceita `pending`, `doing` ou `done`
- Priority só aceita `low`, `medium` ou `high`
- Campos obrigatórios não podem vir vazios (título, status, etc)
- Retornar mensagens de erro claras quando algo estiver errado

**Onde mexer:** dentro do `main.py`, adicionando validações dentro dos endpoints já criados pelos outros  
**Não mexa em:** `models.py`, `requirements.txt` ou qualquer outro arquivo  
**Fila:** ⚠️ só pode começar após todos os endpoints estarem prontos

---

## Ordem de execução

```
1. David Neves   → models.py ✅ (concluído)
2. Karlos        → GET /tasks e GET /tasks/<id>
3. Eduardo       → POST /tasks e POST /users       (paralelo com Karlos)
4. Samia         → GET /users e GET /categories    (paralelo com Karlos)
5. Yara          → DELETE /tasks e POST /categories (após Karlos)
6. Moisés        → PUT /tasks/<id>                 (após Karlos)
7. Zek           → validações                      (após todos os endpoints)
8. João Pedro    → testes no Postman               (conforme endpoints forem prontos)
9. David Neves   → frontend                        (após API completa)
```

---

## Progresso

- [x] Repositório criado
- [x] Estrutura base do projeto
- [x] Classes Category, User e Task (David Neves)
- [ ] GET /tasks e GET /tasks/\<id\> (Karlos)
- [ ] POST /tasks e POST /users (Eduardo)
- [ ] GET /users e GET /categories (Samia)
- [ ] DELETE /tasks/\<id\> e POST /categories (Yara)
- [ ] PUT /tasks/\<id\> (Moisés)
- [ ] Validações (Zek)
- [ ] Documentação no Overleaf (David Neves e Samia)
- [ ] Frontend (David Neves)