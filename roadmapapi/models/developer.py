from django.db import models
from django.contrib.auth.models import User

class DeveloperProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="developer_profile")
    is_developer = models.BooleanField(default=False)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    years_of_experience = models.IntegerField(blank=True, null=True)