from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from roadmapapi.models import Project, Assignment  # Ensure Assignment is imported
from roadmapapi.serializers import ProjectSerializer
from django.db.models import Q

class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        # Include projects owned by the user or where the user is assigned
        user = self.request.user
        return Project.objects.filter(
            Q(owner=user) | Q(assigned_users=user)
        ).distinct()

    def retrieve(self, request, pk=None):
        # Retrieve a specific project with ownership or assignment check
        try:
            project = Project.objects.get(pk=pk)
            if project.owner != request.user and request.user not in project.assigned_users.all():
                return Response({"error": "Not authorized to view this project"}, status=status.HTTP_403_FORBIDDEN)
            serializer = ProjectSerializer(project)
            return Response(serializer.data)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        # Create a new project and automatically set the owner
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        # Update an existing project with ownership check
        try:
            project = Project.objects.get(pk=pk)
            if project.owner != request.user:
                return Response({"error": "Not authorized to update this project"}, status=status.HTTP_403_FORBIDDEN)
            serializer = ProjectSerializer(project, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        # Delete a project with ownership check and reassign developers
        try:
            project = Project.objects.get(pk=pk)
            if project.owner != request.user:
                return Response({"error": "Not authorized to delete this project"}, status=status.HTTP_403_FORBIDDEN)

            # Unassign developers from this project
            Assignment.objects.filter(project=project).delete()

            # Now delete the project itself
            project.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)