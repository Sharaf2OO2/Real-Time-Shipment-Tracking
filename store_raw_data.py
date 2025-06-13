from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, to_json, struct
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, BooleanType, TimestampType
from kafka import KafkaProducer
import json, time
from datetime import date

KAFKA_BROKER = "172.29.198.1:9092"

producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)

spark = SparkSession.builder \
    .appName("RawDataToHDFS") \
    .getOrCreate()

raw_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", "shipments_raw") \
    .option("failOnDataLoss", "false") \
    .load()

shipment_schema = StructType([
    StructField("shipment_id", StringType(), True),
    StructField("order_id", StringType(), True),
    StructField("shipment_type", StringType(), True),
    StructField("shipment_weight", DoubleType(), True),
    StructField("shipment_dimensions", StructType([
        StructField("length", DoubleType(), True),
        StructField("width", DoubleType(), True),
        StructField("height", DoubleType(), True),
    ])),
    StructField("priority_level", StringType(), True),
    StructField("insurance_coverage", DoubleType(), True),
    StructField("customer_id", StringType(), True),
    StructField("customer_first_name", StringType(), True),
    StructField("customer_last_name", StringType(), True),
    StructField("customer_email", StringType(), True),
    StructField("customer_phone", StringType(), True),
    StructField("customer_type", StringType(), True),
    StructField("customer_region", StringType(), True),
    StructField("current_status", StringType(), True),
    StructField("last_updated", TimestampType(), True),
    StructField("estimated_delivery_date", TimestampType(), True),
    StructField("actual_delivery_date", TimestampType(), True),
    StructField("current_location", StructType([
        StructField("address", StringType(), True),
        StructField("postal_code", StringType(), True),
        StructField("country", StringType(), True),
    ])),
    StructField("delivery_attempts", DoubleType(), True),
    StructField("origin_address", StructType([
        StructField("address", StringType(), True),
        StructField("postal_code", StringType(), True),
        StructField("country", StringType(), True),
    ])),
    StructField("destination_address", StructType([
        StructField("address", StringType(), True),
        StructField("postal_code", StringType(), True),
        StructField("country", StringType(), True),
    ])),
    StructField("distance_traveled", DoubleType(), True),
    StructField("transport_mode", StringType(), True),
    StructField("shipment_cost", DoubleType(), True),
    StructField("revenue_generated", DoubleType(), True),
    StructField("delivery_penalty", DoubleType(), True),
    StructField("order_date", StringType(), True),
    StructField("shipment_created_date", StringType(), True),
    StructField("transit_time", DoubleType(), True),
    StructField("delay_reason", StringType(), True),
    StructField("warehouse_id", StringType(), True),
    StructField("delivery_agent_id", StringType(), True),
    StructField("vehicle_id", StringType(), True),
    StructField("temperature_sensitivity", BooleanType(), True),
])

parsed_stream = raw_stream.selectExpr("CAST(value AS STRING)") \
    .withColumn("parsed_value", from_json(col("value"), shipment_schema)) \
    .select("parsed_value.*")

shipments = parsed_stream.withColumn("key", col("shipment_id")) \
    .withColumn("value", to_json(struct(
        "shipment_id",
        "order_id",
        "customer_id",
        "shipment_type",
        "shipment_weight",
        "shipment_dimensions",
        "origin_address",
        "destination_address",
        "priority_level",
        "temperature_sensitivity",
        "transport_mode",
        "shipment_cost",
        "revenue_generated",
        "insurance_coverage"
    )))

customers = parsed_stream.withColumn("key", col("customer_id")) \
    .withColumn("value", to_json(struct(
        "customer_id",
        "customer_first_name",
        "customer_last_name",
        "customer_email",
        "customer_phone",
        "customer_type",
        "customer_region"
    )))

delivery_status = parsed_stream.withColumn("key", col("shipment_id")) \
    .withColumn("value", to_json(struct(
        "shipment_id",
        "current_status",
        "last_updated",
        "estimated_delivery_date",
        "actual_delivery_date",
        "current_location",
        "delivery_attempts",
        "distance_traveled",
        "delivery_penalty",
        "delay_reason"
    )))

metadata = parsed_stream.withColumn("key", col("shipment_id")) \
    .withColumn("value", to_json(struct(
        "shipment_id",
        "shipment_created_date",
        "order_date",
        "warehouse_id",
        "delivery_agent_id",
        "vehicle_id"
    )))

# shipments_query = shipments.select("key", "value") \
#     .writeStream \
#     .format("kafka") \
#     .option("kafka.bootstrap.servers", KAFKA_BROKER) \
#     .option("topic", "shipments") \
#     .option("checkpointLocation", "/tmp/checkpoint/shipments") \
#     .start()

customers_query = customers.select("key", "value") \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("topic", "customers") \
    .option("checkpointLocation", "/tmp/checkpoint/customers") \
    .start()

# # delivery_status_query = delivery_status.select("key", "value") \
# #     .writeStream \
# #     .format("kafka") \
# #     .option("kafka.bootstrap.servers", KAFKA_BROKER) \
# #     .option("topic", "delivery_status") \
# #     .option("checkpointLocation", "/tmp/checkpoint/delivery_status") \
# #     .start()

# # metadata_query = metadata.select("key", "value") \
# #     .writeStream \
# #     .format("kafka") \
# #     .option("kafka.bootstrap.servers", KAFKA_BROKER) \
# #     .option("topic", "metadata") \
# #     .option("checkpointLocation", "/tmp/checkpoint/metadata") \
# #     .start()

# # shipments_query.awaitTermination()
customers_query.awaitTermination()
# # delivery_status_query.awaitTermination()
# # metadata_query.awaitTermination()