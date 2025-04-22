from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(required=False)  # Django сам преобразует в дату

    class Meta:
        model = Message
        fields = "__all__"
