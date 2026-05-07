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
from flask import Flask, jsonify #samia
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
# crie uma nova tarefa aqui
# Moises → PUT /tasks/<id>
# edite uma tarefa aqui (status, prioridade...)
# aguardar Samia concluir antes de comecar
# Yara → DELETE /tasks/<id>
# delete uma tarefa aqui
# aguardar Samia concluir antes de comecar
# ─────────────────────────────────────────────
# ENDPOINTS DE USERS
# responsavel: Eduardo (POST) e Karlos (GET)

# ─────────────────────────────────────────────
# Karlos → GET /users
# liste todos os usuarios aqui
# Eduardo → POST /users
# crie um novo usuario aqui
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
# ─────────────────────────────────────────────
# ENDPOINTS DE CATEGORIES
# responsavel: Yara (POST) e Karlos (GET)
# ─────────────────────────────────────────────
# Karlos → GET /categories
# liste todas as categorias aqui
# Yara → POST /categories
# crie uma nova categoria aqui
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
