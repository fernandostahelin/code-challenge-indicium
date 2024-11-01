from datetime import datetime, timedelta
from airflow.decorators import dag, task  # type: ignore
from airflow.operators.bash import BashOperator  # type: ignore

default_args = {
    "owner": "Fernando Stahelin",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define common environment variables
env_vars = {
    "EXECUTION_DATE": "{{ ds }}",  # Airflow's execution date
}

@dag(
    "meltano_pipeline",
    default_args=default_args,
    description="Incremental load from postgres/csv to parquet and then to postgres.",
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
)
def meltano_pipeline():
    @task.bash(task_id="postgres_to_parquet")
    def extract_postgres():
        return "meltano run tap-postgres target-parquet"

    @task.bash(task_id="csv_to_parquet")
    def extract_csv():
        return "meltano run tap-csv target-parquet"

    @task.bash(task_id="parquet_to_postgres")
    def load_postgres():
        return "meltano run tap-parquet target-postgres"

    [extract_postgres(), extract_csv()] >> load_postgres()


dag = meltano_pipeline()
