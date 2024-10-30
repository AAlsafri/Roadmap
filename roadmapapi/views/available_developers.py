from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from roadmapapi.models import DeveloperProfile
from roadmapapi.serializers import DeveloperProfileSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def available_developers(request):
    today = timezone.now().date()
    developers = DeveloperProfile.objects.filter(
        is_developer=True,
        skills__isnull=False,
        available_date__gte=today  # Available today or later
    )
    serializer = DeveloperProfileSerializer(developers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)