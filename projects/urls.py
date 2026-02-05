from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ProjectTaskCreateView

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('projects/<int:project_id>/tasks/', ProjectTaskCreateView.as_view(), name='project-task-create'),
]