import pandas as pd
import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.engine.url import URL
from config import config

class DatabaseManager:
    def __init__(self):
        self.engine = sqlalchemy.create_engine(self.connection())

    def connection(self):
        db_info = config['database']
        return URL.create(
            drivername=f"{db_info['type']}+{db_info['driver']}",
            username=db_info['username'],
            password=db_info['password'],
            host=db_info['host'],
            port=db_info['port'],
            database=db_info['database_name']
        )

    def create_jwt_table(self):
        metadata = MetaData()

        jwt_table = Table('jwt_keys', metadata,
                          Column('id', Integer, primary_key=True, autoincrement=True),
                          Column('key', String(256), nullable=False))

        metadata.create_all(self.engine)

    def get_jwt_key(self):
        sql_query = "SELECT key FROM jwt_keys LIMIT 1"
        with self.engine.connect() as connection:
            result = connection.execute(sql_query)
            row = result.fetchone()
            if row:
                return row['key']
            else:
                return None

    def insert_jwt_key(self, key):
        metadata = MetaData()
        jwt_table = Table('jwt_keys', metadata,
                          Column('id', Integer, primary_key=True, autoincrement=True),
                          Column('key', String(256), nullable=False))

        metadata.create_all(self.engine)
        with self.engine.connect() as connection:
            connection.execute(jwt_table.insert().values(key=key))
            connection.commit()

    def delete_all_jwt_keys(self):
        sql_query = "DELETE FROM jwt_keys"
        with self.engine.connect() as connection:
            connection.execute(sql_query)
            connection.commit()

    def fetch_data(self):
        """
        Récupère toutes les données de la table 'data_table'.
        """
        with self.engine.connect() as connection:
            result = connection.execute("SELECT * FROM data_table")
            return [dict(row) for row in result]

    def insert_data(self, data):
        """
        Insère des données dans la table 'data_table'.
        """
        metadata = MetaData()
        data_table = Table('data_table', metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('source_id', Integer, nullable=False),
            Column('couche', Integer, nullable=False),
            Column('debout', Integer, nullable=False),
            Column('timestamp', BigInteger, nullable=False)
        )
        metadata.create_all(self.engine)
        with self.engine.connect() as connection:
            connection.execute(
                data_table.insert().values(
                    source_id=data['source_id'],
                    couche=data['couche'],
                    debout=data['debout'],
                    timestamp=data['timestamp']
                )
            )
            connection.commit()

    def query_get_sources(self):
        """
        Récupère la liste des sources distinctes.
        """
        sql_query = "SELECT source FROM data_table GROUP BY source"
        with self.engine.connect() as connection:
            df = pd.read_sql(sql_query, connection)
        return df

    def query_get_dates(self):
        """
        Récupère la liste des dates distinctes.
        """
        sql_query = "SELECT jour AS dates FROM data_table GROUP BY jour"
        with self.engine.connect() as connection:
            df = pd.read_sql(sql_query, connection)
        return df

    def query_get_chevres_heure(self):
        """
        Récupère les données des chèvres par heure.
        """
        sql_query = """
        SELECT jour, source, heure, AVG(brush) AS brush, AVG(drink) AS drink, 
               AVG(eat) AS eat, AVG(class_0) AS class_0, AVG(class_1) AS class_1
        FROM data_table 
        GROUP BY jour, source, heure
        """
        with self.engine.connect() as connection:
            df = pd.read_sql(sql_query, connection)
        return df

    def query_get_chevres_minutes(self):
        """
        Récupère les données des chèvres par minute.
        """
        sql_query = """
        SELECT jour, source, minutes, heure, AVG(brush) AS brush, AVG(drink) AS drink, 
               AVG(eat) AS eat, AVG(class_0) AS class_0, AVG(class_1) AS class_1
        FROM data_table 
        GROUP BY jour, source, minutes, heure
        """
        with self.engine.connect() as connection:
            df = pd.read_sql(sql_query, connection)
        return df

    def query_get_stats_minute(self):
        """
        Récupère les statistiques par minute.
        """
        sql_query = "SELECT * FROM data_table WHERE period = 'minute'"
        with self.engine.connect() as connection:
            df = pd.read_sql(sql_query, connection)
        return df

    def query_get_stats_heure(self):
        """
        Récupère les statistiques par heure.
        """
        sql_query = "SELECT * FROM data_table WHERE period = 'hour'"
        with self.engine.connect() as connection:
            df = pd.read_sql(sql_query, connection)
        return df

    def query_get_serie_jour(self):
        """
        Récupère les séries de données journalières.
        """
        sql_query = "SELECT * FROM data_table WHERE period = 'day'"
        with self.engine.connect() as connection:
            df = pd.read_sql(sql_query, connection)
        return df

    def query_get_serie_heure(self):
        """
        Récupère les séries de données horaires.
        """
        sql_query = "SELECT * FROM data_table WHERE period = 'hour'"
        with self.engine.connect() as connection:
            df = pd.read_sql(sql_query, connection)
        return df

    def query_get_serie_last_jour(self):
        """
        Récupère les séries de données du dernier jour.
        """
        sql_query = "SELECT * FROM data_table WHERE period = 'last_day'"
        with self.engine.connect() as connection:
            df = pd.read_sql(sql_query, connection)
        return df

    def query_get_serie_last_heure(self):
        """
        Récupère les séries de données de la dernière heure.
        """
        sql_query = "SELECT * FROM data_table WHERE period = 'last_hour'"
        with self.engine.connect() as connection:
            df = pd.read_sql(sql_query, connection)
        return df


db_manager = DatabaseManager()
db_manager.create_jwt_table()  # Création de la table lors de l'initialisation
