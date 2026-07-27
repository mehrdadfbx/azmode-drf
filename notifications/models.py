from django.db import models

from accounts.models import User
from orders.models import Order


class Notification(models.Model):
    type        = models.CharField(max_length=30)
    title       = models.CharField(max_length=255)
    message     = models.TextField()
    target_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='notifications')
    order       = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    is_read     = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title