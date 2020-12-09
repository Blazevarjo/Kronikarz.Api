from django.contrib.auth import get_user_model
from model_bakery import baker
from rest_framework import status
from rest_framework.test import (
    APIClient,
    APITestCase
)
from pprint import pprint
import json


User = get_user_model()


class TestEventViewsPermission(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username='correctUser', password='StrongPassword123')
        User.objects.create_user(
            username='incorrectUser', password='StrongPassword123')

        self.unauthUser = APIClient()
        self.permittedUser = APIClient()
        self.forbiddenUser = APIClient()

        self.permittedUser.login(
            username='correctUser', password='StrongPassword123')
        self.forbiddenUser.login(
            username='incorrectUser', password='StrongPassword123')

        tree = baker.make('api.FamilyTree', user=User.objects.filter(
            username='correctUser').first())

        persons = baker.make('api.Person', family_tree=tree,
                             _quantity=5,
                             _fill_optional=True, )

        self.event = baker.make(
            'api.Event', person=persons[0], _fill_optional=True)

    def test_user_permission_list_unathorized(self):
        response = self.unauthUser.get('/events/')
        # pprint(json.dumps(response.__dict__['data'], indent=4))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_permission_list_permitted(self):
        response = self.permittedUser.get('/events/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_permission_list_forbidden(self):
        response = self.forbiddenUser.get('/events/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_permission_detail_unathorized(self):
        response = self.unauthUser.get('/events/1/')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_permission_detail_permitted(self):
        response = self.permittedUser.get('/events/1/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_permission_detail_forbidden(self):
        response = self.forbiddenUser.get('/events/1/')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
