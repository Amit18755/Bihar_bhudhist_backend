import os
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from user.serializers import UpdateUserDetailsSerializer, UpdateUserRoleSerializer, UserCreateSerializer, UserDetailSerializer
from .models import ExtendedUser
from django.contrib.auth.models import User
from rest_framework.decorators import api_view 
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view,permission_classes
from django.core.mail import send_mail
import random 

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            # Creating JWT token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Getting extended user data
            try:
                extended = ExtendedUser.objects.get(auth_user_id=user.id)
                role = extended.role
            except ExtendedUser.DoesNotExist:
                role = 'none'

            response = Response({
                'username': user.username,
                'auth_user_id': user.id,
                'role': role,
                'access_token': access_token,
            }, status=status.HTTP_200_OK)

            # Setting token in cookie for further use
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                samesite='Lax',
                secure=False  # Set True in production 
            )

            return response

        return Response({'detail': 'Invalid Username or Password'}, status=status.HTTP_401_UNAUTHORIZED)



class ForgetPasswordView(APIView):
    def post(self, request):
        username = request.data.get("username")
        new_password = request.data.get("new_password")
        otp = request.data.get("otp")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            extended_user = ExtendedUser.objects.get(auth_user_id=user.id)
        except ExtendedUser.DoesNotExist:
            return Response({"detail": "Extended user not found"}, status=status.HTTP_404_NOT_FOUND)

        if extended_user.otp != otp:
            return Response({"detail": "OTP doesn't match"}, status=status.HTTP_400_BAD_REQUEST)

        # OTP matched, now reset password and clear OTP
        user.set_password(new_password)
        user.save()

        extended_user.otp = None
        extended_user.save()

        return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)


class SendOTPView(APIView):
    def post(self, request):
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "Username not found"}, status=status.HTTP_404_NOT_FOUND)

        #  6 digit otp is generated
        otp = random.randint(100000, 999999)

        # Storing OTP in ExtendedUser
        try:
            extended_user = ExtendedUser.objects.get(auth_user_id=user)
            extended_user.otp = otp
            extended_user.save()
        except ExtendedUser.DoesNotExist:
            return Response({"detail": "Extended user record not found."}, status=status.HTTP_404_NOT_FOUND)

        # Sending  email
        subject = "Your OTP Code for Password Reset"
        message = f"Dear user, your OTP code for reset password is: {otp}"
        send_mail(
            subject,
            message,
            os.getenv('EMAIL_HOST_USER'),
            [user.email],
            fail_silently=False,
        )

        return Response({"detail": "OTP sent successfully to registered email."}, status=status.HTTP_200_OK)



class CreateUserView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=201)
        return Response(serializer.errors, status=400)


 

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def change_password(request):
    username = request.data.get("username")
    new_password = request.data.get("new_password")

    try:
        user = User.objects.get(username=username.upper())
        user.password = make_password(new_password)
        user.save()
        return Response({"message": "Password updated successfully!"}, status=200)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=404)
    


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_users(request):
    # Exclude the user with id=1 from the query (just for safe purpose)
    users = ExtendedUser.objects.exclude(id=1)
    serializer = UserDetailSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def update_user_role(request):
    serializer = UpdateUserRoleSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        new_role = serializer.validated_data['role']

        try:
            user = ExtendedUser.objects.get(username=username)
            user.role = new_role
            user.save()
            return Response({"message": f"Role updated to '{new_role}' for user '{username}'."})
        except ExtendedUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# views.py

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_user_by_username(request, username):
    try:
        user = ExtendedUser.objects.get(username=username.strip().upper())
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)
    except ExtendedUser.DoesNotExist:
        return Response({"error": "User not found."}, status=404)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_user_details(request):
    serializer = UpdateUserDetailsSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username'].strip().upper()
        try:
            extended_user = ExtendedUser.objects.get(username=username)
            serializer.update(extended_user, serializer.validated_data)
            return Response({"message": "User details updated successfully!"})
        except ExtendedUser.DoesNotExist:
            return Response({"error": "User not found."}, status=404)
    return Response(serializer.errors, status=400)
