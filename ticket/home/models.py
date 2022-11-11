from django.db import models
from django.contrib.auth.models import User

"""
    Creating two ticket and response models 
    and using the Django user model for authentication
"""

class Ticket(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name='uticket')
    superuser=models.ForeignKey(User,on_delete=models.CASCADE,related_name='sticket')
    title=models.CharField(max_length=50)
    body=models.TextField(max_length=400)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}-{self.body[:30]}'


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Uanswer')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='Tanswer')
    answer = models.ForeignKey('self', on_delete=models.CASCADE, related_name='Answer', blank=True, null=True)
    is_answer = models.BooleanField(default=False)
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}-{self.body[:30]}'

