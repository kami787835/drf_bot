from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    ordering = ['timestamp']  # Сортировка по времени
    list_display = ('user_id', 'username', 'first_name', 'last_name', 'text', 'timestamp')  # Отображение поля timestamp

admin.site.register(Message, MessageAdmin)
