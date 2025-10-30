from flask import Blueprint, jsonify, request
from models.aluno import Aluno
from models.turma import Turma
from models import db
from datetime import datetime

aluno_bp = Blueprint('aluno_bp', __name__)

@aluno_bp.route('/', methods=['GET'])
def list_alunos():
    alunos = db.session.query(Aluno).all()
    return jsonify([aluno.to_dict() for aluno in alunos])

# ------------------------------------------------------------------

@aluno_bp.route('/<int:aluno_id>', methods=['GET'])
def get_aluno(aluno_id):
    aluno = db.session.query(Aluno).filter_by(id=aluno_id).first()

    if not aluno:
        return jsonify({'error': 'Aluno não encontrado!'}), 404
    
    return jsonify(aluno.to_dict()), 200

# ------------------------------------------------------------------

@aluno_bp.route('/', methods=['POST'])
def create_aluno():
    data = request.json

    # Validação de inteiro para turma
    try:
        turma_id = int(data.get('turma_id'))
    except ValueError:
        return jsonify({'error': 'ID Turma no formato errado! Utilize o número inteiro'}), 400
    
    # Validação de turma existente
    turma_existente = db.session.query(Turma).filter_by(id=turma_id).first()
    if not turma_existente:
        return jsonify ({'error': 'Turma não encontrada!'}), 404
    
    # Validação de inteiro para idade
    try:
        idade = int(data.get('idade'))
    except (TypeError, ValueError):
        return jsonify({'error': 'Idade no formato errado! Utilize o número inteiro'}), 400
    
    # Validação notas
    try:
        nota_primeiro_semestre = float(data.get('nota_primeiro_semestre'))
        nota_segundo_semestre = float(data.get('nota_segundo_semestre'))
    except (TypeError, ValueError):
        return jsonify({'error': 'Nota no formato errado! Utilize o número float'}), 400
    
    # Validação para data de nascimento
    try:
        data_nascimento = datetime.strptime(data.get('data_nascimento'), "%d-%m-%Y").date()
    except Exception:
        return jsonify({'error': 'Data de nascimento no formato incorreto! Utilize DD-MM-YYYY'}), 400
    
    novoAluno = Aluno(
        nome = data.get('nome'),
        idade = idade,
        turma_id = turma_id,
        data_nascimento = data_nascimento,
        nota_primeiro_semestre = nota_primeiro_semestre,
        nota_segundo_semestre = nota_segundo_semestre,
        media_final = (nota_primeiro_semestre + nota_segundo_semestre) / 2
    )

    db.session.add(novoAluno)
    db.session.commit()
    return jsonify({
        'message': 'Aluno criado com sucesso!',
        'aluno': novoAluno.to_dict()
    }), 201

# ------------------------------------------------------------------

@aluno_bp.route('/<int:aluno_id>', methods=['PUT'])
def update_aluno(aluno_id):
    data = request.json
    aluno = db.session.query(Aluno).filter_by(id=aluno_id).first()

    if not aluno:
        return jsonify({'error': 'Aluno não encontrado!'}), 404

    # Validação de inteiro para turma
    try:
        aluno.turma_id = int(data.get('turma_id', aluno.turma_id))
    except (TypeError, ValueError):
        return jsonify({'error': 'ID Turma no formato errado! Utilize o número inteiro'}), 400

    # Validação de turma existente
    turma_existente = db.session.query(Turma).filter_by(id=aluno.turma_id).first()
    if not turma_existente:
        return jsonify ({'error': 'Turma não encontrada!'}), 404

    # Validação de inteiro para idade
    try:
        aluno.idade = int(data.get('idade', aluno.idade))
    except (TypeError, ValueError):
        return jsonify({'error': 'Idade no formato errado! Utilize o número inteiro'}), 400

    # Validação notas
    try:
        aluno.nota_primeiro_semestre = float(data.get('nota_primeiro_semestre', aluno.nota_primeiro_semestre))
        aluno.nota_segundo_semestre = float(data.get('nota_segundo_semestre', aluno.nota_segundo_semestre))
    except (TypeError, ValueError):
        return jsonify({'error': 'Nota no formato errado! Utilize o número float'}), 400

    # Validação para data de nascimento
    data_nascimento = data.get('data_nascimento')
    if data_nascimento:
        try:
            aluno.data_nascimento = datetime.strptime(data_nascimento, "%d-%m-%Y").date()
        except Exception:
            return jsonify({'error': 'Data de nascimento no formato incorreto! Utilize DD-MM-YYYY'}), 400
    
    aluno.nome = data.get('nome', aluno.nome)
    aluno.media_final = (aluno.nota_primeiro_semestre + aluno.nota_segundo_semestre) / 2

    db.session.commit()
    return jsonify({
        'message': 'Aluno atualizado com sucesso!',
        'aluno': aluno.to_dict()
    }), 200

# ------------------------------------------------------------------

@aluno_bp.route('/<int:aluno_id>', methods=['DELETE'])
def delete_aluno(aluno_id):
    aluno = db.session.query(Aluno).filter_by(id=aluno_id).first()

    if not aluno:
        return jsonify({'error': 'Aluno não encontrado!'}), 404
    
    db.session.delete(aluno)
    db.session.commit()
    return jsonify({'message': 'Aluno removido com sucesso!'}), 200