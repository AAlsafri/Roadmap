from rest_framework import viewsets
from roadmapapi.serializers import MilestoneSerializer
from roadmapapi.models.milestone import Milestone

class MilestoneViewSet(viewsets.ModelViewSet):
    queryset = Milestone.objects.all()
    serializer_class = MilestoneSerializer