from django.db import models
import uuid

class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class Task(models.Model):
    job = models.ForeignKey(Job, related_name='tasks', on_delete=models.CASCADE)
    coin = models.CharField(max_length=10)
    status = models.CharField(max_length=20, default='pending')
    result = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.coin} - {self.status}"
