from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime, timedelta

# Define default arguments for the DAG
default_args = {
    'owner': 'Sharaf',
    'depends_on_past': False,
    'start_date': datetime(2025, 6, 20),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'stream_dag',
    default_args=default_args,
    schedule='*/2 * * * *',  # Run every minute
    catchup=False,
)

DBT_PROJECT_DIR = "/opt/airflow/dbt_"

dbt_test = BashOperator(
    task_id='dbt_test',
    bash_command=f'cd {DBT_PROJECT_DIR} && dbt test',
    dag=dag,
)

dbt_run = BashOperator(
    task_id='dbt_run',
    bash_command=f'cd {DBT_PROJECT_DIR} && dbt run --select cost_analysis customer_insights delivery_performance operational_insights shipment_tracking shipments_overview',
    dag=dag,
)

dbt_test >> dbt_run