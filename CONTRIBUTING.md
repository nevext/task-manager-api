# Guia de Contribuição — Task Manager API

Esse arquivo explica **o que cada integrante deve fazer, como fazer e como entregar**. Leia com calma antes de começar.

---

## Antes de tudo: configuração inicial

### 1. Clone o repositório

Abra o terminal (no VS Code: `Ctrl + '`) e rode:

```bash
git clone https://github.com/nevext/task-manager-api.git
cd task-manager-api
```

### 2. Instale as dependências

```bash
py -m pip install -r requirements.txt
```

### 3. Teste se está funcionando

```bash
py main.py
```

Se aparecer algo como `Running on http://127.0.0.1:5000`, está tudo certo. Pode fechar com `Ctrl + C`.

---

## Como funciona o projeto

O projeto é uma API REST feita com Flask. Uma API é basicamente um servidor que recebe requisições HTTP e responde com dados em JSON.

Por exemplo:
- Alguém faz uma requisição `GET /tasks` → o servidor responde com a lista de tarefas em JSON
- Alguém faz uma requisição `POST /tasks` → o servidor cria uma nova tarefa

Os dados **não são salvos em banco de dados**. Ficam em listas na memória enquanto o servidor estiver rodando. Quando parar o servidor, os dados somem. Isso é intencional para simplificar o projeto.

---

## Estrutura do `main.py`

O `main.py` começa com três coisas que **quem for mexer primeiro precisa adicionar**:

```python
from flask import Flask, jsonify, request
from models import Category, User, Task

app = Flask(__name__)

tasks = []
users = []
categories = []
```

- `tasks`, `users` e `categories` são as listas que guardam os objetos na memória
- Cada endpoint vai ler ou modificar essas listas

---

## O que cada integrante deve fazer

---

### Samia — GET /tasks e GET /tasks/\<id\>

**Pode começar imediatamente.**

Você vai implementar dois endpoints de listagem de tarefas.

#### Passo 1: abra o `main.py` no VS Code

#### Passo 2: adicione o código abaixo na seção `# ENDPOINTS DE TASKS`

```python
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify([task.to_dict() for task in tasks])

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    for task in tasks:
        if task.get_id() == task_id:
            return jsonify(task.to_dict())
    return jsonify({'error': 'Tarefa não encontrada'}), 404
```

#### O que esse código faz?

- `@app.route('/tasks', methods=['GET'])` → diz pro Flask que quando alguém acessar `/tasks` com GET, deve chamar a função `get_tasks`
- `[task.to_dict() for task in tasks]` → percorre a lista de tarefas e converte cada uma pra dicionário (para poder virar JSON)
- `jsonify(...)` → transforma o dicionário em JSON e retorna como resposta
- No segundo endpoint, o `<int:task_id>` pega o número da URL (ex: `/tasks/1` → `task_id = 1`)
- Se não achar a tarefa, retorna erro 404

#### Passo 3: teste no Postman ou no navegador

Rode o servidor:
```bash
py main.py
```

Abra o Postman, crie uma requisição `GET` para `http://localhost:5000/tasks` e clique em Send. Deve retornar uma lista vazia `[]` por enquanto (porque ainda não tem tarefas).

#### Passo 4: commit e push

```bash
git add main.py
git commit -m "feat: adiciona GET /tasks e GET /tasks/<id>"
git push
```

---

### Karlos — GET /users e GET /categories

**Pode começar imediatamente.**

Você vai implementar dois endpoints de listagem de usuários e categorias.

#### Passo 1: abra o `main.py` no VS Code

#### Passo 2: adicione o código abaixo nas seções correspondentes

Na seção `# ENDPOINTS DE USERS`:

```python
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify([user.to_dict() for user in users])
```

Na seção `# ENDPOINTS DE CATEGORIES`:

```python
@app.route('/categories', methods=['GET'])
def get_categories():
    return jsonify([category.to_dict() for category in categories])
```

#### O que esse código faz?

Igual ao da Samia, mas para usuários e categorias. Percorre as listas e retorna tudo em JSON.

