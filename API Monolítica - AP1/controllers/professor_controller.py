from flask import Blueprint, jsonify, request
from models import db
from models.professor import Professor

professor_bp = Blueprint('professor_bp', __name__)

@professor_bp.route('/', methods=['GET'])
def list_professores():
    professores = db.session.query(Professor).all()
    return jsonify([professor.to_dict() for professor in professores])

# ------------------------------------------------------------------

@professor_bp.route('/', methods=['POST'])
def create_professor():
    data = request.json
 
    # Validação de inteiro para idade
    try:
        idade = int(data.get('idade'))
    except (TypeError, ValueError):
        return jsonify({'error': 'Idade no formato errado! Utilize o número inteiro'}), 400
    
    novoProfessor = Professor(
        nome = data.get('nome'),
        idade = idade,
        materia = data.get('materia'),
        observacoes = data.get('observacoes')
    )

    db.session.add(novoProfessor)
    db.session.commit()
    return jsonify({
        'message': 'Professor criado com sucesso!',
        'professor': novoProfessor.to_dict()
    }), 201

# ------------------------------------------------------------------

@professor_bp.route('/<int:professor_id>', methods=['PUT'])
def update_professor(professor_id):
    data = request.json
    professor = db.session.query(Professor).filter_by(id=professor_id).first()

    if not professor:
        return jsonify({'error': 'Professor não encontrado!'}), 404

    # Validação de inteiro para idade
    try:
        professor.idade = int(data.get('idade', professor.idade))
    except (TypeError, ValueError):
        return jsonify({'error': 'Idade no formato errado! Utilize o número inteiro'}), 400
    
    professor.nome = data.get('nome', professor.nome)
    professor.materia = data.get('materia', professor.materia)
    professor.observacoes = data.get('observacoes', professor.observacoes)

    db.session.commit()
    return jsonify({
        'message': 'Professor atualizado com sucesso!',
        'professor': professor.to_dict()
    }), 200

# ------------------------------------------------------------------

@professor_bp.route('/<int:professor_id>', methods=['DELETE'])
def delete_professor(professor_id):
    professor = db.session.query(Professor).filter_by(id=professor_id).first()

    if not professor:
        return jsonify({'error': 'Professor não encontrado!'}), 404
    
    if professor.turmas:
        return jsonify({'error': 'Não é possível deletar esse professor porque tem turmas vinculadas!'}), 400
    
    db.session.delete(professor)
    db.session.commit()
    return jsonify({'message': 'Professor removido com sucesso!'}), 200