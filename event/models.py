from datetime import datetime
from django.db import models


class User(models.Model):
    use_in_migrations = True
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'users'


class Event(models.Model):
    use_in_migrations = True
    user_id = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    classification = models.CharField(null=True, max_length=30)
    type = models.CharField(default='user', max_length=30)
    title = models.TextField()
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    location = models.CharField(null=True, max_length=50)
    completion = models.BooleanField(default=False, max_length=30)
    description = models.TextField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'events'

