from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, ValidationError
import re

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, write_only=True,
                                   validators = [UniqueValidator(queryset = User.objects.all())])
    username = serializers.CharField(required=True, write_only=True,
                                   validators = [UniqueValidator(queryset = User.objects.all())])
    password = serializers.CharField(required=True, min_length=8,write_only=True)

    def validate_password(self, value):
        if not re.search(r'[A-Z]', value):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[0-9]', value):
            raise ValidationError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValidationError("Password must contain at least one special character.")
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(username = validated_data['username'],
                                        email = validated_data['email'],
                                        password = validated_data['password']
                                        )

        return user
        
    class Meta:
        model = User
        fields = ['email','username','password']
