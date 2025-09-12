from flask import Flask, request, jsonify
from flasgger import Swagger
import yaml

app = Flask(__name__)


config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  
            "model_filter": lambda tag: True,  
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/" 
}


template = {
    "openapi": "3.0.3",
    "info": {
        "title": "API Simples de Usuários com Flask",
        "description": "Uma API RESTful para gerenciar usuários (CRUD), documentada com Swagger.",
        "version": "1.0.0"
    },
    "paths": {},
    "components": {}
}


try:
    with open('swagger.yaml', 'r', encoding='utf-8') as f:
        custom_definitions = yaml.safe_load(f)
        if custom_definitions:
            template.update(custom_definitions)
except FileNotFoundError:
    print("Atenção: Arquivo 'swagger.yaml' não encontrado. A documentação será gerada a partir das docstrings.")
except yaml.YAMLError as e:
    print(f"Erro ao ler o arquivo YAML: {e}")


swagger = Swagger(app, config=config, template=template)


users = []
current_id = 1



@app.route('/users', methods=['POST'])
def create_user():
    """Cria um novo usuário."""
    global current_id
    data = request.json
    if not data or 'nome' not in data or 'email' not in data:
        return jsonify({"error": "Dados inválidos. 'nome' e 'email' são obrigatórios."}), 400
    
    new_user = {
        'id': current_id,
        'nome': data['nome'],
        'email': data['email']
    }
    users.append(new_user)
    current_id += 1
    return jsonify(new_user), 201

@app.route('/users', methods=['GET'])
def get_all_users():
    """Retorna uma lista de todos os usuários."""
    return jsonify(users), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Busca um usuário específico pelo seu ID."""
    
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "Usuário não encontrado"}), 404

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Atualiza os dados de um usuário existente."""
    user = next((user for user in users if user['id'] == user_id), None)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404
    
    data = request.json
    
    user['nome'] = data.get('nome', user['nome'])
    user['email'] = data.get('email', user['email'])
    
    return jsonify(user), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Exclui um usuário do sistema."""
    global users
    user_found = any(user['id'] == user_id for user in users)
    if not user_found:
        return jsonify({"error": "Usuário não encontrado"}), 404
        
    
    users = [user for user in users if user['id'] != user_id]
    return jsonify({"message": "Usuário excluído com sucesso"}), 200


if __name__ == '__main__':
    app.run(debug=True)