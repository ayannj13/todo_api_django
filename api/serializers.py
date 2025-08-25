from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    # show the owner as text; we’ll set it automatically on create
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = ["id", "title", "description", "status", "user", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
    
from django.contrib.auth import get_user_model
from rest_framework import serializers
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    # enforce min length 6 per the task
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password")

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
