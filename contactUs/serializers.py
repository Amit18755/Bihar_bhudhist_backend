from rest_framework import serializers
from .models import ContactMessage

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'phone_number', 'message', 'action', 'created_at']
        read_only_fields = ['action', 'created_at']   
