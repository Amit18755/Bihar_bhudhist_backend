from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import OfficialLink
from .serializers import OfficialLinkSerializer

@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_official_link(request):
    serializer = OfficialLinkSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Official Link created successfully!"
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        "message": "There was an error creating the Official Link.",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_official_links(request):
    links = OfficialLink.objects.all().order_by('id')  # Ordered by ID
    serializer = OfficialLinkSerializer(links, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_official_link_by_id(request, pk):
    try:
        link = OfficialLink.objects.get(pk=pk)
        serializer = OfficialLinkSerializer(link)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except OfficialLink.DoesNotExist:
        return Response({
            "message": "Official Link not found."
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_official_link(request, pk):
    try:
        link = OfficialLink.objects.get(pk=pk)
        link.delete()
        return Response({
            "message": "Official Link deleted successfully!"
        }, status=status.HTTP_200_OK)
    except OfficialLink.DoesNotExist:
        return Response({
            "message": "Official Link not found."
        }, status=status.HTTP_404_NOT_FOUND)
 

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_official_link(request, pk):
    try:
        link = OfficialLink.objects.get(pk=pk)
    except OfficialLink.DoesNotExist:
        return Response({
            "message": "Official Link not found."
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = OfficialLinkSerializer(link, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Official Link updated successfully!"
        }, status=status.HTTP_200_OK)
    
    return Response({
        "message": "There was an error updating the Official Link.",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)