#### Passo 3: teste no Postman

- `GET http://localhost:5000/users` → deve retornar `[]`
- `GET http://localhost:5000/categories` → deve retornar `[]`

#### Passo 4: commit e push

```bash
git add main.py
git commit -m "feat: adiciona GET /users e GET /categories"
git push
```

---

### Eduardo — POST /tasks e POST /users

**Pode começar imediatamente.**

Você vai implementar os endpoints de criação de tarefas e usuários.

#### Passo 1: entenda como o POST funciona

No POST, o cliente envia dados no corpo da requisição (body) em formato JSON. O Flask lê esses dados com `request.get_json()`.

Exemplo de body para criar uma tarefa:
```json
{
    "title": "Estudar Flask",
    "description": "Ler a documentação",
    "status": "pending",
    "priority": "high",
    "deadline": "2025-06-01",
    "user_id": 1,
    "category_id": 1
}
```

#### Passo 2: adicione o código abaixo nas seções correspondentes

Na seção `# ENDPOINTS DE TASKS`:

```python
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task_id = len(tasks) + 1
    task = Task(
        id=task_id,
        title=data['title'],
        description=data.get('description', ''),
        status=data.get('status', 'pending'),
        priority=data.get('priority', 'low'),
        deadline=data.get('deadline', ''),
        user_id=data.get('user_id'),
        category_id=data.get('category_id')
    )
    tasks.append(task)
    return jsonify(task.to_dict()), 201
```

Na seção `# ENDPOINTS DE USERS`:

```python
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user_id = len(users) + 1
    user = User(
        id=user_id,
        name=data['name'],
        email=data['email']
    )
    users.append(user)
    return jsonify(user.to_dict()), 201
```

#### O que esse código faz?

- `request.get_json()` → lê o corpo da requisição e transforma em dicionário Python
- `data['title']` → pega o valor do campo `title` que veio no body
- `data.get('status', 'pending')` → pega o `status` se existir, senão usa `'pending'` como padrão
- `tasks.append(task)` → adiciona a tarefa criada na lista de tarefas
- O `, 201` no return é o código HTTP de "criado com sucesso"

#### Passo 3: teste no Postman

Crie uma requisição `POST` para `http://localhost:5000/tasks`.

Na aba **Body**, selecione **raw** e **JSON**, e coloque:
```json
{
    "title": "Minha primeira tarefa",
    "status": "pending",
    "priority": "low"
}
```

Clique em Send. Deve retornar a tarefa criada com status 201.

#### Passo 4: commit e push

```bash
git add main.py
git commit -m "feat: adiciona POST /tasks e POST /users"
git push
```

---

### Moisés — PUT /tasks/\<id\>

⚠️ **Aguarde a Samia concluir o GET /tasks antes de começar.**

Você vai implementar o endpoint de edição de tarefas.

#### Passo 1: entenda como o PUT funciona

O PUT recebe o id da tarefa na URL e os novos dados no body. Ele busca a tarefa na lista e atualiza os campos.

Exemplo de body para editar uma tarefa:
```json
{
    "status": "doing",
    "priority": "high"
}
```

#### Passo 2: adicione o código abaixo na seção `# ENDPOINTS DE TASKS`

```python
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task.get_id() == task_id:
            if 'title' in data:
                task.set_title(data['title'])
            if 'description' in data:
                task.set_description(data['description'])
            if 'status' in data:
                task.set_status(data['status'])
            if 'priority' in data:
                task.set_priority(data['priority'])
            if 'deadline' in data:
                task.set_deadline(data['deadline'])
            return jsonify(task.to_dict())
    return jsonify({'error': 'Tarefa não encontrada'}), 404
```

#### O que esse código faz?

- Percorre a lista de tarefas procurando pelo id
- Para cada campo que veio no body (`'title' in data`), atualiza o valor na tarefa
- Retorna a tarefa atualizada
- Se não achar, retorna erro 404

#### Passo 3: teste no Postman

