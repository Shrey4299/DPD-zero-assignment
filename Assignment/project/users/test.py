from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

class RegistrationTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')  # Assuming you've named the registration URL pattern as 'register'
        self.login_url = reverse('login')  # Assuming you've named the login URL pattern as 'login'
        self.valid_payload = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'Test@1234',
            'full_name': 'Test User',
            'age': 25,
            'gender': 'male'
        }

    def test_registration(self):
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_with_existing_email(self):
        # First, register a user with the valid payload
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Now, try to register with the same email again
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_existing_username(self):
        # First, register a user with the valid payload
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Now, try to register with the same username again
        self.valid_payload['email'] = 'test2@example.com'  # Change email to be unique
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')  # Assuming you've named the login URL pattern as 'login'
        self.valid_credentials = {
            'username': 'testuser',
            'password': 'Test@1234',
        }

    def test_login(self):
        # First, register a user with the valid payload
        register_url = reverse('register')  # Assuming you've named the registration URL pattern as 'register'
        valid_payload = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'Test@1234',
            'full_name': 'Test User',
            'age': 25,
            'gender': 'male'
        }
        response = self.client.post(register_url, valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Now, try to login with valid credentials
        response = self.client.post(self.login_url, self.valid_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_invalid_credentials(self):
        # First, register a user with the valid payload
        register_url = reverse('register')  # Assuming you've named the registration URL pattern as 'register'
        valid_payload = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'Test@1234',
            'full_name': 'Test User',
            'age': 25,
            'gender': 'male'
        }
        response = self.client.post(register_url, valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Now, try to login with invalid credentials
        invalid_credentials = {
            'username': 'testuser',
            'password': 'InvalidPassword',
        }
        response = self.client.post(self.login_url, invalid_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
