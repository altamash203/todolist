from rest_framework import  serializers
from .models import  *


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
