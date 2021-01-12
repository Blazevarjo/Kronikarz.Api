from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()


class TestRegisterView(APITestCase):
    def setUp(self):
        User.objects.create_user(username='PierwszyUser',
                                 password='PierwszeHaslo123')

    def test_register_user_success(self):
        username = 'NowyUser'
        password = "MocneHaslo"

        response = self.client.post(r'/register/',
                                    {'username': username,
                                     'password': password
                                     })

        user = User.objects.filter(username=username).first()

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(username, user.username)
        self.assertTrue(user.check_password(password))

    def test_register_user_fail_username_unique(self):
        response = self.client.post(r'/register/',
                                    {'username': 'PierwszyUser',
                                     'password': 'PierwszeHaslo123'
                                     })

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
