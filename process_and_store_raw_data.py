from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, BooleanType, TimestampType
import json, time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

spark = SparkSession.builder \
    .appName("ProcessAndStoreData") \
    .config("spark.jars.packages", "net.snowflake:snowflake-jdbc:3.17.0,net.snowflake:spark-snowflake_2.12:3.0.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .config("spark.sql.catalogImplementation", "in-memory") \
    .config("spark.sql.streaming.checkpointLocation.deleteSourceCheckpointMetadata", "true") \
    .getOrCreate()

raw_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "172.29.198.1:9092") \
    .option("subscribe", "shipments_raw") \
    .option("failOnDataLoss", "false") \
    .option("startingOffsets", "latest") \
    .option("maxOffsetsPerTrigger", "1000") \
    .option("kafka.session.timeout.ms", "30000") \
    .option("kafka.request.timeout.ms", "40000") \
    .load()

raw_stream = raw_stream.selectExpr("CAST(value AS STRING)")

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

flattened_df = raw_stream.withColumn("value", col("value").cast(StringType())) \
    .withColumn("data", from_json(col("value"), shipment_schema)) \
    .select("data.*")

shipments = flattened_df.select(
    col("shipment_id"),
    col("order_id"),
    col("customer_id"),
    col("shipment_type"),
    col("shipment_weight"),
    col("shipment_dimensions.length").alias("shipment_length"),
    col("shipment_dimensions.width").alias("shipment_width"),
    col("shipment_dimensions.height").alias("shipment_height"),
    col("origin_address.address").alias("origin_address"),
    col("origin_address.postal_code").alias("origin_postal_code"),
    col("origin_address.country").alias("origin_country"),
    col("destination_address.address").alias("destination_address"),
    col("destination_address.postal_code").alias("destination_postal_code"),
    col("destination_address.country").alias("destination_country"),
    col("priority_level"),
    col("temperature_sensitivity"),
    col("transport_mode"),
    col("shipment_cost"),
    col("revenue_generated"),
    col("insurance_coverage"),
)

customers = flattened_df.select(
    col("customer_id"),
    col("customer_first_name"),
    col("customer_last_name"),
    col("customer_email"),
    col("customer_phone"),
    col("customer_type"),
    col("customer_region"),
)

delivery_status = flattened_df.select(
    col("shipment_id"),
    col("current_status"),
    col("last_updated"),
    col("estimated_delivery_date"),
    col("actual_delivery_date"),
    col("current_location.address").alias("current_address"),
    col("current_location.postal_code").alias("current_postal_code"),
    col("current_location.country").alias("current_country"),
    col("delivery_attempts"),
    col("delay_reason"),
    col("delivery_penalty"),
    col("distance_traveled")
)

metadata = flattened_df.select(
    col("shipment_id"),
    col("order_date"),
    col("shipment_created_date"),
    col("warehouse_id"),
    col("delivery_agent_id"),
    col("vehicle_id")
)

shipments.createOrReplaceTempView("shipments")
customers.createOrReplaceTempView("customers")
delivery_status.createOrReplaceTempView("delivery_status")
metadata.createOrReplaceTempView("metadata")

query = '''SELECT 
            CASE
                WHEN LENGTH(customer_id) < 10 THEN RPAD(customer_id, 10, 'x')
                ELSE customer_id
            END customer_id,
            customer_first_name first_name,
            customer_last_name last_name,
            customer_email email,
            customer_phone phone,
            LOWER(customer_type) customer_type,
            customer_region
            FROM customers
            '''
customers = spark.sql(query)

query = '''SELECT 
            CASE
                WHEN LENGTH(shipment_id) < 18 THEN RPAD(shipment_id, 18, 'x')
                ELSE shipment_id
            END shipment_id,
            CASE
                WHEN LENGTH(order_id) < 17 THEN RPAD(order_id, 17, 'x')
                ELSE order_id
            END order_id,
            CASE
                WHEN LENGTH(customer_id) < 10 THEN RPAD(customer_id, 10, 'x')
                ELSE customer_id
            END customer_id,
            LOWER(shipment_type) shipment_type,
            shipment_weight,
            shipment_length,
            shipment_width,
            shipment_height,
            origin_address,
            origin_postal_code,
            origin_country,
            destination_address,
            destination_postal_code,
            destination_country,
            LOWER(priority_level) priority_level,
            CASE temperature_sensitivity
                WHEN 'true' THEN 'sensitive'
                ELSE 'insensitive'
            END temperature_sensitivity,
            LOWER(transport_mode) transport_mode,
            shipment_cost,
            revenue_generated,
            insurance_coverage
            FROM shipments
            '''
