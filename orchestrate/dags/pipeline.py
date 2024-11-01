from datetime import datetime, timedelta
from airflow.decorators import dag, task # type: ignore
from airflow.operators.bash import BashOperator # type: ignore

default_args = {
    "owner": "meltano",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
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
    @task(task_id="postgres_to_parquet")
    def extract_postgres():
        BashOperator(
            task_id="postgres_to_parquet",
            bash_command='meltano run tap-postgres target-parquet --config "target-parquet.destination_path=./data/postgres/{{{{ table_name }}}}/{{ ds }}"',  # noqa: E501
        ).execute(context=None)

    @task(task_id="csv_to_parquet")
    def extract_csv():
        BashOperator(
            task_id="csv_to_parquet",
            bash_command='meltano run tap-csv target-parquet --config "target-parquet.destination_path=./data/csv/{{ ds }}"',  # noqa: E501
        ).execute(context=None)

    @task(task_id="parquet_to_postgres")
    def load_postgres():
        BashOperator(
            task_id="parquet_to_postgres",
            bash_command='meltano run tap-parquet target-postgres --config "tap-parquet.filepath=./data/**/{{ ds }}/*.parquet"',  # noqa: E501
        ).execute(context=None)

    # Set task dependencies
    [extract_postgres(), extract_csv()] >> load_postgres()


# Create DAG instance
dag = meltano_pipeline()
