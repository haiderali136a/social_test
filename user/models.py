from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    username = models.CharField(
        max_length=50,
        unique=True,
        error_messages={
            'unique': "username already exists!",
        },
    )
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "email already exists!",
                              })
    gender = models.CharField(max_length=20, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=75, blank=False)
    last_name = models.CharField(max_length=75, blank=False)
    status = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["date_of_birth"]

    def __unicode__(self):
        return self.email
