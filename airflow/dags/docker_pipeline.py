from datetime import datetime, timedelta
from airflow.decorators import dag
from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
    "owner": "Fernando Stahelin",
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
    # Common configuration for all tasks
    docker_config = {
        'image': 'code_challenge_indicium-meltano-1',  # Your local image name
        'api_version': 'auto',
        'auto_remove': True,
        'network_mode': 'code_challenge_indicium_default',  # Your Docker network
        'mount_tmp_dir': False,
        'volumes': ['/Users/fernandostahelin/Projetos/code_challenge_indicium:/project'],  # Map your project directory
    }

    extract_postgres = DockerOperator(
        task_id='postgres_to_parquet',
        command='run tap-postgres target-parquet',
        environment={'EXECUTION_DATE': '{{ ds }}'},
        **docker_config
    )

    extract_csv = DockerOperator(
        task_id='csv_to_parquet',
        command='run tap-csv target-parquet',
        environment={'EXECUTION_DATE': '{{ ds }}'},
        **docker_config
    )

    load_postgres = DockerOperator(
        task_id='parquet_to_postgres',
        command='run tap-parquet target-postgres',
        environment={'EXECUTION_DATE': '{{ ds }}'},
        **docker_config
    )

    [extract_postgres, extract_csv] >> load_postgres

dag = meltano_pipeline()