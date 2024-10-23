from django.db import models
from django.contrib.auth.models import User
from .project import Project

class Assignment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)

    class Meta:
        unique_together = ('project', 'user')

    def __str__(self):
        return f"{self.user.username} assigned to {self.project.name} as {self.role}"