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

    input_file = "data/raw/olist_orders_dataset.csv"
    output_path = "data/processed/orders"

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(input_file)
    )

    print("Quantidade de registros:")
    print(df.count())

    df.printSchema()

    processed_df = (
        df
        .select(
            "order_id",
            "customer_id",
            "order_status",
            "order_purchase_timestamp"
        )
        .filter(col("order_status") == "delivered")
    )

    processed_df.write.mode("overwrite").parquet(output_path)

    spark.stop()


if __name__ == "__main__":
    main()
