from celery import task

from .email import process_email

@task()
def tickManage_process_email():
    process_email()