from models import db

class Reserva(db.Model):
    __tablename__ = 'reservas'

    id = db.Column(db.Integer, primary_key=True)
    num_sala = db.Column(db.Integer, nullable=False)
    lab = db.Column(db.Boolean, default=False)
    data_reserva = db.Column(db.Date, nullable=False)
    turma_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Reserva {self.id}>, Sala {self.num_sala}"

    def to_dict(self):
        return {
            'id': self.id,
            'num_sala': self.num_sala,
            'lab': "Disponível" if self.lab else "Indisponível",
            'data_reserva': self.data_reserva.strftime('%d-%m-%Y'),
            'turma_id': self.turma_id
    }