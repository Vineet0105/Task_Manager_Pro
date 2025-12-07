from celery import shared_task
import time
from django.utils import timezone
from .models import Task

@shared_task
def check_overdue_tasks():
    print("\n[CELERY BEAT] Checking overdue tasks...")
    now = timezone.now()
    overdue = Task.objects.filter(status='todo', due_date__lt = now)
    for task in overdue:
        print(f"[OVERDUE] {task.title} (ID={task.id})")

@shared_task
def send_deadline_reminder(task_id):
    print(f"[CELERY] Task started: reminder for task_id={task_id}")
    time.sleep(5)
    print(f"[CELERY] Reminder sent for task_id={task_id}")