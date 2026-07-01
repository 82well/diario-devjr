from pyspark.sql import SparkSession
from pyspark.sql.functions import col


def create_spark_session():
    return (
        SparkSession.builder
        .appName("OlistOrdersPipeline")
        .getOrCreate()
    )


def main():

    spark = create_spark_session()

    input_path = "data/raw/olist_orders_dataset.csv"
    output_path = "data/processed/orders"

    print("Lendo arquivo CSV...")

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(input_path)
    )

    print(f"Total de registros: {df.count()}")

    print("Schema:")
    df.printSchema()

    delivered_orders = (
        df
        .filter(col("order_status") == "delivered")
        .select(
            "order_id",
            "customer_id",
            "order_status",
            "order_purchase_timestamp"
        )
    )

    print(
    f"Quantidade final no parquet: {delivered_orders.count()}"
    )

    delivered_orders.write \
        .mode("overwrite") \
        .parquet(output_path)

    print("Parquet criado com sucesso!")

    spark.stop()


if __name__ == "__main__":
    main()