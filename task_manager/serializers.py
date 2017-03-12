from django.contrib.auth.models import User
from rest_framework import serializers
from task_manager.models import Person, Role, Task, Project


class UserSerializer(serializers.HyperlinkedModelSerializer):
    role = serializers.ReadOnlyField(source='Person.role.description')
    projects = serializers.HyperlinkedRelatedField(many=True, view_name='project_detail', queryset=Project.objects.all())
    tasks = serializers.HyperlinkedRelatedField(many=True, view_name='task_detail', queryset=Task.objects.all())

    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'role', 'projects', 'tasks',)


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'url', 'title', 'description', 'due_time',
                  'is_finished', 'executor', 'projects')


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    tasks = serializers.HyperlinkedRelatedField(many=True, view_name='person_detail', queryset=Task.objects.all())

    class Meta:
        model = Task
        fields = ('id', 'url', 'title', 'description',
                  'due_time', 'team', 'tasks')