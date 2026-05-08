# main.py
#
# por que main.py?
# é a convencao mais usada em python para indicar o arquivo principal do projeto,
# o ponto de entrada, onde tudo comeca. quando alguem clona o repositorio e quer
# rodar, ja sabe que é o main.py
#
# por que separado do models.py?
# cada arquivo tem uma responsabilidade diferente. o models.py define como os dados
# sao, a estrutura. o main.py define o que o sistema faz com esses dados, as acoes.
# é o principio de separacao de responsabilidades: cada arquivo cuida de uma coisa so.
# se misturasse tudo num arquivo so ficaria uma baguca dificil de cada pessoa mexer
# sem conflito.
#
# importante: quem for comecar esse arquivo deve:
# 1. importar o flask e as classes do models.py
from flask import Flask, jsonify, request #samia #eduardo
from models import Category, User, Task #samia

# 2. criar a instancia do app flask
app = Flask(__name__) #samia

# 3. criar as listas que vao guardar os objetos na memoria
tasks = [] #samia
users = [] #samia
categories = [] #samia

# 4. implementar os endpoints da sua secao
# 5. no final do arquivo, garantir que o servidor rode com app.run(debug=True)
# ─────────────────────────────────────────────
# ENDPOINTS DE TASKS
# responsavel: Samia (GET), Eduardo (POST), Moises (PUT), Yara (DELETE)
# atencao: Moises e Yara so podem comecar apos Samia concluir o GET /tasks
# ─────────────────────────────────────────────
# Samia → GET /tasks
# liste todas as tarefas aqui
@app.route('/tasks', methods=['GET']) #samia
def get_tasks(): #samia
    return jsonify([task.to_dict() for task in tasks]) #samia

@app.route('/tasks/<int:task_id>', methods=['GET']) #samia
def get_task(task_id): #samia
    for task in tasks: #samia
        if task.get_id() == task_id: #samia
            return jsonify(task.to_dict()) #samia
    return jsonify({'error': 'Tarefa não encontrada'}), 404 #samia
# Samia → GET /tasks/<id>
# busque uma tarefa pelo id aqui
# Eduardo → POST /tasks
@app.route('/tasks', methods=['POST']) #eduardo
def create_task(): #eduardo
    data = request.get_json() #eduardo
    task_id = len(tasks) + 1 #eduardo
    task = Task( #eduardo
        id=task_id, #eduardo
        title=data['title'], #eduardo
        description=data.get('description', ''), #eduardo
        status=data.get('status', 'pending'), #eduardo
        priority=data.get('priority', 'low'), #eduardo
        deadline=data.get('deadline', ''), #eduardo
        user_id=data.get('user_id'), #eduardo
        category_id=data.get('category_id') #eduardo
    )
    tasks.append(task) #eduardo
    return jsonify(task.to_dict()), 201 #eduardo
# crie uma nova tarefa aqui
# Moises → PUT /tasks/<id>
# edite uma tarefa aqui (status, prioridade...)
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task.get_id() == task_id:
            # Atualiza apenas o que foi enviado no JSON
            if 'title' in data: task.title = data['title']
            if 'status' in data: task.status = data['status']
            if 'priority' in data: task.priority = data['priority']
            if 'description' in data: task.description = data['description']
            
            return jsonify(task.to_dict()), 200
    return jsonify({'error': 'Tarefa não encontrada'}), 404
# aguardar Samia concluir antes de comecar
# Yara → DELETE /tasks/<id>
# delete uma tarefa aqui

@app.route('/tasks/<int:task_id>', methods=['DELETE']) #yara
def delete_task(task_id): #yara
    for i, task in enumerate(tasks): #yara
        if task.get_id() == task_id: #yara
            tasks.pop(i) #yara
            return jsonify({'message': 'Tarefa deletada com sucesso'}) #yara
    return jsonify({'error': 'Tarefa não encontrada'}), 404 #yara    

# ENDPOINTS DE USERS
# responsavel: Eduardo (POST) e Karlos (GET)

# ─────────────────────────────────────────────
# Karlos → GET /users
# liste todos os usuarios aqui
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify([task.to_dict() for task in tasks])

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    for task in tasks:
        if task.get_id() == task_id:
            return jsonify(task.to_dict())
    return jsonify({'error': 'Tarefa não encontrada'}), 404
# Eduardo → POST /users
# crie um novo usuario aqui
@app.route('/users', methods=['POST']) #eduardo
def create_user(): #eduardo
    data = request.get_json() #eduardo
    user_id = len(users) + 1 #eduardo
    user = User( #eduardo
        id=user_id, #eduardo
        name=data['name'], #eduardo
        email=data['email'] #eduardo
    )
    users.append(user) #eduardo
    return jsonify(user.to_dict()), 201 #eduardo
# ─────────────────────────────────────────────
# ENDPOINTS DE CATEGORIES
# responsavel: Yara (POST) e Karlos (GET)
# ─────────────────────────────────────────────
# Karlos → GET /categories
# liste todas as categorias aqui
@app.route('/categories', methods=['GET'])
def get_categories():
    return jsonify([category.to_dict() for category in categories])
# Yara → POST /categories
# crie uma nova categoria aqui
@app.route('/categories', methods=['POST']) #yara
def create_category(): #yara
    data = request.get_json() #yara
    category_id = len(categories) + 1 #yara
    category = Category( #yara
        id=category_id, #yara
        name=data['name'] #yara
    )
    categories.append(category) #yara
    return jsonify(category.to_dict()), 201 #yara
# ─────────────────────────────────────────────
# VALIDACOES
# responsavel: Zek
# so mexa aqui depois que todos os endpoints acima estiverem prontos
# adicione as validacoes dentro dos endpoints ja criados
# ex: status so aceita pending, doing ou done
# ex: priority so aceita low, medium ou high
# ex: campos obrigatorios nao podem vir vazios
# ─────────────────────────────────────────────

if __name__ == '__main__':
    app.run(debug=True)
