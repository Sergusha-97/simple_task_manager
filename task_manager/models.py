from django.db import models


class CommonInfo(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField()
    due_date = models.DateTimeField()

    class Meta:
        abstract = True


class Task(CommonInfo):
    project = models.ForeignKey(Project, related_name="tasks", on_delete=models.CASCADE)
    executor = models.ForeignKey(Person, related_name="tasks", on_delete=models.PROTECT)
    is_finished = models.BooleanField()


class Project(CommonInfo):
    team = models.ManyToManyField(Person, related_name="projects")


class Person(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    role = models.ForeignKey(Role, related_name="users")  # ON_DELETE


class Role(models.Model):
    MANAGER = "MG"
    DEVELOPER = "DEV"
    ROLES = (
        (MANAGER, "Manager"),
        (DEVELOPER, "Developer"),
    )
    description = models.CharField(max_length=50, null=False, choices=ROLES)


