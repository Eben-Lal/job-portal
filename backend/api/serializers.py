from rest_framework import serializers

from django.contrib.auth.password_validation import validate_password
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('fname', 'lname', 'email', 'phone_number', 'phone_number',
                  'role', 'password')
        extra_kwargs = {
            'email': {'required': True},
            'role': {'required': True}
        }


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(
        write_only=True, required=True)  # confirm password

    class Meta:
        model = CustomUser
        fields = ('email', 'role', 'password', 'password2', 'fname', 'lname',)
        extra_kwargs = {'email': {'required': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)

        return user
