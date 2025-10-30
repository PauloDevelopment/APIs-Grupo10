from flask import Flask
from flasgger import Swagger
from config import Config
from models import db
from flask_cors import CORS

from controllers.aluno_controller import aluno_bp
from controllers.professor_controller import professor_bp
from controllers.turma_controller import turma_bp

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config.from_object(Config)

db.init_app(app)

CORS(app)

@app.after_request
def set_utf8_charset(response):
    if response.mimetype == 'application/json':
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

swagger = Swagger(app, template_file='swagger.json')

app.register_blueprint(aluno_bp, url_prefix="/alunos")
app.register_blueprint(professor_bp, url_prefix="/professores")
app.register_blueprint(turma_bp, url_prefix="/turmas")

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")