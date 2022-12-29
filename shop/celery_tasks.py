from time import sleep
from celery import shared_task

@shared_task
def notify_customers(messages):
    print("sending 10k messages")
    print(messages)
    sleep(10)
    print("Email sent successfull")