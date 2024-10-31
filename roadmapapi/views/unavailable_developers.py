from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from roadmapapi.models import DeveloperProfile, Assignment
from roadmapapi.serializers import DeveloperProfileSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unavailable_developers(request):
    # Fetch all developers who are assigned to at least one project
    assigned_developers = DeveloperProfile.objects.filter(
        is_developer=True,
        user__assignment__isnull=False
    ).distinct()

    serializer = DeveloperProfileSerializer(assigned_developers, many=True)
    return Response(serializer.data)