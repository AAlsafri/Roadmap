from django.db import models
from .project import Project

class Goal(models.Model):
    project = models.ForeignKey(Project, related_name='goals', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateField()

    class Meta:
        unique_together = ('project', 'name')  # When refactoring: Dj 2.2 UniqueConstraints

    def __str__(self):
        return self.name