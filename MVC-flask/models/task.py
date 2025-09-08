from models import db

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(100), nullable=False, default='Pendente')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship('User', back_populates='task')

    def __repr__(self):
        return f"<Task {self.title} - {self.status}>"