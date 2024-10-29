from rest_framework import serializers
from django.contrib.auth.models import User
from roadmapapi.models import Project, Assignment, Milestone, Goal

# *** Users ***
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        extra_kwargs = {'password': {'write_only': True}}

# *** Projects ***
class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    assigned_users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'assigned_users', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        assigned_users = validated_data.pop('assigned_users', [])
        project = Project.objects.create(**validated_data)
        project.assigned_users.set(assigned_users)
        return project

    def update(self, instance, validated_data):
        assigned_users = validated_data.pop('assigned_users', None)
        if assigned_users is not None:
            instance.assigned_users.set(assigned_users)
        return super().update(instance, validated_data)

# *** Assignments ***
class AssignmentSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Assignment
        fields = ['id', 'project', 'user', 'role']

# *** Milestones ***
class MilestoneSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Milestone
        fields = ['id', 'name', 'due_date', 'status', 'project']

# *** Goals ***
class GoalSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = ['id', 'project', 'name', 'description', 'deadline']