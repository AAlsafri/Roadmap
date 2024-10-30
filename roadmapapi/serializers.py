from rest_framework import serializers
from django.contrib.auth.models import User
from roadmapapi.models import Project, Assignment, Milestone, Goal, DeveloperProfile

# *** User Serializer (Basic for Developer Profile Inclusion) ***
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']

# *** Developer Profile Serializer ***
class DeveloperProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Include nested user details

    class Meta:
        model = DeveloperProfile
        fields = ['user', 'is_developer', 'job_title', 'years_of_experience', 'skills', 'available_date']

# *** User Serializer with Developer Profile ***
class UserWithProfileSerializer(serializers.ModelSerializer):
    developer_profile = DeveloperProfileSerializer(required=False)
    password = serializers.CharField(write_only=True)  # Explicitly add the password field

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'developer_profile']

    def create(self, validated_data):
        developer_data = validated_data.pop('developer_profile', None)
        password = validated_data.get('password')
        if not password:
            raise serializers.ValidationError({"password": "Password is required."})
        validated_data.pop('password')  # Remove password to pass it separately
        user = User.objects.create_user(password=password, **validated_data)
        if developer_data:
            DeveloperProfile.objects.create(user=user, **developer_data)
        return user

    def update(self, instance, validated_data):
        developer_data = validated_data.pop('developer_profile', None)
        instance = super().update(instance, validated_data)
        if developer_data:
            DeveloperProfile.objects.update_or_create(user=instance, defaults=developer_data)
        return instance

# *** Milestone Serializer ***
class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = ['id', 'name', 'due_date', 'status', 'project']

# *** Goal Serializer ***
class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'project', 'name', 'description', 'deadline']
        read_only_fields = ['project']

# *** Project Serializer ***
class ProjectSerializer(serializers.ModelSerializer):
    owner = UserWithProfileSerializer(read_only=True)
    assigned_users = UserWithProfileSerializer(many=True, read_only=True)
    milestones = MilestoneSerializer(many=True, read_only=True)
    goals = GoalSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'owner', 'assigned_users', 
            'created_at', 'updated_at', 'milestones', 'goals'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        assigned_user_ids = self.initial_data.get('assigned_users', [])
        project = Project.objects.create(
            name=validated_data['name'],
            description=validated_data['description'],
            owner=validated_data.get('owner')
        )
        project.assigned_users.set(assigned_user_ids)
        for user_id in assigned_user_ids:
            user = User.objects.get(id=user_id)
            Assignment.objects.create(user=user, project=project, role="Developer")
        return project

    def update(self, instance, validated_data):
        assigned_user_ids = self.initial_data.get('assigned_users', None)
        if assigned_user_ids is not None:
            instance.assigned_users.set(assigned_user_ids)
            Assignment.objects.filter(project=instance).delete()
            for user_id in assigned_user_ids:
                user = User.objects.get(id=user_id)
                Assignment.objects.create(user=user, project=instance, role="Developer")
        return super().update(instance, validated_data)

# *** Assignment Serializer ***
class AssignmentSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Assignment
        fields = ['id', 'project', 'user', 'role']