from rest_framework import generics, status
from rest_framework.response import Response
from .models import Place, PlaceImage
from .serializers import PlaceImageSerializer, PlaceSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

# Create a new Place 
class PlaceCreateView(generics.CreateAPIView):
    serializer_class = PlaceSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "message": "Place created successfully."
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "message": "Error creating place.",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

# Get all Places ordered by ID 
class PlaceListView(generics.ListAPIView):
    serializer_class = PlaceSerializer

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                "message": "Places retrieved successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": "Error retrieving places.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_queryset(self):
        return Place.objects.all().order_by('id')
    

# Delete a Place by ID
class PlaceDeleteView(generics.DestroyAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    lookup_field = 'id'  
    permission_classes = [IsAdminUser]
    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({
                "message": "Place deleted successfully."
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": "Error deleting place.",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


# api to upload images
@api_view(['POST'])
@permission_classes([IsAdminUser])
def upload_place_image(request):
    serializer = PlaceImageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Image uploaded successfully!"}, status=status.HTTP_201_CREATED)
    return Response({
        "message": "Error uploading image.",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_images_by_place(request, place_id):
     
    try:
        place = Place.objects.get(id=place_id)
    except Place.DoesNotExist:
        return Response({
            "message": f"No place found with ID {place_id}.",
            "data": 0
        }, status=status.HTTP_404_NOT_FOUND)

    
    images = PlaceImage.objects.filter(place_id=place_id)

    if not images.exists():
        return Response({
            "message": f"No images found for place ID {place_id}.",
            "data": 0
        }, status=status.HTTP_200_OK)

     
    serializer = PlaceImageSerializer(images, many=True)
    return Response({
        "message": f"Images retrieved successfully for place ID {place_id}.",
        "data": serializer.data
    }, status=status.HTTP_200_OK)


# delete a image with id
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_place_image(request, image_id):
    try:
        image = PlaceImage.objects.get(id=image_id)
        image.delete()
        return Response({
            "message": f"Image with ID {image_id} deleted successfully."
        }, status=status.HTTP_200_OK)
    except PlaceImage.DoesNotExist:
        return Response({
            "message": f"No image found with ID {image_id}.",
            "data": 0
        }, status=status.HTTP_404_NOT_FOUND)