shipments = spark.sql(query)

query = '''SELECT 
            CASE
                WHEN LENGTH(shipment_id) < 18 THEN RPAD(shipment_id, 18, 'x')
                ELSE shipment_id
            END shipment_id,
            LOWER(current_status) current_status,
            CAST(last_updated AS TIMESTAMP),
            CAST(estimated_delivery_date AS TIMESTAMP),
            CAST(actual_delivery_date AS TIMESTAMP),
            current_address,
            current_postal_code,
            current_country,
            delivery_attempts,
            CASE
                WHEN delay_reason IS NULL THEN 'n/a'
                ELSE LOWER(delay_reason)
            END delay_reason,
            delivery_penalty,
            distance_traveled
            FROM delivery_status
            '''
delivery_status = spark.sql(query)

query = '''SELECT 
            CASE
                WHEN LENGTH(shipment_id) < 18 THEN RPAD(shipment_id, 18, 'x')
                ELSE shipment_id
            END shipment_id,
            CAST(order_date AS TIMESTAMP),
            CAST(shipment_created_date AS TIMESTAMP),
            CASE
                WHEN LENGTH(warehouse_id) < 5 THEN RPAD(warehouse_id, 5, 'x')
                ELSE warehouse_id
            END warehouse_id,
            CASE
                WHEN LENGTH(delivery_agent_id) < 9 THEN RPAD(delivery_agent_id, 9, 'x')
                ELSE delivery_agent_id
            END delivery_agent_id,
            CASE
                WHEN LENGTH(vehicle_id) < 7 THEN RPAD(vehicle_id, 7, 'x')
                ELSE vehicle_id
            END vehicle_id
            FROM metadata
            '''
metadata = spark.sql(query)

with open("snowflake_config.json") as f:
    options = json.load(f)

def write_to_snowflake(batch_df, batch_id, table_name):
    """Write each batch to Snowflake with duplicate checking"""
    try:
        if batch_df.count() > 0:  # Only write if there's data
            logger.info(f"Processing batch {batch_id} with {batch_df.count()} records for Snowflake table {table_name}")
            
            # Check if the Snowflake table exists first
            try:
                # Try to read from the table to see if it exists
                existing_df = spark.read \
                    .format("snowflake") \
                    .options(**options) \
                    .option("dbtable", table_name) \
                    .load() \
                    .limit(1)
                
                table_exists = True
                logger.info(f"Table {table_name} exists in Snowflake")
                
            except Exception as table_check_error:
                # Table doesn't exist, so we'll write all records
                table_exists = False
                logger.info(f"Table {table_name} doesn't exist in Snowflake, will create and write all records")
            
            if table_exists:
                # Check for duplicates based on table type
                if table_name == "customers":
                    # Get list of customer_ids from the batch
                    batch_ids = [row.customer_id for row in batch_df.select("customer_id").collect()]
                    
                    if batch_ids:
                        # Check which customer_ids already exist
                        ids_str = "', '".join(batch_ids)
                        try:
                            existing_records = spark.read \
                                .format("snowflake") \
                                .options(**options) \
                                .option("query", f"SELECT customer_id FROM {table_name} WHERE customer_id IN ('{ids_str}')") \
                                .load()
                            
                            # Filter out records that already exist
                            new_records = batch_df.join(existing_records, "customer_id", "left_anti")
                            
                        except Exception as e:
                            logger.warning(f"Error checking for existing customers, writing all records: {str(e)}")
                            new_records = batch_df
                    else:
                        new_records = batch_df
                        
                elif table_name == "shipments":
                    # Get list of shipment_ids from the batch
                    batch_ids = [row.shipment_id for row in batch_df.select("shipment_id").collect()]
                    
                    if batch_ids:
                        # Check which shipment_ids already exist
                        ids_str = "', '".join(batch_ids)
                        try:
                            existing_records = spark.read \
                                .format("snowflake") \
                                .options(**options) \
                                .option("query", f"SELECT shipment_id FROM {table_name} WHERE shipment_id IN ('{ids_str}')") \
                                .load()
                            
                            # Filter out records that already exist
                            new_records = batch_df.join(existing_records, "shipment_id", "left_anti")
                            
                        except Exception as e:
                            logger.warning(f"Error checking for existing shipments, writing all records: {str(e)}")
                            new_records = batch_df
                    else:
                        new_records = batch_df
                        
                else:
                    # For other tables (delivery_status, metadata), append all records
                    new_records = batch_df
            else:
                # Table doesn't exist, write all records
                new_records = batch_df
            
            # Only write if there are new records
            if new_records.count() > 0:
                logger.info(f"Writing {new_records.count()} new records to Snowflake table {table_name}")
                new_records.write \
                    .format("snowflake") \
                    .options(**options) \
                    .option("dbtable", table_name) \
                    .mode("append") \
                    .save()
                logger.info(f"Batch {batch_id} written successfully to {table_name}")
            else:
                logger.info(f"All records in batch {batch_id} already exist in {table_name}, skipping write")
                
        else:
            logger.info(f"Batch {batch_id} is empty for {table_name}, skipping write")
    except Exception as e:
        logger.error(f"Error writing batch {batch_id} to {table_name}: {str(e)}")
        raise  # Re-raise the exception to see the full stack trace
    
