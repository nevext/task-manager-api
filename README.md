# Task Manager API

Sistema de cadastro de tarefas e status desenvolvido em Python com Flask.

## Como o repositório foi criado

O repositório foi criado pelo GitHub Desktop com as seguintes configurações:

- **Nome:** task-manager-api
- **Descrição:** Sistema de cadastro de tarefas e status utilizando Flask API e Postman
- **README:** inicializado automaticamente para documentar o projeto
- **Git ignore:** configurado para Python, para ignorar arquivos temporários e desnecessários como `__pycache__`, `.env` e `venv/`
- **Licença:** sem licença definida por enquanto

Ao criar o repositório, dois arquivos foram gerados automaticamente pelo Git:

- **.gitattributes** — define como o Git deve tratar os arquivos do projeto, como o tipo de quebra de linha, evitando conflitos entre membros do grupo que usam sistemas operacionais diferentes (Windows, Linux, Mac)
- **.gitignore** — lista os arquivos e pastas que o Git deve ignorar e não enviar pro GitHub, como arquivos temporários do Python que não fazem sentido compartilhar com o grupo

## Tecnologias utilizadas

- Python 3.14
- Flask 3.1.3
- Postman

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

## Estrutura do projeto

```
task-manager-api/
├── models.py        → classes Category, User e Task (David)
├── main.py          → endpoints da API (Karlos, Eduardo, Moisés, Yara, Samia)
├── requirements.txt → dependências do projeto
└── README.md        → documentação
```

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

## Progresso

- [x] Repositório criado (David)
- [x] Classes Category, User e Task (David)
- [x] Estrutura base do main.py (David)
- [ ] Endpoints de Categories
- [ ] Endpoints de Users
- [ ] Endpoints de Tasks
- [ ] Testes (Zek)
- [ ] Frontend (David)

## Integrantes

- João Pedro Duarte (Tech Lead)
- David / nevext
- Karlos
- Eduardo
- Moisés
- Yara
- Samia
- Zek
```