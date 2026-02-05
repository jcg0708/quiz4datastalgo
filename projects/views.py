from rest_framework import generics, permissions
from django.utils import timezone
from .models import Project
from .serializers import ProjectSerializer, ProjectCreateSerializer
from tasks.models import Task

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class ProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Project.objects.all()
        elif user.role == 'manager':

            return Project.objects.filter(manager=user)
        else:
            
            
            return Project.objects.filter(tasks__user_assigned=user).distinct()

class ProjectDetailView(generics.RetrieveAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        
        user = self.request.user
        if user.role == 'admin':
            return Project.objects.all()
        elif user.role == 'manager':
            return Project.objects.filter(manager=user)
        else:
            return Project.objects.filter(tasks__user_assigned=user).distinct()

class ProjectCreateView(generics.CreateAPIView):
    serializer_class = ProjectCreateSerializer
    permission_classes = [IsAdmin] 

    def perform_create(self, serializer):
        start_date = serializer.validated_data.get('start_date')
        today = timezone.now().date()
        
        status = 'CREATED'
        if start_date == today:
            status = 'IN PROGRESS'
        
        serializer.save(status=status)