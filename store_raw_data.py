from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("RawDataToHDFS") \
    .getOrCreate()

raw_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "172.29.198.1:9092") \
    .option("subscribe", "shipments_raw") \
    .load()

query = raw_stream.writeStream \
    .format("json") \
    .option("path", "hdfs://localhost:9000/raw_shipments") \
    .option("checkpointLocation", "hdfs://localhost:9000//checkpoints/raw_shipments/") \
    .start()

query.awaitTermination()
