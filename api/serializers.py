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
