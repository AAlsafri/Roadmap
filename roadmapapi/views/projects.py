from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from roadmapapi.models import Project
from roadmapapi.serializers import ProjectSerializer

class ProjectViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access

    def list(self, request):
        projects = Project.objects.filter(owner=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            project = Project.objects.get(pk=pk)
            if project.owner != request.user:
                return Response({"error": "Not authorized to view this project"}, status=status.HTTP_403_FORBIDDEN)
            serializer = ProjectSerializer(project)
            return Response(serializer.data)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = ProjectSerializer(data={**request.data, "owner": request.user.id})
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
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

    def partial_update(self, request, pk=None):
        try:
            project = Project.objects.get(pk=pk)
            if project.owner != request.user:
                return Response({"error": "Not authorized to update this project"}, status=status.HTTP_403_FORBIDDEN)
            serializer = ProjectSerializer(project, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            project = Project.objects.get(pk=pk)
            if project.owner != request.user:
                return Response({"error": "Not authorized to delete this project"}, status=status.HTTP_403_FORBIDDEN)
            project.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)