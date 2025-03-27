import pytest
from utils.postgres_utils import PostgresClient

@pytest.fixture(scope="module")
def postgres_client():
    """Fixture pour initialiser le client PostgreSQL."""
    client = PostgresClient()
    yield client
    client.close()

@pytest.fixture(scope="module")
def create_test_table(postgres_client):
    """Fixture pour créer une table de test."""
    postgres_client.execute_query("""
        CREATE TABLE IF NOT EXISTS test_table (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50)
        );
    """)
    yield
    postgres_client.execute_query("DROP TABLE IF EXISTS test_table;")

def test_postgres_connection(postgres_client):
    """Test pour vérifier la connexion à PostgreSQL."""
    result = postgres_client.fetch_one("SELECT 1;")
    assert result is not None
    assert list(result.values())[0] == 1  # Vérifie que le résultat est 1

def test_insert_and_query_data(postgres_client, create_test_table):
    """Test pour insérer et interroger des données."""
    # Insérer des données
    postgres_client.execute_query(
        "INSERT INTO test_table (name) VALUES (%s) RETURNING id;",
        ("Test Name",)
    )
    inserted_id = postgres_client.fetch_one("SELECT id FROM test_table WHERE name = %s;", ("Test Name",))["id"]
    assert inserted_id is not None

    # Vérifier les données insérées
    result = postgres_client.fetch_one("SELECT * FROM test_table WHERE id = %s;", (inserted_id,))
    assert result["name"] == "Test Name"