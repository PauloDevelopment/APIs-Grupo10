from flask import Blueprint, jsonify, request
from servico_atividades_notas.models.atividades import Atividade
from models import db
from datetime import datetime
import requests

atividade_bp = Blueprint('atividade_bp', __name__)
url_gerenciamento = f"http://servico_gerenciamento:5000"

@atividade_bp.route('/', methods=['GET'])
def list_atividades():
    atividades = db.session.query(Atividade).all()
    return jsonify([atividade.to_dict() for atividade in atividades])

# ------------------------------------------------------------------

@atividade_bp.route('/', methods=['POST'])
def create_atividade():
    data = request.json

    # Validação de inteiro para turma
    try:
        turma_id = int(data.get('turma_id'))
    except ValueError:
        return jsonify({'error': 'ID Turma no formato errado! Utilize o número inteiro'}), 400
    
    # Validação de inteiro para professor
    try:
        professor_id = int(data.get('professor_id'))
    except ValueError:
        return jsonify({'error': 'ID Professor no formato errado! Utilize o número inteiro'}), 400

    # Validação de inteiro para peso percentual
    try:
        peso_porcento = int(data.get('peso_porcento'))
    except (TypeError, ValueError):
        return jsonify({'error': 'Peso percentual no formato errado! Utilize o número inteiro'}), 400

    # Validação para data de entrega
    try:
        data_entrega = datetime.strptime(data.get('data_entrega'), "%d-%m-%Y").date()
    except Exception:
        return jsonify({'error': 'Data no formato incorreto! Utilize DD-MM-YYYY'}), 400

    # Validação de turma e professor existentes (Microserviço de Gerenciamento)
    try:
        turma_existente = requests.get(f"{url_gerenciamento}/turmas/{turma_id}")
        professor_existente = requests.get(f"{url_gerenciamento}/professores/{professor_id}")

        if turma_existente.status_code == 200 and professor_existente.status_code == 200:
            novaAtividade = Atividade(
                nome_atividade = data.get('nome_atividade'),
                descricao = data.get('descricao'),
                peso_porcento = peso_porcento,
                data_entrega = data_entrega,
                turma_id = turma_id,
                professor_id = professor_id
            )
            
            db.session.add(novaAtividade)
            db.session.commit()
            return jsonify({
                'message': 'Atividade criada com sucesso!',
                'atividade': novaAtividade.to_dict()
            }), 201

        elif turma_existente.status_code == 404:
            return jsonify({'error': 'Turma não encontrada!'}), 404
        
        elif professor_existente.status_code == 404:
            return jsonify({'error': 'Professor não encontrado!'}), 404
        
        else:
            return jsonify({'error': 'Erro ao verificar o microserviço de Gerenciamento!'}), 500
        
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Erro de comunicação com o microserviço de Gerenciamento!'}), 500

# ------------------------------------------------------------------

@atividade_bp.route('/<int:atividade_id>', methods=['PUT'])
def update_atividade(atividade_id):
    data = request.json
    atividade = db.session.query(Atividade).filter_by(id=atividade_id).first()

    if not atividade:
        return jsonify({'error': 'Atividade não encontrada!'}), 404

    # Validação de inteiro para turma
    try:
        atividade.turma_id = int(data.get('turma_id', atividade.turma_id))
    except (TypeError, ValueError):
        return jsonify({'error': 'ID Turma no formato errado! Utilize o número inteiro'}), 400

    # Validação de inteiro para professor
    try:
        atividade.professor_id = int(data.get('professor_id', atividade.professor_id))
    except (TypeError, ValueError):
        return jsonify({'error': 'ID Professor no formato errado! Utilize o número inteiro'}), 400

    # Validação de inteiro para peso percentual
    try:
        atividade.peso_porcento = int(data.get('peso_porcento', atividade.peso_porcento))
    except (TypeError, ValueError):
        return jsonify({'error': 'Peso percentual no formato errado! Utilize o número inteiro'}), 400

    # Validação para data de entrega
    data_entrega = data.get('data_entrega')
    if data_entrega:
        try:
            atividade.data_entrega = datetime.strptime(data_entrega, "%d-%m-%Y").date()
        except Exception:
            return jsonify({'error': 'Data de entrega no formato incorreto! Utilize DD-MM-YYYY'}), 400
        
    atividade.nome_atividade = data.get('nome_atividade', atividade.nome_atividade)
    atividade.descricao = data.get('descricao', atividade.descricao)

    # Validação de turma e professor existente (Microserviço de Gerenciamento)
    try:
        turma_existente = requests.get(f"{url_gerenciamento}/turmas/{atividade.turma_id}")
        professor_existente = requests.get(f"{url_gerenciamento}/professores/{atividade.professor_id}")

        if turma_existente.status_code == 200 and professor_existente.status_code == 200:
            db.session.commit()
            return jsonify({
                'message': 'Atividade atualizada com sucesso!',
                'atividade': atividade.to_dict()
            }), 200

        elif turma_existente.status_code == 404:
            return jsonify({'error': 'Turma não encontrada!'}), 404
        
        elif professor_existente.status_code == 404:
            return jsonify({'error': 'Professor não encontrado!'}), 404
        
        else:
            return jsonify({'error': 'Erro ao verificar o microserviço de Gerenciamento!'}), 500

    except requests.exceptions.RequestException:
        return jsonify({'error': 'Erro de comunicação com o microserviço de Gerenciamento!'}), 500

# ------------------------------------------------------------------

@atividade_bp.route('/<int:atividade_id>', methods=['DELETE'])
def delete_atividade(atividade_id):
    atividade = db.session.query(Atividade).filter_by(id=atividade_id).first()

    if not atividade:
        return jsonify({'error': 'Atividade não encontrada!'}), 404

    db.session.delete(atividade)
    db.session.commit()
    return jsonify({'message': 'Atividade removida com sucesso!'}), 200