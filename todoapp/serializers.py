from rest_framework import  serializers
from django.contrib.auth import get_user_model
from .models import  *


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(write_only=True)
    def validate_email(self,email):
        if get_user_model().objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email already exists")
        return email
    def validate_confirm_password(self,confirm_password):
        if confirm_password != self.initial_data.get('password'):
            raise serializers.ValidationError("Passwords do not match")
        return confirm_password
    def validate_password(self,password):
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")
        elif password.isdigit():
            raise serializers.ValidationError("Password must have at least one letter")
        elif password.isalpha():
            raise serializers.ValidationError("Password must have at least one number")

        return password
    def create(self, validated_data):
        user = get_user_model().objects.create_user(email=validated_data.get('email'),username=validated_data.get('username'),password=validated_data.get('password'))

        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

class TaskSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True)
    def create(self, validated_data):
        tags = validated_data.pop('tag')
        task = Tasks.objects.create(**validated_data)
        for tag in tags:
            tag, created = Tag.objects.get_or_create(**tag)
            task.tag.add(tag)
        return task
    def update(self, instance, validated_data):
        tags = validated_data.pop('tag')
        instance.title = validated_data.get('title',instance.title)
        instance.description = validated_data.get('description',instance.description)
        instance.dead_line = validated_data.get('dead_line',instance.dead_line)
        instance.priority = validated_data.get('priority',instance.priority)
        instance.status = validated_data.get('status',instance.status)
        instance.save()
        instance.tag.clear()
        for tag in tags:
            tag, created = Tag.objects.get_or_create(**tag)
            instance.tag.add(tag)
        return instance
    class Meta:
        model = Tasks
        fields = "__all__"






