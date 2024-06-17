from flask import request, jsonify, send_file
from flask_restx import Resource, fields
from flask_jwt_extended import jwt_required, create_access_token
from database import db_manager
from statistics import calculate_global_stats, calculate_frame_stats
import tracemalloc
import os
from mlflow.tracking import MlflowClient
import mlflow
from config import config

def configure_routes(app, api):
    ns = api.namespace('animov', description='Operations related to animal data')

    data_model = api.model('Data', {
        'source_id': fields.Integer(required=True, description='ID de la source'),
        'couche': fields.Integer(required=True, description='Nombre de chèvres couchées'),
        'debout': fields.Integer(required=True, description='Nombre de chèvres debout'),
        'timestamp': fields.Integer(required=True, description='Horodatage des données')
    })

    @ns.route('/token')
    class Token(Resource):
        def post(self):
            """
            Génère un token JWT pour un accès sécurisé.
            """
            return jsonify(access_token=create_access_token(identity="machine_user"))

    @ns.route('/jwt_key')
    class JWTKey(Resource):
        @jwt_required()
        def get(self):
            """
            Récupère la clé JWT actuelle.
            """
            key = db_manager.get_jwt_key()
            if key:
                return {"jwt_key": key}, 200
            else:
                return {"message": "No key found"}, 404

        @jwt_required()
        def post(self):
            """
            Met à jour la clé JWT.
            """
            new_key = request.json.get("key")
            if not new_key:
                return {"message": "New key required"}, 400

            db_manager.delete_all_jwt_keys()
            db_manager.insert_jwt_key(new_key)
            return {"message": "JWT key updated"}, 200

    @ns.route('/receive_data_animov')
    class ReceiveData(Resource):
        @ns.expect(data_model, validate=True)
        @ns.response(201, 'Data successfully received and processed.')
        @jwt_required()  # Protéger cette route avec JWT
        def post(self):
            """
            Reçoit les données d'animaux et les traite.
            """
            data = api.payload
            db_manager.insert_data(data)
            
            sources = list(set(item['source_id'] for item in data))
            global_stats = calculate_global_stats(data, sources)
            frame_stats = calculate_frame_stats(data)
            
            return {
                "status": "Data received and processed",
                "global_stats": global_stats,
                "frame_stats": frame_stats
            }, 201

    @ns.route('/get_data_animov_ch')
    class GetDataAnimov(Resource):
        @ns.param('sources', 'Liste des sources à inclure')
        @ns.param('with_images', 'Inclure les images (True/False)')
        @ns.param('with_detect', 'Inclure les détections (True/False)')
        @ns.param('with_stats', 'Inclure les statistiques (Lite/True)')
        @ns.param('with_global_stats', 'Inclure les statistiques globales (True/False)')
        @jwt_required()  # Protéger cette route avec JWT
        def get(self):
            """
            Récupère les données filtrées et génère des statistiques.
            """
            sources = request.args.get('sources').split(',')
            with_images = request.args.get('with_images') == 'True'
            with_detect = request.args.get('with_detect') == 'True'
            with_stats = request.args.get('with_stats')
            with_global_stats = request.args.get('with_global_stats') == 'True'

            data = db_manager.fetch_data()

            if with_stats == 'Lite':
                stats = calculate_frame_stats(data)
            elif with_stats == 'True':
                stats = calculate_frame_stats(data)

            if with_global_stats:
                global_stats = calculate_global_stats(data, sources)

            response = {"data": data, "stats": stats, "global_stats": global_stats}
            return response, 200

    @ns.route('/chevres_heures')
    class ChevresHeures(Resource):
        @jwt_required()  # Protéger cette route avec JWT
        def get(self):
            """
            Récupère les données des chèvres par heure.
            """
            data = db_manager.query_get_chevres_heure()
            return data, 200

    @ns.route('/chevres_minutes')
    class ChevresMinutes(Resource):
        @jwt_required()  # Protéger cette route avec JWT
        def get(self):
            """
            Récupère les données des chèvres par minute.
            """
            data = db_manager.query_get_chevres_minutes()
            return data, 200

    @ns.route('/sources')
    class Sources(Resource):
        @jwt_required()  # Protéger cette route avec JWT
        def get(self):
            """
            Récupère la liste des sources distinctes.
            """
            data = db_manager.query_get_sources()
            return data, 200

    @ns.route('/dates')
    class Dates(Resource):
        @jwt_required()  # Protéger cette route avec JWT
        def get(self):
            """
            Récupère la liste des dates distinctes.
            """
            data = db_manager.query_get_dates()
            return data, 200

    @ns.route('/stats_minute')
    class StatsMinute(Resource):
        @jwt_required()  # Protéger cette route avec JWT
        def get(self):
            """
            Récupère les statistiques par minute.
            """
            data = db_manager.query_get_stats_minute()
            return data, 200

    @ns.route('/stats_heure')
    class StatsHeure(Resource):
        @jwt_required()  # Protéger cette route avec JWT
        def get(self):
            """
            Récupère les statistiques par heure.
            """
            data = db_manager.query_get_stats_heure()
            return data, 200

    @ns.route('/get_serie_heure')
    class SerieHeure(Resource):
        @jwt_required()  # Protéger cette route avec JWT
        def get(self):
            """
            Récupère les séries de données horaires.
            """
            data = db_manager.query_get_serie_heure()
            return data, 200

    @ns.route('/get_serie_jour')
    class SerieJour(Resource):
        @jwt_required()  # Protéger cette route avec JWT
        def get(self):
            """
            Récupère les séries de données journalières.
            """
            data = db_manager.query_get_serie_jour()
            return data, 200

    @ns.route('/get_serie_last_heure')
    class SerieLastHeure(Resource):
        @jwt_required()  # Protéger cette route avec JWT
        def get(self):
            """
            Récupère les séries de données de la dernière heure.
            """
            data = db_manager.query_get_serie_last_heure()
            return data, 200

    @ns.route('/get_serie_last_jour')
    class SerieLastJour(Resource):
        @jwt_required()  # Protéger cette route avec JWT
        def get(self):
            """
            Récupère les séries de données du dernier jour.
            """
            data = db_manager.query_get_serie_last_jour()
            return data, 200

    @ns.route('/trace')
    class Trace(Resource):
        @jwt_required()  # Protéger cette route avec JWT
        def get(self):
            """
            Fournit des informations de suivi de la mémoire.
            """
            snapshot = tracemalloc.take_snapshot()
            top_stats = snapshot.statistics('lineno')
            top_stats = [{"file": stat.traceback[0].filename, "line": stat.traceback[0].lineno, "size": stat.size} for stat in top_stats[:10]]
            return top_stats, 200

    @ns.route('/download-model/<model_name>')
    class DownloadModel(Resource):
        @jwt_required()  # Protéger cette route avec JWT
        def get(self, model_name):
            """
            Télécharge le modèle spécifié à partir de MLflow.
            """
            mlflow.set_tracking_uri(config['MLFLOW_TRACKING_URI'])
            client = MlflowClient()
            latest_versions = client.get_latest_versions(model_name, stages=["None", "Staging", "Production"])
            latest_version = latest_versions[0] if latest_versions else None

            if latest_version:
                local_path = client.download_artifacts(run_id=latest_version.run_id, path="models")
                for root, dirs, files in os.walk(local_path):
                    for file in files:
                        if file.endswith(".pth"):
                            full_file_path = os.path.join(root, file)
                            return send_file(full_file_path, as_attachment=True)
            return {"message": "No model version available"}, 404
