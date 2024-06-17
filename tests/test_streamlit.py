import pytest
from streamlit.testing.v1 import AppTest
import streamlit as st

# # Assurez-vous que votre application Streamlit est importée correctement
# from app_streamlit import app

# def test_streamlit_app():
#     # Initialiser l'application Streamlit avec StreamlitRunner
#     runner = StreamlitRunner(app)

#     # Simuler l'exécution de l'application
#     output = runner.run()

#     # Assurez-vous que certaines chaînes de texte ou widgets sont présents
#     assert "Bienvenue dans l'application Streamlit" in output.text
#     assert st.button("Cliquez-moi") is not None
