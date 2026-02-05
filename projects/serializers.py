from rest_framework import serializers
from .models import Project, Task
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TaskSerializer(serializers.ModelSerializer):
    user_assigned_details = UserSerializer(source='user_assigned', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'task_name', 'task_description', 'status', 
            'hours_consumed', 'user_assigned', 'user_assigned_details',
            'start_date', 'end_date'
        ]

class ProjectDetailSerializer(serializers.ModelSerializer):
    # This nests the tasks inside the project response
    tasks = TaskSerializer(many=True, read_only=True)
    user_assigned_details = UserSerializer(source='user_assigned', read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'project_name', 'project_description', 'status', 
            'hours_consumed', 'start_date', 'end_date', 
            'user_assigned', 'user_assigned_details', 'tasks'
        ]

class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'project_name', 'project_description', 'user_assigned', 
            'start_date', 'end_date'
        ]

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'task_name', 'task_description', 
            'user_assigned', 'start_date', 'end_date'
        ]
        