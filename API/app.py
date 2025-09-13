from flask import Flask, jsonify, request
# Importações para o Swagger UI
from flask_swagger_ui import get_swaggerui_blueprint
import yaml

# Inicializa a aplicação Flask
app = Flask(__name__)

# --- Configuração do Swagger UI ---
SWAGGER_URL = '/apidocs'  # URL para a UI do Swagger
API_URL = '/swagger.json'  # URL para a especificação da API

# Carrega a especificação do arquivo swagger.yml
with open('swagger.yaml', 'r') as f: 
    swagger_spec = yaml.safe_load(f)

# Rota para servir o swagger.json
@app.route(API_URL)
def swagger_json():
    return jsonify(swagger_spec)

# Cria o blueprint do Swagger UI
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "API de Usuários"
    }
)

# Registra o blueprint na aplicação
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


# --- Banco de Dados em Memória ---
users = [
    {"id": 1, "nome": "Alice", "email": "alice@example.com"},
    {"id": 2, "nome": "Bob", "email": "bob@example.com"},
    {"id": 3, "nome": "Charlie", "email": "charlie@example.com"}
]
next_user_id = 4


# --- Definição das Rotas da API ---

@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    global next_user_id
    if request.method == 'GET':
        return jsonify({
            "mensagem": "Lista de usuários retornada com sucesso",
            "dados": users
        }), 200

    elif request.method == 'POST':
        new_user_data = request.get_json()
        if not new_user_data or 'nome' not in new_user_data or 'email' not in new_user_data:
            return jsonify({"erro": "Dados incompletos. 'nome' e 'email' são obrigatórios."}), 400
        new_user = {
            'id': next_user_id,
            'nome': new_user_data['nome'],
            'email': new_user_data['email']
        }
        users.append(new_user)
        next_user_id += 1
        return jsonify({
            "mensagem": "Usuário criado com sucesso",
            "dados": new_user
        }), 201

@app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user(id):
    user = next((user for user in users if user['id'] == id), None)
    if not user:
        return jsonify({"mensagem": "Usuário não encontrado"}), 404

    if request.method == 'GET':
        return jsonify({
            "mensagem": "Usuário encontrado",
            "dados": user
        }), 200

    elif request.method == 'PUT':
        update_data = request.get_json()
        if 'nome' in update_data:
            user['nome'] = update_data['nome']
        if 'email' in update_data:
            user['email'] = update_data['email']
        return jsonify({
            "mensagem": "Usuário atualizado",
            "dados": user
        }), 200

    elif request.method == 'DELETE':
        users.remove(user)
        return jsonify({"mensagem": "Usuário excluído"}), 200


# --- Execução da Aplicação ---
if __name__ == '__main__':
    app.run(debug=True)