# Use unique checkpoint locations with timestamp
timestamp = int(time.time())
checkpoint_paths = {
    "customers": f"/tmp/checkpoint/customers/{timestamp}",
    "shipments": f"/tmp/checkpoint/shipments/{timestamp}",
    "delivery_status": f"/tmp/checkpoint/delivery_status/{timestamp}",
    "metadata": f"/tmp/checkpoint/metadata/{timestamp}"
}

try:
    # Start HDFS write stream for raw data
    hdfs_query = raw_stream.writeStream \
        .format("parquet") \
        .option("path", "/raw_shipments/") \
        .option("checkpointLocation", "/checkpoints/raw_shipments/") \
        .outputMode("append") \
        .trigger(processingTime="1 hour") \
        .start()

    queries = []
    
    # Customers stream
    customers_query = customers.writeStream \
        .foreachBatch(lambda df, batch_id: write_to_snowflake(df, batch_id, "customers")) \
        .outputMode("append") \
        .option("checkpointLocation", checkpoint_paths["customers"]) \
        .trigger(processingTime='30 seconds') \
        .start()
    queries.append(customers_query)
    
    # Shipments stream
    shipments_query = shipments.writeStream \
        .foreachBatch(lambda df, batch_id: write_to_snowflake(df, batch_id, "shipments")) \
        .outputMode("append") \
        .option("checkpointLocation", checkpoint_paths["shipments"]) \
        .trigger(processingTime='30 seconds') \
        .start()
    queries.append(shipments_query)
    
    # Delivery status stream
    delivery_status_query = delivery_status.writeStream \
        .foreachBatch(lambda df, batch_id: write_to_snowflake(df, batch_id, "delivery_status")) \
        .outputMode("append") \
        .option("checkpointLocation", checkpoint_paths["delivery_status"]) \
        .trigger(processingTime='30 seconds') \
        .start()
    queries.append(delivery_status_query)
    
    # Metadata stream
    metadata_query = metadata.writeStream \
        .foreachBatch(lambda df, batch_id: write_to_snowflake(df, batch_id, "metadata")) \
        .outputMode("append") \
        .option("checkpointLocation", checkpoint_paths["metadata"]) \
        .trigger(processingTime='30 seconds') \
        .start()
    queries.append(metadata_query)
    
    logger.info("All streaming queries started successfully")
    
    for query in queries:
        query.awaitTermination()
    
except Exception as e:
    logger.error(f"Streaming query failed: {str(e)}")
    for query in queries:
        query.stop()
    spark.stop()