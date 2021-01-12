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


def set_up_users(self):
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


class TestEventViewsPermission(APITestCase):
    def setUp(self):
        set_up_users(self)

        baker.make('api.Event',
                   person__family_tree__user=User.objects.filter(
                       username='correctUser').first(),
                   _fill_optional=True)

    def test_user_permission_list_unathorized(self):
        response = self.unauthUser.get('/events/')
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


class TestFamilyTreeViewsPermission(APITestCase):
    def setUp(self):
        set_up_users(self)
        baker.make('api.FamilyTree',
                   user=User.objects.filter(username='correctUser').first())

    def test_user_permission_list_unathorized(self):
        response = self.unauthUser.get('/family-trees/')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_permission_list_permitted(self):
        response = self.permittedUser.get('/family-trees/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_permission_list_forbidden(self):
        response = self.forbiddenUser.get('/family-trees/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_permission_detail_unathorized(self):
        response = self.unauthUser.get('/family-trees/1/')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_permission_detail_permitted(self):
        response = self.permittedUser.get('/family-trees/1/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_permission_detail_forbidden(self):
        response = self.forbiddenUser.get('/family-trees/1/')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class TestMariageViewsPermission(APITestCase):
    def setUp(self):
        set_up_users(self)
        baker.make('api.Mariage',
                   person_1__family_tree__user=User.objects.filter(
                       username='correctUser').first(),
                   _fill_optional=True)

    def test_user_permission_list_unathorized(self):
        response = self.unauthUser.get('/mariages/')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_permission_list_permitted(self):
        response = self.permittedUser.get('/mariages/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_permission_list_forbidden(self):
        response = self.forbiddenUser.get('/mariages/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_permission_detail_unathorized(self):
        response = self.unauthUser.get('/mariages/1/')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_permission_detail_permitted(self):
        response = self.permittedUser.get('/mariages/1/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_permission_detail_forbidden(self):
        response = self.forbiddenUser.get('/mariages/1/')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class TestMediaViewsPermission(APITestCase):
    def setUp(self):
        set_up_users(self)
        baker.make('api.Media',
                   person__family_tree__user=User.objects.filter(
                       username='correctUser').first(),
                   _fill_optional=True,
                   _create_files=True)

    def test_user_permission_list_unathorized(self):
        response = self.unauthUser.get('/medias/')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_permission_list_permitted(self):
        response = self.permittedUser.get('/medias/')
        pprint(json.dumps(response.__dict__['data'], indent=4))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_permission_list_forbidden(self):
        response = self.forbiddenUser.get('/medias/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_permission_detail_unathorized(self):
        response = self.unauthUser.get('/medias/1/')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_permission_detail_permitted(self):
        response = self.permittedUser.get('/medias/1/')
        pprint(json.dumps(response.__dict__['data'], indent=4))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_permission_detail_forbidden(self):
        response = self.forbiddenUser.get('/medias/1/')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class TestPersonViewsPermission(APITestCase):
    def setUp(self):
        set_up_users(self)
        baker.make('api.Person',
                   id=1,
                   family_tree__user=User.objects.filter(
                       username='correctUser').first(),
                   _fill_optional=True)

    def test_user_permission_list_unathorized(self):
        response = self.unauthUser.get('/persons/')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_permission_list_permitted(self):
        response = self.permittedUser.get('/persons/')
        pprint(json.dumps(response.__dict__['data'], indent=4))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_permission_list_forbidden(self):
        response = self.forbiddenUser.get('/persons/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_permission_detail_unathorized(self):
        response = self.unauthUser.get('/persons/1/')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_permission_detail_permitted(self):
        response = self.permittedUser.get('/persons/1/')
        pprint(json.dumps(response.__dict__['data'], indent=4))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_permission_detail_forbidden(self):
        response = self.forbiddenUser.get('/persons/1/')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
