import pytest
import boto3
import os
from moto import mock_aws
from fastapi.testclient import TestClient

# Configura variáveis de ambiente ANTES de importar o app
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
os.environ["AWS_REGION"] = "us-east-1"
os.environ["DYNAMODB_TABLE"] = "dados-sprint01"

from main import app

client = TestClient(app)

@pytest.fixture
def tabela_fake():
    with mock_aws():
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        tabela = dynamodb.create_table(
            TableName="dados-sprint01",
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST"
        )
        tabela.wait_until_exists()
        yield tabela

def test_health_check():
    resposta = client.get("/")
    assert resposta.status_code == 200
    assert resposta.json()["sprint"] == 3

def test_criar_dado_sucesso(tabela_fake):
    payload = {"nome": "sensor_01", "valor": 23.5, "categoria": "ambiental"}
    resposta = client.post("/dados", json=payload)
    assert resposta.status_code == 201
    assert "id" in resposta.json()

def test_criar_dado_sem_nome(tabela_fake):
    payload = {"valor": 23.5}
    resposta = client.post("/dados", json=payload)
    assert resposta.status_code == 422

def test_criar_dado_valor_invalido(tabela_fake):
    payload = {"nome": "sensor_01", "valor": "texto"}
    resposta = client.post("/dados", json=payload)
    assert resposta.status_code == 422

def test_buscar_dado_existente(tabela_fake):
    payload = {"nome": "sensor_02", "valor": 10.0}
    post = client.post("/dados", json=payload)
    item_id = post.json()["id"]
    resposta = client.get(f"/dados/{item_id}")
    assert resposta.status_code == 200
    assert resposta.json()["id"] == item_id

def test_buscar_dado_inexistente(tabela_fake):
    resposta = client.get("/dados/id-inexistente")
    assert resposta.status_code == 404