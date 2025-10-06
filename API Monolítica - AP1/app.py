from flask import Flask
from flasgger import Swagger
from config import Config
from models import db

from controllers.aluno_controller import aluno_bp
from controllers.professor_controller import professor_bp
from controllers.turma_controller import turma_bp

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config.from_object(Config)

db.init_app(app)

swagger = Swagger(app, template_file='swagger.json')

app.register_blueprint(aluno_bp, url_prefix="/alunos")
app.register_blueprint(professor_bp, url_prefix="/professores")
app.register_blueprint(turma_bp, url_prefix="/turmas")

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5002)