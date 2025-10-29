from flask import Blueprint, jsonify, request
from servico_atividades_notas.models.atividades import Atividade
from servico_atividades_notas.models.notas import Nota
from models import db
import requests

nota_bp = Blueprint('nota_bp', __name__)
url_gerenciamento = f"http://servico_gerenciamento:5000/alunos"

@nota_bp.route('/', methods=['GET'])
def list_notas():
    notas = db.session.query(Nota).all()
    return jsonify([nota.to_dict() for nota in notas])

# ------------------------------------------------------------------

@nota_bp.route('/', methods=['POST'])
def create_nota():
    data = request.json

    # Validação de inteiro para aluno
    try:
        aluno_id = int(data.get('aluno_id'))
    except ValueError:
        return jsonify({'error': 'ID Aluno no formato errado! Utilize o número inteiro'}), 400

    # Validação de inteiro para atividade
    try:
        atividade_id = int(data.get('atividade_id'))
    except ValueError:
        return jsonify({'error': 'ID Atividade no formato errado! Utilize o número inteiro'}), 400

    # Validação para nota
    try:
        nota = float(data.get('nota'))
    except (TypeError, ValueError):
        return jsonify({'error': 'Nota no formato errado! Utilize o número float'}), 400
    
    # Validação de atividade existente
    atividade = db.session.query(Atividade).filter_by(id=atividade_id).first()
    if not atividade:
        return jsonify({'error': 'Atividade não encontrada!'}), 404
    
    # Validação de alunos existentes (Microserviço de Gerenciamento)
    try:
        aluno_existente = requests.get(f"{url_gerenciamento}/{aluno_id}")

        if aluno_existente.status_code == 200:
            novaNota = Nota(
                nota = nota,
                aluno_id = aluno_id,
                atividade_id = atividade_id
            )

            db.session.add(novaNota)
            db.session.commit()
            return jsonify({
                'message': 'Nota criada com sucesso!',
                'nota': novaNota.to_dict()
            }), 201

        elif aluno_existente.status_code == 404:
            return jsonify({'error': 'Aluno não encontrado!'}), 404

        else:
            return jsonify({'error': 'Erro ao verificar aluno no microserviço de Gerenciamento!'}), 500
        
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Erro de comunicação com o microserviço de Gerenciamento!'}), 500

# ------------------------------------------------------------------

@nota_bp.route('/<int:nota_id>', methods=['PUT'])
def update_nota(nota_id):
    data = request.json
    nota = db.session.query(Nota).filter_by(id=nota_id).first()

    if not nota:
        return jsonify({'error': 'Nota não encontrada!'}), 404

    # Validação de inteiro para aluno
    try:
        nota.aluno_id = int(data.get('aluno_id', nota.aluno_id))
    except (TypeError, ValueError):
        return jsonify({'error': 'ID Aluno no formato errado! Utilize o número inteiro'}), 400

    # Validação de inteiro para atividade
    try:
        nota.atividade_id = int(data.get('atividade_id', nota.atividade_id))
    except (TypeError, ValueError):
        return jsonify({'error': 'ID Atividade no formato errado! Utilize o número inteiro'}), 400

    # Validação de nota
    try:
        nota.nota = float(data.get('nota', nota.nota))
    except (TypeError, ValueError):
        return jsonify({'error': 'Nota no formato errado! Utilize o número float'}), 400
    
    # Validação de atividade existente
    atividade = db.session.query(Atividade).filter_by(id=nota.atividade_id).first()
    if not atividade:
        return jsonify({'error': 'Atividade não encontrada!'}), 404

    # Validação de aluno existente (Microserviço de Gerenciamento)
    try:
        aluno_existente = requests.get(f"{url_gerenciamento}/{nota.aluno_id}")

        if aluno_existente.status_code == 200:
            db.session.commit()
            return jsonify({
                'message': 'Nota atualizada com sucesso!',
                'nota': nota.to_dict()
            }), 200

        elif aluno_existente.status_code == 404:
            return jsonify({'error': 'Aluno não encontrado!'}), 404
        
        else:
            return jsonify({'error': 'Erro ao verificar aluno no microserviço de Gerenciamento!'}), 500

    except requests.exceptions.RequestException:
        return jsonify({'error': 'Erro de comunicação com o microserviço de Gerenciamento!'}), 500

# ------------------------------------------------------------------

@nota_bp.route('/<int:nota_id>', methods=['DELETE'])
def delete_nota(nota_id):
    nota = db.session.query(Nota).filter_by(id=nota_id).first()

    if not nota:
        return jsonify({'error': 'Nota não encontrada!'}), 404

    db.session.delete(nota)
    db.session.commit()
    return jsonify({'message': 'Nota removida com sucesso!'}), 200