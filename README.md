# Diário de um Dev Jr

![AWS](https://img.shields.io/badge/AWS-Cloud-FF9900?style=flat-square&logo=amazonaws&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Apache Spark](https://img.shields.io/badge/Apache_Spark-E25A1C?style=flat-square&logo=apachespark&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI/CD-GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)
![Status](https://img.shields.io/badge/Em_andamento-Sprint_04-blue?style=flat-square)

> Aprendizado estruturado em sprints — do jeito que times reais de tecnologia trabalham.
> Cada quinzena tem backlog definido, critérios de aceite, entrega e retrospectiva.

---

## Sobre o projeto

Em vez de estudar tecnologias de forma isolada, organizei o aprendizado em sprints, seguindo uma abordagem próxima de equipes reais:

objetivos definidos;
entregas técnicas;
documentação;
resolução de problemas;
retrospectivas de aprendizado.

Cada sprint representa uma evolução prática do projeto, transformando estudo em portfólio técnico.
---

## Sprints

| Sprint | Tema | Tecnologias | Status |
|---|---|---|---|
| Sprint 01 | API REST de ingestão de dados | FastAPI · DynamoDB · pytest | ✅ Concluída |
| Sprint 02 | Pipeline de dados serverless | S3 · Glue · Athena · PySpark | ✅ Concluída |
| Sprint 03 | Deploy Lambda + CI/CD | Lambda · API Gateway · GitHub Actions | ✅ Concluída |
| Sprint 04 | Processamento distribuído | Spark · PySpark · AWS S3 · Olist | 🚧 Em andamento |

---

## Sprint 01 — API de Ingestão de Dados

API REST construída com FastAPI e AWS DynamoDB cobrindo o ciclo completo:
modelagem, implementação, integração com nuvem, documentação e testes automatizados.

### Stack
Python · FastAPI · Pydantic · boto3 · AWS DynamoDB · pytest · moto · Uvicorn

### Funcionalidades
- Ingestão de dados via `POST /dados` com validação automática de tipos
- Consulta individual via `GET /dados/{id}` com tratamento de erro 404
- Persistência no DynamoDB com geração automática de UUID
- Documentação interativa Swagger UI em `/docs`
- 8 testes unitários com mock completo da AWS via moto

### Como rodar

```bash
cd Sprint_1
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Configure o .env com suas credenciais AWS
# Crie a tabela (apenas na primeira vez)
python criar_tabela.py

# Suba o servidor
uvicorn main:app --reload
```

### Endpoints

| Método | Rota | Descrição | Status |
|---|---|---|---|
| `GET` | `/` | Health check | 200 |
| `POST` | `/dados` | Ingerir novo dado | 201 / 422 |
| `GET` | `/dados/{id}` | Buscar dado por ID | 200 / 404 |

### Testes

```bash
pytest Sprint_1/tests/ -v
# 8 passed in ~1.2s
```

---

## Sprint 02 — Pipeline de Dados Serverless

Pipeline completa de dados construída com serviços gerenciados da AWS,
cobrindo ingestão, transformação e consulta analítica sem gerenciar servidores.

### Arquitetura

```
CSV/JSON
   ↓
S3 raw/          ← arquivos originais, nunca modificados
   ↓
AWS Glue Crawler  ← infere schema, cria tabela no Data Catalog
   ↓
AWS Glue Job      ← ETL em PySpark, converte CSV → Parquet
   ↓
S3 curated/       ← dados limpos em formato colunar
   ↓
Amazon Athena     ← queries SQL direto no S3
```

### Stack
Amazon S3 · AWS Glue · Apache Spark · PySpark · Amazon Athena
Hive Partitioning · Parquet · boto3 · IAM

### Estrutura do bucket S3

```
sprint02-datalake-wellington/
├── raw/                          ← zona de entrada
│   └── year=2026/month=06/day=09/
│       └── temperatura.csv
├── curated/                      ← zona transformada
│   └── year=2026/month=06/day=09/
│       └── temperatura.parquet
└── athena/                       ← resultados das queries
    └── queries/
```

### Exemplo de query

```sql
SELECT
    sensor,
    COUNT(*)              AS total_leituras,
    ROUND(AVG(valor), 2)  AS media_valor,
    MIN(valor)            AS minimo,
    MAX(valor)            AS maximo
FROM raw
WHERE year = '2026'
GROUP BY sensor
ORDER BY media_valor DESC;
```

### Números da entrega
- Query retornando agregações em **607ms**
- **0.77 KB** de dados escaneados por query
- Custo total da sprint: **~R$ 1,00**

---

### Conceitos aplicados
- Data Lake
- Separação entre dados brutos e tratados
- Formato Parquet
- Consultas SQL sobre dados no S3
- IAM e controle de acesso

---


## Sprint 03 — Deploy Lambda + CI/CD

API FastAPI em produção na AWS com pipeline de deploy automático.
Todo `git push` dispara os testes e, se passarem, faz o deploy no Lambda.

### Arquitetura CI/CD

```
git push
   ↓
GitHub Actions — 6 testes automatizados
   ↓ (se passarem)
Empacota API em zip (formato Linux)
   ↓
Upload para S3
   ↓
AWS Lambda atualizado automaticamente
   ↓
API em produção com novo código
```

### Stack
AWS Lambda · Mangum · API Gateway · GitHub Actions
GitHub Secrets · AWS CLI · pytest · Python 3.11

### URL em produção

```
https://m9mzjov5id.execute-api.us-east-1.amazonaws.com
```

### Como rodar localmente

```bash
cd Sprint_3
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Configure o .env com suas credenciais AWS
uvicorn main:app --reload
```

### Testes

```bash
pytest Sprint_3/tests/ -v
# 6 passed in ~1.2s
```

### Dificuldades reais enfrentadas

**Compatibilidade Windows x Linux**
O Lambda roda em Amazon Linux. As bibliotecas instaladas no Windows
não são compatíveis. Solução: baixar os wheels especificando a plataforma
`manylinux2014_x86_64` e extrair manualmente.

**Arquivo zip recriado várias vezes**
Cada tentativa resolvia um módulo e aparecia outro. Foram necessárias
múltiplas iterações até todos os módulos estarem no formato correto.

**BOM no arquivo YAML**
O Windows adiciona 3 bytes invisíveis (BOM: `EF BB BF`) nos arquivos
de texto que o GitHub rejeitava silenciosamente. Solução: remover com
Python e verificar com `Format-Hex` antes de commitar.

### Números da entrega
- Pipeline CI/CD: **40 segundos** do push ao deploy
- **6 testes** passando automaticamente
- Custo total: **R$ 0,00** (Free Tier)

---

## Segurança

- Credenciais AWS armazenadas em `.env` — nunca versionado
- Credenciais AWS no CI/CD via **GitHub Secrets** — criptografadas
- Usuário IAM dedicado com política de **least privilege** por sprint
- Nenhuma credencial hardcoded no código-fonte
- `.gitignore` configurado para bloquear `.env` em qualquer subpasta

---

## Variáveis de ambiente

Cada sprint tem seu próprio `.env`. Crie com base no exemplo:

```env
AWS_ACCESS_KEY_ID=sua_chave_aqui
AWS_SECRET_ACCESS_KEY=sua_chave_secreta_aqui
AWS_REGION=us-east-1
DYNAMODB_TABLE=dados-sprint01
```
---

## Competências Técnicas Demonstradas

Backend:
- APIs REST
- FastAPI
- Testes automatizados

Cloud:
- AWS Lambda
- S3
- IAM
- API Gateway

Data Engineering:
- Data Lake
- ETL
- Parquet
- Athena
- Glue

DevOps:
- GitHub Actions
- CI/CD
- Secrets Management


---


## Sprint 04 — Processamento Distribuído com Apache Spark

Objetivo

Evoluir o Data Lake criado anteriormente adicionando processamento distribuído utilizando Apache Spark e dados reais do dataset Olist.

## Arquitetura planejada
   Dataset Olist CSV
         ↓
   PySpark DataFrame
         ↓
   Transformações
         ↓
   Parquet
         ↓
   Amazon S3
         ↓
   Athena / QuickSight

## Ambiente configurado
- Windows 10 + WSL2
- Ubuntu 24.04 LTS
- Python 3.11
- Apache Spark
- PySpark
- AWS CLI
- IAM com política de menor privilégio
- Amazon S3
- Checkpoint inicial

✅ Spark executando localmente
✅ Criação e transformação de DataFrames
✅ Ambiente Python configurado
✅ AWS CLI autenticado
✅ Comunicação com bucket S3 validada

## Próximas entregas:

 - Processamento do dataset Olist
 - Transformações utilizando Spark
 - Geração de arquivos Parquet
 - Upload para S3
 - Integração com Athena

---

## Roadmap

```
✅ Módulo 01 — Ingestão e Data Lake
   Sprint 01 — API REST + DynamoDB + testes
   Sprint 02 — Pipeline S3 + Glue + Athena

✅ Módulo 02 — Infraestrutura e Automação
   Sprint 03 — Deploy Lambda + CI/CD GitHub Actions

🔜 Módulo 03 — Processamento Distribuído
   Sprint 04 — Spark com dataset real Olist

⏳ Módulo 04 — Streaming
   Sprint 05 — Pipeline em tempo real com Kafka

🏁 Projeto Final
   Plataforma completa de dados e-commerce na AWS
   Dataset: Olist (100k pedidos reais)
```

---

## Autor

**Wellington** — Dev Jr em evolução para Engenharia de Dados AWS.

Construindo conhecimento através de projetos práticos, documentando erros, soluções e aprendizados.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-conectar-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/SEU_PERFIL)
[![GitHub](https://img.shields.io/badge/GitHub-82well-181717?style=flat-square&logo=github)](https://github.com/82well)