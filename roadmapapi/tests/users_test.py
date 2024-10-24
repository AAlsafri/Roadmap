from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserViewSetTests(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "password": "testpassword"  
        }

        self.user = User.objects.create_user(**self.user_data)
        
        self.token = Token.objects.create(user=self.user)
        self.authenticate()

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_list_users(self):
        response = self.client.get("/users", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_user(self):
        response = self.client.get(f"/users/{self.user.id}", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["username"], self.user_data["username"])
        self.assertEqual(response.data["first_name"], self.user_data["first_name"])
        self.assertEqual(response.data["last_name"], self.user_data["last_name"])

    def test_update_user(self):
        updated_data = {
            "username": self.user_data["username"],
            "first_name": "UpdatedFirstName",
            "last_name": "UpdatedLastName",
            "password": self.user_data["password"]  
        }
        response = self.client.put(f"/users/{self.user.id}", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "UpdatedFirstName")
        self.assertEqual(self.user.last_name, "UpdatedLastName")

    def test_delete_user(self):

        response = self.client.delete(f"/users/{self.user.id}", format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())