Primeiro crie uma tarefa com POST, depois faça `PUT http://localhost:5000/tasks/1` com body:
```json
{
    "status": "doing"
}
```

#### Passo 4: commit e push

```bash
git add main.py
git commit -m "feat: adiciona PUT /tasks/<id>"
git push
```

---

### Yara — DELETE /tasks/\<id\> e POST /categories

⚠️ **Aguarde a Samia concluir o GET /tasks antes de começar.**

Você vai implementar o endpoint de deletar tarefas e criar categorias.

#### Passo 1: adicione o código abaixo nas seções correspondentes

Na seção `# ENDPOINTS DE TASKS`:

```python
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    for i, task in enumerate(tasks):
        if task.get_id() == task_id:
            tasks.pop(i)
            return jsonify({'message': 'Tarefa deletada com sucesso'})
    return jsonify({'error': 'Tarefa não encontrada'}), 404
```

Na seção `# ENDPOINTS DE CATEGORIES`:

```python
@app.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    category_id = len(categories) + 1
    category = Category(
        id=category_id,
        name=data['name']
    )
    categories.append(category)
    return jsonify(category.to_dict()), 201
```

#### O que esse código faz?

- `enumerate(tasks)` → percorre a lista retornando o índice `i` e o objeto `task` ao mesmo tempo
- `tasks.pop(i)` → remove a tarefa da lista pelo índice
- O POST de categories funciona igual ao de users: lê o body e cria um objeto Category

#### Passo 3: teste no Postman

- Crie uma tarefa com POST, depois faça `DELETE http://localhost:5000/tasks/1`
- Para categorias: `POST http://localhost:5000/categories` com body `{"name": "Trabalho"}`

#### Passo 4: commit e push

```bash
git add main.py
git commit -m "feat: adiciona DELETE /tasks/<id> e POST /categories"
git push
```

---

### Zek — Validações

⚠️ **Só comece após todos os endpoints acima estarem prontos.**

Você vai adicionar validações dentro dos endpoints já criados pelos outros.

#### O que validar?

1. **Status** só aceita: `pending`, `doing`, `done`
2. **Priority** só aceita: `low`, `medium`, `high`
3. **Campos obrigatórios** não podem vir vazios

#### Como adicionar as validações?

Dentro de cada endpoint que recebe dados (POST e PUT), adicione verificações antes de criar ou atualizar o objeto. Exemplo dentro do `POST /tasks`:

```python
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()

    # validação de campos obrigatórios
    if not data.get('title'):
        return jsonify({'error': 'O campo title é obrigatório'}), 400

    # validação de status
    status_validos = ['pending', 'doing', 'done']
    if data.get('status') and data['status'] not in status_validos:
        return jsonify({'error': f"Status inválido. Use: {', '.join(status_validos)}"}), 400

    # validação de priority
    prioridades_validas = ['low', 'medium', 'high']
    if data.get('priority') and data['priority'] not in prioridades_validas:
        return jsonify({'error': f"Priority inválida. Use: {', '.join(prioridades_validas)}"}), 400

    # ... resto do código do Eduardo aqui embaixo
```

#### O que esse código faz?

- `data.get('title')` → retorna `None` se o campo não existir, o `not` transforma isso em `True` e entra no if
- O `, 400` é o código HTTP de "requisição inválida"
- A mesma lógica de validação de status e priority deve ser aplicada também no `PUT /tasks/<id>`

#### Passo 3: commit e push

```bash
git add main.py
git commit -m "feat: adiciona validacoes nos endpoints"
git push
```

---

## Regras gerais

- **Mexa apenas nos arquivos e seções que são seus.** Não altere o `models.py` nem o `requirements.txt`
- **Sempre faça pull antes de começar** para pegar as últimas alterações do grupo:
```bash
git pull
```
- **Se der conflito** no git, chame o David Neves ou o João Pedro antes de tentar resolver sozinho
- **Mensagens de commit** devem ser curtas e descritivas, como nos exemplos acima

---

## Dúvidas?

Fale com o **João Pedro Duarte (Tech Lead)** ou com o **David Neves**.
