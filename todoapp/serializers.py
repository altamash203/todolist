from rest_framework import  serializers
from django.contrib.auth import get_user_model,authenticate
from django.contrib.auth.password_validation import  validate_password
from .models import  *


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = get_user_model()
        fields = ['username','email','password']
        extra_kwargs = {'password':{'write_only':True}}

    def validate_password(self,attr):
        password = attr.get('password')
        password2 = attr.get('password2')
        if password != password2:
            raise  serializers.ValidationError("Password Does not match")
        return attr

    def create(self,validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True,required=True)

    def validat(self,attrs):
        email = attrs.get('email')
        password =attrs.get('password')
        user = authenticate(email=email,password=password)
        if not user:
            raise serializers.ValidationError("Invalid Credentials")
        return attrs





class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tasks
        fields = "__all__"

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class UserSignupSerializer(serializers.ModelSerializer):
   password = serializers.CharField(write_only=True)

class UserLoginSerializer(serializers.ModelSerializer):
   username = serializers.CharField()
   password = serializers.CharField(write_only=True)
