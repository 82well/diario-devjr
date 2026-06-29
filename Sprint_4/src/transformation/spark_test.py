from pyspark.sql import SparkSession


def main():
    spark = (
        SparkSession.builder
        .appName("Sprint4-Test")
        .master("local[*]")
        .getOrCreate()
    )

    data = [
        ("João", "DF", 1200),
        ("Maria", "SP", 2500),
        ("Carlos", "RJ", 1800)
    ]

    columns = [
        "cliente",
        "estado",
        "valor"
    ]

    df = spark.createDataFrame(data, columns)

    print("Quantidade de registros:")
    print(df.count())

    print("Dados:")
    df.show()

    print("Maior venda:")
    df.orderBy(
        df.valor.desc()
    ).show()

    spark.stop()


if __name__ == "__main__":
    main()
