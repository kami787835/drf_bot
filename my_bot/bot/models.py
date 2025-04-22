from django.db import models
from django.utils.timezone import now

class Message(models.Model):
    user_id = models.BigIntegerField(verbose_name="ID пользователя")
    username = models.CharField(max_length=255, blank=True, null=True, verbose_name="Username")
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Имя")
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Фамилия")
    text = models.TextField(verbose_name="Текст сообщения")
    timestamp = models.DateTimeField(default=now, verbose_name="Время отправки")  # Добавляем время
