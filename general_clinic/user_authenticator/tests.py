from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from patient.models import Patient


class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse("client-account-create")
        data = {
            "patient": {
                "address": None,
                "contact_info": None,
                "date_of_birth": "1995-1-04",
            },
            "password": "Keydonkey1",
            "email": "waheedkhaled95@gmail.com",
            "first_name": "Waheed",
            "last_name": "Khaled",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patient.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().first_name, "Waheed")

    def test_login_account(self):
        # Create a user to test login
        user = User.objects.create_user(username='testuser', email='test@example.com', password='Testpassword123')
        patient = Patient.objects.create(user=user)

        url = reverse("client-login-view")
        data = {
            "email": "test@example.com",  # Change this to the correct username field used for login
            "password": "Testpassword123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.data)

    def test_delete_account(self):
        # Delete a user to test login
        user = User.objects.create_user(username='testuser', email='test@example.com', password='Testpassword123')
        patient = Patient.objects.create(user=user)
        # Login
        url = reverse("client-login-view")
        data = {
            "email": "test@example.com",  # Change this to the correct username field used for login
            "password": "Testpassword123",
        }
        response = self.client.post(url, data)
        # Include the authorization token in the headers
        token: str = response.data['token']['access']
        auth_headers = {
            'HTTP_AUTHORIZATION': f'Bearer {token}'  # Modify this based on your authentication method
        }
        # Delete
        url = reverse("client-account-delete")  # Replace with your delete account view URL
        response = self.client.delete(url, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 0)  # Verify that the user is deleted
        self.assertEqual(Patient.objects.count(), 0)  # Optionally, check related models deletion

