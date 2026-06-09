import boto3
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BUCKET = "sprint02-datalake-wellington"

s3 = boto3.client(
    "s3",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

def upload_particionado(caminho_local: str, nome_arquivo: str, data: datetime = None):
    """
    Faz upload para a zona raw usando particionamento Hive por data.
    Se data não for informada, usa a data atual.
    """
    if data is None:
        data = datetime.now()

    # Monta o prefixo no padrão Hive
    prefixo = (
        f"raw/"
        f"year={data.strftime('%Y')}/"
        f"month={data.strftime('%m')}/"
        f"day={data.strftime('%d')}/"
    )

    chave_s3 = f"{prefixo}{nome_arquivo}"

    s3.upload_file(caminho_local, BUCKET, chave_s3)
    print(f"✓ Upload realizado:")
    print(f"  s3://{BUCKET}/{chave_s3}")
    return chave_s3

def simular_dados_historicos():
    from datetime import timedelta

    datas = [
        datetime(2026, 6, 7),
        datetime(2026, 6, 8),
        datetime(2026, 6, 9),
    ]

    for data in datas:
        conteudo = gerar_csv_data(data)
        caminho_temp = f"dados/temperatura_{data.strftime('%Y%m%d')}.csv"

        with open(caminho_temp, "w") as f:
            f.write(conteudo)

        upload_particionado(caminho_temp, "temperatura.csv", data)

def gerar_csv_data(data: datetime) -> str:
    """Gera dados simulados para uma data específica."""
    import random

    linhas = ["id,sensor,valor,unidade,timestamp"]
    for i in range(1, 6):
        valor = round(20 + random.uniform(0, 5), 1)
        ts = data.strftime(f"%Y-%m-%dT{8 + i}:00:00")
        linhas.append(f"{i},sensor_0{(i % 3) + 1},{valor},celsius,{ts}")

    return "\n".join(linhas)


if __name__ == "__main__":
    print("Simulando dados históricos particionados...\n")
    simular_dados_historicos()
    print("\nEstrutura criada no S3:")
    print("raw/")
    print("├── year=2025/month=06/day=07/temperatura.csv")
    print("├── year=2025/month=06/day=08/temperatura.csv")
    print("└── year=2025/month=06/day=09/temperatura.csv")