from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from roadmapapi.models import Assignment, Project  

class AssignmentViewSetTests(APITestCase):
    def setUp(self):

        self.user = User.objects.create_user(username="testuser", password="password123")
        
        
        self.project = Project.objects.create(name="Test Project", description="A test project", owner=self.user)
        
        self.assignment_data = {
            "project": self.project,
            "user": self.user,
            "role": "Developer"
        }
        self.assignment = Assignment.objects.create(**self.assignment_data)
        
        self.client.force_authenticate(user=self.user)

    def test_list_assignments(self):
        response = self.client.get("/assignments", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_assignment(self):
        response = self.client.get(f"/assignments/{self.assignment.id}", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["role"], self.assignment_data["role"])

    def test_update_assignment(self):
        updated_data = {
            "project": self.project.id,  
            "user": self.user.id,
            "role": "Lead Developer"
        }
        response = self.client.put(f"/assignments/{self.assignment.id}", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assignment.refresh_from_db()
        self.assertEqual(self.assignment.role, "Lead Developer")

    def test_delete_assignment(self):
        response = self.client.delete(f"/assignments/{self.assignment.id}", format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Assignment.objects.filter(id=self.assignment.id).exists())