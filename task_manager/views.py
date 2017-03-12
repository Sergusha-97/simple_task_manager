from rest_framework import viewsets
from rest_framework import permissions
from task_manager.models import Person, Project, Task
from task_manager.permissions import IsManagerOrReadOnly
from task_manager.serializers import ProjectSerializer, TaskSerializer, UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Person.objects.all()
    serializer_class = UserSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsManagerOrReadOnly,)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsManagerOrReadOnly,)

