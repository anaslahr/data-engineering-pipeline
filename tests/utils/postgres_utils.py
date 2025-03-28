import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class PostgresClient:
    def __init__(self):
        """Initialise la connexion à PostgreSQL."""
        self.connection = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

    def execute_query(self, query, params=None):
        """Exécute une requête SQL."""
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetch_one(self, query, params=None):
        """Récupère une seule ligne."""
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetch_all(self, query, params=None):
        """Récupère toutes les lignes."""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        """Ferme la connexion."""
        self.cursor.close()
        self.connection.close()