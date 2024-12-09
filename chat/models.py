from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.
from  enums import *
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import AbstractUser
from django.db import models

class UserProfile(AbstractUser):
    profile_image = models.ImageField(
        verbose_name='Profile Picture',
        upload_to='user_profile',
        null=True,  # Make profile_image optional
        blank=True
    )
    bio = models.CharField(max_length=255, blank=True)
    dob = models.DateField(null=True, blank=True)
    nick_name = models.CharField(max_length=40, blank=True)

    # Overriding the default reverse relationships to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='userprofile_set',  # Renaming reverse relation for groups
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='userprofile_set',  # Renaming reverse relation for user_permissions
        blank=True,
        help_text='Specific permissions for this user.'
    )

    def __str__(self):
        return self.username  # Or you can return any field like full_name, etc.


class ChatModel(models.Model):
    from_user = models.ForeignKey(UserProfile, related_name= "from_user",on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserProfile, related_name= "to_user",on_delete=models.CASCADE)
    message = models.TextField()
    to_like = models.BooleanField()
    from_like = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)




class FriendsModel(models.Model):
    user1 = models.ForeignKey(UserProfile, related_name="user1_connections", on_delete=models.CASCADE)
    user2 = models.ForeignKey(UserProfile, related_name="user2_connections", on_delete=models.CASCADE)
    is_friend = models.BooleanField(default=False)
    is_requested = models.CharField(max_length=10,choices=request_status,default="Request")
    is_blocked = models.BooleanField(default=False)
    requsted_timeStamp = models.DateTimeField(auto_now_add=True)
    modified_timeStamp = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user1', 'user2'], name='unique_friendship')
        ]

    def save(self, *args, **kwargs):
        # Enforce no duplicate or reversed duplicate
        if self.user1 == self.user2:
            raise ValueError("A user cannot be friends with themselves.")
        if FriendsModel.objects.filter(user1=self.user2, user2=self.user1).exists():
            raise ValueError("Duplicate friendship or reversed duplicate detected.")
        super().save(*args, **kwargs)

