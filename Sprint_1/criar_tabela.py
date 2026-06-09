import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def criar_tabela():
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )

    tabela = dynamodb.create_table(
        TableName=os.getenv("DYNAMODB_TABLE"),
        KeySchema=[
            {"AttributeName": "id", "KeyType": "HASH"}
        ],
        AttributeDefinitions=[
            {"AttributeName": "id", "AttributeType": "S"}
        ],
        BillingMode="PAY_PER_REQUEST"
    )

    tabela.wait_until_exists()
    print(f"Tabela '{tabela.table_name}' criada com sucesso!")

if __name__ == "__main__":
    criar_tabela()