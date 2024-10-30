from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from roadmapapi.models import DeveloperProfile, Assignment
from roadmapapi.serializers import DeveloperProfileSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def developers_list(request):
    # Fetch developers based on assignments
    assigned_developers = DeveloperProfile.objects.filter(
        is_developer=True,
        user__assignment__isnull=False  # Check if developer has an assignment
    ).distinct()

    available_developers = DeveloperProfile.objects.filter(
        is_developer=True,
        user__assignment__isnull=True  # Check if developer has no assignment
    )

    assigned_serializer = DeveloperProfileSerializer(assigned_developers, many=True)
    available_serializer = DeveloperProfileSerializer(available_developers, many=True)

    return Response({
        "assigned_developers": assigned_serializer.data,
        "available_developers": available_serializer.data,
    })