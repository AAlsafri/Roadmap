from rest_framework import viewsets
from roadmapapi.serializers import GoalSerializer
from roadmapapi.models.goal import Goal

class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer