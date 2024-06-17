from flask import Flask
import tracemalloc
from flask_jwt_extended import JWTManager
from routes import configure_routes
from flask_restx import Api
# from database import db_manager

app = Flask(__name__)

# # Récupération de la clé JWT depuis la base de données
# jwt_key = db_manager.get_jwt_key()
# if jwt_key is None:
#     jwt_key = 'fallback_secret_key'
# app.config['JWT_SECRET_KEY'] = jwt_key

# jwt = JWTManager(app)

# api = Api(app, version='1.0', title='Animal Behavior API',
#           description='A simple API for managing animal behavior data')

# configure_routes(app, api)

tracemalloc.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
