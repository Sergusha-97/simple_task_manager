from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from task_manager.models import User

MANAGERS_URL = '/managers/'
JSON = 'json'


class ManagerTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = User.objects.create(username='sergey', email='sergey@admin.com', role=User.MANAGER)
        cls.superuser.is_superuser = True
        cls.superuser.set_password('admin2017')
        cls.superuser.save()

        cls.user = User.objects.create(username='dev', email='dev@dev.com',
                                       role=User.MANAGER)
        cls.user.set_password('admin2017')
        cls.user.save()

    def test_post_manager(self):
        client = APIClient()
        client.force_authenticate(user=self.superuser)

        username = 'Dima'
        user = {'username': username, 'first_name': 'Foo',
                'last_name': 'Bar', 'email': 'foo@foo.com',
                'password': 'admin2017', 'role': User.MANAGER}

        response = client.post(MANAGERS_URL, user, format=JSON)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 3)
        self.assertEqual(User.objects.filter(role=User.MANAGER).count(), 3)
        self.assertEqual(User.objects.get(username=username).username, username)

    def test_get_managers(self):
        client = APIClient()
        client.force_authenticate(user=self.superuser)

        response = client.get(MANAGERS_URL, format=JSON)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_manager(self):
        client = APIClient()
        client.force_authenticate(user=self.superuser)

        url = '{0}2/'.format(MANAGERS_URL)

        response = client.get(url, format=JSON)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_put_manager(self):
        client = APIClient()
        client.force_authenticate(user=self.superuser)

        new_email = 'foo@foo.bar'
        url = '{0}2'.format(MANAGERS_URL)
        user = {"username": 'dev', "email": new_email,
                "password": "admin2017"}

        response = client.put(url, user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], new_email)

    def test_delete_manager(self):
        client = APIClient()
        client.force_authenticate(user=self.superuser)

        url = '{0}2'.format(MANAGERS_URL)

        response = client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
