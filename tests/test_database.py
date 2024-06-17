import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from database import DatabaseManager

# @pytest.fixture
# def db():
#     db_manager = DatabaseManager()
#     yield db_manager
#     # Nettoyage après les tests, si nécessaire

# def test_create_jwt_key(db):
#     db.delete_all_jwt_keys()
#     db.insert_jwt_key('test_key')
#     key = db.get_jwt_key()
#     assert key == 'test_key'

# def test_delete_jwt_keys(db):
#     db.insert_jwt_key('another_test_key')
#     db.delete_all_jwt_keys()
#     key = db.get_jwt_key()
#     assert key is None
