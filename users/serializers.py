from rest_framework import serializers
from .models import CustomerUserModel

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomerUserModel
        fields = ['first_name', 'last_name', 'username', 'email', 'role', 'password']

    def create(self, validated_data):
        user = CustomerUserModel.objects.create_user(**validated_data)
        return user