from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ChatModel(models.Model):
    from_user = models.ForeignKey(User, related_name= "from_user",on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name= "to_user",on_delete=models.CASCADE)
    message = models.TextField()
    to_like = models.BooleanField()
    from_like = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
