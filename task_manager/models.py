from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    MANAGER = 0
    DEVELOPER = 1
    ROLES = (
        (MANAGER, 'Manager'),
        (DEVELOPER, 'Developer'),
    )
    role = models.CharField(max_length=10, null=False, blank=False,
                            choices=ROLES, default=MANAGER)

    def is_manager(self):
        return self.role == 0

    def get_absolute_url(self):
        return ('developers/{}' if self.role == User.DEVELOPER else 'managers/{}').format(self.id)


class CommonInfo(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField()
    due_date = models.DateTimeField()

    class Meta:
        abstract = True
        ordering = ('due_date',)

    def __str__(self):
        return self.title


class Task(CommonInfo):
    project = models.ForeignKey('Project', related_name='tasks',
                                on_delete=models.CASCADE)
    executor = models.ForeignKey(User, related_name='tasks',
                                 on_delete=models.PROTECT)
    reporter = models.ForeignKey(User, related_name='controlled_tasks',
                                 on_delete=models.PROTECT)
    is_finished = models.BooleanField()

    def get_absolute_url(self):
        return 'tasks/{}'.format(self.id)


class Project(CommonInfo):
    team = models.ManyToManyField(User, related_name='projects')

    def get_absolute_url(self):
        return 'projects/{}'.format(self.id)
