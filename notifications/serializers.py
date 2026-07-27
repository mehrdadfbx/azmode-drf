from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id',
            'type',
            'title',
            'message',
            'order',
            'is_read',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'type',
            'title',
            'message',
            'order',
            'created_at',
        ]