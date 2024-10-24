from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from roadmapapi.models import Project  

class ProjectViewSetTests(APITestCase):
    def setUp(self):

        self.user = User.objects.create_user(username="projectuser", password="password123")
        

        self.project_data = {
            "name": "Test Project",
            "description": "A test project description",
            "owner": self.user,  
            "deadline": "2024-12-31",
        }
        self.project = Project.objects.create(**self.project_data)
        
        self.client.force_authenticate(user=self.user)

    def test_list_projects(self):
        response = self.client.get("/projects", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_project(self):
        response = self.client.get(f"/projects/{self.project.id}", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.project_data["name"])
        self.assertEqual(response.data["description"], self.project_data["description"])

    def test_update_project(self):
        updated_data = {
            "name": "Updated Project Name",
            "description": "Updated project description",
            "owner": self.user.id,  
            "deadline": "2025-01-01",
        }
        response = self.client.put(f"/projects/{self.project.id}", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, "Updated Project Name")
        self.assertEqual(self.project.description, "Updated project description")

    def test_delete_project(self):
        response = self.client.delete(f"/projects/{self.project.id}", format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Project.objects.filter(id=self.project.id).exists())