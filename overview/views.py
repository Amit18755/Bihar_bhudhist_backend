from rest_framework import generics, status
from rest_framework.response import Response
from .models import Overview, OverviewImage
from .serializers import OverviewImageSerializer, OverviewSerializer
from rest_framework.permissions import IsAdminUser

# List all Overviews
class OverviewListView(generics.ListAPIView):
    queryset = Overview.objects.all()
    serializer_class = OverviewSerializer

# Create a new Overview (used only one time after that just update the overview)
class OverviewCreateView(generics.CreateAPIView):
    queryset = Overview.objects.all()
    serializer_class = OverviewSerializer
    permission_classes = [IsAdminUser]

# Update an existing Overview
class OverviewUpdateView(generics.UpdateAPIView):
    queryset = Overview.objects.all()
    serializer_class = OverviewSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdminUser]

# List Overview images 
class OverviewImageListView(generics.ListAPIView):
    queryset = OverviewImage.objects.all()
    serializer_class = OverviewImageSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "message": "Images retrieved successfully.",
            "data": serializer.data
        })
# Create a new Overview Image
class OverviewImageCreateView(generics.CreateAPIView):
    queryset = OverviewImage.objects.all()
    serializer_class = OverviewImageSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "success": True,
                "message": "Image uploaded successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "success": False,
            "message": "Failed to upload image.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# Update an existing Overview Image
class OverviewImageUpdateView(generics.UpdateAPIView):
    queryset = OverviewImage.objects.all()
    serializer_class = OverviewImageSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({
                "success": True,
                "message": "Image updated successfully.",
                "data": serializer.data
            })
        return Response({
            "success": False,
            "message": "Failed to update image.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# Delete an Overview Image
class OverviewImageDeleteView(generics.DestroyAPIView):
    queryset = OverviewImage.objects.all()
    serializer_class = OverviewImageSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdminUser]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "success": True,
            "message": "Image deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)