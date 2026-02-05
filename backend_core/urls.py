"""
URL configuration for backend_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from projects.views import ProjectListView, ProjectDetailView, ProjectCreateView
from tasks.views import TaskCreateView
from users.views import UserCreateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Users
    path('api/v1/users/create/', UserCreateView.as_view()),

    # Projects
    path('api/v1/projects/', ProjectListView.as_view()),
    path('api/v1/projects/<int:pk>/', ProjectDetailView.as_view()),
    path('api/v1/projects/create/', ProjectCreateView.as_view()),

    # Tasks
    path('api/v1/tasks/create/', TaskCreateView.as_view()),
]