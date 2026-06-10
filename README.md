# Diário de um Dev Jr

![AWS](https://img.shields.io/badge/AWS-Cloud-FF9900?style=flat-square&logo=amazonaws&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Apache Spark](https://img.shields.io/badge/Apache_Spark-E25A1C?style=flat-square&logo=apachespark&logoColor=white)
![Status](https://img.shields.io/badge/Em_andamento-Sprint_03-blue?style=flat-square)

> Aprendizado estruturado em sprints — do jeito que times reais de tecnologia trabalham.
> Cada quinzena tem backlog definido, critérios de aceite, entrega e retrospectiva.

---

## Sobre o projeto

Este repositório documenta minha jornada de recolocação como Desenvolvedor Back-end Jr
em transição para Engenharia de Dados. Em vez de estudar de forma isolada, organizei
o aprendizado como acontece em equipes ágeis reais: com objetivos claros, entregas
concretas e evolução sprint a sprint.

Cada sprint gera um projeto funcional, um README técnico e uma retrospectiva pública
no LinkedIn — transformando estudo em portfólio real.

---

## Sprints

| Sprint | Tema | Tecnologias | Status |
|---|---|---|---|
| Sprint 01 | API REST de ingestão de dados | FastAPI · DynamoDB · pytest | ✅ Concluída |
| Sprint 02 | Pipeline de dados serverless | S3 · Glue · Athena · PySpark | ✅ Concluída |
| Sprint 03 | Deploy + Auth + CI/CD | EC2/Lambda · JWT · GitHub Actions | 🔜 Em breve |

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

### Decisões técnicas

**Hive Partitioning** — prefixos `year=/month=/day=` permitem ao Athena
pular partições inteiras na execução das queries, reduzindo dados escaneados
e custo por consulta.

**CSV → Parquet** — formato colunar reduz o volume de dados escaneados em
até 95% em queries que selecionam poucas colunas. Impacto direto em custo
e velocidade de análise.

**Data Catalog como contrato** — o Glue Job lê do catálogo em vez do S3
diretamente. Trocar o storage no futuro não exige mudança no script.

### Como rodar

```bash
cd Sprint_2
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Configure o .env com suas credenciais AWS

# Cria a estrutura no S3
python setup_s3.py

# Faz upload dos dados particionados
python upload_raw.py
```

Depois no Console AWS:
1. Rodar o Glue Crawler `crawler-temperatura`
2. Rodar o Glue Job `job-csv-para-parquet`
3. Consultar via Athena no banco `sprint02_db`

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

## Segurança

- Credenciais AWS armazenadas em `.env` — nunca versionado
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

## Autor

**Wellington** — Dev Jr em transição para Engenharia de Dados

[![LinkedIn](https://img.shields.io/badge/LinkedIn-conectar-0A66C2?style=flat-square&logo=linkedin)]([https://linkedin.com/in/SEU_PERFIL](https://www.linkedin.com/in/wellington-rodrigues-de-oliveira-35023181/))
[![GitHub](https://img.shields.io/badge/GitHub-82well-181717?style=flat-square&logo=github)](https://github.com/82well)
