from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from roadmapapi.models import Goal, Project

class GoalViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="goaluser", password="password123")
        self.project = Project.objects.create(name="Test Project", description="A test project", owner=self.user)
        self.goal_data = {
            "name": "Complete Phase 1",
            "description": "Goal description",
            "project": self.project,
            "deadline": "2024-12-31"
        }
        self.goal = Goal.objects.create(**self.goal_data)
        self.client.force_authenticate(user=self.user)

    def test_list_goals(self):
        response = self.client.get("/goals", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_goal(self):
        response = self.client.get(f"/goals/{self.goal.id}", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.goal_data["name"])

    def test_update_goal(self):
        updated_data = {
            "name": "Complete Phase 2",
            "description": "Updated goal description",
            "project": self.project.id,
            "deadline": "2025-01-15"
        }
        response = self.client.put(f"/goals/{self.goal.id}", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.goal.refresh_from_db()
        self.assertEqual(self.goal.name, "Complete Phase 2")
        self.assertEqual(self.goal.description, "Updated goal description")

    def test_delete_goal(self):
        response = self.client.delete(f"/goals/{self.goal.id}", format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Goal.objects.filter(id=self.goal.id).exists())