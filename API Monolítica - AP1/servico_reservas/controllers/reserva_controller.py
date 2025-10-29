from flask import Blueprint, jsonify, request
from servico_reservas.models.reserva import Reserva
from models import db
from datetime import datetime
import requests

reserva_bp = Blueprint('reserva_bp', __name__)
url_gerenciamento = f"http://servico_gerenciamento:5000/turmas"

@reserva_bp.route('/', methods=['GET'])
def list_reservas():
    reservas = db.session.query(Reserva).all()
    return jsonify([reserva.to_dict() for reserva in reservas])

# ------------------------------------------------------------------

@reserva_bp.route('/', methods=['POST'])
def create_reserva():
    data = request.json

    # Validação de inteiro para turma
    try:
        turma_id = int(data.get('turma_id'))
    except ValueError:
        return jsonify({'error': 'ID Turma no formato errado! Utilize o número inteiro'}), 400
    
    # Validação de inteiro para número da sala
    try:
        num_sala = int(data.get('num_sala'))
    except (TypeError, ValueError):
        return jsonify({'error': 'Número da sala no formato errado! Utilize o número inteiro'}), 400

    # Validação para data
    try:
        data_reserva = datetime.strptime(data.get('data_reserva'), "%d-%m-%Y").date()
    except Exception:
        return jsonify({'error': 'Data no formato incorreto! Utilize DD-MM-YYYY'}), 400
    
    # Validação para lab
    novo_lab = data.get('lab')
    if not isinstance(novo_lab, bool):
        return jsonify({'error': 'Campo lab no formato errado! Utilize true ou false'}), 400

    # Validação de turma existente (Microserviço de Gerenciamento)
    try:
        turma_existente = requests.get(f"{url_gerenciamento}/{turma_id}")
        
        if turma_existente.status_code == 200:
            novaReserva = Reserva(
                num_sala = num_sala,
                lab = novo_lab,
                data_reserva = data_reserva,
                turma_id = turma_id
            )
            
            db.session.add(novaReserva)
            db.session.commit()
            return jsonify({
                'message': 'Reserva criada com sucesso!',
                'reserva': novaReserva.to_dict()
            }), 201

        elif turma_existente.status_code == 404:
            return jsonify({'error': 'Turma não encontrada!'}), 404
        
        else:
            return jsonify({'error': 'Erro ao verificar turma no microserviço de Gerenciamento!'}), 500
        
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Erro de comunicação com o microserviço de Gerenciamento!'}), 500

# ------------------------------------------------------------------

@reserva_bp.route('/<int:reserva_id>', methods=['PUT'])
def update_reserva(reserva_id):
    data = request.json
    reserva = db.session.query(Reserva).filter_by(id=reserva_id).first()

    if not reserva:
        return jsonify({'error': 'Reserva não encontrada!'}), 404

    # Validação de inteiro para turma
    try:
        reserva.turma_id = int(data.get('turma_id', reserva.turma_id))
    except (TypeError, ValueError):
        return jsonify({'error': 'ID Turma no formato errado! Utilize o número inteiro'}), 400

    # Validação de inteiro para número da sala
    try:
        reserva.num_sala = int(data.get('num_sala', reserva.num_sala))
    except (TypeError, ValueError):
        return jsonify({'error': 'Número da sala no formato errado! Utilize o número inteiro'}), 400

    # Validação para data da reserva
    data_reserva = data.get('data_reserva')
    if data_reserva:
        try:
            reserva.data_reserva = datetime.strptime(data_reserva, "%d-%m-%Y").date()
        except Exception:
            return jsonify({'error': 'Data da reserva no formato incorreto! Utilize DD-MM-YYYY'}), 400

    novo_lab = data.get('lab', reserva.lab)
    if not isinstance(novo_lab, bool):
        return jsonify({'error': 'Campo lab no formato errado! Utilize true ou false'}), 400
    reserva.lab = novo_lab

    # Validação de turma existente (Microserviço de Gerenciamento)
    try:
        turma_existente = requests.get(f"{url_gerenciamento}/{reserva.turma_id}")
        if turma_existente.status_code == 200:
            db.session.commit()
            return jsonify({
                'message': 'Reserva atualizada com sucesso!',
                'reserva': reserva.to_dict()
            }), 200

        elif turma_existente.status_code == 404:
            return jsonify({'error': 'Turma não encontrada!'}), 404
        
        else:
            return jsonify({'error': 'Erro ao verificar turma no microserviço de Gerenciamento!'}), 500

    except requests.exceptions.RequestException:
        return jsonify({'error': 'Erro de comunicação com o microserviço de Gerenciamento!'}), 500

# ------------------------------------------------------------------

@reserva_bp.route('/<int:reserva_id>', methods=['DELETE'])
def delete_reserva(reserva_id):
    reserva = db.session.query(Reserva).filter_by(id=reserva_id).first()

    if not reserva:
        return jsonify({'error': 'Reserva não encontrada!'}), 404

    db.session.delete(reserva)
    db.session.commit()
    return jsonify({'message': 'Reserva removida com sucesso!'}), 200