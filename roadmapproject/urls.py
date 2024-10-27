from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from roadmapapi.views.users import UserViewSet, register_user, login_user
from roadmapapi.views.projects import ProjectViewSet
from roadmapapi.views.assignments import AssignmentViewSet
from roadmapapi.views.milestones import MilestoneViewSet
from roadmapapi.views.goals import GoalViewSet


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
    path("admin/", admin.site.urls),
]
