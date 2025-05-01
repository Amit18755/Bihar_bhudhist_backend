# overview/serializers.py
from rest_framework import serializers
from .models import Overview, OverviewImage
import base64

class OverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Overview
        fields = ['id', 'details']


class OverviewImageSerializer(serializers.ModelSerializer):
    image_base64 = serializers.SerializerMethodField()
    image_upload = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = OverviewImage
        fields = ['id', 'image_base64', 'image_upload', 'uploaded_at']

    def get_image_base64(self, obj):
        if obj.image:
            return base64.b64encode(obj.image).decode('utf-8')
        return None

    def create(self, validated_data):
        image_data = validated_data.pop('image_upload', None)
        if image_data:
            validated_data['image'] = base64.b64decode(image_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        image_data = validated_data.pop('image_upload', None)
        if image_data:
            instance.image = base64.b64decode(image_data)
        return super().update(instance, validated_data)
