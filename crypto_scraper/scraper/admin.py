from django.contrib import admin
from .models import Job, Task

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('job', 'coin', 'status')
