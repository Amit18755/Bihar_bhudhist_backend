from rest_framework import serializers
from .models import ExtendedUser
from django.contrib.auth.models import User


class ExtendedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtendedUser
        fields = ['id', 'username', 'role', 'auth_user_id']


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    role = serializers.ChoiceField(choices=ExtendedUser.ROLE_CHOICES)

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value.strip().upper()).exists():
            raise serializers.ValidationError("Username already exists.")
        return value.strip().upper()

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value.strip().upper()).exists():
            raise serializers.ValidationError("Email already exists.")
        return value.strip().upper()

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        first_name = validated_data['first_name'].strip().upper()
        last_name = validated_data.get('last_name', '').strip().upper()
        password = validated_data['password']
        role = validated_data['role']

        # Create User instance and set password securely
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_staff=True
        )
        user.set_password(password)
        user.save()

        # Create ExtendedUser
        ExtendedUser.objects.create(
            username=username,
            role=role,
            auth_user_id=user
        )

        return {"username": username, "email": email, "role": role}
    

class UserDetailSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='auth_user_id.first_name')
    last_name = serializers.CharField(source='auth_user_id.last_name')
    email = serializers.EmailField(source='auth_user_id.email')
    role = serializers.CharField()

    class Meta:
        model = ExtendedUser
        fields = ['username', 'first_name', 'last_name', 'email', 'role']

class UpdateUserRoleSerializer(serializers.Serializer):
    username = serializers.CharField()
    role = serializers.ChoiceField(choices=ExtendedUser.ROLE_CHOICES)

 

class UpdateUserDetailsSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField()

    def validate_email(self, value):
        email = value.strip().upper()
        username = self.initial_data.get("username").strip().upper()
        if User.objects.filter(email__iexact=email).exclude(username__iexact=username).exists():
            raise serializers.ValidationError("Email already exists.")
        return email

    def update(self, instance, validated_data):
        user = instance.auth_user_id
        user.first_name = validated_data['first_name'].strip().upper()
        user.last_name = validated_data.get('last_name', '').strip().upper()
        user.email = validated_data['email'].strip().upper()
        user.save()
        return instance
