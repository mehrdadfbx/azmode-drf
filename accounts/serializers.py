from rest_framework import serializers
from .models import User


class AdminCreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=4)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'phone', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user