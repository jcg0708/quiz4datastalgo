from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Sum
from .models import Task
from projects.models import Project
from datetime import date

# Signal 1: Calculate Task Hours when COMPLETED
@receiver(pre_save, sender=Task)
def calculate_task_hours(sender, instance, **kwargs):
    if instance.pk: # Only on update
        try:
            old_instance = Task.objects.get(pk=instance.pk)
            # Check if status changed to COMPLETED
            if instance.status == 'COMPLETED' and old_instance.status != 'COMPLETED':
                if instance.start_date:
                    today = timezone.now().date()
                    # Calculation: (Date Completed - Start Date) * 24
                    delta = today - instance.start_date
                    # Ensure at least 24 hours if completed same day or later
                    days = delta.days if delta.days > 0 else 1 
                    # If marked completed same day (0 days diff), request implies 24 hours (01/01 to 01/02 example)
                    # Correct logic based on example: 01/01 to 01/03 = 2 days = 48 hours.
                    # 01/01 to 01/01 = 0 days.
                    
                    # Let's stick strictly to day difference * 24.
                    # Example: Start Jan 1. Mark Complete Jan 3. Delta = 2 days. Hours = 48.
                    calculated_hours = delta.days * 24
                    
                    # Edge case: If completed on same day as start, delta is 0. 
                    # Assuming minimum 24 hours based on "01/01 to 01/02 is 24".
                    if calculated_hours == 0:
                        calculated_hours = 24
                        
                    instance.hours_consumed = calculated_hours
        except Task.DoesNotExist:
            pass

# Signal 2: Recalculate Project Hours when Task hours change
@receiver(post_save, sender=Task)
def update_project_hours(sender, instance, **kwargs):
    project = instance.project
    total_hours = project.tasks.aggregate(total=Sum('hours_consumed'))['total'] or 0.00
    project.hours_consumed = total_hours
    project.save()