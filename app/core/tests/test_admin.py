from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):

    # create a function that is run before every test is run ---> setup func

    def setUp(self):

        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='ndemoo@gmail.com',
            password='test12345'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            'ndemo@gmail.com',
            'aubameyang'
        )

    def test_users_listed(self):
        """Test that users are listed on user Page"""

        # we use reverse so that we do not have to update in the future
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        # check that response contains a certain item and http response is 200
        self.assertContains(res, self.user.username)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that user edit change works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        # /admin/core/user/<int:id>
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
