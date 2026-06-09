import pytest
import boto3
import os
from moto import mock_aws
from fastapi.testclient import TestClient
from unittest.mock import patch

# Configura variáveis de ambiente ANTES de importar o app
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
os.environ["AWS_REGION"] = "us-east-1"
os.environ["DYNAMODB_TABLE"] = "dados-sprint01"

from main import app

client = TestClient(app)

# --- Fixture: cria tabela falsa antes de cada teste ---
@pytest.fixture
def tabela_fake():
    with mock_aws():
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        tabela = dynamodb.create_table(
            TableName="dados-sprint01",
            KeySchema=[
                {"AttributeName": "id", "KeyType": "HASH"}
            ],
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "S"}
            ],
            BillingMode="PAY_PER_REQUEST"
        )
        tabela.wait_until_exists()
        yield tabela  # os testes rodam aqui
        # depois do yield o moto limpa tudo automaticamente


# =====================
# Testes do GET /
# =====================

def test_health_check():
    resposta = client.get("/")
    assert resposta.status_code == 200
    assert resposta.json()["mensagem"] == "API no ar!"


# =====================
# Testes do POST /dados
# =====================

def test_criar_dado_sucesso(tabela_fake):
    payload = {
        "nome": "temperatura_sensor_01",
        "valor": 23.5,
        "categoria": "ambiental"
    }
    resposta = client.post("/dados", json=payload)

    assert resposta.status_code == 201
    assert "id" in resposta.json()
    assert resposta.json()["mensagem"] == "Dado salvo com sucesso"


def test_criar_dado_sem_nome(tabela_fake):
    payload = {
        "valor": 23.5,
        "categoria": "ambiental"
    }
    resposta = client.post("/dados", json=payload)

    assert resposta.status_code == 422


def test_criar_dado_valor_invalido(tabela_fake):
    payload = {
        "nome": "sensor_01",
        "valor": "isso_nao_e_numero",
        "categoria": "ambiental"
    }
    resposta = client.post("/dados", json=payload)

    assert resposta.status_code == 422


def test_criar_dado_nome_muito_curto(tabela_fake):
    payload = {
        "nome": "x",
        "valor": 10.0
    }
    resposta = client.post("/dados", json=payload)

    assert resposta.status_code == 422


def test_criar_dado_categoria_default(tabela_fake):
    payload = {
        "nome": "sensor_pressao",
        "valor": 101.3
        # categoria não enviada — deve usar o default "geral"
    }
    resposta = client.post("/dados", json=payload)

    assert resposta.status_code == 201


# =====================
# Testes do GET /dados/{id}
# =====================

def test_buscar_dado_existente(tabela_fake):
    # Primeiro cria um dado
    payload = {"nome": "sensor_temp", "valor": 36.6, "categoria": "saude"}
    post = client.post("/dados", json=payload)
    item_id = post.json()["id"]

    # Depois busca pelo ID retornado
    resposta = client.get(f"/dados/{item_id}")

    assert resposta.status_code == 200
    assert resposta.json()["id"] == item_id
    assert resposta.json()["nome"] == "sensor_temp"


def test_buscar_dado_inexistente(tabela_fake):
    resposta = client.get("/dados/id-que-nao-existe")

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Dado não encontrado"