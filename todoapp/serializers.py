from rest_framework import  serializers
from django.contrib.auth import get_user_model,authenticate
from .models import  *


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = get_user_model()
        fields = ['username','email','password']




class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True,required=True)



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"



class TaskSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    class Meta:
        model = Tasks
        fields = "__all__"




