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
from flask import Flask, jsonify, request, send_file #samia #eduardo
from flask_cors import CORS #david
from models import Category, User, Task #samia
import os

# 2. criar a instancia do app flask
app = Flask(__name__, static_folder='frontend', static_url_path='') #samia
CORS(app) #david - permitir requisicoes do frontend


@app.route('/')
def index():
    return send_file('frontend/index.html')    #kkkkkkkkkkk sem isso o flask nao acha o index.html e da erro, ai a gente fica se perguntando pq nao ta funcionando lol

@app.route('/<path:filename>')
def serve_static(filename):
    return send_file(f'frontend/{filename}')

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
    
    # ========== VALIDACOES DO ZEK ========== #zek
    # validação de campos obrigatórios #zek
    if not data.get('title') or data.get('title').strip() == '': #zek
        return jsonify({'error': 'O campo title é obrigatório'}), 400 #zek
    
    # validação de status #zek
    status_validos = ['pending', 'doing', 'done'] #zek
    if data.get('status') and data['status'] not in status_validos: #zek
        return jsonify({'error': f"Status inválido. Use: {', '.join(status_validos)}"}), 400 #zek
    
    # validação de priority #zek
    prioridades_validas = ['low', 'medium', 'high'] #zek
    if data.get('priority') and data['priority'] not in prioridades_validas: #zek
        return jsonify({'error': f"Priority inválida. Use: {', '.join(prioridades_validas)}"}), 400 #zek
    # ========== FIM DAS VALIDACOES ========== #zek
    
    task_id = len(tasks) + 1 #eduardo
    
    # buscar o usuario e a categoria pelos IDs #eduardo
    user = None #eduardo
    category = None #eduardo
    if data.get('user_id'): #eduardo
        for u in users: #eduardo
            if u.get_id() == data.get('user_id'): #eduardo
                user = u #eduardo
                break #eduardo
    if data.get('category_id'): #eduardo
        for c in categories: #eduardo
            if c.get_id() == data.get('category_id'): #eduardo
                category = c #eduardo
                break #eduardo
    
    task = Task( #eduardo
        id=task_id, #eduardo
        title=data['title'], #eduardo
        description=data.get('description', ''), #eduardo
        status=data.get('status', 'pending'), #eduardo
        priority=data.get('priority', 'low'), #eduardo
        deadline=data.get('deadline', ''), #eduardo
        user=user, #eduardo
        category=category #eduardo
    )
    tasks.append(task) #eduardo
    return jsonify(task.to_dict()), 201 #eduardo
# crie uma nova tarefa aqui
# Moises → PUT /tasks/<id>
# edite uma tarefa aqui (status, prioridade...)
@app.route('/tasks/<int:task_id>', methods=['PUT']) #moises
def update_task(task_id): #moises
    data = request.get_json() #moises
    
    # ========== VALIDACOES DO ZEK ========== #zek
    # validação de status #zek
    if data.get('status'): #zek
        status_validos = ['pending', 'doing', 'done'] #zek
        if data['status'] not in status_validos: #zek
            return jsonify({'error': f"Status inválido. Use: {', '.join(status_validos)}"}), 400 #zek
    
    # validação de priority #zek
    if data.get('priority'): #zek
        prioridades_validas = ['low', 'medium', 'high'] #zek
        if data['priority'] not in prioridades_validas: #zek
            return jsonify({'error': f"Priority inválida. Use: {', '.join(prioridades_validas)}"}), 400 #zek
    
    # validação de title (se fornecido, não pode estar vazio) #zek
    if data.get('title') and data.get('title').strip() == '': #zek
        return jsonify({'error': 'O campo title não pode estar vazio'}), 400 #zek
    # ========== FIM DAS VALIDACOES ========== #zek
    
    for task in tasks: #moises
        if task.get_id() == task_id: #moises
            if 'title' in data: #moises
                task.set_title(data['title']) #moises
            if 'description' in data: #moises
                task.set_description(data['description']) #moises
            if 'status' in data: #moises
                task.set_status(data['status']) #moises
            if 'priority' in data: #moises
                task.set_priority(data['priority']) #moises
            if 'deadline' in data: #moises
                task.set_deadline(data['deadline']) #moises
            return jsonify(task.to_dict()) #moises
    return jsonify({'error': 'Tarefa não encontrada'}), 404 #moises
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
@app.route('/users', methods=['GET']) #karlos
def get_users(): #karlos
    return jsonify([user.to_dict() for user in users]) #karlos

@app.route('/users/<int:user_id>', methods=['GET']) #karlos
def get_user(user_id): #karlos
    for user in users: #karlos
        if user.get_id() == user_id: #karlos
            return jsonify(user.to_dict()) #karlos
    return jsonify({'error': 'Usuário não encontrado'}), 404 #karlos
# Eduardo → POST /users
# crie um novo usuario aqui
@app.route('/users', methods=['POST']) #eduardo
def create_user(): #eduardo
    data = request.get_json() #eduardo
    
    # ========== VALIDACOES DO ZEK ========== #zek
    # validação de campos obrigatórios #zek
    if not data.get('name') or data.get('name').strip() == '': #zek
        return jsonify({'error': 'O campo name é obrigatório'}), 400 #zek
    
    if not data.get('email') or data.get('email').strip() == '': #zek
        return jsonify({'error': 'O campo email é obrigatório'}), 400 #zek
    # ========== FIM DAS VALIDACOES ========== #zek
    
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
@app.route('/categories', methods=['POST']) #yara                           #(david) yara mexe so aiii
def create_category(): #yara
    data = request.get_json() #yara
    
    # ========== VALIDACOES DO ZEK ========== #zek
    # validação de campos obrigatórios #zek
    if not data.get('name') or data.get('name').strip() == '': #zek
        return jsonify({'error': 'O campo name é obrigatório'}), 400 #zek
    # ========== FIM DAS VALIDACOES ========== #zek
    
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

if __name__ == '__main__': #(david) tava faltando isso aqui, ai o app nao rodava quando a gente dava python main.py
    app.run(debug=True)
