from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(username, **params):
    return get_user_model().objects.create_user(username=username, **params)


class PublicUserApiTests(TestCase):
    """Test the users API(public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating using with valid payload is successful"""
        payload = {
            'email': 'test@andela.com',
            'password': 'tesnovak',
            'username': 'Ndemo'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        payload = {
            'email': 'test@andela.com',
            'password': 'tesnovak',
            'username': 'novak'
        }

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Password more than two character"""
        payload = {
            'email': 'onkundi@gmail.com',
            'password': 'nv'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """token created for user"""
        payload = {
            "email": "ndemokelvin@gmail.com",
            "username": "onkundi",
            "password": "aubameyang"
        }

        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credential(self):
        """test that token is not created if invalid credential are given"""
        create_user = ({
            'email': 'ndemo@gmail.com',
            'username': 'onkundi254',
            'password': 'aubameyang'
        })

        payload = {
            'email': 'ndemo@gmail.com',
            'username': 'onkundi254',
            'password': 'ndjsdksdshdshds'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test token not created if no user exists"""
        payload = {
            'email': 'ndemokelvin@gmail.com',
            'username': 'onkundi',
            'password': 'ndkdwhnd'

        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """test email and password are required"""
        res = self.client.post(TOKEN_URL, {
            'email': 'ndemokelvin@gmail.com',
            'username': 'onkundi',
            'password': ''

        })
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
