from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('pending', 'Pending'),
    ]

    project_name = models.CharField(max_length=200)
    project_description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    hours_consumed = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    user_assigned = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_projects')

    def __str__(self):
        return self.project_name

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    task_name = models.CharField(max_length=200)
    task_description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    hours_consumed = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    user_assigned = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.task_name