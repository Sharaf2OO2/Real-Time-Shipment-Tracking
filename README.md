# Real-Time Shipment Tracking System

## 🚀 Project Overview

This is a comprehensive real-time shipment tracking and analytics platform designed for logistics businesses. The system provides end-to-end data pipeline capabilities from real-time data generation to business intelligence dashboards. It enables logistics companies to monitor shipments in real-time, analyze customer activity and shipment trends, optimize operations, and generate actionable insights for business growth.

![image](https://github.com/user-attachments/assets/8a24ac07-88fc-4f6c-85f9-5db7f4125bde)


## 🏗️ System Architecture

The platform follows a modern data architecture with the following components:

### Core Components
- **Data Generation**: Python-based synthetic shipment data generation using Faker
- **Real-time Streaming**: Apache Kafka for real-time data streaming
- **Data Processing**: Apache Spark for stream processing and ETL operations
- **Data Warehouse**: Snowflake for analytics and reporting
- **Data Transformation**: dbt (Data Build Tool) for data modeling and transformations
- **Workflow Orchestration**: Apache Airflow for scheduling and managing data pipelines
- **Business Intelligence**: Power BI for dashboards and data visualization
- **Storage**: HDFS for raw data storage before processing

### Data Flow Architecture
```
Data Generation (shipment_api.py) 
    ↓
Kafka Producer (kafka_producer.py)
    ↓
Kafka Topic (shipments_raw)
    ↓
Spark Streaming (process_and_store_raw_data.py)
    ↓
HDFS Storage (/user/shipment_data/)
    ├── /raw/          # Raw shipment data
    ├── /processed/    # Processed data before Snowflake
    └── /analytics/    # Analytics results
    ↓
Snowflake Data Warehouse
    ├── Staging Tables (SILVER schema)
    │   ├── customers
    │   ├── shipments
    │   ├── delivery_status
    │   └── metadata
    └── Analytics Views (GOLD schema)
        ├── Real-time Analytics
        └─ Historical Analytics
    ↓
Power BI Dashboards
```

## 📁 Project Structure

```
Real-Time-Shipment-Tracking/
├── 📄 kafka_producer.py              # Streams synthetic shipment data to Kafka
├── 📄 process_and_store_raw_data.py  # Consumes Kafka data, processes with Spark, writes to Snowflake
├── 📄 shipment_api.py                # Generates fake shipment data using Faker
├── 📄 snowflake_config.json          # Snowflake connection configuration (excluded from git)
├── 📁 dags/                          # Apache Airflow DAG definitions
│   ├── 📄 stream_dag.py              # Real-time streaming DAG (runs every 2 minutes)
│   └── 📄 historical_dag.py          # Historical analysis DAG (runs quarterly)
├── 📁 dbt_/                          # dbt project for data transformations
│   ├── 📄 dbt_project.yml            # dbt project configuration
│   ├── 📄 models/                    # dbt models (SQL transformations)
│   │   ├── 📁 cost_analysis/         # Cost and revenue analysis models
│   │   ├── 📁 customer_insights/     # Customer analytics models
│   │   ├── 📁 delivery_performance/  # Delivery metrics models
│   │   ├── 📁 operational_insights/  # Operational analytics models
│   │   ├── 📁 shipment_tracking/     # Real-time tracking models
│   │   ├── 📁 shipments_overview/    # Shipment summary models
│   │   ├── 📁 hist_customer_insights/ # Historical customer analysis
│   │   ├── 📁 hist_revenue_trends/   # Historical revenue analysis
│   │   └── 📁 hist_shipment_volume/  # Historical volume analysis
│   ├── 📄 sources.yml                # Source table definitions and tests
│   └── 📁 logs/                      # dbt execution logs
├── 📁 logs/                          # Airflow and application logs
└── 📁 spark-warehouse/               # Spark warehouse directory
```

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.8+**: Primary programming language for data generation and processing
- **Apache Kafka 2.8+**: Real-time data streaming platform
- **Apache Spark 3.5+**: Distributed computing for stream processing and ETL
- **Snowflake**: Cloud data warehouse for analytics
- **dbt (Data Build Tool)**: Data transformation and modeling
- **Apache Airflow 2.7+**: Workflow orchestration and scheduling
- **Power BI**: Business intelligence and data visualization

### Python Dependencies
```bash
pip install pyspark
pip install kafka-python
pip install faker
pip install dbt-snowflake
pip install apache-airflow
pip install snowflake-connector-python
```

## ⚙️ Configuration

### 1. Snowflake Configuration
Create a `snowflake_config.json` file in the project root with your Snowflake credentials:

```json
{
    "sfURL": "<your_snowflake_account_url>",
    "sfDatabase": "<your_database_name>",
    "sfSchema": "<your_schema_name>",
    "sfWarehouse": "<your_warehouse_name>",
    "sfRole": "<your_role>",
    "sfUser": "<your_username>",
    "sfPassword": "<your_password>"
}
```

### 2. Kafka Configuration
Update the Kafka broker address in the following files if needed:
- `kafka_producer.py` (default: `172.29.198.1:9092`)
- `process_and_store_raw_data.py` (default: `172.29.198.1:9092`)

### 3. Airflow Configuration
For on-premise Airflow installation, ensure the following:
- Airflow home directory is properly configured
- DAGs folder is set to `/opt/airflow/dags`
- dbt project directory is accessible at `/opt/airflow/dbt_`

## 🚀 Background Components Setup

### 1. Apache Kafka Setup
```bash
# Start Zookeeper (if not already running)
bin/zookeeper-server-start.sh config/zookeeper.properties

# Start Kafka Broker
bin/kafka-server-start.sh config/server.properties

# Create the shipments topic
bin/kafka-topics.sh --create --topic shipments_raw --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### 2. Apache Spark Setup
```bash
# Set SPARK_HOME environment variable
export SPARK_HOME=/path/to/spark

# Add Spark to PATH
export PATH=$PATH:$SPARK_HOME/bin

# Verify Spark installation
spark-submit --version
```

### 3. HDFS (Hadoop Distributed File System) Setup
```bash
# Set HADOOP_HOME environment variable
export HADOOP_HOME=/path/to/hadoop

# Add Hadoop to PATH
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Format HDFS (only needed for first-time setup)
hdfs namenode -format

# Start HDFS services
# Terminal 1: Start NameNode
hadoop-daemon.sh start namenode

# Terminal 2: Start DataNode
hadoop-daemon.sh start datanode

# Verify HDFS is running
jps | grep -E "(NameNode|DataNode)"

# Create required directories in HDFS
hdfs dfs -mkdir -p /user/shipment_data/raw
hdfs dfs -mkdir -p /user/shipment_data/processed
hdfs dfs -mkdir -p /user/shipment_data/analytics

# Set permissions
hdfs dfs -chmod 755 /user/shipment_data
hdfs dfs -chmod 755 /user/shipment_data/raw
hdfs dfs -chmod 755 /user/shipment_data/processed
hdfs dfs -chmod 755 /user/shipment_data/analytics

# Verify HDFS directories
hdfs dfs -ls /user/shipment_data/
```

### 4. Snowflake Setup
- Ensure your Snowflake account is active
- Create the required database, schema, and warehouse
- Verify network connectivity and credentials

### 5. Apache Airflow Setup (On-Premise)
```bash
# Install Airflow
pip install apache-airflow

# Set Airflow home
export AIRFLOW_HOME=/opt/airflow

# Initialize Airflow database
airflow db init

# Create admin user
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin

# Start Airflow webserver
airflow webserver --port 8080

# Start Airflow scheduler (in separate terminal)
airflow scheduler
```

## 🏃‍♂️ How to Start the System

### Step 1: Start Background Services
1. **Start HDFS Services**:
   ```bash
   # Start NameNode
   hadoop-daemon.sh start namenode
   
   # Start DataNode
   hadoop-daemon.sh start datanode
   
   # Verify HDFS is running
   jps | grep -E "(NameNode|DataNode)"
   ```

2. **Start Kafka Services**:
   ```bash
   # Start Zookeeper first (required for Kafka)
   bin/zookeeper-server-start.sh config/zookeeper.properties
   
   # Start Kafka Broker (in a new terminal)
   bin/kafka-server-start.sh config/server.properties
   
   # Verify Kafka is running
   jps | grep -E "(Kafka|QuorumPeerMain)"
   ```

3. **Start Airflow Services**:
   ```bash
   # Terminal 1: Start Airflow webserver
   airflow webserver --port 8080
   
   # Terminal 2: Start Airflow scheduler
   airflow scheduler
   ```

4. **Verify Snowflake Connection**:
   - Test connection using the credentials in `snowflake_config.json`

### Step 2: Start Data Generation
```bash
# Start the Kafka producer to generate shipment data
python kafka_producer.py
```

### Step 3: Start Data Processing
```bash
# Start the Spark streaming job
python process_and_store_raw_data.py
```

### Step 4: Monitor Airflow DAGs
1. Open Airflow web UI at `http://localhost:8080`
2. Login with admin credentials
3. Enable the DAGs:
   - `stream_dag`: Runs every 2 minutes for real-time analytics
   - `historical_dag`: Runs quarterly for historical analysis

## 📊 DBT Models & Analytics

### Real-Time Analytics Models
- **customer_insights/**: Customer analytics and segmentation
- **shipments_overview/**: Shipment summary and metrics
- **delivery_performance/**: Delivery success rates and performance
- **operational_insights/**: Operational efficiency metrics
- **shipment_tracking/**: Real-time shipment status tracking
- **cost_analysis/**: Cost and revenue analysis

### Historical Analytics Models
- **hist_customer_insights/**: Historical customer behavior analysis
- **hist_revenue_trends/**: Revenue trends and patterns
- **hist_shipment_volume/**: Historical shipment volume analysis

### Key Business Metrics
- Customer acquisition and retention rates
- Delivery performance and on-time delivery rates
- Revenue vs. cost analysis by transport mode
- Shipment volume trends and seasonality
- Customer satisfaction metrics
- Operational efficiency indicators

## 🔄 Airflow DAGs

### Stream DAG (`stream_dag.py`)
- **Schedule**: Every 2 minutes (`*/2 * * * *`)
- **Purpose**: Real-time data processing and analytics
- **Tasks**:
  - `dbt_test`: Run data quality tests
  - `dbt_run`: Execute real-time analytics models

### Historical DAG (`historical_dag.py`)
- **Schedule**: Quarterly on 1st day (`0 0 1 */3 *`)
- **Purpose**: Historical data analysis and reporting
- **Tasks**:
  - `dbt_test`: Run data quality tests
  - `dbt_run`: Execute historical analytics models

## 📈 Data Pipeline Flow

### 1. Data Generation
- `shipment_api.py` generates realistic shipment data using Faker
- Data includes customer information, shipment details, tracking status, and financial metrics

### 2. Real-time Streaming
- `kafka_producer.py` streams data to Kafka topic `shipments_raw`
- Data is produced at 10 records per second (0.1 second intervals)

### 3. Stream Processing
- `process_and_store_raw_data.py` consumes data from Kafka
- Apache Spark processes and transforms the data
- Raw data is stored in HDFS at `/user/shipment_data/raw/`
- Processed data is stored in HDFS at `/user/shipment_data/processed/`
- Data is normalized into separate tables: customers, shipments, delivery_status, metadata

### 4. Data Warehouse Storage
- Processed data from HDFS is loaded into Snowflake data warehouse
- Data is stored in the `silver` schema for analytics
- HDFS serves as a fault-tolerant storage layer before Snowflake ingestion

### 5. Data Transformation
- dbt models transform raw data into analytics-ready tables
- Business logic is applied for metrics calculation
- Data quality tests ensure data integrity
- Analytics results can be stored back to HDFS at `/user/shipment_data/analytics/`

### 6. Business Intelligence
- Power BI connects to Snowflake for dashboard creation
- Real-time and historical analytics are visualized
- Business insights are generated for decision making

## 🐛 Troubleshooting

### Common Issues and Solutions

1. **HDFS Connection Issues**:
   - Verify HDFS services are running: `jps | grep -E "(NameNode|DataNode)"`
   - Check HDFS status: `hdfs dfsadmin -report`
   - Verify HDFS directories exist: `hdfs dfs -ls /user/shipment_data/`
   - Check HDFS logs in `$HADOOP_HOME/logs/`

2. **Kafka Connection Issues**:
   - Verify Kafka broker is running: `netstat -an | grep 9092`
   - Check broker address in configuration files
   - Ensure topic `shipments_raw` exists

3. **Spark Job Failures**:
   - Check Java version (requires Java 8+)
   - Verify SPARK_HOME environment variable
   - Check Snowflake connectivity and credentials
   - Ensure HDFS is accessible from Spark

4. **Airflow DAG Issues**:
   - Verify DAG files are in the correct directory
   - Check Airflow logs in `/opt/airflow/logs`
   - Ensure dbt project path is correct

5. **dbt Model Failures**:
   - Check Snowflake connection in `~/.dbt/profiles.yml`
   - Verify source table existence in Snowflake
   - Review dbt logs for specific error messages

6. **Data Quality Issues**:
   - Run `dbt test` to identify data quality problems
   - Check source data for null values or format issues
   - Verify data types match expected schemas

### Log Locations
- **Airflow Logs**: `/opt/airflow/logs/`
- **dbt Logs**: `dbt_/logs/`
- **Application Logs**: `logs/`
- **HDFS Logs**: `$HADOOP_HOME/logs/`
- **Kafka Logs**: `$KAFKA_HOME/logs/`

## 📚 Resources and Documentation

### Official Documentation
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [Snowflake Documentation](https://docs.snowflake.com/)
- [dbt Documentation](https://docs.getdbt.com/)
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)

### Project-Specific Resources
- [Faker Documentation](https://faker.readthedocs.io/)
- [Kafka Python Client](https://kafka-python.readthedocs.io/)
- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)

### Project Full Documentation
- [Real-Time-Shipment-Tracking](https://deepwiki.com/Sharaf2OO2/Real-Time-Shipment-Tracking/)

## 📩 Contact

For questions or collaboration opportunities, feel free to reach out:

- [**Gmail**](mailto:sharafahmed2002@gmail.com)
- [**LinkedIn**](https://www.linkedin.com/in/sharaf-ahmed-72955b248/)
- [**X**](https://x.com/SharafAhmed_)
## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Note**: This system is designed for demonstration and learning purposes. For production use, implement proper security measures, error handling, and monitoring capabilities. 
