from rest_framework import serializers
from .models import Place, PlaceImage
import base64
from django.core.files.base import ContentFile

# Serializer for adding & deleting only Place
class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'heading', 'district']

# Serializer for adding & deleting images only
class PlaceImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    image_upload = serializers.CharField(write_only=True, required=True)
    place_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = PlaceImage
        fields = ['id', 'image', 'image_upload', 'place_id']

    def get_image(self, obj):
        if obj.image:
            return base64.b64encode(obj.image).decode('utf-8')
        return None

    def create(self, validated_data):
        image_data = validated_data.pop('image_upload')
        place_id = validated_data.pop('place_id')

        try:
            place = Place.objects.get(id=place_id)
        except Place.DoesNotExist:
            raise serializers.ValidationError({'place_id': 'No place found with this ID.'})

        binary_data = base64.b64decode(image_data)
        return PlaceImage.objects.create(place=place, image=binary_data)