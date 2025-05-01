from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ContactMessage
from .serializers import ContactMessageSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
 

# API for the creating contact 
class ContactMessageCreateView(APIView):
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # action defaults to 'pending'
            return Response({"message": "Message received successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# list all the contact messages   
class ContactMessageListView(ListAPIView):
    serializer_class = ContactMessageSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return ContactMessage.objects.all().order_by('-created_at')

# filtering the message based on the action performed
class ContactMessageByActionView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, action):
        valid_actions = ['pending', 'replied', 'ignored']
        
        if action not in valid_actions:
            return Response({"error": "Invalid action type."}, status=400)

        messages = ContactMessage.objects.filter(action=action).order_by('-created_at')

        if not messages.exists():
            return Response(0)

        serializer = ContactMessageSerializer(messages, many=True)
        return Response(serializer.data)

 
# updating the action field to contact us message
@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def update_contact_action(request, pk):
    try:
        contact = ContactMessage.objects.get(pk=pk)
    except ContactMessage.DoesNotExist:
        return Response({"error": "Message not found."}, status=status.HTTP_404_NOT_FOUND)

    new_action = request.data.get('action')
    if new_action not in dict(ContactMessage.ACTION_CHOICES).keys():
        return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

    contact.action = new_action
    contact.save()

    return Response({"message": "Action updated successfully!"}, status=status.HTTP_200_OK)

