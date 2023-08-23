from datetime import datetime, timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.providers.microsoft.azure.operators.container_instances import AzureContainerInstancesOperator

default_args = {
    "owner": "Raul Macias",
    "retries": 1,
    "retry_delay": timedelta(seconds=5),
}

with DAG(
    dag_id="best_city_dag",
    max_active_runs=1,
    start_date=datetime(2023, 8, 17),
    schedule=timedelta(days=1),
    catchup=False,
    tags=["azure", "best_city", "container"],
    default_args=default_args,
) as dag:
    opr_run_container = AzureContainerInstancesOperator(
        task_id="run_etl_python_container",
        ci_conn_id="azure_container_conn_id",
        registry_conn_id="raulscontainerreg_conn_id",
        resource_group="my-resource-gp",
        name="best-city-container",
        image="raulscontainerreg.azurecr.io/best-city-python:latest",
        region="East US",
        cpu=1,
        memory_in_gb=1.5,
        fail_if_exists=False,
    )
