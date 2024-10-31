from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from roadmapapi.views.users import UserViewSet, register_user, login_user
from roadmapapi.views.projects import ProjectViewSet
from roadmapapi.views.assignments import AssignmentViewSet
from roadmapapi.views.milestones import MilestoneViewSet
from roadmapapi.views.goals import GoalViewSet
from roadmapapi.views.available_developers import available_developers  
from roadmapapi.views.work_request import request_work 
from roadmapapi.views.developers import developers_list 
from roadmapapi.views.unavailable_developers import unavailable_developers as assigned_developers  # Rename the import here

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet, basename='user')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'assignments', AssignmentViewSet, basename='assignment')
router.register(r'milestones', MilestoneViewSet, basename='milestone')
router.register(r'goals', GoalViewSet, basename='goal')  

urlpatterns = [
    path("", include(router.urls)),
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("available-developers/", available_developers, name="available_developers"),  
    path("request-work/", request_work, name="request_work"),  
    path("admin/", admin.site.urls),
    path("developers/", developers_list, name="developers"),
    path("assigned-developers/", assigned_developers, name="assigned_developers"),  # Use the renamed view here
]