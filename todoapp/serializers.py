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


class UserSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields ="__all__"

