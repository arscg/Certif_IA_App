import pytest
from flask import Flask
from flask_jwt_extended import create_access_token

# # Importe l'application Flask
# from app import app

# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     with app.test_client() as client:
#         yield client

# @pytest.fixture
# def auth_token():
#     # Crée un token JWT pour les tests
#     return create_access_token(identity="test_user")

# def test_token(client):
#     response = client.post('/animov/token')
#     assert response.status_code == 200
#     data = response.get_json()
#     assert 'access_token' in data

# def test_protected_route(client, auth_token):
#     headers = {
#         'Authorization': f'Bearer {auth_token}'
#     }
#     response = client.get('/animov/chevres_heures', headers=headers)
#     assert response.status_code == 200

# def test_protected_route_no_token(client):
#     response = client.get('/animov/chevres_heures')
#     assert response.status_code == 401
