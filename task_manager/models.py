from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    MANAGER = 'MG'
    DEVELOPER = 'DEV'
    ROLES = (
        (MANAGER, 'Manager'),
        (DEVELOPER, 'Developer'),
    )
    description = models.CharField(max_length=50, null=False, choices=ROLES,
                                   blank=False, unique=True)


class User(AbstractUser):
    DEFAULT_ROLE_ID = 1
    role = models.ForeignKey(Role, related_name='users', null=False,
                             blank=False, default=DEFAULT_ROLE_ID)  # ON_DELETE


class CommonInfo(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField()
    due_date = models.DateTimeField()

    class Meta:
        abstract = True
        ordering = ('due_date',)


class Task(CommonInfo):
    project = models.ForeignKey('Project', related_name='tasks',
                                on_delete=models.CASCADE)
    executor = models.ForeignKey(User, related_name='tasks',
                                 on_delete=models.PROTECT)
    is_finished = models.BooleanField()


class Project(CommonInfo):
    team = models.ManyToManyField(User, related_name='projects')

