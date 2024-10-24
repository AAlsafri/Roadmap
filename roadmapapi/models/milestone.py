from django.db import models
from .project import Project  

class Milestone(models.Model):
    name = models.CharField(max_length=255)
    due_date = models.DateField()
    status = models.CharField(max_length=100, choices=[('open', 'Open'), ('completed', 'Completed'), ('pending','Pending')])
    project = models.ForeignKey(Project, related_name='milestones', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'due_date', 'project')  # When refactoring: alt UniqueConstraint Dj ver2.2

    def __str__(self):
        return self.name