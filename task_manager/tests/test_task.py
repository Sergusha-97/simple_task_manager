from datetime import datetime
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from task_manager.models import Project, Task, User

TASKS_URL = '/tasks/'
JSON = 'json'


class TaskTests(APITestCase):
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

        cls.project = Project.objects.create(title='Project', description='Description',
                                             due_date=datetime.now())
        cls.project.team = [cls.manager, cls.developer]
        cls.project.save()

        cls.task = Task.objects.create(title='Task', description='Description',
                                       due_date=datetime.now(), is_finished=False,
                                       executor=cls.developer, project=cls.project,
                                       reporter=cls.manager)
        cls.task.save()

    def test_post_task(self):
        client = APIClient()
        client.force_authenticate(user=self.manager)

        task = {'title': 'Task1', 'description': 'Task description',
                'reporter': self.manager.pk, 'executor': self.developer.pk,
                'due_date': datetime.now(), 'is_finished': False, 'project': self.project.pk}

        response = client.post(TASKS_URL, task, format=JSON)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_get_tasks(self):
        client = APIClient()
        client.force_authenticate(user=self.manager)

        response = client.get(TASKS_URL, format=JSON)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_task(self):
        client = APIClient()
        client.force_authenticate(user=self.manager)

        url = '{0}1/'.format(TASKS_URL)

        response = client.get(url, format=JSON)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task.title)

    def test_put_task(self):
        client = APIClient()
        client.force_authenticate(user=self.manager)

        new_description = 'New task description'
        task = {'title': 'Task1', 'description': new_description,
                'reporter': self.manager.pk, 'executor': self.developer.pk,
                'due_date': datetime.now(), 'is_finished': False, 'project': self.project.pk}

        url = '{0}1/'.format(TASKS_URL)

        response = client.put(url, task, format=JSON)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], new_description)

    def test_delete_task(self):
        # Arrange
        client = APIClient()
        client.force_authenticate(user=self.manager)

        url = '{0}1/'.format(TASKS_URL)

        response = client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
