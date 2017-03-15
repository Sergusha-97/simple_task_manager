from celery.task import periodic_task, task
from datetime import datetime
from datetime import timedelta
from .models import User, Task
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

TASKS_EMAIL_SENDING_TIME_HOURS = 12
TASK_STATE_CHECKING_TIME_MINUTES = 15


@periodic_task(run_every=timedelta(hours=TASKS_EMAIL_SENDING_TIME_HOURS),
               name="mass_email_sending", ignore_result=True)
def mass_email_sending_task():
    users = User.objects.filter(role=User.DEVELOPER)
    for user in users:
        send_tasks_to_user.delay(user.pk)


@task(name="send_tasks_to_user")
def send_tasks_to_user(user_id):
    user = User.objects.get(pk=user_id)
    tasks = user.tasks.all().filter(is_finished=False)
    if tasks:
        context = {
            'tasks': tasks.filter(due_date__gte=datetime.now()),
            'expired_tasks': tasks.filter(due_date__lt=datetime.now()),
            'user': user
        }
        message = render_to_string('email_templates/tasks_email_template.html', context=context)
        letter = EmailMessage('Tasks status', message, settings.EMAIL_HOST_USER, [user.email])
        letter.content_subtype = "html"
        letter.send()


@periodic_task(run_every=timedelta(minutes=TASK_STATE_CHECKING_TIME_MINUTES),
               name="check_tasks_state", ignore_result=True)
def mass_email_sending_task_state():
    users = User.objects.all()
    for user in users:
        if user.role == User.MANAGER:
            tasks = user.controlled_tasks.all().filter(is_done=False).filter(due_date__gte=datetime.now())
            for task in tasks:
                send_task_to_user.delay(user.pk, task.pk, "This task is overdue")
        elif user.role == User.DEVELOPER:
            tasks = user.tasks.all().filter(is_done=False).filter(due_date__lt=datetime.now())
            for task in tasks:
                if (task.due_date - datetime.now()) < timedelta(hours=1):
                    send_task_to_user.delay(user.pk, task.pk, "You have less than hour to do this task! Hurry up!")


@task(name="send_new_task_to_user")
def send_task_to_user(user_id, task_id, message):
    user = User.objects.get(pk=user_id)
    task = Task.objects.get(pk=task_id)
    context = {
        'message': message,
        'task': task,
        'user': user
    }
    body = render_to_string('email_templates/users_task_email_template.html', context=context)
    letter = EmailMessage('Task notification', body, settings.EMAIL_HOST_USER, [user.email])
    letter.content_subtype = "html"
    letter.send()
