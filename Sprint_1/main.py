from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from database import get_table
import uuid

# --- Metadados da API ---
description = """
## API de Ingestão de Dados

Projeto desenvolvido como parte do **Diário de um Dev Jr** em recolocação.

### O que essa API faz
* Recebe dados via endpoint POST e persiste no DynamoDB
* Permite buscar dados individuais por ID
* Serve como base para um pipeline de dados na AWS

### Tecnologias
* FastAPI + Python
* AWS DynamoDB via boto3
"""

tags_metadata = [
    {
        "name": "health",
        "description": "Verificação de saúde da API."
    },
    {
        "name": "dados",
        "description": "Operações de ingestão e consulta de dados no DynamoDB."
    }
]

app = FastAPI(
    title="API de Ingestão de Dados",
    description=description,
    version="0.1.0",
    contact={
        "name": "Wellington",
        "url": "https://github.com/82well/Diario_Dev_Jr_Sprint_1_FastAPI",
    },
    license_info={
        "name": "MIT",
    },
    openapi_tags=tags_metadata
)

# --- Modelo Pydantic com exemplos ---
class DadoEntrada(BaseModel):
    nome: str = Field(
        ...,
        min_length=2,
        description="Nome identificador do dado",
        examples=["temperatura_sensor_01"]
    )
    valor: float = Field(
        ...,
        description="Valor numérico capturado",
        examples=[23.5]
    )
    categoria: str = Field(
        default="geral",
        description="Categoria para classificação do dado",
        examples=["ambiental"]
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nome": "temperatura_sensor_01",
                    "valor": 23.5,
                    "categoria": "ambiental"
                }
            ]
        }
    }

class DadoResposta(BaseModel):
    id: str = Field(description="ID único gerado automaticamente")
    nome: str = Field(description="Nome do dado")
    valor: str = Field(description="Valor numérico em string")
    categoria: str = Field(description="Categoria do dado")
    criado_em: str = Field(description="Timestamp de criação no formato ISO 8601")

# --- Endpoints ---
@app.get(
    "/",
    tags=["health"],
    summary="Health check",
    description="Verifica se a API está no ar e retorna informações básicas."
)
def raiz():
    return {"mensagem": "API no ar!", "sprint": 1}

@app.post(
    "/dados",
    status_code=201,
    tags=["dados"],
    summary="Ingerir novo dado",
    description="Recebe um dado via JSON, valida os campos e persiste no DynamoDB.",
    response_model=dict,
    responses={
        201: {"description": "Dado criado com sucesso"},
        422: {"description": "Dados inválidos — verifique os campos obrigatórios"}
    }
)
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

@app.get(
    "/dados/{item_id}",
    tags=["dados"],
    summary="Buscar dado por ID",
    description="Busca um dado específico no DynamoDB usando o ID gerado no POST.",
    response_model=DadoResposta,
    responses={
        200: {"description": "Dado encontrado"},
        404: {"description": "Dado não encontrado para o ID informado"}
    }
)
def buscar_dado(item_id: str):
    tabela = get_table()

    resposta = tabela.get_item(Key={"id": item_id})
    item = resposta.get("Item")

    if not item:
        raise HTTPException(status_code=404, detail="Dado não encontrado")

    return item