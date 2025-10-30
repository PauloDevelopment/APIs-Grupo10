from flask import Flask
from flasgger import Swagger
from config import Config
from models import db
from flask_cors import CORS

from controllers.reserva_controller import reserva_bp

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

app.register_blueprint(reserva_bp, url_prefix="/reservas")

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5001, host="0.0.0.0")