from flask import Flask, jsonify, request
app = Flask(__name__)

users = []
current_id = 0

@app.route('/users', methods=['POST'])
def createUsers():
    global current_id
    data = request.json

    if not 'name' in data or not 'email' in data:
        return jsonify({'error': 'É necessário informar nome e e-mail!'}), 400
    
    current_id += 1

    newUser = {
        'id': current_id,
        'name': data.get('name'),
        'email': data.get('email')
    }

    users.append(newUser)
    return jsonify(newUser), 201


@app.route('/users', methods=['GET'])
def getUsers():
    return jsonify(users), 200


@app.route('/users/<int:id>', methods=['GET'])
def getUser(id):
    for user in users:
        if user['id'] == id:
            return jsonify(user), 200
    return jsonify({'error': 'Usuário não encontrado!'}), 404


@app.route('/users/<int:id>', methods=['PUT'])
def updateUser(id):
    data = request.json
    for user in users:
        if user['id'] == id:
            user['name'] = data.get('name', user['name'])
            user['email'] = data.get('email', user['email'])
            return jsonify(user), 200
    return jsonify({'error': 'Usuário não encontrado!'}), 404

@app.route('/users/<int:id>', methods=['DELETE'])
def deleteUsers(id):
    for user in users:
        if user['id'] == id:
            users.remove(user)
            return jsonify({'message': 'Usuário excluído com sucesso!'}), 200

    return jsonify({'error': 'Usuário não encontrado!'}), 404
    
if __name__ == '__main__':
    app.run(debug=True, port=5001)