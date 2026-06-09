import boto3
import os
from dotenv import load_dotenv

load_dotenv()

BUCKET = "sprint02-datalake-wellington"  # nomes de bucket  globais na AWS
REGION = os.getenv("AWS_REGION", "us-east-1")

s3 = boto3.client(
    "s3",
    region_name=REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

def criar_bucket():
    # us-east-1 não aceita o parâmetro LocationConstraint — é a única exceção
    if REGION == "us-east-1":
        s3.create_bucket(Bucket=BUCKET)
    else:
        s3.create_bucket(
            Bucket=BUCKET,
            CreateBucketConfiguration={"LocationConstraint": REGION}
        )
    print(f"Bucket '{BUCKET}' criado com sucesso!")

def criar_estrutura():
    # No S3 "pastas"  fazendo upload de um objeto vazio
    # com a chave terminando em "/"
    prefixos = ["raw/", "curated/", "athena/queries/"]
    for prefixo in prefixos:
        s3.put_object(Bucket=BUCKET, Key=prefixo)
        print(f"  Prefixo criado: {prefixo}")

if __name__ == "__main__":
    criar_bucket()
    criar_estrutura()