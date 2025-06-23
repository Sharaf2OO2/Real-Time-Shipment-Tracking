from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Define default arguments for the DAG
default_args = {
    'owner': 'Sharaf',
    'depends_on_past': False,
    'start_date': datetime(2025, 7, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'historical_dag',
    default_args=default_args,
    schedule='0 0 1 */3 *',     # Run on the first day of every third month at midnight
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
    bash_command=f'cd {DBT_PROJECT_DIR} && dbt run --select hist_customer_insights hist_revenue_trends hist_shipment_volume',
    dag=dag,
)

dbt_test >> dbt_run