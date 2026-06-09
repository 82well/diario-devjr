# API de Ingestão de Dados

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat-square&logo=fastapi&logoColor=white)
![AWS DynamoDB](https://img.shields.io/badge/AWS-DynamoDB-FF9900?style=flat-square&logo=amazondynamodb&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-8 testes-brightgreen?style=flat-square&logo=pytest&logoColor=white)
![Status](https://img.shields.io/badge/Sprint_01-concluída-teal?style=flat-square)

> Projeto desenvolvido como parte do **Diário de um Dev Jr** — aprendizado estruturado em sprints, do jeito que times reais de tecnologia trabalham.

---

## Sobre o projeto

API REST de ingestão de dados construída do zero em duas semanas, cobrindo o ciclo completo de desenvolvimento: modelagem, implementação, integração com nuvem, documentação e testes automatizados.

O objetivo foi além de "fazer funcionar" — cada decisão técnica foi tomada com boas práticas em mente: separação de responsabilidades, segurança por padrão e cobertura de testes antes do deploy.

---

## Funcionalidades

- Ingestão de dados via `POST /dados` com validação automática de tipos e regras de negócio
- Consulta de dados individuais via `GET /dados/{id}` com tratamento de erro 404
- Persistência no AWS DynamoDB com geração automática de UUID
- Documentação interativa via Swagger UI em `/docs`
- Testes unitários com mock completo da AWS (sem chamadas reais nos testes)

---

## Stack

| Camada | Tecnologia |
|---|---|
| Framework | FastAPI |
| Validação | Pydantic v2 |
| Banco de dados | AWS DynamoDB |
| SDK AWS | boto3 |
| Servidor | Uvicorn |
| Testes | pytest + moto |
| Segurança | IAM com least privilege |

---

## Arquitetura

```
sprint01-api/
├── main.py          # Endpoints e modelos Pydantic
├── database.py      # Conexão com DynamoDB (responsabilidade isolada)
├── criar_tabela.py  # Script de setup — roda uma única vez
├── .env             # Credenciais AWS (não versionado)
├── requirements.txt
└── tests/
    ├── __init__.py
    └── test_main.py # 8 testes cobrindo fluxos de sucesso e erro
```

A conexão com o DynamoDB foi isolada em `database.py` deliberadamente — trocar o banco de dados no futuro exige mudança em um único arquivo, sem refatoração nos endpoints.

---

## Como rodar localmente

**Pré-requisitos:** Python 3.11+, conta AWS com usuário IAM configurado.

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/sprint01-api-ingestao.git
cd sprint01-api-ingestao

# 2. Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as credenciais AWS
cp .env.example .env
# Preencha com suas credenciais no arquivo .env

# 5. Crie a tabela no DynamoDB (apenas na primeira vez)
python criar_tabela.py

# 6. Suba o servidor
uvicorn main:app --reload
```

Acesse `http://127.0.0.1:8000/docs` para explorar a API via Swagger UI.

---

## Endpoints

| Método | Rota | Descrição | Status |
|---|---|---|---|
| `GET` | `/` | Health check | 200 |
| `POST` | `/dados` | Ingerir novo dado | 201 / 422 |
| `GET` | `/dados/{id}` | Buscar dado por ID | 200 / 404 |

### Exemplo de requisição

```bash
curl -X POST http://127.0.0.1:8000/dados \
  -H "Content-Type: application/json" \
  -d '{"nome": "temperatura_sensor_01", "valor": 23.5, "categoria": "ambiental"}'
```

```json
{
  "mensagem": "Dado salvo com sucesso",
  "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
}
```

---

## Testes

```bash
pytest tests/ -v
```

```
tests/test_main.py::test_health_check                   PASSED
tests/test_main.py::test_criar_dado_sucesso             PASSED
tests/test_main.py::test_criar_dado_sem_nome            PASSED
tests/test_main.py::test_criar_dado_valor_invalido      PASSED
tests/test_main.py::test_criar_dado_nome_muito_curto    PASSED
tests/test_main.py::test_criar_dado_categoria_default   PASSED
tests/test_main.py::test_buscar_dado_existente          PASSED
tests/test_main.py::test_buscar_dado_inexistente        PASSED

8 passed in ~1.2s
```

Os testes usam `moto` para simular o DynamoDB localmente — nenhuma chamada real à AWS é feita durante a execução da suíte.

---

## Segurança

- Credenciais AWS armazenadas em `.env` (nunca versionado)
- Usuário IAM dedicado com política de **least privilege** — acesso restrito à tabela `dados-sprint01`
- Nenhuma credencial hardcoded no código-fonte

---

## Variáveis de ambiente

Crie um arquivo `.env` na raiz com base no exemplo abaixo:

```env
AWS_ACCESS_KEY_ID=sua_chave_aqui
AWS_SECRET_ACCESS_KEY=sua_chave_secreta_aqui
AWS_REGION=us-east-1
DYNAMODB_TABLE=dados-sprint01
```

---

## Contexto do projeto

Este projeto faz parte do **Diário de um Dev Jr** — uma metodologia pessoal de aprendizado onde cada quinzena é tratada como uma sprint real: backlog definido, critérios de aceite, entrega e retrospectiva.

| Sprint | Tema | Status |
|---|---|---|
| Sprint 01 | API REST + DynamoDB + Testes | ✅ Concluída |
| Sprint 02 | Deploy AWS (S3, GLUE, ATHENA) + CI/CD | 🔜 Em breve |

---

## Autor

**Wellington** — Dev Jr Engenharia de Dados

[![LinkedIn](https://img.shields.io/badge/LinkedIn-conectar-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/wellington-rodrigues-de-oliveira-35023181)
[![GitHub](https://img.shields.io/badge/GitHub-perfil-181717?style=flat-square&logo=github)](https://github.com/82well)