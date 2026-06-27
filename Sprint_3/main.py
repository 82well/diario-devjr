from fastapi import FastAPI, HTTPException
from mangum import Mangum
from pydantic import BaseModel, Field
from datetime import datetime
import boto3
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="API de Ingestão de Dados",
    description="Sprint 03 — Deploy Lambda + CI/CD",
    version="0.3.0"
)

class DadoEntrada(BaseModel):
    nome: str = Field(..., min_length=2, description="Nome do dado")
    valor: float = Field(..., description="Valor numérico")
    categoria: str = Field(default="geral", description="Categoria")

def get_table():
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    return dynamodb.Table(os.getenv("DYNAMODB_TABLE", "dados-sprint01"))

@app.get("/")
def raiz():
    return {"mensagem": "API no ar!", "sprint": 3, "deploy": "Lambda"}

@app.post("/dados", status_code=201)
def criar_dado(dado: DadoEntrada):
    tabela = get_table()
    item = {
        "id": str(uuid.uuid4()),
        "nome": dado.nome,
        "valor": str(dado.valor),
        "categoria": dado.categoria,
        "criado_em": datetime.now().isoformat()
    }
    tabela.put_item(Item=item)
    return {"mensagem": "Dado salvo com sucesso", "id": item["id"]}

@app.get("/dados/{item_id}")
def buscar_dado(item_id: str):
    tabela = get_table()
    resposta = tabela.get_item(Key={"id": item_id})
    item = resposta.get("Item")
    if not item:
        raise HTTPException(status_code=404, detail="Dado não encontrado")
    return item

# Handler para o Lambda — esta linha é o que conecta o FastAPI ao Lambda
handler = Mangum(app)