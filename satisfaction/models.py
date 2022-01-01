from django.db import models
from event.models import User
from suggestion.models import SuggestionEvent


class Satisfaction(models.Model):
    use_in_migrations = True
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    title = models.TextField(null=True)
    type = models.CharField(max_length=30)
    result = models.CharField(max_length=30)
    #accept #reject

    def __str__(self):
        return f'[{self.pk}] \n {self.user} \n {self.created} \n {self.type}\n' \
               f'{self.result} 등 입력 완료'

    class Meta:
        db_table = 'satisfaction'

