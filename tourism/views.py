from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import TouristPlace
from .serializers import TouristPlaceSerializer
from rest_framework.permissions import IsAdminUser

@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_tourist_place(request):
    serializer = TouristPlaceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Tourist Place created successfully!"
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        "message": "There was an error creating the Tourist Place.",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_tourist_places(request):
    places = TouristPlace.objects.all().order_by('id')
    serializer = TouristPlaceSerializer(places, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_tourist_place_by_id(request, pk):
    try:
        place = TouristPlace.objects.get(pk=pk)
        serializer = TouristPlaceSerializer(place)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except TouristPlace.DoesNotExist:
        return Response({
            "message": "Tourist Place not found."
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_tourist_place(request, pk):
    try:
        place = TouristPlace.objects.get(pk=pk)
        place.delete()
        return Response({
            "message": "Tourist Place deleted successfully!"
        }, status=status.HTTP_200_OK)
    except TouristPlace.DoesNotExist:
        return Response({
            "message": "Tourist Place not found."
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_tourist_place(request, pk):
    try:
        place = TouristPlace.objects.get(pk=pk)
    except TouristPlace.DoesNotExist:
        return Response({
            "message": "Tourist Place not found."
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = TouristPlaceSerializer(place, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Tourist Place updated successfully!"
        }, status=status.HTTP_200_OK)
    
    return Response({
        "message": "There was an error updating the Tourist Place.",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
