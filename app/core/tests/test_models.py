from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):

    def test_create_user_email_successful(self):
        """ Test creating a new user with an email is successful """

        email = 'kelvin.onkundi@novak.com'
        password = 'testpass123'
        user = (get_user_model().objects.
                create_user(email=email, password=password))

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = "test@ONKUNDINDEMO.COM"
        user = get_user_model().objects.create_user(email, 'novak254')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating new user without email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_super_user_is_created(self):
        """Test creating a new super user"""
        user = get_user_model().objects.create_superuser('ndemo@gmail',
                                                         'novak')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
