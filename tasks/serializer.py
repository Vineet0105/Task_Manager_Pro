from rest_framework import serializers
from .models import Task, Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ['owner']


class TaskSerializer(serializers.ModelSerializer):
    
    def validate_project(self, project):
        if project.owner != self.context["request"].user:
            raise serializers.ValidationError("Invalid project.")
        return project

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ['owner']

