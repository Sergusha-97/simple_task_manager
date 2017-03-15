from rest_framework import viewsets
from rest_framework import permissions
from task_manager.routines import send_task_to_user
from task_manager.models import User, Project, Task
from task_manager.permissions import IsManagerOrReadOnly, IsTaskOwnerOrReadOnly, IsSuperUserOrReadOnly
from task_manager.serializers import ManagerSerializer, DeveloperSerializer, ProjectSerializer, \
    DeveloperTaskSerializer, ManagerTaskSerializer


class ManagerViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role=0)
    serializer_class = ManagerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsSuperUserOrReadOnly,)


class DeveloperViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role=1)
    serializer_class = DeveloperSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsManagerOrReadOnly,)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsManagerOrReadOnly,)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsTaskOwnerOrReadOnly,)

    def perform_create(self, serializer):
        task = serializer.save(reporter=self.request.user)
        if not task.is_finished:
            send_task_to_user.delay(task.executor.pk, task.pk, "Added a new task!")

    def perform_update(self, serializer):
        task = serializer.save()
        if task.is_finished:
            send_task_to_user.delay(task.reporter.pk, task.pk, "Task is finished!")

    def get_serializer_class(self):
        if self.request.user.is_anonymous or self.request.user.is_manager():
            return ManagerTaskSerializer
        else:
            return DeveloperTaskSerializer
