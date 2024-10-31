from django.contrib import admin
from .models import Project, Assignment, Milestone, Goal, DeveloperProfile

admin.site.register(Project)
admin.site.register(Assignment)
admin.site.register(Milestone)
admin.site.register(Goal)
admin.site.register(DeveloperProfile)