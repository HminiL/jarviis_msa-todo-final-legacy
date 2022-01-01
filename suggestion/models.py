from django.db import models
from event.models import User


class SuggestionEvent(models.Model):
    use_in_migrations = True
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    classification = models.CharField(max_length=30)
    title = models.TextField()
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    day = models.IntegerField(null=True)
    time = models.IntegerField(null=True)
    location = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return f'{self.id}, {self.title}, {self.start}, {self.end}'

    class Meta:
        db_table = 'suggestions'





