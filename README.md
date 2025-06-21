# Real-Time Shipment Tracking

## Project Overview
This project provides a real-time shipment tracking and analytics platform for logistics businesses. It simulates shipment data, streams it via Kafka, processes and stores it using Apache Spark, and provides business insights using dbt and Snowflake. The system enables:
- Real-time tracking of shipments
- Customer and shipment analytics
- Revenue and cost analysis
- Business intelligence dashboards

## Business Purpose
The platform is designed for logistics companies to:
- Monitor shipments in real time
- Analyze customer activity and shipment trends
- Optimize operations and improve customer satisfaction
- Generate actionable insights for business growth

## Architecture & Tools Used
- **Python**: Core language for data generation, streaming, and processing
- **Kafka**: Real-time data streaming platform
- **Apache Spark**: Stream processing and ETL
- **Snowflake**: Cloud data warehouse for analytics
- **dbt (Data Build Tool)**: Data modeling and transformation
- **Faker**: Synthetic data generation
- **Apache Airflow**: Workflow orchestration and scheduling for dbt operations and batch time analysis
- **Power BI**: Business intelligence dashboards and data visualization
- **HDFS (Hadoop Distributed File System)**: Storage layer for raw shipment data before processing

## Directory Structure
```
├── kafka_producer.py                # Streams synthetic shipment data to Kafka
├── process_and_store_raw_data.py    # Consumes Kafka data, processes with Spark, writes to Snowflake
├── shipment_api.py                  # Generates fake shipment data
├── snowflake_config.json            # Snowflake connection config (excluded from git)
├── dbt_/
│   ├── dbt_project.yml              # dbt project config
│   ├── models/                      # dbt models (SQL transformations)
│   └── ...
├── logs/                            # Log files
└── ...
```

## Prerequisites
- Python 3.8+
- Java 8+ (for Spark)
- Apache Kafka (running broker)
- Apache Spark (with PySpark)
- Snowflake account
- dbt (installed via pip)

### Python Dependencies
Install with:
```bash
pip install pyspark kafka-python faker dbt-snowflake
```

## Configuration
1. **Snowflake**: Create a `snowflake_config.json` in the project root with your credentials:
```json
{
    "sfURL": "<your_snowflake_url>",
    "sfDatabase": "<your_db>",
    "sfSchema": "<your_schema>",
    "sfWarehouse": "<your_warehouse>",
    "sfRole": "<your_role>",
    "sfUser": "<your_user>",
    "sfPassword": "<your_password>"
}
```
2. **Kafka**: Update the broker address in `kafka_producer.py` and `process_and_store_raw_data.py` if needed (default: `172.29.198.1:9092`).

## What Needs to Be Running in the Background
- **Kafka Broker**: Start your Kafka server and create the topic `shipments_raw`.
- **Snowflake Warehouse**: Ensure your Snowflake warehouse is running and accessible.

## How to Run the Project
The workflow is orchestrated using Apache Airflow, which schedules and manages the following tasks:
- Streaming and storing raw shipment data in HDFS
- Processing data from HDFS using Spark and writing results to Snowflake
- Running dbt models for data transformation and analytics
- Batch time analysis and reporting

Raw shipment data is first ingested and stored in HDFS, providing scalable and fault-tolerant storage. Spark jobs then process this data, and the results are loaded into Snowflake for analytics and reporting.

Business intelligence dashboards and analytics are built and visualized in Power BI, connecting directly to the Snowflake data warehouse.

## DBT Models & Business Logic
- **customer_insights/**
  - `customer_type_distribution.sql`: Calculates the percentage of individual vs. business customers.
  - `top_revenue_generating_customers.sql`: Lists top 10 customers by total revenue.
  - `active_customers_by_region.sql`: Counts active customers per region.
- **shipments_overview/**
  - `shipments_by_priority_level.sql`: Number of shipments by priority.
  - `revenue_vs_cost_by_transport_mode.sql`: Revenue and cost by transport mode.
  - `total_shipments_by_shipment_type.sql`: Shipments count by type.

## Troubleshooting
- Ensure all services (Kafka, Snowflake) are running and accessible.
- Check log files in the `logs/` directory for errors.
- Verify Python dependencies are installed.
- For dbt issues, consult the [dbt documentation](https://docs.getdbt.com/docs/introduction).

## Resources
- [dbt Documentation](https://docs.getdbt.com/docs/introduction)
- [Apache Kafka Quickstart](https://kafka.apache.org/quickstart)
- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [Snowflake Documentation](https://docs.snowflake.com/en/)
- [Faker Documentation](https://faker.readthedocs.io/en/master/)
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Power BI Documentation](https://learn.microsoft.com/en-us/power-bi/)
- [HDFS Documentation](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsUserGuide.html)

---

**Note:** Do not commit your `snowflake_config.json` with credentials to version control. 