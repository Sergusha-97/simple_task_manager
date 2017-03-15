from datetime import datetime
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from task_manager.models import User, Project

PROJECTS_URL = '/projects/'
JSON = 'json'


class ProjectTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manager = User.objects.create(username='sergey', email='sergey@user.com',
                                          role=User.MANAGER)
        cls.manager.set_password('admin2017')
        cls.manager.save()

        cls.developer = User.objects.create(username='dev', email='dev@dev.com',
                                            role=User.DEVELOPER)
        cls.developer.set_password('admin2017')
        cls.developer.save()

        cls.project = Project.objects.create(title='Project', description='Description', due_date=datetime.now())
        cls.project.team = [cls.manager, cls.developer]
        cls.project.save()

    def test_post_project(self):
        client = APIClient()
        client.force_authenticate(user=self.manager)

        project = {'title': 'Project', 'description': 'Project description',
                   'team': [self.manager.pk, self.developer.pk], 'due_date': datetime.now()}

        response = client.post(PROJECTS_URL, project, format=JSON)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)

    def test_get_projects(self):
        client = APIClient()
        client.force_authenticate(user=self.manager)

        response = client.get(PROJECTS_URL, format=JSON)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_project(self):
        client = APIClient()
        client.force_authenticate(user=self.manager)

        url = '{0}1/'.format(PROJECTS_URL)

        response = client.get(url, format=JSON)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.project.title)

    def test_put_project(self):
        client = APIClient()
        client.force_authenticate(user=self.manager)

        new_description = 'new description'
        project = {'title': 'NewProject', 'description': new_description,
                   'team': [self.manager.pk, self.developer.pk], 'due_date': datetime.now()}

        url = '{0}1/'.format(PROJECTS_URL)

        response = client.put(url, project, format=JSON)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], new_description)

    def test_delete_project(self):
        client = APIClient()
        client.force_authenticate(user=self.manager)

        url = '{0}1/'.format(PROJECTS_URL)

        response = client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
