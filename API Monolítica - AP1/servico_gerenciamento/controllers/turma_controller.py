from flask import Blueprint, jsonify, request
from models import db
from models.turma import Turma
from models.professor import Professor

turma_bp = Blueprint('turma_bp', __name__)

@turma_bp.route('/', methods=['GET'])
def list_turmas():
    turmas = db.session.query(Turma).all()
    return jsonify([turma.to_dict() for turma in turmas])

# ------------------------------------------------------------------

@turma_bp.route('/', methods=['POST'])
def create_turma():
    data = request.json

    # Validação de inteiro para professor
    try:
        professor_id = int(data.get('professor_id'))
    except (TypeError, ValueError):
        return jsonify({'error': 'ID Professor no formato errado! Utilize o número inteiro'}), 400
    
    # Validação de turma existente
    professor_existente = db.session.query(Professor).filter_by(id=professor_id).first()
    if not professor_existente:
        return jsonify ({'error': 'Professor não encontrado!'}), 404
    
    novaTurma = Turma(
        descricao = data.get('descricao'),
        professor_id = professor_id
    )

    db.session.add(novaTurma)
    db.session.commit()
    return jsonify({
        'message': 'Turma criada com sucesso!',
        'turma': novaTurma.to_dict()
    }), 201

# ------------------------------------------------------------------

@turma_bp.route('/<int:turma_id>', methods=['PUT'])
def update_turma(turma_id):
    data = request.json
    turma = db.session.query(Turma).filter_by(id=turma_id).first()

    if not turma:
        return jsonify({'error': 'Turma não encontrada!'}), 404
    
    # Validação de inteiro para professor
    try:
        turma.professor_id = int(data.get('professor_id', turma.professor_id))
    except (TypeError, ValueError):
        return jsonify({'error': 'ID Professor no formato errado! Utilize o número inteiro'}), 400

    # Validação de professor existente
    professor_existente = db.session.query(Professor).filter_by(id=turma.professor_id).first()
    if not professor_existente:
       return jsonify ({'error': 'Professor não encontrado!'}), 404
    
    turma.descricao = data.get('descricao', turma.descricao)
    
    novo_ativo = data.get('ativo', turma.ativo)
    if not isinstance(novo_ativo, bool):
        return jsonify({'error': 'Campo ativo no formato errado! Utilize true ou false'}), 400
    turma.ativo = novo_ativo

    db.session.commit()
    return jsonify({
        'message': 'Turma atualizada com sucesso!',
        'turma': turma.to_dict()
    }), 200

# ------------------------------------------------------------------

@turma_bp.route('/<int:turma_id>', methods=['DELETE'])
def delete_turma(turma_id):
    turma = db.session.query(Turma).filter_by(id=turma_id).first()

    if not turma:
        return jsonify({'error': 'Turma não encontrada!'}), 404
    
    if turma.alunos:
        return jsonify({'error': 'Não é possível deletar essa turma porque tem alunos vinculados!'}), 400
    
    db.session.delete(turma)
    db.session.commit()
    return jsonify({'message': 'Turma removida com sucesso!'}), 200

# ------------------------------------------------------------------