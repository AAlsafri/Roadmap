from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from roadmapapi.models import DeveloperProfile
from roadmapapi.serializers import DeveloperProfileSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_work(request):
    profile = request.user.developer_profile
    serializer = DeveloperProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)