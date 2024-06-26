'''
Put this file in the ~/airflow/dags folder.
'''

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta


with DAG(
    'retrieve_images_511ON',
    default_args = {
        'owner': 'airflow',
        "depends_on_past": False,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 0,
        "retry_delay": timedelta(minutes=5),
    },
    description = "Retrieve real-time CCTV images from 511ON website",
    schedule="@weekly",
    schedule_interval=None,
    start_date=datetime(2024, 6, 21),
    catchup=False,
    tags=["511ON"],
) as dag:
    t1 = BashOperator(
        task_id = "retrieve_images_task1",
        bash_command = "/home/shamir/Documents/GitHub/511ON-streaming/retrieve.sh 0 ",
    )

    t2 = BashOperator(
        task_id = "retrieve_images_task2",
        bash_command = "/home/shamir/Documents/GitHub/511ON-streaming/retrieve.sh 100 ",
    )

    t3 = BashOperator(
        task_id = "retrieve_images_task3",
        bash_command = "/home/shamir/Documents/GitHub/511ON-streaming/retrieve.sh 200 ",
    )

    t4 = BashOperator(
        task_id = "retrieve_images_task4",
        bash_command = "/home/shamir/Documents/GitHub/511ON-streaming/retrieve.sh 300 ",
    )
    
    t5 = BashOperator(
        task_id = "retrieve_images_task5",
        bash_command = "/home/shamir/Documents/GitHub/511ON-streaming/retrieve.sh 400 ",
    )

    t6 = BashOperator(
        task_id = "retrieve_images_task6",
        bash_command = "/home/shamir/Documents/GitHub/511ON-streaming/retrieve.sh 500 ",
    )

    t7 = BashOperator(
        task_id = "retrieve_images_task7",
        bash_command = "/home/shamir/Documents/GitHub/511ON-streaming/retrieve.sh 600 ",
    )

    t8 = BashOperator(
        task_id = "retrieve_images_task8",
        bash_command = "/home/shamir/Documents/GitHub/511ON-streaming/retrieve.sh 700 ",
    )

    t9 = BashOperator(
        task_id = "retrieve_images_task9",
        bash_command = "/home/shamir/Documents/GitHub/511ON-streaming/retrieve.sh 800 ",
    )

    t1 >> t5 >> t9
    t2 >> t6
    t3 >> t7
    t4 >> t8