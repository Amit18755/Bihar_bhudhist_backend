from rest_framework import serializers
from .models import TouristPlace
import base64

class TouristPlaceSerializer(serializers.ModelSerializer):
    place_image = serializers.SerializerMethodField()
    image_upload = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = TouristPlace
        fields = ['id', 'place_name', 'place_address', 'place_description', 'place_image', 'image_upload']

    def get_place_image(self, obj):
        if obj.place_image:
            return base64.b64encode(obj.place_image).decode('utf-8')
        return None

    def create(self, validated_data):
        image_data = validated_data.pop('image_upload', None)
        if image_data:
            validated_data['place_image'] = base64.b64decode(image_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        image_data = validated_data.pop('image_upload', None)
        if image_data:
            instance.place_image = base64.b64decode(image_data)
        return super().update(instance, validated_data)
