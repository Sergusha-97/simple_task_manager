from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from task_manager.models import Task, Project, User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    projects = serializers.PrimaryKeyRelatedField(many=True,
                                                  read_only=True)
    password = serializers.CharField(allow_blank=False, write_only=True, style={'input_type': 'password'})

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role'],
        )
        return user

    def update(self, instance, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)


class ManagerSerializer(UserSerializer):
    controlled_tasks = serializers.PrimaryKeyRelatedField(many=True,
                                                          read_only=True)
    role = serializers.HiddenField(default=User.MANAGER)

    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'first_name', 'last_name',
                  'email', 'password', 'role', 'projects', 'controlled_tasks',)


class DeveloperSerializer(UserSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    role = serializers.HiddenField(default=User.DEVELOPER)

    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'first_name', 'last_name',
                  'email', 'password', 'projects', 'tasks', 'role')


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    reporter = serializers.PrimaryKeyRelatedField(read_only=True)


class DeveloperTaskSerializer(TaskSerializer):
    executor = serializers.PrimaryKeyRelatedField(read_only=True)
    project = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'url', 'title', 'description', 'due_date',
                  'is_finished', 'executor', 'reporter', 'project')
        read_only_fields = ('id', 'url', 'title', 'description', 'due_date',
                            'executor', 'reporter', 'project')


class ManagerTaskSerializer(TaskSerializer):
    executor = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role=User.DEVELOPER))
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = Task
        fields = ('id', 'url', 'title', 'description', 'due_date',
                  'is_finished', 'executor', 'reporter', 'project')


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    tasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    team = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, write_only=True)
    managers = serializers.SerializerMethodField()
    developers = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'url', 'title', 'description',
                  'due_date', 'team', 'tasks', 'managers', 'developers')

    def get_managers(self, obj):
        return [user.id for user in obj.team.filter(role=User.MANAGER)]

    def get_developers(self, obj):
        return [user.id for user in obj.team.filter(role=User.DEVELOPER)]
