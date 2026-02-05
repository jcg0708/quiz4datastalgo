from rest_framework import generics, permissions
from .models import CustomerUserModel
from .serializers import UserCreateSerializer

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class UserCreateView(generics.CreateAPIView):
    queryset = CustomerUserModel.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAdmin]