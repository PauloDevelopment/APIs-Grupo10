from models import db

class Turma(db.Model):
    __tablename__ = "turmas"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'), nullable=False)

    professor = db.relationship('Professor', back_populates='turmas')
    alunos = db.relationship('Aluno', back_populates='turma')

    def __repr__(self):
        return f"<Turma {self.id} - {self.descricao}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'descricao': self.descricao,
            'ativo': "Ativa" if self.ativo else "Desativada",
            'professor_id': self.professor_id
    }